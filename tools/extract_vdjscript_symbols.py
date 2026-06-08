#!/usr/bin/env python3
"""Extract VDJScript implementation-symbol evidence from the VirtualDJ binary.

This is a read-only helper. It does not disassemble the executable; it only
uses the Mach-O symbol table to summarize parser/editor anchors and ACTION_*
implementation capabilities.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


DEFAULT_APP = Path("/Applications/VirtualDJ.app")
ACTION_METHOD_RE = re.compile(
    r"\b(ACTION_[A-Za-z0-9_]+)::"
    r"(onExecute|onQuery|onQueryBool|onQueryText|onQueryController|"
    r"onQueryBoolController|onTooltip)\("
)
ANCHOR_MARKERS = (
    "CActionEdit::",
    "DLGActionWizard::",
    "CSkinEngine::createAction",
    "IController::execute",
    "CMacroEngine::addAction",
    "SActionParam::",
)
ANCHOR_SKIP = ("std::__1::__function", "typeinfo", "vtable", "guard variable")
NM_SYMBOL_PREFIXES = (
    "non-external (was a private external) ",
    "non-external ",
    "private external ",
    "weak private external ",
    "weak external ",
    "external ",
)


@dataclass(frozen=True)
class AnchorRow:
    address: str
    group: str
    symbol: str


def demangled_symbols(app: Path, arch: str) -> list[str]:
    binary = app / "Contents/MacOS/VirtualDJ"
    raw = subprocess.check_output(["nm", "-arch", arch, "-m", str(binary)], text=True)
    return subprocess.check_output(["c++filt"], input=raw, text=True).splitlines()


def action_capabilities(lines: list[str]) -> dict[str, set[str]]:
    actions: dict[str, set[str]] = defaultdict(set)
    for line in lines:
        match = ACTION_METHOD_RE.search(line)
        if not match:
            continue
        class_name, method = match.groups()
        action_name = class_name.removeprefix("ACTION_")
        actions[action_name].add(method)
    return actions


def parser_anchors(lines: list[str]) -> list[str]:
    return [f"{row.address} {row.symbol}" for row in parser_anchor_rows(lines)]


def symbol_name(line: str) -> str:
    section_match = re.match(r"^[0-9a-fA-F]+\s+\([^)]*\)\s+(.*)$", line)
    symbol = section_match.group(1) if section_match else line
    for prefix in NM_SYMBOL_PREFIXES:
        if symbol.startswith(prefix):
            return symbol.removeprefix(prefix)
    return symbol


def symbol_address(line: str) -> str:
    return line.split(None, 1)[0]


def anchor_group(symbol: str) -> str:
    if symbol.startswith("CActionEdit::"):
        return "editor_dialog"
    if "CSkinEngine::createAction" in symbol or "CMacroEngine::addAction" in symbol or "IController::execute" in symbol:
        return "runtime_create_execute"
    if symbol.startswith("SActionParam::") or " SActionParam::" in symbol:
        return "action_param"
    if "DLGActionWizard::STree::" in symbol or "DLGActionWizard::SItem" in symbol:
        return "syntax_tree"
    if any(
        marker in symbol
        for marker in (
            "customDraw",
            "setPosition",
            "posToRealPos",
            "realPosToPos",
            "posToXY",
            "xyToPos",
        )
    ):
        return "render_position"
    if any(
        marker in symbol
        for marker in (
            "getCurrentWord",
            "onTouchOver",
            "onTouchOverLeave",
            "onTouchRelease",
            "updateHint",
            "setHelp",
            "onHelp",
        )
    ):
        return "hover_help"
    if any(marker in symbol for marker in ("onCategory", "updateList", "onList", "deckArguments")):
        return "catalog_list"
    if symbol.startswith("DLGActionWizard::"):
        return "wizard_lifecycle"
    return "other"


def parser_anchor_rows(lines: list[str]) -> list[AnchorRow]:
    anchors: list[AnchorRow] = []
    for line in lines:
        if not any(marker in line for marker in ANCHOR_MARKERS):
            continue
        if any(skip in line for skip in ANCHOR_SKIP):
            continue
        symbol = symbol_name(line)
        anchors.append(AnchorRow(symbol_address(line), anchor_group(symbol), symbol))
    return anchors


def method_count(actions: dict[str, set[str]], method: str) -> int:
    return sum(1 for methods in actions.values() if method in methods)


def print_name_list(title: str, names: list[str], limit: int) -> None:
    print(f"{title}: {len(names)}")
    if not names:
        return
    shown = names[:limit]
    print("  " + ", ".join(shown))
    if len(names) > limit:
        print(f"  ... {len(names) - limit} more")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=Path, default=DEFAULT_APP)
    parser.add_argument("--arch", default="arm64")
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument(
        "--show-anchors",
        action="store_true",
        help="Print parser/editor anchor symbol lines",
    )
    parser.add_argument(
        "--anchors-format",
        choices=("csv", "json"),
        help="Print only structured parser/editor anchor rows",
    )
    args = parser.parse_args()

    lines = demangled_symbols(args.app, args.arch)
    actions = action_capabilities(lines)
    query_methods = {"onQuery", "onQueryBool", "onQueryText", "onQueryController", "onQueryBoolController"}
    execute_names = sorted(name for name, methods in actions.items() if "onExecute" in methods)
    query_names = sorted(name for name, methods in actions.items() if methods & query_methods)
    text_query_names = sorted(name for name, methods in actions.items() if "onQueryText" in methods)
    bool_query_names = sorted(name for name, methods in actions.items() if "onQueryBool" in methods)
    tooltip_names = sorted(name for name, methods in actions.items() if "onTooltip" in methods)
    execute_only = sorted(name for name, methods in actions.items() if "onExecute" in methods and not methods & query_methods)
    query_only = sorted(name for name, methods in actions.items() if methods & query_methods and "onExecute" not in methods)
    anchor_rows = parser_anchor_rows(lines)
    anchors = [f"{row.address} {row.symbol}" for row in anchor_rows]

    if args.anchors_format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=list(asdict(anchor_rows[0]).keys()) if anchor_rows else [])
        writer.writeheader()
        for row in anchor_rows:
            writer.writerow(asdict(row))
        return 0
    if args.anchors_format == "json":
        print(json.dumps([asdict(row) for row in anchor_rows], indent=2, sort_keys=True))
        return 0

    print(f"App: {args.app}")
    print(f"Architecture: {args.arch}")
    print(f"Demangled symbol lines: {len(lines)}")
    print(f"ACTION_* implementation classes: {len(actions)}")
    print(f"  with onExecute: {method_count(actions, 'onExecute')}")
    print(f"  with onQuery: {method_count(actions, 'onQuery')}")
    print(f"  with onQueryBool: {method_count(actions, 'onQueryBool')}")
    print(f"  with onQueryText: {method_count(actions, 'onQueryText')}")
    print(f"  with onTooltip: {method_count(actions, 'onTooltip')}")
    print(f"Parser/editor anchor symbols: {len(anchors)}")
    group_counts: dict[str, int] = defaultdict(int)
    for row in anchor_rows:
        group_counts[row.group] += 1
    for group, count in sorted(group_counts.items()):
        print(f"  {group}: {count}")
    print()

    print_name_list("Query-capable ACTION classes", query_names, args.limit)
    print_name_list("Execute-only ACTION classes", execute_only, args.limit)
    print_name_list("Query-only ACTION classes", query_only, args.limit)
    print_name_list("Text-query ACTION classes", text_query_names, args.limit)
    print_name_list("Bool-query ACTION classes", bool_query_names, args.limit)
    print_name_list("Tooltip-aware ACTION classes", tooltip_names, args.limit)

    if args.show_anchors:
        print()
        print("Parser/editor anchors:")
        current_group = None
        for row in sorted(anchor_rows, key=lambda item: (item.group, item.address, item.symbol)):
            if row.group != current_group:
                current_group = row.group
                print(f"  [{current_group}]")
            print(f"    {row.address} {row.symbol}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
