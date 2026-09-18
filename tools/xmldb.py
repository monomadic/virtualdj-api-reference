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
from skin_categories import category, categories, validate
import skin_relations

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
            yield family, name, {**entry, "category": category(name, family)}


def family_matches(wanted, family):
    return wanted == "all" or (wanted == "skin" and family in {"skins", "video_skins"}) or wanted == family


def cmd_categories(args):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", default="skin")
    ap.add_argument("--format", choices=("json", "text"), default="text")
    ap.add_argument("--check", action="store_true")
    opts = ap.parse_args(args)
    data = load()
    validate(data)
    if opts.check:
        print("Skin categories check passed")
        return
    members = list(rows(data))
    result = [{**c, "elements": len({n for f, n, e in members
               if family_matches(opts.family, f)
               and e["category"]["id"] == c["id"]})} for c in categories()]
    if opts.format == "json":
        print(json.dumps(result, indent=1))
    else:
        print("Editorial categories; unique element names in selected families")
        for c in result:
            print(f"{c['id']:<24} {c['label']:<28} {c['elements']}")


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
        print(f"<{n}>  [{family}]  {e['category']['label']}  uses={e['uses']} files={e['files']}  {doc}")
        attrs = e["attributes"]
        if attrs:
            for attr, count in attrs.items():
                print(f"    {attr} ({count})")
        else:
            print("    (no attributes observed)")


def cmd_search(args):
    terms, opts = [], {}
    fmt, limit = "table", 0
    for a in args:
        if a.startswith("--"):
            key, _, val = a[2:].partition("=")
            if key == "format":
                fmt = val
            elif key == "limit":
                limit = int(val) if val else 0
            elif key in {"undocumented", "uncategorized"}:
                opts[key] = True
            elif key in {"family", "has-attr", "min-uses", "category", "parent", "child"}:
                opts[key] = val
            else:
                sys.exit(f"unknown option --{key}; filters: --family, "
                         "--undocumented, --has-attr, --min-uses, --category, --uncategorized, --parent, --child")
        else:
            terms.append(a.lower())

    data = load()
    if "category" in opts and opts["category"] not in {c["id"] for c in categories()}:
        sys.exit("Unknown category; use `just list-skin-categories` for IDs.")
    edges = skin_relations.load()["relationships"] if {"parent", "child"} & opts.keys() else []
    hits = []
    for family, name, e in rows(data):
        if not family_matches(opts.get("family", "all").lower(), family):
            continue
        if opts.get("undocumented") and e["documented"] is not False:
            continue
        if "category" in opts and e["category"]["id"] != opts["category"]:
            continue
        if opts.get("uncategorized") and e["category"]["id"] != "uncategorized":
            continue
        if "parent" in opts and not any(r["family"] == family and r["parent"] == opts["parent"].strip("<>") and r["child"] == name for r in edges):
            continue
        if "child" in opts and not any(r["family"] == family and r["child"] == opts["child"].strip("<>") and r["parent"] == name for r in edges):
            continue
        if "has-attr" in opts and not any(
                opts["has-attr"].lower() in a.lower() for a in e["attributes"]):
            continue
        if "min-uses" in opts and e["uses"] < int(opts["min-uses"]):
            continue
        if terms:
            hay = (name + " " + e["category"]["label"] + " " + " ".join(e["attributes"])).lower()
            if not all(t in hay for t in terms):
                continue
        hit = {"family": family, "element": name, **e}
        if {"parent", "child"} & opts.keys():
            hit["relationship_evidence"] = skin_relations.NOTE
        hits.append(hit)

    hits.sort(key=lambda h: (-h["uses"], h["element"]))
    shown = hits[:limit] if limit else hits
    if fmt == "json":
        print(json.dumps(shown, indent=1, ensure_ascii=False))
    else:
        from element_summary import doc_sections
        print("XML corpus usage — observed attributes attest syntax, not behavior.")
        print("Docs = element-name coverage only; attributes are ordered by usage.\n")
        if {"parent", "child"} & opts.keys():
            print(skin_relations.NOTE + "\n")
        for h in shown:
            doc = {True: "name documented", False: "NAME UNDOCUMENTED",
                   None: "no doc coverage check"}[h["documented"]]
            print(f"<{h['element']}>  [{h['family']}]  {doc}")
            print(f"  Category: {h['category']['label']} (editorial)")
            print(f"  Corpus: {h['uses']} uses in {h['files']} files; "
                  f"{len(h['attributes'])} observed attributes")
            attrs = sorted(h["attributes"], key=lambda a: (-h["attributes"][a], a))
            preview = ", ".join(attrs[:10]) or "none observed"
            if len(attrs) > 10:
                preview += f" (+{len(attrs) - 10} more)"
            print(f"  Attributes: {preview}")
            sections = doc_sections(h["element"], [h["family"]])
            for section in sections[:2]:
                print(f"  Docs: {section['doc']}:{section['line']} — {section['heading']}")
            if not sections:
                print("  Docs: no dedicated heading found")
            print()
        print("Details, reader leads, probe notes and examples: just element <name>")
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


COMMANDS = {"get": cmd_get, "search": cmd_search, "stats": cmd_stats, "categories": cmd_categories}

USAGE = """usage: xmldb.py <command> ... | xmldb.py <element>

  <element>              shorthand for `get <element>`
  get <element>          uses, files, documented state, attribute counts
  search [term] [--family=X --undocumented --has-attr=NAME --min-uses=N
                 --category=ID --uncategorized --parent=TAG --child=TAG
                 --format=json --limit=N]
  categories [--family=skin --format=json --check]  editorial category vocabulary
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
