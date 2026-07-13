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

### 1. Author And Load-Test A Minimal Custom Device Definition

Status: Ready

The mapper reference's device-definition schema is official-doc-derived but never load-tested locally. A `SIMPLE_MIDI` device context already exists in the local install's Mappers folder.

Start here:

- [docs/Mapper XML.md](docs/Mapper%20XML.md)
- [examples/Mappers/README.md](examples/Mappers/README.md)

Done when:

- A minimal `<device type="MIDI">` XML placed in the VirtualDJ `Devices/` folder is detected by the app, and a paired mapper's `<map>` bindings fire.
- Results (including failures) are recorded in [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md) and promoted into `Mapper XML.md` source labels (`Local test`).

### 2. Repeat `dualdeckmode_decks` In A Better Context

Status: Ready

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

### 3. Continue Hidden Button Editor Candidate Probes

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

### 4. Build The FX Introspection Table

Status: Ready

Start here:

- [tests/Pads/Reference - FX Introspection Test.xml](tests/Pads/Reference%20-%20FX%20Introspection%20Test.xml)

Read first:

- [docs/Effects Engines.md](docs/Effects%20Engines.md)
- [docs/Effects Usage.md](docs/Effects%20Usage.md)
- [docs/VDJScript Verbs.md](docs/VDJScript%20Verbs.md)

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Promote to:

- [docs/Effects Engines.md](docs/Effects%20Engines.md)
- [docs/Effects Usage.md](docs/Effects%20Usage.md)
- [docs/VDJScript Verbs.md](docs/VDJScript%20Verbs.md)

Done when:

- Slider/button counts, labels, defaults, text readbacks, and `effect_has_*` behavior are recorded for representative built-in effects.
- Generic FX control guidance distinguishes observed behavior from inference.

### 5. Characterize FX Bank Save And Load

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

### 6. Separate Release FX From Normal Slot FX

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

### 7. Keep BeatGrid `effect_command` Plugin-Specific

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
