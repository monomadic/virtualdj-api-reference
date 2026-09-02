#!/usr/bin/env python3
"""Probe verb tails in EXECUTE position, where the query path is blind.

Why this exists: `deck all` broadcasts to every deck when executed, yet in query
position it silently collapses to deck 1 and reads exactly like a bare call.
32,376 queries could not see it; one execute did. Every negative verdict in
tests/verb-arg-forms.json inherits that blindness, so a token being
"indistinguishable-from-nonsense" under /query is weaker evidence than it looks.

The observable is the verb's own state, read back independently (Evidence
Standards rule 4) — never the return value of the call that made the change.

THE OBSERVABLE IS ALSO THIS TOOL'S LIMIT. It can only see a token that changes
what the verb does to its OWN readable state. A token that steers how an action
runs, or that touches different state, is invisible here and will be reported
`tail-ignored-in-execute` — which means "not visible in this observable", never
"not a parameter". `auto_bpm_transition source_original` is the type case: the
official appendix documents it as forcing which BPM the transition lands on,
while this tool watches a boolean saying whether a transition is running, so it
scored identically to junk. Verbs whose tail selects a mode or a target need an
observable chosen for that tail.

The method is TWO BASELINES, and it is what makes a real argument separable from
an ignored one. A bare toggle flips, so from a single baseline `beatlock on` and
`beatlock <garbage>` both end up on and look identical. Run each form from both
baselines and the signatures diverge:

    from off / from on
    on      -> (on,  on)     the token sets a value
    off     -> (off, off)    the token sets the other value
    garbage -> (on,  off)    the token is discarded and the verb just flips

Safety. Executing arbitrary VDJScript against a live instance can destroy work,
so the target list is an allowlist, never a sweep:

  * `executes` AND queries — no readback, no probe
  * family toggle or slider — a value that can be put back
  * a name deny-list (delete/save/load/record/crash/...) and a category
    deny-list (browser, database, system, cues, ...)
  * an audible deny-list on top: nothing that moves volume, faders, mics,
    playback, stems or prelisten, so a live set is not interrupted

Every form restores the value it found and VERIFIES the restore; a failed
restore aborts the whole run rather than continuing to write.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import Channel, FixtureError, is_error  # noqa: E402
from probe_arg_forms import CONTROLS, shared_lexicon  # noqa: E402

CONTRACTS = "tests/action-contracts.json"
VERB_TABLE = "tests/verb-table.json"
ARTIFACT = "tests/verb-execute-forms.json"

DENY_NAME = re.compile(
    r"(crash|close|quit|exit|delete|remove|clear|erase|reset|save|write|export|import|rename|"
    r"reveal|edit|load|unload|record|broadcast|stream|publish|send|post|upload|download|purchase|"
    r"buy|license|login|logout|sandbox|database|file|folder|list|playlist|tag|comment|lyric|"
    r"karaoke|update|install|restart|shutdown|sleep|netsearch|cloud|server|mail|share|print|"
    r"system|script|plugin|skin|window|dialog|popup|menu|wizard|settings?|config|options)")
DENY_AUDIBLE = re.compile(
    r"(volume|gain|level|crossfader|fader|mute|mic|balance|mono|headphone|booth|reverse|dump|"
    r"automix|relay|scratch|slip|hold|vinyl|pitch|key|eq_|equalizer|filter|echo|play|cue|loop|"
    r"sampler|video|master|aux|linein|dualdeck|power|stem|preview|prelisten|effect|"
    r"colorfx|fx|flip|deck)")
DENY_CATEGORY = {"browser", "record", "sandbox", "system", "macro", "plugins", "skin", "window",
                 "karaoke", "text", "variables", "defines", "param", "flow", "repeat", "poi",
                 "cues", "timecode", "rane"}

SLIDER_BASELINES = ("0%", "100%")
TOGGLE_BASELINES = ("off", "on")


def targets(contracts: dict, table: dict, want: list[str] | None, audible: bool) -> dict:
    verbs = contracts["verbs"]
    categories = table["verbs"]  # NOT `table` — the artifact wraps them in "verbs"
    if not any(v.get("category") for v in categories.values()):
        sys.exit("verb table carries no categories — the category deny-list would be inert")
    out = {}
    for name, rec in verbs.items():
        if not (rec["executes"] and (rec["queries"] or rec["query_bool"])):
            continue
        if rec.get("family") not in ("toggle", "slider"):
            continue
        if DENY_NAME.search(name):
            continue
        if not audible and DENY_AUDIBLE.search(name):
            continue
        if categories.get(name, {}).get("category") in DENY_CATEGORY:
            continue
        out[name] = {"family": rec["family"],
                     "candidates": sorted(dict.fromkeys(rec.get("keyword_candidates") or []))}
    if want:
        missing = [w for w in want if w not in out]
        if missing:
            sys.exit(f"not allowlisted for execute probing: {', '.join(missing)}")
        out = {k: v for k, v in out.items() if k in want}
    return out


def restore_form(family: str, value: str) -> str | None:
    """The tail that puts `value` back, or None if it cannot be expressed."""
    if is_error(value) or value == "":
        return None
    if family == "toggle":
        return {"yes": "on", "no": "off", "on": "on", "off": "off"}.get(value.lower())
    return value  # sliders echo a form they accept ("0.5", "50%")


def set_baseline(channel: Channel, verb: str, family: str, baseline: str) -> str:
    channel.execute(f"{verb} {baseline}")
    return channel.query(verb)


def probe(channel: Channel, verb: str, spec: dict, forms: list[tuple[str, ...]],
          verbose: bool) -> dict:
    family = spec["family"]
    baselines = TOGGLE_BASELINES if family == "toggle" else SLIDER_BASELINES
    original = channel.query(verb)
    restore = restore_form(family, original)
    if restore is None:
        return {"skipped": f"cannot express a restore for {original!r}"}

    other = {"yes": "off", "no": "on"}.get(original.lower()) if family == "toggle" else None
    if other:
        channel.execute(f"{verb} {other}")
        moved = channel.query(verb)
        channel.execute(f"{verb} {restore}")
        if channel.query(verb) != original:
            raise FixtureError(
                f"{verb} does not round-trip: set to {other} it read {moved!r} and would not "
                f"return to {original!r}. Left changed by one flip; probing no further.")
        if moved == original:
            return {"skipped": "does not respond to on/off, so no observable to compare"}

    results: dict[str, dict] = {}
    try:
        for form in forms:
            tail = " ".join(form)
            signature = {}
            for baseline in baselines:
                start = set_baseline(channel, verb, family, baseline)
                channel.execute(f"{verb} {tail}".strip())
                signature[baseline] = {"from": start, "to": channel.query(verb)}
            results[tail or "(bare)"] = signature
    finally:
        channel.execute(f"{verb} {restore}")
        back = channel.query(verb)
        if back != original:
            raise FixtureError(
                f"RESTORE FAILED for {verb}: was {original!r}, now {back!r} — aborting "
                f"before any further writes")
    if verbose:
        print(f"    {verb}: restored to {original!r}", file=sys.stderr)
    return {"family": family, "original": original, "signatures": results}


def baselines_value(baseline: str) -> str:
    """What the state reads as after being set to `baseline` (toggles answer yes/no)."""
    return {"on": "yes", "off": "no"}.get(baseline, baseline)


def classify(rec: dict, baselines: tuple[str, ...]) -> dict:
    """A form is execute-recognized when its two-baseline signature differs from garbage."""
    sigs = rec["signatures"]
    controls = [sigs.get(c) for c in CONTROLS if sigs.get(c)]
    if len(controls) < 2 or controls[0] != controls[1]:
        rec["verdict"] = "unstable-controls"
        return rec
    control = controls[0]
    control_shape = tuple(control[b]["to"] for b in baselines)
    recognized, ignored = [], []
    for tail, sig in sigs.items():
        if tail in CONTROLS or tail == "(bare)":
            continue  # bare is the reference, not a candidate token
        shape = tuple(sig[b]["to"] for b in baselines)
        (recognized if shape != control_shape else ignored).append(
            {"tokens": tail.split(),
             "from_baselines": {b: sig[b]["to"] for b in baselines}})
    bare = sigs.get("(bare)")
    rec["bare_shape"] = [bare[b]["to"] for b in baselines] if bare else None
    rec["control_shape"] = list(control_shape)
    # An unrecognized tail suppresses the action entirely — garbage is a no-op,
    # not a flip — so any token that moves the value at all is recognized.
    rec["garbage_is_noop"] = control_shape == tuple(baselines_value(b) for b in baselines)
    rec["recognized"] = recognized
    rec["ignored_count"] = len(ignored)
    rec["verdict"] = "has-execute-tokens" if recognized else "tail-ignored-in-execute"
    return rec


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--verbs", help="comma-separated subset of the allowlist")
    p.add_argument("--lexicon", type=int, nargs="?", const=25, metavar="N",
                   help="also try the N most cross-verb tokens proven real under /query")
    p.add_argument("--include-audible", action="store_true",
                   help="lift the audible deny-list (moves faders, mics, playback) — only on "
                        "an instance nobody is listening to")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--check", action="store_true")
    args = p.parse_args()

    if args.check:
        artifact = Path(ARTIFACT)
        if not artifact.exists():
            print("execute-form probe check skipped: tests/verb-execute-forms.json not collected")
            return 0
        s = json.load(open(artifact))["summary"]
        if s.get("aborted"):
            sys.exit(f"execute-form probe check FAILED: run aborted — {s['aborted']}")
        print(f"execute-form probe check passed: {s['verbs']}/{s['planned']} verbs, "
              f"{s['with_execute_tokens']} with execute-only tokens, "
              f"{s['tail_ignored']} ignoring their tail, {len(s['skipped'])} skipped")
        return 0

    contracts = json.load(open(CONTRACTS))
    table = json.load(open(VERB_TABLE))
    want = [v.strip() for v in args.verbs.split(",")] if args.verbs else None
    plan = targets(contracts, table, want, args.include_audible)

    lexicon = shared_lexicon(Path("tests/verb-arg-forms.json"), args.lexicon) if args.lexicon else []
    for spec in plan.values():
        spec["forms"] = [()] + [(t,) for t in dict.fromkeys(
            spec["candidates"] + lexicon + list(CONTROLS))]

    writes = sum(len(s["forms"]) * 2 * 2 + 2 for s in plan.values())
    print(f"allowlisted verbs: {len(plan)}"
          f"{' (audible deny-list lifted)' if args.include_audible else ''}\n"
          f"forms per verb: {len(next(iter(plan.values()))['forms']) if plan else 0} "
          f"(incl. {len(CONTROLS)} controls)\n"
          f"executes: ~{writes} — every one restored and verified", file=sys.stderr)
    if args.dry_run:
        for name, spec in sorted(plan.items()):
            print(f"   {name:26s} {spec['family']:7s} {spec['candidates']}", file=sys.stderr)
        return 0

    channel = Channel()
    if not channel.reachable():
        raise FixtureError("HTTP channel unreachable — is VirtualDJ running?")

    out, aborted = {}, None
    for i, (name, spec) in enumerate(sorted(plan.items()), 1):
        if not args.quiet:
            print(f"  [{i}/{len(plan)}] {name}", file=sys.stderr)
        try:
            rec = probe(channel, name, spec, spec["forms"], verbose=not args.quiet)
        except FixtureError as exc:
            # Stop writing, but never lose the verbs already measured.
            aborted = f"{name}: {exc}"
            print(f"ABORTED — {aborted}", file=sys.stderr)
            break
        if "skipped" in rec:
            out[name] = rec
            continue
        baselines = TOGGLE_BASELINES if spec["family"] == "toggle" else SLIDER_BASELINES
        out[name] = classify(rec, baselines)

    hits = {v: r["recognized"] for v, r in out.items() if r.get("recognized")}
    json.dump({
        "summary": {
            "verbs": len(out),
            "with_execute_tokens": len(hits),
            "tail_ignored": sum(1 for r in out.values()
                                if r.get("verdict") == "tail-ignored-in-execute"),
            "skipped": {v: r["skipped"] for v, r in out.items() if "skipped" in r},
            "controls": list(CONTROLS),
            "audible_included": args.include_audible,
            "aborted": aborted,
            "planned": len(plan),
        },
        "verbs": out,
    }, sys.stdout, indent=1)
    print(file=sys.stdout)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FixtureError as exc:
        raise SystemExit(f"execute probe aborted: {exc}")
