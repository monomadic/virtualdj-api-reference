#!/usr/bin/env python3
"""VirtualDJ reference MCP server — the repo's query layer over stdio.

Exposes the flat data commands (`topic`, `verb`, `get-fx`, `element`, ...) and
the live HTTP probe channel as MCP tools, so any MCP client can answer a
VirtualDJ authoring question without loading the large docs.

Zero dependencies: newline-delimited JSON-RPC 2.0 on stdin/stdout, the same
`python3 + curl` toolchain the rest of `tools/` uses. stdout carries protocol
frames only; everything else goes to stderr.

Run:      python3 tools/mcp_server.py
Register: see docs/MCP Server.md

Executing script against a live instance is off by default. Set
VDJ_MCP_EXECUTE=1 to enable `vdj_execute`; `vdj_query` is read-only and always
available.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PY = sys.executable or "python3"

PROTOCOL_VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")
SERVER_INFO = {"name": "virtualdj-reference", "version": "0.1.0"}

# Sent at initialize; clients hand it to the model before any tool description.
INSTRUCTIONS = """\
Reference and live-verification tools for VirtualDJ skins, pad pages, controller
mappers and VDJScript. VirtualDJ publishes no complete developer docs; this is the
evidence-graded reference that fills the gap.

Workflow for authoring:
1. vdj_topic <term> first. It returns the verbs, effects and XML elements for a
   topic plus real shipped files that use them; a working example often answers
   the task outright.
2. vdj_grammar before writing any VDJScript. The runtime never reports a syntax
   error, so wrong script silently does something else; the summary is short.
3. Drill in with vdj_verb, vdj_get_fx, vdj_element, vdj_controllers (mapper
   control names) or vdj_sysicons (icon keys).
4. vdj_lint everything you write: XML files or an unsaved draft (content), or one
   script string (kind script). Fix every ERROR; read every WARNING.
5. If vdj_up answers, round-trip each construct with vdj_query (read-only).

Evidence: every record carries a tier. Only local tests (HTTP interface, pad
runs, the running app) prove that something works; vendor files, the binary and
forums are leads. Do not say a verb works unless its record is test_status=Pass
or you verified it with vdj_query. Shipped files are the authority for XML format
vocabulary only.

