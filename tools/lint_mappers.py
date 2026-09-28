#!/usr/bin/env python3
"""Lint VirtualDJ mapper XML files.

Structural checks (errors, exit 1):
- well-formed XML with a `<mapper>` root
- root has a non-empty `device` attribute; only known root attributes
- children are only `<info>` and `<map>`
- every `<map>` has a non-empty `value` and an `action`; only known attributes

The script inside each action is checked by tools/lint_script.py (`--xml`),
against the build-stamped verb table rather than the doc-derived index this
linter used to read: the index still listed names the binary disproves.

Usage:
  python3 tools/lint_mappers.py [paths ...]   # default: examples/Mappers/**/*.xml, minus <device> definitions
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLOB = "examples/Mappers/**/*.xml"

KNOWN_ROOT_ATTRS = {"device", "author", "version", "date", "priority"}
KNOWN_MAP_ATTRS = {"value", "action", "name"}

def lint_file(path: Path, errors: list[str]) -> None:
    # A lint tool asked about a file outside the repo should lint it, not raise:
    # `relative_to` throws on any absolute path elsewhere, which turned a normal
    # "lint this scratch file" into a traceback.
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        rel = path
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


def root_tag(path: Path) -> str | None:
    try:
        for _, elem in ET.iterparse(path, events=("start",)):
            return elem.tag
    except ET.ParseError:
        return None
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="mapper XML files (default: examples/Mappers)")
    args = parser.parse_args()

    if args.paths:
        files = [Path(p).resolve() for p in args.paths]
    else:
        # Controller add-ons ship their <device> definition beside the mapper
        # (examples/Mappers/Official-Addons); discovery skips those, an
        # explicit path still gets the <mapper> root check.
        files = [p for p in sorted(ROOT.glob(DEFAULT_GLOB)) if root_tag(p) != "device"]
    if not files:
        print("No mapper XML files found")
        return 1

    errors: list[str] = []
    for path in files:
        lint_file(path, errors)

    for line in errors:
        print(f"ERROR {line}")
    if errors:
        return 1
    print(f"Mappers lint passed: {len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
