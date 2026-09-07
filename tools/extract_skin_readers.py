#!/usr/bin/env python3
"""Recover the skin XML vocabulary the binary actually compares against.

`tools/extract_xml_inventory.py` answers what shipped skins *use*; the Skin SDK
doc answers what Atomix *documented*. Neither answers what the reader will
accept, and the three disagree: `clickthrough` is read by every skin object and
appears in no shipped skin and no doc.

Method (the stripped-build method from `extract_binary_vocabularies.py`, with
the enumeration heuristics removed — a skin reader is exactly the "dispatcher
referencing far more strings than it hits" that module deliberately discards):
each reader is anchored by strings only that reader compares. The tightest
`__text` window holding an xref to every anchor is the reader; every string
referenced from inside that window, in address order, is its vocabulary.

Each name is then classified against the two other sources, and what is in the
binary but in neither is the candidate queue. Note what that means over time:
writing a candidate into the Skin SDK doc — even as "in the reader, untested" —
moves it to `documented_only` and shrinks `summary.candidates`. That is the
intended reading (`candidates` is *undocumented* names, not *unconfirmed* ones);
the record of which documented names are still unconfirmed lives in the doc and
the tracker, not here. A candidate is a *lead*, tier 2:
the reader knowing a word does not say what the word does, and skin readers
ignore words they do not know, so confirming one needs a fixture where the
forms would differ (see `tests/Skins/clickthrough-probe/`).

    python3 tools/extract_skin_readers.py > tests/skin-reader-vocabulary.json
    python3 tools/extract_skin_readers.py --get skin_object_base
    python3 tools/extract_skin_readers.py --candidates
"""

from __future__ import annotations

import argparse
import json
import plistlib
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_binary_vocabularies import Image  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APP = Path("/Applications/VirtualDJ.app")
ARTIFACT = ROOT / "tests" / "skin-reader-vocabulary.json"
INVENTORY = ROOT / "docs" / "skin-xml-inventory.json"
SDK = ROOT / "docs" / "Skin SDK.md"

# A reader is named by anchors no other reader compares. Keep anchors rare:
# `visibility` is read in four places, `clickthrough` in exactly one.
READERS = {
    "skin_object_base": {
        "anchors": ["condition", "canstretch", "clickthrough", "mousemask", "mousecircle"],
        "what": "attributes read for every skin object (panel, group, button, ...)",
    },
    "element_dispatch": {
        "anchors": ["multibutton", "resizepanel", "keyboardmap", "pannel"],
        "what": "the element-name switch: which tags the skin parser knows",
    },
    "panel_builder": {
        "anchors": ["forceshow", "childtooltip", "breakline1", "grabzone"],
        "what": "panel/menu-item construction, including the forceshow vocabulary",
    },
}
# A reader window wider than this means an anchor matched in the wrong function.
MAX_SPAN = 0x2000
# Single letters (`x`, `y`, `r`) are real attribute names; format scraps are not.
NOISE = {"\n", "\\n", "0123456789.%", "constant ", "image/", "Right-click: "}
# Booleans the reader parses for every boolean attribute; not a vocabulary find.
BOOLEANS = {"yes", "no", "true", "false"}


def window(img: Image, anchors: list[str]) -> tuple[int, int, dict[str, list[int]]]:
    """The tightest window containing one xref to each anchor."""
    per: dict[str, list[int]] = {}
    for anchor in anchors:
        pcs = sorted(pc for vm in img.by_text.get(anchor, []) for pc in img.xrefs.get(vm, []))
        if not pcs:
            raise SystemExit(f"anchor {anchor!r} is not referenced from __text on this build")
        per[anchor] = pcs
    # Anchors are rare, so a sweep over the rarest one's xrefs is cheap.
    rarest = min(per, key=lambda a: len(per[a]))
    best = None
    for pc in per[rarest]:
        picks = {}
        for anchor, pcs in per.items():
            picks[anchor] = min(pcs, key=lambda p: abs(p - pc))
        lo, hi = min(picks.values()), max(picks.values())
        if hi - lo > MAX_SPAN:
            continue
        if best is None or hi - lo < best[1] - best[0]:
            best = (lo, hi, picks)
    if best is None:
        raise SystemExit(f"no window under {hex(MAX_SPAN)} holds all of {anchors}")
    return best


