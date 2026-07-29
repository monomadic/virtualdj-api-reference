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

### 0b. Topic Search Across Every Corpus

Status: First cut landed (2026-07-26) — coverage tagging remains

The done-when is met: `just topic <term>` ([tools/topic.py](tools/topic.py)) answers a topic
question with matching verbs, effects, and XML elements *and* the real example files that
use them (grep-verified, ranked by coverage), plus topical docs and local-test quirks. It
is pure aggregation over the already-gated stores — no artifact, no hand-tagging — deriving
everything from verb `section`, inventory families, and word-boundary grep. Wired into
`AGENTS.md`, `INDEX.yml`, and `just check` (cross-store smoke test).

Remaining — the metadata layer, which is the part that needs real tagging:

- **Topic reach for name-opaque items.** An item is only found under a topic if the topic
  appears in its name, section, or a grep of it. That misses families whose topic is not in
  the element name — searching `waveform` does not surface `rhythmzone`, `scratchwave`,
  `blockwave`, `beattunnel` (only the doc pointer saves it). These need an explicit topic
  tag. This is the "rich metadata to each searchable item" idea, and it is good mechanical
  subagent work: add a `topics: [...]` field to store records and an element→topics map,
  then have `topic.py` consult it alongside the derived matches.
- Multi-word terms are treated as one string (`color fx` ≠ `colorfx`); a synonym/alias map
  would fold those together.
- Keep it a query — no generated topic pages. Same rule as everywhere else.

Read first:

- [tools/topic.py](tools/topic.py) — the aggregator to extend with a tag lookup.

### 1. Complete The Per-Effect FX Introspection Sweep

Status: Structural sweep COMPLETE (2026-07-22) — only rendering behavior is left

[tools/sweep_fx_introspection.py](tools/sweep_fx_introspection.py) captured counts, short+full labels, normalized **defaults**, live value text, and length/beats flags for all **119** installed effects into [tests/fx-introspection-dump.json](tests/fx-introspection-dump.json), plus the enabled cycle for all three targets. Query it with `just get-fx <effect>` / `just find-fx [--category=deck_fx|video_fx|transition] [--has-length]` / `just fx-stats` — do not read the dump and do not hand-transcribe it.

What the sweep settled:

- **Introspection is read-only.** Every `get_effect_*` helper accepts an effect *name* where the docs show a slot number (`get_effect_slider_count 'Echo'`, `get_effect_slider_default 'Echo' 3`), returning the same values as the slot form for all 119 title-resolvable effects with no `effect_select` and no state change. This is the cheap way to ask about an effect that is not loaded.
- **`get_effect_title '<name>'`** returns `'<Canonical> - Deck N'` or `''`, so it resolves a name to its canonical spelling and probes existence. Case-insensitive, *not* space-insensitive. Blind spot: `''` for `Stems` and `Vocals`, which select and introspect fine through a slot — so a title miss must be confirmed by selecting before the name is called unknown.
- **Audio-vs-video: cycle membership, not loadability.** All three selectors accept any installed effect name (`video_fx_select 'Echo'` really does set the video slot to Echo), so what a target accepts discriminates nothing. The three `+1` cycles *are* disjoint and are the app's own category assignment: 63 deck FX, 17 video FX, 35 transitions. Each is the enabled/favorites subset, so an installed effect in no cycle (`Lottery`, `Sweep`, `Title`, `Vocals`) is category-*unknown*, not uncategorised.
- **`Brake` and `Shader` resolved.** `Brake` is not a selector name on this build at all — a docs-catalog error; the real ones are `BrakeStart`, `VinylBrake`, `Beat Brake`. `Shader` is an alias for `Visuals`, which loads into a deck slot perfectly well; the original sweep only ever asked for it by the wrong name. `BeatGrid` is likewise a spacing error for `Beat Grid`. Nothing here was ever "video-only".
- **`*_skip_length` re-indexes, it does not blank.** Index *i* is the *i*-th slider with the length slider removed, so the last index is always empty. Verified on all 47 length-bearing effects; the length slider is not always index 2 and not always labelled `LEN`.

