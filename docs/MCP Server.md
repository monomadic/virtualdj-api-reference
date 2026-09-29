# MCP Server

`tools/mcp_server.py` serves this repo's query layer to any MCP client over stdio, so an
agent can author VirtualDJ skins, pad pages, mappers and VDJScript without loading the
large docs into context.

The economics are the point. The Markdown under `docs/` is over a megabyte and the XML
under `examples/` is several times that; a single `vdj_topic` call answers a typical
authoring question in about a thousand tokens, and answers it *better*, because it returns
grep-verified real example files ranked by how much of the topic each demonstrates.

Zero dependencies — newline-delimited JSON-RPC 2.0 on stdin/stdout, the same
`python3 + curl` toolchain as the rest of `tools/`. There is no `mcp` package to install
and no virtualenv to maintain. stdout carries protocol frames only; logs go to stderr.

## Registering it

Inside this checkout nothing is needed: the repo's `.mcp.json` registers it. To use it from
every project — the point of it — register it once at user scope with Claude Code:

```bash
claude mcp add --scope user virtualdj -- python3 /absolute/path/to/virtualdj-api-reference/tools/mcp_server.py
```

The equivalent JSON (`.mcp.json` in a repo root, or `~/.claude.json` for a user-level entry):

```json
{
  "mcpServers": {
    "virtualdj": {
      "command": "python3",
      "args": ["/absolute/path/to/virtualdj-api-reference/tools/mcp_server.py"]
    }
  }
}
```

Claude Desktop uses the same shape in `claude_desktop_config.json`. Any other MCP client
that speaks stdio takes the same command. `just mcp-serve` runs it by hand for debugging.

The two tools that change the running app are each off until opted in, separately, so
you can allow script execution without allowing restarts:

```json
"env": { "VDJ_MCP_EXECUTE": "1", "VDJ_MCP_RESTART": "1" }
```

`VDJ_MCP_HTTP_BASE` overrides `http://localhost` if the network interface is on another host.

## What a client is told

At `initialize` the server returns `instructions`, which clients hand to the model before any
tool description: the authoring workflow (`vdj_topic` → `vdj_grammar` → drill-in tools →
`vdj_lint` → `vdj_query`), the evidence rule (a verb works only on a `Pass` record or a
`vdj_query` round-trip), and what the two write tools do. The self-check fails if they name a
tool that does not exist.

Every tool also carries MCP annotations. All but three are `readOnlyHint: true`, so a client
can approve them without asking; `vdj_screenshot` writes a PNG it creates
(`destructiveHint: false`), and `vdj_execute` and `vdj_restart` change the running app
(`destructiveHint: true`). Annotations are listed per tool in `ANNOTATIONS`, with no default:
a new tool without an entry fails the self-check, so a write tool cannot inherit a read-only
label.

## Tools

Offline — these read the store and artifacts and need no running VirtualDJ:

| Tool | Wraps | Use for |
| --- | --- | --- |
| `vdj_topic` | `topic.py` | **Start here.** One term → verbs, effects, XML elements, real example files, topical docs, known quirks |
| `vdj_grammar` | `docs/VDJScript Grammar.md` | **Read before writing script.** Summary by default; `section` for detail |
| `vdj_verb` | `verb_summary.py` | Everything about one verb: record, vendor prose, usages, argument shapes, probe state, tiers |
| `vdj_get_verb` | `verbdb.py get` | The bare authoritative record; follows aliases |
| `vdj_list_verbs` | `verbdb.py search` | Find by name fragment or filter by surface/section/tier/status |
| `vdj_verb_stats` | `verbdb.py stats` | Tier and test-status breakdown |
| `vdj_get_fx` | `fxdb.py get` | Slider/button map with normalized defaults, spelling-tolerant |
| `vdj_list_fx` | `fxdb.py search` | Effects by category or control shape |
| `vdj_element` | `element_summary.py` | One XML element: usage, docs, categories, probe results; `parents`/`children` give observed nesting and sources |
| `vdj_list_xml_elements` | `xmldb.py search` | Filter by family, category, attribute, observed parent/child, or usage; nesting does not prove support |
| `vdj_list_skin_categories` | `xmldb.py categories` | Editorial category IDs and derived unique-name totals |
| `vdj_attested_tails` | `extract_attested_tails.py` | Argument tails Atomix wrote in shipped scripts, with return evidence |
| `vdj_controllers` | `controller_schema_inventory.py` | A device's control names for mapper authoring (`device`, `match`), mapper comparison (`compare`), or attributes on a definition path (`path`); shipped syntax, Tier 2 |
| `vdj_sysicons` | `sysicon_atlas.py` | Built-in icon keys by description (`search`), `cell` or `unnamed`, each with how it is known |
| `vdj_action_catalog` | `extract_action_catalog.py` | The vendor's own description and parameters, read from the app bundle |
| `vdj_lint` | `lint_{skins,pads,mappers}.py`, `lint_script.py` | Validate what you author: XML files and the script inside them, or one script string (`kind: "script"`, `content`, `context`). XML kinds take `content` in place of `paths` for an unsaved draft |