def referenced(img: Image, lo: int, hi: int) -> list[tuple[int, str]]:
    out = []
    for vm, pcs in img.xrefs.items():
        for pc in pcs:
            if lo <= pc <= hi:
                s = img.strings[vm]
                if s not in NOISE:
                    out.append((pc, s))
    return sorted(out)


def sources() -> tuple[dict[str, set[str]], set[str]]:
    """(elements -> attributes) from the shipped corpus, and the SDK's words."""
    elements: dict[str, set[str]] = defaultdict(set)
    if INVENTORY.exists():
        inv = json.load(open(INVENTORY))
        for family in inv["families"].values():
            for name, rec in family.get("elements", {}).items():
                elements[name] |= set(rec.get("attributes", {}))
    documented: set[str] = set()
    if SDK.exists():
        import re
        text = SDK.read_text(encoding="utf-8").lower()
        documented = set(re.findall(r"[a-z][a-z0-9_]{2,}", text))
        # Short names are invisible to that pattern, so a one- or two-letter
        # attribute stays a "candidate" however thoroughly it is written up.
        # A backtick-quoted token is the doc naming something deliberately, so
        # take those at any length — `r` is why.
        documented |= set(re.findall(r"`([a-z][a-z0-9_]*)`", text))
    return elements, documented


def classify(name: str, elements: dict[str, set[str]], attributes: set[str],
             documented: set[str]) -> str:
    if name in BOOLEANS:
        return "boolean_value"
    if name in elements:
        return "shipped_element"
    if name in attributes:
        return "shipped_attribute"
    if name in documented:
        return "documented_only"
    return "candidate"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--app", type=Path, default=DEFAULT_APP)
    ap.add_argument("--get", help="print one reader")
    ap.add_argument("--candidates", action="store_true",
                    help="print only the names in no other source")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if (args.get or args.candidates) and ARTIFACT.exists():
        art = json.load(open(ARTIFACT))
        if args.get:
            rec = art["readers"].get(args.get)
            print(json.dumps(rec or {"error": f"no reader {args.get}",
                                     "known": sorted(art["readers"])}, indent=1))
        else:
            print(json.dumps({"build": art["summary"]["build"],
                              "candidates": art["summary"]["candidates"]}, indent=1))
        return 0

    img = Image(args.app)
    elements, documented = sources()
    attributes = {a for attrs in elements.values() for a in attrs}

    readers = {}
    for name, spec in READERS.items():
        lo, hi, picks = window(img, spec["anchors"])
        refs = referenced(img, lo, hi)
        seen, vocabulary = set(), []
        for pc, s in refs:
            if s in seen:
                continue
            seen.add(s)
            vocabulary.append({"name": s, "first_ref": hex(pc),
                               "where": classify(s, elements, attributes, documented)})
        readers[name] = {
            "what": spec["what"],
            "anchors": {a: hex(p) for a, p in sorted(picks.items())},
            "text_range": [hex(lo), hex(hi)],
            "refs": len(refs),
            "vocabulary": vocabulary,
        }

    candidates = sorted({v["name"] for r in readers.values()
                         for v in r["vocabulary"] if v["where"] == "candidate"})
    with open(args.app / "Contents/Info.plist", "rb") as fh:
        info = plistlib.load(fh)
    summary = {
        "build": info.get("CFBundleVersion", "?"),
        "readers": len(readers),
        "names": sum(len(r["vocabulary"]) for r in readers.values()),
        "candidates": candidates,
    }

    if args.check:
        if not ARTIFACT.exists():
            print("skin reader check skipped: artifact not extracted yet")
            return 0
        stored = json.load(open(ARTIFACT))["summary"]
        if stored["build"] != summary["build"]:
            print(f"skin reader check skipped: artifact is build {stored['build']}, "
                  f"installed is {summary['build']} — re-extract to re-anchor")
            return 0
        if stored["names"] != summary["names"] or stored["candidates"] != summary["candidates"]:
            sys.exit("skin reader check FAILED: artifact disagrees with a re-extraction "
                     f"({stored['names']} names / {len(stored['candidates'])} candidates "
                     f"vs {summary['names']} / {len(summary['candidates'])}) — re-extract")
        print(f"skin reader check passed: {stored['readers']} readers, {stored['names']} names, "
              f"{len(stored['candidates'])} in neither the shipped corpus nor the SDK doc "
              f"(build {stored['build']})")
        return 0

    json.dump({"summary": summary, "readers": readers}, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
