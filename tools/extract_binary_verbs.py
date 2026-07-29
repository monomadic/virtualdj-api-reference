#!/usr/bin/env python3
"""Extract a STRUCTURED verb list from the VirtualDJ binary and language catalog.

Two structured sources, each meaningful on its own terms:

  symbol   mangled `ACTION_<name>` implementation classes in the executable's
           string table (e.g. `19ACTION_browser_sort`). One per canonical verb
           implementation.
  catalog  action names documented in `Resources/languages.zip` -> `English.xml`
           `<Actions>`, i.e. the app's own descriptions.
  table    the parser's alphabetically sorted name table, recovered as the long
           ascending runs of identifier strings (`action_deck` .. `zoom_vertical`).
           This is the source that carries ALIASES — `hotcue`, `eq_med`,
           `skin_pannel`, `lock_pannel`, the `*_slider` family — which the other
           two omit. A universal binary contains one run per architecture slice.

Membership in any of the three is PROOF the name is a real verb — no HTTP needed.
The union covers 998 of the 1,007 names the HTTP sweep proved real.

**It is still not a completeness oracle.** Nine proven-real names are in none of
the three sources: `browser`, `config`, `jog`, `no`, `off`, `on`, `preview`,
`volume`, `yes` — all short, common single words, presumably fast-pathed. The
name table also omits some core verbs (`load`, `loop`, `cue`, `hot_cue`,
`nothing`), which is why all three sources are unioned rather than trusting one.
So absence from this list does not disprove a name; disproof needs the additional
string/context test in docs/Undocumented VDJScript Candidates.md.

ALIAS DERIVATION: a name in the `table` with no `symbol` of its own cannot be its
own implementation, so it must be dispatched to another class — i.e. an alias or
variant form. That rule recovers 52 of the store's independently-recorded aliases
and predicts 11 more (flagged `alias_candidate`). It identifies a name AS an
alias; it does not say which verb it aliases. That needs a behavioral test.

    python3 tools/extract_binary_verbs.py > tests/binary-verbs.json
    python3 tools/extract_binary_verbs.py --get browser_sort
    python3 tools/extract_binary_verbs.py --check

Note: `extract_vdjscript_symbols.py` (nm/c++filt based) reports 0 classes on
VirtualDJ 2026 — the names survive only as mangled strings now — and
`extract_vdjscript_taxonomy.py` is address-pinned to an older build. This tool
uses the string table and works on the current one.
"""
import json
import re
import sys
import subprocess
import zipfile

APP = "/Applications/VirtualDJ.app"
BINARY = f"{APP}/Contents/MacOS/VirtualDJ"
LANGZIP = f"{APP}/Contents/Resources/languages.zip"
ARTIFACT = "tests/binary-verbs.json"


def binary_strings() -> str:
    # Default minimum length (4). A lower minimum floods the output with 2-3 char
    # fragments, which breaks the sorted-run detection in table_names() — the runs
    # stop being verb tables. Short verb names (`no`, `on`, `off`, `yes`, `jog`) are
    # consequently absent from every source here; they are documented exceptions.
    return subprocess.run(["strings", "-a", BINARY],
                          capture_output=True, text=True, errors="replace").stdout


def symbol_names(raw: str) -> set:
    """Mangled Itanium ABI names embed a length prefix: 19ACTION_browser_sort."""
    return set(re.findall(r"\d+ACTION_([a-z0-9_]+)", raw))


def table_names(raw: str) -> set:
    """Recover the parser's sorted name table as long ascending identifier runs."""
    ident = re.compile(r"^[a-z][a-z0-9_]{1,40}$")
    runs, cur = [], []
    for line in (l.strip() for l in raw.split("\n")):
        if ident.match(line) and (not cur or line > cur[-1]):
            cur.append(line)
        else:
            if len(cur) >= 200:
                runs.append(cur)
            cur = [line] if ident.match(line) else []
    if len(cur) >= 200:
        runs.append(cur)
    return set().union(*runs) if runs else set()


def catalog_names() -> set:
    data = zipfile.ZipFile(LANGZIP).read("English.xml").decode("utf-8", errors="replace")
    body = re.search(r"<Actions>(.*?)</Actions>", data, re.S)
    if not body:
        return set()
    return set(re.findall(r"<([a-z][a-z0-9_]{2,})>", body.group(1)))


def build() -> dict:
    raw = binary_strings()
    sym, cat, tbl = symbol_names(raw), catalog_names(), table_names(raw)
    out = {}
    for name in sorted(sym | cat | tbl):
        sources = [s for s, members in (("symbol", sym), ("catalog", cat), ("table", tbl))
                   if name in members]
        rec = {"sources": sources}
        # In the parser's table but with no implementation class of its own, so it
        # must dispatch to another verb: an alias or variant form.
        if "table" in sources and "symbol" not in sources:
            rec["alias_candidate"] = True
        out[name] = rec
    return {
        "summary": {
            "symbol": len(sym),
            "catalog": len(cat),
            "table": len(tbl),
            "union": len(out),
            "alias_candidates": sum(1 for r in out.values() if r.get("alias_candidate")),
        },
        "verbs": out,
    }


def cmd_get(name: str) -> None:
    data = json.load(open(ARTIFACT))["verbs"]
    rec = data.get(name)
    if rec is None:
        print(json.dumps({"name": name, "in_structured_list": False,
                          "note": "absent — NOT a disproof; aliases and variant "
                                  "spellings are legitimately absent"}, indent=1))
        return
    print(json.dumps({"name": name, "in_structured_list": True, **rec}, indent=1))


def cmd_check() -> None:
    data = json.load(open(ARTIFACT))
    verbs, summary = data["verbs"], data["summary"]
    if summary["union"] != len(verbs):
        sys.exit("binary verb list summary does not match verb count")
    if summary["symbol"] < 900 or summary["catalog"] < 700 or summary["table"] < 800:
        sys.exit(f"binary verb extraction looks broken: {summary}")
    print(f"binary verb list check passed: {summary['union']} names "
          f"({summary['symbol']} symbol, {summary['catalog']} catalog, "
          f"{summary['table']} table, {summary['alias_candidates']} alias candidates)")


def main() -> None:
    if len(sys.argv) > 2 and sys.argv[1] == "--get":
        return cmd_get(sys.argv[2])
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        return cmd_check()
    print(json.dumps(build(), indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
