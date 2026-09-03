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

SHAPES (added 2026-09-03). Tails are vocabulary; a verb whose arguments are
values has none — "fadeout 10000ms 3000ms `loop`" yielded nothing, and 114
verbs with vendor examples were invisible. So every statement also contributes
a SHAPE: its argument tokens classified as DUR (`200ms`, `8bt`), PCT (`50%`),
NUM, REL (`+1`), STR (quoted), VAR (`$x`), BOOL (`on`/`off`/`yes`/`no`/
`true`/`false`), KW (a bare keyword), or NAME (a bare keyword that is also a
verb name — `loop_roll video`, `browser_window sideview` — a keyword for most
verbs). An EXPRESSION argument reduces to the type its inner verb returns,
because that is what the callee receives: a backticked one is written
`` `BOOL` `` / `` `NUM` `` / `` `STR` `` (`` `?` `` when the inner verb's type
is unmeasured), and a bare one under a `param_*` comparator, whose bare-word
arguments are expressions, is written `EXP:NUM` etc. The surface form is kept
because it changes behaviour: transport verbs reject a computed argument where
the literal works (VirtualDJ Reference, Tested Grammar Rules). Examples:
"fadeout DUR DUR `BOOL`", "param_bigger EXP:NUM EXP:NUM". The `deck` wrapper is not a verb but a grammar
construct that takes a selector and the rest of the statement as an expression
(`deck SEL EXP`); it is unwrapped so the inner verb gets its shape, and the
selectors seen are recorded under `wrappers`. Each shape carries its RETURN
evidence, three ways: the attribute the vendor wrote it into (`color` ⇒ color,
`value` ⇒ number, `visibility` ⇒ bool or a 0–1 fade level, since skins fade
elements with it — attested, but only for the chain's last statement, and the
attribute constrains the type rather than pinning it), the catalog's own
"returns …" prose, and the Tier-1 bare-form sweep
(`tests/verb-return-types.json`), which cannot see argument-dependent types.

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
RETURN_TYPES = Path("tests/verb-return-types.json")
CONTRACTS = Path("tests/action-contracts.json")

TOKEN = re.compile(r"`[^`]*`|'[^']*'|\"[^\"]*\"|\S+")
DURATION = re.compile(r"^[+-]?[\d.]+(ms|s|bt)$", re.I)
PERCENT = re.compile(r"^[+-]?[\d.]+%$")
NUMBER = re.compile(r"^[\d.]+$")
RELATIVE = re.compile(r"^[+-][\d.]+$")
# What the vendor's attribute tells us about the value of the chain it holds.
CONTEXT_TYPE = {"visibility": "bool_or_fade", "enabled": "bool", "color": "color",
                "textcolor": "color", "value": "number", "query": "value",
                "tooltip_query": "text", "action": "none", "onstart": "none",
                "onstop": "none", "ondblclick": "none"}
RETURN_PROSE = re.compile(r"\breturns?\b[^.\n]{0,120}", re.I)
BOOLEANS = {"on", "off", "yes", "no", "true", "false"}
# Verbs whose bare-word arguments are expressions: `param_bigger pitch pitch_slider`.
EXPRESSION_HEADS = re.compile(r"^param_")
# `deck 1 play`, `deck left …`, `deck [SWAPDECK] …`: a wrapper, not a verb.
DECK = re.compile(r"^deck\s+(\S+)\s+(.+)$")

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
            statement, _wrapped = unwrap(statement.strip(), {})
            tokens = statement.split()
            if len(tokens) < 2 or tokens[0] not in known:
                continue
            verb, raw = tokens[0], tokens[1]
            token = raw.strip("'\"")
            if not WORD.match(token):
                continue
            if token in MODIFIERS or LITERAL.match(token) or VARIABLE.match(raw):
                continue
            if token in BOOLEANS or (token in known and EXPRESSION_HEADS.match(verb)):
                continue  # `hold on` is a value; `param_bigger pitch …` an expression
            found[verb][token].append({
                "snippet": record["script"][:200],
                "sources": record["sources"],
                "origin": record["origins"][0],
            })
    return {v: dict(t) for v, t in found.items()}


# Observed bare-form type (tests/verb-return-types.json) -> shape class.
TYPE_CLASS = {"bool": "BOOL", "int": "NUM", "float": "NUM", "percent": "PCT", "text": "STR"}


def reduced_type(expression: str, known: set[str], observed: dict) -> str:
    """The class of what an expression evaluates to: its last verb's return type."""
    statements = [st.strip() for st in SPLIT.split(expression) if st.strip()]
    if not statements:
        return "?"
    head = statements[-1].split()[0] if statements[-1].split() else ""
    head = DECK.sub(lambda m: m.group(2), statements[-1]).split()[0] if DECK.match(statements[-1]) else head
    if head in BOOLEANS:
        return "BOOL"
    if head not in known:
        return "?"
    return TYPE_CLASS.get((observed.get(head) or {}).get("observed_type"), "?")


