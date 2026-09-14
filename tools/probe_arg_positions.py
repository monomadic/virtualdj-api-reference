#!/usr/bin/env python3
"""Which ARGUMENT POSITIONS a verb actually reads.

Every existing prober asks "is this token recognized", one token at a time.
That question is blind to a verb whose keyword lives in the second position:
`get_sample_info <slot> <field>` errors on every single-token probe, real
fields included, so the sweep filed all three documented fields as
indistinguishable from nonsense. They were fine — the shape was wrong.

This asks a different question, and answers it without nonsense at all: hold
the attested shape, vary ONE position between two values of its own class, and
see whether the returned value moves. A position whose value changes the answer
is read. Nonsense is still sent, but only to tell "reads it" apart from
"ignores everything here".

    python3 tools/probe_arg_positions.py --plan            # no live instance needed
    python3 tools/probe_arg_positions.py --run > tests/verb-arg-positions.json
    python3 tools/probe_arg_positions.py --get get_sample_info
    python3 tools/probe_arg_positions.py --check

A keyword position can only be varied where the verb has TWO keywords to vary
between, and most have one — the first pass therefore held a probeable shape for
a third of the multi-token verbs and skipped the rest. `--keywords` widens the
source of that second word beyond the attested tails; every value carries the
source that supplied it, so a verdict is read together with what it rests on.

Query position only, so nothing is executed and no state changes. Verbs whose
baseline disagrees with itself between two reads are reported `unstable` and
scored nowhere — the `get_cpu` drift lesson, which repeat-agreement alone did
not catch.
"""

from __future__ import annotations

import argparse
import json
import plistlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixtures import (Channel, FixtureError, build_fixtures, ensure_audio,  # noqa: E402
                      establish, is_error, teardown)

ROOT = Path(__file__).resolve().parents[1]
TAILS = ROOT / "tests" / "attested-tails.json"
CATALOG = ROOT / "tests" / "action-catalog.json"
VOCAB = ROOT / "tests" / "binary-vocabularies.json"
SWEEP = ROOT / "tests" / "verb-existence-sweep.json"
ARTIFACT = ROOT / "tests" / "verb-arg-positions.json"
APP = Path("/Applications/VirtualDJ.app")

# Two values per shape class: same class, different value. Varying WITHIN the
# class is the point — a difference then means the position was read, not that
# the verb rejected a type it never accepts.
POOL: dict[str, tuple[str, str]] = {
    "NUM": ("1", "2"),
    "DUR": ("1000ms", "4000ms"),
    "PCT": ("25%", "75%"),
    "REL": ("+1", "-1"),
    "BOOL": ("on", "off"),
    "VAR": ("'$vdjprobe_a'", "'$vdjprobe_b'"),
}
# Keyword-ish positions can only be varied with keywords this verb is actually
# attested to take. Inventing two words would test nothing but the floor.
KEYWORDISH = {"KW", "STR", "NAME"}
# Where a keyword value may come from, best evidence first. A verb needs TWO to
# be probeable at a keyword position, and most have one — which is why the first
# pass skipped 2 of every 3 multi-token shapes it could otherwise have held.
#
#   attested — Atomix wrote it in a shipped script (`tests/attested-tails.json`)
#   catalog  — the vendor's own parameter list for that verb, minus the buckets
#              the cross-check already disowns
#   vocab    — a member of the shared enumeration the verb draws from; a Tier-2
#              LEAD, not a confirmed token, so it is opt-in
#
# The order is a priority, not a preference: the baseline value takes the
# best-sourced keyword, so a conclusion never rests on a lead when an attested
# token was available to anchor it.
KEYWORD_SOURCES = ("attested", "catalog", "vocab")
DEFAULT_SOURCES = ("attested", "catalog")
NONSENSE = ("'qzqzqz'", "'wvwvwv'")
# Spacing for the confirmation reads on a positive. Three samples over ~1.05s
# cross the phase of anything blinking on a sub-second to one-second period,
# which is the range the skin verbs use. Paid only on a `reads` candidate.
SETTLE_SAMPLES, SETTLE_SECONDS = 3, 0.35
# The states to hold the shape in. A position that reads is only visible where
# the state makes two values ANSWER differently: `get_sample_info <slot> <field>`
# cannot separate its fields with an empty sampler, and the first capture of
# this prober — taken in whatever state the app happened to be in — scored eight
# verbs as reading a position that a later run in a different state scored
# differently. Ambient state is not a control.
DEFAULT_FIXTURES = ("sampler_slot_loaded", "one_deck_loaded", "both_decks_loaded",
                    "deck2_playing", "loop_active", "fx_slot_1_on")
