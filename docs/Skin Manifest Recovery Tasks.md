# Skin manifest recovery: prioritized tasks

Prepared 2026-09-30. Goal: recover a build-specific manifest of skin elements,
parent–child relationships, attributes, defaults, and embedded script bindings,
then use it for useful linting and compiler development.

This is the requested implementation proposal, in priority order. Execution
status belongs in [TODO.md](../TODO.md) (tasks K1–K3); this document is not a second live queue.
The priority order does not change the repository's existing task selection.

## Starting point and boundaries

The symbol-rich 18.0.9246 arm64 experiment can parse XML, construct selected skin
objects, trace reader calls and returns, and watch whether specific values are
read. It also reaches the script parser through a button's action attribute.
[Offline XML Parser](Offline%20XML%20Parser.md) records the experiments and limits.

Reuse the existing factory analysis, reader audit, and ownership pilot in
[extract_skin_classes.py](../tools/extract_skin_classes.py),
[skin_reader_audit.py](../tools/skin_reader_audit.py), and
[skin_schema.py](../tools/skin_schema.py). They are partial evidence, not complete
schemas. Keep their existing build anchors; do not silently merge another build's
results into the 9246 manifest.

The output should be a **contextual relationship graph**, not a single tree:
elements can have multiple parents, shared readers, and conditional meanings.
Factory object tags, child configuration tags, directives, and template-defined
names need distinct roles. Null construction does not mean an unknown name, and
absence from a trace does not prove rejection.

Offline native observations and static analysis remain Tier 2 under
[Evidence Standards](Evidence%20Standards.md). Record them separately from vendor
examples and live application confirmation.

## First milestone: a useful manifest for a bounded pilot

### 1. P0 — Define the smallest manifest contract around the existing button evidence

- Represent element/context, object class where applicable, child relationships,
  attribute reader/type, defaults, conditions, and script-binding role.
- Attach build, architecture, binary hash, routine/call-site identity, fixture,
  and evidence kind to each finding. Keep defaults tied to their consumer.
- Represent unresolved calls and incomplete context coverage explicitly. Allow
  conflicting evidence without overwriting it.
- Start with the existing button captures; extend the current ownership records
  where possible rather than introducing a parallel store.

**Deliverable:** a machine-readable pilot and a validator for its contract.
**Acceptance:** it can distinguish `button → size → width` from a button-level
`width`, and can represent “unconsumed in this fixture” without claiming “unknown
everywhere.” No renderer claim comes from a constructor result alone.
**Dependency:** none beyond the existing evidence.

### 2. P0 — Recover the object factory's dispatch and fallback rules on 9246

- Map recognized object tags to constructors, aliases, and case handling.
- Identify non-object branches, platform/condition gates, custom-class lookup,
  and the default path. Preserve anything unresolved.
- Compare known objects, deliberate nonsense, and recognized child-only tags such
  as `size`; separate name recognition from object creation.

**Deliverable:** a build-pinned dispatch map with branch evidence and unresolved
fallbacks, linked to the pilot manifest.
**Acceptance:** each recovered dispatch entry has an identified code path;
“factory returned null” is never the sole reason for declaring a tag unknown.
**Dependency:** task 1.

### 3. P0 — Finish reader ownership through shared helpers for the pilot

- Follow the XML node from `CSkinButton` through `ISkinObject::load`, base readers,
  and relevant helpers. Use the existing audit's unresolved-call frontier.
- Recover the parent of each child lookup and the owner of each attribute read.
- Cover fallback-name getters, sibling iteration, direct node traversal, and
  indirect calls where encountered. Track unknown ownership rather than guessing.
- Preserve shared-reader provenance instead of copying inherited attributes into
  unrelated element records without explanation.

**Deliverable:** a contextual button reader graph and a precise remaining frontier.
**Acceptance:** fields read from `size`, button attributes, and text-state children
are assigned to their actual receivers; an unresolved helper keeps its affected
context incomplete.
**Dependencies:** tasks 1–2.

### 4. P0 — Verify pilot relationships and conversions with paired native fixtures

- Change one dimension at a time: parent, child name, attribute spelling, value,
  missing value, duplicate value, and nesting depth.
- Compare observed output objects and getter values with known and nonsense
  controls. Include condition-dependent branches identified in task 3.
- Use hardware read watches where named-call traces leave direct/inlined reads
  uncertain. Retain positive read controls and full before/after trees.
- Test whether children are iterated, selected once, flattened, or skipped;
  investigate ordering and repeated children rather than inferring cardinality
  from the presence of a getter.

**Deliverable:** reproducible paired fixtures and trace-backed manifest entries.
**Acceptance:** the manifest can explain the observed valid and typo cases, and
records exactly which construction path was exercised. No-read conclusions are
bounded to the watched values and time window.
**Dependency:** task 3.

### 5. P1 — Expose the pilot through the existing query and lint tools

- Add context-aware queries for parents, children, attributes, defaults, evidence,
  and unresolved coverage, using existing `just element`/schema tooling where
  practical. Expose the same information through the MCP query layer.
- Join vendor nesting as a separate evidence source, using
  [Skin Element Discovery](Skin%20Element%20Discovery.md); retain source locations.
- Add targeted lint diagnostics for demonstrated mistakes: misplaced fields,
  misspellings, invalid numeric conversions, duplicates, and trailing content.
- Separate strict XML diagnostics from VirtualDJ compatibility diagnostics.
  Incomplete contexts produce qualified warnings or no finding, not unsupported
  hard errors.

