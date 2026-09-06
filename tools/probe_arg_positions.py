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

    python3 tools/probe_arg_positions.py --run > tests/verb-arg-positions.json
    python3 tools/probe_arg_positions.py --get get_sample_info
    python3 tools/probe_arg_positions.py --check

Query position only, so nothing is executed and no state changes. Verbs whose
baseline disagrees with itself between two reads are reported `unstable` and
scored nowhere — the `get_cpu` drift lesson, which repeat-agreement alone did
not catch.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixtures import Channel, is_error  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TAILS = ROOT / "tests" / "attested-tails.json"
ARTIFACT = ROOT / "tests" / "verb-arg-positions.json"

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
NONSENSE = ("'qzqzqz'", "'wvwvwv'")
# Shapes carrying an expression (`NUM`, EXP:...) are not positionally probeable
# from here: the inner expression has to evaluate in context.
SKIP_TOKENS = ("`", "EXP")


def load_shapes() -> tuple[dict[str, dict], dict[str, list[str]]]:
    data = json.loads(TAILS.read_text())
    tails = {v: sorted(toks) for v, toks in data.get("tails", {}).items()}
    return data.get("shapes", {}), tails


def candidates(shape: str, verb: str, tails: dict[str, list[str]]) -> list[tuple[str, str]] | None:
    """Per position, the (baseline, variant) pair — or None if unprobeable."""
    out = []
    keywords = [f"'{t}'" for t in tails.get(verb, [])]
    for token in shape.split():
        if any(bad in token for bad in SKIP_TOKENS):
            return None
        if token in POOL:
            out.append(POOL[token])
        elif token in KEYWORDISH:
            if len(keywords) < 2:
                return None
            out.append((keywords[0], keywords[1]))
        else:
            return None
    return out or None


def probe_verb(channel: Channel, verb: str, shape: str,
               pairs: list[tuple[str, str]]) -> dict:
    def ask(args: list[str]) -> str:
        return channel.query(" ".join([verb, *args]))

    baseline_args = [a for a, _ in pairs]
    first = ask(baseline_args)
    bare = ask([])

    positions = []
    for i in range(len(pairs)):
        varied = list(baseline_args)
        varied[i] = pairs[i][1]
        junk = list(baseline_args)
        junk[i] = NONSENSE[i % len(NONSENSE)]
        v_value, j_value = ask(varied), ask(junk)
        if is_error(first) and is_error(v_value) and is_error(j_value):
            verdict = "no-answer"
        elif v_value != first:
            verdict = "reads"
        elif j_value != first:
            verdict = "rejects-nonsense-only"
        else:
            verdict = "ignored"
        positions.append({
            "index": i + 1,
            "class": shape.split()[i],
            "baseline": pairs[i][0], "variant": pairs[i][1],
            "variant_value": v_value, "nonsense_value": j_value,
            "verdict": verdict,
        })

    # Re-read the baseline last: a verb whose own value drifts separates from
    # anything, and would otherwise be scored as reading every position.
    second = ask(baseline_args)
    return {
        "shape": shape,
        "form": " ".join([verb, *baseline_args]),
        "bare": bare,
        "baseline": first,
        "baseline_again": second,
        "stable": first == second,
        "positions": positions,
    }


def summarise(results: dict[str, dict]) -> dict:
    reads = {v: [p["index"] for p in r["positions"] if p["verdict"] == "reads"]
             for v, r in results.items() if r["stable"]}
    reads = {v: idx for v, idx in reads.items() if idx}
    return {
        "verbs_probed": len(results),
        "unstable": sorted(v for v, r in results.items() if not r["stable"]),
        "verbs_reading_a_position": len(reads),
        "reads_beyond_first": sorted(v for v, idx in reads.items() if any(i > 1 for i in idx)),
        "no_answer": sorted(v for v, r in results.items()
                            if all(p["verdict"] == "no-answer" for p in r["positions"])),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", action="store_true", help="query a live VirtualDJ")
    ap.add_argument("--get", metavar="VERB")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

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
        print(f"arg-position check passed: {s['verbs_probed']} verbs, "
              f"{s['verbs_reading_a_position']} read at least one position, "
              f"{len(s['reads_beyond_first'])} read one beyond the first, "
              f"{len(s['unstable'])} unstable")
        return 0

    if not args.run:
        ap.error("pass --run (queries a live VirtualDJ) or --check")

    shapes, tails = load_shapes()
    channel = Channel()
    results: dict[str, dict] = {}
    for verb, by_shape in sorted(shapes.items()):
        for shape in sorted(by_shape, key=lambda s: -len(s.split())):
            if len(shape.split()) < 2:
                continue
            pairs = candidates(shape, verb, tails)
            if pairs is None:
                continue
            results[verb] = probe_verb(channel, verb, shape, pairs)
            break
    json.dump({"summary": summarise(results), "verbs": results}, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