Live — these need VirtualDJ running (all but `vdj_screenshot` and `vdj_restart` need its network interface too):

| Tool | Use for |
| --- | --- |
| `vdj_up` | Reachability check; run before planning live-test work |
| `vdj_query` | **Verify script.** Read-only, safe to sweep |
| `vdj_execute` | Run an action. Opt-in and denylisted — see below |
| `vdj_restart` | Quit and relaunch the app (launch arguments allowed); `status` is read-only. Opt-in — see below |
| `vdj_screenshot` | PNG of the VirtualDJ window (macOS), saved under `tests/screenshots/` and returned as an image; cite the path as evidence |

## Two things the tool descriptions enforce

**Evidence tier travels with every answer.** Most records are catalog-tier — the vendor
named the verb — rather than locally tested; `vdj_verb_stats` gives the current split. The
descriptions tell the model to check the tier before claiming a verb works, so a retrieved
name does not become an asserted behaviour. See [Evidence Standards](Evidence%20Standards.md).

**Verification is available, so use it.** `vdj_query` is the reason this beats a document
dump: VDJScript's characteristic failure is silent — the runtime never reports a syntax
error — so a model that can round-trip a construct against a live instance is
categorically better than one that cannot. The working rule is to return nothing that has
not been either round-tripped through `vdj_query` or grounded in a `test_status=Pass`
record.

## Execute safety

`vdj_execute` writes to a running application, so it is off unless the server starts with
`VDJ_MCP_EXECUTE=1`. Even then it screens every identifier in the script — not just
statement starts, so a verb hidden in a scope wrapper (`deck 2 system …`) is caught — and
refuses destructive families: `system`, anything matching *delete* or *database*, `file_*`,
destructive `browser_*` forms, settings writes, and `timecode_cd_mode`, which can be set
from script and only a restart clears. Over-matching an argument costs a refusal, which is
the safe direction to fail. This mirrors the allowlist discipline in
`tools/probe_execute_forms.py`.

## Restart safety

`vdj_restart` (`tools/vdj_restart.py`, `just vdj-restart`) is off unless the server starts
with `VDJ_MCP_RESTART=1`. It refuses while any deck is playing — only an explicit `no` from
`deck N play` counts as stopped — and refuses when the HTTP interface is down, since playback
then cannot be checked; `allow_playing` and `force` override those. It quits through an
AppleEvent so the app saves its settings, and terminates only on `force` when that stalls.
After relaunching it waits for `get_version`; a launch that stays silent is quit and retried,
because the Network Control listener occasionally does not open — see
[HTTP Control Interface](HTTP%20Control%20Interface.md#a-relaunch-occasionally-comes-up-without-the-listener-2026-09-29).

## Checking it

`just mcp-check` drives every offline tool in-process, asserts the execute denylist refuses
its four known-bad shapes, and checks that every tool is annotated and that the
instructions name only real tools. It then starts the real server as a subprocess from a
temp directory and talks to it over stdio — initialize, tools/list, a draft lint, an unknown
tool, a malformed line, and both write tools without their opt-ins — which catches what
in-process calls cannot: a stray print on stdout, a path that resolves only from the repo
root, a framing bug. It runs inside `just check`, so a tool that stops working fails the
repo's own gate rather than failing silently in a client.

`just mcp-check --live` adds read-only calls against a running VirtualDJ — `vdj_up`,
`vdj_query` with a real and an unknown verb, `vdj_restart` status — and skips them when the
app does not answer. It never restarts or executes anything.
