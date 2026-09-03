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

Separating from nonsense is NOT enough for a two-token form: `is_using loop
zzqqx` separates from garbage purely because `loop` does, with the tail
discarded. So each recognized pair is additionally compared against its own
single-token forms and labelled `first-token-wins`, `last-token-wins`,
`beyond-singles` (a value neither token produces alone — the only real evidence
of two-token grammar) or `singles-agree` (both singles read the same, so the
pair cannot discriminate).

Caveat this design does not fix: a verb whose value drifts on its own — CPU
load, position, level meters — can separate from a control by measurement noise
alone. `--repeat N` reads every form N times and demands agreement; the run
recorded in tests/verb-arg-forms.json used the default of 1, so treat
time-varying verbs (`get_cpu` is the type case) as unproven.
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

# Sentinel written when --repeat reads disagree: the verb answers differently to
# identical questions, so no comparison against it can mean anything.
DRIFTING = "\0drifting"

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
        cands = [c for c in (rec.get("keyword_candidates") or [])
                 if not _looks_like_symbol_fragment(c, verbs)]
        if name in optional or cands:
            out[name] = sorted(dict.fromkeys(cands))
    if want:
        missing = [w for w in want if w not in out]
        if missing:
            sys.exit(f"not probe targets: {', '.join(missing)}")
        out = {k: v for k, v in out.items() if k in want}
    return out


def _looks_like_symbol_fragment(token: str, verbs: dict) -> bool:
    """Drop candidates that are a tail of some `ACTION_<verb>` symbol.

    String recovery off a method body picks up fragments of neighbouring
    symbols: `param_equal` was credited with a keyword `TION_get_text`, which is
    `ACTION_get_text` with the head sheared off. These are never real tokens.
    """
    # The token must reach back INTO the `ACTION_` prefix to be a fragment.
    # A token that merely equals a verb name (`left`, `loop`, `top`) is a
    # perfectly good keyword and must survive.
    return any(f"ACTION_{name}".endswith(token) and len(token) > len(name)
               for name in verbs)


def shared_lexicon(artifact: Path, limit: int) -> list[str]:
    """Tokens already proven real for more than one verb.

    A token that separates from nonsense on two unrelated verbs is part of a
    shared vocabulary, not a quirk of one parser — the best guess available for
    verbs whose own candidates were never recovered.
    """
    if not artifact.exists():
        sys.exit(f"--lexicon needs {artifact}; run the probe first")
    counts: dict[str, int] = {}
    for rec in json.load(open(artifact))["verbs"].values():
        for form in rec["forms"]:
            if len(form["tokens"]) == 1 and form["verdict"] == "recognized":
                counts[form["tokens"][0]] = counts.get(form["tokens"][0], 0) + 1
    shared = [tok for tok, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])) if n > 1]
    return shared[:limit]


def forms_for(tokens: list[str], pairs: bool) -> list[tuple[str, ...]]:
    """Bare, each token alone, then ordered pairs — as token tuples."""
    forms: list[tuple[str, ...]] = [()]
    forms += [(t,) for t in tokens]
    if pairs and len(tokens) > 1:
        forms += list(permutations(tokens, 2))
    return forms


def script_for(verb: str, form: tuple[str, ...]) -> str:
    return " ".join((verb,) + form)


def read_form(channel: Channel, script: str, repeat: int) -> str:
    """Read a form, demanding agreement across `repeat` reads.

    A verb that answers differently to two identical reads is time-varying, and
    no comparison against it means anything — say so rather than record one of
    the values.
    """
    first = channel.query(script)
    for _ in range(repeat - 1):
        if channel.query(script) != first:
            return DRIFTING
    return first


def probe_fixture(channel: Channel, plan: dict[str, list[tuple[str, ...]]],
                  fixture_name: str, readings: dict, verbose: bool,
                  repeat: int = 1) -> None:
    """Read every form of every verb, in the state currently established."""
    for i, (verb, forms) in enumerate(plan.items(), 1):
        for form in forms:
            readings[verb][form][fixture_name] = read_form(
                channel, script_for(verb, form), repeat)
        for control in CONTROLS:
            readings[verb][("\0control", control)][fixture_name] = read_form(
                channel, script_for(verb, (control,)), repeat)
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
            if value == DRIFTING or DRIFTING in controls:
                unstable.append(fx)
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
    _label_pairs(out_forms)
    out_forms.sort(key=lambda r: (len(r["tokens"]), r["tokens"]))
    recognized = [r for r in out_forms if r["verdict"] == "recognized"]
    beyond = [r for r in recognized if r.get("pair_shape") in ("beyond-singles",
                                                               "last-token-wins")]
    return {
        "forms": out_forms,
        "controls": {c: {fx: verb_readings[("\0control", c)].get(fx) for fx in fixtures
                         if fx in verb_readings[("\0control", c)]} for c in CONTROLS},
        "recognized_tokens": [list(t) for t in sorted(
            {tuple(r["tokens"]) for r in recognized}, key=lambda t: (len(t), t))],
        "two_token_grammar": bool(beyond),
        "two_token_forms": [r["tokens"] for r in beyond],
    }


