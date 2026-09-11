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
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PY = sys.executable or "python3"

PROTOCOL_VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")
SERVER_INFO = {"name": "virtualdj-reference", "version": "0.1.0"}

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
    return tool_script("element_summary.py", *args)


def t_list_xml_elements(a):
    flags = opt_flags(a, {
        "family": "family", "undocumented": "undocumented",
        "has_attr": "has-attr", "min_uses": "min-uses",
        "limit": "limit", "format": "format",
    })
    term = [a["term"]] if a.get("term") else []
    return tool_script("xmldb.py", "search", *term, *flags)


def t_attested_tails(a):
    return tool_script("extract_attested_tails.py", "--verb", a["verb"])


def t_action_catalog(a):
    if a.get("cross_check"):
        return tool_script("extract_action_catalog.py", "--cross-check")
    return tool_script("extract_action_catalog.py", "--get", a["name"])


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


def t_lint(a):
    kind = a["kind"]
    script = {"skin": "lint_skins.py", "pad": "lint_pads.py",
              "mapper": "lint_mappers.py"}[kind]
    return tool_script(script, *a["paths"])


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
            "usage in shipped skins, and which of its attributes no doc explains."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": S(type="string", description="Element name, e.g. 'panel' or 'mousecircle'."),
                "format": S(type="string", enum=["text", "json"]),
            },
            "required": ["name"],
        },
        "fn": t_element,
    },
    {
        "name": "vdj_list_xml_elements",
        "description": "Search the skin/pad XML element inventory by name, family, attribute, or usage count.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "term": S(type="string"),
                "family": S(type="string"),
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
        "description": "Validate skin, pad-page, or mapper XML files before handing them back. Run this on anything you author.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "kind": S(type="string", enum=["skin", "pad", "mapper"]),
                "paths": S(type="array", items={"type": "string"},
                           description="Paths relative to the repo root."),
            },
            "required": ["kind", "paths"],
        },
        "fn": t_lint,
    },
]

BY_NAME = {t["name"]: t for t in TOOLS}


def public_tools():
    return [{k: t[k] for k in ("name", "description", "inputSchema")} for t in TOOLS]


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


def self_check():
    """Exercise the handlers in-process: no client, no live app, no state change."""
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
    check("vdj_list_xml_elements", lambda: t_list_xml_elements({"limit": 3}))
    check("vdj_attested_tails", lambda: t_attested_tails({"verb": "fadeout"}))
    check("vdj_action_catalog", lambda: t_action_catalog({"name": "get_song_event"}))

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

    if failures:
        print(f"\n{len(failures)} failure(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nself-check passed (live HTTP tools not exercised; use `just vdj-up`)")
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
        raise SystemExit(self_check())
    try:
        main()
    except (KeyboardInterrupt, BrokenPipeError):
        pass
