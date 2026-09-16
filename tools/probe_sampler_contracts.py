#!/usr/bin/env python3
"""Bounded sampler addressing/level contracts on an owned, generated bank.

prepare writes only a NEW fixture directory; run journals each mutation before
dispatch, never retries it, restores every case and the original bank, and keeps
partial captures. No playback, assignment, recording, deletion or library writes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import time
import wave
import xml.etree.ElementTree as ET
from pathlib import Path

from fixtures import FixtureError
from runtime_grammar_actions import OnceChannel

ROOT = Path(__file__).resolve().parents[1]
BANK = "VDJ Contract Fixture"
SLOTS = {1: ("Alpha", "#FF0000"), 2: ("Alpha", "#00FF00"),
         3: ("Alpha", "#0000FF"), 5: ("Beta", "#FFFF00"),
         9: ("", "#00FFFF"), 12: ("Gamma", "#FF00FF")}
LEVELS = {1: .21, 2: .32, 3: .43, 5: .54, 9: .65, 12: .76}
VOLUME_VERBS = ("sampler_volume", "sampler_volume_nogroup", "sampler_group_volume")


def save(path, data):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n")
    tmp.replace(path)


def prepare(path):
    # Never overwrite an installed bank or a user's files.
    path.mkdir(parents=True, exist_ok=False)
    root = ET.Element("samplerbank")
    for slot, (group, color) in SLOTS.items():
        filename = f"ContractTone{slot:02}.wav"
        rate, seconds = 8000, slot + 1
        with wave.open(str(path / filename), "wb") as w:
            w.setparams((1, 2, rate, 0, "NONE", "not compressed"))
            w.writeframes(b"".join(struct.pack("<h", round(1000 * math.sin(
                2 * math.pi * (180 + slot * 30) * i / rate)))
                for i in range(rate * seconds)))
        attrs = {"path": filename, "slot": str(slot - 1), "col": str(slot - 1),
                 "color": color}
        if group:
            attrs["group"] = group
        ET.SubElement(root, "sample", attrs)
    ET.ElementTree(root).write(path / "bank.xml", encoding="utf-8", xml_declaration=True)
    manifest = {"fixture": BANK, "slots": {str(k): {"group": v[0], "color": v[1],
                 "seconds": k + 1} for k, v in SLOTS.items()},
                "files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(path.iterdir())}}
    save(path / "fixture-manifest.json", manifest)
    print(f"Prepared {path}")


def quoted(value):
    # Bank names are runtime data, never arbitrary script fragments.
    if any(c in value for c in "'\"`&\r\n"):
        raise FixtureError("bank name cannot be safely quoted")
    return "'" + value + "'"


def close(a, b):
    try:
        return math.isfinite(float(a)) and abs(float(a) - float(b)) < .0001
    except (ValueError, TypeError):
        return a == b


def same(a, b):
    return a.keys() == b.keys() and all(close(a[k], b[k]) for k in a)


class Runner:
    def __init__(self, output):
        self.output = output
        if output.exists():
            raise FixtureError("capture exists; choose a new output to preserve earlier runs")
        self.ch = OnceChannel()
        self.data = {"schema": 1, "fixture": BANK, "summary": self.ch.provenance(),
                     "scope": "HTTP, stopped generated WAV bank; no pad/controller/audio proof",
                     "journal": [], "cases": [], "queries": [], "restored": False}

    def persist(self):
        save(self.output, self.data)

    def query(self, script):
        time.sleep(.01)
        return self.ch.query(script)

    def execute(self, script, phase):
        # Hard allowlist. Values are generated internally; no arbitrary CLI scripts.
        head = script.split()[0]
        verb = script.split()[2] if head == "deck" else head
        if verb not in {*VOLUME_VERBS, "sampler_bank", "sampler_select"}:
            raise FixtureError(f"mutation not allowlisted: {verb}")
        if verb != "sampler_bank" and phase != "restore-original-selection":
            if self.query("get_sampler_bank") != BANK:
                raise FixtureError("fixture bank changed; refusing sampler mutation")
        row = {"script": "sampler_bank <original-bank>" if phase == "restore-original-bank" else script,
               "phase": phase, "outcome": "pending"}
        self.data["journal"].append(row)
        self.persist()
        try:
            # Avoid inheriting an exhausted HTTP keep-alive connection after a
            # large readback batch. This is a fresh dispatch, never a replay.
            self.ch.close()
            row["response"] = self.ch.execute(script)
            row["outcome"] = "responded"
        except Exception as exc:
            row["outcome"] = "uncertain"
            row["error"] = type(exc).__name__
            raise
        finally:
            self.persist()

    def selection(self):
        return {f"deck {d} {verb}": self.query(f"deck {d} {verb}")
                for d in (1, 2) for verb in ("get_sampler_slot", "sampler_select")}

    def levels(self):
        return {str(s): self.query(f"sampler_volume_nogroup {s}") for s in SLOTS}

    def silent(self):
        if self.query("sampler_used") != "0":
            raise FixtureError("sampler is playing; stopped fixture required")

    def wait_bank(self, expected):
        deadline = time.monotonic() + 5
        attempts = 0
        while True:
            attempts += 1
            if self.query("get_sampler_bank") == expected:
                return {"matches": True, "queries": attempts}
            if time.monotonic() >= deadline:
                return {"matches": False, "queries": attempts}
            time.sleep(.05)

    def selection_probe(self):
        before = self.selection()
        row = {"before": before, "observations": []}
        self.data["selection_probe"] = row
        try:
            for deck, slot in ((1, 2), (2, 5), (1, 9)):
                script = f"deck {deck} sampler_select {slot}"
                self.execute(script, "selection-probe")
                readback = self.selection()
                names = {str(d): self.query(f"deck {d} get_sample_name") for d in (1, 2)}
                row["observations"].append({"script": script, "readback": readback,
                                            "names": names})
                self.persist()
        finally:
            # sampler_select queries a normalized selector, not a slot index.
            # Restore from the independent one-based get_sampler_slot readback.
            for deck in (1, 2):
                value = before[f"deck {deck} get_sampler_slot"]
                if not value.isdecimal():
                    raise FixtureError("selection has no numeric restore value")
                self.execute(f"deck {deck} sampler_select {value}", "restore-selection")
            row["restored"] = self.selection()
            self.persist()
            if row["restored"] != before:
                raise FixtureError("selection restore failed")

    def fixture(self):
        self.silent()
        if self.query("get_sampler_bank") != BANK:
            raise FixtureError("dedicated bank is not selected")
        rows = {}
        for slot in range(1, 14):
            row = {"loaded": self.query(f"sampler_loaded {slot}")}
            if slot in SLOTS:
                row.update(name=self.query(f"get_sample_name {slot}"),
                           group=self.query(f"get_sample_info {slot} 'group'"),
                           length=self.query(f"get_sample_info {slot} 'length'"),
                           color=self.query(f"get_sample_color {slot}"))
                if (row["loaded"] != "yes" or row["name"] != f"ContractTone{slot:02}"
                        or row["group"] != SLOTS[slot][0]):
                    raise FixtureError(f"fixture slot {slot} does not match generated bank: {row}")
            elif row["loaded"] != "no":
                raise FixtureError(f"fixture slot {slot} should be empty")
            rows[str(slot)] = row
        return rows

    def restore_levels(self, expected):
        for slot, value in expected.items():
            if not close(self.query(f"sampler_volume_nogroup {slot}"), value):
                self.execute(f"sampler_volume_nogroup {slot} {value}", "restore-level")
        got = self.levels()
        if not same(got, expected):
            raise FixtureError(f"level restore failed: {got}")
        return got

    def measure(self, script, run, label):
        self.silent()
        before = self.levels()
        row = {"run": run, "script": script, "purpose": label, "before": before,
               "readback": "sampler_volume_nogroup SLOT for every loaded fixture slot"}
        self.data["cases"].append(row)
        self.persist()
        try:
            self.execute(script, "probe")
            row["after"] = self.levels()
            row["changed_slots"] = [s for s in before if not close(before[s], row["after"][s])]
        finally:
            row["restored"] = self.restore_levels(before)
            self.persist()

    def query_matrix(self, run):
        for verb in ("get_sample_name", "sampler_loaded", "sampler_volume",
                     "sampler_volume_nogroup"):
            for tail in ("", "1", "2", "5", "9", "4", "current", "0", "all",
                         "'ContractTone02'", "zzqqx", "vfnrbq"):
                script = (verb + " " + tail).strip()
                self.data["queries"].append({"run": run, "script": script,
                                             "result": self.query(script)})
        for slot in (1, 2, 5, 9, 4):
            for field in ("group", "length", "pos", "zzqqx", "vfnrbq"):
                script = f"get_sample_info {slot} '{field}'"
                self.data["queries"].append({"run": run, "script": script,
                                             "result": self.query(script)})
        self.persist()

    def run(self):
        original = None
        entered = False
        try:
            self.silent()
            original = {"bank": self.query("get_sampler_bank"), "selection": self.selection()}
            # Bank and selection are kept only in this process: no personal bank
            # names or sample metadata in committed captures.
            restore_bank = quoted(original["bank"])
            if any(not original["selection"][f"deck {d} get_sampler_slot"].isdecimal()
                   or int(original["selection"][f"deck {d} get_sampler_slot"]) < 1 for d in (1, 2)):
                raise FixtureError("original deck selections have no absolute-slot restore value")
            if original["bank"] == BANK:
                raise FixtureError("start on the original bank, not the fixture")
            entered = True
            self.execute(f"sampler_bank '{BANK}'", "enter-fixture")
            self.data["bank_ready"] = self.wait_bank(BANK)
            self.data["fixture_readback"] = self.fixture()
            baseline = self.levels()
            self.data["initial_fixture_levels"] = baseline
            try:
                # Round-trip before the suite: prove slot-specific writes and cleanup.
                self.measure("sampler_volume_nogroup 2 0.37", 0, "round-trip")
                first = self.data["cases"][-1]
                if first["changed_slots"] != ["2"] or not close(first["after"]["2"], .37):
                    raise FixtureError("slot-specific setter failed round-trip")
                self.selection_probe()
                for run in (1, 2):
                    wanted = {str(s): v if run == 1 else round(.9 - v, 2)
                              for s, v in LEVELS.items()}
                    self.restore_levels(wanted)
                    self.data.setdefault("baselines", []).append({"run": run, "levels": self.levels()})
                    self.query_matrix(run)
                    for verb in VOLUME_VERBS:
                        tails = (("1 0.61", "numeric slot/group"),
                                 ("1 37%", "percentage value"),
                                 ("1 +5%", "relative value"),
                                 ("current 0.61", "current selector"),
                                 ("all 0.61", "all selector"),
                                 ("zzqqx 0.61", "nonsense selector 1"),
                                 ("vfnrbq 0.61", "nonsense selector 2"))
                        for tail, label in tails:
                            self.measure(f"{verb} {tail}", run, label)
                        target = "'Alpha'" if verb == "sampler_group_volume" else "'ContractTone02'"
                        self.measure(f"{verb} {target} 0.61", run, "named selector")
            finally:
                self.data["fixture_levels_restored"] = self.restore_levels(baseline)
            self.data["completed"] = True
        except Exception as exc:
            self.data["error"] = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            try:
                if original is not None and entered:
                    # Redact only the original bank name, preserving the exact
                    # generated-fixture calls and all experimental readbacks.
                    self.execute(f"sampler_bank {restore_bank}", "restore-original-bank")
                    bank_wait = self.wait_bank(original["bank"])
                    bank_ok = bank_wait["matches"]
                    if bank_ok:
                        for deck in (1, 2):
                            script = f"deck {deck} get_sampler_slot"
                            value = original["selection"][script]
                            if self.query(script) != value:
                                self.execute(f"deck {deck} sampler_select {value}", "restore-original-selection")
                    selection_ok = self.selection() == original["selection"]
                    self.data["original_restoration"] = {"bank_matches": bank_ok,
                                                        "bank_readback_queries": bank_wait["queries"],
                                                        "selection_matches": selection_ok,
                                                        "sampler_used": self.query("sampler_used")}
                    self.data["restored"] = bank_ok and selection_ok and self.data["original_restoration"]["sampler_used"] == "0"
                    if not self.data["restored"]:
                        self.data["restoration_error"] = "original sampler state did not restore"
                        raise FixtureError("original sampler state did not restore")
            finally:
                self.persist()
                self.ch.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    choice = ap.add_mutually_exclusive_group(required=True)
    choice.add_argument("--prepare", type=Path, help="create a new .bank directory")
    choice.add_argument("--run", action="store_true")
    ap.add_argument("--output", type=Path, default=ROOT / "tests/sampler-contracts-9598.json")
    args = ap.parse_args()
    if args.prepare:
        prepare(args.prepare)
    else:
        Runner(args.output).run()
        print(f"Captured {args.output}")


if __name__ == "__main__":
    main()
