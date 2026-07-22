# TODO

This is the operational queue for open-ended VirtualDJ reference work.

Agents should start here for maintenance, cleanup, documentation, and evidence-pass tasks. Pick the first `Ready` task unless the user names a different task. Read the task-listed files before running broad repository searches.

## Queue Rules

- `Ready`: startable now with the listed files and fixtures.
- `Blocked`: needs hardware, a live VirtualDJ setup, or a clearer external source.
- `Parking lot`: useful later, but not the next best use of time.
- Record manual VirtualDJ observations in [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md).
- Promote stable conclusions into the topical docs named by the task.
- Run `just check` after documentation, fixture, or status edits.
- `Read first` lists are section-scoped: read only the named rows/sections. Use `just grep-verb-docs <name>` for verb lookups instead of opening `docs/VDJScript Verbs.md`.
- [docs/VDJScript Reference Consolidation Plan.md](docs/VDJScript%20Reference%20Consolidation%20Plan.md) and [docs/Completeness Roadmap.md](docs/Completeness%20Roadmap.md) are frozen design references. Do not refresh, reorder, or re-scope them; this file is the only active queue.

## Ready Tasks

### 0. Build The Verb Record Store And `just` Data API

Status: Foundation landed (2026-07-22) — generation + migration remain

The store and its query/edit API exist and are wired into `just check`. This is the compounding-cost reducer: it replaces the record-in-tracker-then-promote-to-three-docs cycle with one `just put-verb`, and lets agents query verb state without loading the 6,300-line monolith.

Done in this pass:

- [tools/verbdb.py](tools/verbdb.py) over the authoritative store [docs/vdjscript-verbs.json](docs/vdjscript-verbs.json), fronted by `just get-verb / put-verb / find-verbs / next-incomplete-verb / verb-stats`. Storage is private behind the API so it can later become one-file-per-verb without retraining agents.
- Merge-safe `bootstrap` seeded all 991 records from the index + coverage audit (official names + Needs-Local-Test gap) + tracker status tables. It correctly finds the 19-name gap (17 hardware-blocked → skipped by `next-incomplete`), leaving `dualdeckmode_decks` and `system` as the 2 active items, and auto-detected 7 tracker `Pass` rows.
- `verbdb.py check` (schema, alias resolution, index coverage, count freshness) is in `just check`. Entrypoints (`AGENTS.md`, `INDEX.yml`, `docs/README.md`, `tools/README.md`) route verb lookups and result-recording to the flat `just get-verb` / `find-verbs` / `put-verb` commands.

Reports are queries, not files (2026-07-22):

- `just find-verbs` filters on `--surface`, `--section`, `--tier`, `--status`, `--kind`, `--needs-test`, with `--format=json` for structured output and `--limit`. A category listing is just an unfiltered query, so **no derived Markdown is written to disk** — nothing can drift, and there is no staleness gate to maintain. An earlier pass generated `docs/VDJScript/generated/*.md` and was reverted for exactly this reason.
- Rule for future work: do not add a generator that writes a Markdown copy of store data. If a view is wanted, add a query or a flag. Building reader-facing documentation is a later phase, driven by findings — not something to design for now.

Remaining:

- Add richer record fields as needed by contracts (`forms`, `platforms`, `deck_scope`); `put` currently covers the scalar/list fields, nested contract detail is hand-edited in the JSON.
- Grow the query layer where a real question is awkward to ask (e.g. verbs by evidence source, or by presence of a local-test note).
- The monolith still holds the authored prose. Retiring it follows the frozen plan's phased, one-family-at-a-time migration; do not delete hand-authored docs ahead of that.

Effect catalog is queryable (2026-07-22): [tools/fxdb.py](tools/fxdb.py) / `just get-fx / find-fx / fx-stats` answers slider/button questions straight from the sweep artifact, gated by `fxdb.py check` in `just check`. No Markdown copy — same rule as the verb store.

Tasks 1-4 are one FX cluster: they share the same VirtualDJ session and the same deck-FX context. Batch them into one local-test session where possible. Preferred readback channel: the [HTTP control interface](docs/HTTP%20Control%20Interface.md) (`just vdj-query`), which returns exact strings and makes the sweeps scriptable — the older `name=`-interpolation pad technique (proven on v2026-m b9482) is now needed only for pad/skin-surface-specific checks.

### 1. Complete The Per-Effect FX Introspection Sweep

Status: Ready

