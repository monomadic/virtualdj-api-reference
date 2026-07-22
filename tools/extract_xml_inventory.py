#!/usr/bin/env python3
"""Generate an element/attribute inventory of the in-repo XML corpora.

Scans skins, pads, samplerbanks, and mapper XML with a tolerant tokenizer
(built-in skin XML is not strict XML: raw `&`, `&&`, and `>` appear inside
quoted attribute values), cross-checks element names against the reference
docs, and writes the data artifact `docs/skin-xml-inventory.json`.
Query it with `just get-xml-element` / `find-xml-elements` / `xml-stats`;
no Markdown view is written to disk.

Usage:
    python3 tools/extract_xml_inventory.py           # (re)write the report
    python3 tools/extract_xml_inventory.py --check   # fail on new undocumented elements
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
import json
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "skin-xml-inventory.json"

# family name -> (glob patterns, reference docs to cross-check)
FAMILIES: list[tuple[str, list[str], list[str]]] = [
    (
        "skins",
        [
            "examples/Skins/Built-In/**/*.xml",
            "examples/Skins/SDK Example - Custom Browser Skin/skin.xml",
            "examples/Skins/ModularSkeleton/build/*.xml",
            "examples/Skins/GraveRaver/build/*.xml",
            "tests/Skins/**/*.xml",
        ],
        ["docs/Skin SDK.md", "docs/Skin Waveforms.md"],
    ),
    (
        "pads",
        ["examples/Pads/**/*.xml", "tests/Pads/*.xml"],
        ["docs/Pad Page XML.md", "docs/Example Pad XML Pages.md"],
    ),
    (
        "video_skins",
        ["examples/VideoSkins/**/*.xml"],
        ["docs/Skin SDK.md", "docs/Skin Waveforms.md"],
    ),
    (
        "samplerbanks",
        ["examples/Samplerbanks/**/*.xml"],
        [],
    ),
    (
        "mappers",
        ["examples/Mappers/**/*.xml"],
        ["docs/Mapper XML.md"],
    ),
]

NAME_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.:-]*")


@dataclass
class ElementStats:
    uses: int = 0
    files: set[str] = field(default_factory=set)
    attributes: Counter = field(default_factory=Counter)


def scan_tags(text: str) -> list[tuple[str, list[str]]]:
    """Tolerantly tokenize open tags: returns (element, [attribute names]).

    Quote-aware so `>` / `<` / raw `&` inside quoted attribute values (VDJScript
    ternaries etc.) do not break tag detection. Skips comments, CDATA, prolog,
    doctype, and closing tags.
    """
    tags: list[tuple[str, list[str]]] = []
    i = 0
    n = len(text)
    while True:
        i = text.find("<", i)
        if i == -1:
            break
        if text.startswith("<!--", i):
            end = text.find("-->", i + 4)
            i = n if end == -1 else end + 3
            continue
        if text.startswith("<![CDATA[", i):
            end = text.find("]]>", i + 9)
            i = n if end == -1 else end + 3
            continue
        if text.startswith("<?", i) or text.startswith("<!", i):
            end = text.find(">", i)
            i = n if end == -1 else end + 1
            continue
        if text.startswith("</", i):
            end = text.find(">", i)
            i = n if end == -1 else end + 1
            continue
        match = NAME_RE.match(text, i + 1)
        if not match:
            i += 1
            continue
        name = match.group(0).lower()
        k = match.end()
        attrs: list[str] = []
        while k < n:
            c = text[k]
            if c == ">":
                k += 1
                break
            if c in " \t\r\n/":
                k += 1
                continue
            attr_match = NAME_RE.match(text, k)
            if not attr_match:
                k += 1
                continue
            attrs.append(attr_match.group(0).lower())
            k = attr_match.end()
            while k < n and text[k] in " \t\r\n":
                k += 1
            if k < n and text[k] == "=":
                k += 1
                while k < n and text[k] in " \t\r\n":
                    k += 1
                if k < n and text[k] in "\"'":
                    quote = text[k]
                    end = text.find(quote, k + 1)
                    k = n if end == -1 else end + 1
                else:
                    while k < n and text[k] not in " \t\r\n>":
                        k += 1
        tags.append((name, attrs))
        i = k
    return tags


def collect_family(patterns: list[str]) -> tuple[dict[str, ElementStats], list[Path]]:
    files: list[Path] = []
    seen: set[Path] = set()
    for pattern in patterns:
        for path in sorted(ROOT.glob(pattern)):
            if path.is_file() and path not in seen:
                seen.add(path)
                files.append(path)
    stats: dict[str, ElementStats] = {}
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = str(path.relative_to(ROOT))
        for name, attrs in scan_tags(text):
            entry = stats.setdefault(name, ElementStats())
            entry.uses += 1
            entry.files.add(rel)
            entry.attributes.update(attrs)
    return stats, files


def load_doc_texts(doc_paths: list[str]) -> tuple[str, str, list[tuple[str, bool]]]:
    """Return (full doc text, fenced-code-block text, per-doc availability)."""
    combined: list[str] = []
    availability: list[tuple[str, bool]] = []
    for rel in doc_paths:
        path = ROOT / rel
        exists = path.is_file()
        availability.append((rel, exists))
        if exists:
            combined.append(path.read_text(encoding="utf-8"))
    text = "\n".join(combined)
    fenced = "\n".join(re.findall(r"^```[^\n]*\n(.*?)^```", text, re.MULTILINE | re.DOTALL))
    return text, fenced, availability


NUMBERED_ELEMENT = re.compile(r"^(shift_pad|pad|param)([1-9]|1[0-6])$", re.IGNORECASE)


def is_documented(name: str, doc_text: str, fenced_text: str) -> bool:
    """Documented = backticked `<name>` mention (headings included) or a
    `<name ...>` tag inside a fenced code block. Numbered pad-family elements
    (pad2..pad16, shift_padN, paramN) count as documented when their
    1-numbered representative is documented."""
    if not doc_text:
        return False
    numbered = NUMBERED_ELEMENT.match(name)
    if numbered and numbered.group(2) != "1":
        return is_documented(numbered.group(1) + "1", doc_text, fenced_text)
    escaped = re.escape(name)
    if re.search(r"`</?" + escaped + r"[\s/>`]", doc_text, re.IGNORECASE):
        return True
    return bool(re.search(r"</?" + escaped + r"[\s/>]", fenced_text, re.IGNORECASE))


def format_attributes(attributes: Counter) -> str:
    if not attributes:
        return "—"
    parts = [
        f"`{attr}` ({count})"
        for attr, count in sorted(attributes.items(), key=lambda kv: (-kv[1], kv[0]))
    ]
    return ", ".join(parts)


def build_inventory() -> dict:
    families: dict[str, dict] = {}
    total_elements = 0
    total_undocumented = 0

    for family, patterns, doc_paths in FAMILIES:
        stats, files = collect_family(patterns)
        doc_text, fenced_text, availability = load_doc_texts(doc_paths)
        ordered = sorted(stats.items(), key=lambda kv: (-kv[1].uses, kv[0]))

        undocumented: list[str] = []
        elements: dict[str, dict] = {}
        for name, entry in ordered:
            documented = None
            if doc_paths:
                documented = is_documented(name, doc_text, fenced_text)
                if not documented:
                    undocumented.append(name)
            elements[name] = {
                "uses": entry.uses,
                "files": len(entry.files),
                "documented": documented,
                "attributes": dict(sorted(entry.attributes.items(),
                                          key=lambda kv: (-kv[1], kv[0]))),
            }

        families[family] = {
            "files_scanned": len(files),
            "docs_checked": [{"path": rel, "exists": exists}
                             for rel, exists in availability],
            "elements": elements,
            "undocumented": undocumented,
        }
        total_elements += len(ordered)
        total_undocumented += len(undocumented)

    return {
        "_meta": {
            "generated_by": "tools/extract_xml_inventory.py",
            "note": "Element/attribute inventory of every offline XML corpus, "
                    "cross-checked against the reference docs. Built-in skin XML is "
                    "not strict XML (raw `&`, `&&`, `>` inside quoted values), so this "
                    "comes from a tolerant quote-aware tokenizer, not an XML parser. "
                    "Query via `just get-xml-element` / `find-xml-elements` / "
                    "`xml-stats`; do not generate a Markdown copy.",
        },
        "totals": {"elements": total_elements, "undocumented": total_undocumented},
        "families": families,
    }


def serialize(inventory: dict) -> str:
    return json.dumps(inventory, indent=1, ensure_ascii=False) + "\n"


def run_check(inventory: dict) -> int:
    """Fail when an element becomes undocumented that was not already."""
    if not OUTPUT.is_file():
        OUTPUT.write_text(serialize(inventory), encoding="utf-8")
        print(f"{OUTPUT.relative_to(ROOT)}: did not exist, wrote initial inventory")
        return 0
    committed = json.loads(OUTPUT.read_text(encoding="utf-8")).get("families", {})
    failures: list[str] = []
    for family, data in inventory["families"].items():
        was = set(committed.get(family, {}).get("undocumented", []))
        new = sorted(set(data["undocumented"]) - was)
        if new:
            failures.append(f"{family}: new undocumented elements: {', '.join(new)}")
    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        print("Document the elements or regenerate with "
              "`python3 tools/extract_xml_inventory.py`.", file=sys.stderr)
        return 1
    print("XML inventory check passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit nonzero if a new undocumented element appears vs the committed report",
    )
    args = parser.parse_args()

    inventory = build_inventory()
    if args.check:
        return run_check(inventory)

    OUTPUT.write_text(serialize(inventory), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} "
          f"({inventory['totals']['elements']} elements, "
          f"{inventory['totals']['undocumented']} undocumented)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
