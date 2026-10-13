# Verb-tail analysis and linter: prioritized tasks

Prepared 2026-09-30. Goals: recover which arguments each verb reads, recognizes,
converts, ignores or rejects, and use that evidence to build a useful VDJScript
linter.

This is a prioritized implementation proposal, not a second live queue.
[TODO.md](../TODO.md) is the operational queue (its task V2 uses A1–A4 as its method); the
priorities here do not change its selection order. The previous owners, now in
[RETIRED.md](../RETIRED.md), were task 10 (verb contracts), 10a
(native introspection), 10b (prepared-state probes), 12 (vendor tails), and 13/13b
(enumerations and argument fixtures). The frozen consolidation and completeness
plans remain unchanged.

## Starting point

- The [offline parser host](Offline%20Parser%20Host.md) works for a fixed suite on
  symbol-rich build 18.0.9246 arm64 and build 18.0.9644 arm64. It inspects argument
  tags and payloads without evaluating actions. Its 9246 comparison uses a 9644
  live baseline; it is not a same-build live validation or an arbitrary-script API.
- [Named consumer analysis](Runtime%20Memory%20Probe.md#shared-time-consumer--2026-09-23-build-1809246-arm64)
  already associates candidate keywords with argument positions and follows a
  shared time reader. Output-parameter tracking, prefix suffixes, and unresolved
  receivers remain concrete gaps.
- [The script linter](../tools/lint_script.py) already checks names and known
  grammar traps. Extend it incrementally; a complete replacement is not a
  prerequisite for useful argument diagnostics.
- Existing live fixtures measure argument types, statement branches, return
  values and consumer behavior. Start from those captures and their checkers
  rather than repeating broad, unprepared sweeps.

**Working distinction:** parsing, keyword recognition, conversion, and behavioral
effect are separate questions. Nonsense can survive as a text parameter; an
accepted argument can have no visible effect in the current state. An HRESULT,
empty string, zero, or unchanged value is not a universal validity verdict.

Offline execution and structural analysis remain separate from live behavior
confirmation under [Evidence Standards](Evidence%20Standards.md). Keep build,
architecture, surface, fixture, and evidence kind attached to every finding.

## Proposed order

P0 establishes a small end-to-end result. P1 makes it dependable and broadly
useful. P2 expands coverage and authoring surfaces after the core is sound.

| Order | Priority | Task | Depends on | Main work channel |
| --- | --- | --- | --- | --- |
| A1 | P0 | Freeze a representative argument corpus | Existing evidence | Desk |
| A2 | P0 | Finish position-aware consumer recovery for the pilot | A1 | Named 9246 code |
| A3 | P0 | Expand typed parser inspection within a bounded allowlist | A1 | Offline native host |
| A4 | P0 | Trace recognition, fallback and ignored-tail paths | A2, A3 | Isolated native instrumentation |
| A5 | P0 | Calibrate the candidate contracts against live behavior | A1; then A2–A4 findings | Prepared live fixtures |
| L1 | P0 | Ship a small set of evidence-backed argument diagnostics | Relevant A5 results | Existing linter |
| L2 | P1 | Add a source-preserving syntax tree | A3; existing grammar evidence | Independent parser |
| L3 | P1 | Model consumer-specific types and conversions | A2, A5, L2 | Contract queries and linter |
| L4 | P1 | Establish differential and diagnostic regression gates | Starts at A1; expands through L3 | Offline tests plus scoped live checks |
| A6 | P2 | Scale extraction by shared consumer families | A2–A5, L1 | Named code and targeted fixtures |
| L5 | P2 | Resolve embedded-script context and template boundaries | L2–L4 | XML extraction and skin work |
| L6 | P2 | Package stable diagnostics for CLI, MCP and editors | L1, L4; richer output after L2 | Tool integration |

A2 and A3 are independent investigations after A1. A5 can reuse established live
facts immediately; it need not wait for every tracing capability. L1 should ship
as soon as a bounded rule is supported. Full language recovery is not its gate.

## First milestone: explain a tail and lint it correctly

### A1. Freeze a representative argument corpus and explicit predictions

Use `just verb NAME`, `just attested-tails --verb NAME`, and existing capture
queries to choose contrasting cases. Start with `is_using`, `filter_label`,
`get_song_event`, and the shared `get_time` family: they already have useful
position, recognition or delegation evidence.

Cover omitted arguments, known tokens, independent nonsense controls, quoted
forms, misplaced tokens, extra trailing arguments, numeric values and units.
Separate open-ended text, numbers, prefix families and enumerations. Preserve
counterexamples where a successful parse or evaluation result is misleading.

**Deliverable:** a small machine-readable case manifest referencing existing
evidence, with expected parse and consumer outcomes kept separate.
**Acceptance:** every case states what observation would distinguish recognition
from fallback and what state is needed. Unknown predictions are explicit. No
new universal contract schema is required before the pilot exposes a real gap.
**Reuse:** [parser_objects.py](../tools/parser_objects.py),
[probe_argument_types.py](../tools/probe_argument_types.py),
[probe_statement_branches.py](../tools/probe_statement_branches.py).

### A2. Finish argument provenance through the pilot consumers

Extend [tail_consumers.py](../tools/tail_consumers.py) through the demonstrated
gaps: the shared time reader's output parameter, conditional selection of that
parameter, and the `cue` prefix's suffix conversion. Recover where `short` comes
from before assigning it a position. For each comparison, retain its argument
index, comparison kind, applicable branch, shared helper and unresolved paths.

**Deliverable:** a bounded, build-pinned consumer graph with position-aware
candidate tails and conversion routes.
**Acceptance:** output/localization strings cannot enter a keyword list without
input provenance; prefix comparisons cannot become exact-token enumerations;
shared helpers are attached only to verified callers. Unexpanded edges remain
visible. An absent comparison never means the argument is forbidden.
**Fallback:** if general alias tracking becomes expensive, model the specific
reviewed helper and keep its code hash guard rather than rebuild the extractor.

### A3. Expand typed parser inspection without requiring evaluation

Extend the 9246 host through reviewed fixtures, first within understood action
classes. Inspect omitted, quoted, signed, unit-bearing and extra operands. Add
compound classes only after checking their object layouts and destruction paths.
Investigate the parser's end-pointer output before using it as a consumed-source
boundary; neither its name nor one returned pointer proves span semantics.

**Deliverable:** normalized object/parameter captures with raw tags preserved,
build-specific guards, bounded traversal and explicit unsupported cases.
**Acceptance:** recognized and nonsense text can both be represented without a
validity label. Successful cleanup is recorded; unknown classes stop inspection
without guessed dereferences or destructors. Nested objects have depth, node and
cycle limits. Numeric payloads are decoded according to their tags.
**Reuse:** [prepare_symbol_parser.py](../tools/prepare_symbol_parser.py),
[offline_parser.py](../tools/offline_parser.py), and the existing fixed-suite gates.

### A4. Distinguish recognition from fallback using consumer traces

For the pilot, instrument a small set of named comparisons and fallback branches.
Compare known, nonsense, omitted and wrong-position arguments. Record which
parameter reaches which comparison, its result, and the selected branch. Where
an argument is never read in a fixture, report that observation rather than
declaring it universally ignored.

Parsing a script does not run its consumer. Before calling a query method in an
offline worker, establish its ABI, required state and cleanup; some methods need
decks, settings or other initialized services. Use the existing native plugin in
a prepared app instance when the offline boundary cannot supply that context.

**Deliverable:** paired traces linking candidate recognition and fallback to
specific inputs and code locations.
**Acceptance:** a differing return value alone is insufficient; the trace must
support the claimed path. An unavailable service or uninitialized object is an
environment limitation, not an invalid argument. Preserve sandboxing, deadlines,
and explicit call allowlists. Do not bulk-evaluate arbitrary verbs.

### A5. Calibrate against live fixtures and record scoped contracts

Use same-build 9246 live comparisons where practical to distinguish host setup
differences from parser differences. Test selected cases on the installed build
separately. Reuse discriminating states for time, track events and settings;
unloaded or zero-valued state is often inadequate. Retain numeric/text returns,
HRESULT, independent behavioral readbacks and restoration where writes occur.

**Deliverable:** linked observations for parsed representation, recognition,
conversion and effect, with conflicts and nondiscriminating cases retained.
**Acceptance:** no cross-build result is relabeled as same-build evidence; no
error code becomes a universal invalid-tail rule. Confirmed ignored/rejected
forms have the requisite controls and stated scope. Drift-sensitive cases have
independent confirmation.
**Recording:** use `just put-verb` for settled per-verb conclusions and the tracker
for run narratives. If existing records cannot express a demonstrated contract,
make the smallest API-backed extension under task 0/10; do not hand-edit private
store layout or create a Markdown copy of its contents.

### L1. Ship the first argument-aware lint rules

Consume the pilot's established contracts through the existing query layer.
Candidate rules include a keyword in a proven wrong position, a missing required
operand, a recognized unit that a particular consumer mishandles, and an extra
argument demonstrated to be ignored. These are proposed rule families, not
findings that every pilot verb has these defects.

**Deliverable:** a small patch to the existing linter, with rule IDs, evidence
references, affected build/surface and actionable messages.
**Acceptance:** every diagnostic has a failing example and a nearby valid
counterexample. Hard errors require a supported invalidity claim; silent
fallback or ignored-input traps are normally warnings. Unresolved forms remain
unknown, and recommendations are distinguished from language restrictions.
Do not reject a token solely because it is absent from a candidate list.

**Milestone demonstration:** explain one verb's argument positions and observed
handling through a query, then lint a supported mistake and accept its corrected
form. Achieve this before expanding to the entire verb set.

## Second milestone: a dependable language front end

### L2. Build a syntax tree that preserves the user's source

Extend or refactor the tokenizer into an independent syntax tree for statements,
chains, conditionals, scope wrappers, quoted text and nested expressions. Preserve
raw spelling, normalized meaning and source spans separately. Test behavior
against the existing grammar cases and native object captures where available;
the Button Editor's tree is a separate comparison surface.

**Deliverable:** a parser usable by the linter, with error recovery and explicit
unsupported constructs. This can later serve a compiler front end.
**Acceptance:** precedence, branch ownership, quoting and scope are covered by
contrasting fixtures; incomplete input produces bounded diagnostics. Span tests
cover Unicode and map correctly to the original source. A source span is not
invented from an object that retains no position information.

### L3. Add a consumer-specific type and conversion layer

Keep lexical spelling, native parameter tag, consumer conversion, result type,
and boolean interpretation distinct. Record per-position alternatives and
conditional forms. Fixed keywords, arbitrary strings, numbers, unit-bearing
values, prefixes and deferred expressions need different constraints.

**Deliverable:** a minimal contract view that the syntax-tree linter can query,
reusing the current store and typed-result artifacts.
**Acceptance:** percentage normalization does not imply every consumer accepts
percentages; a numeric query does not automatically become a boolean predicate;
dynamic values are not declared invalid because they cannot be resolved
statically. Suggestions name the applicable consumer and evidence.

### L4. Gate parser compatibility and diagnostic quality

Start the regression corpus during A1. Keep independent native observations,
live behavioral fixtures, and linter expectations separate so tests do not
merely restate the implementation. Include supported constructs, known traps,
malformed input and intentionally unresolved forms. Minimize disagreements into
small reproductions and retain them as regression cases.

**Deliverable:** offline checks for contracts, parse structure, spans, diagnostic
severity and build isolation, integrated with `just check`.
**Acceptance:** known-valid fixtures cannot acquire unexplained hard errors;
unknown forms cannot silently become confirmed rules; changed binaries fail
closed before private calls. Run corpus comparisons against shipped scripts,
but keep their status as attested usage rather than universal runtime proof.
Fuzz the independent parser first; native fuzzing is a later, separately bounded
experiment after ownership and isolation are proven.

## Expansion after the pilot

### A6. Scale by shared consumer family and measured usefulness

Rank the next families by real usage, existing evidence and reuse of already
understood helpers. Extend position-aware comparisons and conversions rather
than accumulating nearby strings. Handle open vocabularies such as effect names,
settings names and resource identifiers through the appropriate catalogs and
context; do not freeze them as generic keyword enums.

**Deliverable:** incremental family coverage, queried from regenerable artifacts.
**Acceptance:** each family adds usable constraints or closes a named uncertainty;
unresolved indirect calls remain visible. Hardware/state-dependent families can
remain named gaps. A claim to have found every possible overload is not the gate.

### L5. Preserve context when linting scripts embedded in XML

Coordinate with [Skin Manifest Recovery Tasks](Skin%20Manifest%20Recovery%20Tasks.md).
Carry the embedding role into linting: action, query, visibility, text/color
expression, pad body or mapper binding. Preserve XML entity decoding and map
diagnostics back to the original file. Resolve known template substitutions;
keep unknown placeholders symbolic instead of reporting them as nonexistent verbs.

**Deliverable:** context-aware XML-to-script extraction feeding the same linter.
**Acceptance:** equivalent standalone and embedded fixtures agree after known
transformations, while demonstrated surface differences remain explicit. Script
linting does not claim that a skin renders correctly or validate undocumented
skin relationships. Reuse the current XML tooling instead of treating strict
standard XML parsing as VirtualDJ compatibility.

### L6. Expose stable diagnostics to authoring tools

Extend `just lint-script` and its existing MCP counterpart with structured
diagnostics, spans, rule IDs, evidence, build/surface selection and conservative
suggestions. Editor integration can follow once that output is stable.

**Deliverable:** the same diagnostics in CLI and MCP, suitable for CI and editors.
**Acceptance:** normal linting works without loading vendor code or running
VirtualDJ. Native hosts remain optional development/comparison instruments.
Automatic edits are limited to transformations with demonstrated preservation of
meaning; ambiguous corrections remain suggestions.

## Suggested first work package

Begin with A1 and the shared-reader gap in A2, while expanding A3 only as required
to answer those cases. Use A4 when equal outputs conceal recognition, then A5 to
settle scoped conclusions and L1 to deliver the first useful diagnostics.

Defer a standalone VDJScript runtime, private compiled-output format, exhaustive
keyword enumeration and broad native fuzzing. None is necessary for the argument
analysis or linter goals. The independent syntax tree and contract queries leave
a path toward later compilation to validated VDJScript/XML without making that a
prerequisite for the first useful release.