UNDISCERNING_SHARE = 0.5


def _flag_undiscerning(verbs_out: dict) -> set:
    """Strip verbs that "recognize" most of an arbitrary vocabulary.

    The shared lexicon is not tailored to any one verb, so a verb separating
    from nonsense on half of it is not speaking that vocabulary — its answer is
    drifting under the probe (`record_vu` matched 24 of 25 tokens, `pioneer_cue`
    15) and every hit is measurement noise. Same failure as get_cpu, one level
    up: --repeat catches a value that moves between two reads, this catches one
    that moves between a token read and its control.
    """
    flagged = set()
    for verb, rec in verbs_out.items():
        singles = [f for f in rec["forms"] if len(f["tokens"]) == 1]
        hits = [f for f in singles if f["verdict"] == "recognized"]
        if len(singles) >= 10 and len(hits) > UNDISCERNING_SHARE * len(singles):
            flagged.add(verb)
            for form in hits:
                form["verdict"] = "undiscerning"
                form["undiscerning"] = f"{len(hits)}/{len(singles)} of an arbitrary lexicon"
            rec["recognized_tokens"] = []
            rec["two_token_grammar"] = False
            rec["two_token_forms"] = []
    return flagged


def _pair_shape_counts(verbs_out: dict) -> dict:
    from collections import Counter
    c = Counter(f["pair_shape"] for r in verbs_out.values() for f in r["forms"]
                if "pair_shape" in f)
    return dict(sorted(c.items(), key=lambda kv: -kv[1]))


