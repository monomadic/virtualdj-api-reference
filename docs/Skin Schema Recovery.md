# Skin schema recovery

## Button ownership pilot — 2026-09-22, build 18.0.9644, arm64

The [capture](../tests/skin-schema-button-9644.json) is a **Tier 2 structural
pilot**, not a complete accepted XML schema. It separates possible reads from
`/button`, shared-base reads on that same node, and reads from named children.
No live skin was loaded and no skin object was inspected in this pass.

Start with `just skin-schema button`; add `--format=json` for a structured
summary. `just element button` and its MCP twin point here. `owners` contains
tracked read paths and separately labelled partial/ambiguous attributes;
`shared_outer_attributes` identifies reads in the common base routine. Query
`unresolved_reads` and `frontier_calls` for the remaining measured gaps. The
capture's `reads` retain each getter, call site, enclosing routine, origin,
possible XML paths and uncertainty flags. Do not copy that list into prose.

## What the pilot establishes

The current factory's button branch forwards its XML receiver to constructor
argument `x1`, through a single branch thunk. The target installs the
`CSkinButton` vtable. The capture retains the forwarding instructions and the
existing extractor's constructor/vtable evidence.

Tracking that input through XML getter calls distinguishes reads that the old
class-level list merged together. Examples on this build:

- `action`, `query` and mouse-action strings have reads on `/button`.
- `clickthrough` and `visibility` have reads on `/button` in the shared base reader.
- `sysicon`, `dx`, `dy`, `downx` and `downy` have reads on `/button/icon`.
- `r` has a read on `/button/mousecircle`; `width` and `height` have reads on
  `/button/mouserect`.
- Text-state helper calls preserve `/button/text`, `/button/textover`,
  `/button/textdown` and `/button/textselected` receivers, including nested
  `font` reads. This is not a claim that these exhaust the text-state vocabulary.

These are positive structural paths, **not exclusive ownership or behavior
claims**. In particular, the icon result does not disprove a direct button
`sysicon` form elsewhere, or template forwarding of that name.

The shape helper can substitute another node before reading `color`, `shape`,
`border_size` and related fields. Its unresolved return path stays visible beside
known state-node paths. A class-only attribute union would erase that uncertainty.

## Relationship to the memory probe

The extractor re-verifies [the existing memory capture](../tests/plugin-memory-9644.json)
against the current disk image: UUID, build, verb table location and records.
It binds the new analysis to that verified binary hash. **This reuses the plugin's
image identity, not a fresh runtime observation of the skin parser.** Function
bounds come from `LC_FUNCTION_STARTS`; analyzed routines carry code hashes.
No private function was called, hook installed or application state changed.

The [general class extractor](../tools/extract_skin_classes.py) now supports
current-image generation without the historical app bundle. Optional historical
matching remains available. Generation writes stdout or a new `--output` path;
it no longer silently overwrites the historical main/debug artifacts. A diagnostic
capture requires an explicit new `--debug-output` path. This pass retains the
older build-9598 artifacts unchanged.

## Method and limits

[The ownership analyzer](../tools/skin_schema.py) propagates possible node paths
through ARM64 register copies and control-flow joins. Known child getters extend
the path; ordinary calls invalidate caller-saved registers and unknown returns.
Unmodeled instructions invalidate their written registers. Unknown alternatives
survive joins; excessive alternatives widen to an unresolved value.

Traversal covers direct constructor callees, then selectively follows named
text-state child receivers to the depth in `limits`. It is not a global call-graph
sweep. Both branch edges are explored without proving feasibility. Stack spills,
heap aliases, indirect calls, unmodeled getter families and conditional-node
replacement are not solved. Helper traversal may overapproximate arguments that
the callee ignores. `frontier` records node-carrying calls left outside scope,
including literal arguments to help choose the next bounded target.

An absent attribute means unknown. Template parameters remain open. This artifact
must not be used as a strict linter allowlist or labelled an XSD.

## Reproduction and checks

Read-only queries need only the project's usual interpreter:

```sh
just skin-schema button
just skin-schema button --format=json
just check-skin-schema
```

Extraction additionally needs capstone and numpy. It must run against the image
matching the memory capture; a mismatch aborts. Run `just doctor` first.

```sh
uv run --with capstone --with numpy --python .venv/bin/python3 \
  python tools/skin_schema.py --check
uv run --with capstone --with numpy --python .venv/bin/python3 \
  python tools/skin_schema.py --extract --output /tmp/skin-schema-new.json
```

`--check` freshly regenerates structural discovery and ownership and compares
every retained field. `--output` refuses an existing file. An optional
`--structural-capture` avoids repeating general discovery during local iteration;
the binary hash must match. Final verification should omit that shortcut.
Regression tests cover ambiguous joins, call clobbers, unknown helper returns,
child-path propagation, narrow writes, unreachable instructions and the recorded
outer-versus-child distinction. Ordinary `just check` runs these without optional
disassembly dependencies.

## Next bounded work

1. Resolve the conditional-node lookup/replacement helpers in the frontier. The
   common reader's size/position routes and shape-state alternatives are the
   highest-value gaps; their code and exact call sites are already located.
2. Track additional XML getter families and text helpers, retaining node ownership
   and unresolved alternatives. Do not expand all callees indiscriminately.
3. Prepare a minimal live button fixture with a known form, the same attribute on
   the competing node, and a nonsense control. Independent visual or interaction
   readback must distinguish the forms before promoting behavior.
4. Add targeted plugin instrumentation only where static ownership remains
   ambiguous. Runtime node/path capture requires new code and a load-time capture
   strategy; the existing memory probe does not intercept XML reads.

For agents: use the summary first, then select `reads` or `frontier` by function,
path or literal. The full class inventory and raw disassembly are unnecessary
context for most follow-up questions. Keep the next claim scoped to its node,
build and surface; do not repeat a broad string-extraction sweep.
