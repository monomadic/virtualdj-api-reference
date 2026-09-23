#!/usr/bin/env python3
"""Collect every VDJScript snippet Atomix themselves wrote, in one place.

Sanctioned sources, kept apart by provenance because they prove different
things:

- **catalog** — snippets quoted inside the Button Editor's own action
  descriptions (`Resources/languages.zip`), the same prose the official verbs
  appendix publishes. These are documentation: they say what a form MEANS.
- **builtin** — script attributes in the shipped pad pages, skins, sampler banks
  and video skins under `examples/`. These are usage: whatever the parser
  actually accepts in a file Atomix ships.

- **addon** — the same script attributes, plus the one add-on mapper, in the
  Atomix-published add-ons under `examples/*/Official-Addons/`. Usage as well,
  and the only source covering the controller *screen* skins and the browser,
  sideview and playlist verbs a bundle skin never writes. Graded apart from
  `builtin` because these are catalog downloads, not bundle members, so
  check_bundle_copies.py cannot hold them against a file the app still ships.
- **mapper** — the `action=""` of each `<map>` in a shipped factory controller
  mapping. Usage, and the only source that exercises the hardware families:
  `padshift`, `pad_button_color`, `get_key_modifier`, `silent_cue` and the
  `SHIFT`/`ONINIT`/`LED_*` idioms appear in no skin or pad page, because no skin
  has a shift key. Graded apart from `builtin` because a mapping reaches this
  repo as a file copied off a local install, not as a file read from the bundle.
- **factory** — every `<map action="">` in the factory controller mappings, and
  every `onchange=""` callback in the device definitions, decoded from the
  bundle's `controllers.dat` (`just controllers-vendor`; format in
  docs/Compiled Controller Definitions.md). Usage, from the vendor's own files,
  and by far the largest script corpus Atomix has published: hundreds of
  mappings, each carrying the verbs a skin never touches — the mixer, EQ,
  timecode, and hardware-display families. The decoded XML is vendor
  copyright and lives under the gitignored `vendor/` tree, never in `tests/`;
  each file is verified against the committed manifest's SHA-256 before it is
  read, so a stale or edited extraction cannot attest anything.
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

# Atomix-published add-ons: same authorship as the bundle trees, but they are
# NOT bundle copies, so they get their own `addon` source rather than joining
# `builtin`. check_bundle_copies.py verifies every `builtin` snippet against a
# file the installed app still ships, and an add-on has no bundle member to
# match. Authorship is the add-on catalog's `author: "Atomix Productions"`, per
# folder, not the XML `author=` attribute — see examples/Mappers/README.md for
# why that attribute grades nothing. Each folder's README records the add-on id
# and the installed zip's SHA-256.
ADDON_XML_ROOTS = (Path("examples/Pads/Official-Addons"),
                   Path("examples/Skins/Official-Addons"),
                   Path("examples/Samplerbanks/Official-Addons"))

# Named one by one, never globbed: `examples/Mappers/` also holds personal
# mappings, and a personal mapping legitimately contains experiments and guesses
# that were never claimed to work (examples/Mappers/README.md). A glob would let
# one land in the corpus the day it is added.
#
# Only the DDJ-XP2 file qualifies. It is Atomix's shipped factory mapping for
# that controller, `author="Atomix Productions"`, copied unmodified. The
# DDJ-GRV6 "Factory Default" file is deliberately NOT here: it is a local
# *export* produced by Settings -> Controllers -> Factory default -> Save on
# this machine, not a file Atomix shipped, so it carries a round-trip through
# the app's own writer that nothing here has checked.
MAPPER_FILES = (Path("examples/Mappers/Local/Pioneer DDJ-XP2 - Pioneer DDJ-XP2.xml"),)

# The mapper half of an Atomix controller add-on, named for the same reason.
# The definition beside it (`<device>`) is not mined here: `onchange` is the one
# definition attribute that holds script, and from_factory already reads it.
ADDON_MAPPER_FILES = (
    Path("examples/Mappers/Official-Addons/Traktor Kontrol S4 MK3/"
         "Traktor Kontrol S4 MK3 mapping.xml"),
)

# The decoded controller archive: gitignored (vendor copyright, like the SDK
# headers), regenerated by `just controllers-vendor`, and trusted only where a
# file's SHA-256 matches the committed manifest the reader wrote from the same
# bundle. One tree and one manifest PER ARCHIVE, keyed `<bundle>-r<revision>`
# (tools/controller_archives.py): a full extraction mines the installed app's
# archive; `--check` re-verifies the archive the artifact was mined from, and
# says so instead of failing when this machine holds a different one.
# `onchange` is the one attribute in a <device> definition that holds script
# (AKAI APC64's AfterTouchVelocity setting).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from controller_archives import (archive_key, find_manifest, load_manifest,  # noqa: E402
                                 vendor_dir)
ONCHANGE = re.compile(r'\bonchange\s*=\s*"([^"]*)"', re.I)

# In a mapper, `value=""` is the CONTROL NAME (`PLAY_PAUSE`, `SHIFT`, `LED_CUE`),
# not script — and some control names collide with real verb names (`SEARCH`,
# `PREVIEW`, `REVERSE`), so running SCRIPT_ATTRS over a mapper would mint
# snippets out of hardware labels. Only `<map action="">` holds script.
MAP_ACTION = re.compile(r'<map\b[^>]*\baction\s*=\s*"([^"]*)"', re.I)

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


def from_builtins(known: set[str], roots: tuple[Path, ...] = XML_ROOTS,
                  source: str = "builtin") -> list[dict]:
    out = []
    for root in roots:
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
                out.append({"script": script, "source": source, "origin": str(path),
                            "context": attr.lower(), "verbs": found})
    return out


def from_mappers(known: set[str], files: tuple[Path, ...] = MAPPER_FILES,
                 source: str = "mapper") -> list[dict]:
    """Script bound to hardware controls in a shipped factory mapping."""
    out = []
    for path in files:
        if not path.exists():
            continue
        for value in MAP_ACTION.findall(path.read_text(encoding="utf-8", errors="replace")):
            script = unescape_xml(value).strip()
            if not script or len(script) > 400:
                continue
            found = verbs_in(script, known)
            if not found:
                continue
            out.append({"script": script, "source": source, "origin": str(path),
                        "context": "map", "verbs": found})
    return out


def from_addons(known: set[str]) -> list[dict]:
    """Script in an Atomix-published add-on: pad pages, skins, sampler banks,
    and the one add-on mapper. Kept apart from `builtin` because these files
    are not bundle members (see ADDON_XML_ROOTS)."""
    return (from_builtins(known, ADDON_XML_ROOTS, "addon")
            + from_mappers(known, ADDON_MAPPER_FILES, "addon"))


def installed_or_unknown(app: Path) -> str:
    from controller_archives import installed_bundle_version
    return installed_bundle_version(app) or "no app found"


def resolve_archive(app: Path | None = None, key: str | None = None) -> dict | None:
    """The manifest to mine or verify: an explicit key, else the installed app's build."""
    if key:
        return load_manifest(key)
    path = find_manifest(app=app) if app else None
    return load_manifest(path) if path else None