Remaining (rendering behavior, needs video output — not introspection):

- `video_fx_slider`, `video_fx_clear`, `video_transition_slider`, and `deck master` scoping: what they actually render.
- Whether the 4 category-unknown effects land in a target's list when enabled in the FX list editor.
- **Promotion stays deferred to TODO task 0**: the data is queried from the artifact, not copied into `Effects Engines.md`. Do not hand-transcribe the dump.

Start here:

- Re-run after a VirtualDJ update: `python3 tools/sweep_fx_introspection.py > tests/fx-introspection-dump.json` (needs `just vdj-up` green)
- [tests/Pads/Reference - FX Introspection Test.xml](tests/Pads/Reference%20-%20FX%20Introspection%20Test.xml) (pad-surface checks only)

Read first:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md) (FX Helpers rows only, for the established method)
- `just get-fx <effect>` instead of [docs/Effects Engines.md](docs/Effects%20Engines.md) for control maps

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md), and `just put-verb <name> test_status=… evidence="…"`

Done when:

- The remaining video-rendering verbs get at least one recorded pass each.
- Generic FX control guidance distinguishes observed behavior from inference.

### 2. Characterize FX Bank Save And Load

Status: DONE (2026-07-26, HTTP). A bank is a rack of effect SELECTIONS for slots 1-6 — not active state, not slider values, and global across decks. `effect_bank_load` returns true/false as a bank-populated probe. Recorded in the tracker and on `effect_bank_save`/`effect_bank_load` (`just get-verb effect_bank_save`).

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

Status: PARTIAL (2026-07-26, HTTP). Confirmed the release-FX path is separate from deck slots 1-6 (`is_releasefx` never flips from loading effects into numbered slots); the release sliders are accepted but inert without an armed release FX, which needs a momentary control HTTP can't drive. Remaining: arm a release FX on a pad/mapper surface and characterize activation. Recorded in the tracker and verb store.

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

Status: DONE (2026-07-26, HTTP). Confirmed plugin-instance-scoped (targets the BeatGrid slot), with a bare form and an unquoted-slot-number form; get/set/cur are BeatGrid's own vocabulary. Recorded as BeatGrid-specific, not generic. See `just get-verb effect_command`.

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

Status: MAPPER FIRING DONE (2026-07-27, DDJ-GRV6 hardware) — device-definition schema still open. HTTP-verified on real hardware that the mapper `<map value action>` schema binds and fires (ONINIT on load, PLAY_PAUSE on press), plus three gotchas: control names must match the device definition exactly (wrong name fails silently), loading a mapping resets `$` globals, and editing an active mapper file needs a full restart (re-select does not reload). See the tracker's "Mapper Firing" section and `docs/Mapper XML.md`. Factory-mapping export (Factory default -> Save) was tried as a shortcut to the device definition: it yields the factory `<mapper>` (control names + canonical actions, 293 bindings, lints clean) but NOT the `<device>` definition, so it does not unblock this. STILL OPEN: the custom `<device>` definition schema is untested because the DDJ-GRV6 is factory-recognized — needs unrecognized hardware or a virtual MIDI port + injection to exercise a custom device definition.

The mapper reference's device-definition schema is official-doc-derived but never load-tested locally. A `SIMPLE_MIDI` device context already exists in the local install's Mappers folder. Mappers are one of the repo's named coverage cliffs, so this is the highest-value task outside the FX cluster.

Start here:

- [docs/Mapper XML.md](docs/Mapper%20XML.md)
- [examples/Mappers/README.md](examples/Mappers/README.md)

Done when:

