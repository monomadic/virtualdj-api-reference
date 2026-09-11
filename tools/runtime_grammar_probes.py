"""Exact-script comparisons for probe_arg_forms.py; no execute endpoint.

The suite is a collection of falsifiable predictions, not a language reference.
HTTP results constrain observable output only, not internal parameter types.
"""
from __future__ import annotations

from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path

from fixtures import Channel, FixtureError, build_fixtures, establish


def validate_suite(suite):
    fixtures = build_fixtures(None)
    ids = set()
    for case in suite["cases"]:
        if case["id"] in ids:
            raise ValueError(f"duplicate case: {case['id']}")
        ids.add(case["id"])
        if not case.get("hypothesis") or not case.get("binary_sites"):
            raise ValueError(f"missing hypothesis or binary sites: {case['id']}")
        f = fixtures[case["fixture"]]
        if f.setup or f.teardown or f.decks or f.needs_audio_file:
            raise ValueError("exact-script mode requires a read-only fixture")
        if len(case["controls"]) != 2 or len(set(case["controls"])) != 2:
            raise ValueError("two distinct nonsense controls are required")
        if not case["contrasts"] or not any(
                c["expected"] != case["expected"] for c in case["contrasts"]):
            raise ValueError(f"no discriminating alternative: {case['id']}")
        scripts = [case["script"], *case["controls"],
                   *(c["script"] for c in case["contrasts"])]
        if any(not isinstance(s, str) or not s for s in scripts):
            raise ValueError("scripts must be nonempty strings")
    return suite


def verdict(case, passes):
    """Expected values are frozen before measurement; never inferred from a run."""
    if not passes:
        return "not-run"
    stable = []
    for samples in passes:
        if any(len(set(reads)) != 1 for reads in samples.values()):
            return "inconclusive-drift"
        stable.append({s: reads[0] for s, reads in samples.items()})
    if any(p != stable[0] for p in stable[1:]):
        return "inconclusive-drift"
    values = stable[0]
    if len({values[s] for s in case["controls"]}) != 1:
        return "inconclusive-controls"
    if any(values[c["script"]] != c["expected"] for c in case["contrasts"]):
        return "inconclusive-oracle"
    if values[case["script"]] != case["expected"]:
        return "prediction-not-held"
    return "held-in-fixture"


def write_capture(path, capture):
    capture["summary"]["verdicts"] = dict(Counter(r["verdict"] for r in capture["cases"]))
    data = json.dumps(capture, indent=2, ensure_ascii=True) + "\n"
    if path:
        target = Path(path)
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_text(data)
        temporary.replace(target)
    return data


def run_suite(args):
    suite = validate_suite(json.loads(args.grammar_cases.read_text()))
    if args.check or args.dry_run:
        print(json.dumps({"cases": len(suite["cases"]),
                          "fixtures": sorted({c["fixture"] for c in suite["cases"]}),
                          "mode": "read-only exact scripts",
                          "request_upper_bound": args.rounds * max(2, args.repeat) * sum(
                              3 + len(c["contrasts"]) for c in suite["cases"])}, indent=2))
        return 0
    if args.rounds < 2 or args.repeat < 2:
        raise ValueError("grammar probes require --rounds >= 2 and --repeat >= 2")
    channel = Channel()
    capture = {"summary": {"suite_sha256": hashlib.sha256(
        args.grammar_cases.read_bytes()).hexdigest(), "suite": str(args.grammar_cases),
        "repeat": args.repeat, "rounds_requested": args.rounds,
        "rounds_completed": 0, "status": "running",
        "claim_scope": "exact HTTP outputs in named fixtures; no universal grammar proof"},
        "fixture_checks": [], "cases": [{**c, "passes": [], "verdict": "not-run"}
                                        for c in suite["cases"]]}
    try:
        capture["summary"].update(channel.provenance())
        fixtures = build_fixtures(None)
        for round_index in range(args.rounds):
            # Reverse the second pass to expose order-dependent observations.
            ordered = capture["cases"] if round_index % 2 == 0 else reversed(capture["cases"])
            for name in sorted({c["fixture"] for c in suite["cases"]}):
                fixture = fixtures[name]
                establish(channel, fixture, verbose=False)
                capture["fixture_checks"].append({"round": round_index + 1,
                    "fixture": name, "assertions": [
                        {"script": a.script, "value": channel.query(a.script)}
                        for a in fixture.assertions],
                    "context": {q: channel.query(q) for q in (
                        "deck 1 loaded", "deck 2 loaded", "deck 1 play", "deck 2 play",
                        "get_deck")}})
            for case in ordered:
                scripts = list(dict.fromkeys([*case["controls"],
                    *(c["script"] for c in case["contrasts"]), case["script"]]))
                samples = {}
                for script in scripts:
                    capture["summary"]["pending_query"] = {"case": case["id"],
                        "round": round_index + 1, "script": script}
                    samples[script] = [channel.query(script) for _ in range(args.repeat)]
                case["passes"].append(samples)
                case["verdict"] = verdict(case, case["passes"])
            capture["summary"].pop("pending_query", None)
            capture["summary"]["rounds_completed"] = round_index + 1
            if channel.query("get_build") != capture["summary"]["build"]:
                raise FixtureError("live build changed during capture")
            write_capture(args.out, capture)
        for name in sorted({c["fixture"] for c in suite["cases"]}):
            establish(channel, fixtures[name], verbose=False)
        capture["summary"]["status"] = "complete"
    except Exception as error:
        capture["summary"]["status"] = "aborted"
        capture["summary"]["error"] = str(error)
        for case in capture["cases"]:
            case["verdict"] = "incomplete-run"
        write_capture(args.out, capture)
        raise
    finally:
        channel.close()
    data = write_capture(args.out, capture)
    print(json.dumps(capture["summary"], indent=2) if args.out else data)
    return 0


