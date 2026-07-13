#!/usr/bin/env python3
"""Extract local VDJScript catalog evidence from an installed VirtualDJ app.

This is a read-only helper for comparing three local sources:

- bundled language action descriptions in Resources/languages.zip
- verb-looking runtime strings in the Mach-O executable
- this repo's official appendix coverage audit
"""

from __future__ import annotations

import argparse
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile


DEFAULT_APP = Path("/Applications/VirtualDJ.app")
DEFAULT_AUDIT = Path("docs/Official VDJScript Coverage Audit.md")
DEFAULT_XML_ROOTS = (
    Path("examples/Pads/Built-In"),
    Path("examples/Skins/Built-In"),
    Path("examples/Samplerbanks/Built-In"),
)


def language_catalogs(app: Path) -> dict[str, dict[str, set[str]]]:
    zip_path = app / "Contents/Resources/languages.zip"
    catalogs: dict[str, dict[str, set[str]]] = {}
    with ZipFile(zip_path) as archive:
        for name in archive.namelist():
            if not name.endswith(".xml"):
                continue
            root = ET.fromstring(archive.read(name))
            catalogs[name] = {}
            for section in ("Actions", "tooltips", "skintooltips"):
                node = root.find(section)
                catalogs[name][section] = {child.tag for child in node} if node is not None else set()
    return catalogs


def binary_action_block(app: Path, block_number: int) -> set[str]:
    binary = app / "Contents/MacOS/VirtualDJ"
    output = subprocess.check_output(["strings", "-a", str(binary)], text=True, errors="ignore")
    block: list[str] = []
    current = 0
    capture = False
    for line in output.splitlines():
        if line == "action_deck":
            current += 1
            capture = True
        if capture and current == block_number:
            block.append(line)
        if line == "zoom_vertical" and capture:
            capture = False
    return set(block)


def official_names(audit: Path) -> set[str]:
    text = audit.read_text()
    marker = "## Covered Official Names"
    start = text.find(marker)
    if start != -1:
        end = text.find("\n## ", start + len(marker))
        section = text[start:end] if end != -1 else text[start:]
        names = set(re.findall(r"`([a-z][a-z0-9_]*)`", section))
        if names:
            return names
    return set(re.findall(r"`([a-z][a-z0-9_]*)`", text))


def print_delta(title: str, left: set[str], right: set[str]) -> None:
    delta = sorted(left - right)
    print(f"{title}: {len(delta)}")
    if delta:
        print("  " + ", ".join(delta))


def shipped_xml_hits(names: set[str], roots: tuple[Path, ...]) -> dict[str, list[str]]:
    files = [path for root in roots if root.exists() for path in root.rglob("*.xml")]
    hits: dict[str, list[str]] = {}
    for name in sorted(names):
        pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])")
        for path in files:
            text = path.read_text(errors="ignore")
            for lineno, line in enumerate(text.splitlines(), 1):
                if pattern.search(line):
                    hits.setdefault(name, []).append(f"{path}:{lineno}")
                    break
    return hits


def print_xml_hits(title: str, hits: dict[str, list[str]]) -> None:
    print(f"{title}: {len(hits)}")
    if not hits:
        print("  None")
        return
    for name, locations in sorted(hits.items()):
        print(f"  {name}: " + "; ".join(locations[:8]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=Path, default=DEFAULT_APP)
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--binary-block", type=int, default=2)
    parser.add_argument(
        "--xml-root",
        action="append",
        type=Path,
        dest="xml_roots",
        help="Root to scan for shipped XML evidence; repeat to override defaults",
    )
    args = parser.parse_args()

    catalogs = language_catalogs(args.app)
    english = catalogs["English.xml"]["Actions"]
    action_union = set().union(*(catalog["Actions"] for catalog in catalogs.values()))
    action_intersection = set.intersection(*(catalog["Actions"] for catalog in catalogs.values()))
    tooltips_union = set().union(*(catalog["tooltips"] for catalog in catalogs.values()))
    skintips_union = set().union(*(catalog["skintooltips"] for catalog in catalogs.values()))
    binary = binary_action_block(args.app, args.binary_block)
    official = official_names(args.audit)
    xml_roots = tuple(args.xml_roots) if args.xml_roots else DEFAULT_XML_ROOTS
    button_not_official = action_union - official
    runtime_only = binary - official - action_union
    non_official_candidates = button_not_official | runtime_only

    print(f"App: {args.app}")
    print(f"Languages: {len(catalogs)}")
    print(f"English Actions: {len(english)}")
    print(f"Actions union: {len(action_union)}")
    print(f"Actions present in every language: {len(action_intersection)}")
    print(f"Tooltips union: {len(tooltips_union)}")
    print(f"Skin tooltips union: {len(skintips_union)}")
    print(f"Binary action block {args.binary_block}: {len(binary)}")
    print(f"Official audit names: {len(official)}")
    print()

    varying = action_union - action_intersection
    print(f"Language-varying action tags: {len(varying)}")
    if varying:
        print("  " + ", ".join(sorted(varying)))
    print()

    print_delta("Action union not in official audit", action_union, official)
    print_delta("Official audit not in action union", official, action_union)
    print_delta("Action union not in binary block", action_union, binary)
    print_delta("Binary block not in action union", binary, action_union)
    print_delta("Binary block not in official audit or action union", binary, official | action_union)
    print()
    print("Shipped XML evidence roots:")
    for root in xml_roots:
        print(f"  {root}")
    print_xml_hits(
        "Non-official candidates with shipped XML evidence",
        shipped_xml_hits(non_official_candidates, xml_roots),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
