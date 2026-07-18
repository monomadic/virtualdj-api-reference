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

## Ready Tasks

Tasks 1-4 are one FX cluster: they share the same VirtualDJ session, the same deck-FX context, and the same `name=`-interpolation readback technique (proven on v2026-m b9482 — `debug` logs backtick expressions literally, so exact strings must be read via `name=`). Batch them into one local-test session where possible.

### 1. Complete The Per-Effect FX Introspection Sweep

Status: Ready

In progress. Already done (v2026-m b9482): the fixture passed for deck FX slot 1, both overloaded `get_effect_slider_default` forms are resolved, the label/shortname family split is recorded, and the per-effect map in `Effects Engines.md` has its first entry (Backspin). What remains is the mechanical sweep: the rest of the native effects catalog, then the `video` and `transition` targets.

Start here:

- [tests/Pads/Reference - FX Introspection Test.xml](tests/Pads/Reference%20-%20FX%20Introspection%20Test.xml)
- [docs/Effects Engines.md](docs/Effects%20Engines.md) (per-effect map section)

Read first:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md) (FX Helpers rows for the established method)
- [docs/Effects Usage.md](docs/Effects%20Usage.md)
- [docs/VDJScript Verbs.md](docs/VDJScript%20Verbs.md)

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

- [docs/Effects Engines.md](docs/Effects%20Engines.md)
- [docs/VDJScript Verbs.md](docs/VDJScript%20Verbs.md)

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

- [docs/Effects Engines.md](docs/Effects%20Engines.md)
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

- [docs/Effects Engines.md](docs/Effects%20Engines.md)
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
- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

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

- [docs/Completeness Roadmap.md](docs/Completeness%20Roadmap.md)
- [docs/Official VDJScript Coverage Audit.md](docs/Official%20VDJScript%20Coverage%20Audit.md)

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Promote to:

- [docs/VDJScript Verbs.md](docs/VDJScript%20Verbs.md)

Done when:

- A build, deck/controller context, observed result, and follow-up decision are recorded.
- The official local-test status is updated only if the repeat confirms behavior well enough for promotion.

### 8. Close The Remaining Stem-Format Unknowns

Status: Ready

The July 2026 tone-probe rounds settled the stem-file contracts (sidecar
writing-application gate, sample-rate matching, FLAC/ALAC sidecars, 16-bit
ALAC standalones, 4-stem family dead). Five cheap listening probes remain,
each answerable with the existing harness plus one short VirtualDJ session:

1. PCM sidecar — do `pcm_s16le` streams in the Matroska sidecar play?
2. Sidecar bit depth — does a 24-bit FLAC sidecar play correctly, or is
   the 16-bit-only limit (proven for standalone MP4 ALAC) container-wide?
3. Writing-application version string — does any `VirtualDJ <x>.stems2`
   value pass (try `2025.8800.stems2`), or must it be current? Does the
   version affect VirtualDJ regenerating/replacing the sidecar?
4. Role-title case sensitivity — does a sidecar titled `Vocal`/`Kick`
   (capitalized) still map correctly?
5. FLAC-in-MP4 standalone — ffmpeg can mux FLAC into M4A; does VirtualDJ
   accept it as a stems file, or is standalone lossless ALAC-only?

Extend the harness with one probe file per question (master = white noise,
stems = the 100/200/400/800/1600 Hz tone ladder, one variable changed per
file), listen once in VirtualDJ, and record results.

Start here:

- [tests/Stems/make-diagnostic-stems.zsh](tests/Stems/make-diagnostic-stems.zsh)

Read first:

- [docs/Stem File Format.md](docs/Stem%20File%20Format.md) (contracts, acceptance matrix, Known Unknowns)

Record results in:

- [docs/Stem File Format.md](docs/Stem%20File%20Format.md) (acceptance matrix + Known Unknowns)

Promote to:

- [docs/Stem File Format.md](docs/Stem%20File%20Format.md)
- Local toolchain (`/Users/nom/config/config/zsh/bin/vdjstems-pack`) if any
  result changes the recommended codecs or adds a new capability

Done when:

- Each of the five questions has a `Local test` row with the VirtualDJ
  build noted, and the Known Unknowns section lists none of them.

## Blocked Or Hardware-Gated

- Controller display helpers: `controllerscreen_deck`, `controller_battery`.
- Gemini display helper: `gemini_waveform_zoomlevel`.
- Phase helpers: `phase_movement`, `phase_position`, `phase_active`.
- Numark V7 helper: `v7_status`.
- Pioneer RZX helpers: `rzx_touch`, `rzx_touch_x`, `rzx_touch_y`.
- DJC-family helpers: `djc_shift`, `djc_button`, `djc_button_popup`, `djc_button_slider`, `djc_button_select`, `djc_panel`.
- Denon platter/display helper: `denon_platter`.

## Parking Lot

- Consolidation plan Phase 0: build the family-row generators/checker described in [docs/VDJScript Reference Consolidation Plan.md](docs/VDJScript%20Reference%20Consolidation%20Plan.md) by extending `tools/extract_verb_index.py`. No VirtualDJ or hardware needed, so it is a good fit for a session without a live install — but the behavior-evidence queue above outranks restructuring.
- `system`: revisit only if an official example, bundled-resource context, or clearly harmless parameter appears.
- Skin `visual type` canaries: do after the current no-hardware VDJScript evidence queue unless a skin-specific question makes it urgent.
