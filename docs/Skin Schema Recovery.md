# Skin schema recovery

## Breadth-first structure — 2026-09-23, build 18.0.9246, arm64

The active S6 plan now inventories element structure before finishing descendant
behavior. [The broad capture](../tests/skin-structure-9246.json) separates element
identities from canonical reader definitions. Aliases reference the same reader
record: `panel`, `group` and `pannel` share a constructor; `text` and `textzone`
retain the same conditional constructor variants. That is structural reuse, not
proof of identical runtime behavior.

```sh
just skin-structure
just skin-structure button
just skin-structure panel
just skin-structure text
```

Each query projects own-attribute candidates and direct child identities from
the constructor and shared base. The parameterized button text-child helper is
defined once, with caller-specific name bindings. Descendant reads remain in
reader records and are not merged into the outer element's attributes. Parent
and child examples from vendor XML are separately labelled observations, not a
complete accepted nesting schema. `parent_source_matches_capture` reports
whether the queried vendor relations still match the extraction's source hash.

Entries distinguish factory elements, reader-discovered child identities and
observed-only XML identities. A tag with no recovered attributes is unknown,
not attribute-free. The factory binding for `edit`/`search` uses x2 as established
by its named signature and the factory's forwarding; `window` has a no-argument
constructor and its separate initialization remains explicitly unresolved.
Other helpers, templates and lifecycle routes remain recorded gaps. This first
pass marks factory entries `partial_structure`; it is not a strict validator.

**Context model:** a reader's node role identifies which argument is the XML
node being read. Other arguments, defaults, inherited state and caller event
handling can still differ. A nested tag name alone does not select the same
reader as its factory entry. For example, the text child of a button is a
separate binding route from the general factory's text/textzone variants. An
enclosing panel may contribute state without changing the button's reader
definition; contextual behavior must be demonstrated, not inferred from the
shared definition. No runtime-equivalence claim is made for panel/button/text.

A structurally complete parent entry requires its own attributes and direct
children to be accounted for, plus explicit parent scope and remaining gaps.
Its children's internal behavior can remain unverified. Detailed rendering
results remain a separate layer, with shared facts referenced once and proven
context differences recorded where they occur.

Reproduce with fresh factory discovery and the pinned live-image anchors:

```sh
uv run --with capstone --with numpy --python .venv/bin/python3 \
  python tools/skin_structure.py --check \
  --app '/Users/nom/src/virtualdj-api-reference-resources/unpacked/9246/vdj.pkg/Payload/VirtualDJ.app'
```

Use `--output NEW_PATH` for a new capture. Queries require only stdlib; extraction
also requires the disassembly dependencies. The text/geometry and earlier button
captures below remain dated evidence, not the active breadth-first sequence.

## Text candidate review — 2026-09-23, build 18.0.9246, arm64

[The focused review](../tests/skin-text-attribute-review-9246.json) checks the
newly tracked `CTextObject` reads against their actual getter calls, the existing
reference, and the local built-in skin subset. These are **new to this ownership
analysis**, not collectively new VirtualDJ capabilities. `align`, `valign`,
`format`, `width` and `multiline` already appear in the Skin SDK text-attribute
section. Built-in XML also attests ordinary offsets and state colors. The review
retains source hashes and representative token locations; an empty example list
means no match in this subset, not unsupported behavior.

The most useful remaining live-test candidates from this group are `height`,
`scroll`, `overdx`/`overdy`, `downdx`/`downdy`, and `backcolor`. Their names reach
the text reader; this review does not establish rendering effects, units,
scrolling rules, clipping, precedence or dynamic reevaluation.

**Extraction omission:** the hover-color call at `0x1006a95ec` supplies
`overcolor` in x1 and `colorover` in x3 to `getParam2`. The inspected getter accepts
either key while scanning the attribute list. The first-key-only schema capture
therefore omits `colorover`; it must not be treated as a complete color vocabulary.
This structural observation does not establish live precedence when both are set.
The shipped examples in this review use `colorover`.

The nested `/button/text/font` route is also present: the enclosing reader
selects a `font` child and passes it to `CTextObject`, with an outer-text fallback
route. This does not assign these attributes to the skin's global `<font>`
definition. Text-state and nested-font placement remain separate live questions.
No new rendering fixture was run for this review; all newly recorded evidence
here is Tier 2.

## Text, geometry and conditions — 2026-09-23, build 18.0.9246, arm64

[This capture](../tests/skin-schema-button-text-geometry-9246.json) extends the
color checkpoint through `getRectangle`, `checkCondition` and the `CTextObject`
constructor. [The follow manifest](../tests/skin-follow-readers-9246.json) pins
their binary/routine hashes, reviewed XML argument registers and depth limit.
Only the named readers gain this traversal; the default older captures remain
reproducible. Conditional register selections in these readers preserve both
alternatives, including unknowns. Unused node-looking argument registers are
removed when entering an explicitly reviewed reader.

