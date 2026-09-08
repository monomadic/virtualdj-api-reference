# Verb tail structural discovery

The transfer assessment on 2026-09-08 found a real boundary gap in
`extract_action_contracts.py`: its method scan stopped at the first RET and its
helper scan imposed instruction and call-count windows. The extractor now uses
`LC_FUNCTION_STARTS` intervals, shared with skin discovery. The decoder reads the
`__TEXT` segment address rather than assuming an image base. Code after an early
return remains in scope; unknown entry addresses are reported instead of guessed.
For example, the regenerated own-method candidates include `cue_display` literals
`distance` and `position`. These are Tier-2 leads, not new behavioral findings.

Shared helper vocabularies were already covered by `extract_binary_vocabularies.py`:
its seeded groups, ADRP/ADD regions and pointer tables remain useful. What was
missing was a per-verb direct-call association with literals *inside* helpers.
`method_traces` now records, for each slot that found something, its root and
the helper literals grouped by the helper that compares them. The call-graph
addresses behind that — direct edges, visited functions, deeper unvisited
targets, unbounded targets and their counts, for every slot including the quiet
ones — live in `tests/action-contracts-debug.json`, one command away as
`just verb-traces NAME`, because `just get-verb` embeds the contract record
whole and those arrays were 58% of every contract line. The check fails if the
two artifacts disagree about the binary they came from, and
`summary.unbounded_targets` carries the bounds canary: an entry address outside
every `LC_FUNCTION_STARTS` interval is reported, never guessed past. `browser_window` and `padfx` expose helper candidates in
this channel. This is comparison co-occurrence, not argument dataflow proof —
and a helper is not always the verb's own argument matcher. Every helper
therefore carries two measurements, `fanout` (how many `ACTION_` classes reach
it) and `verb_id_fraction` (how much of its literal set is verb ids), because
neither separates a dispatcher alone: on build 18.0.9598 the pad helper is
shared by four classes yet holds four literals, and the song-field helper holds
63 literals for three classes. Together they isolate the script evaluator's own
dispatch, which twelve unrelated classes reach — `set`, `fadeout`, `pulse`,
`custom_button` and the param verbs among them — and whose literals are 71% verb
ids. Its names are kept, in `dispatcher_candidates` and never in
`helper_only_candidates`, and they never count as recovering a documented tail.
The label is a ranking signal, not a verdict: real tails (`toggle`,
`while_pressed`) sit in that dump beside `skin_pannel` and `browser_zoom`.
The vocabulary extractor now shares those bounds. A code region used to be a
cluster of member references padded by a fixed distance, which could not tell
where a function ended: `get_bpm` carried `all`, referenced 0x1c past the end of
the function that compares `absolute` and `ghost`, and that member is now gone.
A region is a comparison chain inside one named function — members still cluster
and reach within it, since the skin element factory compares its vocabulary at
sites kilobytes apart and one span over the whole function would fail the
dispatcher cap — and the chain is clipped to the function it sits in. Direct BL
callees are followed one level for a switch that delegates its matching; on this
build no group gains a member that way, and one that did would carry the
`callee_region` label and its caller in `via`. Its associations remain
separately labelled.

The unstripped escape hatch is already implemented: `action-vtables-9246.json`
holds named virtual methods and `action-modules-9246.json` holds the STABS source
partition. Their historical source is build 18.0.9246; the current extraction's
build, architecture and binary hash are in `action-contracts.json` → `source`.
Re-extracting those historical names would duplicate existing tooling. The new
queue joins historical annotations by class spelling and slot index, without
claiming current methods have the old implementation or transferring addresses.
Unmatched historical classes remain unannotated. Module membership does not prove
current source layout, parameter vocabulary, or behavior.

## Regeneration and queries

Run in this order after updating the input artifacts:

```
just extract-action-contracts
just extract-binary-vocabularies
just extract-action-tail-leads
just check
```

`just verb-contract NAME` exposes the bounded traces. `just action-tail-leads`
reports provenance, limitations and derived summary fields; `--get NAME` shows
one verb and `--queue` emits the ranked queue. `just binary-vocab --verb NAME`
retains the broader enumeration leads and their pointer-table/region evidence.
No copied Markdown vocabulary tables or verb-store test statuses are generated.
The queue's input hashes and `--check` detect stale joins.

The verb store is the one input that is **not** hashed in: it is live state,
read on every query rather than baked into the artifact, so a `put-verb` never
makes the artifact stale and the queue never lags behind it. That join is what
keeps settled work out of the queue — the catalog cross-check only knows what
the arg-form prober confirmed, so on its own it still offered `get_slip_time`
min/sec/msec and `auto_bpm_transition`'s parameters, closed on 2026-09-08 in
the store. A tail a tested record quotes as a token moves to
`recorded_worklist_tails`, negative results included (`sampler_pad_volume`'s
`'siren'` is the catalog's example file, not vocabulary), since neither is
fresh probe work; the verb drops to priority 2 when nothing is left open.
Recorded is not confirmed, and the exception is the house marker: an evidence
entry calling its own result UNDISCRIMINATED keeps its token open and flagged,
which is why `get_saved_loop 'pos'` stays at priority 0. Unquoted prose never
counts, so the join errs toward re-probing.

## Probe handoff

The queue puts the action catalog's `documented_but_not_probe_confirmed` verbs
first — minus the tails the store already records — then prefers open worklist
literals present in bounded methods/helpers, then helper-only candidates from
verb-specific helpers. Dispatcher literals are ranked last. Existing
vocabulary-group associations remain separate from traced calls. The queue
retains worklist verbs even without literal hits.
Read each verb's catalog, attested tails, prior argument forms and fixture needs
before choosing a script: candidate names do not establish argument position.

For query-capable methods, use the delayed plugin channel to retain HRESULT
separately from numeric/text output, followed by HTTP reads in discriminating
fixtures. Bare and nonsense controls, independent runs for drifting values, and
surface-specific testing still apply. A successful HRESULT alone does not prove
that a particular argument is used. Execute-only candidates require an explicit
allowlist, a successful round trip, independent readback, and verified restoration.
This handoff performs no live mutations or behavioral status promotions.

## Reach and limits

The traversal visits overridden methods and direct BL callees only. Indirect
calls, tail branches and deeper helpers are not traversed; their absence from the
candidate set is not evidence of absence. ADRP/ADD scanning is heuristic and does
not track register liveness or full control flow. Literal co-occurrence with a
comparison can include UI labels or unrelated implementation strings. Pointer
loads, computed strings and argument-to-comparison dataflow remain unresolved.

Values are the major blind spot: numeric magnitudes, indices, durations, names,
expressions and other open vocabularies cannot be enumerated by keyword recovery.
Use attested argument shapes and controlled live tests for these verbs. Neither
an empty candidate set nor `arg_demand_slots` supplies a parameter type or grammar.
Every recovered name remains a Tier-2 lead under [Evidence Standards.md](Evidence%20Standards.md).
