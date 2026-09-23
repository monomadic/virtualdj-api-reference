#!/usr/bin/env python3
"""Extract literal direct-parent relationships from vendor skin XML.

Quote-aware because shipped XML contains raw script operators in attributes.
Unbalanced files contribute diagnostics, never guessed edges. No templates or
includes are expanded; this is corpus evidence, not a supported-child schema.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tests/skin-xml-relations.json"
SOURCES = (
    ("skins", "builtin", "Built-in skin", "examples/Skins/Built-In/**/*.xml"),
    # Atomix catalog downloads are Published skins (Tier 2). Keep `addon`
    # separate: unlike bundle copies, they cannot be checked against the app.
    ("skins", "addon", "Published skin", "examples/Skins/Official-Addons/**/*.xml"),
    ("skins", "official_example", "Published skin", "examples/Skins/SDK Example - Custom Browser Skin/skin.xml"),
    ("video_skins", "builtin", "Built-in skin", "examples/VideoSkins/Built-In/**/*.xml"),
)
NOTE = ("Observed literal direct nesting in vendor XML (Tier 2); not a supported-child "
        "schema. Templates and includes are not expanded. Missing edges are unknown. "
        "Confirm behavior with a discriminating skin fixture and independent live readback.")
NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_.:-]*")


def scan(text: str) -> tuple[list[dict], list[dict]]:
    """Return edges and diagnostics; discard all edges if nesting is uncertain."""
    stack, edges, errors = [], [], []
    newlines = [i for i, char in enumerate(text) if char == "\n"]
    line = lambda pos: bisect_right(newlines, pos) + 1
    i, roots = 0, 0
    while i < len(text):
        start = text.find("<", i)
        if start < 0:
            break
        special = next(((prefix, suffix) for prefix, suffix in
                        (("<!--", "-->"), ("<![CDATA[", "]]>"), ("<?", "?>"))
                        if text.startswith(prefix, start)), None)
        if special:
            end = text.find(special[1], start + len(special[0]))
            if end < 0:
                errors.append({"line": line(start), "reason": "unterminated XML comment, CDATA or instruction"})
                break
            i = end + len(special[1])
            continue
        if text.startswith("<!", start):
            errors.append({"line": line(start), "reason": "unsupported declaration; nesting omitted"})
            break
        closing = text.startswith("</", start)
        match = NAME.match(text, start + (2 if closing else 1))
        if not match:
            errors.append({"line": line(start), "reason": "unrecognized tag start"})
            break
        name = match.group().lower()
        pos, quote = match.end(), None
        while pos < len(text):
            char = text[pos]
            if quote:
                if char == quote:
                    quote = None
            elif char in "\"'":
                quote = char
            elif char == ">":
                break
            elif char == "<":
                break
            pos += 1
        if pos == len(text) or text[pos] != ">":
            errors.append({"line": line(start), "reason": "unterminated or malformed tag"})
            break
        tail = text[match.end():pos]
        if closing:
            if tail.strip() or not stack or stack[-1][0] != name:
                errors.append({"line": line(start), "reason": f"unmatched closing tag </{name}>"})
                break
            stack.pop()
        else:
            if stack:
                edges.append({"parent": stack[-1][0], "child": name,
                              "parent_line": stack[-1][1], "line": line(start)})
            else:
                roots += 1
            if not tail.rstrip().endswith("/"):
                stack.append((name, line(start)))
        i = pos + 1
    if stack and not errors:
        errors.append({"line": stack[-1][1], "reason": f"unclosed tag <{stack[-1][0]}>"})
    if roots != 1 and not errors:
        errors.append({"line": 1, "reason": f"expected one root, observed {roots}"})
    return ([] if errors else edges), errors


def build() -> dict:
    groups, sources, diagnostics = defaultdict(list), [], []
    for family, kind, label, pattern in SOURCES:
        for path in sorted(ROOT.glob(pattern)):
            raw = path.read_bytes()
            rel = path.relative_to(ROOT).as_posix()
            edges, errors = scan(raw.decode("utf-8-sig"))
            sources.append({"path": rel, "family": family, "source_kind": kind,
                            "source_label": label,
                            "sha256": hashlib.sha256(raw).hexdigest(),
                            "status": "omitted" if errors else "scanned"})
            diagnostics.extend({"path": rel, **error} for error in errors)
            for edge in edges:
                groups[family, edge["parent"], edge["child"], rel, kind, label].append(
                    [edge["parent_line"], edge["line"]])
    relations = defaultdict(list)
    for (family, parent, child, path, kind, label), lines in sorted(groups.items()):
        relations[family, parent, child].append({"path": path, "source_kind": kind,
                                                "source_label": label,
                                                "lines": lines})
    return {"schema_version": 1, "line_format": "[parent_line, child_line]", "generated_by": "tools/skin_relations.py", "note": NOTE,
            "sources": sources, "diagnostics": diagnostics,
            "relationships": [
                {"family": family, "parent": parent, "child": child,
                 "evidence": "observed_vendor_xml", "tier": 2,
                 "uses": sum(len(loc["lines"]) for loc in locations), "locations": locations}
                for (family, parent, child), locations in sorted(relations.items())]}


def load() -> dict:
    if not DATA.exists():
        raise SystemExit("missing skin relationships; run `just skin-relations`")
    return json.loads(DATA.read_text())


def relationships(name: str, family: str | None = None, data: dict | None = None) -> dict:
    data = load() if data is None else data
    edges = [r for r in data["relationships"] if family is None or r["family"] == family]
    return {"note": data["note"],
            "parents": [r for r in edges if r["child"] == name],
            "children": [r for r in edges if r["parent"] == name]}


def render(result: dict) -> str:
    lines = [result["note"]]
    for direction, other in (("parents", "parent"), ("children", "child")):
        if direction not in result:
            continue
        lines.append(f"Observed {direction}:")
        for edge in result[direction]:
            loc = edge["locations"][0]
            lines.append(f"  <{edge[other]}> [{edge['family']}] — {edge['uses']} occurrences; "
                         f"{loc['source_label']}: {loc['path']}:{loc['lines'][0][1]} "
                         f"(parent line {loc['lines'][0][0]})")
        if not result[direction]:
            lines.append("  None observed; support unknown.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generated = build()
    if args.check:
        if load() != generated:
            print("Skin relationships are stale; run `just skin-relations`.")
            return 1
        print("Skin relationships check passed (including source hashes and diagnostics)")
    else:
        serialized = json.dumps(generated, indent=1)
        serialized = re.sub(r"\[\s+(\d+),\s+(\d+)\s+\]", r"[\1, \2]", serialized)
        DATA.write_text(serialized + "\n")
        print(f"Wrote {DATA.relative_to(ROOT)}; {len(generated['diagnostics'])} files omitted with diagnostics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