The text-state and nested font paths gain possible reads for alignment,
formatting, scrolling, dimensions, offsets and state colors. Drawing states
gain condition reads. These remain **Tier 2 possible paths**, not a guarantee
that each attribute affects rendering in every listed location. The geometry
reader can use the supplied node or its nested `size` child; the analyzer retains
those alternatives and unresolved receiver paths rather than claiming exclusive
ownership. Broadening the traversal exposes more unresolved reads and does not
establish a completeness percentage.

Query with `just skin-schema button --capture
tests/skin-schema-button-text-geometry-9246.json`. Reproduce using the historical
expanded command below, with this `--capture`, the color manifest, and
`--follow-manifest tests/skin-follow-readers-9246.json`. The artifact's
`follow_models`, `reads`, `frontier` and `limits` retain the exact scope.

[The refreshed frontier review](../tests/skin-schema-button-text-geometry-frontier-9246.json)
retains localization/template routes and remaining image/color-action contexts.
It also exposes the `CFont` constructor: its absence of direct XML getter calls
does not close that route, because deeper and tail calls are outside the direct
call count. Next, inspect font delegation and template/localization handling;
keep the geometry ambiguities and lifecycle coverage separate from that work.
No live skin state changed and no 9644 live result is attributed to 9246.

## Icon color keys and frontier review — 2026-09-22, build 18.0.9246, arm64

[The color capture](../tests/skin-schema-button-color-9246.json) resolves the
previously unnamed color-helper reads on `/button/icon`. It uses
[guarded call-site evidence](../tests/skin-color-helpers-9246.json): the button
constructs a temporary C++ string at SP, passes the same object straight to the
color helper, and that helper forwards its contents as an XML key. Exact caller,
string-constructor and color-helper hashes guard the model. This does not add
general stack/heap tracking or change the older extraction defaults.

The additional possible keys include `colordown`, `colorover`, `colorselected`
and `coloroverselected`. Conditional selections retain both possible names;
branch feasibility, fallback precedence and rendering behavior are not proven.
The literal `dontfindme` is retained in `internal_fallback_literals` as an
internal fallback and excluded from the reported attributes. All findings here
are Tier 2, and the previous expanded capture remains immutable.

Query this checkpoint with `just skin-schema button --capture
tests/skin-schema-button-color-9246.json`. Reproduce it using the expanded
historical command below, changing `--capture` to this file and adding
`--color-manifest tests/skin-color-helpers-9246.json`. The color evidence itself
reproduces with `tools/skin_color_helpers.py --check --app HISTORICAL_APP` in the
same capstone/numpy environment.

[The frontier review](../tests/skin-schema-button-frontier-9246.json) groups the
remaining incoming call contexts by target and retains named direct XML calls.
It identifies localization, template application, rectangle/image readers,
color-action readers and `CTextObject` as further investigation routes. Calls
without direct XML reads remain visible: unused argument-register contents can
produce an incoming node association, while indirect/deeper reads can escape
this direct-call search. Neither case permits silently closing a route.

Reproduce the review with `tools/skin_schema_frontier.py
tests/skin-schema-button-color-9246.json --app HISTORICAL_APP --check
tests/skin-schema-button-frontier-9246.json` using the project interpreter.
The later text/geometry checkpoint above follows the shared geometry/condition
reads and `CTextObject` constructor. Template/localization analysis remains open.
Zero unresolved names inside this traversal would still not mean complete XML
coverage; the review and lifecycle gaps remain separate.

## Expanded historical ownership — 2026-09-22, build 18.0.9246, arm64

[The expanded capture](../tests/skin-schema-button-expanded-9246.json) replaces
the constructor-only assumption with a verified structural binding: the factory
at `0x10036abcc` forwards its XML receiver through the button branch to constructor
`0x1004cb21c`. The capture retains dispatch, forwarding instructions and routine
hashes. The earlier named-reader audit stays unchanged as its baseline.

[Historical conditional-node evidence](../tests/skin-node-helpers-9246.json)
separately records the named-child and matching-sibling selectors, their condition
predicate and comparison helpers. Manual inspection of the historical instructions
establishes the same possible non-null path models, guarded by this binary and
these routines' hashes. The 9644 live fixture is **not** evidence of behavior on
9246; the historical query intentionally reports no joined live evidence.

The analyzer now accepts explicit build-matching node models and a named-reader
audit. It rejects mismatched images and changed reader code, preserves the older
anchor-calibrated roles, and adds first-key reads from the remaining named XML
getter families. This resolves additional position, size and signed-number read
paths without treating getter names as a complete behavioral/type contract.
Fallback names and additional getter arguments remain outside that model.

Queries:

```sh
just skin-schema button --capture tests/skin-schema-button-expanded-9246.json
just skin-schema button --capture tests/skin-schema-button-expanded-9246.json --format=json
```

