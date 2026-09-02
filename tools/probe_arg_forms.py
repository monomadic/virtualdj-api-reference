#!/usr/bin/env python3
"""Probe VDJScript verb tails: which trailing tokens a verb actually recognizes.

A verb's tail is whatever follows its name (`get_bpm absolute ghost`). VirtualDJ
receives the whole line as one string and each `ACTION_` class parses its own
remainder, so there is no signature anywhere to read — the only way to learn a
tail's grammar is to compare answers.

Two things make that comparison hard, and this tool is built around both:

1. **A bad tail is silently ignored** (`loaded bogusword` -> `yes`), so "it
   answered" proves nothing. Every candidate is therefore measured against
   NONSENSE CONTROLS. A token that answers differently from garbage is
   recognized; a token that matches garbage is not a token at all. Two
   independent controls must agree with each other, or the reading is discarded
   as unstable rather than reported.
2. **A form can only be told from another in a state where they would
   disagree.** `loaded opposite` says nothing with both decks empty. So every
   probe runs inside each named state from tools/fixtures.py, and a candidate
   counts as recognized if it separates from the controls in ANY state.

Read-only: /query alone, never /execute. Fixture setup is the only thing that
writes, and it restores what it changed.

    python3 tools/probe_arg_forms.py --dry-run          # plan and request count
    python3 tools/probe_arg_forms.py > tests/verb-arg-forms.json
    python3 tools/probe_arg_forms.py --verbs loaded,get_bpm --fixtures one_deck_loaded

Forms are recorded as TOKEN LISTS, never a single argument string, because
whether a verb accepts more than one token is exactly what is unknown.
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import permutations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import (Channel, FixtureError, build_fixtures, ensure_audio,  # noqa: E402
                      establish, is_error, teardown)

CONTRACTS = "tests/action-contracts.json"
VERB_TABLE = "tests/verb-table.json"

# Two unrelated junk tokens. They must agree with each other for a reading to
# count: if garbage A and garbage B disagree, the verb's answer is unstable
# (time-varying, say) and nothing can be concluded from it.
CONTROLS = ("zzqqx", "vfnrbq")

# Fixtures worth sweeping, cheapest first. sampler_slot_loaded asserts a state
# it does not create, so it is a free extra reading rather than a setup step.
DEFAULT_FIXTURES = ("sampler_slot_loaded", "one_deck_loaded", "both_decks_loaded",
                    "deck2_playing", "loop_active", "fx_slot_1_on")


def targets(contracts: dict, table: dict, want: list[str] | None) -> dict[str, list[str]]:
    """verb -> candidate tokens, for every verb worth probing."""
    verbs, summary = contracts["verbs"], contracts["summary"]
    optional = set(summary.get("optional_arg_queries", []))
    real = set(table["verbs"])
    out = {}
    for name, rec in verbs.items():
        if name not in real:
            continue
        cands = rec.get("keyword_candidates") or []
        if name in optional or cands:
            out[name] = sorted(dict.fromkeys(cands))
    if want:
        missing = [w for w in want if w not in out]
        if missing:
            sys.exit(f"not probe targets: {', '.join(missing)}")
        out = {k: v for k, v in out.items() if k in want}
    return out


def forms_for(tokens: list[str], pairs: bool) -> list[tuple[str, ...]]:
    """Bare, each token alone, then ordered pairs — as token tuples."""
    forms: list[tuple[str, ...]] = [()]
    forms += [(t,) for t in tokens]
    if pairs and len(tokens) > 1:
        forms += list(permutations(tokens, 2))
    return forms


def script_for(verb: str, form: tuple[str, ...]) -> str:
    return " ".join((verb,) + form)


def probe_fixture(channel: Channel, plan: dict[str, list[tuple[str, ...]]],
                  fixture_name: str, readings: dict, verbose: bool) -> None:
    """Read every form of every verb once, in the state currently established."""
    for i, (verb, forms) in enumerate(plan.items(), 1):
        for form in forms:
            readings[verb][form][fixture_name] = channel.query(script_for(verb, form))
        for control in CONTROLS:
            readings[verb][("\0control", control)][fixture_name] = channel.query(
                script_for(verb, (control,)))
        if verbose and i % 50 == 0:
            print(f"    {fixture_name}: {i}/{len(plan)} verbs", file=sys.stderr)


def classify(verb_readings: dict, fixtures: list[str]) -> dict:
    """Per form: does it separate from garbage, and where?"""
    control_keys = [("\0control", c) for c in CONTROLS]
    out_forms = []
    for form, by_fixture in verb_readings.items():
        if form in control_keys:
            continue
        separates, unstable, matches_bare = [], [], []
        for fx in fixtures:
            value = by_fixture.get(fx)
            controls = [verb_readings[k].get(fx) for k in control_keys]
            bare = verb_readings.get((), {}).get(fx)
            if value is None or any(c is None for c in controls):
                continue
            if controls[0] != controls[1]:
                unstable.append(fx)
                continue
            if value != controls[0]:
                separates.append(fx)
            if bare is not None and value == bare:
                matches_bare.append(fx)
        if form == ():
            verdict = "bare"
        elif separates:
            verdict = "recognized"
        elif unstable and len(unstable) == len(fixtures):
            verdict = "unstable"
        else:
            verdict = "indistinguishable-from-nonsense"
        rec = {
            "tokens": list(form),
            "verdict": verdict,
            "values": {fx: by_fixture.get(fx) for fx in fixtures if fx in by_fixture},
        }
        if separates:
            rec["separates_in"] = separates
        if unstable:
            rec["unstable_in"] = unstable
        if form != () and matches_bare and len(matches_bare) == len(rec["values"]):
            rec["same_as_bare_everywhere"] = True
        out_forms.append(rec)
    out_forms.sort(key=lambda r: (len(r["tokens"]), r["tokens"]))
    recognized = [r for r in out_forms if r["verdict"] == "recognized"]
    return {
        "forms": out_forms,
        "controls": {c: {fx: verb_readings[("\0control", c)].get(fx) for fx in fixtures
                         if fx in verb_readings[("\0control", c)]} for c in CONTROLS},
        "recognized_tokens": [list(t) for t in sorted(
            {tuple(r["tokens"]) for r in recognized}, key=lambda t: (len(t), t))],
        "multi_token_recognized": any(len(r["tokens"]) > 1 for r in recognized),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--verbs", help="comma-separated subset")
    p.add_argument("--fixtures", default=",".join(DEFAULT_FIXTURES))
    p.add_argument("--no-pairs", action="store_true", help="skip ordered two-token forms")
    p.add_argument("--check", action="store_true")
    p.add_argument("--get", metavar="NAME", help="report one verb from the artifact")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()

    contracts = json.load(open(CONTRACTS))
    table = json.load(open(VERB_TABLE))
    want = [v.strip() for v in args.verbs.split(",")] if args.verbs else None
    cands = targets(contracts, table, want)
    plan = {v: forms_for(t, not args.no_pairs) for v, t in cands.items()}
    fixture_names = [f.strip() for f in args.fixtures.split(",") if f.strip()]

    if args.get:
        artifact = Path("tests/verb-arg-forms.json")
        if not artifact.exists():
            sys.exit("tests/verb-arg-forms.json not collected yet — run "
                     "`just probe-arg-forms` with VirtualDJ up")
        rec = json.load(open(artifact))["verbs"].get(args.get)
        if rec is None:
            print(json.dumps({"name": args.get, "probed": False,
                              "hint": "not an arg-form target (no candidates, needs no args)"},
                             indent=1))
            return 0
        print(json.dumps({"name": args.get, **rec}, indent=1))
        return 0

    if args.check:
        artifact = Path("tests/verb-arg-forms.json")
        if not artifact.exists():
            print("arg-form probe check skipped: tests/verb-arg-forms.json not collected yet")
            return 0
        data = json.load(open(artifact))
        s = data["summary"]
        if s["controls"] != list(CONTROLS):
            sys.exit(f"arg-form probe check FAILED: controls changed {s['controls']}")
        print(f"arg-form probe check passed: {s['verbs']} verbs, {s['forms']} forms, "
              f"{s['recognized_forms']} recognized, fixtures {s['fixtures']}")
        return 0

    forms_total = sum(len(f) for f in plan.values())
    requests = (forms_total + len(plan) * len(CONTROLS)) * len(fixture_names)
    if args.dry_run or not args.quiet:
        print(f"targets: {len(plan)} verbs, {forms_total} forms "
              f"({sum(1 for f in plan.values() for x in f if len(x) == 1)} single-token, "
              f"{sum(1 for f in plan.values() for x in f if len(x) == 2)} ordered pairs)\n"
              f"fixtures: {', '.join(fixture_names)}\n"
              f"requests: {requests} (+ {len(fixture_names)} fixture setups)",
              file=sys.stderr)
    if args.dry_run:
        return 0

    channel = Channel()
    if not channel.reachable():
        raise FixtureError("HTTP channel unreachable on localhost:80 — is VirtualDJ running?")
    track = ensure_audio(verbose=not args.quiet)
    fixtures = build_fixtures(track)
    readings = {v: {f: {} for f in forms} for v, forms in plan.items()}
    for v in readings:
        for c in CONTROLS:
            readings[v][("\0control", c)] = {}

    done: list[str] = []
    for name in fixture_names:
        fixture = fixtures[name]
        if not args.quiet:
            print(f"  establishing {name}", file=sys.stderr)
        before = establish(channel, fixture, verbose=False)
        try:
            probe_fixture(channel, plan, name, readings, verbose=not args.quiet)
            done.append(name)
        finally:
            teardown(channel, fixture, before, verbose=False)

    verbs_out = {v: classify(readings[v], done) for v in plan}
    recognized = sum(1 for v in verbs_out.values()
                     for f in v["forms"] if f["verdict"] == "recognized")
    multi = sorted(v for v, r in verbs_out.items() if r["multi_token_recognized"])
    json.dump({
        "summary": {
            "verbs": len(verbs_out),
            "forms": forms_total,
            "recognized_forms": recognized,
            "verbs_with_recognized_token": sum(1 for r in verbs_out.values()
                                               if r["recognized_tokens"]),
            "multi_token_verbs": multi,
            "fixtures": done,
            "controls": list(CONTROLS),
        },
        "verbs": verbs_out,
    }, sys.stdout, indent=1)
    print(file=sys.stdout)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FixtureError as exc:
        raise SystemExit(f"fixture error: {exc}")