Structural sweep DONE (2026-07-22, VirtualDJ 2026, HTTP interface): [tools/sweep_fx_introspection.py](tools/sweep_fx_introspection.py) captured slider/button counts, short+full labels, and live value text for all 95 effects reachable into an audio deck-FX slot → [tests/fx-introspection-dump.json](tests/fx-introspection-dump.json). Spot-check reproduced the prior hand map exactly. Finding: the `effect_select +1` cycle is only the enabled subset (63); the full installed set is larger and name-reachable. Both overloaded `get_effect_slider_default` forms were already resolved (v2026-m b9482).

Remaining:

- Normalized slider **defaults** (`get_effect_slider_default '<effect>' <fallback>`) and reset-value text — needs a per-slider reset pass; extend the sweep script with a defaults pass.
- **Audio-vs-video classification.** Slot 1 accepts video effects by name (`Blinds`, `Cube`, `Camera` all load and report controls), so the 95 swept effects mix both and the sweep cannot currently tell them apart. Find a discriminator (a `video`-target query, or the effect's own metadata) and record it per effect.
- Resolve why `Brake` and `Shader` do not load under any spelling — reason is unresolved, and "video-only" is ruled out by the video effects that do load.
- The `video` and `transition` targets (the dump covers deck-FX slot 1 only).
- **Promotion is deferred to TODO task 0**: the verb-store bootstrap ingests `tests/fx-introspection-dump.json` mechanically instead of hand-writing 95 rows into `Effects Engines.md`. Do not hand-transcribe the dump.

Start here:

- Regenerate/extend: `python3 tools/sweep_fx_introspection.py` (needs `just vdj-up` green)
- [tests/Pads/Reference - FX Introspection Test.xml](tests/Pads/Reference%20-%20FX%20Introspection%20Test.xml) (pad-surface checks only)
- [docs/Effects Engines.md](docs/Effects%20Engines.md) (per-effect map section)

Read first:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md) (FX Helpers rows only, for the established method)
- [docs/Effects Usage.md](docs/Effects%20Usage.md)
- `just grep-verb-docs get_effect_slider_default` and `just grep-verb-docs effect_slider` for the verb rows

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Promote to:

- [docs/Effects Engines.md](docs/Effects%20Engines.md)
- [docs/Effects Usage.md](docs/Effects%20Usage.md)
- [docs/VDJScript Verbs.md](docs/VDJScript%20Verbs.md)

Done when:

- Slider/button counts, labels, defaults, and text readbacks are recorded per native effect in the `Effects Engines.md` map, with build noted.
- The `video` and `transition` targets get at least one recorded pass each.
- Generic FX control guidance distinguishes observed behavior from inference.

### 2. Characterize FX Bank Save And Load

Status: Ready

Start here:

- [tests/Pads/Reference - FX Bank Test.xml](tests/Pads/Reference%20-%20FX%20Bank%20Test.xml)

Read first:

- [docs/Effects Engines.md](docs/Effects%20Engines.md) (bank save/load rows only — `rg -n effect_bank`)
- `just grep-verb-docs effect_bank_save`

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Promote to:

- [docs/Effects Engines.md](docs/Effects%20Engines.md)
- [docs/Effects Usage.md](docs/Effects%20Usage.md)

Done when:

- Restored effect names, active states, slider values, and deck scope are recorded.

### 3. Separate Release FX From Normal Slot FX

Status: Ready

Start here:

- [tests/Pads/Reference - Release FX Test.xml](tests/Pads/Reference%20-%20Release%20FX%20Test.xml)

Read first:

- [docs/Effects Engines.md](docs/Effects%20Engines.md) (release-FX rows only — `rg -n releaseslider`)
- [docs/Effects Usage.md](docs/Effects%20Usage.md)

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Promote to:

- [docs/Effects Engines.md](docs/Effects%20Engines.md)
- [docs/Effects Usage.md](docs/Effects%20Usage.md)

Done when:

- `effect_releaseslider*` and `is_releasefx` behavior is described separately from normal deck FX controls.

### 4. Keep BeatGrid `effect_command` Plugin-Specific

Status: Ready

Start here:

- [tests/Pads/Reference - BeatGrid Command Test.xml](tests/Pads/Reference%20-%20BeatGrid%20Command%20Test.xml)

Read first:

- [docs/Effects Engines.md](docs/Effects%20Engines.md) (BeatGrid and `effect_command` rows only — `rg -n effect_command`)
- [docs/Native Effects.md](docs/Native%20Effects.md)

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Promote to:

