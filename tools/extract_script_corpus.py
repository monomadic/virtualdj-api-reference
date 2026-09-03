#!/usr/bin/env python3
"""Collect every VDJScript snippet Atomix themselves wrote, in one place.

Four sanctioned sources, kept apart by provenance because they prove different
things:

- **catalog** — snippets quoted inside the Button Editor's own action
  descriptions (`Resources/languages.zip`), the same prose the official verbs
  appendix publishes. These are documentation: they say what a form MEANS.
- **builtin** — script attributes in the shipped pad pages, skins, sampler banks
  and video skins under `examples/`. These are usage: whatever the parser
  actually accepts in a file Atomix ships.

- **binary** — VDJScript statements compiled into the app itself: the scripts
  behind its own menus, toolbars and default actions, found as string
  literals in the `__cstring` pool. Usage too, and executed by the app's own
  UI, so every form here is one the vendor runs.

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
import plistlib
import re
import sys
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_action_contracts import sections, slice_offset  # noqa: E402

DEFAULT_APP = Path("/Applications/VirtualDJ.app")
ARTIFACT = Path("tests/vdjscript-corpus.json")
VERB_TABLE = Path("tests/verb-table.json")
WIKI = Path("tests/sources/wiki-examples.json")
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
# `color 0.8 0.5 0.25` / `color 75% "red" (returns a dimmed red)`: some entries
# list examples as bare lines rather than quoting them. A line counts when it
# opens with the entry's own verb, is short, and has no prose after a trailing
# parenthetical is removed.
TRAILING_NOTE = re.compile(r"\s*\([^)]*\)\s*$")
PROSE = re.compile(r"\b(the|a|an|of|to|is|are|and|or|with|when|if|will|for|in|on|this|that|be|by|it|use|used|returns?)\b")

# --- binary source filters ---------------------------------------------------
# The string pool also holds ffmpeg option help ("set the global palette"),
# SQLite messages and UI prose, and `set`, `select`, `color`, `key` are verbs.
# A string is a statement only if it is built from script tokens and carries
# at least one marker no prose has.
STOPWORDS = {"the", "a", "an", "of", "in", "for", "to", "is", "are", "and", "with", "by",
             "when", "if", "not", "be", "this", "that", "from", "at", "as", "it", "on", "or",
             "error", "failed", "failure", "invalid", "missing", "mismatch", "supported",
             "unsupported", "cannot", "too", "because", "your", "you", "only", "while",
             "no", "yes", "new", "was", "has", "have", "use", "using", "must", "should"}
BIN_TOKEN = re.compile(r"'[^']*'|\S+")
BIN_LITERAL = re.compile(r"^[+-]?\d+(\.\d+)?(ms|bt|%|s)?$|^[+-]$")
BIN_OPERATOR = {"&", "&&", "?", ":", "(", ")"}
BIN_VARIABLE = re.compile(r"^[$%][a-z_][a-z0-9_]*$", re.I)
BIN_KEYWORD = re.compile(r"^[a-z][a-z0-9_]*$")
BIN_DECK = re.compile(r"^(deck (\d|master|left|right|active|default|all) )")
# printf/format templates (`pad %d %d`, `scratch_dna '{}'`) are patterns, not statements.
BIN_TEMPLATE = re.compile(r"%[-0-9.]*[a-zA-Z]|\{\}")


def unescape_xml(text: str) -> str:
    for entity, char in (("&apos;", "'"), ("&quot;", '"'), ("&lt;", "<"),
                         ("&gt;", ">"), ("&amp;", "&")):
        text = text.replace(entity, char)
    return text


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
        for line in text.splitlines():
            line = TRAILING_NOTE.sub("", line.strip())
            head = WORD.match(line)
            if not head or head.group(0) != name or " " not in line or len(line) > 80:
                continue
            if PROSE.search(line) or len(line.split()) > 8:
                continue
            out.append({"script": line, "source": "catalog", "origin": name,
                        "verbs": verbs_in(line, known)})
    return out


def from_builtins(known: set[str]) -> list[dict]:
    out = []
    for root in XML_ROOTS:
        for path in sorted(root.rglob("*.xml")) if root.exists() else []:
            text = path.read_text(encoding="utf-8", errors="replace")
            for attr, value in ATTR.findall(text):
                # Attribute values are XML-escaped on disk. Without this the
                # corpus stores `color &apos;red&apos;`, which no parser accepts
                # — caught by the parse-regression run, which reported eight
                # such snippets as structural failures.
                script = unescape_xml(value).strip()
                if not script or len(script) > 400:
                    continue
                found = verbs_in(script, known)
                if not found:
                    continue
                out.append({"script": script, "source": "builtin", "origin": str(path),
                            "context": attr.lower(), "verbs": found})
    return out


def from_wiki(known: set[str]) -> list[dict]:
    """Examples transcribed from the official wiki pages.

    Third source, and the only one carrying whole idioms — threading brackets,
    `while_pressed`, sweep loops — rather than single-verb forms. Transcribed by
    fetch rather than byte-verified, so every snippet is verb-checked here: a
    slip that invents a verb is dropped and reported, one that alters an
    argument is not detectable and the provenance note says so.
    """
    if not WIKI.exists():
        return []
    data = json.loads(WIKI.read_text())
    out, rejected = [], []
    for item in data["examples"]:
        script = item["script"].strip()
        found = verbs_in(script, known)
        if not found:
            rejected.append(script)
            continue
        out.append({"script": script, "source": "wiki",
                    "origin": f"wiki:{item['section']}", "verbs": found})
    if rejected:
        print(f"  {len(rejected)} wiki snippets dropped (no known verb): "
              f"{rejected[:3]}", file=sys.stderr)
    return out


def is_statement(script: str, known: set[str]) -> bool:
    """A script-shaped string: verb first, script tokens after, one marker."""
    body = BIN_DECK.sub("", script)
    tokens = BIN_TOKEN.findall(body)
    if len(tokens) < 2 or tokens[0] not in known or BIN_TEMPLATE.search(script):
        return False
    if tokens[-1] in BIN_OPERATOR or script.endswith("'") and script.count("'") % 2:
        return False  # a format prefix (`nothing & `) or an unterminated literal
    markers = plain = 0
    for tok in tokens[1:]:
        if tok.startswith("'"):
            markers += 1
        elif tok in BIN_OPERATOR or BIN_VARIABLE.match(tok) or BIN_LITERAL.match(tok):
            markers += 1
        elif tok in ("on", "off"):
            markers += 1
        elif tok in known:
            continue
        elif BIN_KEYWORD.match(tok):
            if tok in STOPWORDS:
                return False
            plain += 1  # a keyword argument, or a word of prose
        else:
            return False
    if plain >= 2:
        return False  # `no 'data' tag found`: two bare words is a sentence
    # `pad_page +1` is script; `set list`, `play count` and ffmpeg's `set
    # ambisonics_mode` are prose unless the VERB carries an underscore.
    if markers:
        return True
    return len(tokens) == 2 and "_" in tokens[0]


def from_binary(app: Path, known: set[str]) -> list[dict]:
    binary = app / "Contents/MacOS/VirtualDJ"
    if not binary.exists():
        return []
    with open(app / "Contents/Info.plist", "rb") as fh:
        build = plistlib.load(fh).get("CFBundleVersion", "?")
    data = binary.read_bytes()
    base = slice_offset(data)
    cstr = next(s for s in sections(data, base) if s[1] == "__cstring")
    blob = data[base + cstr[4]: base + cstr[4] + cstr[3]]
    out, pos = [], 0
    while pos < len(blob):
        end = blob.find(b"\0", pos)
        if end < 0:
            break
        if 3 < end - pos <= 200:
            try:
                script = blob[pos:end].decode().strip()
            except UnicodeDecodeError:
                script = ""
            if script and is_statement(script, known):
                out.append({"script": script, "source": "binary",
                            "origin": f"binary:{build}:{hex(cstr[2] + pos)}",
                            "verbs": verbs_in(script, known)})
        pos = end + 1
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
    merged = merge(from_catalog(args.app, known) + from_builtins(known)
                   + from_wiki(known) + from_binary(args.app, known))

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
