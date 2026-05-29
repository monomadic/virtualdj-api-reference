#!/usr/bin/env python3
"""Extract VDJScript implementation-symbol evidence from the VirtualDJ binary.

This is a read-only helper. It does not disassemble the executable; it only
uses the Mach-O symbol table to summarize parser/editor anchors and ACTION_*
implementation capabilities.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from collections import defaultdict
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
    anchors: list[str] = []
    for line in lines:
        if not any(marker in line for marker in ANCHOR_MARKERS):
            continue
        if any(skip in line for skip in ANCHOR_SKIP):
            continue
        anchors.append(line)
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
    anchors = parser_anchors(lines)

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
        for anchor in anchors:
            print(f"  {anchor}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