**Deliverable:** a usable first manifest/query surface and bounded linter pilot.
**Acceptance:** a valid pilot fixture stays clean; each negative control produces
an actionable diagnostic with its context and evidence. Corpus-only or unseen
names are not automatically rejected. Reports remain queries rather than
maintained Markdown copies of manifest data.
**Dependencies:** tasks 1–4.

## Second milestone: broader hierarchy and trustworthy context rules

### 6. P1 — Expand to representative object families and containers

- Apply the proven workflow to text, panels/containers, sliders, and selected
  complex controls, prioritizing shared helpers and real authoring needs.
- Determine which readers recursively dispatch children and which explicitly
  select named configuration children.
- Recover root-level skin metadata and directives separately from widget
  construction; add window/image dependencies only when a fixture needs them.

**Deliverable:** additional context graphs, each with its own coverage boundary.
**Acceptance:** newly covered families have discriminating fixtures and evidence;
shared attribute or child rules are reused only where the call graph supports it.
**Dependencies:** tasks 3–5.

### 7. P1 — Recover template, class, include, and condition semantics

- Locate definition registration and reference resolution; establish lookup
  scope, expansion order, overrides, substitution, and nested expansion behavior.
- Trace how platform and condition gates affect dispatch and field consumption.
- Preserve source locations through expansion so diagnostics point to authored
  XML and can explain the expansion path.
- Test a custom-defined name against an undefined name in the same context.

**Deliverable:** explicit expansion/resolution rules and contextual fixtures.
**Acceptance:** the checker can distinguish a resolvable custom name from an
unresolved reference in the tested cases. A valid template use is not rejected
merely because it is absent from the built-in factory map.
**Dependencies:** tasks 2–4; use task 6's contexts as needed.

### 8. P1 — Reconcile static candidates, native traces, and vendor nesting

- Join the sources by build, parent/context, name, and consumer rather than by
  bare tag name. Preserve literal versus expanded nesting.
- Triage differences into unexercised branches, template effects, unresolved
  helpers, version differences, or contradictory observations.
- Choose the next fixture from a concrete discrepancy. Derive coverage summaries
  from artifacts and expose them through queries.

**Deliverable:** a regenerable discrepancy report and a manifest with explicit
coverage boundaries.
**Acceptance:** every discrepancy has an evidence route or unresolved reason;
missing corpus examples and missing trace calls remain distinct from rejection.
**Dependencies:** tasks 5–7.

### 9. P1 — Confirm representative manifest rules in the running application

- Load paired fixtures on the same build as the manifest, observing geometry,
  text, script bindings, diagnostics, and relevant later state changes.
- Compare full-engine results with isolated construction, especially rules that
  depend on windows, images, templates, or global engine state.
- Preserve screenshots and exact fixture/build provenance for UI observations.
  Record disagreements without changing historical captures.

**Deliverable:** live confirmations and documented offline-versus-live limits.
**Acceptance:** each promoted behavior has direct application evidence; successful
loading or a native return value alone is insufficient.
**Dependencies:** task 4 for an early pilot; tasks 6–8 for broader confirmation.
Run this earlier whenever a proposed diagnostic would otherwise overstate evidence.

## Third milestone: compiler use and maintenance across builds

### 10. P2 — Connect the manifest to a compiler's intermediate representation

- Represent parsed XML, contextual element roles, expanded definitions, typed
  values, and script bindings with source spans and evidence-backed semantics.
- Feed representative action/query/string-expression attributes through their
  actual native consumer paths; do not assume all script surfaces compile alike.
- Differentially compare the project's interpretation with native trees,
  conversions, selected classes, and script parser outputs.

**Deliverable:** an inspectable intermediate representation and differential
fixtures for the supported subset.
**Acceptance:** supported examples explain their lowering and defaults;
unsupported constructs are explicit. This does not claim a vendor-compatible
serialized skin binary format unless one is separately discovered and verified.
**Dependencies:** tasks 5, 7, and the relevant confirmations from task 9.

### 11. P2 — Establish cross-build mapping and regression checks

- Map recovered routines onto a newer build using guarded structural evidence;
  validate reader ABI/layout assumptions before calling them.
- Re-run the paired fixtures and classify changes in names, context rules,
  conversions, and diagnostics.
- Keep per-build artifacts and provenance. Add saved-evidence checks to normal
  CI; keep vendor execution/debugger runs explicitly invoked.

**Deliverable:** a version-difference report and repeatable update procedure.
**Acceptance:** an unmapped or changed routine stops its dependent extraction
instead of silently inheriting 9246 semantics. Historical results remain intact.
**Dependencies:** tasks 4–5; broaden with each additional covered family.

### 12. P2 — Enable strict validation only for contexts with demonstrated coverage

- Define a completion gate for each context: dispatch/fallbacks, shared helpers,
  condition branches, templates, and relevant direct reads must be accounted for.
- Test the gate against known-valid fixtures and adversarial negatives. Check
  required fields, child multiplicity, and order only where separately established.
- Keep incomplete contexts permissive and show users the build/coverage scope.

**Deliverable:** an opt-in strict mode for explicitly covered contexts.
**Acceptance:** “unknown here” errors have a demonstrated recognition boundary;
there is no blanket closed-world rejection based on the union of observed names.
**Dependencies:** tasks 7–9 and task 11 for every additional supported build.

## Recommended stopping point for the first delivery

Complete tasks 1–5 for the button pilot. That yields something useful for authors:
a queryable contextual manifest and evidence-backed diagnostics. Then expand by
shared reader and concrete discrepancies, while confirming behavior in the live
application. Full skin coverage is not a prerequisite for shipping that bounded
first result.
