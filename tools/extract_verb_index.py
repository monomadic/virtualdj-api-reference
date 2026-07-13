#!/usr/bin/env python3
"""Generate a machine-readable VDJScript verb index from docs/VDJScript Verbs.md.

Offline. Parses three layers of the curated verb reference:

- the High-Frequency Alias Index table (canonical -> official aliases),
- curated ``### `verb` `` entries (Aliases / Kind / Typical surfaces fields),
- broad-catalog table rows after the "## Broad Verb Index" marker.

Output: docs/vdjscript-verb-index.json, sorted by name. Curated entries win
over catalog rows for the same name. Alias names get their own rows pointing
at the canonical verb so lookup tools can resolve either spelling.

Usage:
  python3 tools/extract_verb_index.py           # regenerate the JSON
  python3 tools/extract_verb_index.py --check   # exit 1 if committed JSON is stale
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "VDJScript Verbs.md"
AUDIT = ROOT / "docs" / "Official VDJScript Coverage Audit.md"
OUTPUT = ROOT / "docs" / "vdjscript-verb-index.json"

CURATED_HEADING = re.compile(r"^### `([^`]+)`\s*$")
SECTION_HEADING = re.compile(r"^## (.+?)\s*$")
BACKTICKED = re.compile(r"`([^`]+)`")
TABLE_ROW = re.compile(r"^\|(.+)\|\s*$")
BROAD_MARKER = "## Broad Verb Index"
ALIAS_MARKER = "## High-Frequency Alias Index"

VERB_NAME = re.compile(r"^[a-z0-9_]+$")


def split_cells(row_line: str) -> list[str]:
    body = row_line.strip().strip("|")
    cells, cur, depth = [], [], 0
    for ch in body:
        if ch == "`":
            depth ^= 1
        if ch == "|" and depth == 0:
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    cells.append("".join(cur).strip())
    return cells


def parse_alias_index(lines: list[str]) -> dict[str, list[str]]:
    aliases: dict[str, list[str]] = {}
    in_section = False
    for line in lines:
        if line.startswith(ALIAS_MARKER):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("|"):
            continue
        cells = split_cells(line)
        if len(cells) < 2 or cells[0].startswith("---") or cells[0] == "Canonical":
            continue
        canonical = BACKTICKED.findall(cells[0])
        official = BACKTICKED.findall(cells[1])
        if canonical:
            aliases[canonical[0]] = official
    return aliases


def parse_curated(lines: list[str]) -> dict[str, dict]:
    entries: dict[str, dict] = {}
    broad_at = next((i for i, l in enumerate(lines) if l.startswith(BROAD_MARKER)), len(lines))
    i = 0
    while i < broad_at:
        match = CURATED_HEADING.match(lines[i])
        if not match:
            i += 1
            continue
        name = match.group(1)
        entry: dict = {"tier": "curated"}
        j = i + 1
        while j < broad_at and not CURATED_HEADING.match(lines[j]) and not lines[j].startswith("## "):
            line = lines[j]
            if line.startswith("Aliases:"):
                found = BACKTICKED.findall(line)
                entry["aliases"] = found
            elif line.startswith("Kind:"):
                found = BACKTICKED.findall(line)
                if found:
                    entry["kind"] = found[0]
            elif line.startswith("Typical surfaces:"):
                entry["surfaces"] = BACKTICKED.findall(line)
            j += 1
        entries[name] = entry
        i = j
    return entries


def parse_catalog(lines: list[str]) -> dict[str, dict]:
    entries: dict[str, dict] = {}
    in_broad = False
    section = ""
    for line in lines:
        if line.startswith(BROAD_MARKER):
            in_broad = True
            continue
        if not in_broad:
            continue
        heading = SECTION_HEADING.match(line)
        if heading:
            section = heading.group(1)
            continue
        if not line.startswith("|"):
            continue
        cells = split_cells(line)
        if len(cells) < 2:
            continue
        names = BACKTICKED.findall(cells[0])
        names = [n for n in names if VERB_NAME.match(n)]
        if not names:
            continue
        description = cells[1] if len(cells) > 1 else ""
        example = BACKTICKED.findall(cells[2])[0] if len(cells) > 2 and BACKTICKED.findall(cells[2]) else ""
        primary = names[0]
        entry = {
            "tier": "catalog",
            "section": section,
            "description": description,
        }
        if example:
            entry["example"] = example
        if len(names) > 1:
            entry["aliases"] = names[1:]
        entries.setdefault(primary, entry)
    return entries


def parse_official_names() -> set[str]:
    """Full official-name list from the coverage audit's Covered section."""
    text = AUDIT.read_text()
    match = re.search(r"## Covered Official Names(.*?)(?:\n## |\Z)", text, re.S)
    if not match:
        return set()
    return set(re.findall(r"`([a-z0-9_]+)`", match.group(1)))


def build_index() -> dict:
    lines = SOURCE.read_text().splitlines()
    alias_index = parse_alias_index(lines)
    curated = parse_curated(lines)
    catalog = parse_catalog(lines)
    official_names = parse_official_names()

    verbs: dict[str, dict] = {}
    for name, entry in catalog.items():
        verbs[name] = entry
    for name, entry in curated.items():
        merged = dict(verbs.get(name, {}))
        merged.update(entry)
        # curated tier wins, but keep catalog description/section for context
        merged["tier"] = "curated"
        verbs[name] = merged
    for canonical, official in alias_index.items():
        if canonical in verbs:
            existing = set(verbs[canonical].get("aliases", []))
            existing.update(official)
            existing.discard("none")
            if existing:
                verbs[canonical]["aliases"] = sorted(existing)

    # alias rows resolve to their canonical verb
    for name in list(verbs):
        for alias in verbs[name].get("aliases", []):
            if alias and alias != "none" and alias not in verbs:
                verbs[alias] = {"tier": "alias", "canonical": name}

    # official appendix names without a dedicated row become name-only entries
    for name in official_names:
        if name not in verbs:
            verbs[name] = {"tier": "official-name-only"}

    for name, entry in verbs.items():
        entry["official"] = name in official_names

    counts = {"total": len(verbs)}
    for tier in ("curated", "catalog", "alias", "official-name-only"):
        counts[tier] = sum(1 for v in verbs.values() if v["tier"] == tier)
    counts["official"] = sum(1 for v in verbs.values() if v["official"])
    return {
        "_meta": {
            "generated_by": "tools/extract_verb_index.py",
            "source": "docs/VDJScript Verbs.md + docs/Official VDJScript Coverage Audit.md",
            "counts": counts,
        },
        "verbs": {name: verbs[name] for name in sorted(verbs)},
    }


def render(index: dict) -> str:
    return json.dumps(index, indent=1, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if committed JSON is stale")
    args = parser.parse_args()

    index = build_index()
    text = render(index)
    counts = index["_meta"]["counts"]
    summary = (
        f"{counts['total']} names ({counts['curated']} curated, "
        f"{counts['catalog']} catalog, {counts['alias']} alias, "
        f"{counts['official-name-only']} official-name-only; "
        f"{counts['official']} official)"
    )

    if args.check:
        if not OUTPUT.exists():
            print(f"{OUTPUT.relative_to(ROOT)} missing; run: python3 tools/extract_verb_index.py")
            return 1
        if OUTPUT.read_text() != text:
            print(f"{OUTPUT.relative_to(ROOT)} is stale; run: python3 tools/extract_verb_index.py")
            return 1
        print(f"Verb index check passed: {summary}")
        return 0

    OUTPUT.write_text(text)
    print(f"Wrote {OUTPUT.relative_to(ROOT)}: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
