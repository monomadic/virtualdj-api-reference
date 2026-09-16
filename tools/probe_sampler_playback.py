#!/usr/bin/env python3
"""Frozen, bounded playback tests on the generated sampler bank.

Starts only owned quiet tones. Reads activity, elapsed position, percent position
and active count independently of execute results. Every case stops its players;
the run restores fixture levels, deck defaults and the original bank. No audio
recording, routing, loop/mode changes, file operations or controller simulation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from fixtures import FixtureError
from probe_sampler_contracts import BANK, ROOT, SLOTS, Runner, quoted

PLAN = ROOT / "tests/sampler-playback-cases.json"
VERBS = {"sampler_play", "sampler_stop", "sampler_play_stop", "sampler_play_stutter"}
OBSERVED = (9, 12)


def load_plan():
    plan = json.loads(PLAN.read_text())
    allowed = {f"{v} {tail}" for v in VERBS for tail in ("9", "all", "zzqqx", "vfnrbq")}
    allowed |= {f"deck 1 {v}" for v in VERBS}
    ids = set()
    for row in plan["cases"]:
        if row["id"] in ids or row["script"] not in allowed or row["verb"] not in VERBS:
            raise FixtureError("invalid or duplicate playback case")
        ids.add(row["id"])
        if row["playing"] not in ([], [9, 12]) or row["expected_active"] not in ([], [9], [12], [9, 12]):
            raise FixtureError("unexpected playback fixture state")
    return plan


class PlaybackRunner(Runner):
    MUTATION_VERBS = Runner.MUTATION_VERBS | VERBS

    def __init__(self, output):
        super().__init__(output)
        self.plan = load_plan()
        self.data.update(kind="sampler-playback", scope=self.plan["scope"],
                         plan_sha256=hashlib.sha256(PLAN.read_bytes()).hexdigest(),
                         audio_observation={"captured": False,
                                            "reason": "No verified loopback route for current speaker output; transport claims only"},
                         readback_scripts={"activity": "sampler_play SLOT", "count": "sampler_used",
                                           "elapsed": "get_sample_info SLOT 'pos'", "position": "sampler_position SLOT"})
        self.epoch = time.monotonic()

    def query(self, script):
        # A stale keep-alive read can consume a sample's entire duration before
        # retrying. Fresh read connections keep timed observations bounded;
        # timestamp checks still reject delayed snapshots.
        self.ch.close()
        return super().query(script)

    def snapshot(self):
        start = time.monotonic() - self.epoch
        slots = {str(s): {"playing": self.query(f"sampler_play {s}")} for s in SLOTS}
        for slot in OBSERVED:
            slots[str(slot)].update(elapsed=self.query(f"get_sample_info {slot} 'pos'"),
                                    position=self.query(f"sampler_position {slot}"))
        counts = {"bare": self.query("sampler_used")}
        for n in range(5):
            counts[str(n)] = self.query(f"sampler_used {n}")
            counts[f"predicate_{n}"] = self.query(f"sampler_used {n} ? constant 1 : constant 0")
        return {"start": round(start, 4), "end": round(time.monotonic() - self.epoch, 4),
                "slots": slots, "counts": counts}

    def stopped(self):
        """Cleanup is explicit slot-stop; never rely on the all form under test."""
        if self.query("get_sampler_bank") != BANK:
            raise FixtureError("fixture bank changed; refusing playback cleanup writes")
        for slot in SLOTS:
            status = self.query(f"sampler_play {slot}")
            if status == "yes":
                self.execute(f"sampler_stop {slot}", "stop-fixture-slot")
            elif status != "no":
                raise FixtureError("no reliable per-slot activity readback")
        deadline = time.monotonic() + 3
        while True:
            state = self.snapshot()
            if (state["counts"]["bare"] == "0"
                    and all(r["playing"] == "no" for r in state["slots"].values())):
                return state
            if time.monotonic() >= deadline:
                raise FixtureError("fixture players did not stop")
            time.sleep(.05)

    def case(self, spec, run):
        row = {"id": spec["id"], "run": run, "script": spec["script"],
               "prediction": {"active": spec["expected_active"], "motion": spec["motion"]},
               "control": spec["control"]}
        self.data["cases"].append(row)
        self.persist()
        try:
            row["initial"] = self.stopped()
            for slot in spec["playing"]:
                self.execute(f"sampler_play {slot}", "establish-players")
            if spec["playing"]:
                time.sleep(1.1 if run == 1 else 1.5)
            row["before"] = self.snapshot()
            active = [int(s) for s, v in row["before"]["slots"].items() if v["playing"] == "yes"]
            if active != spec["playing"] or row["before"]["counts"]["bare"] != str(len(active)):
                raise FixtureError("independent active-player baseline did not establish")
            self.persist()
            row["dispatch_start"] = round(time.monotonic() - self.epoch, 4)
            self.execute(spec["script"], "playback-probe")
            row["dispatch_end"] = round(time.monotonic() - self.epoch, 4)
            row["after"] = self.snapshot()
            time.sleep(.45)
            row["later"] = self.snapshot()
        finally:
            row["restored"] = self.stopped()
            self.persist()

    def count_probe(self, run, playing):
        row = {"run": run, "playing": playing}
        self.data.setdefault("count_probes", []).append(row)
        try:
            row["initial"] = self.stopped()
            for slot in playing:
                self.execute(f"sampler_play {slot}", "establish-count")
            row["after"] = self.snapshot()
            time.sleep(.1)
            row["later"] = self.snapshot()
        finally:
            row["restored"] = self.stopped()
            self.persist()

    def run(self):
        original, levels, selection = None, None, None
        entered = False
        try:
            self.silent()
            decks = int(self.query("get_decks"))
            guards = {f"deck {d} play": self.query(f"deck {d} play") for d in range(1, decks + 1)}
            if any(value != "no" for value in guards.values()):
                raise FixtureError("start playback suite with decks stopped")
            self.data["deck_guard_before"] = guards
            original = {"bank": self.query("get_sampler_bank"), "selection": self.selection()}
            restore_bank = quoted(original["bank"])
            if original["bank"] == BANK or any(
                    not original["selection"][f"deck {d} get_sampler_slot"].isdecimal()
                    or int(original["selection"][f"deck {d} get_sampler_slot"]) < 1 for d in (1, 2)):
                raise FixtureError("start from an original bank with restorable deck defaults")
            entered = True
            self.execute(f"sampler_bank '{BANK}'", "enter-fixture")
            self.data["bank_ready"] = self.wait_bank(BANK)
            self.data["fixture_readback"] = self.fixture()
            levels, selection = self.levels(), self.selection()
            self.data["initial_fixture_levels"] = levels
            self.data["initial_fixture_selection"] = selection
            self.restore_levels({str(s): .1 for s in SLOTS})
            self.data["quiet_levels"] = self.levels()
            self.execute("deck 1 sampler_select 9", "set-fixture-default")
            self.execute("deck 2 sampler_select 12", "set-fixture-default")
            self.data["fixture_defaults"] = self.selection()
            if self.query("deck 1 get_sampler_slot") != "9" or self.query("deck 2 get_sampler_slot") != "12":
                raise FixtureError("distinct sampler defaults did not establish")
            # Calibration is preserved separately. It must prove independent
            # position movement and explicit per-slot stop before the full pass.
            calibration = next(c for c in self.plan["cases"] if c["id"] == "sampler_play-start")
            self.case(calibration, 0)
            from sampler_playback_evidence import classify_case
            if classify_case(self.data["cases"][-1]) != "start":
                raise FixtureError("play/position/stop round-trip did not calibrate")
            for run in self.plan["runs"]:
                for spec in self.plan["cases"]:
                    self.case(spec, run)
                    result = classify_case(self.data["cases"][-1])
                    self.data["cases"][-1]["observed"] = result
                    self.persist()
                # Independent groups avoid exclusivity; slot 1 lasts only 2s,
                # so read these count-only probes immediately, without warmup.
                self.count_probe(run, [5, 9, 12])
                self.count_probe(run, [1, 5, 9, 12])
            self.data["completed"] = True
        except Exception as exc:
            self.data["error"] = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            try:
                if entered and self.query("get_sampler_bank") == BANK:
                    self.data["fixture_stopped"] = self.stopped()
                    if levels is not None:
                        self.data["fixture_levels_restored"] = self.restore_levels(levels)
                    if selection is not None:
                        for deck in (1, 2):
                            slot = selection[f"deck {deck} get_sampler_slot"]
                            self.execute(f"deck {deck} sampler_select {slot}", "restore-selection")
                        self.data["fixture_selection_restored"] = self.selection()
                        if self.data["fixture_selection_restored"] != selection:
                            raise FixtureError("fixture selection restore failed")
            finally:
                try:
                    if entered and original is not None:
                        self.restore_original(original, restore_bank)
                    if "deck_guard_before" in self.data:
                        self.data["deck_guard_after"] = {q: self.query(q) for q in self.data["deck_guard_before"]}
                        if self.data["deck_guard_after"] != self.data["deck_guard_before"]:
                            raise FixtureError("deck transport changed during playback pass")
                finally:
                    self.persist()
                    self.ch.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", action="store_true", help="play quiet owned samples and restore")
    ap.add_argument("--output", type=Path, default=ROOT / "tests/sampler-playback-9598.json")
    args = ap.parse_args()
    if args.run:
        PlaybackRunner(args.output).run()
        print(f"Captured {args.output}")
    else:
        print(json.dumps(load_plan(), indent=2))


if __name__ == "__main__":
    main()
