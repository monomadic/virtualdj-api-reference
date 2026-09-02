#!/usr/bin/env python3
"""Collect every VDJScript snippet Atomix themselves wrote, in one place.

Two sanctioned sources, kept apart by provenance because they prove different
things:

- **catalog** — snippets quoted inside the Button Editor's own action
  descriptions (`Resources/languages.zip`), the same prose the official verbs
  appendix publishes. These are documentation: they say what a form MEANS.
- **builtin** — script attributes in the shipped pad pages, skins, sampler banks
  and video skins under `examples/`. These are usage: whatever the parser
  actually accepts in a file Atomix ships.

Why bother, when `tests/verb-arg-forms.json` probes tails directly: the probe can
only tell a token apart from nonsense, never what it does, and it is blind
wherever the state does not discriminate. A tail that appears in shipped XML is
attested regardless, and a tail quoted in the catalog comes with its meaning. The
three sources are independent, so agreement is corroboration and disagreement is
a worklist.

Use it as a test corpus: every snippet here is a form the vendor considers
valid, which makes it a regression set for any grammar claim this repo makes.

    python3 tools/extract_script_corpus.py > tests/vdjscript-corpus.json
    python3 tools/extract_script_corpus.py --verb sampler_loaded
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

DEFAULT_APP = Path("/Applications/VirtualDJ.app")
ARTIFACT = Path("tests/vdjscript-corpus.json")
VERB_TABLE = Path("tests/verb-table.json")
# ONLY vendor-shipped trees. examples/Pads/Quarantine and examples/Skins/GraveRaver
# are this repo's own fixtures — including them would let our test files
# masquerade as vendor evidence, which is the whole point of the corpus.
XML_ROOTS = (Path("examples/Pads/Built-In"), Path("examples/Skins/Built-In"),
             Path("examples/Samplerbanks/Built-In"), Path("examples/VideoSkins/Built-In"))

# Attributes that hold script in shipped pad/skin XML.
SCRIPT_ATTRS = ("action", "query", "visibility", "color", "textcolor", "value",
                "onstart", "onstop", "ondblclick", "tooltip_query", "enabled")
ATTR = re.compile(r'\b(%s)\s*=\s*"([^"]*)"' % "|".join(SCRIPT_ATTRS), re.I)
ACTION_BLOCK = re.compile(r"<Actions>(.*?)</Actions>", re.S)
ACTION_ENTRY = re.compile(r"<([a-z0-9_]+)>(.*?)</\1>", re.S)
QUOTED = re.compile(r"['\"]([^'\"\n]{4,120})['\"]")
WORD = re.compile(r"[a-z_][a-z0-9_]*")


def verbs_in(script: str, known: set[str]) -> list[str]:
    return sorted({w for w in WORD.findall(script.lower()) if w in known})


def from_catalog(app: Path, known: set[str]) -> list[dict]:
    with ZipFile(app / "Contents/Resources/languages.zip") as bundle:
        xml = bundle.read("English.xml").decode("utf-8", errors="replace")
    block = ACTION_BLOCK.search(xml)
    out = []
    for name, body in ACTION_ENTRY.findall(block.group(1) if block else ""):
        text = body.replace("&quot;", '"').replace("&apos;", "'").replace("&amp;", "&")
        for snippet in QUOTED.findall(text):
            snippet = snippet.strip()
            # A snippet is an example only if it actually starts with a verb and
            # carries an argument — otherwise it is just a quoted keyword.
            head = WORD.match(snippet.lower())
            if not head or head.group(0) not in known or " " not in snippet:
                continue
            if not snippet[0].islower():
                continue  # "Load saved loop named ..." is prose, not an example
            out.append({"script": snippet, "source": "catalog", "origin": name,
                        "verbs": verbs_in(snippet, known)})
    return out


def from_builtins(known: set[str]) -> list[dict]:
    out = []
    for root in XML_ROOTS:
        for path in sorted(root.rglob("*.xml")) if root.exists() else []:
            text = path.read_text(encoding="utf-8", errors="replace")
            for attr, value in ATTR.findall(text):
                script = value.strip()
                if not script or len(script) > 400:
                    continue
                found = verbs_in(script, known)
                if not found:
                    continue
                out.append({"script": script, "source": "builtin", "origin": str(path),
                            "context": attr.lower(), "verbs": found})
    return out


def merge(entries: list[dict]) -> dict[str, dict]:
    merged: dict[str, dict] = {}
    for entry in entries:
        record = merged.setdefault(entry["script"], {
            "script": entry["script"], "verbs": entry["verbs"],
            "sources": [], "origins": []})
        if entry["source"] not in record["sources"]:
            record["sources"].append(entry["source"])
        origin = entry["origin"] + (f"@{entry['context']}" if "context" in entry else "")
        if origin not in record["origins"]:
            record["origins"].append(origin)
    return merged


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=Path, default=DEFAULT_APP)
    parser.add_argument("--verb", help="only snippets mentioning this verb")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    known = set(json.load(open(VERB_TABLE))["verbs"])
    merged = merge(from_catalog(args.app, known) + from_builtins(known))

    if args.check:
        if not ARTIFACT.exists():
            print("script corpus check skipped: tests/vdjscript-corpus.json not extracted yet")
            return 0
        stored = json.load(open(ARTIFACT))["summary"]
        if stored["snippets"] != len(merged):
            sys.exit(f"script corpus check FAILED: artifact has {stored['snippets']} snippets, "
                     f"re-extraction finds {len(merged)} — re-extract")
        print(f"script corpus check passed: {stored['snippets']} snippets "
              f"({stored['by_source']}), covering {stored['verbs_covered']} verbs")
        return 0

    if args.verb:
        hits = [r for r in merged.values() if args.verb in r["verbs"]]
        print(json.dumps({"verb": args.verb, "snippets": len(hits), "examples": hits}, indent=1))
        return 0

    by_verb = defaultdict(int)
    for record in merged.values():
        for verb in record["verbs"]:
            by_verb[verb] += 1
    by_source = defaultdict(int)
    for record in merged.values():
        for source in record["sources"]:
            by_source[source] += 1
    json.dump({
        "summary": {
            "snippets": len(merged),
            "by_source": dict(by_source),
            "verbs_covered": len(by_verb),
            "most_exampled": sorted(by_verb.items(), key=lambda kv: -kv[1])[:15],
        },
        "snippets": sorted(merged.values(), key=lambda r: r["script"]),
    }, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