# Shapes carrying an expression (`NUM`, EXP:...) are not positionally probeable
# from here: the inner expression has to evaluate in context.
SKIP_TOKENS = ("`", "EXP")


def load_shapes() -> tuple[dict[str, dict], dict[str, list[str]]]:
    data = json.loads(TAILS.read_text())
    tails = {v: sorted(toks) for v, toks in data.get("tails", {}).items()}
    return data.get("shapes", {}), tails


def catalog_keywords() -> dict[str, list[str]]:
    """The vendor's documented parameters, minus what the cross-check disowns.

    `documented_parameters` is a tokenizer's reading of the verb's own prose, so
    it carries the doc author's example names (`loop_load "myloop"`) alongside
    real vocabulary. Feeding a placeholder in here would be worse than useless:
    varying between a real keyword and an invented one is a keyword-vs-nonsense
    test wearing the clothes of a within-class comparison, and the nonsense
    control already asks that question. The catalog extractor has already sorted
    both buckets out — use its answer rather than re-deriving one.
    """
    data = json.loads(CATALOG.read_text())
    cross = data["cross_check"]
    disowned: dict[str, set[str]] = {}
    for bucket in ("documented_example_placeholders", "documented_but_locally_refuted"):
        for verb, tokens in cross.get(bucket, {}).items():
            disowned.setdefault(verb, set()).update(tokens)
    return {verb: sorted(set(rec["documented_parameters"]) - disowned.get(verb, set()))
            for verb, rec in data["actions"].items()}


def vocab_keywords() -> dict[str, list[str]]:
    """Members of the shared enumerations a verb is seen to walk. Tier-2 leads."""
    if not VOCAB.exists():
        return {}
    out: dict[str, set[str]] = {}
    for group in json.loads(VOCAB.read_text())["groups"].values():
        members = set(group.get("members", []))
        for verb in group.get("verbs", {}):
            out.setdefault(verb, set()).update(members)
    return {verb: sorted(members) for verb, members in out.items()}


def keyword_pool(enabled: tuple[str, ...], tails: dict[str, list[str]]) -> dict[str, list[tuple[str, str]]]:
    """Per verb, (token, source) in priority order, de-duplicated by token."""
    by_source = {
        "attested": tails,
        "catalog": catalog_keywords() if "catalog" in enabled else {},
        "vocab": vocab_keywords() if "vocab" in enabled else {},
    }
    pool: dict[str, list[tuple[str, str]]] = {}
    for source in KEYWORD_SOURCES:
        if source not in enabled:
            continue
        for verb, tokens in by_source[source].items():
            seen = {tok for tok, _ in pool.get(verb, [])}
            pool.setdefault(verb, []).extend(
                (tok, source) for tok in tokens if tok not in seen)
    return pool


def candidates(shape: str, verb: str,
               keywords: dict[str, list[tuple[str, str]]]) -> list[dict] | None:
    """Per position, the values to compare — or None if the shape is unprobeable.

    Each entry is `{baseline, variant, source}`. `source` is `pool` for a class
    with a fixed within-class pair, or the keyword source that supplied the two
    words. It travels into the artifact because it decides what a `reads`
    verdict is worth: two attested tokens make it a Tier-1 observation over
    vendor-written vocabulary, while a token that only a Tier-2 lead vouches for
    leaves open the duller reading — that the position separates because one of
    the two words is not vocabulary at all.
    """
    out = []
    available = keywords.get(verb, [])
    for token in shape.split():
        if any(bad in token for bad in SKIP_TOKENS):
            return None
        if token in POOL:
            base, variant = POOL[token]
            out.append({"baseline": base, "variant": variant, "source": "pool"})
        elif token in KEYWORDISH:
            # Every keyword position gets the same best-sourced pair. A word
            # that belongs in position 2 may well be unknown in position 1, and
            # an unknown word can move the answer just as a read one does — that
            # confound is resolved against the nonsense control at verdict time,
            # not by rationing words between positions.
            if len(available) < 2:
                return None
            (a, a_src), (b, b_src) = available[:2]
            out.append({"baseline": f"'{a}'", "variant": f"'{b}'",
                        "source": a_src if a_src == b_src else f"{a_src}+{b_src}"})
        else:
            return None
    return out or None


