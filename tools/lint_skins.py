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

Vocabulary findings are warnings by default (exit 0); --strict makes them fail.

Structure is checked first, against what VirtualDJ's own parser demonstrably
accepts rather than against the XML spec: shipped skins load with raw `&` in
attribute values, tag names whose case differs between open and close
(`<Tooltip>...</tooltip>`), duplicate attributes, and stray text before the root.
A stdlib parser rejects most of the shipped corpus for those, so it is not used.
What remains an error is what a truncated or hand-broken file looks like: an
unterminated tag, comment or quoted value, a close tag that matches nothing,
an element left open at end of file, or no root element. Those always fail.

Usage:
  python3 tools/lint_skins.py [paths ...]
  python3 tools/lint_skins.py --strict my-generated-skin.xml
"""

from __future__ import annotations

import argparse
import difflib
import re
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


NAME_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.:-]*")
ATTR_RE = re.compile(r"\s*([A-Za-z_][A-Za-z0-9_.:-]*)\s*=\s*")


def display(path: Path) -> Path:
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def check_structure(text: str) -> tuple[list[str], list[str]]:
    """Tag balance under VirtualDJ's tolerances. Returns (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    stack: list[tuple[str, str, int]] = []  # (lowercase name, as written, line)
    roots = 0
    i, n = 0, len(text)

    def line(at: int) -> int:
        return text.count("\n", 0, at) + 1

    while True:
        i = text.find("<", i)
        if i == -1:
            break
        for opener, closer in (("<!--", "-->"), ("<![CDATA[", "]]>")):
            if text.startswith(opener, i):
                end = text.find(closer, i + len(opener))
                if end == -1:
                    errors.append(f"line {line(i)}: unterminated {opener}")
                    return errors, warnings
                i = end + len(closer)
                break
        else:
            if text.startswith("<?", i) or text.startswith("<!", i):
                end = text.find(">", i)
                i = n if end == -1 else end + 1
                continue
            closing = text.startswith("</", i)
            match = NAME_RE.match(text, i + (2 if closing else 1))
            if not match:
                i += 1  # a bare `<` in text, not a tag
                continue
            name, start = match.group(0), i
            # Walk to the tag's `>`, skipping quoted values (which may hold `<`, `>`, `&`).
            k, attrs, quote = match.end(), [], None
            while k < n:
                c = text[k]
                if quote:
                    if c == quote:
                        quote = None
                elif c in "\"'":
                    quote = c
                elif c == ">":
                    break
                elif not closing:
                    m = ATTR_RE.match(text, k)
                    if m:
                        attrs.append(m.group(1).lower())
                        k = m.end()
                        continue
                k += 1
            if k >= n:
                what = "quoted value" if quote else "tag"
                errors.append(f"line {line(start)}: unterminated {what} in <{'/' if closing else ''}{name}")
                return errors, warnings
            i = k + 1
            lower = name.lower()
            if closing:
                depth = next((d for d in range(len(stack) - 1, -1, -1) if stack[d][0] == lower), None)
                if depth is None:
                    errors.append(f"line {line(start)}: </{name}> closes no open element")
                    continue
                for _, written, opened in stack[depth + 1:]:
                    errors.append(f"line {opened}: <{written}> is not closed before </{name}> "
                                  f"at line {line(start)}")
                del stack[depth:]
                continue
            dupes = sorted({a for a in attrs if attrs.count(a) > 1})
            if dupes:
                warnings.append(f"line {line(start)}: <{name}> repeats {', '.join(dupes)} "
                                "(shipped skins do this; which value wins is untested)")
            if not stack:
                roots += 1
            if text[k - 1] != "/":
                stack.append((lower, name, line(start)))
            continue
    for _, written, opened in stack:
        errors.append(f"line {opened}: <{written}> is never closed")
    if roots == 0:
        errors.append("no root element")
    return errors, warnings


def lint_file(path: Path, vocab: dict[str, set[str]], findings: list[str]) -> None:
    rel = display(path)
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
    errors: list[str] = []
    for path in files:
        try:
            text = path.read_text(errors="replace")
        except OSError as exc:
            errors.append(f"{display(path)}: cannot read: {exc.strerror}")
            continue
        structural, warned = check_structure(text)
        errors += [f"{display(path)}: {e}" for e in structural]
        findings += [f"{display(path)}: {w}" for w in warned]
        lint_file(path, vocab, findings)

    for line in findings:
        print(f"WARN  {line}")
    for line in errors:
        print(f"ERROR {line}")
    if errors:
        print(f"Skins lint FAILED: {len(errors)} structural errors in {len(files)} files")
        return 1
    if findings and args.strict:
        return 1
    print(
        f"Skins lint passed: {len(files)} files against "
        f"{len(vocab)}-element vocabulary, {len(findings)} warnings"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
