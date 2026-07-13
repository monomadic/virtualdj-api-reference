#!/usr/bin/env python3
"""Lint VirtualDJ skin XML against the shipped-skin vocabulary.

VirtualDJ's skin parser silently ignores unknown elements and attributes
(demonstrated by typos in Atomix's own shipped skins: `ction=`,
`hightlight=`). This linter catches that class of mistake before it ships:
it checks every element name, and every attribute name per element, against
the vocabulary actually used by the built-in skins and the official SDK
example, and suggests the closest known name for anything unknown.

Vocabulary source: the shipped corpora under examples/Skins (Built-In + SDK
example), tokenized with the same tolerant scanner as the XML inventory.
Known shipped typos are excluded from the vocabulary so they stay flagged.

Default lint targets: the repo's own hand-authored skins
(examples/Skins/ModularSkeleton/build, examples/Skins/GraveRaver/build,
tests/Skins). Pass explicit paths to lint generated or external skin XML.

Findings are warnings by default (exit 0); --strict makes them fail.

Usage:
  python3 tools/lint_skins.py [paths ...]
  python3 tools/lint_skins.py --strict my-generated-skin.xml
"""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from extract_xml_inventory import scan_tags  # noqa: E402

VOCAB_GLOBS = [
    "examples/Skins/Built-In/**/*.xml",
    "examples/Skins/SDK Example - Custom Browser Skin/skin.xml",
]
DEFAULT_TARGET_GLOBS = [
    "examples/Skins/ModularSkeleton/build/*.xml",
    "examples/Skins/GraveRaver/build/*.xml",
    "tests/Skins/**/*.xml",
]

# Shipped typos kept out of the vocabulary so new occurrences stay flagged.
KNOWN_TYPO_ATTRS = {"ction", "hightlight"}
# Legitimate namespaced attributes used by build-time tooling.
IGNORED_ATTR_PREFIXES = ("xml:", "xmlns")


def build_vocabulary() -> dict[str, set[str]]:
    vocab: dict[str, set[str]] = {}
    for pattern in VOCAB_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            for element, attrs in scan_tags(path.read_text(errors="replace")):
                element = element.lower()
                bucket = vocab.setdefault(element, set())
                bucket.update(a.lower() for a in attrs)
    for attrs in vocab.values():
        attrs.difference_update(KNOWN_TYPO_ATTRS)
    return vocab


def lint_file(path: Path, vocab: dict[str, set[str]], findings: list[str]) -> None:
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        rel = path
    all_attrs = set().union(*vocab.values()) if vocab else set()
    for element, attrs in scan_tags(path.read_text(errors="replace")):
        element_lc = element.lower()
        if element_lc not in vocab:
            suggestion = difflib.get_close_matches(element_lc, vocab, n=1)
            hint = f" (closest known: <{suggestion[0]}>)" if suggestion else ""
            findings.append(f"{rel}: unknown element <{element}>{hint}")
            continue
        lowered = [a.lower() for a in attrs]
        if "class" in lowered:
            # class instantiation: extra attributes are define-placeholder
            # values with arbitrary user-chosen names; not checkable.
            continue
        known = vocab[element_lc]
        for attr in attrs:
            attr_lc = attr.lower()
            if attr_lc.startswith(IGNORED_ATTR_PREFIXES):
                continue
            if attr_lc in known:
                continue
            # attribute is known on other elements: still fine (global attrs
            # like visibility/os/panel travel widely) unless it is a typo
            if attr_lc in all_attrs and attr_lc not in KNOWN_TYPO_ATTRS:
                continue
            pool = known | all_attrs
            suggestion = difflib.get_close_matches(attr_lc, pool, n=1)
            hint = f" (closest known: {suggestion[0]!r})" if suggestion else ""
            findings.append(f"{rel}: <{element}> unknown attribute {attr!r}{hint}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="skin XML files (default: repo-authored skins)")
    parser.add_argument("--strict", action="store_true", help="findings fail the run")
    args = parser.parse_args()

    if args.paths:
        files = [Path(p).resolve() for p in args.paths]
    else:
        files = [p for g in DEFAULT_TARGET_GLOBS for p in sorted(ROOT.glob(g))]
    if not files:
        print("No skin XML files found")
        return 1

    vocab = build_vocabulary()
    if not vocab:
        print("No vocabulary corpora found under examples/Skins")
        return 1

    findings: list[str] = []
    for path in files:
        lint_file(path, vocab, findings)

    for line in findings:
        print(f"WARN  {line}")
    if findings and args.strict:
        return 1
    print(
        f"Skins lint passed: {len(files)} files against "
        f"{len(vocab)}-element vocabulary, {len(findings)} warnings"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