def weakest_source(pairs: list[dict]) -> str:
    """The least-trusted source any position in this form leans on."""
    order = {"pool": 0, "attested": 1, "catalog": 2, "vocab": 3}
    worst = "pool"
    for pair in pairs:
        for part in pair["source"].split("+"):
            if order.get(part, 99) > order.get(worst, 99):
                worst = part
    return worst


def plan(shapes: dict[str, dict], keywords: dict[str, list[tuple[str, str]]]) -> dict:
    """Which verbs a run would probe, and on what evidence — no live instance.

    The prober costs a live VirtualDJ and a few hundred queries; knowing what it
    would reach costs neither, and this repo queues work on measurements rather
    than on estimates.
    """
    chosen: dict[str, dict] = {}
    for verb, by_shape in sorted(shapes.items()):
        for shape in sorted(by_shape, key=lambda s: -len(s.split())):
            if len(shape.split()) < 2:
                continue
            pairs = candidates(shape, verb, keywords)
            if pairs is None:
                continue
            chosen[verb] = {
                "shape": shape,
                "form": " ".join([verb, *(p["baseline"] for p in pairs)]),
                "weakest_source": weakest_source(pairs),
                "positions": pairs,
            }
            break
    by_source: dict[str, list[str]] = {}
    for verb, rec in chosen.items():
        by_source.setdefault(rec["weakest_source"], []).append(verb)
    return {
        "verbs_probeable": len(chosen),
        "by_weakest_source": {k: sorted(v) for k, v in sorted(by_source.items())},
        "verbs": chosen,
    }


def probe_verb(channel: Channel, verb: str, shape: str,
               pairs: list[dict]) -> dict:
    """One reading of one verb, in whatever state is currently established."""
    def ask(args: list[str]) -> str:
        return channel.query(" ".join([verb, *args]))

    baseline_args = [p["baseline"] for p in pairs]
    first = ask(baseline_args)
    bare = ask([])

    positions = []
    for i in range(len(pairs)):
        varied = list(baseline_args)
        varied[i] = pairs[i]["variant"]
        junk = list(baseline_args)
        junk[i] = NONSENSE[i % len(NONSENSE)]
        v_value, j_value = ask(varied), ask(junk)
        if is_error(first) and is_error(v_value) and is_error(j_value):
            verdict = "no-answer"
        elif v_value != first and j_value != first and v_value == j_value:
            # Both the variant and the junk moved the answer to the SAME place.
            # That is the position rejecting what it does not recognize, and the
            # variant landing in the same bucket — so this run cannot tell the
            # variant apart from nonsense. It is the failure mode that widening
            # the keyword sources introduces (a word real in position 2 is
            # nonsense in position 1), and it must not read as `reads`.
            verdict = "variant-indistinct-from-nonsense"
        elif v_value != first:
            verdict = "reads"
        elif j_value != first:
            verdict = "rejects-nonsense-only"
        else:
            verdict = "ignored"
        if verdict == "reads":
            # Confirm before believing it, and confirm ACROSS TIME. `blink` is
            # why: it alternates on a period its own argument sets, so a variant
            # differs from a baseline taken moments earlier for no reason but
            # the clock, and back-to-back reads agree because they land in the
            # same phase. Sampling the baseline over about a second catches a
            # value that moves while nothing changes — which is the whole claim
            # a `reads` verdict makes about the variant.
            steady = True
            for _ in range(SETTLE_SAMPLES):
                time.sleep(SETTLE_SECONDS)
                if ask(baseline_args) != first:
                    steady = False
                    break
            if not steady or ask(varied) != v_value:
                verdict = "reads-not-reproduced"

        positions.append({
            "index": i + 1,
            "class": shape.split()[i],
            "baseline": pairs[i]["baseline"], "variant": pairs[i]["variant"],
            "value_source": pairs[i]["source"],
            "variant_value": v_value, "nonsense_value": j_value,
            "verdict": verdict,
        })

    # Re-read the baseline last: a verb whose own value drifts separates from
    # anything, and would otherwise be scored as reading every position.
    second = ask(baseline_args)
    return {
        "bare": bare,
        "baseline": first,
        "baseline_again": second,
        "stable": first == second,
        "positions": positions,
    }