def vendor_controller_files(manifest: dict | None) -> list[tuple[Path, str]]:
    """(path, root) for every decoded archive member whose bytes match the manifest.

    Returns [] when the extraction is absent; raises when it is present but
    disagrees with the manifest, because a mismatch means the vendor tree is
    stale or edited and must not be mined as evidence.
    """
    if manifest is None:
        return []
    tree = vendor_dir(manifest["_key"])
    if not tree.exists():
        return []
    import hashlib
    out, bad = [], []
    for index, block in enumerate(manifest["blocks"]):
        for member in block["members"]:
            path = tree / f"block-{index:03d}" / member["name"]
            if not path.exists():
                bad.append(f"missing {path}")
                continue
            if hashlib.sha256(path.read_bytes()).hexdigest() != member["sha256"]:
                bad.append(f"sha256 mismatch {path}")
                continue
            out.append((path, member["root"]))
    if bad:
        sys.exit(f"{tree} disagrees with {manifest['_path']} "
                 f"({len(bad)} files, first: {bad[0]}) — delete it and rerun "
                 "`just controllers-vendor`")
    return out


def from_factory(known: set[str], manifest: dict | None) -> list[dict]:
    """Script in the factory mappings and device definitions decoded from controllers.dat.
    The origin carries the archive key, so a snippet names the build and revision it came from."""
    out = []
    root_dir = Path(__file__).resolve().parents[1]
    for path, root in vendor_controller_files(manifest):
        text = path.read_text(encoding="utf-8", errors="replace")
        if root == "mapper":
            pairs = [("map", v) for v in MAP_ACTION.findall(text)]
        elif root == "device":
            pairs = [("onchange", v) for v in ONCHANGE.findall(text)]
        else:
            continue
        for context, value in pairs:
            script = unescape_xml(value).strip()
            if not script or len(script) > 400:
                continue
            found = verbs_in(script, known)
            if not found:
                continue
            out.append({"script": script, "source": "factory",
                        "origin": str(path.relative_to(root_dir)),
                        "context": context, "verbs": found})
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


