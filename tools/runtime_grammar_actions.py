"""Stateful, allowlisted H4 comparisons, reached through probe_arg_forms.py.

Only zoom and beatlock writes are permitted. Each observation starts from a
verified baseline and ends with independently verified restoration. A lost
execute response is never retried. Suite predictions are frozen before a run.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import http.client
import json
import math
import time
from pathlib import Path
import urllib.parse

from fixtures import Channel, FixtureError
from runtime_grammar_probes import write_capture

FIXTURES = {
    "parser_zoom_levels": {"queries": ["zoom"], "baselines": [["0.25"], ["0.65"]]},
    "parser_beatlock_levels": {"queries": ["deck 1 beatlock"], "baselines": [["no"], ["yes"]]},
    "parser_all_decks_asymmetric": {
        "queries": [f"deck {d} beatlock" for d in range(1, 5)],
        "baselines": [["no", "yes", "no", "yes"], ["yes", "no", "yes", "no"]]},
}
# Literal tails only; no arbitrary action, chain, parameter expression, or file operation.
TAILS = {"", "on", "off", "toggle", "1", "0", "-1", "+0", "+1", "1.0", "0.0",
         "100%", "25%", "+25%", "-25%", "0.25", "+0.25", "-0.25", "2.0", "-2.0",
         "25 %", "25ms", "25bt", "25MS", "25BT", "0,25", ".25", "1e-1", "0x1",
         "'on'", '"on"', "'default'", "default", "all", "value", "auto",
         "zzqqx", "vvnnz", "#zzqqx", "0.25zzqqx", "0.25 zzqqx", "0.25\t", "0.25\n",
         "`constant 0.25`", "'`constant 0.25`'", "`constant 1`", "'`constant 1`'"}
PREFIXES = {"parser_zoom_levels": "zoom", "parser_beatlock_levels": "deck 1 beatlock",
            "parser_all_decks_asymmetric": "deck all beatlock"}
GUARDS = ["get_decks", "get_deck", "masterdeck_auto"] + [
    f"deck {d} {v}" for d in range(1, 5) for v in ("loaded", "play", "select", "pfl", "masterdeck")]
RESOURCES = ["zoom"] + [f"deck {d} beatlock" for d in range(1, 5)]


class OnceChannel(Channel):
    def execute(self, script):
        time.sleep(0.025)  # Bound mutation bursts; not a retry or a readiness assertion.
        # Do not use Channel._request: it replays on a lost response, which is
        # invalid for toggles and relative actions.
        if self._conn is None:
            self._conn = http.client.HTTPConnection(self.host, self.port, timeout=self.timeout)
        try:
            self._conn.request("GET", "/execute?" + urllib.parse.urlencode({"script": script}))
            return self._conn.getresponse().read().decode(errors="replace").strip()
        except Exception:
            self.close()
            raise


def equal(actual, expected):
    if len(actual) != len(expected):
        return False
    for a, b in zip(actual, expected):
        try:
            if not (math.isfinite(float(a)) and math.isfinite(float(b))) or abs(float(a) - float(b)) > 0.00001:
                return False
        except ValueError:
            if a != b:
                return False
    return True


def validate(suite):
    ids = set()
    for c in suite["cases"]:
        if c["id"] in ids:
            raise ValueError(f"duplicate case id: {c['id']}")
        ids.add(c["id"])
        if c["fixture"] not in FIXTURES:
            raise ValueError(f"unknown fixture: {c['fixture']}")
        f = FIXTURES[c["fixture"]]
        if not c.get("hypothesis") or not c.get("binary_sites"):
            raise ValueError(f"missing hypothesis or binary sites: {c['id']}")
        if len(c["controls"]) != 2 or len(set(c["controls"])) != 2:
            raise ValueError(f"two distinct controls required: {c['id']}")
        variants = [c["script"], *c["controls"], *(x["script"] for x in c["contrasts"])]
        prefix = PREFIXES[c["fixture"]]
        allowed = {prefix + (" " + t if t else "") for t in TAILS}
        if not all(s in allowed for s in variants):
            raise ValueError(f"script outside allowlist: {c['id']}")
        if len(c["expected"]) != len(f["baselines"]):
            raise ValueError(f"expected baseline count mismatch: {c['id']}")
        if not any(x["expected"] != c["expected"] for x in c["contrasts"]):
            raise ValueError(f"no discriminating contrast: {c['id']}")
        for expected in [c["expected"], *(x["expected"] for x in c["contrasts"])]:
            if len(expected) != len(f["baselines"]):
                raise ValueError(f"contrast baseline count mismatch: {c['id']}")
            if not all(len(row) == len(f["queries"]) for row in expected):
                raise ValueError(f"contrast query count mismatch: {c['id']}")
    return suite


def classify(c):
    passes = c["passes"]
    if not passes:
        return "not-run"
    stable = []
    for p in passes:
        out = {}
        for script, baseline_samples in p.items():
            out[script] = []
            for reads in baseline_samples:
                if not reads or any(not equal(r, reads[0]) for r in reads):
                    return "inconclusive-drift"
                out[script].append(reads[0])
        stable.append(out)
    for p in stable[1:]:
        for s in p:
            if any(not equal(a, b) for a, b in zip(p[s], stable[0][s])):
                return "inconclusive-drift"
    values = stable[0]
    if any(not equal(a, b) for a, b in zip(*(values[s] for s in c["controls"]))):
        return "inconclusive-controls"
    for x in c["contrasts"]:
        if any(not equal(a, b) for a, b in zip(values[x["script"]], x["expected"])):
            return "inconclusive-oracle"
    if any(not equal(a, b) for a, b in zip(values[c["script"]], c["expected"])):
        return "prediction-not-held"
    return "held-in-fixture"


class Session:
    def __init__(self, channel, capture, path):
        self.channel, self.capture, self.path = channel, capture, path
        self.original = None
        self.guards = None

    def read(self, queries):
        return [self.channel.query(q) for q in queries]

    def snapshot(self):
        self.guards = self.read(GUARDS)
        g = dict(zip(GUARDS, self.guards))
        if g["get_decks"] != "4" or any(g[f"deck {d} {v}"] != "no"
                for d in range(1, 5) for v in ("loaded", "play")):
            raise FixtureError("requires four unloaded, stopped decks before any mutation")
        self.original = self.read(RESOURCES)
        float(self.original[0])
        if not 0 <= float(self.original[0]) <= 1 or any(v not in ("yes", "no") for v in self.original[1:]):
            raise FixtureError("unrestorable initial readback")
        self.capture["initial_state"] = {"resources": dict(zip(RESOURCES, self.original)),
                                          "guards": g}

    def write(self, script, purpose):
        row = {"script": script, "purpose": purpose, "status": "pending"}
        self.capture["journal"].append(row)
        write_capture(self.path, self.capture)
        try:
            row["response"] = self.channel.execute(script)
            row["status"] = "response-received"
            write_capture(self.path, self.capture)
        except Exception as e:
            row["status"] = "response-uncertain"
            row["error"] = str(e)
            write_capture(self.path, self.capture)
            raise

    def put(self, queries, values, purpose):
        for q, v in zip(queries, values):
            # Absolute forms only for baseline/restore, never toggle.
            if not equal([self.channel.query(q)], [v]):
                tail = (format(float(v), ".9f") if q == "zoom"
                        else {"yes": "on", "no": "off"}[v])
                self.write(q + " " + tail, purpose)
        actual = self.read(queries)
        if not equal(actual, values):
            raise FixtureError(f"{purpose} mismatch: {actual!r} != {values!r}")

    def restore(self):
        self.capture.setdefault("restoration_events", [])
        summary = self.capture.setdefault("summary", {})
        summary["restoration_status"] = "started"
        self.capture["restoration_events"].append({"status": "started"})
        write_capture(self.path, self.capture)
        try:
            self.put(RESOURCES, self.original, "restore")
            actual_guards = self.read(GUARDS)
            if actual_guards != self.guards:
                raise FixtureError("collateral guard changed; aborting rather than guessing restoration")
            restored = {"resources": self.read(RESOURCES),
                        "guards": actual_guards, "verified": True}
            self.capture["restorations"].append(restored)
            self.capture["restoration_events"].append({"status": "success", **restored})
            summary["restoration_status"] = "verified"
            summary["manual_restore_required"] = False
            write_capture(self.path, self.capture)
        except Exception as e:
            self.capture["restoration_events"].append({"status": "failure", "error": str(e)})
            summary["restoration_status"] = "failed"
            summary["manual_restore_required"] = True
            write_capture(self.path, self.capture)
            raise

    def sample(self, fixture, baseline, script, repeat):
        try:
            self.put(fixture["queries"], baseline, "baseline")
            self.capture["baseline_checks"].append({"script": script, "expected": baseline,
                                                       "observed": self.read(fixture["queries"])})
            self.write(script, "probe")
            return [self.read(fixture["queries"]) for _ in range(repeat)]
        finally:
            self.restore()


def run_suite(args):
    suite = validate(json.loads(args.grammar_actions.read_text()))
    if args.check or args.dry_run:
        print(json.dumps({"mode": "allowlisted reversible state comparisons", "fixtures": FIXTURES,
                          "cases": len(suite["cases"])}, indent=2))
        return 0
    if args.rounds < 2 or args.repeat < 2 or not args.out:
        raise ValueError("stateful grammar requires --rounds >= 2 --repeat >= 2 and --out")
    capture = {"summary": {"suite": str(args.grammar_actions), "suite_sha256": hashlib.sha256(
        args.grammar_actions.read_bytes()).hexdigest(), "status": "running", "rounds_requested": args.rounds,
        "rounds_completed": 0, "repeat": args.repeat, "mode": "reversible-actions",
        "claim_scope": "state readback in named fixtures on recorded build only"},
        "fixtures": FIXTURES, "cases": [{**c, "passes": [], "verdict": "not-run"} for c in suite["cases"]],
        "journal": [], "restorations": [], "restoration_events": [], "baseline_checks": []}
    channel = OnceChannel()
    session = Session(channel, capture, args.out)
    try:
        capture["summary"].update(channel.provenance())
        session.snapshot()
        # Test absolute setters and restoration before any candidate is issued.
        for name in sorted({c["fixture"] for c in suite["cases"]}):
            f = FIXTURES[name]
            for b in f["baselines"]:
                try:
                    session.put(f["queries"], b, "roundtrip")
                finally:
                    session.restore()
        for i in range(args.rounds):
            ordered = list(capture["cases"] if i % 2 == 0 else reversed(capture["cases"]))
            scripts_by_fixture = {}
            for c in ordered:
                scripts = scripts_by_fixture.setdefault(c["fixture"], [])
                for script in [*c["controls"], *(x["script"] for x in c["contrasts"]), c["script"]]:
                    if script not in scripts:
                        scripts.append(script)
            samples_by_fixture = {}
            for fixture_name, scripts in scripts_by_fixture.items():
                f = FIXTURES[fixture_name]
                samples_by_fixture[fixture_name] = {
                    script: [session.sample(f, b, script, args.repeat) for b in f["baselines"]]
                    for script in scripts}
            for c in ordered:
                scripts = dict.fromkeys([*c["controls"], *(x["script"] for x in c["contrasts"]), c["script"]])
                c["passes"].append({script: samples_by_fixture[c["fixture"]][script] for script in scripts})
                c["verdict"] = classify(c)
                write_capture(args.out, capture)
            capture["summary"]["rounds_completed"] = i + 1
            if channel.query("get_build") != capture["summary"]["build"]:
                raise FixtureError("build changed")
        session.restore()
        capture["summary"]["status"] = "complete"
    except BaseException as e:
        capture["summary"]["status"] = "aborted"
        capture["summary"]["error"] = str(e)
        capture["summary"].setdefault("restoration_status", "not-started")
        capture["summary"].setdefault("manual_restore_required", False)
        for c in capture["cases"]:
            c["verdict"] = "incomplete-run"
        raise
    finally:
        write_capture(args.out, capture)
        channel.close()
    print(json.dumps(capture["summary"], indent=2))
    return 0


def check_capture(path):
    capture = json.loads(path.read_text())
    s = capture["summary"]
    p = Path(s["suite"])
    suite = validate(json.loads(p.read_text()))
    if hashlib.sha256(p.read_bytes()).hexdigest() != s["suite_sha256"]:
        raise ValueError("suite hash mismatch")
    if s.get("status") not in {"complete", "aborted"}:
        raise ValueError(f"invalid capture status: {s.get('status')!r}")
    if s["rounds_requested"] < 2 or not 0 <= s["rounds_completed"] <= s["rounds_requested"]:
        raise ValueError("invalid round counts")
    if capture["fixtures"] != FIXTURES:
        raise ValueError("fixture definitions changed")
    if len(capture["cases"]) != len(suite["cases"]):
        raise ValueError("case count mismatch")
    for spec, c in zip(suite["cases"], capture["cases"]):
        if not all(c[k] == v for k, v in spec.items()):
            raise ValueError(f"case definition mismatch: {c.get('id')}")
        if s["status"] == "complete" and len(c["passes"]) != s["rounds_requested"]:
            raise ValueError(f"incomplete passes: {c.get('id')}")
        required = {c["script"], *c["controls"], *(x["script"] for x in c["contrasts"])}
        f = FIXTURES[c["fixture"]]
        for p in c["passes"]:
            if set(p) != required:
                raise ValueError(f"script set mismatch: {c['id']}")
            for bs in p.values():
                if len(bs) != len(f["baselines"]) or not all(len(reads) == s["repeat"] >= 2 for reads in bs):
                    raise ValueError(f"sample shape mismatch: {c['id']}")
        if s["status"] == "complete" and c["verdict"] != classify(c):
            raise ValueError(f"verdict mismatch: {c['id']}")
        if s["status"] == "aborted" and c["verdict"] != "incomplete-run":
            raise ValueError(f"aborted case is not incomplete: {c['id']}")
    if not capture.get("initial_state"):
        raise ValueError("missing initial state")
    if s["status"] == "complete" and (not capture.get("restoration_events") or not capture.get("restorations")):
        raise ValueError("missing restoration events")
    if s["status"] == "complete" and s["rounds_completed"] != s["rounds_requested"]:
        raise ValueError("round count incomplete")
    if not all(r.get("verified") and equal(r["resources"], list(capture["initial_state"]["resources"].values()))
               and r["guards"] == list(capture["initial_state"]["guards"].values()) for r in capture["restorations"]):
        raise ValueError("unverified restoration")
    if not all(equal(b["expected"], b["observed"]) for b in capture["baseline_checks"]):
        raise ValueError("baseline mismatch")
    if s["status"] == "complete" and not all(j["status"] == "response-received" for j in capture["journal"]):
        raise ValueError("unfinished journal entry")
    if s["status"] == "complete" and s.get("restoration_status") != "verified":
        raise ValueError("complete capture lacks verified final restoration")
    if s["status"] == "aborted" and s.get("restoration_status") == "failed" and not s.get("manual_restore_required"):
        raise ValueError("failed restoration lacks manual restore marker")
    if s["verdicts"] != dict(Counter(c["verdict"] for c in capture["cases"])):
        raise ValueError("verdict summary mismatch")
    manifest_path = Path("tests/runtime-parser-9246/manifest.json")
    manifest = json.loads(manifest_path.read_text())
    if manifest["source"].get("bundle_version") != "18.0.9246" or manifest["source"].get("architecture") != "x86_64":
        raise ValueError("unexpected runtime parser manifest")
    for symbol in manifest["symbols"].values():
        assembly = manifest_path.parent / symbol["file"]
        if not assembly.is_file() or hashlib.sha256(assembly.read_bytes()).hexdigest() != symbol["asm_sha256"]:
            raise ValueError(f"assembly artifact hash mismatch: {symbol['file']}")
    for case in suite["cases"]:
        for site in case["binary_sites"]:
            name, address = site.rsplit("@", 1)
            if name not in manifest["symbols"]:
                raise ValueError(f"unknown binary site symbol: {site}")
            symbol = manifest["symbols"][name]
            if not int(symbol["start"], 16) <= int(address, 16) < int(symbol["end_exclusive"], 16):
                raise ValueError(f"binary site outside bounded symbol: {site}")
    return capture


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--artifact", type=Path, default=Path("tests/runtime-grammar-actions-9598.json"))
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    c = check_capture(a.artifact) if a.check else json.loads(a.artifact.read_text())
    print(json.dumps(c["summary"], indent=2))
