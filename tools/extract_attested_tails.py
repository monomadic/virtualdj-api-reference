#!/usr/bin/env python3
"""Recover argument tails from scripts Atomix themselves shipped.

A third source of argument evidence, independent of the other two and stronger
than either in one respect: **attestation needs no probe.** A tail written into
a shipped Built-In skin is a form the parser accepts and the vendor intended,
whether or not any fixture can make it observable. The probe can only separate a
token from nonsense, and it is blind wherever the state does not discriminate —
that is why 81 documented parameters still read as "indistinguishable".

    binary  `keyword_candidates`   strings near the verb's own code — noisy
    catalog documented parameters  what a token MEANS — vendor prose
    corpus  attested tails         that a token is USED — vendor scripts

Statements are split on `& ? : ( )`, the leading word must be a known verb, and
the token after it is the candidate tail.

FILTERING IS THE WHOLE DIFFICULTY. Three classes of false parameter have already
shipped in this repo and been retracted: a symbol fragment (`TION_get_text`), a
prose sentence beginning with a verb-like word ("Load saved loop named ..."),
and a statement suffix read as an argument (`dump while_pressed`). So a
candidate is dropped when it is the `while_pressed` modifier, a unit-bearing or
numeric literal, a variable reference, or itself a verb name — a second verb
after the first is a chained statement, not an argument.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

CORPUS = Path("tests/vdjscript-corpus.json")
VERB_TABLE = Path("tests/verb-table.json")
ARTIFACT = Path("tests/attested-tails.json")
ARG_FORMS = Path("tests/verb-arg-forms.json")
CATALOG = Path("tests/action-catalog.json")

SPLIT = re.compile(r"[&?:()]")
WORD = re.compile(r"^[a-z_][a-z0-9_]*$")
# `volume 100% while_pressed` — a modifier on the statement, not an argument.
MODIFIERS = {"while_pressed", "while_press", "instant"}
# 100ms, 8bt, 50%, +1, -0.5, 0.25 — values, not vocabulary.
LITERAL = re.compile(r"^[+-]?[\d.]+(ms|bt|%|s)?$", re.I)
VARIABLE = re.compile(r"^[$#%@`]")


def tails(corpus: list[dict], known: set[str]) -> dict[str, dict[str, list[dict]]]:
    found: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for record in corpus:
        for statement in SPLIT.split(record["script"]):
            tokens = statement.strip().split()
            if len(tokens) < 2 or tokens[0] not in known:
                continue
            verb, raw = tokens[0], tokens[1]
            token = raw.strip("'\"")
            if not WORD.match(token):
                continue
            if token in MODIFIERS or LITERAL.match(token) or VARIABLE.match(raw):
                continue
            if token in known:
                continue  # a second verb is a chained statement, not an argument
            found[verb][token].append({
                "snippet": record["script"][:200],
                "sources": record["sources"],
                "origin": record["origins"][0],
            })
    return {v: dict(t) for v, t in found.items()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verb")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--new-only", action="store_true",
                        help="only tokens absent from both the probe artifact and the catalog")
    args = parser.parse_args()

    known = set(json.load(open(VERB_TABLE))["verbs"])
    corpus = json.load(open(CORPUS))["snippets"]
    found = tails(corpus, known)

    probed = json.load(open(ARG_FORMS))["verbs"] if ARG_FORMS.exists() else {}
    catalog = json.load(open(CATALOG))["actions"] if CATALOG.exists() else {}

    def elsewhere(verb: str) -> set[str]:
        confirmed = {t[0] for t in probed.get(verb, {}).get("recognized_tokens", [])
                     if len(t) == 1}
        return confirmed | set(catalog.get(verb, {}).get("documented_parameters", []))

    novel = {v: sorted(set(t) - elsewhere(v)) for v, t in found.items()}
    novel = {v: t for v, t in novel.items() if t}

    if args.check:
        if not ARTIFACT.exists():
            print("attested tails check skipped: tests/attested-tails.json not extracted yet")
            return 0
        stored = json.load(open(ARTIFACT))["summary"]
        if stored["verbs"] != len(found):
            sys.exit(f"attested tails check FAILED: artifact has {stored['verbs']} verbs, "
                     f"re-extraction finds {len(found)} — re-extract")
        print(f"attested tails check passed: {stored['tokens']} tokens on {stored['verbs']} "
              f"verbs, {stored['novel_tokens']} not otherwise known")
        return 0

    if args.verb:
        print(json.dumps({"verb": args.verb, "tails": found.get(args.verb, {})}, indent=1))
        return 0
    if args.new_only:
        print(json.dumps(novel, indent=1))
        return 0

    json.dump({
        "summary": {
            "verbs": len(found),
            "tokens": sum(len(t) for t in found.values()),
            "novel_tokens": sum(len(t) for t in novel.values()),
            "novel_verbs": len(novel),
            "filtered": {"modifiers": sorted(MODIFIERS),
                         "rule": "literals, variables and verb names dropped"},
        },
        "novel": novel,
        "tails": found,
    }, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