Writes: vdj_execute runs actions on a live instance and vdj_restart quits and
relaunches the app. Each is off unless the server was started with its opt-in
(VDJ_MCP_EXECUTE=1, VDJ_MCP_RESTART=1); execute refuses destructive verbs and
restart refuses while a deck plays. Use them only when the task asks for a change
to the running app. If vdj_up stops answering mid-session, vdj_restart is the fix.
"""

SUBPROCESS_TIMEOUT = 60
HTTP_BASE = os.environ.get("VDJ_MCP_HTTP_BASE", "http://localhost")
HTTP_TIMEOUT = 5

# Verb families that must never reach a live instance through this channel.
# Mirrors the allowlist discipline in tools/probe_execute_forms.py: the cost of
# a wrong execute is unbounded (timecode_cd_mode needs an app restart to clear).
EXECUTE_DENY = re.compile(
    r"""^(?: system
          | .*delete.*
          | .*database.*
          | .*_remove(?:_.*)?
          | file_.*
          | browser_(?:delete|remove|move|rename|write|setfolder)
          | timecode_cd_mode
          | settings?_.*
          | restart | quit | exit | shutdown
        )$""",
    re.VERBOSE | re.IGNORECASE,
)


# --------------------------------------------------------------------------
# plumbing
# --------------------------------------------------------------------------

def log(msg):
    print(f"[vdj-mcp] {msg}", file=sys.stderr, flush=True)


def run(argv, timeout=SUBPROCESS_TIMEOUT):
    """Run a repo tool and return its combined output as text."""
    try:
        p = subprocess.run(
            argv, cwd=str(REPO), capture_output=True, text=True, timeout=timeout
        )
    except FileNotFoundError as e:
        raise ToolError(f"tool not found: {e}") from e
    except subprocess.TimeoutExpired:
        raise ToolError(f"timed out after {timeout}s: {' '.join(argv[1:])}")
    out = p.stdout.strip()
    err = p.stderr.strip()
    if p.returncode != 0:
        # These tools exit non-zero for "not found" as well as real failures;
        # surface whatever they said rather than swallowing it.
        return (out + ("\n" + err if err else "")).strip() or (
            f"(no output; exit {p.returncode})"
        )
    if err:
        out = (out + "\n\n[stderr] " + err).strip()
    return out or "(no output)"


def tool_script(name, *args):
    return run([PY, str(REPO / "tools" / name), *[str(a) for a in args if a is not None]])


def http(endpoint, script):
    url = f"{HTTP_BASE}/{endpoint}?" + urllib.parse.urlencode({"script": script})
    try:
        with urllib.request.urlopen(url, timeout=HTTP_TIMEOUT) as r:
            return r.read().decode("utf-8", "replace").strip()
    except urllib.error.URLError as e:
        raise ToolError(
            f"VirtualDJ HTTP interface unreachable at {HTTP_BASE} ({e.reason}). "
            "Is VirtualDJ running with the network interface enabled?"
        ) from e


class ToolError(Exception):
    pass


def opt_flags(args, names):
    """Build --flag=value args from a params dict, skipping unset values."""
    out = []
    for key, flag in names.items():
        v = args.get(key)
        if v is None or v == "":
            continue
        if v is True:
            out.append(f"--{flag}")
        elif v is not False:
            out.append(f"--{flag}={v}")
    return out


# --------------------------------------------------------------------------
# tool implementations
# --------------------------------------------------------------------------

def t_topic(a):
    args = [a["term"]]
    if a.get("limit"):
        args.append(f"--limit={a['limit']}")
    if a.get("format") == "json":
        args.append("--format=json")
    return tool_script("topic.py", *args)


def t_verb(a):
    args = [a["name"]]
    if a.get("examples"):
        args.append(f"--examples={a['examples']}")
    if a.get("format") == "json":
        args.append("--format=json")
    return tool_script("verb_summary.py", *args)


def t_get_verb(a):
    return tool_script("verbdb.py", "get", a["name"])


def t_list_verbs(a):
    flags = opt_flags(a, {
        "surface": "surface", "section": "section", "tier": "tier",
        "status": "status", "kind": "kind", "module": "module",
        "needs_test": "needs-test", "limit": "limit", "format": "format",
    })
    term = [a["term"]] if a.get("term") else []
    return tool_script("verbdb.py", "search", *term, *flags)


def t_verb_stats(a):
    return tool_script("verbdb.py", "stats")


def t_grammar(a):
    path = REPO / "docs" / "VDJScript Grammar.md"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    heads = [(i, l[3:].strip()) for i, l in enumerate(lines) if l.startswith("## ")]
    want = (a.get("section") or "").strip().lower()

    if not want or want in ("read this much", "summary"):
        # Default: the whole language in a dozen lines, plus the section list.
        start = next(i for i, h in heads if h.lower() == "read this much")
        end = next(i for i, h in heads if i > start)
        body = "\n".join(lines[start:end]).strip()
        toc = "\n".join(f"  - {h}" for _, h in heads if h.lower() != "contents")
        return (f"{body}\n\n---\nOther sections (pass `section`):\n{toc}")

    for i, h in heads:
        if want in h.lower():
            end = next((j for j, _ in heads if j > i), len(lines))
            return "\n".join(lines[i:end]).strip()
    names = ", ".join(h for _, h in heads)
    raise ToolError(f"no grammar section matching {a['section']!r}. Sections: {names}")


def t_get_fx(a):
    return tool_script("fxdb.py", "get", a["effect"])


def t_list_fx(a):
    flags = opt_flags(a, {
        "category": "category", "has_slider": "has-slider",
        "has_button": "has-button", "min_sliders": "min-sliders",
        "max_sliders": "max-sliders", "has_length": "has-length",
        "name_only": "name-only", "limit": "limit", "format": "format",
    })
    term = [a["term"]] if a.get("term") else []
    return tool_script("fxdb.py", "search", *term, *flags)


def t_element(a):
    args = [a["name"]]
    if a.get("format") == "json":
        args += ["--format", "json"]
    args += opt_flags(a, {"parents": "parents", "children": "children", "family": "family"})
    return tool_script("element_summary.py", *args)


def t_list_xml_elements(a):
    flags = opt_flags(a, {
        "family": "family", "undocumented": "undocumented",
        "has_attr": "has-attr", "min_uses": "min-uses",
        "category": "category", "uncategorized": "uncategorized", "parent": "parent", "child": "child",
        "limit": "limit", "format": "format",
    })
    term = [a["term"]] if a.get("term") else []
    return tool_script("xmldb.py", "search", *term, *flags)


def t_skin_categories(a):
    return tool_script("xmldb.py", "categories", *opt_flags(a, {"family": "family", "format": "format"}))


def t_attested_tails(a):
    return tool_script("extract_attested_tails.py", "--verb", a["verb"])


def t_action_catalog(a):
    if a.get("cross_check"):
        return tool_script("extract_action_catalog.py", "--cross-check")
    return tool_script("extract_action_catalog.py", "--get", a["name"])


def t_controllers(a):
    if a.get("path"):
        return tool_script("controller_schema_inventory.py", "--path", a["path"])
    if not a.get("device"):
        raise ToolError("pass `device` (e.g. DDJGRV6) or `path` (e.g. /device/slider)")
    args = ["--device", a["device"]]
    if not a.get("compare"):
        args.append("--controls")
        if a.get("match"):
            args += ["--match", a["match"]]
    return tool_script("controller_schema_inventory.py", *args)


def t_sysicons(a):
    args = []
    if a.get("cell"):
        args += ["--cell", a["cell"]]
    if a.get("search"):
        args += ["--search", a["search"]]
    if a.get("unnamed"):
        args.append("--unnamed")
    return tool_script("sysicon_atlas.py", *args)


def t_screenshot(a):
    """Capture the VirtualDJ window; returns text plus the PNG as an image block."""
    import base64
    args = []
    if a.get("out"):
        args += ["--out", a["out"]]
    path = tool_script("vdj_screenshot.py", *args).strip().splitlines()[-1]
    data = base64.b64encode(Path(path).read_bytes()).decode()
    return [{"type": "text", "text": f"Saved {path}"},
            {"type": "image", "data": data, "mimeType": "image/png"}]


def t_up(a):
    try:
        v = http("query", "get_version")
    except ToolError as e:
        return str(e)
    return f"VirtualDJ HTTP interface reachable at {HTTP_BASE} (get_version -> {v!r})"


def t_query(a):
    result = http("query", a["script"])
    note = ""
    if result.startswith("error:"):
        note = ("\n\n(An `error:` body means the verb or form was not recognized. "
                "The HTTP status is 200 either way — the body is the answer.)")
    return f"{result!r}{note}"


def t_execute(a):
    if os.environ.get("VDJ_MCP_EXECUTE") != "1":
        raise ToolError(
            "vdj_execute is disabled. It writes to a live VirtualDJ instance, so it "
            "is opt-in: restart this server with VDJ_MCP_EXECUTE=1. Use vdj_query "
            "for read-only probing, which needs no opt-in."
        )
    script = a["script"]
    # Every identifier-ish token, not just statement starts: a denied verb can hide
    # inside a scope wrapper (`deck 2 system ...`). Over-matching an argument only
    # costs a refusal, which is the safe direction to fail.
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", script)
    blocked = sorted({t for t in tokens if EXECUTE_DENY.match(t)})
    if blocked:
        raise ToolError(
            f"refused: {', '.join(blocked)} is in the destructive-verb denylist. "
            "Run it by hand if the task genuinely requires it."
        )
    result = http("execute", script)
    return (f"{result!r}\n\n(This is the verb's own true/false result, not transport "
            "success — `nothing` returns 'false'.)")


def t_restart(a):
    if a.get("status"):
        return tool_script("vdj_restart.py", "--status")
    if os.environ.get("VDJ_MCP_RESTART") != "1":
        raise ToolError(
            "vdj_restart is disabled. It quits and relaunches VirtualDJ, so it is opt-in: "
            "restart this server with VDJ_MCP_RESTART=1. status (read-only) needs no opt-in."
        )
    args = []
    if a.get("force"):
        args.append("--force")
    if a.get("allow_playing"):
        args.append("--allow-playing")
    for launch_arg in a.get("launch_args") or []:
        args.append(f"--arg={launch_arg}")
    # Up to three quit + launch-and-wait cycles (20s + 60s each) outlast the default timeout.
    return run([PY, str(REPO / "tools" / "vdj_restart.py"), *args], timeout=330)


def t_lint(a):
    kind = a["kind"]
    if kind == "script":
        if not a.get("content"):
            raise ToolError("kind 'script' takes the script in `content`")
        return tool_script("lint_script.py", "--script", a["content"],
                           "--context", a.get("context", "action"))
    linter = {"skin": "lint_skins.py", "pad": "lint_pads.py",
              "mapper": "lint_mappers.py"}[kind]

    def lint(paths):
        # The XML check, then the script inside it (action/query attributes, pad bodies).
        return tool_script(linter, *paths) + "\n\n" + tool_script("lint_script.py", "--xml", *paths)

    if a.get("content") and a.get("paths"):
        raise ToolError("pass `paths` or `content`, not both")
    if a.get("content"):
        # A draft from another repo: lint it from a temp file and report it as <content>.
        with tempfile.TemporaryDirectory() as tmp:
            draft = Path(tmp) / f"content.{kind}.xml"
            draft.write_text(a["content"])
            # Linters print the resolved path; on macOS the temp dir is a symlink.
            return lint([draft]).replace(str(draft.resolve()), "<content>").replace(str(draft), "<content>")
    if not a.get("paths"):
        raise ToolError(f"kind '{kind}' takes file `paths` or the XML itself in `content`")
    return lint(a["paths"])


# --------------------------------------------------------------------------
# tool declarations
# --------------------------------------------------------------------------

def S(**props):
    return props


TOOLS = [
    {
        "name": "vdj_topic",
        "description": (
            "START HERE for any 'how do I do X in VirtualDJ' question. Aggregates, for "
            "one term, the matching VDJScript verbs, effects and skin/pad XML elements, "
            "plus the real example files that use them (grep-verified, ranked by how "
            "much of the topic each demonstrates), the topical docs, and known "
            "local-test quirks. A working example often answers the task outright. "
            "Examples: 'sampler', 'colorfx', 'waveform', 'loop roll'."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "term": S(type="string", description="Topic, e.g. 'sampler' or 'colorfx'."),
                "limit": S(type="integer", description="Max items per section (default 8)."),
                "format": S(type="string", enum=["text", "json"]),
            },
            "required": ["term"],
        },
        "fn": t_topic,
    },
    {
        "name": "vdj_verb",
        "description": (
            "EVERYTHING about one VDJScript verb on one screen: store record, the "
            "vendor's own description, real usages from shipped scripts, argument shapes "
            "with return evidence, every tail candidate by source, vocabulary groups, and "
            "probe state — each labelled with its evidence tier. Use this before writing "
            "any script that calls the verb."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": S(type="string", description="Verb name, e.g. 'loop' or 'sampler_pad'."),
                "examples": S(type="integer", description="How many real usages to show."),
                "format": S(type="string", enum=["text", "json"]),
            },
            "required": ["name"],
        },
        "fn": t_verb,
    },
    {
        "name": "vdj_get_verb",
        "description": (
            "The bare store record for one verb — the authoritative per-verb fact "
            "(tier, test_status, confidence, evidence). Follows aliases and suggests near "
            "matches on a miss. Use vdj_verb when you want the full evidence picture."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"name": S(type="string")},
            "required": ["name"],
        },
        "fn": t_get_verb,
    },
    {
        "name": "vdj_list_verbs",
        "description": (
            "Find verbs when you do not know the exact name, or filter the store. "
            "IMPORTANT: check the returned tier/status before claiming a verb works — "
            "most records are catalog-tier (the vendor named it) rather than "
            "locally tested."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "term": S(type="string", description="Substring to match."),
                "surface": S(type="string", description="e.g. 'SkinQuery'."),
                "section": S(type="string", description="e.g. 'Sampler'."),
                "tier": S(type="string", description="curated | catalog | official-name-only | unofficial | alias."),
                "status": S(type="string", description="Pass | Fail | Partial | Untested."),
                "kind": S(type="string"),
                "module": S(type="string"),
                "needs_test": S(type="boolean"),
                "limit": S(type="integer"),
                "format": S(type="string", enum=["text", "json"]),
            },
        },
        "fn": t_list_verbs,
    },
    {
        "name": "vdj_verb_stats",
        "description": "Store breakdown by evidence tier and test status. Use to calibrate how much of the surface is actually verified.",
        "inputSchema": {"type": "object", "properties": {}},
        "fn": t_verb_stats,
    },
    {
        "name": "vdj_grammar",
        "description": (
            "READ THIS BEFORE WRITING ANY VDJScript. The runtime never reports a syntax "
            "error, so wrong script silently does something else — grammar is the one "
            "thing lookup cannot save you on. With no arguments returns the whole "
            "language in about a dozen lines plus a section list; pass `section` for "
            "detail (e.g. 'Conditionals', 'Variables', 'Backticks'). Skip it only if you "
            "are editing XML structure and writing no script."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "section": S(type="string", description="Optional section name; omit for the summary."),
            },
        },
        "fn": t_grammar,
    },
    {
        "name": "vdj_get_fx",
        "description": (
            "The full slider/button map for one effect, with normalized defaults. "
            "Spelling-tolerant ('BeatGrid' resolves to 'Beat Grid'). Use this instead of "
            "guessing effect parameter indices."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"effect": S(type="string", description="Effect name, e.g. 'Echo'.")},
            "required": ["effect"],
        },
        "fn": t_get_fx,
    },
    {
        "name": "vdj_list_fx",
        "description": "Search the effect catalog by name, category, or control shape.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "term": S(type="string"),
                "category": S(type="string", enum=["deck_fx", "video_fx", "transition"]),
                "has_slider": S(type="string"),
                "has_button": S(type="string"),
                "min_sliders": S(type="integer"),
                "max_sliders": S(type="integer"),
                "has_length": S(type="boolean"),
                "name_only": S(type="boolean"),
                "limit": S(type="integer"),
                "format": S(type="string", enum=["text", "json"]),
            },
        },
        "fn": t_list_fx,
    },
    {
        "name": "vdj_element",
        "description": (
            "Everything about one skin/pad XML element on one screen: inventory row, doc "
            "section, reader vocabulary, live probe results (negatives included), real "
            "usage in shipped skins, editorial categories and observed nesting. "
            "parents/children return source locations; observed nesting is not parser support."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": S(type="string", description="Element name, e.g. 'panel' or 'mousecircle'."),
                "parents": S(type="boolean"),
                "children": S(type="boolean"),
                "family": S(type="string", enum=["skins", "video_skins"], description="For parents/children lookup only."),
                "format": S(type="string", enum=["text", "json"]),
            },
            "required": ["name"],
        },
        "fn": t_element,
    },
    {
        "name": "vdj_list_xml_elements",
        "description": "Search XML elements by name, family, attribute, category or observed parent/child. Nesting is vendor corpus evidence, not parser support. Category IDs: vdj_list_skin_categories.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "term": S(type="string"),
                "family": S(type="string"),
                "category": S(type="string"),
                "uncategorized": S(type="boolean"),
                "parent": S(type="string"),
                "child": S(type="string"),
                "undocumented": S(type="boolean"),
                "has_attr": S(type="string"),
                "min_uses": S(type="integer"),
                "limit": S(type="integer"),
                "format": S(type="string", enum=["text", "json"]),
            },
        },
        "fn": t_list_xml_elements,
    },
    {
        "name": "vdj_list_skin_categories",
        "description": "List editorial skin XML category IDs and derived unique-element totals.",
        "inputSchema": {"type": "object", "properties": {
            "family": S(type="string"),
            "format": S(type="string", enum=["text", "json"]),
        }},
        "fn": t_skin_categories,
    },
    {
        "name": "vdj_attested_tails",
        "description": (
            "Argument tails Atomix themselves wrote in shipped scripts, with argument "
            "shapes and return evidence. For the many verbs whose arguments are values "
            "rather than keywords this is the only record of what a real call looks like. "
            "Check it before probing a verb's arguments."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"verb": S(type="string")},
            "required": ["verb"],
        },
        "fn": t_attested_tails,
    },
    {
        "name": "vdj_action_catalog",
        "description": (
            "The vendor's own description and documented parameters for a verb, read "
            "offline from the app bundle's language resources — the same prose "
            "virtualdj.com publishes. Pass cross_check instead of name to diff documented "
            "parameters against probe findings."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": S(type="string"),
                "cross_check": S(type="boolean"),
            },
        },
        "fn": t_action_catalog,
    },
    {
        "name": "vdj_controllers",
        "description": (
            "Controller vocabulary for writing a mapper. device (a built-in identifier such "
            "as DDJGRV6, substring allowed) lists the control names its shipped definition "
            "declares — the names <map value=\"\"> refers to — grouped by element, with the "
            "device's decks and pad layout; match narrows the names. compare instead shows "
            "how the repo's own mappers for that device line up with the shipped ones. path "
            "(e.g. /device/slider) shows which attributes shipped definitions use on an XML "
            "path. All of it is shipped syntax (Tier 2): it says what Atomix wrote, not what "
            "the parser accepts or what a control does."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "device": S(type="string"),
                "match": S(type="string", description="With device: keep control names containing this."),
                "compare": S(type="boolean", description="With device: local-vs-shipped mapper comparison instead."),
                "path": S(type="string", description="An XML path in device definitions, e.g. /device/slider."),
            },
        },
        "fn": t_controllers,
    },
    {
        "name": "vdj_sysicons",
        "description": (
            "Built-in skin icon atlas: each cell's description and the key that names it for "
            "skins and pads, with how the key is known — wiki-listed, tested live, or only a "
            "binary candidate (a lead, not proof). search matches descriptions and keys "
            "('sideview', 'play'); cell takes an atlas cell such as H6; unnamed lists the "
            "cells the wiki gives no key. Unknown means no key established here, not that "
            "none exists."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "search": S(type="string"),
                "cell": S(type="string"),
                "unnamed": S(type="boolean"),
            },
        },
        "fn": t_sysicons,
    },
    {
        "name": "vdj_screenshot",
        "description": (
            "Screenshot the VirtualDJ window (macOS; needs Screen Recording permission). "
            "Saves a PNG under tests/screenshots/ (or out) and returns it as an image. A UI "
            "observation is evidence only if the file is kept: cite the returned path."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"out": S(type="string", description="Output PNG path; default tests/screenshots/virtualdj-<timestamp>.png.")},
        },
        "fn": t_screenshot,
    },
    {
        "name": "vdj_restart",
        "description": (
            "Quit and relaunch VirtualDJ (macOS), then wait until its HTTP interface answers. "
            "Use it when the interface stops answering after a crash-recover, to clear session "
            "state or timecode_cd_mode, or to launch with arguments (launch_args, e.g. -remote). "
            "Off unless the server runs with VDJ_MCP_RESTART=1. Refuses while any deck plays "
            "(allow_playing overrides) and when playback cannot be checked (force overrides; "
            "force also terminates a quit that stalls). status reports state and changes nothing."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": S(type="boolean", description="Report running / answering / playing; change nothing."),
                "force": S(type="boolean"),
                "allow_playing": S(type="boolean"),
                "launch_args": S(type="array", items={"type": "string"}),
            },
        },
        "fn": t_restart,
    },
    {
        "name": "vdj_up",
        "description": "Check whether a live VirtualDJ is reachable over the HTTP control interface. Run this before planning any live-test work.",
        "inputSchema": {"type": "object", "properties": {}},
        "fn": t_up,
    },
    {
        "name": "vdj_query",
        "description": (
            "VERIFY YOUR SCRIPT. Evaluates a VDJScript query against the live instance and "
            "returns the exact result string. Read-only and safe to sweep — use it freely "
            "to confirm a verb exists, check a value, or test a construct before handing "
            "script back. An 'error:' body means the verb or form was not recognized "
            "(HTTP status is 200 either way). Note: a verb's value is not its truth — "
            "get_version reports 2026 and is false as a condition."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"script": S(type="string", description="VDJScript query, e.g. \"get_effect_name 1\".")},
            "required": ["script"],
        },
        "fn": t_query,
    },
    {
        "name": "vdj_execute",
        "description": (
            "Run a VDJScript action against the live instance. WRITES TO A RUNNING APP — "
            "disabled unless the server was started with VDJ_MCP_EXECUTE=1, and "
            "destructive verb families are refused outright. Execute only verbs the "
            "current task names. Prefer vdj_query, which proves existence and value "
            "without changing state."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"script": S(type="string")},
            "required": ["script"],
        },
        "fn": t_execute,
    },
    {
        "name": "vdj_lint",
        "description": (
            "Validate what you author before handing it back. kind skin/pad/mapper checks XML "
            "files and then the VDJScript inside them; kind script checks one script string. "
            "The runtime never reports a script error, so this is the only static check there "
            "is. Each finding cites its evidence: ERROR is broken, WARNING is legal but tested "
            "to misbehave, NOTE is a known trap that may be intended. It does not run anything; "
            "verify behaviour with vdj_query."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "kind": S(type="string", enum=["skin", "pad", "mapper", "script"]),
                "paths": S(type="array", items={"type": "string"},
                           description="For skin/pad/mapper: absolute paths, or paths relative to the repo root."),
                "content": S(type="string", description="The VDJScript to check (kind script), or an unsaved XML draft instead of paths."),
                "context": S(type="string", enum=["action", "query"],
                             description="For script: where it runs, e.g. action= vs query=/visibility= (default action)."),
            },
            "required": ["kind"],
        },
        "fn": t_lint,
    },
]

BY_NAME = {t["name"]: t for t in TOOLS}

# MCP tool annotations: clients use them to auto-approve safe calls and to ask
# before others. Every tool is listed explicitly — the self-check fails on a tool
# missing here, so a new write tool cannot inherit a read-only label by default.
READ = {"readOnlyHint": True, "openWorldHint": False}
LIVE_READ = {"readOnlyHint": True, "openWorldHint": True}  # asks the running app
ANNOTATIONS = {
    **{name: READ for name in (
        "vdj_topic", "vdj_verb", "vdj_get_verb", "vdj_list_verbs", "vdj_verb_stats",
        "vdj_grammar", "vdj_get_fx", "vdj_list_fx", "vdj_element", "vdj_list_xml_elements",
        "vdj_list_skin_categories", "vdj_attested_tails", "vdj_action_catalog",
        "vdj_controllers", "vdj_sysicons", "vdj_lint")},
    "vdj_up": LIVE_READ,
    "vdj_query": LIVE_READ,
    # Writes a PNG under tests/screenshots/; changes nothing it did not create.
    "vdj_screenshot": {"readOnlyHint": False, "destructiveHint": False,
                       "idempotentHint": False, "openWorldHint": True},
    # Quits and relaunches the app; `status` is the only read-only form.
    "vdj_restart": {"readOnlyHint": False, "destructiveHint": True,
                    "idempotentHint": False, "openWorldHint": True},
    # Runs actions on the live app; the denylist narrows it, it does not make it safe.
    "vdj_execute": {"readOnlyHint": False, "destructiveHint": True,
                    "idempotentHint": False, "openWorldHint": True},
}


def public_tools():
    return [{**{k: t[k] for k in ("name", "description", "inputSchema")},
             "annotations": ANNOTATIONS[t["name"]]} for t in TOOLS if t["name"] in ANNOTATIONS]


# --------------------------------------------------------------------------
# JSON-RPC
# --------------------------------------------------------------------------

def handle(msg):
    """Return a response dict, or None for notifications."""
    mid = msg.get("id")
    method = msg.get("method")
    params = msg.get("params") or {}

    if method == "initialize":
        want = params.get("protocolVersion")
        version = want if want in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0]
        return ok(mid, {
            "protocolVersion": version,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": SERVER_INFO,
            "instructions": INSTRUCTIONS,
        })

    if method in ("notifications/initialized", "notifications/cancelled"):
        return None

    if method == "ping":
        return ok(mid, {})

    if method == "tools/list":
        return ok(mid, {"tools": public_tools()})

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        tool = BY_NAME.get(name)
        if tool is None:
            return err(mid, -32602, f"unknown tool: {name}")
        try:
            text = tool["fn"](args)
            if isinstance(text, list):  # tool returned ready-made content blocks
                return ok(mid, {"content": text})
            return ok(mid, {"content": [{"type": "text", "text": text}]})
        except ToolError as e:
            return ok(mid, {"content": [{"type": "text", "text": str(e)}], "isError": True})
        except KeyError as e:
            return ok(mid, {"content": [{"type": "text",
                                         "text": f"missing required argument: {e}"}],
                            "isError": True})
        except Exception as e:  # never let one bad call kill the server
            log(f"tool {name} failed: {e!r}")
            return ok(mid, {"content": [{"type": "text", "text": f"{type(e).__name__}: {e}"}],
                            "isError": True})

    if mid is None:
        return None
    return err(mid, -32601, f"method not found: {method}")


def ok(mid, result):
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def err(mid, code, message):
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}}


def stdio_check(failures):
    """Drive the real server over stdio from a foreign cwd, as another repo's client would.

    The in-process checks call handlers directly, so they cannot see a stray print on
    stdout, a path that only resolves from the repo root, or a framing bug.
    """
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "vdj_lint", "arguments": {
            "kind": "pad", "content": "<page name=\"draft\">\n<pad1>shift ? play : </pad1>\n</page>\n"}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "vdj_nope", "arguments": {}}},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "vdj_execute", "arguments": {"script": "play"}}},
        {"jsonrpc": "2.0", "id": 6, "method": "ping"},
        {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "vdj_restart", "arguments": {}}},
    ]
    stdin = "\n".join(json.dumps(r) for r in requests[:4]) + "\n{not json\n" + \
            "\n".join(json.dumps(r) for r in requests[4:]) + "\n"
    env = {k: v for k, v in os.environ.items() if k not in ("VDJ_MCP_EXECUTE", "VDJ_MCP_RESTART")}
    with tempfile.TemporaryDirectory() as tmp:
        try:
            proc = subprocess.run([PY, str(Path(__file__).resolve())], input=stdin, cwd=tmp, env=env,
                                  capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT)
        except subprocess.TimeoutExpired:
            failures.append("stdio: server did not exit at end of input")
            return
    frames = []
    for line in proc.stdout.splitlines():
        try:
            frames.append(json.loads(line))
        except json.JSONDecodeError:
            failures.append(f"stdio: non-JSON on stdout: {line[:120]!r}")
    by_id = {f.get("id"): f for f in frames}
    if sorted(by_id) != [1, 2, 3, 4, 5, 6, 7]:
        failures.append(f"stdio: expected one response per request id 1-7, got {sorted(by_id, key=str)}")
        return
    if "instructions" not in by_id[1].get("result", {}):
        failures.append("stdio: initialize carried no instructions")
    if len(by_id[2]["result"]["tools"]) != len(TOOLS):
        failures.append("stdio: tools/list did not return every tool")
    text = by_id[3]["result"]["content"][0]["text"]
    if "<content>:2" not in text or "empty-branch" not in text or tmp in text:
        failures.append(f"stdio: lint of a draft from a foreign cwd went wrong: {text[:200]}")
    if by_id[4].get("error", {}).get("code") != -32602:
        failures.append("stdio: unknown tool was not a -32602 error")
    if not by_id[5]["result"].get("isError") or "disabled" not in by_id[5]["result"]["content"][0]["text"]:
        failures.append("stdio: vdj_execute ran without VDJ_MCP_EXECUTE=1")
    if by_id[6].get("result") != {}:
        failures.append("stdio: ping did not answer")
    if not by_id[7]["result"].get("isError") or "disabled" not in by_id[7]["result"]["content"][0]["text"]:
        failures.append("stdio: vdj_restart ran without VDJ_MCP_RESTART=1")
    print(f"  ok    stdio from a foreign cwd: {len(frames)} frames, bad JSON survived, "
          "execute and restart refused without opt-in")


def live_check(failures):
    """Read-only calls against a running VirtualDJ; skipped when it does not answer."""
    up = t_up({})
    if "reachable at" not in up:
        print(f"  skip  live tools: {up.splitlines()[0]}")
        return
    print(f"  ok    vdj_up  ({up})")
    version = t_query({"script": "get_version"})
    if "error:" in version:
        failures.append(f"vdj_query get_version failed: {version}")
    unknown = t_query({"script": "zzinvalidalpha"})
    if not unknown.startswith("'error:"):
        failures.append(f"vdj_query did not report an unknown verb as error: {unknown[:120]}")
    print(f"  ok    vdj_query  (get_version -> {version.splitlines()[0]}; an unknown verb -> error body)")
    state = t_restart({"status": True})
    if "running:" not in state:
        failures.append(f"vdj_restart status failed: {state[:120]}")
    print(f"  ok    vdj_restart status  ({state.strip()})")


def self_check(live=False):
    """Exercise the handlers in-process, then over stdio; --live adds read-only live calls."""
    failures = []

    def check(label, fn):
        try:
            out = fn()
        except Exception as e:
            failures.append(f"{label}: {type(e).__name__}: {e}")
            print(f"  FAIL  {label}: {type(e).__name__}: {e}")
            return
        print(f"  ok    {label}  ({len(out)} chars)")

    print(f"{len(TOOLS)} tools declared")
    for t in TOOLS:
        if t["name"] not in ANNOTATIONS:
            failures.append(f"{t['name']}: no entry in ANNOTATIONS (read-only or not must be stated)")
    for name in set(ANNOTATIONS) - set(BY_NAME):
        failures.append(f"ANNOTATIONS lists {name}, which is not a tool")
    for t in TOOLS:
        for field in ("name", "description", "inputSchema"):
            if not t.get(field):
                failures.append(f"{t.get('name', '?')}: missing {field}")
        schema = t["inputSchema"]
        for req in schema.get("required", []):
            if req not in schema.get("properties", {}):
                failures.append(f"{t['name']}: required '{req}' is not a declared property")

    r = handle({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {"protocolVersion": "2025-06-18"}})
    if r["result"]["protocolVersion"] != "2025-06-18":
        failures.append("initialize did not echo a supported protocol version")
    # Every tool the instructions name must exist.
    for named in sorted(set(re.findall(r"\bvdj_[a-z_]+", r["result"].get("instructions", "")))):
        if named not in BY_NAME:
            failures.append(f"instructions name {named}, which is not a tool")
    if handle({"jsonrpc": "2.0", "method": "notifications/initialized"}) is not None:
        failures.append("notification produced a response")
    if len(handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})["result"]["tools"]) != len(TOOLS):
        failures.append("tools/list did not return every tool")

    # Offline calls only — nothing here touches a running VirtualDJ.
    check("vdj_grammar", lambda: t_grammar({}))
    check("vdj_grammar section", lambda: t_grammar({"section": "Conditionals"}))
    check("vdj_topic", lambda: t_topic({"term": "sampler", "limit": 3}))
    check("vdj_verb", lambda: t_verb({"name": "loop"}))
    check("vdj_get_verb", lambda: t_get_verb({"name": "beatjump"}))
    check("vdj_list_verbs", lambda: t_list_verbs({"section": "Sampler", "limit": 3}))
    check("vdj_verb_stats", lambda: t_verb_stats({}))
    check("vdj_get_fx", lambda: t_get_fx({"effect": "Echo"}))
    check("vdj_list_fx", lambda: t_list_fx({"category": "video_fx", "limit": 3}))
    check("vdj_element", lambda: t_element({"name": "panel"}))
    check("vdj_list_skin_categories", lambda: t_skin_categories({"format": "json"}))
    check("vdj_element children", lambda: t_element({"name": "button", "children": True, "family": "video_skins"}))
    check("vdj_list_xml_elements parent", lambda: t_list_xml_elements({"parent": "button", "category": "text-labels", "limit": 2}))
    check("vdj_list_xml_elements", lambda: t_list_xml_elements({"limit": 3}))
    check("vdj_attested_tails", lambda: t_attested_tails({"verb": "fadeout"}))
    check("vdj_action_catalog", lambda: t_action_catalog({"name": "get_song_event"}))
    # Committed inventory; the control listing needs the gitignored vendor tree and
    # says so when it is absent, which is an answer, not a failure.
    check("vdj_controllers path", lambda: t_controllers({"path": "/device/slider"}))
    check("vdj_controllers device", lambda: t_controllers({"device": "DDJGRV6", "match": "loop"}))
    check("vdj_sysicons", lambda: t_sysicons({"search": "sideview"}))

    # vdj_lint must lint the file it is given: a malformed page fails, a real one passes.
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "broken.xml"
        bad.write_text("<page name=\"broken\">\n<pad><<<\n")
        out = t_lint({"kind": "pad", "paths": [str(bad)]})
        if "parse error" not in out:
            failures.append(f"vdj_lint pad passed a malformed file: {out[:200]}")
        bad.write_text("<skin>\n<panel>\n<button action=\"play_pause\"\n")
        out = t_lint({"kind": "skin", "paths": [str(bad)]})
        if "FAILED" not in out:
            failures.append(f"vdj_lint skin passed a malformed file: {out[:200]}")
    # A repo test page, not a Built-In copy: shipped pages omit name="", which
    # the linter rightly requires of authored ones.
    good = sorted((REPO / "tests" / "Pads").rglob("*.xml"))[:1]
    out = t_lint({"kind": "pad", "paths": [str(p) for p in good]})
    if "passed: 1 XML files" not in out:
        failures.append(f"vdj_lint pad did not lint exactly the given file: {out[:200]}")
    print("  ok    vdj_lint pad/skin fail a malformed file; pad lints only the paths given")

    out = t_lint({"kind": "script", "content": "shift ? loop 32 ? : off"})
    if "empty-branch" not in out or "FAILED" not in out:
        failures.append(f"vdj_lint script missed an empty branch: {out[:200]}")
    out = t_lint({"kind": "script", "content": "var_equal '$x' 1 ? play : nothing"})
    if "passed" not in out:
        failures.append(f"vdj_lint script failed a clean script: {out[:200]}")
    print("  ok    vdj_lint script fails an empty branch and passes a clean ternary")

    out = t_lint({"kind": "pad", "content": "<page name=\"draft\">\n<pad1>shift ? loop 32 ? : off</pad1>\n</page>\n"})
    if "Pads lint passed: 1 XML files" not in out or " <content>:2" not in out or "empty-branch" not in out:
        failures.append(f"vdj_lint pad content did not lint the draft: {out[:300]}")
    out = t_lint({"kind": "mapper", "content": "<mapper device=\"x\">\n<map value=\"PLAY\" action=\"none\"/>\n</mapper>"})
    if "disproved" not in out:
        failures.append(f"vdj_lint mapper content missed a disproved verb: {out[:300]}")
    print("  ok    vdj_lint content: a pad draft and a mapper draft are linted as <content>")

    # The execute gate must refuse, whether or not the opt-in is set.
    for script in ("system 'x'", "deck 2 system 'x'", "browser_delete", "timecode_cd_mode 1"):
        os.environ["VDJ_MCP_EXECUTE"] = "1"
        try:
            t_execute({"script": script})
        except ToolError as e:
            if "denylist" not in str(e):
                failures.append(f"execute gate wrong refusal for {script!r}: {e}")
        else:
            failures.append(f"execute gate did NOT refuse {script!r}")
        finally:
            os.environ.pop("VDJ_MCP_EXECUTE", None)
    print("  ok    execute denylist refuses system / scope-wrapped / browser_delete / timecode_cd_mode")

    stdio_check(failures)
    if live:
        live_check(failures)

    if failures:
        print(f"\n{len(failures)} failure(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nself-check passed" + ("" if live else " (live tools not exercised; `just mcp-check --live`)"))
    return 0


def main():
    log(f"serving {len(TOOLS)} tools from {REPO}"
        f"{'' if os.environ.get('VDJ_MCP_EXECUTE') == '1' else ' (execute disabled)'}")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError as e:
            log(f"bad JSON: {e}")
            continue
        for one in (msg if isinstance(msg, list) else [msg]):
            try:
                resp = handle(one)
            except Exception as e:
                log(f"handler crashed: {e!r}")
                resp = err(one.get("id"), -32603, str(e))
            if resp is not None:
                sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    if "--self-check" in sys.argv[1:]:
        raise SystemExit(self_check(live="--live" in sys.argv[1:]))
    try:
        main()
    except (KeyboardInterrupt, BrokenPipeError):
        pass