# Aggregation order across states. A position that reads in ONE state reads: the
# others simply did not discriminate, which the repo's probing rule already says
# is not evidence against a token. The negatives only win when nothing positive
# was seen anywhere.
VERDICT_RANK = ("reads", "variant-indistinct-from-nonsense", "reads-not-reproduced",
                "rejects-nonsense-only", "ignored", "no-answer")


def sweep_kinds() -> dict[str, str]:
    """Each verb's kind from the existence sweep, for reading a no-answer.

    An action-only verb cannot answer in query position at all, so `no-answer`
    from this prober is its EXPECTED result, not a finding — and not a fixture's
    fault either. `automix_editor_movetrack` cost a wrong conclusion this way: it
    was filed as "wants the automix editor open" when the editor was open and
    irrelevant, because the verb never answers a query in any state.

    Used to LABEL, never to skip. `stem_pad` is classified action-only and
    answers anyway, so excluding this class up front would have discarded the
    run that confirmed its `isolate` token.
    """
    if not SWEEP.exists():
        return {}
    data = json.loads(SWEEP.read_text())
    verbs = data.get("verbs", data)
    return {name: rec["kind"] for name, rec in verbs.items()
            if isinstance(rec, dict) and "kind" in rec}


def installed_build() -> str | None:
    """CFBundleVersion of the VirtualDJ this capture was taken against."""
    plist = APP / "Contents" / "Info.plist"
    if not plist.exists():
        return None
    with plist.open("rb") as fh:
        return plistlib.load(fh).get("CFBundleVersion")


def merge_fixtures(readings: dict[str, dict], shape: str, pairs: list[dict],
                   verb: str, kinds: dict[str, str] | None = None) -> dict:
    """One per-verb record from the readings taken in each state.

    A state where the verb's own baseline drifts is dropped before merging, not
    after: an unstable reading separates from everything, and letting one into
    the merge would hand back exactly the false positives the two-read guard was
    written to catch.
    """
    stable = {name: r for name, r in readings.items() if r["stable"]}
    # Instability is a fact about the VERB, not about the state that exposed it.
    # `blink` alternates on a timer: it held still in three fixtures and moved in
    # two, and across three runs it scored `reads` on position 1 once and
    # position 2 twice, in a different fixture each time. Merging only the
    # steady states would let each run keep whichever accident it saw. A verb
    # that drifts anywhere is scored nowhere.
    drifts = bool(set(readings) - set(stable))
    positions = []
    for i, pair in enumerate(pairs):
        by_fixture = {name: r["positions"][i]["verdict"] for name, r in stable.items()}
        best = min(by_fixture.values(), key=VERDICT_RANK.index) if by_fixture else "no-answer"
        positions.append({
            "index": i + 1,
            "class": shape.split()[i],
            "baseline": pair["baseline"], "variant": pair["variant"],
            "value_source": pair["source"],
            "verdict": best,
            # WHERE it was seen is the evidence, not a footnote: "position 2
            # reads in sampler_slot_loaded" is reproducible, "position 2 reads"
            # is a claim about one afternoon.
            "seen_in": sorted(f for f, v in by_fixture.items() if v == best),
            "by_fixture": dict(sorted(by_fixture.items())),
        })
    return {
        "shape": shape,
        "form": " ".join([verb, *(p["baseline"] for p in pairs)]),
        "weakest_source": weakest_source(pairs),
        "sweep_kind": (kinds or {}).get(verb),
        "stable": bool(stable) and not drifts,
        "unstable_in": sorted(set(readings) - set(stable)),
        "positions": positions,
        "readings": dict(sorted(readings.items())),
    }


