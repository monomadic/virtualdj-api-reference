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

Claude Code (`.mcp.json` in the repo root, or `~/.claude.json` for a user-level entry):

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

To allow writes to a live instance, add the opt-in:

```json
"env": { "VDJ_MCP_EXECUTE": "1" }
```

`VDJ_MCP_HTTP_BASE` overrides `http://localhost` if the network interface is on another host.

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
| `vdj_element` | `element_summary.py` | One skin/pad XML element: usage, docs, probe results, unexplained attributes |
| `vdj_list_xml_elements` | `xmldb.py search` | The element inventory, filtered |
| `vdj_attested_tails` | `extract_attested_tails.py` | Argument tails Atomix wrote in shipped scripts, with return evidence |
| `vdj_action_catalog` | `extract_action_catalog.py` | The vendor's own description and parameters, read from the app bundle |
| `vdj_lint` | `lint_{skins,pads,mappers}.py` | Validate authored XML before handing it back |

Live — these need VirtualDJ running with the network interface enabled:

| Tool | Use for |
| --- | --- |
| `vdj_up` | Reachability check; run before planning live-test work |
| `vdj_query` | **Verify script.** Read-only, safe to sweep |
| `vdj_execute` | Run an action. Opt-in and denylisted — see below |

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

## Checking it

`just mcp-check` drives every offline tool in-process and asserts the execute denylist
refuses its four known-bad shapes. It runs as the first step of `just check`, so a tool
that stops working fails the repo's own gate rather than failing silently in a client.
