#!/usr/bin/env python3
"""Send every vendor-written snippet through the parser and record what happens.

The first check in this repo that can FALSIFY a grammar claim rather than extend
one: each of the 1,427 snippets in tests/vdjscript-corpus.json is a form Atomix
shipped or documented, so a structural parse failure means this reference (or
the corpus extraction) is wrong about the language.

Reading the results needs care, and the traps are already documented:

- **Query only.** The corpus contains `load`, `unload`, `browsed_song color` and
  broadcast verbs; executing it would rewrite the library. Nothing here is ever
  sent to /execute.
- **`E_FAIL` is silence, not denial** (Evidence Standards rule 4). A real verb
  returns it — `remote_action` does. So E_FAIL is classified `no-value`, never
  as a parse failure.
- **Environmental misses are not grammar failures.** A snippet naming an effect,
  skin, folder or file this install lacks fails for reasons that say nothing
  about syntax. `E_INVALIDARG` on a snippet whose arguments name content is
  therefore reported separately from a bare structural rejection.

Only `structural` outcomes are candidate contradictions, and each still needs a
nonsense control before it is called one.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import Channel, FixtureError  # noqa: E402

CORPUS = Path("tests/vdjscript-corpus.json")
SWEEP = Path("tests/verb-existence-sweep.json")
ARTIFACT = Path("tests/corpus-parse-results.json")

E_FAIL = "error:-2147467259"
E_INVALIDARG = "error:-2147024809"
E_NOTIMPL = "error:-2147467263"
# Arguments that name installed content rather than describe syntax.
CONTENT = re.compile(r"['\"][^'\"]*[ ./\\][^'\"]*['\"]|\.(mp3|wav|m4a|mp4|vdjsample|zip)\b", re.I)
PLACEHOLDER = re.compile(r"\b[XY]\b")
# param_* verbs read the value passed down the chain; over HTTP there is none.
PIPELINE = re.compile(r"(^|&)\s*param_[a-z_]+", re.I)  # `sampler_bank X & sampler_play_stop Y` from the wiki


def classify(script: str, answer: str, kinds: dict[str, str] | None = None) -> str:
    if not answer.startswith("error:"):
        return "parsed"
    if answer == E_FAIL:
        return "no-value"          # silence, not denial
    if answer == E_NOTIMPL:
        return "not-implemented"   # verb exists, this form does nothing here
    if answer == E_INVALIDARG:
        if PLACEHOLDER.search(script):
            return "placeholder"   # documentation stand-in, not a real argument
        if PIPELINE.search(script):
            # `get_bpm & param_cast`, `display_time & param_uppercase`: param_*
            # consumes the value flowing down the chain, and the HTTP query
            # surface has no such value to give it. A skin text context does.
            return "pipeline"
        if CONTENT.search(script):
            return "environmental"  # names content this install may not have
        head = re.match(r"[a-z_][a-z0-9_]*", script.strip())
        if kinds and head and kinds.get(head.group(0)) in ("needs-args", "action-only"):
            # An action-position verb sent to /query. The vendor ships
            # `hot_cue 1` in pad pages where it works; the HTTP query surface
            # simply cannot evaluate it, the same boundary that makes
            # remote_action answer E_FAIL while being a real verb.
            return "surface-gated"
        return "structural"
    return "other-error"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    if args.check:
        if not ARTIFACT.exists():
            print("corpus parse check skipped: tests/corpus-parse-results.json not collected")
            return 0
        summary = json.load(open(ARTIFACT))["summary"]
        if summary["outcomes"].get("structural", 0) > summary["allowed_structural"]:
            sys.exit(f"corpus parse check FAILED: {summary['outcomes']['structural']} structural "
                     f"rejections, above the recorded {summary['allowed_structural']}")
        print(f"corpus parse check passed: {summary['snippets']} snippets, "
              f"{summary['outcomes']}")
        return 0

    snippets = json.load(open(CORPUS))["snippets"]
    kinds = {v: r.get("kind") for v, r in json.load(open(SWEEP))["verbs"].items()} \
        if SWEEP.exists() else {}
    if args.limit:
        snippets = snippets[:args.limit]
    channel = Channel()
    if not channel.reachable():
        raise FixtureError("HTTP channel unreachable — is VirtualDJ running?")

    results = []
    for i, record in enumerate(snippets, 1):
        answer = channel.query(record["script"])
        results.append({"script": record["script"], "answer": answer,
                        "outcome": classify(record["script"], answer, kinds),
                        "sources": record["sources"], "origin": record["origins"][0]})
        if not args.quiet and i % 200 == 0:
            print(f"  {i}/{len(snippets)}", file=sys.stderr)

    outcomes = Counter(r["outcome"] for r in results)
    structural = [r for r in results if r["outcome"] == "structural"]
    json.dump({
        "summary": {
            "snippets": len(results),
            "outcomes": dict(outcomes),
            "allowed_structural": len(structural),
            "note": "only `structural` outcomes are candidate contradictions; each still needs "
                    "a nonsense control before it is called one",
        },
        "structural": structural,
        "results": results,
    }, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FixtureError as exc:
        raise SystemExit(f"corpus parse run aborted: {exc}")
