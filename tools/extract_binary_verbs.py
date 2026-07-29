#!/usr/bin/env python3
"""Extract a STRUCTURED verb list from the VirtualDJ binary and language catalog.

Two structured sources, each meaningful on its own terms:

  symbol   mangled `ACTION_<name>` implementation classes in the executable's
           string table (e.g. `19ACTION_browser_sort`). One per canonical verb
           implementation.
  catalog  action names documented in `Resources/languages.zip` -> `English.xml`
           `<Actions>`, i.e. the app's own descriptions.

Membership in either is PROOF the name is a real verb — no HTTP needed.

**It is not a completeness oracle.** Aliases and variant spellings (`hotcue`,
`auto_sync`, `pitch_slider`, `skin_pannel`, `on`/`off`) are resolved by the
parser to a canonical class and appear in NEITHER source, so absence from this
list does not disprove a name. Disproof needs the additional string/context test
in docs/Undocumented VDJScript Candidates.md.

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
    return subprocess.run(["strings", "-a", "-n", "2", BINARY],
                          capture_output=True, text=True, errors="replace").stdout


def symbol_names(raw: str) -> set:
    """Mangled Itanium ABI names embed a length prefix: 19ACTION_browser_sort."""
    return set(re.findall(r"\d+ACTION_([a-z0-9_]+)", raw))


def catalog_names() -> set:
    data = zipfile.ZipFile(LANGZIP).read("English.xml").decode("utf-8", errors="replace")
    body = re.search(r"<Actions>(.*?)</Actions>", data, re.S)
    if not body:
        return set()
    return set(re.findall(r"<([a-z][a-z0-9_]{2,})>", body.group(1)))


def build() -> dict:
    raw = binary_strings()
    sym, cat = symbol_names(raw), catalog_names()
    out = {}
    for name in sorted(sym | cat):
        sources = []
        if name in sym:
            sources.append("symbol")
        if name in cat:
            sources.append("catalog")
        out[name] = {"sources": sources}
    return {
        "summary": {
            "symbol": len(sym),
            "catalog": len(cat),
            "union": len(out),
            "both": sum(1 for r in out.values() if len(r["sources"]) == 2),
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
    if summary["symbol"] < 900 or summary["catalog"] < 700:
        sys.exit(f"binary verb extraction looks broken: {summary}")
    print(f"binary verb list check passed: {summary['union']} names "
          f"({summary['symbol']} symbol, {summary['catalog']} catalog)")


def main() -> None:
    if len(sys.argv) > 2 and sys.argv[1] == "--get":
        return cmd_get(sys.argv[2])
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        return cmd_check()
    print(json.dumps(build(), indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
