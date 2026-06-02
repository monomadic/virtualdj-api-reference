#!/usr/bin/env python3
"""Join VDJScript taxonomy, catalog, official-name, and symbol capability evidence.

This is a read-only helper that combines:

- compiled Button Editor taxonomy rows
- bundled language-catalog presence
- official appendix audit presence
- ACTION_* implementation methods from the Mach-O symbol table
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from extract_vdjscript_catalogs import DEFAULT_AUDIT, official_names
from extract_vdjscript_symbols import action_capabilities, demangled_symbols
from extract_vdjscript_taxonomy import (
    CPU_TYPES,
    DEFAULT_ACTION_ITEMS_VA,
    DEFAULT_APP,
    DEFAULT_CATEGORY_IDS_VA,
    DEFAULT_CATEGORY_NAMES_VA,
    MachOReader,
    category_names,
    filtered_entries,
    language_action_union,
    taxonomy_entries,
)


QUERY_METHODS = {
    "onQuery",
    "onQueryBool",
    "onQueryText",
    "onQueryController",
    "onQueryBoolController",
}
METHOD_ORDER = (
    "onExecute",
    "onQuery",
    "onQueryBool",
    "onQueryText",
    "onQueryController",
    "onQueryBoolController",
    "onTooltip",
)


@dataclass(frozen=True)
class MetadataRow:
    name: str
    category: str
    category_id: str
    action_id: str
    taxonomy_visible: bool
    flag0_hidden: bool
    flag1_hidden: bool
    taxonomy_flags: str
    in_official_audit: bool
    in_language_catalog: bool
    has_action_class: bool
    has_execute: bool
    has_query: bool
    has_query_bool: bool
    has_query_text: bool
    has_query_controller: bool
    has_query_bool_controller: bool
    has_tooltip: bool
    capability_bucket: str
    symbol_methods: str


def capability_bucket(methods: set[str]) -> str:
    has_execute = "onExecute" in methods
    has_query = bool(methods & QUERY_METHODS)
    if has_execute and has_query:
        return "execute+query"
    if has_execute:
        return "execute-only"
    if has_query:
        return "query-only"
    if "onTooltip" in methods:
        return "tooltip-only"
    return "no-action-class"


def metadata_rows(
    taxonomy,
    official: set[str],
    language: set[str],
    capabilities: dict[str, set[str]],
    include_external: bool,
) -> list[MetadataRow]:
    rows: list[MetadataRow] = []
    taxonomy_by_name = {entry.name: entry for entry in taxonomy}
    names = set(taxonomy_by_name)
    if include_external:
        names.update(official)
        names.update(language)
        names.update(capabilities)

    for name in sorted(names):
        entry = taxonomy_by_name.get(name)
        methods = capabilities.get(name, set())
        ordered_methods = [method for method in METHOD_ORDER if method in methods]
        rows.append(
            MetadataRow(
                name=name,
                category=entry.category if entry else "",
                category_id=str(entry.category_id) if entry else "",
                action_id=str(entry.action_id) if entry else "",
                taxonomy_visible=entry.visible if entry else False,
                flag0_hidden=entry.flag0_hidden if entry else False,
                flag1_hidden=entry.flag1_hidden if entry else False,
                taxonomy_flags=entry.flags if entry else "",
                in_official_audit=name in official,
                in_language_catalog=name in language,
                has_action_class=bool(methods),
                has_execute="onExecute" in methods,
                has_query=bool(methods & QUERY_METHODS),
                has_query_bool="onQueryBool" in methods,
                has_query_text="onQueryText" in methods,
                has_query_controller="onQueryController" in methods,
                has_query_bool_controller="onQueryBoolController" in methods,
                has_tooltip="onTooltip" in methods,
                capability_bucket=capability_bucket(methods),
                symbol_methods="|".join(ordered_methods),
            )
        )
    return rows


def print_summary(rows: list[MetadataRow], include_external: bool) -> None:
    visible_rows = [row for row in rows if row.taxonomy_visible]
    taxonomy_rows = [row for row in rows if row.category]
    official_rows = [row for row in rows if row.in_official_audit]
    language_rows = [row for row in rows if row.in_language_catalog]
    action_class_rows = [row for row in rows if row.has_action_class]
    buckets = Counter(row.capability_bucket for row in rows)
    visible_buckets = Counter(row.capability_bucket for row in visible_rows)

    print(f"Rows: {len(rows)}")
    print(f"Include external non-taxonomy names: {str(include_external).lower()}")
    print(f"Compiled taxonomy rows: {len(taxonomy_rows)}")
    print(f"Visible taxonomy rows: {len(visible_rows)}")
    print(f"Official audit names in matrix: {len(official_rows)}")
    print(f"Language-catalog names in matrix: {len(language_rows)}")
    print(f"Rows with exact ACTION_* class match: {len(action_class_rows)}")
    print()
    print("Capability buckets:")
    for bucket, count in sorted(buckets.items()):
        print(f"  {bucket}: {count}")
    print()
    print("Visible Button Editor capability buckets:")
    for bucket, count in sorted(visible_buckets.items()):
        print(f"  {bucket}: {count}")
    print()
    print("Visible taxonomy rows without exact ACTION_* class match:")
    missing_visible = [row.name for row in visible_rows if not row.has_action_class]
    print(f"  {len(missing_visible)}")
    if missing_visible:
        print("  " + ", ".join(missing_visible[:80]))
    print()
    print("Exact ACTION_* classes not in compiled taxonomy:")
    symbol_only = [row.name for row in rows if row.has_action_class and not row.category]
    print(f"  {len(symbol_only)}")
    if symbol_only:
        print("  " + ", ".join(symbol_only[:80]))


def write_csv(rows: list[MetadataRow]) -> None:
    writer = csv.DictWriter(sys.stdout, fieldnames=list(asdict(rows[0]).keys()) if rows else [])
    writer.writeheader()
    for row in rows:
        writer.writerow(asdict(row))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=Path, default=DEFAULT_APP)
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--arch", choices=sorted(CPU_TYPES), default="arm64")
    parser.add_argument("--category", help="Limit taxonomy rows to one category")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden taxonomy entries")
    parser.add_argument(
        "--include-external",
        action="store_true",
        help="Also include official/language/symbol names that are not in the compiled taxonomy",
    )
    parser.add_argument("--format", choices=("summary", "csv", "json", "names"), default="summary")
    parser.add_argument("--category-names-va", type=lambda text: int(text, 0), default=DEFAULT_CATEGORY_NAMES_VA)
    parser.add_argument("--action-items-va", type=lambda text: int(text, 0), default=DEFAULT_ACTION_ITEMS_VA)
    parser.add_argument("--category-ids-va", type=lambda text: int(text, 0), default=DEFAULT_CATEGORY_IDS_VA)
    args = parser.parse_args()

    reader = MachOReader(args.app / "Contents/MacOS/VirtualDJ", args.arch)
    language = language_action_union(args.app)
    official = official_names(args.audit)
    categories = category_names(reader, args.category_names_va)
    taxonomy = taxonomy_entries(
        reader,
        categories,
        language,
        args.action_items_va,
        args.category_ids_va,
    )
    taxonomy = filtered_entries(taxonomy, args.category, args.include_hidden)
    capabilities = action_capabilities(demangled_symbols(args.app, args.arch))
    rows = metadata_rows(taxonomy, official, language, capabilities, args.include_external)

    if args.format == "summary":
        print_summary(rows, args.include_external)
    elif args.format == "csv":
        write_csv(rows)
    elif args.format == "json":
        print(json.dumps([asdict(row) for row in rows], indent=2, sort_keys=True))
    elif args.format == "names":
        for row in rows:
            print(row.name)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
