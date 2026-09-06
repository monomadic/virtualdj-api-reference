#!/usr/bin/env python3
"""Generate the machine-readable VDJScript verb index from the ARTIFACTS.

This used to parse `docs/VDJScript Verbs.md` — correct when hand-authored prose
was the best evidence here, backwards once the verb table decided existence.
The index is consumed by `lint_mappers.py` and `verbdb.py bootstrap`, so
building it from the weaker source was a live correctness defect, not a tidiness
one: every editor-hidden verb was missing, and `lint_mappers.py` called
`flip_record`, `flip_play` and `get_pad_page_name` "unknown verbs" while all
three were real and locally tested.

Sources now, strongest first:

- `tests/verb-table.json` — VirtualDJ's own verb table. Decides EXISTENCE
  (membership proves, absence disproves) and ALIASES (records sharing an `id`
  are one verb; `flags & 1` marks the alias spelling, so the canonical is the
  member without it).
- `docs/vdjscript-verbs.json` — the record store, for the curated layer the
  table has no room for: tier, section, description, example, kind, surfaces.
- `docs/Official VDJScript Coverage Audit.md` — the official-name set.

The output schema is unchanged, so both consumers keep working.

Store names absent from the verb table are kept and marked `not_in_verb_table`,
because they are the cases the table is silent on rather than negative about:
mapper/skin structural keywords (`ONINIT`, `while_pressed`, `deck`) and names
this repo disproved (`browser_filter`, `browser_search`, `none`), whose disproof
is worth keeping addressable.

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
VERB_TABLE = ROOT / "tests" / "verb-table.json"
STORE = ROOT / "docs" / "vdjscript-verbs.json"
OUTPUT = ROOT / "docs" / "vdjscript-verb-index.json"
# Curated fields the verb table has no room for; copied through from the store.
STORE_FIELDS = ("section", "description", "example", "kind", "surfaces")

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


def load_json(path: Path, key: str = "verbs") -> dict:
    data = json.loads(path.read_text())
    return data[key] if isinstance(data, dict) and key in data else data


def alias_groups(table: dict) -> tuple[dict[str, str], dict[str, list[str]]]:
    """(alias -> canonical, canonical -> aliases), straight from shared ids."""
    by_id: dict[int, list[tuple[str, int]]] = {}
    for name, rec in table.items():
        if isinstance(rec, dict) and "id" in rec:
            by_id.setdefault(rec["id"], []).append((name, rec.get("flags", 0)))
    canonical_of, aliases_of = {}, {}
    for members in by_id.values():
        if len(members) < 2:
            continue
        heads = [n for n, f in members if not f & 1]
        # A group with no unflagged member has no canonical to point at; take
        # the first name alphabetically and keep the group rather than drop it.
        head = heads[0] if heads else sorted(n for n, _ in members)[0]
        rest = sorted(n for n, _ in members if n != head)
        if not rest:
            continue
        aliases_of[head] = rest
        for alias in rest:
            canonical_of[alias] = head
    return canonical_of, aliases_of


def build_index() -> dict:
    table = load_json(VERB_TABLE)
    store = load_json(STORE)
    official_names = parse_official_names()
    canonical_of, aliases_of = alias_groups(table)

    verbs: dict[str, dict] = {}
    for name in table:
        if name in canonical_of:
            verbs[name] = {"tier": "alias", "canonical": canonical_of[name]}
            continue
        record = store.get(name) or {}
        entry: dict = {"tier": record.get("tier") or "official-name-only"}
        for field in STORE_FIELDS:
            value = record.get(field)
            if value:
                entry[field] = value
        if name in aliases_of:
            entry["aliases"] = aliases_of[name]
        verbs[name] = entry

    # Names the store carries that the table does not list. The table is silent
    # on these rather than negative, so they stay addressable and say so.
    for name, record in store.items():
        if name in verbs or not isinstance(record, dict):
            continue
        entry = {"tier": record.get("tier") or "official-name-only",
                 "not_in_verb_table": True}
        for field in STORE_FIELDS:
            value = record.get(field)
            if value:
                entry[field] = value
        verbs[name] = entry

    for name in official_names:
        verbs.setdefault(name, {"tier": "official-name-only",
                                "not_in_verb_table": True})

    for name, entry in verbs.items():
        entry["official"] = name in official_names

    counts = {"total": len(verbs)}
    for tier in ("curated", "catalog", "alias", "official-name-only"):
        counts[tier] = sum(1 for v in verbs.values() if v["tier"] == tier)
    counts["official"] = sum(1 for v in verbs.values() if v["official"])
    counts["not_in_verb_table"] = sum(1 for v in verbs.values()
                                      if v.get("not_in_verb_table"))
    return {
        "_meta": {
            "generated_by": "tools/extract_verb_index.py",
            "source": ("tests/verb-table.json + docs/vdjscript-verbs.json + "
                       "docs/Official VDJScript Coverage Audit.md"),
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