- [docs/Effects Engines.md](docs/Effects%20Engines.md)
- [docs/VDJScript Verbs.md](docs/VDJScript%20Verbs.md)

Done when:

- Confirmed `effect_command` examples are documented as BeatGrid-specific rather than generic plugin control advice.

### 5. Author And Load-Test A Minimal Custom Device Definition

Status: Ready

The mapper reference's device-definition schema is official-doc-derived but never load-tested locally. A `SIMPLE_MIDI` device context already exists in the local install's Mappers folder. Mappers are one of the repo's named coverage cliffs, so this is the highest-value task outside the FX cluster.

Start here:

- [docs/Mapper XML.md](docs/Mapper%20XML.md)
- [examples/Mappers/README.md](examples/Mappers/README.md)

Done when:

- A minimal `<device type="MIDI">` XML placed in the VirtualDJ `Devices/` folder is detected by the app, and a paired mapper's `<map>` bindings fire.
- Results (including failures) are recorded in [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md) and promoted into `Mapper XML.md` source labels (`Local test`).
- While in the mapper context, the `just check` mapper-lint warnings for `none`, `browser_filter`, and `browser_search` (factory-mapper verb candidates) are probed and either confirmed as real verbs or recorded as unresolved.

### 6. Continue Hidden Button Editor Candidate Probes

Status: Ready

Start here:

- [tests/Pads/Reference - Hidden Button Editor Tests.xml](tests/Pads/Reference%20-%20Hidden%20Button%20Editor%20Tests.xml)
- [docs/Undocumented VDJScript Candidates.md](docs/Undocumented%20VDJScript%20Candidates.md)

Read first:

- [docs/Button Editor Catalog Audit.md](docs/Button%20Editor%20Catalog%20Audit.md)
- [docs/Button Editor Taxonomy.md](docs/Button%20Editor%20Taxonomy.md)
- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md) (hidden-candidate probe table only)

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)
- [docs/Undocumented VDJScript Candidates.md](docs/Undocumented%20VDJScript%20Candidates.md)

Promote to:

- [docs/VDJScript Verbs.md](docs/VDJScript%20Verbs.md), only when behavior is locally observed and useful enough for normal guidance.

Done when:

- Candidate behavior is recorded as pass, partial, failed, or still discovery-only.
- Catalog-only names stay out of ordinary recommendations unless behavior proof supports promotion.

### 7. Repeat `dualdeckmode_decks` In A Better Context

Status: Ready, but low expected yield until a concrete context is identified

The first pad-context run (v2026-m b9336) recorded `dualdeckmode` toggling on while current and deck-scoped `dualdeckmode_decks` readbacks stayed false on both decks. The promotion condition is a visible dual-deck pair or controller context (deck pairs 1/3 or 2/4), which realistically means a 4-deck skin setup or a controller. Do not repeat the same pad-context probe; identify the better context first, or treat this as semi-blocked.

Start here:

- [tests/Pads/Reference - Dual Deck Mode Test.xml](tests/Pads/Reference%20-%20Dual%20Deck%20Mode%20Test.xml)
- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Read first:

- [docs/Official VDJScript Coverage Audit.md](docs/Official%20VDJScript%20Coverage%20Audit.md) (the `dualdeckmode` rows only)

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Promote to:

- [docs/VDJScript Verbs.md](docs/VDJScript%20Verbs.md)

Done when:

- A build, deck/controller context, observed result, and follow-up decision are recorded.
- The official local-test status is updated only if the repeat confirms behavior well enough for promotion.

## Blocked Or Hardware-Gated

- Controller display helpers: `controllerscreen_deck`, `controller_battery`.
- Gemini display helper: `gemini_waveform_zoomlevel`.
- Phase helpers: `phase_movement`, `phase_position`, `phase_active`.
- Numark V7 helper: `v7_status`.
- Pioneer RZX helpers: `rzx_touch`, `rzx_touch_x`, `rzx_touch_y`.
- DJC-family helpers: `djc_shift`, `djc_button`, `djc_button_popup`, `djc_button_slider`, `djc_button_select`, `djc_panel`.
- Denon platter/display helper: `denon_platter`.

## Parking Lot

- `system`: revisit only if an official example, bundled-resource context, or clearly harmless parameter appears.
- Skin `visual type` canaries: do after the current no-hardware VDJScript evidence queue unless a skin-specific question makes it urgent.