- A minimal `<device type="MIDI">` XML placed in the VirtualDJ `Devices/` folder is detected by the app, and a paired mapper's `<map>` bindings fire.
- Results (including failures) are recorded in [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md) and promoted into `Mapper XML.md` source labels (`Local test`).
- While in the mapper context, the `just check` mapper-lint warnings for `none`, `browser_filter`, and `browser_search` (factory-mapper verb candidates) are probed and either confirmed as real verbs or recorded as unresolved. **The HTTP channel has already been tried and cannot settle it** (2026-07-22): all three return `error:-2147467259`/`false`, and so do the official verb `nothing` and a bogus name. Bind them in a scratch keyboard mapper instead.

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

### 8. Characterize The VirtualDJ Remote App Wire Protocol

Status: DONE (2026-07-27) — transport, wire format, subscriptions, and actions are all
verified in both directions; only minor open questions remain (see end of this task)

Settled with a live session (socket watcher + `dns-sd` + per-connection `nettop` deltas;
recorded in the tracker, [docs/HTTP Control Interface.md](docs/HTTP%20Control%20Interface.md),
and [docs/Application Internals.md](docs/Application%20Internals.md) Remote Skins):

- Remote does **not** use the Network Control HTTP channel; port 80 saw no Remote traffic.
- Discovery is inverted from the obvious guess: the **phone advertises** Bonjour type
  `_vdjremote8._tcp` (SRV → phone, port 4243 observed) and listens; **VirtualDJ connects
  out** to the phone as the TCP client, one persistent connection.
- Semantics are **event-driven push**: idle seconds carry 0 bytes on that connection; a
  deck load pushed ~249 KiB desktop→phone in one second with no inbound request; unload
  ~1.4 KiB; otherwise only sub-KB keepalives.

**Wire format also DONE (2026-07-27)** — see [docs/Remote Protocol.md](docs/Remote%20Protocol.md).
Framing is `8JDV` + `u32` total length + `u16` type; the device opens with subscription
frames carrying ordinary VDJScript queries by id, and VirtualDJ pushes typed values
(`val` float32 / `txt` / `fail`) plus browser folder XML, settings, and selected-folder
state. Replaying a captured opener is enough to hold a session — no pairing token. Capture
tool: `python3 tools/vdjremote_dial.py <device-ip>`; reference capture at
[tests/vdjremote-opener.bin](tests/vdjremote-opener.bin).

**Subscriptions also DONE (2026-07-27)**: the vocabulary is *all of VDJScript*, not a fixed
schema. Verified by substituting synthetic SUBSCRIBE frames into a replayed opener —
`get_version`, `get_effect_name 1`, `deck 3 get_bpm`, and a full ternary all resolved, and
push-on-change was measured (a load pushed title/artist/BPM/path within the same second;
`get_position` streamed at 33-34 Hz while playing, silent when paused). KIND is a hint, not
a request; `fail` means "no value now", not "bad query". Tool:
`python3 tools/vdjremote_subscribe.py tests/vdjremote-opener.bin 'left:get_title' 'get_clock'`
paired with a `dns-sd -R` advert.

Remaining:

- **Mid-session subscribe/unsubscribe** is untested; only opening-burst registration has
  been exercised. A client that switches views needs it.
- **Map or bypass the `0x02` control id space.** Only four ids are known, all from one
  device skin (`0xc6` play, `0xc7` cue, `0x41` crossfader, `0x36` volume). Whether the space
  is global or skin-defined is open — but `0x31` may make it moot for third-party clients.
- **Mid-session subscribe/unsubscribe** is untested — only opening-burst registration has
  been exercised. A client that switches views needs it.
- **Undecoded types**: device→desktop `0x09`, `0x0c`, `0x27`, `0x29`, `0x34`; desktop→device
  `0x2b`, `0x3b`. Sessions work without understanding them (replay reproduces them), so this
  is lower priority.
- **Waveform data** has not been located in any frame; check inside the `0x25` ZIP payloads.

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Promote to:

- [docs/Remote Protocol.md](docs/Remote%20Protocol.md)

Done when:

- Action frames are catalogued with example payloads, and the subscription vocabulary is
  characterized as either "any VDJScript query" or a documented subset.

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
