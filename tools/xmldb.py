#!/usr/bin/env python3
"""Query API over the skin/pad/mapper XML element inventory.

Reads `docs/skin-xml-inventory.json` (written by
`tools/extract_xml_inventory.py`) and answers element/attribute questions
directly. No Markdown view is written to disk — reports are queries.

Usage:
    python3 tools/xmldb.py get <element>
    python3 tools/xmldb.py search [term ...] [--family=X] [--undocumented]
                                  [--has-attr=NAME] [--min-uses=N]
                                  [--format=json] [--limit=N]
    python3 tools/xmldb.py stats
"""
from __future__ import annotations

import difflib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "skin-xml-inventory.json"


def load() -> dict:
    if not DATA.exists():
        sys.exit(f"missing {DATA.relative_to(ROOT)}; run `just inventory`")
    return json.loads(DATA.read_text())


def rows(data: dict):
    """Flatten to (family, element, entry) triples."""
    for family, fam in data["families"].items():
        for name, entry in fam["elements"].items():
            yield family, name, entry


def cmd_get(args):
    if not args:
        sys.exit("usage: get <element>")
    name = args[0].strip("<>")
    data = load()
    found = [(f, n, e) for f, n, e in rows(data) if n == name]
    if not found:
        names = sorted({n for _, n, _ in rows(data)})
        near = difflib.get_close_matches(name, names, n=5, cutoff=0.6)
        msg = f"no element <{name}> in the inventory"
        if near:
            msg += "\ndid you mean: " + ", ".join(f"<{n}>" for n in near)
        sys.exit(msg)
    for family, n, e in found:
        doc = {True: "documented", False: "UNDOCUMENTED", None: "no doc to check"}[
            e["documented"]]
        print(f"<{n}>  [{family}]  uses={e['uses']} files={e['files']}  {doc}")
        attrs = e["attributes"]
        if attrs:
            for attr, count in attrs.items():
                print(f"    {attr} ({count})")
        else:
            print("    (no attributes observed)")


def cmd_search(args):
    terms, opts = [], {}
    fmt, limit = "table", 50
    for a in args:
        if a.startswith("--"):
            key, _, val = a[2:].partition("=")
            if key == "format":
                fmt = val
            elif key == "limit":
                limit = int(val) if val else 0
            elif key == "undocumented":
                opts["undocumented"] = True
            elif key in {"family", "has-attr", "min-uses"}:
                opts[key] = val
            else:
                sys.exit(f"unknown option --{key}; filters: --family, "
                         "--undocumented, --has-attr, --min-uses")
        else:
            terms.append(a.lower())

    data = load()
    hits = []
    for family, name, e in rows(data):
        if "family" in opts and opts["family"].lower() not in family.lower():
            continue
        if opts.get("undocumented") and e["documented"] is not False:
            continue
        if "has-attr" in opts and not any(
                opts["has-attr"].lower() in a.lower() for a in e["attributes"]):
            continue
        if "min-uses" in opts and e["uses"] < int(opts["min-uses"]):
            continue
        if terms:
            hay = (name + " " + " ".join(e["attributes"])).lower()
            if not all(t in hay for t in terms):
                continue
        hits.append({"family": family, "element": name, **e})

    hits.sort(key=lambda h: (-h["uses"], h["element"]))
    shown = hits[:limit] if limit else hits
    if fmt == "json":
        print(json.dumps(shown, indent=1, ensure_ascii=False))
    else:
        for h in shown:
            flag = "" if h["documented"] is not False else "  UNDOCUMENTED"
            print(f"<{h['element']:<22} [{h['family']:<12}] uses={h['uses']:<5} "
                  f"attrs={len(h['attributes'])}{flag}")
    note = f"showing {len(shown)} of {len(hits)}" if len(shown) != len(hits) \
        else f"{len(hits)} match(es)"
    print(f"\n{note}", file=sys.stderr)


def cmd_stats(args):
    data = load()
    out = {"totals": data["totals"], "families": {}}
    for family, fam in data["families"].items():
        out["families"][family] = {
            "files_scanned": fam["files_scanned"],
            "elements": len(fam["elements"]),
            "undocumented": fam["undocumented"],
        }
    print(json.dumps(out, indent=1, ensure_ascii=False))


COMMANDS = {"get": cmd_get, "search": cmd_search, "stats": cmd_stats}

USAGE = """usage: xmldb.py <command> ... | xmldb.py <element>

  <element>              shorthand for `get <element>`
  get <element>          uses, files, documented state, attribute counts
  search [term] [--family=X --undocumented --has-attr=NAME --min-uses=N
                 --format=json --limit=N]
  stats                  per-family totals and undocumented lists"""


def main(argv):
    if not argv:
        sys.exit(USAGE)
    cmd, rest = argv[0], argv[1:]
    if cmd in {"-h", "--help", "help"}:
        print(USAGE)
        return
    if cmd in COMMANDS:
        COMMANDS[cmd](rest)
        return
    cmd_get(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
