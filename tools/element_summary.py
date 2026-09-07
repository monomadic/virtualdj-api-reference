#!/usr/bin/env python3
"""One skin/pad/mapper XML element, everything this repo knows, on one screen.

    just element mousecircle
    just element mousecircle --format=json

The counterpart to `just verb`. `just get-xml-element` answers one question —
what the inventory recorded — the way `just get-verb` does; this joins the rest:
the element's own doc section, whether the binary's reader vocabulary knows the
name, real usage from shipped skins, what a live probe established (including
the negatives, which live nowhere else), and which of its attributes no
documentation explains.

That last one is the reason this exists rather than being a convenience wrapper.
The inventory's `documented` flag is about the ELEMENT NAME only, so an element
reads `documented` while most of its attributes are unexplained — `<panel>`
writes 29 distinct attributes across the shipped skins. Per-element is the only
altitude at which that gap is actionable.

Three directions of blindness, all reported rather than papered over:

- The inventory sees only what a shipped file happens to WRITE. `r` is the
  `<mousecircle>` radius, confirmed live, and appears in no shipped skin — so it
  is absent from the attribute list here and present in the doc section.
- The doc check sees only backticked mentions and fenced code. An attribute
  discussed in prose without backticks reads as undocumented. Undocumented here
  means "not written the way the checker recognises", which is a lead, not a
  finding — see docs/Evidence Standards.md.
- Not every attribute in shipped XML is an attribute the reader READS. The skin
  format substitutes template parameters textually before any reader runs, so
  those names are author-invented and can never be vocabulary; they are marked
  `~`, not counted as gaps, and `template_parameters()` explains the test.
  Counting them was overstating the gap by 30 attributes and 3,065 uses.

Nothing here is new evidence: the existing artifacts and docs, read together.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "docs" / "skin-xml-inventory.json"
READERS = ROOT / "tests" / "skin-reader-vocabulary.json"
# Where a family's element names are checked for documentation, mirroring
# extract_xml_inventory.py's own table so the two never drift apart silently.
FAMILY_DOCS = {
    "skins": ["docs/Skin SDK.md", "docs/Skin Waveforms.md"],
    "video_skins": ["docs/Skin SDK.md", "docs/Skin Waveforms.md"],
    "pads": ["docs/Pad Page XML.md", "docs/Example Pad XML Pages.md"],
    "mappers": ["docs/Mapper XML.md"],
    "samplerbanks": [],
}
PROBE_DIRS = ROOT / "tests" / "Skins"


def load(path: Path, what: str) -> dict:
    if not path.exists():
        sys.exit(f"missing {path.relative_to(ROOT)}; run `just {what}`")
    return json.loads(path.read_text())


def find(name: str, data: dict) -> list[tuple[str, dict]]:
    return [(fam, f["elements"][name]) for fam, f in data["families"].items()
            if name in f["elements"]]


def doc_sections(name: str, families: list[str]) -> list[dict]:
    """The element's own headings, so the reader is sent to a section rather
    than to a grep hit in a 2,900-line file."""
    out = []
    seen = set()
    for fam in families:
        for rel in FAMILY_DOCS.get(fam, []):
            if rel in seen:
                continue
            seen.add(rel)
            path = ROOT / rel
            if not path.is_file():
                continue
            lines = path.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines, 1):
                if not line.startswith("#"):
                    continue
                if re.search(r"</?" + re.escape(name) + r"[\s/>`]", line + " ", re.I):
                    out.append({"doc": rel, "line": i,
                                "heading": line.lstrip("# ").strip()})
    return out


def doc_mentions_attribute(attr: str, families: list[str]) -> bool:
    """The same test extract_xml_inventory.py applies to element names, applied
    to an attribute: a backticked mention, or a use inside a fenced block."""
    for fam in families:
        for rel in FAMILY_DOCS.get(fam, []):
            path = ROOT / rel
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            if re.search(r"`" + re.escape(attr) + r"[=`\s]", text):
                return True
            fenced = "\n".join(re.findall(r"^```[^\n]*\n(.*?)^```", text,
                                          re.MULTILINE | re.DOTALL))
            if re.search(r"\b" + re.escape(attr) + r"\s*=", fenced):
                return True
    return False


# XInclude's own: `xml:base` is injected during processing and `xmlns:xi` declares
# the namespace. Both are XML standard attributes, not skin vocabulary, and no
# VirtualDJ doc will ever explain them.
NOT_SKIN_VOCABULARY = {"xml:base", "xmlns:xi"}

_placeholders: set[str] | None = None
_placeholder_scan_ok = True


def template_parameters() -> set[str]:
    """Attribute names the skin format substitutes rather than reads.

    `<panel class="rm_hc" action1="hot_cue 1">` instantiates a template: `class=`
    names it, and the remaining attributes supply values that the loader
    substitutes for `[ACTION1]` in the template body, textually, before any
    reader sees the XML. So the name is author-invented, unbounded, and can
    never be reader vocabulary or appear in a doc.

    Detected by the placeholder token, which is the substitution's own evidence:
    an attribute is a template parameter when the corpus writes `[NAME]`
    somewhere. Without this the metric badly overstates — 29 of the 67
    attributes no doc explains are template parameters, and they carry 3,065 of
    the 4,206 uses.

    Note the overlap is real: `width` and `action2` are BOTH reader attributes
    and template parameters, so this never overrides a documented attribute — it
    only reclassifies what would otherwise be reported as an unexplained one.
    """
    global _placeholders, _placeholder_scan_ok
    if _placeholders is None:
        try:
            proc = subprocess.run(["rg", "-oIN", r"\[[A-Z0-9_]+\]", "examples", "tests"],
                                  cwd=ROOT, capture_output=True, text=True, timeout=60)
            _placeholders = {t.strip("[]").lower() for t in proc.stdout.split()}
            _placeholder_scan_ok = bool(_placeholders)
        except (OSError, subprocess.SubprocessError):
            _placeholders, _placeholder_scan_ok = set(), False
    return _placeholders


def classify_attribute(attr: str, families: list[str]) -> str:
    """documented | template_param | not_vocabulary | unexplained."""
    if attr in NOT_SKIN_VOCABULARY:
        return "not_vocabulary"
    if doc_mentions_attribute(attr, families):
        return "documented"
    if attr.lower() in template_parameters():
        return "template_param"
    return "unexplained"


def reader_vocabulary(name: str) -> dict:
    """Whether the binary's skin reader knows the name, and via which reader.

    A name the reader knows that no shipped file writes is the interesting case:
    it is real vocabulary with no example anywhere, which is exactly what the
    inventory's `undocumented: 0` cannot see.
    """
    if not READERS.exists():
        return {"available": False}
    data = json.loads(READERS.read_text())
    hits = []
    for reader, rec in data.get("readers", {}).items():
        names = rec.get("names", rec) if isinstance(rec, dict) else rec
        if isinstance(names, dict):
            names = list(names)
        if isinstance(names, list) and name in names:
            hits.append(reader)
    summary = data.get("summary", {})
    return {"available": True, "build": summary.get("build"), "readers": hits,
            "unused_candidate": name in (summary.get("candidates") or [])}


def probes(name: str) -> list[dict]:
    """Live probe fixtures that exercised this element. The probe READMEs carry
    the NEGATIVE results too — that <song_pos> and <rack> were tested and build
    nothing on the deck-skin surface is recorded nowhere else."""
    out = []
    if not PROBE_DIRS.is_dir():
        return out
    for readme in sorted(PROBE_DIRS.glob("*/README.md")):
        text = readme.read_text(encoding="utf-8")
        if not re.search(r"\b" + re.escape(name) + r"\b", text):
            continue
        hits = [ln.strip() for ln in text.splitlines()
                if re.search(r"\b" + re.escape(name) + r"\b", ln)]
        out.append({"fixture": str(readme.parent.relative_to(ROOT)),
                    "lines": hits[:4]})
    return out


def usages(name: str, limit: int) -> list[dict]:
    """Real files that write the element, shipped ones first — a working example
    usually answers the question outright."""
    try:
        proc = subprocess.run(
            ["rg", "-l", "--fixed-strings", f"<{name}", "examples", "tests"],
            cwd=ROOT, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return []
    files = [f for f in proc.stdout.splitlines() if f]

    def rank(p: str) -> tuple:
        return (0 if "Built-In" in p else 1 if p.startswith("examples/") else 2, p)

    out = []
    for path in sorted(files, key=rank)[:limit]:
        out.append({"file": path,
                    "shipped": "Built-In" in path,
                    "probe_fixture": path.startswith("tests/")})
    return {"files": out, "total": len(files)}


def summary(name: str, limit: int) -> dict:
    name = name.strip("<>")
    data = load(INVENTORY, "inventory")
    found = find(name, data)
    if not found:
        import difflib
        names = sorted({n for f in data["families"].values() for n in f["elements"]})
        near = difflib.get_close_matches(name, names, n=5, cutoff=0.6)
        vocab = reader_vocabulary(name)
        msg = f"no element <{name}> in the inventory"
        if vocab.get("readers"):
            msg += (f"\nbut the binary's reader vocabulary knows it "
                    f"({', '.join(vocab['readers'])} on build {vocab['build']}) — "
                    "real vocabulary that no shipped file writes")
        # Absent from the inventory is not the same as never investigated. R7
        # carried a batch of candidate names to live tests and most came back
        # negative; that result is the answer to this lookup, not a near-miss
        # spelling list.
        tested = probes(name)
        if tested:
            msg += "\na live probe already tested this name:"
            for p in tested:
                msg += f"\n  {p['fixture']}"
                for ln in p["lines"][:2]:
                    msg += f"\n      {ln[:110]}"
        if near:
            msg += "\ndid you mean: " + ", ".join(f"<{n}>" for n in near)
        sys.exit(msg)

    families = [f for f, _ in found]
    attributes: dict[str, int] = {}
    for _, entry in found:
        for attr, n in entry["attributes"].items():
            attributes[attr] = attributes.get(attr, 0) + n
    kind = {a: classify_attribute(a, families) for a in attributes}

    return {
        "element": name,
        "families": {fam: {"uses": e["uses"], "files": e["files"],
                           "name_documented": e["documented"]}
                     for fam, e in found},
        "attributes": [{"name": a, "uses": attributes[a], "kind": kind[a],
                        "documented": kind[a] == "documented"}
                       for a in sorted(attributes, key=lambda a: (-attributes[a], a))],
        # Genuinely unexplained: template parameters and XInclude's own
        # attributes are excluded, because neither is reader vocabulary and
        # neither could ever be documented as such.
        "attributes_unexplained": sorted(a for a, k in kind.items() if k == "unexplained"),
        "attributes_template_params": sorted(a for a, k in kind.items()
                                             if k == "template_param"),
        "template_detection": "ok" if _placeholder_scan_ok else "unavailable (rg failed)",
        "doc_sections": doc_sections(name, families),
        "reader_vocabulary": reader_vocabulary(name),
        "probes": probes(name),
        "usage": usages(name, limit),
        "tiers": {
            "inventory/usage": "Tier 2 — shipped XML attests the form, not the behaviour",
            "doc_sections": "whatever label the section itself carries; check it",
            "reader_vocabulary": "Tier 2 structural — the binary names it; a lead",
            "probes": "Tier 1 local test — the only source that proves behaviour",
        },
    }


def render(s: dict) -> str:
    L = [f"<{s['element']}>", "=" * (len(s["element"]) + 2)]
    for fam, f in s["families"].items():
        doc = {True: "name documented", False: "NAME UNDOCUMENTED",
               None: "no doc to check"}[f["name_documented"]]
        L.append(f"  {fam:<14} uses={f['uses']:<6} files={f['files']:<4} {doc}")

    v = s["reader_vocabulary"]
    if v.get("available"):
        if v["readers"]:
            note = f"named by {', '.join(v['readers'])} on build {v['build']}"
            if v["unused_candidate"]:
                note += " — and no shipped file writes it"
            L.append(f"  reader vocab   {note}")
        else:
            L.append("  reader vocab   not in the extracted reader vocabulary "
                     "(the extractor covers 3 readers, not the whole parser)")
    L.append("")

    if s["doc_sections"]:
        L.append("Documentation")
        for d in s["doc_sections"]:
            L.append(f"  {d['doc']}:{d['line']}  {d['heading']}")
    else:
        L.append("Documentation: no heading names this element "
                 "(it may still be covered inside a broader section)")
    L.append("")

    attrs = s["attributes"]
    if attrs:
        unexplained = s["attributes_unexplained"]
        tmpl = s["attributes_template_params"]
        head = f"Attributes written by shipped files ({len(attrs)}; "
        head += f"{len(unexplained)} unexplained"
        if tmpl:
            head += f", {len(tmpl)} template parameters"
        L.append(head + ")")
        MARK = {"documented": " ", "unexplained": "!", "template_param": "~",
                "not_vocabulary": "·"}
        for a in attrs:
            L.append(f"  {MARK[a['kind']]} {a['name']:<24} {a['uses']:>5}")
        if unexplained:
            L.append("  ! = no backticked mention and no fenced-block use in this "
                     "family's docs — a lead, not a finding")
        if tmpl:
            L.append("  ~ = substituted, not read: the corpus writes `[NAME]` for it, so "
                     "this is a template")
            L.append("      parameter supplied at the `class=` call site, never reader "
                     "vocabulary")
        if any(a["kind"] == "not_vocabulary" for a in attrs):
            L.append("  · = not skin vocabulary (XInclude injects it)")
        if s["template_detection"] != "ok":
            L.append("  NOTE: template detection " + s["template_detection"]
                     + " — unexplained counts are overstated")
    else:
        L.append("Attributes: none written by any shipped file")
    L.append("")

    if s["probes"]:
        L.append("Live probes (Tier 1 — includes negatives recorded nowhere else)")
        for p in s["probes"]:
            L.append(f"  {p['fixture']}")
            for ln in p["lines"]:
                L.append(f"      {ln[:110]}")
    else:
        L.append("Live probes: none — no fixture under tests/Skins/ names this element")
    L.append("")

    u = s["usage"]
    if u and u.get("files"):
        L.append(f"Usage ({u['total']} files write it; shipped first)")
        for f in u["files"]:
            tag = "built-in" if f["shipped"] else "probe fixture" if f["probe_fixture"] else "example"
            L.append(f"  {f['file']}   [{tag}]")
    else:
        L.append("Usage: no file in the corpora writes this element")
    L.append("")
    L.append("Tiers: shipped XML attests a form, never behaviour; the reader vocabulary is a "
             "structural lead; only a live probe proves what the element does.")
    return "\n".join(L)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("element")
    ap.add_argument("--format", choices=("text", "json"), default="text")
    ap.add_argument("--usages", type=int, default=8, metavar="N",
                    help="how many usage files to list (default 8)")
    args = ap.parse_args(argv)
    s = summary(args.element, args.usages)
    print(json.dumps(s, indent=1) if args.format == "json" else render(s))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
