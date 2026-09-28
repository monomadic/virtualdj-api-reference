#!/usr/bin/env python3
"""Lint VirtualDJ pad page XML files.

With no arguments, lints the repo's pad pages. Given paths, lints only those
files; a pad_page target that resolves to neither them nor a repo page is then a
warning, since it may name a page installed outside the repo.
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PADS_DIR = ROOT / "examples" / "Pads"
TEST_PADS_DIR = ROOT / "tests" / "Pads"
PAD_PAGE_REF = re.compile(r"\bpad_page\s+['\"]([^'\"]+)['\"]")
FILTER_SELECT_IN_QUERY = re.compile(
    r"\bquery\s*=\s*(['\"])(?:(?!\1).)*\bfilter_selectcolorfx\b",
    re.IGNORECASE,
)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def display(path: Path) -> Path:
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def repo_pad_files() -> list[Path]:
    return sorted(PADS_DIR.glob("*.xml")) + sorted(TEST_PADS_DIR.rglob("*.xml"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="pad page XML files (default: repo pad pages)")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    page_names: dict[Path, str] = {}
    names_to_paths: dict[str, list[Path]] = defaultdict(list)
    refs: list[tuple[Path, int, str]] = []

    explicit = bool(args.paths)
    pad_files = [Path(p).resolve() for p in args.paths] if explicit else repo_pad_files()
    if not pad_files:
        errors.append("no pad XML files found in Pads/ or Test/Pads/")

    for path in pad_files:
        rel = display(path)
        try:
            text = path.read_text(encoding="utf-8-sig")
        except OSError as exc:
            errors.append(f"{rel}: cannot read: {exc.strerror}")
            continue

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
            files = ", ".join(str(display(path)) for path in paths)
            errors.append(f"duplicate pad page name {name!r}: {files}")

    valid_names = set(page_names.values())
    known_names = set(valid_names)
    if explicit:
        for path in repo_pad_files():
            try:
                known_names.add((ET.parse(path).getroot().get("name") or "").strip())
            except ET.ParseError:
                pass
    for path, line, target in refs:
        if target not in known_names:
            (warnings if explicit else errors).append(
                f"{display(path)}:{line}: pad_page target {target!r} "
                "does not match any known pad page name"
            )

    for warning in warnings:
        print(f"WARN  {warning}")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Pads lint passed: {len(pad_files)} XML files, {len(valid_names)} page names, "
          f"{len(warnings)} warnings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