def classify(token: str, head: str = "", known: set[str] = frozenset(),
             observed: dict | None = None) -> str:
    observed = observed or {}
    if token in BOOLEANS:
        return "BOOL"
    if token in known:
        if EXPRESSION_HEADS.match(head):
            return "EXP:" + reduced_type(token, known, observed)
        return "NAME"
    if token.startswith("`"):
        return "`%s`" % reduced_type(token.strip("`"), known, observed)
    if token[0] in "'\"":
        return "STR"
    if token.startswith("$"):
        return "VAR"
    if DURATION.match(token):
        return "DUR"
    if PERCENT.match(token):
        return "PCT"
    if RELATIVE.match(token):
        return "REL"
    if NUMBER.match(token):
        return "NUM"
    return "KW"


def unwrap(statement: str, wrappers: dict) -> tuple[str, str | None]:
    """Strip a `deck <selector>` prefix, counting the selector."""
    m = DECK.match(statement)
    if not m:
        return statement, None
    sel = m.group(1)
    wrappers.setdefault("deck", {"shape": "SEL EXP", "selectors": {}})
    wrappers["deck"]["selectors"][sel] = wrappers["deck"]["selectors"].get(sel, 0) + 1
    return m.group(2).strip(), f"deck {sel}"


def shapes(corpus: list[dict], known: set[str], wrappers: dict,
           observed: dict) -> dict[str, dict[str, dict]]:
    """verb -> shape -> {snippets, contexts}."""
    found: dict[str, dict[str, dict]] = defaultdict(dict)
    for record in corpus:
        contexts = [o.rsplit("@", 1)[1] for o in record["origins"] if "@" in o]
        contexts += ["catalog"] * ("catalog" in record["sources"])
        statements = [st.strip() for st in SPLIT.split(record["script"]) if st.strip()]
        for i, statement in enumerate(statements):
            statement, wrapped = unwrap(statement, wrappers)
            tokens = TOKEN.findall(statement)
            if len(tokens) < 2 or tokens[0] not in known:
                continue
            classes = []
            for tok in tokens[1:]:
                if tok in MODIFIERS:
                    break
                classes.append(classify(tok, tokens[0], known, observed))
            if not classes:
                continue
            shape = " ".join(classes)
            rec = found[tokens[0]].setdefault(shape, {"snippets": [], "contexts": {}})
            terminal = i == len(statements) - 1
            entry = {"snippet": record["script"][:200], "sources": record["sources"],
                     "origin": record["origins"][0], "terminal": terminal}
            if wrapped:
                entry["wrapped_by"] = wrapped
            rec["snippets"].append(entry)
            if terminal:
                for ctx in contexts:
                    rec["contexts"][ctx] = rec["contexts"].get(ctx, 0) + 1
    return {v: dict(sh) for v, sh in found.items()}


def returns_for(verb: str, contexts: dict[str, int], catalog: dict, observed: dict,
                contracts: dict) -> dict:
    attested = sorted({CONTEXT_TYPE[c] for c in contexts if c in CONTEXT_TYPE} - {"none"})
    text = catalog.get(verb, {}).get("text", "")
    prose = [m.group(0).strip() for m in RETURN_PROSE.finditer(text)]
    obs = observed.get(verb) or {}
    con = contracts.get(verb) or {}
    return {
        "attested": attested,
        "executed_in": sorted(c for c in contexts if CONTEXT_TYPE.get(c) == "none"),
        "catalog_prose": prose[:3],
        "observed_bare": obs.get("observed_type"),
        "structural": {k: con[k] for k in ("queries", "query_bool", "query_text") if k in con},
    }


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
    observed = json.load(open(RETURN_TYPES))["verbs"] if RETURN_TYPES.exists() else {}
    wrappers: dict = {}
    shaped = shapes(corpus, known, wrappers, observed)
    contracts = json.load(open(CONTRACTS))["verbs"] if CONTRACTS.exists() else {}

    probed = json.load(open(ARG_FORMS))["verbs"] if ARG_FORMS.exists() else {}
    catalog = json.load(open(CATALOG))["actions"] if CATALOG.exists() else {}
    for verb, by_shape in shaped.items():
        for shape, rec in by_shape.items():
            rec["returns"] = returns_for(verb, rec["contexts"], catalog, observed, contracts)

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
              f"verbs, {stored['novel_tokens']} not otherwise known; "
              f"{stored.get('shapes', '?')} shapes on {stored.get('shaped_verbs', '?')} verbs")
        return 0

    if args.verb:
        print(json.dumps({"verb": args.verb, "tails": found.get(args.verb, {}),
                          "shapes": shaped.get(args.verb, {}),
                          **({"wrapper": wrappers[args.verb]} if args.verb in wrappers else {})},
                         indent=1))
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
            "shapes": sum(len(sh) for sh in shaped.values()),
            "shaped_verbs": len(shaped),
            "shape_only_verbs": sorted(v for v in shaped if v not in found),
            "filtered": {"modifiers": sorted(MODIFIERS),
                         "rule": "literals, variables and verb names dropped"},
        },
        "novel": novel,
        "tails": found,
        "shapes": shaped,
        "wrappers": wrappers,
    }, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