# `eq_low` appears in over three hundred factory mappings. Listing every file
# would multiply the artifact by the corpus size for no evidence gain, so a
# snippet keeps one origin per (source, attribute) pair — enough for the tail
# extractor to see every context it was written in — and counts the rest.
def merge(entries: list[dict]) -> dict[str, dict]:
    merged: dict[str, dict] = {}
    for entry in entries:
        record = merged.setdefault(entry["script"], {
            "script": entry["script"], "verbs": entry["verbs"],
            "sources": [], "origins": [], "occurrences": 0})
        record["occurrences"] += 1
        if entry["source"] not in record["sources"]:
            record["sources"].append(entry["source"])
        context = entry.get("context")
        origin = entry["origin"] + (f"@{context}" if context else "")
        key = (entry["source"], context)
        seen = record.setdefault("_keys", set())
        if key not in seen:
            seen.add(key)
            record["origins"].append(origin)
    for record in merged.values():
        record.pop("_keys", None)
    return merged


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=Path, default=DEFAULT_APP)
    parser.add_argument("--verb", help="only snippets mentioning this verb")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--vendor-check", action="store_true",
                        help="verify the decoded archive against its manifest and stop")
    parser.add_argument("--controllers", metavar="KEY",
                        help="mine this archive (`18.0.9598-r2241`, or a bundle version) "
                             "instead of the installed app's")
    args = parser.parse_args()

    if args.vendor_check:
        manifest = resolve_archive(args.app, args.controllers)
        if manifest is None:
            sys.exit(f"no controller manifest for the installed build "
                     f"({installed_or_unknown(args.app)}) — run `just controllers-vendor`")
        files = vendor_controller_files(manifest)
        if not files:
            sys.exit(f"vendor/controllers/{manifest['_key']} is absent — run `just controllers-vendor`")
        print(f"vendor/controllers/{manifest['_key']} verified: {len(files)} files match "
              f"tests/controllers-manifests/{manifest['_key']}.json")
        return 0

    known = set(json.load(open(VERB_TABLE))["verbs"])

    if args.check:
        if not ARTIFACT.exists():
            print("script corpus check skipped: tests/vdjscript-corpus.json not extracted yet")
            return 0
        stored = json.load(open(ARTIFACT))["summary"]
        # Verify the archive the ARTIFACT was mined from, not whichever is installed:
        # a per-archive layout means both can be present, and only the stamped one
        # can reproduce the stamped counts.
        stamped = stored.get("factory_archive") or stored.get("factory_bundle")
        manifest = load_manifest(stamped) if stamped else None
        if stored["by_source"].get("factory") and manifest is None:
            sys.exit("script corpus check FAILED: the artifact carries factory-mapping "
                     f"snippets but no manifest matches its stamp {stamped!r}")
        factory = from_factory(known, manifest)
        if stored["by_source"].get("factory") and not factory:
            installed = installed_or_unknown(args.app)
            print(f"script corpus check skipped: artifact mined factory snippets from "
                  f"controller archive {manifest['_key']}, which is not decoded here "
                  f"(installed build {installed}) — `just controllers-vendor` on a "
                  f"{manifest['bundle_version']} install re-verifies it; to re-anchor, "
                  f"`just script-corpus > tests/vdjscript-corpus.json` on this build")
            return 0
        merged = merge(from_catalog(args.app, known) + from_builtins(known)
                       + from_addons(known) + from_mappers(known) + factory
                       + from_wiki(known) + from_binary(args.app, known))
        if stored["snippets"] != len(merged):
            sys.exit(f"script corpus check FAILED: artifact has {stored['snippets']} snippets, "
                     f"re-extraction finds {len(merged)} — re-extract")
        print(f"script corpus check passed: {stored['snippets']} snippets "
              f"({stored['by_source']}), covering {stored['verbs_covered']} verbs"
              + (f", factory archive {manifest['_key']}" if manifest else ""))
        return 0

    manifest = resolve_archive(args.app, args.controllers)
    factory = from_factory(known, manifest)
    merged = merge(from_catalog(args.app, known) + from_builtins(known)
                   + from_addons(known) + from_mappers(known) + factory
                   + from_wiki(known) + from_binary(args.app, known))

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
            "factory_bundle": manifest["bundle_version"] if factory else None,
            "factory_archive": manifest["_key"] if factory else None,
            "verbs_covered": len(by_verb),
            "most_exampled": sorted(by_verb.items(), key=lambda kv: -kv[1])[:15],
        },
        "snippets": sorted(merged.values(), key=lambda r: r["script"]),
    }, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