def _label_pairs(out_forms: list[dict]) -> None:
    """A recognized pair means nothing until compared with its own singles."""
    single = {tuple(r["tokens"]): r for r in out_forms if len(r["tokens"]) == 1}
    for rec in out_forms:
        if len(rec["tokens"]) != 2 or rec["verdict"] != "recognized":
            continue
        a, b = (single.get((rec["tokens"][0],)), single.get((rec["tokens"][1],)))
        def same(other):
            return other is not None and all(
                rec["values"].get(fx) == other["values"].get(fx) for fx in rec["values"])
        eq_a, eq_b = same(a), same(b)
        if eq_a and eq_b:
            rec["pair_shape"] = "singles-agree"
        elif eq_a:
            rec["pair_shape"] = "first-token-wins"
        elif eq_b:
            rec["pair_shape"] = "last-token-wins"
        else:
            rec["pair_shape"] = "beyond-singles"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--verbs", help="comma-separated subset")
    p.add_argument("--fixtures", default=",".join(DEFAULT_FIXTURES))
    p.add_argument("--no-pairs", action="store_true", help="skip ordered two-token forms")
    p.add_argument("--from-corpus", action="store_true",
                   help="take candidates from tails Atomix actually wrote in shipped scripts "
                        "(tests/attested-tails.json) — attested forms, so a miss means the "
                        "fixtures cannot see it, not that the token is unreal")
    p.add_argument("--from-catalog", action="store_true",
                   help="take each verb's candidates from the Button Editor catalog's own "
                        "prose (tests/action-catalog.json) instead of the binary — these are "
                        "documented parameters, so a hit confirms and a miss is a real gap")
    p.add_argument("--lexicon", type=int, metavar="N", nargs="?", const=25,
                   help="probe the N most cross-verb tokens already proven real against the "
                        "verbs whose own candidates were never recovered (default 25)")
    p.add_argument("--check", action="store_true")
    p.add_argument("--merge", metavar="FILE",
                   help="fold a targeted re-probe into the artifact, replacing "
                        "those verbs and recording how many reads backed them")
    p.add_argument("--reclassify", action="store_true",
                   help="recompute verdicts from the stored artifact values, "
                        "without touching VirtualDJ")
    p.add_argument("--get", metavar="NAME", help="report one verb from the artifact")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--repeat", type=int, default=1, metavar="N",
                   help="read each form N times and keep the value only if every read "
                        "agrees; guards against verbs whose value drifts on its own")
    args = p.parse_args()

    contracts = json.load(open(CONTRACTS))
    table = json.load(open(VERB_TABLE))
    want = [v.strip() for v in args.verbs.split(",")] if args.verbs else None
    cands = targets(contracts, table, want)
    if args.from_corpus:
        attested = json.load(open("tests/attested-tails.json"))["tails"]
        real = set(table["verbs"])
        cands = {v: sorted(toks) for v, toks in attested.items()
                 if v in real and (not want or v in want)}
        if not args.quiet:
            print(f"corpus-attested tails on {len(cands)} verbs", file=sys.stderr)
    if args.from_catalog:
        catalog = json.load(open("tests/action-catalog.json"))["actions"]
        documented = {v: r["documented_parameters"] for v, r in catalog.items()
                      if r["documented_parameters"]}
        real = set(table["verbs"])
        cands = {v: toks for v, toks in documented.items()
                 if v in real and (not want or v in want)}
        if not args.quiet:
            print(f"catalog-documented parameters on {len(cands)} verbs", file=sys.stderr)
    if args.lexicon:
        lexicon = shared_lexicon(Path("tests/verb-arg-forms.json"), args.lexicon)
        # Only verbs with no vocabulary of their own — the ones the first sweep
        # could do nothing for beyond reading them bare.
        cands = {v: lexicon for v, own in cands.items() if not own} if not want else \
                {v: lexicon for v in cands}
        if not args.quiet:
            print(f"lexicon ({len(lexicon)}): {' '.join(lexicon)}", file=sys.stderr)
    plan = {v: forms_for(t, not args.no_pairs) for v, t in cands.items()}
    fixture_names = [f.strip() for f in args.fixtures.split(",") if f.strip()]

    if args.merge:
        artifact = Path("tests/verb-arg-forms.json")
        base = json.load(open(artifact))
        add = json.load(open(args.merge))
        # More states is more evidence and merges cleanly; a DIFFERENT set does
        # not, because a verdict computed under states the base never saw is not
        # comparable with one it did.
        base_fixtures, add_fixtures = set(base["summary"]["fixtures"]), set(add["summary"]["fixtures"])
        if not base_fixtures <= add_fixtures:
            sys.exit(f"merge refused: the incoming run is missing fixtures the artifact used "
                     f"({sorted(base_fixtures - add_fixtures)}); re-run with a superset")
        base["summary"]["fixtures"] = sorted(add_fixtures, key=lambda f: (f not in base_fixtures, f))
        repeat = add["summary"].get("repeat_reads", 1)
        disputed = set(base["summary"].get("disputed_verbs", []))
        undiscerning = _flag_undiscerning(add["verbs"])
        for verb, rec in add["verbs"].items():
            prior = base["verbs"].get(verb)
            if prior is None:
                rec["repeat_reads"] = repeat
                base["verbs"][verb] = rec
                continue
            # UNION the form lists, never replace. A targeted re-probe covers a
            # narrower set of forms than the sweep it refines (--from-catalog
            # skips pairs entirely), so replacing would silently delete
            # measurements and turn "not probed this time" into "not a token".
            by_tokens = {tuple(f["tokens"]): f for f in prior["forms"]}
            reprobed = {tuple(f["tokens"]): f for f in rec["forms"]}
            # A verdict that flips on a form BOTH runs measured is a real
            # dispute; one the new run never sent is not.
            for tokens, form in reprobed.items():
                was = by_tokens.get(tokens)
                # Separation is positive evidence; failing to separate is not
                # evidence of absence — it usually means this run's states did
                # not discriminate. So a token recognized in ANY run stays
                # recognized, with a note that a later run did not reproduce it.
                if was and was["verdict"] == "recognized" and form["verdict"] != "recognized":
                    was.setdefault("not_reproduced_in", []).append(
                        {"fixtures": add["summary"]["fixtures"],
                         "verdict": form["verdict"]})
                    continue
                if (was and prior.get("repeat_reads", 1) > 1
                        and was.get("pair_shape") and form.get("pair_shape")
                        and was["pair_shape"] != form["pair_shape"]):
                    disputed.add(verb)
                    form["disputed"] = (f"pair shape for {' '.join(tokens)} differed between "
                                        f"runs: {was['pair_shape']} vs {form['pair_shape']}")
                by_tokens[tokens] = form
            merged_forms = sorted(by_tokens.values(),
                                  key=lambda f: (len(f["tokens"]), f["tokens"]))
            recognized = [f for f in merged_forms if f["verdict"] == "recognized"
                          and "disputed" not in f]
            prior.update({
                "forms": merged_forms,
                "controls": {**prior.get("controls", {}), **rec.get("controls", {})},
                "recognized_tokens": [list(x) for x in sorted(
                    {tuple(f["tokens"]) for f in recognized}, key=lambda x: (len(x), x))],
                "two_token_grammar": any(
                    f.get("pair_shape") in ("beyond-singles", "last-token-wins")
                    for f in recognized),
                "repeat_reads": max(prior.get("repeat_reads", 1), repeat),
            })
            prior["two_token_forms"] = [f["tokens"] for f in recognized
                                        if f.get("pair_shape") in ("beyond-singles",
                                                                   "last-token-wins")]
        recognized = sum(1 for r in base["verbs"].values()
                         for f in r["forms"] if f["verdict"] == "recognized")
        base["summary"].update({
            "recognized_forms": recognized,
            "verbs_with_recognized_token": sum(1 for r in base["verbs"].values()
                                               if r["recognized_tokens"]),
            "two_token_grammar_verbs": sorted(v for v, r in base["verbs"].items()
                                              if r["two_token_grammar"]),
            "pair_shapes": _pair_shape_counts(base["verbs"]),
            "confirmed_with_repeat": sorted(v for v, r in base["verbs"].items()
                                            if r.get("repeat_reads", 1) > 1),
            "disputed_verbs": sorted(disputed),
            "undiscerning_verbs": sorted(
                set(base["summary"].get("undiscerning_verbs", [])) | undiscerning),
        })
        artifact.write_text(json.dumps(base, indent=1) + "\n")
        print(f"merged {len(add['verbs'])} verbs read {repeat}x: "
              f"two-token grammar now {base['summary']['two_token_grammar_verbs']}",
              file=sys.stderr)
        return 0

    if args.reclassify:
        artifact = Path("tests/verb-arg-forms.json")
        data = json.load(open(artifact))
        fixtures_done = data["summary"]["fixtures"]
        rebuilt = {}
        for verb, rec in data["verbs"].items():
            readings = {tuple(f["tokens"]): dict(f["values"]) for f in rec["forms"]}
            for control, values in rec["controls"].items():
                readings[("\0control", control)] = dict(values)
            rebuilt[verb] = classify(readings, fixtures_done)
        recognized = sum(1 for r in rebuilt.values()
                         for f in r["forms"] if f["verdict"] == "recognized")
        data["verbs"] = rebuilt
        data["summary"].update({
            "recognized_forms": recognized,
            "verbs_with_recognized_token": sum(1 for r in rebuilt.values()
                                               if r["recognized_tokens"]),
            "two_token_grammar_verbs": sorted(v for v, r in rebuilt.items()
                                              if r["two_token_grammar"]),
            "pair_shapes": _pair_shape_counts(rebuilt),
        })
        data["summary"].pop("multi_token_verbs", None)
        artifact.write_text(json.dumps(data, indent=1) + "\n")
        print(f"reclassified {len(rebuilt)} verbs from stored values: "
              f"{data['summary']['pair_shapes']}", file=sys.stderr)
        return 0

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
            probe_fixture(channel, plan, name, readings, verbose=not args.quiet,
                          repeat=args.repeat)
            done.append(name)
        finally:
            teardown(channel, fixture, before, verbose=False)

    verbs_out = {v: classify(readings[v], done) for v in plan}
    recognized = sum(1 for v in verbs_out.values()
                     for f in v["forms"] if f["verdict"] == "recognized")
    multi = sorted(v for v, r in verbs_out.items() if r["two_token_grammar"])
    json.dump({
        "summary": {
            "verbs": len(verbs_out),
            "forms": forms_total,
            "recognized_forms": recognized,
            "verbs_with_recognized_token": sum(1 for r in verbs_out.values()
                                               if r["recognized_tokens"]),
            "two_token_grammar_verbs": multi,
            "pair_shapes": _pair_shape_counts(verbs_out),
            "repeat_reads": args.repeat,
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