def check_capture(path):
    capture = json.loads(path.read_text())
    summary = capture["summary"]
    suite_path = Path(summary["suite"])
    suite = validate_suite(json.loads(suite_path.read_text()))
    assert hashlib.sha256(suite_path.read_bytes()).hexdigest() == summary["suite_sha256"]
    assert [c["id"] for c in suite["cases"]] == [c["id"] for c in capture["cases"]]
    assert summary["build"].isdecimal() and summary["channel"] == "HTTP"
    for definition, case in zip(suite["cases"], capture["cases"]):
        assert all(case[k] == v for k, v in definition.items()), case["id"]
        if summary["status"] == "complete":
            assert len(case["passes"]) == summary["rounds_requested"] >= 2
            required = {case["script"], *case["controls"],
                        *(c["script"] for c in case["contrasts"])}
            for samples in case["passes"]:
                assert set(samples) == required
                assert all(len(reads) == summary["repeat"] >= 2 for reads in samples.values())
            assert case["verdict"] == verdict(case, case["passes"]), case["id"]
        else:
            assert case["verdict"] == "incomplete-run", case["id"]
    assert summary["verdicts"] == dict(Counter(c["verdict"] for c in capture["cases"]))
    manifest_path = Path("tests/runtime-parser-9246/manifest.json")
    manifest = json.loads(manifest_path.read_text())
    assert manifest["source"]["bundle_version"] == "18.0.9246"
    assert manifest["source"]["architecture"] == "x86_64"
    for symbol in manifest["symbols"].values():
        assembly = manifest_path.parent / symbol["file"]
        assert hashlib.sha256(assembly.read_bytes()).hexdigest() == symbol["asm_sha256"]
    for case in suite["cases"]:
        for site in case["binary_sites"]:
            name, address = site.rsplit("@", 1)
            symbol = manifest["symbols"][name]
            assert int(symbol["start"], 16) <= int(address, 16) < int(symbol["end_exclusive"], 16), site
    return capture


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path,
                        default=Path("tests/runtime-grammar-confirmation-9598.json"))
    parser.add_argument("--get", metavar="CASE")
    parser.add_argument("--group")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    capture = check_capture(args.artifact) if args.check else json.loads(args.artifact.read_text())
    if args.get:
        selected = [c for c in capture["cases"] if c["id"] == args.get]
        if not selected:
            parser.error(f"unknown case: {args.get}")
        print(json.dumps(selected[0], indent=2))
    elif args.group:
        print(json.dumps([{"id": c["id"], "hypothesis": c["hypothesis"],
                           "script": c["script"], "verdict": c["verdict"],
                           "observed": c["passes"][0][c["script"]] if c["passes"] else []}
                          for c in capture["cases"] if c["group"] == args.group], indent=2))
    else:
        print(json.dumps(capture["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