Reproduce with fresh factory discovery (no cached structural input):

```sh
uv run --with capstone --with numpy --python .venv/bin/python3 \
  python tools/skin_schema.py --check \
  --capture tests/skin-schema-button-expanded-9246.json \
  --app '/Users/nom/src/virtualdj-api-reference-resources/unpacked/9246/vdj.pkg/Payload/VirtualDJ.app' \
  --memory-capture tests/plugin-memory-9246.json \
  --node-manifest tests/skin-node-helpers-9246.json \
  --reader-audit tests/skin-reader-audit-9246.json
```

The helper evidence independently reproduces through `tools/skin_node_helpers.py
--check` with the same `--app` and `--memory-capture`, plus `--manifest
tests/skin-node-helpers-9246.json`. The original default 9644 extraction remains
unchanged. No private functions are called by either extraction.

This expanded checkpoint left an unresolved first-key name in `ISkinObject::getColorParam` at
`0x10036aa94` arrives as a C++ string object, so the literal-pointer tracker cannot
recover it. The later color-key checkpoint above addresses that gap. The capture's `frontier`
still contains node-carrying calls outside scope, and lifecycle, template and
indirect routes remain open. This is not a closed button schema.

## Named-reader audit — 2026-09-22, build 18.0.9246, arm64

The active execution plan and resumption checkpoint are task **S6** in
[TASKS.md](../TASKS.md). The objective remains element/attribute vocabulary and
node ownership; runtime-access setup is complete. Historical and current-build
evidence stay separate.

[The named-reader audit](../tests/skin-reader-audit-9246.json) binds symbol names,
routine hashes and direct skin call sites to the verified historical executable.
It also applies the existing node tracker to the named XML button constructor,
with its single-branch constructor alias explicitly retained. This is **Tier 2**.
The constructor signature and arm64 ABI supply the initial node argument;
this pass does not independently re-prove the factory's forwarding on 9246.

Use `just skin-reader-audit getSigned` or `just skin-reader-audit getColor` for
focused routine summaries. `just skin-reader-audit --button` returns the
constructor's candidate reads and the node-carrying helper frontier as JSON.
The source artifact retains methods with no observed direct skin calls too:
zero is a limit of this call-site search, not an unused-reader verdict.

The named signed-number reader is called with `value` and `rightclick` on the
constructor's input node. Do not infer that every signed-number reader handles
coordinates. Shared load, color and text routes remain outside this bounded
constructor traversal. The audit tracks only the first name argument, so
multi-name/fallback readers require separate work. It establishes neither
runtime support nor a closed button schema.

Reproduce with the exact historical app location (queries need only stdlib;
extraction needs numpy, capstone and the system symbol tools):

```sh
uv run --with capstone --with numpy --python .venv/bin/python3 \
  python tools/skin_reader_audit.py --check \
  --app '/Users/nom/src/virtualdj-api-reference-resources/unpacked/9246/vdj.pkg/Payload/VirtualDJ.app'
```

For a new extraction use `--output NEW_PATH`; existing files are rejected.
For agents inspecting this baseline, use `button_constructor.frontier` and the named
reader signatures; use S6 for the current resumption point. Do not rerun the memory-access experiment or treat the
9644 conditional-node guard as applicable to 9246.

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

## Attribute value records and generated tables

[skin-attribute-contracts.json](skin-attribute-contracts.json) is the editable
source for attribute value descriptions. Shared value types describe syntax or
known enum members; definitions attach meaning, context, evidence, build and
verification status; element mappings reference those definitions. Aliases reuse
a definition. Distinct meanings, such as button and text `action`, stay separate.

Run `just skin-attributes text` (or another tag) for an **Attribute | Value |
Description** Markdown table on stdout; `--format=json` retains the full metadata.
`just build-reference` embeds the same rows in the skin section of the human
reference through `design/human-api-reference.template.html`. These tables are
artifacts of the records: edit the source records, not the rendered table.

The initial records cover reviewed text fields and button action/query fields.
Other inventoried attributes remain visible with **Unknown** values. A null
accepted-value set, default or constraint means **not recorded**, never that any
value is accepted. Integer/boolean getter evidence does not establish numeric
ranges, units, or every accepted spelling. Documentation summaries and static
reader candidates remain Tier 2; neither is live behavior verification.

Element mappings are lookup aids, not a closed schema or a promise that every
parent context behaves identically. The reviewed text routes share definitions;
the global `font` element and unreviewed routes do not inherit them. Context and
evidence remain available in the JSON and expandable table details. Keep reader
identity and parent/child structure in `just skin-structure`; add a distinct
attribute definition when evidence establishes a context-specific difference.

Next value work should add exact constraints and defaults only with cited
parser evidence or discriminating live fixtures, preserving their build and
node role. Continue breadth-first structural discovery independently of those
behavior checks.
