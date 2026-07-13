#!/usr/bin/env python3
"""Lint VirtualDJ mapper XML files.

Structural checks (errors, exit 1):
- well-formed XML with a `<mapper>` root
- root has a non-empty `device` attribute; only known root attributes
- children are only `<info>` and `<map>`
- every `<map>` has a non-empty `value` and an `action`; only known attributes

Verb checks (warnings, exit 0 unless --strict):
- the leading verb of each action statement is resolved against the
  generated docs/vdjscript-verb-index.json (regenerate with
  `python3 tools/extract_verb_index.py`); unknown verbs get a
  closest-match suggestion.

Usage:
  python3 tools/lint_mappers.py [paths ...]   # default: examples/Mappers/**/*.xml
  python3 tools/lint_mappers.py --strict      # verb warnings become failures
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLOB = "examples/Mappers/**/*.xml"
VERB_INDEX = ROOT / "docs" / "vdjscript-verb-index.json"

KNOWN_ROOT_ATTRS = {"device", "author", "version", "date", "priority"}
KNOWN_MAP_ATTRS = {"value", "action", "name"}

# Splits an action into statements at chain/conditional boundaries, then the
# first bare token of each statement is the candidate verb. Deck prefixes are
# consumed ("deck 1 play" -> "play"). Backticked segments are dropped first.
BACKTICK_SEGMENT = re.compile(r"`[^`]*`")
QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"")
STATEMENT_SPLIT = re.compile(r"[&?:]")
DECK_TARGET = re.compile(
    r"^(?:\d+|left|right|master|active|all|default|leftdeck|rightdeck)$", re.IGNORECASE
)
TOKEN_IS_VERB = re.compile(r"^[a-z][a-z0-9_]*$")


def load_verbs() -> set[str]:
    if not VERB_INDEX.exists():
        return set()
    data = json.loads(VERB_INDEX.read_text())
    return set(data.get("verbs", {}))


def leading_verbs(action: str) -> list[str]:
    text = BACKTICK_SEGMENT.sub(" ", action)
    text = QUOTED.sub(" ", text)
    verbs: list[str] = []
    for statement in STATEMENT_SPLIT.split(text):
        tokens = statement.split()
        while len(tokens) >= 2 and tokens[0].lower() == "deck" and DECK_TARGET.match(tokens[1]):
            tokens = tokens[2:]
        if not tokens:
            continue
        head = tokens[0]
        if TOKEN_IS_VERB.match(head):
            verbs.append(head)
    return verbs


def lint_file(path: Path, verbs: set[str], errors: list[str], warnings: list[str]) -> None:
    rel = path.relative_to(ROOT)
    try:
        root = ET.fromstring(path.read_text())
    except ET.ParseError as exc:
        errors.append(f"{rel}: XML parse error: {exc}")
        return

    if root.tag != "mapper":
        errors.append(f"{rel}: root element is <{root.tag}>, expected <mapper>")
        return
    if not root.get("device"):
        errors.append(f"{rel}: <mapper> is missing a non-empty device attribute")
    for attr in sorted(set(root.attrib) - KNOWN_ROOT_ATTRS):
        errors.append(f"{rel}: unknown <mapper> attribute {attr!r}")

    for child in root:
        if child.tag == "info":
            continue
        if child.tag != "map":
            errors.append(f"{rel}: unexpected element <{child.tag}> under <mapper>")
            continue
        value = child.get("value")
        action = child.get("action")
        if not value:
            errors.append(f"{rel}: <map> with missing/empty value attribute")
        if action is None:
            errors.append(f"{rel}: <map value={value!r}> has no action attribute")
        for attr in sorted(set(child.attrib) - KNOWN_MAP_ATTRS):
            errors.append(f"{rel}: <map value={value!r}> unknown attribute {attr!r}")
        if action and verbs:
            for verb in leading_verbs(action):
                if verb not in verbs:
                    suggestion = difflib.get_close_matches(verb, verbs, n=1)
                    hint = f" (closest known: {suggestion[0]!r})" if suggestion else ""
                    warnings.append(
                        f"{rel}: <map value={value!r}> unknown verb {verb!r}{hint}"
                    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="mapper XML files (default: examples/Mappers)")
    parser.add_argument("--strict", action="store_true", help="verb warnings fail the run")
    args = parser.parse_args()

    if args.paths:
        files = [Path(p).resolve() for p in args.paths]
    else:
        files = sorted(ROOT.glob(DEFAULT_GLOB))
    if not files:
        print("No mapper XML files found")
        return 1

    verbs = load_verbs()
    errors: list[str] = []
    warnings: list[str] = []
    for path in files:
        lint_file(path, verbs, errors, warnings)

    for line in errors:
        print(f"ERROR {line}")
    for line in warnings:
        print(f"WARN  {line}")
    if not verbs:
        print("note: docs/vdjscript-verb-index.json missing; verb checks skipped")
    if errors or (args.strict and warnings):
        return 1
    print(
        f"Mappers lint passed: {len(files)} files, "
        f"{len(warnings)} verb warnings"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
