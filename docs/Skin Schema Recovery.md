# Skin schema recovery

## Current result — conditional children, 2026-09-22

`just skin-schema button` now uses the
[conditional-node capture](../tests/skin-schema-button-conditional-9644.json),
on build **18.0.9644, arm64**, and separately joins the
[live fixture result](../tests/Skins/schema-condition-probe/result-9644.json).
The original structural capture below remains unchanged as the baseline.

The [guarded helper evidence](../tests/skin-node-helpers-9644.json) resolves two
previously unknown return paths. One walks the XML child vector for a matching
name whose condition passes. The other looks for a different same-name child
of the supplied parent when the current drawing node's condition fails. Exact
binary and routine hashes guard these manually interpreted models; no private
function is called. The node tracker now retains `/button/size`, `/button/pos`
and drawing-state ownership across those returns. It does not infer individual
node identity or whether every possible branch is feasible.

**Local test:** the [synthetic fixture](../tests/Skins/schema-condition-probe/README.md)
confirmed `condition="off"` selecting the alternate `<pos>`, `<size>` and `<up>`
child, with true-condition and nonsense-attribute controls as documented there.
Independent HTTP hit flags distinguish position/size, and retained screenshots
with color samples distinguish drawing selection. The results repeat after
restoring/reloading the fixture and reversing phase/row order in the same app
session. These live results do not promote the remaining structural attribute
list or establish dynamic reevaluation without reloading.

Original skin and empty/stopped decks were restored and verified, and the
installed test skin was removed. Originally unset probe variables remain zero;
absence was not restored. The fixture journal records an initially stale skin
readback and an intermediate cleanup error, followed by verified final cleanup.

The query's `live_evidence` field keeps the tested `condition` ownership separate
from the Tier 2 `owners` list. `unresolved_reads` is a measurement of the modeled
paths, not a percentage of the whole parser. XML getter families and branches
outside the recorded traversal still need recovery, even when every known read
in a particular routine has a tracked receiver.

## Original button ownership pilot — 2026-09-22, build 18.0.9644, arm64

The [capture](../tests/skin-schema-button-9644.json) is a **Tier 2 structural
pilot**, not a complete accepted XML schema. It separates possible reads from
`/button`, shared-base reads on that same node, and reads from named children.
No live skin was loaded and no skin object was inspected in that original pass.

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

The original capture left the shape helper unresolved: it can substitute another node before reading `color`, `shape`,
`border_size` and related fields. Its unresolved return path remains visible in the original capture beside
known state-node paths; the current guarded model resolves the matching-sibling case. A class-only attribute union would erase that uncertainty.

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
heap aliases, indirect calls and unmodeled getter families are not solved. Only
the explicitly guarded conditional-node helpers have return models. Helper traversal may overapproximate arguments that
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

1. Recover the remaining XML getter families (especially coordinate and color
   readers) using the now-tracked node receivers. Model additional returns only
   after their code establishes ownership; do not infer support from the reduced
   unresolved-read total.
2. Track additional XML getter families and text helpers, retaining node ownership
   and unresolved alternatives. Do not expand all callees indiscriminately.
3. Extend live discrimination to outer-versus-child attribute placement and
   coordinate precedence. The conditional-child fixture establishes selection,
   not those separate contracts. Reuse its journal and independent readbacks.
4. Add targeted plugin instrumentation only where static ownership remains
   ambiguous. Runtime node/path capture requires new code and a load-time capture
   strategy; the existing memory probe does not intercept XML reads.

For agents: use the summary first, then select `reads` or `frontier` by function,
path or literal. The full class inventory and raw disassembly are unnecessary
context for most follow-up questions. Keep the next claim scoped to its node,
build and surface; do not repeat a broad string-extraction sweep.

The conditional helpers reproduce with `tools/skin_node_helpers.py --check` in
the same capstone/numpy environment. `just check` also validates the live journal,
fixture hashes and screenshot hashes. Pixel resampling is an optional Pillow
check documented in the fixture README.
