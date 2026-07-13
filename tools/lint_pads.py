#!/usr/bin/env python3
"""Lint local VirtualDJ pad page XML files."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PADS_DIR = ROOT / "xml" / "Pads"
TEST_PADS_DIR = ROOT / "tests" / "Pads"
PAD_PAGE_REF = re.compile(r"\bpad_page\s+['\"]([^'\"]+)['\"]")
FILTER_SELECT_IN_QUERY = re.compile(
    r"\bquery\s*=\s*(['\"])(?:(?!\1).)*\bfilter_selectcolorfx\b",
    re.IGNORECASE,
)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def main() -> int:
    errors: list[str] = []
    page_names: dict[Path, str] = {}
    names_to_paths: dict[str, list[Path]] = defaultdict(list)
    refs: list[tuple[Path, int, str]] = []

    pad_files = sorted(PADS_DIR.glob("*.xml")) + sorted(TEST_PADS_DIR.rglob("*.xml"))
    if not pad_files:
        errors.append("no pad XML files found in Pads/ or Test/Pads/")

    for path in pad_files:
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8-sig")

        try:
            root = ET.fromstring(text)
        except ET.ParseError as exc:
            errors.append(f"{rel}: XML parse error: {exc}")
            continue

        if root.tag != "page":
            errors.append(f"{rel}: root element is <{root.tag}>, expected <page>")

        name = (root.get("name") or "").strip()
        if not name:
            errors.append(f"{rel}: page is missing a non-empty name attribute")
        else:
            page_names[path] = name
            names_to_paths[name].append(path)

        for match in PAD_PAGE_REF.finditer(text):
            refs.append((path, line_number(text, match.start()), match.group(1)))

        for match in FILTER_SELECT_IN_QUERY.finditer(text):
            errors.append(
                f"{rel}:{line_number(text, match.start())}: "
                "query uses filter_selectcolorfx; use filter_label 'name' for read-only selected-state checks"
            )

    for name, paths in sorted(names_to_paths.items()):
        if len(paths) > 1:
            files = ", ".join(str(path.relative_to(ROOT)) for path in paths)
            errors.append(f"duplicate pad page name {name!r}: {files}")

    valid_names = set(page_names.values())
    for path, line, target in refs:
        if target not in valid_names:
            errors.append(
                f"{path.relative_to(ROOT)}:{line}: pad_page target {target!r} "
                "does not match any known pad page name"
            )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Pads lint passed: {len(pad_files)} XML files, {len(valid_names)} page names")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