def summarise(results: dict[str, dict]) -> dict:
    reads = {v: [p["index"] for p in r["positions"] if p["verdict"] == "reads"]
             for v, r in results.items() if r["stable"]}
    reads = {v: idx for v, idx in reads.items() if idx}
    # A `reads` verdict earned with two attested tokens and one earned with a
    # Tier-2 lead are not the same claim; keep them apart in the summary rather
    # than in a footnote nobody reads.
    by_source: dict[str, list[str]] = {}
    for verb in reads:
        by_source.setdefault(results[verb].get("weakest_source", "pool"), []).append(verb)
    return {
        "verbs_probed": len(results),
        "unstable": sorted(v for v, r in results.items() if not r["stable"]),
        "verbs_reading_a_position": len(reads),
        "reads_beyond_first": sorted(v for v, idx in reads.items() if any(i > 1 for i in idx)),
        # Verbs whose apparent read failed to reproduce on the spot: drift, not
        # a position. Named rather than dropped — this is the `blink` class.
        "drifting": sorted(v for v, r in results.items()
                           if r["unstable_in"]
                           or any(p["verdict"] == "reads-not-reproduced"
                                  for p in r["positions"])),
        "reads_by_weakest_source": {k: sorted(v) for k, v in sorted(by_source.items())},
        # Split the silences. An action-only verb answering nothing in query
        # position is the definition of action-only; a query-capable verb
        # answering nothing is a real gap, and the only one worth chasing.
        "no_answer_expected_action_only": sorted(
            v for v, r in results.items()
            if r.get("sweep_kind") == "action-only"
            and all(p["verdict"] == "no-answer" for p in r["positions"])),
        "no_answer_unexplained": sorted(
            v for v, r in results.items()
            if r.get("sweep_kind") != "action-only"
            and all(p["verdict"] == "no-answer" for p in r["positions"])),
        # Structure says one thing, observation another. Kept because this repo
        # treats that disagreement as a finding, not a bug to smooth over.
        "answers_despite_action_only": sorted(
            v for v, r in results.items()
            if r.get("sweep_kind") == "action-only"
            and not all(p["verdict"] == "no-answer" for p in r["positions"])),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", action="store_true", help="query a live VirtualDJ")
    ap.add_argument("--plan", action="store_true",
                    help="what a run would reach, and on what evidence; no live instance")
    ap.add_argument("--get", metavar="VERB")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--fixtures", default=",".join(DEFAULT_FIXTURES),
                    help="named states to hold the shape in (default: %(default)s)")
    ap.add_argument("--keywords", default=",".join(DEFAULT_SOURCES),
                    metavar=",".join(KEYWORD_SOURCES),
                    help="keyword value sources, best first (default: %(default)s)")
    args = ap.parse_args()

    sources = tuple(s.strip() for s in args.keywords.split(",") if s.strip())
    unknown = [s for s in sources if s not in KEYWORD_SOURCES]
    if unknown:
        ap.error(f"unknown keyword source(s): {', '.join(unknown)} "
                 f"(known: {', '.join(KEYWORD_SOURCES)})")

    if args.get:
        if not ARTIFACT.exists():
            sys.exit("no capture yet: python3 tools/probe_arg_positions.py --run > "
                     "tests/verb-arg-positions.json")
        art = json.loads(ARTIFACT.read_text())
        print(json.dumps(art["verbs"].get(args.get, {"error": f"no record for {args.get}"}),
                         indent=1))
        return 0

    if args.check:
        if not ARTIFACT.exists():
            print("arg-position check skipped: not captured yet")
            return 0
        s = json.loads(ARTIFACT.read_text())["summary"]
        line = (f"arg-position check passed: {s['verbs_probed']} verbs"
                f"{' in ' + str(len(s['fixtures'])) + ' fixtures' if s.get('fixtures') else ''}, "
                f"{s['verbs_reading_a_position']} read at least one position, "
                f"{len(s['reads_beyond_first'])} read one beyond the first, "
                f"{len(s['unstable'])} unstable")
        # Captures predating the widened keyword sources carry neither field.
        if "keyword_sources" in s:
            line += f"; keywords from {','.join(s['keyword_sources'])}"
        print(line)
        if s.get("build"):
            line += f"; build {s['build']}"
        if "fixtures" not in s:
            print("  notice: captured in ambient state, before the prober held named "
                  "fixtures — re-run `just probe-arg-positions` to make it reproducible")
        elif "reads_by_weakest_source" not in s:
            print("  notice: captured before value provenance was recorded — "
                  "re-run `just probe-arg-positions` to score verdicts by source")
        return 0

    if args.plan:
        shapes, tails = load_shapes()
        json.dump(plan(shapes, keyword_pool(sources, tails)), sys.stdout, indent=1)
        print()
        return 0

    if not args.run:
        ap.error("pass --run (queries a live VirtualDJ), --plan or --check")

    fixture_names = [f.strip() for f in args.fixtures.split(",") if f.strip()]
    shapes, tails = load_shapes()
    keywords = keyword_pool(sources, tails)

    # Choose the shape per verb once, before any state is touched.
    chosen: dict[str, tuple[str, list[dict]]] = {}
    for verb, by_shape in sorted(shapes.items()):
        for shape in sorted(by_shape, key=lambda s: -len(s.split())):
            if len(shape.split()) < 2:
                continue
            pairs = candidates(shape, verb, keywords)
            if pairs is None:
                continue
            chosen[verb] = (shape, pairs)
            break

    channel = Channel()
    if not channel.reachable():
        raise FixtureError("HTTP channel unreachable on localhost:80 — is VirtualDJ "
                           "running with Network Control enabled?")
    track = ensure_audio(verbose=True)
    fixtures = build_fixtures(track)
    readings: dict[str, dict[str, dict]] = {verb: {} for verb in chosen}

    done: list[str] = []
    unavailable: dict[str, str] = {}
    for name in fixture_names:
        fixture = fixtures[name]
        print(f"  establishing {name}", file=sys.stderr)
        try:
            before = establish(channel, fixture, verbose=False)
        except FixtureError as exc:
            # Some fixtures assert a state they cannot create — `sampler_slot_loaded`
            # needs a sample the user has actually loaded. That is a state this
            # machine could not offer today, not a failed run, and the merge is
            # explicitly written to survive a missing state. Record which ones
            # were unavailable so a thin result is never read as a negative.
            unavailable[name] = str(exc).splitlines()[0]
            print(f"    unavailable: {unavailable[name]}", file=sys.stderr)
            continue
        try:
            for verb, (shape, pairs) in chosen.items():
                readings[verb][name] = probe_verb(channel, verb, shape, pairs)
            done.append(name)
        finally:
            teardown(channel, fixture, before, verbose=False)

    if not done:
        raise FixtureError("no fixture could be established; nothing was probed")

    kinds = sweep_kinds()
    results = {verb: merge_fixtures(readings[verb], shape, pairs, verb, kinds)
               for verb, (shape, pairs) in chosen.items()}
    summary = summarise(results)
    summary["keyword_sources"] = list(sources)
    summary["fixtures"] = done
    summary["fixtures_unavailable"] = unavailable
    # Stamp the build. Fixtures pin deck, transport and FX state, and they pin
    # the AUDIO — `fixtures.py` generates its own track so nothing depends on
    # the user's collection. They do not pin the LIBRARY: sampler bank contents,
    # karaoke files and browser folders belong to the machine, and a verb that
    # reads one of those answers differently on a different install for reasons
    # no fixture can reach. Two captures of this artifact taken on two machines
    # are not directly comparable, and without this line nothing says so.
    summary["build"] = installed_build()
    json.dump({"summary": summary, "verbs": results}, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
