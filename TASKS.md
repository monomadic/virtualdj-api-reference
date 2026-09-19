# Tasks

This is the operational queue for open-ended VirtualDJ reference work.

Agents should start here for maintenance, cleanup, documentation, and evidence-pass tasks. Pick the first `Ready` task unless the user names a different task. Read the task-listed files before running broad repository searches.

## Queue Rules

### Status convention

Every `### <id>. <title>` task carries exactly one status line, and it is the first line under
the heading:

```
Status: <state>
```

The state is one word from a closed vocabulary and nothing else — no date, no bold, no
qualifier, no trailing prose. Everything else goes in a `Note:` paragraph directly below it.
This is machine-readable on purpose: `just next-task` parses it, and a status line it cannot
read stops the run instead of quietly skipping the task.

| State | Meaning |
| --- | --- |
| `Ready` | Startable now with the listed files and fixtures. Launching VirtualDJ locally counts as startable. |
| `Blocked` | Needs hardware or an external source not available here. |
| `Conditional` | Start only when the named trigger occurs; the `Note:` names it. |
| `Parking lot` | Useful later, but not the next best use of time. |
| `Done` | Complete; kept as the record of what was established. |

The state describes the task **now**. For a task whose first pass landed with work remaining,
it describes that remaining work — `Ready` if the remainder is startable, `Blocked` if it is
not — and the `Note:` carries what already landed. Task identifiers must be unique;
`just check` fails on a duplicate.

### Working rules

- Record manual VirtualDJ observations in [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md).
- Promote stable conclusions into the topical docs named by the task.
- Run `just check` after documentation, fixture, or status edits.
- `Read first` lists are section-scoped: read only the named rows/sections. Use `just grep-verb-docs <name>` for verb lookups instead of opening `docs/VDJScript Verbs.md`.
- [docs/VDJScript Reference Consolidation Plan.md](docs/VDJScript%20Reference%20Consolidation%20Plan.md) and [docs/Completeness Roadmap.md](docs/Completeness%20Roadmap.md) are frozen design references. Do not refresh, reorder, or re-scope them; this file is the only active queue; completed tasks move to [HISTORY.md](HISTORY.md).

## Accepted next sequence (2026-09-05 review)

This sequence takes precedence over the historical task ordering below. It reconciles the
review into this queue; the dated assessment is not another worklist. Existing task numbers
remain the owners of their broader work. Read their scoped evidence before probing.

### R4. Only the infrastructure change demonstrated by R2 or R3

Status: Conditional

Note: Start only with a concrete blocker from R2 or R3. **Neither produced one (2026-09-06).** R2's wall was that many shipped skin attributes are `class=""` template placeholders rather than reader vocabulary — a fact about the format, not a reference the extractor failed to resolve. R3's fixture fitted the existing capture contract without change. So this stays Conditional and waits for a later finding the current record genuinely cannot hold; index inversion remains task 11 and is not a prerequisite for anything here.

Owners: task 0/10 for representation, 10/10b for shared runtime helpers. A specific extractor
repair is new work; index inversion remains task 11 and is not a pilot prerequisite.

Name the exact finding the current record cannot hold or the reader/reference the extractor
cannot resolve. Make the smallest data-command or extraction change that represents it or
recovers it, with a focused regression. Follow `CSkinEngine::createAction` or another shared
helper only when the investigation supplies a concrete question. No upfront coverage schema,
general extractor rebuild, or agent-cost bookkeeping is part of this task.

## Ready Tasks

### 0. Build The Verb Record Store And `just` Data API

Status: Conditional

Note: Foundation landed (2026-07-22) — generation + migration remain

The store and its query/edit API exist and are wired into `just check`. This is the compounding-cost reducer: it replaces the record-in-tracker-then-promote-to-three-docs cycle with one `just put-verb`, and lets agents query verb state without loading the 6,300-line monolith.

Done in this pass:

- [tools/verbdb.py](tools/verbdb.py) over the authoritative store [docs/vdjscript-verbs.json](docs/vdjscript-verbs.json), fronted by `just get-verb / put-verb / list-verbs / next-incomplete-verb / verb-stats`. Storage is private behind the API so it can later become one-file-per-verb without retraining agents.
- Merge-safe `bootstrap` seeded all 991 records from the index + coverage audit (official names + Needs-Local-Test gap) + tracker status tables. It correctly finds the 19-name gap (17 hardware-blocked → skipped by `next-incomplete`), leaving `dualdeckmode_decks` and `system` as the 2 active items, and auto-detected 7 tracker `Pass` rows.
- `verbdb.py check` (schema, alias resolution, index coverage, count freshness) is in `just check`. Entrypoints (`AGENTS.md`, `INDEX.yml`, `docs/README.md`, `tools/README.md`) route verb lookups and result-recording to the flat `just get-verb` / `list-verbs` / `put-verb` commands.

Reports are queries, not files (2026-07-22):

- `just list-verbs` filters on `--surface`, `--section`, `--tier`, `--status`, `--kind`, `--needs-test`, with `--format=json` for structured output and `--limit`. A category listing is just an unfiltered query, so **no derived Markdown is written to disk** — nothing can drift, and there is no staleness gate to maintain. An earlier pass generated `docs/VDJScript/generated/*.md` and was reverted for exactly this reason.
- Rule for future work: do not add a generator that writes a Markdown copy of store data. If a view is wanted, add a query or a flag. Building reader-facing documentation is a later phase, driven by findings — not something to design for now.

Remaining:

- Add richer record fields as needed by contracts (`forms`, `platforms`, `deck_scope`); `put` currently covers the scalar/list fields, nested contract detail is hand-edited in the JSON.
- Grow the query layer where a real question is awkward to ask (e.g. verbs by evidence source, or by presence of a local-test note).
- The monolith still holds the authored prose. Retiring it follows the frozen plan's phased, one-family-at-a-time migration; do not delete hand-authored docs ahead of that.

Effect catalog is queryable (2026-07-22): [tools/fxdb.py](tools/fxdb.py) / `just get-fx / list-fx / fx-stats` answers slider/button questions straight from the sweep artifact, gated by `fxdb.py check` in `just check`. No Markdown copy — same rule as the verb store.

Tasks 1-4 are one FX cluster: they share the same VirtualDJ session and the same deck-FX context. Batch them into one local-test session where possible. Preferred readback channel: the [HTTP control interface](docs/HTTP%20Control%20Interface.md) (`just vdj-query`), which returns exact strings and makes the sweeps scriptable — the older `name=`-interpolation pad technique (proven on v2026-m b9482) is now needed only for pad/skin-surface-specific checks.

### 1. Complete The Per-Effect FX Introspection Sweep

Status: Conditional

Note: Structural sweep complete 2026-07-22; the rendering half closed 2026-09-06. One settings-UI question is left, named at the end.

[tools/sweep_fx_introspection.py](tools/sweep_fx_introspection.py) captured counts, short+full labels, normalized **defaults**, live value text, and length/beats flags for all **119** installed effects into [tests/fx-introspection-dump.json](tests/fx-introspection-dump.json), plus the enabled cycle for all three targets. Query it with `just get-fx <effect>` / `just list-fx [--category=deck_fx|video_fx|transition] [--has-length]` / `just fx-stats` — do not read the dump and do not hand-transcribe it.

What the sweep settled:

- **Introspection is read-only.** Every `get_effect_*` helper accepts an effect *name* where the docs show a slot number (`get_effect_slider_count 'Echo'`, `get_effect_slider_default 'Echo' 3`), returning the same values as the slot form for all 119 title-resolvable effects with no `effect_select` and no state change. This is the cheap way to ask about an effect that is not loaded.
- **`get_effect_title '<name>'`** returns `'<Canonical> - Deck N'` or `''`, so it resolves a name to its canonical spelling and probes existence. Case-insensitive, *not* space-insensitive. Blind spot: `''` for `Stems` and `Vocals`, which select and introspect fine through a slot — so a title miss must be confirmed by selecting before the name is called unknown.
- **Audio-vs-video: cycle membership, not loadability.** All three selectors accept any installed effect name (`video_fx_select 'Echo'` really does set the video slot to Echo), so what a target accepts discriminates nothing. The three `+1` cycles *are* disjoint and are the app's own category assignment: 63 deck FX, 17 video FX, 35 transitions. Each is the enabled/favorites subset, so an installed effect in no cycle (`Lottery`, `Sweep`, `Title`, `Vocals`) is category-*unknown*, not uncategorised.
- **`Brake` and `Shader` resolved.** `Brake` is not a selector name on this build at all — a docs-catalog error; the real ones are `BrakeStart`, `VinylBrake`, `Beat Brake`. `Shader` is an alias for `Visuals`, which loads into a deck slot perfectly well; the original sweep only ever asked for it by the wrong name. `BeatGrid` is likewise a spacing error for `Beat Grid`. Nothing here was ever "video-only".
- **`*_skip_length` re-indexes, it does not blank.** Index *i* is the *i*-th slider with the length slider removed, so the last index is always empty. Verified on all 47 length-bearing effects; the length slider is not always index 2 and not always labelled `LEN`.

Narrowed 2026-09-06 (HTTP, build 18.0.9598). Three of the four remaining questions turned out
not to need rendering at all, and answering them found a broken verb. See the tracker's "Video
FX Over HTTP" section; state was recorded and restored.

- **`deck master` scoping: answered.** The video FX chain hangs off the master output, and an
  unscoped video verb addresses it — `video_fx_select` bare and `deck master video_fx_select`
  both read `0.18` while `deck 1 video_fx_select` reads `0`.
- **`video_fx_slider`: answered.** It indexes correctly in both positions; execute moves the
  named slider and nothing else. Recorded `Pass`.
- **`get_video_fx_slider_label`: answered, and it is broken.** The index argument is never
  read: with Colorize selected (labels COL/STR/SAT/SPD/BRI) every index 0–99 returned `COL`.
  Recorded `Fail`; use `get_effect_slider_label '<effect>' <n>`, which indexes correctly and
  needs no selection.
- **The 4 category-unknown effects: half answered.** Walking `video_fx_select +1` traversed
  exactly 17 effects and wrapped cleanly, matching the catalog's `video_fx` category and
  containing none of `Lottery`, `Sweep`, `Title`, `Vocals`. Whether *enabling* one in the FX
  list editor puts it in a cycle is still a GUI question.

Rendering half closed 2026-09-06 — **the gate was the video window, not video output.**
`video_fx` could not be activated with no track, with an audio track, or even with a real video
loaded; what was missing was the window itself. `video` ("Open/close video window") opens it, a
paused deck is enough to render a frame, and the identical `video_fx on` call then works. Four
rendering passes recorded, each watched on screen, all state restored (tracker: "Video FX
Rendering: The Gate Was The Video Window"):

| Verb | Watched | Result |
| --- | --- | --- |
| `video_fx` | `Negative` on a colour-bar pattern | every colour inverted |
| `video_fx_slider` | `Colorize` hue `0.1` → `0.7` | tint went amber → magenta |
| `video_fx_clear` | `Colorize` actively tinting | render returned to the source |
| `video_transition_slider` | `Blinds` NB `0.15` → `0.95` at crossfader `0.5` | ~5 thick blinds → ~15 thin |

`video_fx_clear` **deactivates only** — selection and slider values survive it, which the earlier
pass could not tell because it had only ever run with nothing active. Fixtures were generated
with ffmpeg (a `testsrc2` pattern and a white clip), never the user's library; the transition
needed two *different* videos or the crossfade would have been invisible.

**Conditional on one settings-UI action:** enable one of the four category-unknown effects
(`Lottery`, `Sweep`, `Title`, `Vocals`) in the FX list editor and re-walk the `+1` cycles to see
whether it joins one. There is no verb for that step. Everything else in this task is done.

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

### 3. Separate Release FX From Normal Slot FX

Status: Conditional

Note: 2026-09-06. The done-when is met — the release path is now described separately from
ordinary deck FX, in `docs/Effects Engines.md` §Release FX and `docs/Effects Usage.md`, with
local-test evidence on all three verbs. What is left waits on one operator action, named at the
bottom. Full narrative: the tracker's "Release FX: The Arming Path Does Not Exist In Script".

**This pass overturned the task's own diagnosis.** The 2026-07-26 note said the sliders were
inert because arming "needs a momentary control HTTP can't drive". That is not the obstacle.
`effect_releaseslider_active` is documented to activate *without* one — "and auto activate the
effect" — and it does nothing: `true` returned, `is_releasefx` still `no`, its own query still
`0`, every numbered slot inactive, with deck 1 empty, loaded and playing, scoped and unscoped.
And a pad would run the same script — `tests/Pads/Reference - Release FX Test.xml` fires plain
`effect_releaseslider 25%`, no `down`/`up` wrapper — so that surface adds nothing.

**What is actually missing has no verb.** The verb table, where absence disproves a name, holds
exactly three release names: `effect_releaseslider`, `effect_releaseslider_active`,
`is_releasefx`. There is **no selector**. `effect_select 'releasefx' 'Echo Out'` returns `false`
and changes nothing, scoped or unscoped, leaving the numbered slots untouched. The slot is armed
in the app's own FX lists — the binary carries `Deck %i release effects` and `Master release
effects` beside the other FX-list-editor categories, and `settings.xml` stores eight entries per
deck where script reaches only six. So VDJScript can *drive* the release slot and can never
*create* it.

`is_releasefx` was tried bare, deck-scoped, with slot arguments 0-10, and with the names of
effects this instance really has configured (`Echo Out`, `Phaser`, `Delay`, `Reverb`, `Cut`,
`Backspin`) — `no` throughout, so the earlier negative was never about naming the wrong effect.

**Conditional on one operator action:** assign a release effect in VirtualDJ's own FX lists, then
re-run against `tests/Pads/Reference - Release FX Test.xml` (or over HTTP — the surface does not
matter, as established above) to watch an armed slot for the first time. Until then no release-FX
*behavior* has been observed, and `is_releasefx` has never been seen returning `yes` on any
surface, so its catalog wording "query if **this effect** is in the release effect slot" — which
reads as effect-scoped, the question a plugin GUI asks about itself — stays plausible but
unestablished.

### 7. Repeat `dualdeckmode_decks` In A Better Context

Status: Parking lot

Note: Low expected yield until a concrete context is identified. Deprioritised by the operator
2026-09-06 in favour of tasks 10b/11/12/13; move it back to Ready when a concrete context turns
up, not on a schedule.

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

### 10. Discover The Full Function Contract Per Verb

Status: Ready

Note: 2026-07-29 — the ratified priority now that existence, aliases, hidden flag, and
categories are settled. Goal: for every verb, the complete calling contract — **query return
type, accepted argument forms, and undocumented overloads** — established at Tier 1 where
possible and recorded as structured per-verb data, not prose.

**Completion criterion (2026-09-12):** every verb either has an evidence-backed contract for
the stated build and surfaces, or a named open item carrying one of five reasons — not
measured; measured but the observable did not discriminate; state, surface or hardware
unavailable; conflicting observations; evidence only in prose. `just coverage --frontier` is
the test, `just verb <name>` shows one verb's assessment, and both read the same `assess()`.
"Every undocumented overload found" is not finite and is not the criterion.

Contract fields to establish per verb:

- **Return type in query position: HTTP leg DONE (2026-07-30)** —
  [tools/sweep_return_types.py](tools/sweep_return_types.py) sampled all 652 query verbs in
  three read-only contexts against live VirtualDJ: 623 typed (334 bool / 145 int / 68 float /
  4 percent / 72 text), 0 capability conflicts vs the structural matrix, gated in
  `just check`, queried with `just verb-return-type <name>`. It also refuted the first slot
  labeling: slot 3 is a generic variant query, not onQueryBool — structure claims capability,
  observation claims type. Remaining sub-legs: the 29 all-empty verbs need richer contexts,
  and the Remote-protocol typed sweep (`val` float32 vs `txt` VALUE frames) would confirm
  wire-level types independently of HTTP text rendering.
- **Argument forms — binary-first (reprioritized 2026-07-30, partially DONE)**. The
  E_INVALIDARG method fingerprint landed in the contracts artifact: **436 verbs demand an
  argument somewhere, 114/116 agreement with the sweep's needs-args kind, and 301
  bare-answering query verbs flagged as taking OPTIONAL arguments** — the
  undocumented-overload queue (`summary.optional_arg_queries`), invisible to the bare sweep.
  `method_strings` recovers per-method keywords (`loaded` → `opposite`, `get_time` →
  `short`). Remaining streams for the *forms and types*:

  0. **Runtime parser walk (H4, added 2026-09-07; closed with named limits 2026-09-19).**
     This stream followed the named `IAction::create` on the unstripped 18.0.9246 build for
     delimiter, quoting and fallback rules, and each rule became a discriminating 10b test.
     The closed block, its limits and its log are in
     [HISTORY.md](HISTORY.md#h4-runtime-argument-parsing-from-the-named-iactioncreate).
     For computed-argument probing, the `evaluation_callers` section of
     [tests/runtime-parser-branch-routes.json](tests/runtime-parser-branch-routes.json) is a
     Tier-2 lead list of the b9246 verb methods that call the evaluator and boolean helpers
     directly (`just runtime-grammar --callers IAction::getParamEval`), not evidence of any
     verb's behaviour.
  1. **Argument keywords — DONE (2026-07-30)**; **types — closed as not-extractable.**
     `__stubs` are now named via DYSYMTAB's indirect symbol table (this build is classic
     `LC_DYLD_INFO_ONLY`, not chained fixups), so methods that compare an argument against
     literals are detectable: **259 verbs carry `keyword_candidates`**, recovering
     undocumented enums (`get_bpm absolute|ghost`, `browser_window sidelist|karaoke|…`,
     `loaded opposite`, `get_time short`, `sampler_group_volume touchrelative|locked`).
     Argument *types* were attempted through the same route and do not survive: param access
     is inlined, and a verb's library calls describe what it does with an argument, not how
     it fetches one (`_strcasecmp` appears in numeric-arg verbs). Types are a Tier-1 job.
  2. **HTTP probe in query position** (Tier 1): start with the 301 optional-arg queries and
     the recovered keywords. **Method note (2026-07-30, probed live)**: optional-arg verbs
     silently ignore unknown arguments (`loaded bogusword` → `yes`), so error codes cannot
     confirm a form — probes must compare VALUES across forms in a state where they would
     differ (e.g. `loaded opposite` with exactly one deck loaded). `get_time` demonstrated
     the pattern: bare returns one mode, any argument switches to another. Query-position
     probing is side-effect-free; execute-position confirmation only for whitelisted safe
     verbs, with independent readback (rule 4), never `system`/file/database verbs.
  3. **Shipped-XML corpus mining + appendix parsing** (Tier 2): demoted to corroboration of
     actually-used forms — the binary and the probes discover; the corpus confirms
     parser-accepted usage.
- **Capability matrix: DONE (2026-07-29)** — the vtable-override extraction worked on the
  first attempt. [tools/extract_action_contracts.py](tools/extract_action_contracts.py) walks
  the surviving RTTI (name → typeinfo → vtable) and emits
  [tests/action-contracts.json](tests/action-contracts.json): 955 classes ↔ 955 ids as a
  checked bijection, capability matrix (execute / bool / number / text query) with slot
  meanings calibrated from HTTP-proven verbs, family taxonomy from the class hierarchy
  (100 toggles, 56 sliders), and context mixins. Sweep agreement 652/652 (query) and
  181/186 (action-only); the 5 outliers surfaced a lead — slot 7 is probably the
  options-menu provider (`browser_export`, `*_options` override only it). Gated in
  `just check`; query with `just verb-contract <name>`. See the Candidates doc §Contract
  structure.

- **Slot names: DONE (2026-08-29)** — bundle `18.0.9246` is the last unstripped build, so
  [tools/extract_action_vtables.py](tools/extract_action_vtables.py) resolves every vtable
  entry to a named method ([tests/action-vtables-9246.json](tests/action-vtables-9246.json)).
  Slot 7 is `onUp`, not the options-menu provider guessed above; 8/9 are `onSaveState`/
  `onLoadState`. Recalibrating `query_text` off slot 5 (was reading slot 4, the bool query)
  moved 154 verbs; the old values are preserved as `query_bool`.
- **Verb table: refreshed to 18.0.9583 (2026-09-02).** 1,032 records, 958 distinct ids,
  62 alias groups. Four verbs are new since 9482 — `goto_beat_in_bar` (canonical spelling of
  `goto_bar`, same id 106), `karaoke_clear`, `repeat_start_fade`, `shoutout` — all four with
  bundled English descriptions, now in the Broad Verb Index and the store. The contracts
  bijection is whole again at 958 ↔ 958.
  9583 **dropped the `const char *[38]` category-name array** (no member survives anywhere in
  the executable, nor in `languages.zip`), but the `uint8[distinct_ids + 1]` id → category
  array is intact. `extract_verb_table.py` now falls back to a pinned name list and records
  `summary.categories_source`. The pinned order is not a guess: it is what the array reads on
  both `18.0.9246` (unstripped, read directly) and `18.0.9482`, and carrying it forward
  reproduces the previous category for **1,028/1,028** verbs shared with 9482 and
  **1,025/1,025** shared with 9246, placing the four new verbs in audio / karaoke / repeat /
  sampler. Re-anchor on the binary again if a later build restores the names.

### 10a. A read-only introspection plugin — the only instrument for four questions

Status: Ready

Note: **The channel is OPEN (2026-08-15).** The plugin builds, loads, and has returned its
first full capture: 1,028 verbs × both query callbacks, in `tests/plugin-introspection.json`
(`just plugin-probe <name>`). See the tracker's "Plugin Channel (VDJIntrospect)" section for
the evidence table. Headline results:

- **The documented `DllGetClassObject` path is live.** VirtualDJ type-probes with six IIDs in
  order (Dsp, Buffer, VideoFx, VideoTransition, VideoTransitionMultiDeck, then Basic) and stops
  at the first accepted one. Ad-hoc signing suffices; Xcode is not required.
- **`master_beat_num` is settled: the float-bits defect is in the CORE.** `GetInfo` hands back
  the double `1083943558.0` — the int32 reinterpretation of float32 `4.8646` — so HTTP was
  faithfully rendering an already-broken number. This was the first named experiment; it is
  done.
- **A definitive channel map**: 532 verbs answer on both callbacks, 67 text-only, 11
  numeric-only, 418 on neither, agreeing with the HTTP sweep's kinds (181/181 action-only).
  `E_INVALIDARG` is the numeric channel's "wrong channel" code; the text side says `S_FALSE`.
  Caveat: VirtualDJ writes `0.0` to `*result` even on `E_INVALIDARG`, so the HRESULT is the
  answer, not the value.

Follow-up captures, 2026-08-15 (`tests/plugin-introspection-{leads,controls}.json`) — all
three leads closed, details in the tracker:

- **The HRESULT keyword-discrimination hypothesis is CONFIRMED.** 26 of 165 keyword/nonsense
  pairs differ by HRESULT (`is_using zzznotakeyword` → `E_NOTIMPL`; `action_deck`,
  `device_side`, `get_ns7_platter` → `E_INVALIDARG`), 14 more by value. **This is the method
  for the keyword queue** — it needs no prepared state, unlike value comparison. Two argument
  traps found: `get_license` and `mixermode` return `on` for nonsense arguments.
- **Slot 5 is the label provider** (`stop_button` → `"■"`), and **slot 3 backs both
  callbacks**; slot 4's role is unproven. Exact partition, no remainder — the slot table in
  [docs/Plugin SDK.md](docs/Plugin%20SDK.md) is corrected.
- **Deck context was the wrong explanation** for the 50 silent query verbs, proven with a
  control (`deck 1 get_bpm` → `120`, so the prefix does work; `left get_bpm` fails — the
  `deck` scope word is required). They are 27 verbs HTTP also answered empty (the plugin
  channel distinguishes "no value" from "empty value"; HTTP cannot), 7 wanting an argument,
  and 21 needing **implicit defaults HTTP supplies and a plugin call does not**
  (`get_effect_slider_name 1 1` → `Strength`).

Fourth and fifth captures, 2026-08-15 (`-remaining`, `-late`), closing both remaining items:

- **The silent browser readers were startup timing, not a missing plugin context.** `OnLoad`
  fires while VirtualDJ is still starting. The plugin now sweeps an optional second list ~40s
  after load, and all six `get_browsed_folder*` verbs answer there with nothing else changed.
  **Method rule: an `E_INVALIDARG` from a load-time probe means "not available now", not "no
  such form"** — re-take negatives from the delayed sweep before recording them. Song-level
  readers (`get_browsed_comment|composer|song`) stay silent even late; a highlighted song is
  the next variable.
- **The execute-capable keyword verbs are swept**: 1,126 probes over 217 verbs, query position
  only, 10 excluded outright (file/config/system families, listed in the tracker). 51 pairs
  confirmed by HRESULT over 25 verbs, 36 more by value over 27 — full enum sets recovered for
  `crossfader_curve`, `maximize`, `loop_adjust`, `browser_scroll`, `cue_display`,
  `auto_bpm_transition_options`, `djc_button_select`. Reproduce with
  `just plugin-keyword-report remaining`.
- **Probing execute-capable verbs in query position changed no state**: all 217 bare verbs
  shared with the baseline returned byte-identical values afterwards, HTTP agreeing. One idle
  session's evidence, not a general proof.
- **Host callbacks work off the main thread** — the delayed sweep runs on a detached timer
  thread and completed cleanly. Undocumented in the SDK; one session's evidence.

Sixth capture, 2026-08-15 (`-prepared`) — taken through a **trigger loop** rather than a
restart, which is the ergonomic fix for this whole task: the plugin's thread now polls for a
trigger file, so `just plugin-go` re-sweeps in ~1s while VirtualDJ keeps running. Set the app
up by hand, then ask for a capture.

- **`loaded opposite` is confirmed** — with one deck loaded it returns `off` where nonsense
  returns `on`. This was the case named on 2026-07-30 as needing prepared state, and it is the
  proof that the *value* test works where error codes cannot.
- 25 more pairs confirmed over 12 verbs, including `get_key pioneer|rane|roland|harmonic`
  (controller key notations: 14, 13, 2, 02A vs a default `Ebm`), `get_loaded_song_color
  red|green|blue`, `get_position loopin|loopout`, and `get_song_event`.
- **Browser readers are state-gated, not unsupported**: `get_browsed_key`,
  `get_browsed_filepath` and `sidereco_song` answer once a song is *highlighted*.

Still open, and now clearly bounded:

1. **705 keyword pairs still indistinguishable.** Not disproof — each needs the specific state
   its own verb reacts to. This is per-verb work with a fixture, not another sweep, and the
   trigger loop makes each attempt cheap.
2. **`get_browsed_comment|composer|song`, `get_sample_info`** — likeliest reading is that this
   track carries no comment/composer tag, so `E_INVALIDARG` means "no value". Needs a track
   known to have one.
3. **The untouched half of the SDK.** `GetSongBuffer` is now **DONE** — fully characterized
   2026-08-15 (frames, interleaved stereo, interior pointers into one resident decoded buffer,
   44.1 kHz), which is the input side of the waveform cliff.

   `OnKey` is **attempted and unresolved**. Two plugin types were built and tested — a basic
   `AutoStart` plugin and an active Sound Effect with a visible panel — and neither receives
   anything through `IVdjVideoMouseCallbacks8`, though the slot is accepted every time. The
   interface name is the best remaining explanation: its `(x, y)` coordinates want a *video*
   surface. The last candidate is a video FX plugin, which needs video output.

   Worth knowing before spending more on it: the plugin *lifecycle* question is settled as a
   by-product. A recognised functional type is driven (`OnStart`, `OnProcessSamples`,
   `OnParameter` all fire); a basic plugin is loaded and left alone. So "get a surface, get
   input" has been tested twice and failed twice, and video FX is the only shape left.

   `VDJINTERFACE_SKIN` is **DONE, and it paid off** (2026-08-22). A Sound Effect built with
   `tools/plugin/build.sh --skin --install` returns `VDJINTERFACE_SKIN` from
   `OnGetUserInterface`; VirtualDJ calls it when the effect's GUI is shown, and calls it
   **again on every panel open**. The plugin serves `skin.xml` / `skin.png` from disk rather
   than from bundle resources, so a skin edit costs a panel re-open instead of a restart:
   `just plugin-skin-prepare <xml>` → `just plugin-skin-reload` → `just plugin-skin-log`.
   Everything rendered — backtick VDJScript, `action=""` queries, `visibility=""` conditions,
   `<define>` classes, sprite offsets against an in-memory PNG.

   First results off the new loop, all in the tracker: **starred placeholders are required**
   to substitute at all (in `format=""`, `text=""`, numeric attributes *and* conditions), and a
   starred placeholder inside a condition is genuinely evaluated — which closes the "still
   unclear, should be tested per pattern" note in [Skin SDK](docs/Skin%20SDK.md). The panel
   surface is a **flat element list**: `<group>` renders nothing. And `<group class="...">`
   **crashes VirtualDJ** — twice, reproducibly enough to be worth a warning, mechanism unknown.

   What the loop cannot reach: the waveform family. A plugin panel has no deck, so
   `<scratchwave>` and the stacked-`<size condition="">` question in
   [Skin Waveforms](docs/Skin%20Waveforms.md) need a real deck skin as the fixture. That is the
   next skin task, and it is now a well-specified one.

Ergonomic note for whoever continues: **each capture costs a VirtualDJ restart**, because the
sweep runs at plugin load. Three restarts got the above. If iteration gets heavy, a watcher
thread re-sweeping when `probes.txt` changes would remove that — at the cost of calling the
host callbacks off the main thread, which is untested.

Revised 2026-08-11 after re-reading the full `IVdjCallbacks8` surface; the earlier framing of
this task ("faster verb prober") undersold it in one direction and oversold it in another, and
both are corrected below.

Landed 2026-08-15 — plan steps 1 and 2, minus the host:

- [tools/plugin/VDJIntrospect.cpp](tools/plugin/VDJIntrospect.cpp) builds and ad-hoc signs with
  **Command Line Tools `clang++` — Xcode is not required** (`just plugin-build --install`), and
  VirtualDJ carries `com.apple.security.cs.disable-library-validation`, so a self-signed bundle
  is loadable. It reads a probe list at load and records, per probe, both HRESULTs, the raw
  `double` with its bit pattern, and the text buffer. Read-only by construction: the source
  contains no `SendCommand` call at all.
- An offline harness with a fake `IVdjCallbacks8` proved the sweep, the JSON escaping (binary
  answers survive), the once-guard, and GUID negotiation. The python side
  ([tools/plugin_introspect.py](tools/plugin_introspect.py): `prepare`/`status`/`collect`/
  `--get`/`--check`, gated in `just check` with an explicit skip until the first capture)
  round-trips that harness capture.
- Untested is everything needing the host: whether VirtualDJ loads it, from which folder
  (`AutoStart` is the first guess; override with `VDJ_PLUGIN_SUBDIR=`), and via which IID. The
  plugin answers for both published IIDs and logs every `DllGetClassObject` call, so a failed
  load is still diagnosable — and that log is the evidence for the second-loading-path question
  in [docs/Plugin SDK.md](docs/Plugin%20SDK.md).
- Next step is manual: install, restart VirtualDJ, `just plugin-prepare`, restart,
  `just plugin-status`.

**What it is genuinely the only channel for.** These have no HTTP, Remote, binary or XML
equivalent — not a speedup, an access path that does not otherwise exist:

```cpp
HRESULT GetSongBuffer(int pos, int nb, short **buffer);   // PCM of the loaded song, any position
HRESULT OnProcessSamples(float *buffer, int nb);          // the live audio stream
void    OnKey(const char *ch, int vkey, int modifiers, int flag, int scancode);
bool    OnMouseDown/Up/Move(int x, int y, int buttons, int keyModifiers);
HRESULT GetTexture(EVdjVideoEngine, int deck, void **texture, TVertex **vertices);
HRESULT DrawDeck(int deck, TVertex *vertices);
HRESULT OnTransformPosition(double *songPos, double *videoPos, float *volume, float *srcVolume);
// plus VDJINTERFACE_SKIN: the plugin supplies skin XML at runtime
```

Mapped onto this repo's three standing cliffs:

- **Waveforms.** [docs/Skin Waveforms.md](docs/Skin%20Waveforms.md) is reverse-engineered from
  skin XML and observed rendering. `GetSongBuffer` returns the sample data VirtualDJ itself
  draws from, at arbitrary positions; `OnProcessSamples` gives the live stream. That is the
  input side of every `<scratchwave>` / `<blockwave>` / `<beattunnel>` question.
- **Mappers.** `OnKey` exposes VirtualDJ's own input model — virtual key, modifier mask,
  scancode, plus a `flag` that is a **candidate for press/release** (unverified; confirm from
  inside). `while_pressed` and the whole down/up half of the mapper contract are currently
  "not established" precisely because **HTTP has no press**. This is the first channel that
  might carry one.
- **Skins.** `VDJINTERFACE_SKIN` takes a skin XML buffer at runtime. Today, testing a skin
  hypothesis costs an edit-file-and-restart cycle; this makes it a loop, against a 2,600-line
  SDK doc with open `visibility` / `condition` questions.

Additionally, there is **no push channel anywhere else in the repo** — HTTP and Remote are both
pull-only from our side. `OnParameter(int id)`, `OnKey` and the sample callbacks are events,
which is the only way to observe *when* something changes rather than sampling for it.

**What it does for verb signatures specifically — a real but narrower win.**

```cpp
virtual HRESULT SendCommand(const char *command)=0;                            // execute
virtual HRESULT GetInfo(const char *command, double *result)=0;                // numeric query
virtual HRESULT GetStringInfo(const char *command, void *result, int size)=0;  // text query
```

- **The HRESULT is returned separately from the value.** HTTP collapses both into one response
  body, so any case where the status code carries information the value does not is invisible
  to us today. That is exactly the silent-fallback problem: `loaded opposite` and
  `loaded bogusword` return the same value over HTTP, but may differ in HRESULT. **This is the
  one place the plugin can discriminate a recognized keyword from an ignored one**, and it is
  worth an early experiment — but it is a hypothesis, not a known result.
- **Native types, no flattening.** Settles the `master_beat_num` float-bits defect in one call
  (core defect vs HTTP rendering), and calling both `GetInfo` and `GetStringInfo` per verb
  yields a definitive type-path map rather than one inferred from rendered strings.
- **Different prerequisites.** No Network Control plugin, no Pro license — a fifth Tier-1
  channel, which [docs/Evidence Standards.md](docs/Evidence%20Standards.md) already lists as
  planned and explicitly forbids claiming anything from until it exists.

**What it does NOT solve, stated plainly.** Throughput is not the bottleneck — the 2026-07-30
sweeps ran ~3,000 HTTP probes in minutes. And apart from the HRESULT channel above, argument
forms still need **prepared state** where forms would produce different values; a plugin
supplies no state a fixture harness cannot. See 10b, which is cheaper and should not wait on
this.

Plan:

1. Build the minimal plugin read-only: `GetInfo`/`GetStringInfo` sweeps only, **no
   `SendCommand`**, so loading it cannot change state. Execute-position testing comes later
   behind an explicit switch.
2. Emit the same artifact shape as the existing sweeps (`tests/…json` + a `just` query) so it
   joins `just get-verb` for free.
3. First experiments, in order: **the HRESULT discrimination test** (a known-good keyword vs a
   nonsense one on the same verb — if the codes differ, the entire 217-verb undocumented
   keyword queue becomes mechanically decidable, and that single result is what determines how
   much the plugin is worth); `master_beat_num` via `GetInfo`; the both-channels type map.
4. Then the cliff work, which is the larger prize: `GetSongBuffer` against a known file to
   ground [docs/Skin Waveforms.md](docs/Skin%20Waveforms.md); `OnKey` logging to establish the
   press/release model for [docs/Mapper XML.md](docs/Mapper%20XML.md).

Prerequisites and constraints:

- SDK headers are **not** vendored — no license grant exists. Fetch to `vendor/` (gitignored);
  see the `.gitignore` entry and [docs/Plugin SDK.md](docs/Plugin%20SDK.md).
- Xcode build, macOS arm64. The community examples build under Xcode 14.3 / macOS 13.3.
- Open question to resolve while building: the shipped `beatport16_vdj` bundle exports no
  `DllGetClassObject`, so a second loading path may exist. A built test plugin settles it.
- Also worth probing from inside: whether an *internal* verb-registration path exists, which
  is the one scope limit on Evidence Standards rule 1b.

Storage: **DONE (2026-07-30)** — `just get-verb <name>` joins the store record with the verb
table, the structural contract, the HTTP existence probe, and the observed return type at
read time (`--raw` for the bare record). Artifacts stay authoritative; nothing is copied into
the store, so a re-extraction is picked up without a migration.

Done when:

- Every query verb has an observed return type with the observing channel recorded.
- Every verb has an arg-forms record: observed forms, rejected forms, or `no-args`.
- Overloads (same verb, distinct arg shapes with distinct behavior) are recorded as such.
- The store's per-verb record surfaces all of it through `just get-verb`.

### 10b. State-fixture harness + argument prober (do this first — it is the cheap unblock)

Status: Ready

Note: **Steps 1-2 built and the first full sweep run 2026-09-02** (results below). Python
over the existing HTTP channel; no build toolchain, no SDK, no new evidence tier. Added
2026-08-11.

Step 1 shipped as [tools/fixtures.py](tools/fixtures.py) (`just fixtures`,
`just fixture-verify <name>`, `just fixture-establish <name>`): six named states —
`one_deck_loaded`, `both_decks_loaded`, `deck2_playing`, `loop_active`, `fx_slot_1_on`,
`sampler_slot_loaded` — each polling its own readbacks and raising `FixtureError` rather
than reporting a state it could not confirm. Fixture audio is generated locally with ffmpeg
(90 s, 120 BPM pulse train, cached under `~/Library/Caches/virtualdj-api-reference/`) so
results never depend on the user's collection, and teardown restores each deck to the
contents and transport state observed at establish time. `--check` validates definitions
offline, so `just check` stays hermetic.

Not yet done: `stems_active` needs a stem-capable fixture track and an analysis wait, so it
is deliberately absent rather than half-verified.

Step 2 shipped as [tools/probe_arg_forms.py](tools/probe_arg_forms.py)
(`just probe-arg-forms`, `just verb-arg-forms <name>`): 483 target verbs — the 300 that answer
bare while demanding an argument somewhere, plus every verb carrying recovered
`keyword_candidates` — probed as **token lists** (bare, each token alone, then all ordered
pairs: 835 single-token and 3,112 pair forms), inside each fixture, `/query` only. Two
unrelated nonsense controls run alongside every verb; they must agree with each other or the
reading is reported `unstable` rather than scored. A form is `recognized` only where it
separates from garbage in at least one state. Full sweep: 32,376 requests over 6 fixtures
(13,704 with `--no-pairs`).

**Run 2026-09-02** (`tests/verb-arg-forms.json`): 176 single-token tails confirmed across 89
verbs. The pair result needed the classifier fixed first — separating from nonsense is not
enough for a two-token form, since `is_using loop zzqqx` separates purely because `loop` does.
Comparing each pair against its own singles splits 763 apparent hits into 416 first-token-wins,
288 singles-agree, 51 beyond-singles and 5 last-token-wins, leaving **8 verbs with real
two-token grammar**, not the 62 first claimed.

`get_song_event` and `browsed_song` were then confirmed by direct query: the first takes
`[current|next] <field>` with the selector defaulting to `current`, the second is an exact-match
predicate `browsed_song <field> <value>` requiring both tokens. Both are documented in
[VDJScript Verbs](docs/VDJScript%20Verbs.md).

`get_cpu` and `is_using` are **disputed** — their two-token verdict flipped between independent
`--repeat 3` runs, `get_cpu` because its value drifts faster than repeat-agreement can catch and
`is_using` because `effect inaudible` depends on FX state the fixture does not pin. Two agreeing
runs is the guard that caught both; `--repeat` alone was not enough.

**Catalog + corpus extraction, 2026-09-03.** `Resources/languages.zip` is the source of the
official verbs-appendix prose — verified verbatim against the published page — so the appendix
is available offline and the repo had been reading that file for verb *names* only, discarding
816 descriptions. [tools/extract_action_catalog.py](tools/extract_action_catalog.py) now emits
them (`tests/action-catalog.json`), with the quoted parameters pulled out: 97 verbs document
parameters, 18 promise more than one argument.

The cross-check against the probe artifacts is the useful part, and it cuts three ways:
**16 verbs confirmed by both**, **90 documented but never probe-confirmed** (`auto_cue`
always/on/off, `display_time` elapsed/remain/total, `broadcast` direct/podcast/server/video …
— each one a state the fixtures never built, or an observable the probe could not see), and
**64 probe-confirmed but undocumented** (`browser_scroll` top/bottom/parent, `cue_display`
num/number, `action_deck` left/right …). The 90 are the immediate worklist: the meaning is
already written down, only the local confirmation is missing.

[tools/extract_script_corpus.py](tools/extract_script_corpus.py) collects the sanctioned
examples into `tests/vdjscript-corpus.json`: 1,390 snippets over 372 verbs, 269 quoted in
catalog descriptions and 1,131 from shipped Built-In XML, deduped with provenance on each.
Two provenance traps were fixed while building it — prose sentences beginning with a verb-like
word (`"Load saved loop named …"`) are excluded by requiring a lowercase first character, and
only `Built-In` trees are read, since `examples/Pads/Quarantine` and the repo's own skins would
otherwise let our test fixtures masquerade as vendor evidence.

**Catalog-driven probe run 2026-09-03** (`--from-catalog`: take each verb's candidates from the
catalog's own prose rather than the binary). 97 verbs, 196 single-token forms, read 2x in all
six fixtures. **27 verbs confirmed a documented parameter locally, 16 of them tokens no
previous sweep had found** — `display_time` elapsed/remain/total, `get_time` absolute/remain/
total, `loop_adjust` in/move/out, `sampler_mode` hold/stutter/unmute, `wheel_mode` jog/loop_in/
loop_move/loop_out, `param_cast` frac/ms/relative, `scratch_dna_option` drymix/quantized,
`auto_cue always`, `cross_assign thru`, `timecode_mode relative`, `get_vu_meter sampler`,
`effect_select audioonlyvisualisation`, `effect_select_multi video`. The catalog is a better
candidate source than the binary: it is written for these verbs, so its hit rate is far above a
generic lexicon's.

Cross-check moved from 16/90/64 to 26/81/64. The 81 that remain documented-but-unconfirmed are
mostly *contextual* — `broadcast` direct/podcast/server/video, `effect_arm_deck` aux/mic/sampler,
`automix_editor_movetrack` current/next/previous — states no fixture builds. Those need
fixtures, not more probing.

Fixed while doing this: `--merge` **replaced** a verb's forms with the incoming run's, so
merging a narrow re-probe over a broad sweep deleted measurements (950 recognized forms
collapsed to 535) and manufactured disputes for verbs whose pairs the new run never sent. It
now UNIONs form lists and disputes only a form both runs actually measured.

Still next: (1) fixtures for the contextual parameters — the count is
`just action-catalog --cross-check` → `documented_but_not_probe_confirmed`, not a figure to
quote; (2) mine corpus tails as a third independent source of argument forms; (3) use the corpus
as a parse-regression set for every grammar claim in
[VDJScript Grammar](docs/VDJScript%20Grammar.md). (2) and (3) have since landed.

**The worklist itself was wrong, and was repaired 2026-09-06 before more probing.** Three defects
in the catalog's parameter tokenizer, each distorting it in a different direction:

- **Nested quotes desynchronised the scanner.** In `'get time_min "absolute"'` the inner `"`
  closed the outer `'` span, so the scanner resumed mid-example and silently dropped the real
  parameters that followed. Single- and double-quoted spans are now scanned separately, which
  raised the verbs with documented parameters from 96 to **146** — fifty verbs whose documented
  vocabulary had never been visible to the cross-check at all.
- **The verb's own name came out as one of its parameters** (`browser_gotofolder`,
  `get_beat_num`, `loop`, `pad_page` …), because the catalog quotes whole examples.
- **Doc example names were treated as vocabulary to confirm** — `loop_load "myloop"`,
  `rack "unit1"`, `set "varname"`, `os2l_scene "myscene"`. These can never be confirmed. They now
  land in `documented_example_placeholders`, classified by absence from the binary's string pool,
  with two guards learned the hard way: a token any other source vouches for is never a
  placeholder (whole-string matching had called the real `sampler_mode` keywords `stutter` and
  `unmute` placeholders, since they only occur inside longer strings), and a signed token is
  stripped before the lookup (`browser_sort "+bpm"` is a real key wearing a direction prefix).

**Two new inputs so focused work stops being invisible.** A probe that writes its own artifact —
the known-position fixture proving `get_time cue1/loopin/loopout` — now feeds the cross-check, so
it stops listing settled tokens as unconfirmed. And a `documented_but_locally_refuted` bucket
holds tokens a local test measured behaving exactly like its nonsense controls, so nobody is sent
after them again.

**First worklist entries actually closed, same day.** The `get_time_*` family, probed on a fixture
paused at a known position with deck pitch at **+8.33%** so the pitched and unpitched timelines
differ: `elapsed`, `remain`, `total` and `absolute` all separate from two agreeing nonsense
controls on `get_time_sec` (32 / 50 / 23 / 55), corroborated on `_min` and `_ms`. `display_time`
returned exactly what both nonsense tokens returned on every variant — it was never a parameter,
only the setting named in prose, and it is refuted on all seven verbs that listed it.

That pitch also sharpened an earlier result: `get_time 'absolute'` returned **55000** where
`remain` returned 50769, and 55000 is exactly 90000 − 35000 — the remaining time on the
*unpitched* timeline. The known-position run could not separate the two because pitch was 0 there,
which is why `absolute` had looked merely equal to `remain`.

**Execute-position pass run 2026-09-03** ([tools/probe_execute_forms.py](tools/probe_execute_forms.py),
`just probe-execute-forms`, artifact `tests/verb-execute-forms.json`). Motivated by `deck all`:
32,376 queries could not see it because the query path collapses it to deck 1, and one execute
made it obvious. Method is two baselines per form — from `off` and from `on` — which is what
separates *set* from *flip* from *no-op*; from one baseline they are indistinguishable.

**Query-side entries closed 2026-09-07** (tracker: "Documented Parameters Taken Live
2026-09-07"): `get_loaded_song` album/title/artist/playcount, `get_key` harmonic,
`get_saved_loop` next (and the undocumented `len`, seconds), `get_pitch_zero` absolute, and
`get_date` as a strftime format string with the catalog's `format` reclassified as a
placeholder. Undiscriminated, not refuted, and needing a state no fixture builds:
`get_limiter` outputs (nothing playing), `get_time_sign` (never negative here),
`get_time_hour` (short track), `get_key musical` (keyDisplay already musical). Recorded in
`LOCAL_CONFIRMED` so the cross-check stops listing them. A second batch the same day added
`get_browsed_song` title/playcount/artist, `browsed_song` rating (a predicate in query
position), `sampler_loop` current, `get_time` to_lyrics; reclassified `get_version` 2026,
`get_text` title/on/off and `get_artist_before_feat` featuring as the doc's own words
(`LOCAL_PLACEHOLDERS`); and left `get_song_event`, `get_automix_song`, `get_slip_time`,
`filter_label`, `effects_used` undiscriminated — each returned E_FAIL or one constant on every
form in the state built, so they want a playing deck, an automix list, slip, or an active effect.
A third pass the same day used the `fx_slot_1_on` and `deck2_playing` fixtures: `get_song_event`
current/next and volume/hasbeats/remaining confirmed on a playing deck; the effect-name argument
confirmed on `effect_active`, `effect_select`, `effect_select_multi` with the loaded Phaser, and
the catalog's `flanger`/`echo` recorded as example names; level/VU/limiter tails still
undiscriminated because the meters read 0 on a playing deck in this setup (routing, not the
verb). Tracker: "Documented Parameters Taken Live 2026-09-07 (fixtures)".

**Corrected same day:** the pass reported `auto_bpm_transition`'s own candidates
(`source_original`, `target_original`, `target_current`) as behaving like junk, and this file
first recorded that as corroborating the query negative. The official verbs appendix documents
all three as parameters forcing which BPM the transition lands on — the probe's observable was
a boolean saying whether a transition is *running*, which cannot see which BPM it targets. The
appendix also documents `auto_bpm_transition_options 'stems' 'vocal'`, a two-token tail, which
independently confirms what `verb-arg-forms.json` found structurally. **Read
`tail-ignored-in-execute` as "not visible in this observable".** ~~Open task: re-test those three
with two decks at different BPMs, reading the resulting BPM over time.~~

**That open task is closed (2026-09-07)**, and it settled the reading above.
[tools/probe_bpm_transition.py](tools/probe_bpm_transition.py) (`just bpm-transition`, artifact
`tests/bpm-transition-forms.json`, gated in `just check`) builds the state no fixture has — a
100 BPM track on deck 1 against a 120 BPM track pitched to 132 on deck 2, both stopped, so
`source_original`/`target_original`/`target_current` are three distinct numbers — and reads
**where the pair of decks settles** instead of whether a transition is running. Two runs, order
reversed. `source_original` lands on 100 and `target_current` on 132, neither reachable by
anything else, so both are confirmed; `all` lands like `target_current` but disengages, where
`target_current` alone leaves the transition running. Bare and both nonsense controls land on
120, which is also where `target_original` lands: it **names the default**, so this observable
cannot separate it from an ignored tail — retested with `smart_play` off, same default — and it
stays on the worklist with the reason recorded rather than being called refuted. Two method
findings came out of it, both of which had corrupted a run first: the verb is a **toggle**, so a
form that leaves a transition engaged makes the next form stop it instead of starting one (the
prober now waits for disengagement and aborts if one will not stop), and a form that lands where
the deck already sits is stable from the first read, so the settle loop needs a minimum window.
Tracker: "`auto_bpm_transition`: The Observable Was Wrong, Not The Parameters".

Yield: the tail-handling rule is **verb-specific**, not universal. On 9 of 10 toggles a junk
tail suppresses the action entirely; on `auto_bpm_transition` it is ignored and the toggle
flips anyway. Only one token turned up that the query sweeps had missed —
`auto_bpm_transition all` — and it reads as the target keyword again, not verb vocabulary. The
verbs' own binary-recovered candidates behaved like junk in execute position too, so the query
sweep's negatives are corroborated rather than overturned.

**Two safety lessons, both worth keeping.** The first run aborted on `timecode_cd_mode`, which
went `on` and would not come back — `off`, `0`, bare toggle and deck-scoped forms all left it
`yes`. It is not in `settings.xml`, so it should be runtime-only and clear on restart; **verified
2026-09-07 — after a restart the query reads `no`**, recorded on the verb record. Still one-way
within a session: no form found here turns it off. It reached the probe because of a plain bug: `table.get(name)`
against an artifact shaped `{"summary":…, "verbs":{…}}` returns `None` for every verb, so the
**entire category deny-list was inert** — `timecode`, `browser`, `cues`, `database` were never
excluded and only the name and audible filters were doing any work. Fixed, and the tool now
exits if the table carries no categories rather than trusting it. Added since: a **pre-flight
round-trip** (flip once, put it back, skip the verb if it does not return — it caught four
verbs that ignore `on`/`off` entirely) and **partial results on abort**, because the first run
threw away 25 verbs of completed work when the exception escaped.

Next in this direction: the allowlist is deliberately tiny (18 verbs, settings-only, silent).
Widening it to the audible tier (`--include-audible`: faders, mics, playback) needs an instance
nobody is listening to, and widening past toggles/sliders needs a restore story for verbs whose
state is not a single readable value.

**Shared-lexicon pass run 2026-09-02** (`--lexicon`, 25 tokens proven real for more than one
verb, 215 candidate-less verbs, 5,375 forms read 2x per fixture). Yield: **`all` is a reserved
tail token on 22 verbs** — the whole sampler family plus `loop_load`, `loop_select`,
`load_skin`, `load_pulse`, `effect_stems`, `effect_dock_gui`, `apply_audio_config` — and
`wheel_mode` takes `browser`/`search`. What `all` *does* was answered on 2026-09-07, in the
`sampler_slots_differ` fixture that follow-up asked for: **`all` returns exactly the bare value in
query position and does nothing in execute position** on the two verbs whose state is readable and
restorable — `sampler_volume all 0.7` and `sampler_volume_nogroup all 0.3` moved nothing, where
`current` and a slot number both did. The `recognized` verdict was an artifact of how these verbs
fail: an unrecognized tail *errors*, so separation from a nonsense control is satisfied by any
token the parser accepts. **Where junk errors, separation from junk is evidence of parsing, not of
meaning** — the comparison that carries meaning there is against the *bare* form, which the
artifact already records as `same_as_bare_everywhere`. Not a claim about the other 24 verbs:
`sampler_stop all` is the shape that would mean "every slot", and confirming it needs samples
actually playing, which is audible and was not run. By-product, and worth more than the answer:
**`sampler_volume` is group-scoped** — `sampler_volume 1 0.5` moved all three `Drums` slots
together and left the ungrouped slot alone, where `sampler_volume_nogroup` moved exactly one.
Tracker: "`all`: Recognized By The Sweep, Inert Where It Was Tested".

The pass also needed a second guard. `record_vu` matched 24 of the 25 arbitrary tokens and
`pioneer_cue` 15 — a verb separating from nonsense on half a vocabulary that was not written for
it is drifting under the probe, not speaking. `_flag_undiscerning` now strips those (recorded in
`summary.undiscerning_verbs`), which is the same failure as `get_cpu` one level up: `--repeat`
catches a value that moves between two reads, this catches one that moves between a token read
and its control.

Candidate filtering is done, and the first version of it was wrong in an instructive way: "is
this token a suffix of some `ACTION_<verb>` symbol" is true of nearly every real keyword, since
verbs named `left`, `loop` and `top` all exist — it dropped 300 candidates including
probe-confirmed ones. The token has to reach back *into* the `ACTION_` prefix
(`len(token) > len(verb)`), which drops exactly the one real fragment, `TION_get_text`.

**Superseded — this said the sweep was unrun:** the write-side fixtures unload decks, and the machine's decks
were live. `tests/verb-arg-forms.json` does not exist yet; `--check` skips cleanly until it
does. Run it on an idle instance — the first real question it answers is whether any verb
accepts a two-token tail at all, which nothing to date has established.

**Pass 2026-09-08: pick entries by how they FAIL, not by verb family** (tracker:
"Documented Parameters, 2026-09-08"). One sweep of bare/`zzqqx`/`wubfar` over all 54 worklist
verbs sorts them by error code, and each group wants a different instrument: `E_NOTIMPL` on
both bare and tailed means no query implementation at all (11 verbs — an execute-position
question); `E_INVALIDARG` on both means query position rejects every form (5); error bare but
answering tailed means the tail is required (7); and **answering bare but `E_INVALIDARG`
tailed means the verb rejects what it does not know, so its vocabulary is enumerable by
acceptance** — which is the row nothing had used. For a token whose *meaning* the appendix
already states, parsing is the only missing half, so acceptance closes it.

Closed by that pass: `param_cast` absolute/relative (exact match, not prefix — `int` and
`percent` are accepted, `inte`/`perc` are not, and the digit format generalises past `000`);
`browser_sort`/`sideview_sort`, whose query position is a membership oracle that reads off a
**36-name sort-field enumeration** identical for both verbs, with one leading `+`/`-` and
case-insensitive matching; `get_slip_time` min/sec/msec, where the earlier `Fail` was the
wrong enabler — **`slip` and `slip_mode` are independent states** and only `slip` makes the
verb answer; `effect_arm_stem`, where the parameter tokenizer had read the quoted *slot* name
`stems` and missed the unquoted sentence listing the real vocabulary (vocal/instru/kick/
hihat/bass, all five confirmed, `+` combining with no surrounding space and conjunctive in
query position); `pitch <n> bpm`, a two-token execute form whose second token is required;
`effects_used master`; `loaded_song rating`; and `hot_cue` cue/cue_play/cue_stop moved to
placeholders, since the appendix sentence names *other buttons* being pressed.

That pass also added a third non-worklist bucket. `documented_but_names_the_default` holds
real vocabulary that **no state can separate**, because it selects what the verb does anyway
— `effects_used 'deck'` (bare *is* the deck scope, measured against a master-only effect),
`mixermode 'internal'`, `auto_bpm_transition 'target_original'`. They were being re-probed
every pass. Worklist 54 verbs / 97 tokens → 43 / 77.

Next buildable state, with the recipe worked out: **`get_time_hour` wants a track longer than
an hour.** Total 2h05m with the playhead at 1h10m makes `elapsed` 1, `remain` 0, `total` 2,
and reading it once with `display_time` on `elapsed` and once on `remain` (bare and junk
follow the setting) separates all three; `absolute` needs the playhead where pitched and
unpitched remaining time fall on opposite sides of an hour boundary, e.g. 3,700 s in at +12%.
Everything else left on the worklist needs a pad surface, an audio input, a broadcast
session, timecode hardware, or a meter that is not reading zero.

The blocker for argument forms is not the channel, it is **prepared state**. Unknown arguments
are silently ignored (`loaded bogusword` → `yes`), so a form can only be confirmed by comparing
values across forms **in a state where the forms would disagree**. `loaded opposite` is
meaningless with both decks empty — which is how the decks sat for most of 2026-07-30's
session, and why 301 optional-arg verbs are still unprobed.

Plan:

1. **Fixture layer.** Named states, each set up and torn down over HTTP execute, each asserting
   its own preconditions before probes run: `one_deck_loaded`, `both_decks_loaded`,
   `deck2_playing`, `loop_active`, `fx_slot_1_on`, `sampler_slot_loaded`, `stems_active`. Fail
   loudly if setup does not verify — a probe against an unestablished state is worse than none.
2. **Prober.** For each verb in `summary.optional_arg_queries` (301) crossed with its
   `keyword_candidates` (259 verbs, 217 undocumented), sample bare vs each keyword vs a
   nonsense control, in every fixture. Record: value-differs-from-bare, value-differs-from-
   nonsense-control. **The nonsense control is the whole design** — a keyword that behaves
   differently from garbage is recognized; one that matches garbage is not.
3. **Multiple tail tokens.** Nothing established so far says whether a verb accepts *more than
   one* token in its tail (`get_time short absolute`, `get_bpm absolute ghost`) — the
   `E_INVALIDARG` fingerprint only reports "demands an argument somewhere", and every probe run
   to date has been single-token. Add a cross-product pass over each verb's recovered
   `keyword_candidates`: bare, each token alone, each ordered pair, and a pair with one nonsense
   member. Four outcomes to distinguish per pair — both recognized, first wins, last wins, pair
   rejected entirely. Cheap to fold in here; expensive to retrofit once the artifact shape is
   fixed, so **design `verb-arg-forms.json` for a token list from the start, not a single
   `argument` string**.

   This matters more than it looks: `GetInfo(const char *command, …)` takes the whole command as
   **one string**, so there is no ABI-level parameter list anywhere — each `ACTION_` class parses
   its own tail. "Signature" for a VDJScript verb therefore means *the grammar of its tail*, and
   token count is the first unknown of that grammar.
4. Emit `tests/verb-arg-forms.json` in the existing artifact shape, gated in `just check`,
   joined by `just get-verb`.

Constraint: query position only. Execute-position confirmation is whitelist-only with
independent readback (rule 4), and never `system` / file / database verbs.

Done when the 217 undocumented keyword sets are each classified recognized / ignored /
state-dependent, with the fixture that decided it recorded alongside.

### 12. Mine Argument Tails From The Vendor Corpus

Status: Ready

Note: The cheapest source left — static extraction, no live VirtualDJ, no fixtures. Added
2026-09-03.

Measured before queueing: splitting every snippet in
[tests/vdjscript-corpus.json](tests/vdjscript-corpus.json) on `& ? : ( )` and reading the token
after each leading verb yields bare-word tails on **73 verbs**, of which **119 tokens across 50
verbs appear in neither [tests/verb-arg-forms.json](tests/verb-arg-forms.json) nor
[tests/action-catalog.json](tests/action-catalog.json)** — `browser_window folders|songs`,
`eq_mode frequency|stems`, `effect_arm_deck master|single`, `effect_stems vocal`,
`dump quantized|notquantized`, `effect_show_gui transition|audioonlyvisualisation`,
`cue_name active`.

These are attested by construction: Atomix shipped them in Built-In skins and pad pages, so the
parser accepts them. That makes the corpus a **third independent source** alongside the binary's
`keyword_candidates` and the catalog's prose, and it is the best remaining candidate list to feed
`probe_arg_forms.py` — the catalog scored 27 verbs from 97 where the generic lexicon scored 24
from 215, and a source written *for these verbs* is why.

Plan:

1. `--from-corpus` in [tools/probe_arg_forms.py](tools/probe_arg_forms.py), mirroring
   `--from-catalog`: candidates per verb taken from attested tails.
2. Record attestation in its own right. A tail in shipped XML is evidence *without* a probe: the
   probe can only separate a token from nonsense, and it is blind wherever no fixture
   discriminates. Emit `tests/attested-tails.json` with the snippet and file each token came
   from, so a token can be documented as attested even when unprobeable.
3. Then probe them, in fixtures, `--repeat 2`, and merge (the union-merge, so nothing is lost).

**Filter the known non-arguments first**, or the extraction will invent parameters. Already
visible in the sample: `dump while_pressed` is the statement suffix from
[VDJScript Grammar](docs/VDJScript%20Grammar.md), not an argument to `dump`. Same failure class
as the `TION_get_text` symbol fragment and the `"Load saved loop named …"` prose sentence — both
of which shipped before being caught. Exclude `while_pressed`, the unit suffixes, and anything
that is itself a verb name.

**DONE 2026-09-03.** [tools/extract_attested_tails.py](tools/extract_attested_tails.py)
(`just attested-tails`) emits `tests/attested-tails.json`: **154 tokens on 71 verbs, 116 of them
unknown to both other sources**, each carrying the snippet and shipped file it came from.
`probe_arg_forms.py --from-corpus` probes them; 33 verbs confirmed an attested tail locally and
**11 were newly confirmed** — `browser_window songs`, `effect_stems vocal`, `stem_pad vocal`,
`skin_panel audiomixer|defaultwave`, `get_next_karaoke_song artist|singer|title`,
`setting eqmode`, `pad_page btn1`, `cue_display name`, `effect_slider active`,
`get_sample_name active`, `color green`.

**Extended 2026-09-03 — a fourth corpus source and the tails' binary locations.** The app
binary compiles its own menu and toolbar scripts as `__cstring` literals; 83 statements pass
the statement filter in `extract_script_corpus.py`, 80 in no other source, and they add 22
attested tails on 15 verbs (`show_splitpanel effects|info`, `sideview clone`, `font_size big`,
`scratch_dna_option continue`, `browser_options le`) plus a real two-token form,
`sideview 'automix' 'blink'`. Locating every attested tail in the binary split them 52 in the
verb's own method / 67 shared / 66 absent — the shared ones are enumerations matched in
helpers, which is what §13 recovers.

**Shapes, 2026-09-03 — the first verb tried exposed the gap.** `fadeout` has two catalog
examples and two shipped ones, and every command answered "nothing": the catalog extractor's
quote regex rejected examples containing `&` or backticks, the tails extractor drops literals
by design, and the prober then declared the verb "needs no args". Measured: 114 verbs with
vendor examples had tails made only of values and were invisible to every source. Fixed three
ways — the catalog regex admits chains, ternaries and backticks (and bare example lines such
as `color 0.8 0.5 0.25` now enter the corpus); `attested-tails.json` carries `shapes` (410 on
262 verbs, 167 with no keyword tail; classes DUR/PCT/NUM/REL/STR/VAR/BOOL/KW/NAME, expressions reduced to their inner return type (`` `BOOL` ``, `EXP:NUM`), and
the `deck SEL EXP` wrapper unwrapped so inner verbs are shaped) with per-shape return evidence from the vendor's
attribute, the catalog prose and the bare-form sweep; and `verb-arg-forms` points at the
shapes. Confirming a shape live still needs a fixture.

**Shape probing landed 2026-09-06** as [tools/probe_arg_positions.py](tools/probe_arg_positions.py)
(`just probe-arg-positions`, `just verb-arg-positions <name>`), asking a better question than the
planned "`DUR DUR` against `DUR` and nonsense": hold the attested shape and vary ONE position
*within its own class*, so a changed answer means that position is read. Nonsense is still sent,
but only to separate "reads it" from "ignores everything here". Query-only; the baseline is
re-read last so a drifting verb is reported unstable rather than scored as reading everything.

37 verbs probed, 0 unstable, 8 read at least one position and **4 read one beyond the first** — a
class of fact no artifact here carried. The keeper is a pair with identical `NUM NUM` shapes:
`effect_slider_active` reads both slot and index, while **`effect_arm_slider` ignores its slot
position entirely** (slot 1 and slot 2 both return `0.73`, as does nonsense) and reads only the
index. Nothing short of varying the slot on its own would have shown that.
`get_effect_slider_label`, independently confirmed the same day, doubles as the method's
calibration. Full table: the tracker's "Argument Positions: A Question The Other Probers Cannot
Ask".

**Second keyword source landed 2026-09-09.** `probe_arg_positions.py` no longer takes its
keyword values from the attested tails alone: `--keywords` (default `attested,catalog`) adds the
vendor's own `documented_parameters`, minus the two buckets the catalog cross-check already
disowns — feeding a placeholder in would have made a keyword-vs-nonsense test wear the clothes of
a within-class comparison, which is the question the nonsense control already asks. **The
placeholder filter is a precondition, not a nicety**: with numpy missing, the catalog silently
reclassified 30 of the doc's own example names as vocabulary — and those are exactly the tokens
this now consumes. That is why `just install` and `just doctor` exist (README §Setup); the
extractor no longer swallows the ImportError that caused it.

Every value carries the source that supplied it, and `summary.reads_by_weakest_source` splits the
verdicts, because a `reads` earned between two attested tokens and one earned against a Tier-2
lead are not the same claim. `--plan` / `just probe-arg-positions-plan` reports what a run would
reach with no live instance at all, so coverage is measurable before VirtualDJ is up.

Measured 2026-09-09 with `--plan`: probeable verbs went 37 → 44 on `attested,catalog`, the seven
added being `auto_bpm_transition_options`, `automix_editor_movetrack`, `get_sample_info`, `padfx`,
`slicer`, `stem_pad`, `stems_split`; adding the opt-in `vocab` source reaches 48
(`cue_color`, `effect_stems`, `get_browsed_color`, `setting_setdefault`).

One verdict changed shape at the same time and it is the reason widening is safe: a variant and
the nonsense control that move the answer to the **same** value now score
`variant-indistinct-from-nonsense` rather than `reads`. A word that is real in position 2 can be
unknown in position 1, and an unknown word moves the answer exactly as a read one does; the old
three-way verdict could not see the difference and would have counted the widened sources as
discoveries.

**Run taken 2026-09-09 on build 18.0.9583, and it cost the prober three method changes.**
Full narrative: the tracker's "Argument Positions Re-Taken In Fixtures, 2026-09-09" and
"`blink`: The Prober Cannot See It". Headline: **44 verbs in 5 fixtures, 2 disqualified as
drifting, 6 read at least one position, 4 beyond the first**, each reproducing in four or five
independent states.

Three things the run established about the method, all of which cost a claim:

- **This machine is not the machine the earlier captures came from** — build 18.0.9583 against
  9598, and a different library. Fixtures pin deck, transport and FX state, and they pin the
  audio (generated locally, so no dependence on a collection); they do **not** pin the library.
  `get_next_karaoke_song`, `get_sample_info`, `padfx` and `automix_editor_movetrack` answer
  `no-answer` here because the sampler bank is empty and there is no karaoke content, not because
  anything was refuted. The artifact now carries `summary.build`.
- **Instability anywhere disqualifies a verb everywhere.** Merging only the steady states let each
  run keep whichever accident it saw; `blink` scored `reads` on a different position, in a
  different fixture, on each of three runs.
- **`stem_pad`'s position claim did not reproduce, and its token did.** `isolate` separates from
  nonsense in all five states, so it leaves `documented_but_not_probe_confirmed`; whether position
  1 is read depends on stem-pad state this method does not pin.

`blink` turned out to be the interesting one, and it is now `Pass` in the store. It is an
oscillator: both arguments are read (`DUR` → period, `PCT` → duty, the latter optional and
defaulting to ~50%), **and `DUR` takes beat units that lock to the master tempo** — `blink 1bt`
and `blink 500ms` measured 0.467 s and 0.495 s in the same run at 129.44 BPM. No comparison of
single reads can see any of that; a verb whose arguments parameterise behaviour over time needs a
waveform measurement, not a prober.

**Still next here**, in cost order:

1. **DONE 2026-09-09** — a sample went into slot 1, `sampler_slot_loaded` established, and the
   run covered all six fixtures. `get_sample_info` came out of it confirmed: position 2 reads
   (`group` vs `length`) in 6/6 states, from two **catalog**-sourced words, closing the verb this
   prober was written for. `padfx` and `automix_editor_movetrack` did NOT come with it — they want
   a pad context and the automix editor, not the sampler, and no fixture here offers either.
   **Next, and cheaper still: load a SECOND sample.** `get_sample_info` position 1 is
   undiscriminated only because slot 2 is empty, so slot 2 and nonsense answer alike. The karaoke
   verbs still need the original library.
2. **`automix_editor_movetrack` wants the execute prober, not this one** (2026-09-09). It is
   action-only — E_NOTIMPL invariant across editor open/closed, empty automix, and every
   documented form including the appendix's `'current' +10` — so no query-position work will ever
   reach it. `probe_execute_forms.py` is the right instrument, and it needs three things:
   the editor open, tracks in the automix, and a readback for track order. **The readback is
   found**: `get_automix_song '<field>' <n>` — field first, index second, 1-based from the NEXT
   song, verified against the Automix panel with six tracks loaded.
   `automix_editor_getselectedtrack`, `get_playlist_song` and `playlist_count` do NOT exist
   (`in_verb_table: false`); their E_FAIL was never evidence. So the only precondition left is
   the editor open (`automix_editor` reports and can set it). Also record the appendix's shape:
   the number is OPTIONAL ("can be mapped to rotary knobs or jog wheels"), so it is `KW [REL]`.
   The test writes to a live automix and moves what plays next, so it needs the user's say-so.
3. The opt-in `vocab` source reaches four more verbs — `cue_color`, `effect_stems`,
   `get_browsed_color`, `setting_setdefault`. Its members are Tier-2 leads, so a `reads` there
   rests on a word nothing has confirmed; `reads_by_weakest_source` keeps that apart, but decide
   deliberately before running with it.
4. **The prober captures one run and cannot see cross-run disagreement.** `stem_pad` scored
   `reads` in two of four runs on 2026-09-09 and `rejects-nonsense-only` in the other two, stable
   within each. `probe_arg_forms.py` has `--repeat` and a union merge; this one has neither, and
   until it does, a single capture's weakest rows (anything seen in one or two states) are leads.
5. Multi-token shapes still take the same keyword pair at every keyword position. Where a verb has
   four or more candidates, giving each position its own pair would separate "this position is
   read" from "this word belongs here".
6. **Both remaining instrument problems already have an instrument in this repo** (2026-09-09):
   - *Oscillators* (`blink`, and any verb whose arguments set a period, duty or rate) want the
     **Remote protocol subscription**, not polling. `tools/vdjremote_subscribe.py` takes arbitrary
     queries and prints every value VirtualDJ *pushes*, so an oscillator reports its own edges —
     exact period and duty, no aliasing, no polling load. It needs `tests/vdjremote-opener.bin`
     (present), a `dns-sd -R` advert, and Remote enabled in VirtualDJ, because VirtualDJ dials in
     as the TCP client. This supersedes "write a waveform prober".
   - *Sweeps* want the **introspection plugin** (task 10a). It is in-process, so the HTTP
     connection churn that wedged `/query` twice today does not exist, and it returns the
     **HRESULT separately from the value** — the "recognized keyword vs silently ignored" confound
     every nonsense control in this repo is a workaround for. **Rebuilt and re-captured on this
     machine 2026-09-09** (`just download-sdk` → `just plugin-build --install` → `just
     plugin-prepare` → restart → `just plugin-collect`), plus the delayed sweep in
     `tests/plugin-introspection-late-9583.json`.

     **But it is not the richer channel for every question.** Tested 2026-09-09 against ground
     truth: an empty field (`get_browsed_album`) and an unimplemented query
     (`automix_editor_movetrack`) are **byte-identical** on the plugin — E_INVALIDARG numeric,
     S_FALSE text, empty string — while HTTP separates them outright, returning an empty body for
     the first and `E_NOTIMPL` for the second. `GetInfo`/`GetStringInfo` are the query interface,
     and S_FALSE is its single word for both "no query here" and "nothing to say". The plugin's
     real edge remains keyword discrimination; for "does this verb answer queries at all", HTTP
     and the structural artifacts are better and cheaper. Tracker: "The Plugin Channel Does NOT
     Separate Empty From Unimplemented".

     That capture produced a method result worth carrying forward: **an absent channel is three
     different facts wearing one face** — a subsystem not yet up (comes back in the +40 s sweep,
     6 `get_browsed_folder*` verbs), an empty slot (differs between two load-time sweeps, the 11
     `get_effect_slider_*` label verbs), or an item with no such field (stable across both, and
     HTTP agrees — `get_browsed_album`, `get_browsed_genre`). Only the third is about the library.
     A single capture cannot tell them apart, so **always take the delayed sweep**, and check a
     suspected content-absence independently. Tracker: "Plugin Channel Re-Taken On A Second
     Machine".
7. **`DUR` is not one class.** `probe_arg_positions.py` varies a duration position between
   `1000ms` and `4000ms` — two values of the same unit. `blink` shows the *unit* selects the
   clock: `1bt` and `500ms` are both `DUR` and run off different ones. Any verb reading a duration
   may behave differently across units while looking identical across two values of one unit, so
   the pool wants a unit-crossing pair, and `attested-tails.json`'s `DUR` shape may be hiding two
   things.
8. **The prober picks its keyword pair blind.** `get_sample_info` proved the cost: its pair was
   (`group`, `length`), and `group` is empty on both loaded samples while `length` is `4bt` on
   both, so no comparison it could make would have separated the slots — while `bpm`, `key`,
   `title`, `filename` and `fullpath` all do. **A pair that both return the floor proves nothing,
   and nothing in the prober notices.** Reading each candidate once before choosing, and
   preferring a pair whose values differ, is the fix.

### 13. Probe The Shared Enumerations The Binary Serialises

Status: Ready

Note: 2026-09-03 — candidates extracted, fixtures exist, needs `just vdj-up`. **Two groups done
2026-09-06**, with opposite outcomes; the rest of the list below is still open. Full evidence:
the tracker's "Shared Enumerations: The Colour Table Confirmed, The Pad-Page Table Unreachable".

- **`colors`: confirmed, and cheaply.** `color '<name>'` resolves in *query* position — it echoes
  the canonical spelling for a recognized colour and returns `transparent` for anything else — so
  the whole group is classifiable read-only with a free floor. **24 of 26 members echo
  themselves**, 16 of them names no per-verb source knew. Three nonsense controls and a two-word
  control all returned `transparent`; `RED` returned `red`, so matching is case-insensitive.
  `none` and `reset` are **undiscriminated, not disproved**: they return `transparent`, which is
  itself a real member, so this observable cannot separate them from the floor. Group-level
  conclusion recorded: for `color`, the serialised table *is* the accepted vocabulary.
- **`pad_pages`: unreachable through `pad_page`, and this is the more instructive half.**
  `pad_page 'sampler'` and `pad_page 'cueloop'` both returned `true` and the query then reported
  that page as current — which looks like confirmation until the control runs.
  **`pad_page 'qzqzqz'` behaved identically.** The verb takes an arbitrary string and reports it
  back, so the 17 table names are undiscriminated *through this verb*, not unconfirmed by it.
  Confirming them needs an observable reflecting what a page contains, not what it is called.
- Also settled while the colour vocabulary was in hand: the sibling verbs do **not** share the
  resolver. `browsed_file_color` echoes any argument verbatim, nonsense included — it looks like a
  resolver and confirms nothing. `sampler_color` bare returns hex, not a name. `get_browsed_color`
  is stable over three runs but context-dependent and not interpretable in this state.

**Three more groups done 2026-09-08, and they sharpen the question.** Tracker: "Shared
Enumerations, 2026-09-08: Three Groups, One Pattern".

- **`song_fields`**: `get_loaded_song` and `get_browsed_song` accept exactly the same 16 of the
  41 members and reject the same 25, on two different tracks. The floor is unusually clean —
  a real but empty field returns `''` where an unknown one raises E_INVALIDARG — and `author`
  is an alias of `artist`. The 25 rejected members are visibly another consumer's vocabulary
  (RIFF chunk ids `iart`/`icmt`/…, two-letter forms `al`/`ar`/`ti`/…).
- **`audio_channels`**: `effect_arm_deck` reads four of fifteen — `master` (new; the catalog
  documents only aux/mic/sampler), `mic`, `sampler`, `aux`. The negative is directional rather
  than merely undiscriminated: in the `effect_armed` fixture bare and an ignored tail both read
  `yes` while a channel the verb actually reads must read `no`.
- **`settings_pages`**: the verb's vocabulary is the **dialog's tab list**, not the table —
  audio, broadcast, controllers, extensions, interface, licenses, options, record, tutorials.
  Four of those nine are absent from the serialised table and fourteen of the table's members
  are not accepted, so reading that table as the argument list would have produced fourteen
  wrong entries and missed four right ones.

**So the pattern to carry into the remaining groups: a serialised table is a table, not a
signature.** Each is shared by several consumers, every verb takes its own subset, and that
subset is not always contained in the table. A group-level conclusion must name which verb it
holds for. Two operational notes for the settings group specifically: opening the dialog stalls
the HTTP interface for several seconds (a timeout there is not a result), and it **cannot be
closed from script** — bare `settings`, `'close'` and `'off'` all return false — so budget a
GUI click for the way out before opening it.

[tests/binary-vocabularies.json](tests/binary-vocabularies.json) (`just binary-vocab`) holds
21 argument groups recovered as *structures* — pointer tables and switch functions — with
190 members no per-verb source names. The highest-yield leads, each already tied to a verb:

- `settings <page>`: 18 unprobed pages from a 19-entry table (`settings 'audio'` is attested).
- `color` / `get_loaded_song_color` / `cue_color`: 16 unprobed colour names from the 38-entry
  table — `beige`, `marine`, `violet`, `transparent`, `none`, `reset`.
- `effect_arm_deck` / `effect_fxsendreturndeck`: `booth auxin auxout mic2 preview samplerin
  timecode deckfxsend deckfxreturn` from the audio-channel switch.
- `browser_window`: the 17 root-folder names (`itunes`, `rekordbox`, `history`, `crates` …).
- `pad_page`: the 17 table names, several with spaces (`'loop roll'`, `'saved loops'`).
- `stem_pad instrumental`, `get_time cue`, `effect_show_gui` × 14.

Read first (added 2026-09-07): the named `CSettingEnum::unserialize`, `getActionParam` and
`setActionParam` on 18.0.9246 (`unserialize` at `0x10078a142` x86_64; re-resolve with `nm`)
walk the typed candidate values and conversion rules for the `settings` pages and other
enum-typed keys. Associate a default with a key only where the initializer does; a type name
alone is not a schema. Any persistent write in the live confirmation needs round-trip
restoration.

Probe with `probe_arg_forms.py` against nonsense controls in a discriminating fixture (colours
need a coloured track; settings pages need the dialog observable), `--repeat 2`, union-merge.
Record confirmations with `just put-verb`; record a group-level conclusion (the table IS the
vocabulary) in the tracker, since it does not reduce to one verb. Rule reminder: a member that
fails to separate is undiscriminated, not disproved.

The filters earned their place immediately: `dump while_pressed` is correctly gone while
`dump quantized|notquantized` survives.

`just action-catalog --cross-check` now reports a fourth column, `confirmed_by_all_three` — 8
verbs whose tokens are documented by the vendor, written by the vendor, *and* locally
reproduced (`crossfader_curve` cut/full/smooth, `loop_adjust` in/move/out, `is_using`
effect/equalizer/pads/sample, `get_time` remain/total). That is as settled as this project can
make a claim.

### 13b. Fixtures For The Documented-But-Unconfirmed Parameters

Status: Ready

Note: Needs a live instance — the expensive one of this group. Added 2026-09-03. **Three more
verbs closed 2026-09-06, and the premise needs qualifying**: two of the three were not waiting on
a fixture at all. Tracker: "Contextual Parameters: Three Verbs Off The Worklist, One Wall".

- **`get_sample_info`: all three documented fields confirmed** (`group` → `Drums`, `length` →
  `4bt`, `pos` → `00:00.0`), two nonsense controls returning `''`. **The obstacle was the argument
  SHAPE, not the state** — the form is slot-first, `get_sample_info <slot> <field>`, and a
  single-argument probe errors on every token including the real ones, so the sweep read the
  documented fields as indistinguishable from nonsense. The state had been there since
  `sampler_slots_differ` landed. This is exactly the failure task 12 predicted when it measured
  114 verbs whose vendor examples are value-shaped.
- **`get_saved_loop`: `length` and `name` confirmed** against two agreeing controls, on a fixture
  built and torn down (a 32-beat loop saved, then deleted with the deletion verified). `pos` is
  **undiscriminated** — it returns the right value but so do bare and both nonsense tokens, so it
  is the default. `next` is **out of context** rather than refuted: nothing upcoming to report.
- **`get_slip_time`: a wall.** E_FAIL in every form, bare included, with a track loaded,
  `slip_mode` on, playing, and the playhead jumped. Because the *bare* form errors, no token can
  separate, so the three documented units are untested rather than refuted.

**So before building a fixture for an entry, re-read its documented example for the shape.** The
count to work from is `just action-catalog --cross-check` →
`documented_but_not_probe_confirmed`, and it now excludes doc example placeholders, verb-name
self-references and locally refuted tokens.

`just action-catalog --cross-check` lists, under `documented_but_not_probe_confirmed`, the
verbs whose parameters the vendor documents and no local probe has confirmed. They are
overwhelmingly **contextual**, not wrong: `broadcast` direct/podcast/server/video,
`effect_arm_deck` aux/mic/sampler, `automix_editor_movetrack` current/next/previous,
`browser_move` top/bottom. The fixtures in [tools/fixtures.py](tools/fixtures.py) (`just
fixtures`) never build the state in which these would differ, so the probe reads them as
indistinguishable from nonsense and that verdict means nothing.

The meaning is already written down for every one of them, so this is confirmation work, not
discovery: each needs a state, then a re-probe with `--from-catalog --verbs <name>`.

Fixture candidates, cheapest first: `sideview_populated` (automix list, sidelist),
`browser_folder_deep` (a folder tree with a scrollable parent), `sampler_slots_differ` (several
slots loaded with *different* tracks — also settles what the sampler `all` means, still open from
2026-09-02), `effect_armed`, `broadcast_configured` (likely blocked: needs a server).

Each fixture must assert its own preconditions and fail loudly, per the rule the harness already
follows: a probe against an unestablished state is worse than none.

**PARTLY DONE 2026-09-03.** Two fixtures added, both **assert-only** — the shipped state already
satisfies them, so they write nothing and refuse to run if it is absent:

- `sampler_slots_differ` (slots 1-5 hold different samples, 6-8 empty) — settled what the
  sampler `all` means: **the selected slot**, not an aggregate. See
  [VDJScript Verbs](docs/VDJScript%20Verbs.md).
- `sideview_populated` (`file_count sideview` nonzero).

Re-probing all 97 catalog verbs across 8 fixtures added `get_time` cue1/loopin/loopout/
to_lyrics and more `param_cast` types, but the cross-check middle column did not move (81). The
new states simply are not the ones those 81 parameters need.

**It also exposed a drift verb.** In the 8-fixture run `get_time` tripped the undiscerning guard
— with a deck playing its value moves, so it separates from a control by noise, the `get_cpu`
pattern again. Its absolute/remain/total tokens stay recognized because the *catalog documents
them*, not because the probe is trustworthy here.

**Two more fixtures, 2026-09-03 (after the restart).** `effect_armed` (deck 1 loaded, slot 1
active, deck arm engaged — round-trip verified on `effect_arm_deck` before being written into a
fixture) and `browser_populated` (assert-only: it reads whatever the user is already browsing
rather than navigating somewhere it cannot return from). Re-probing all 97 catalog verbs across
**10 fixtures** confirmed `effect_arm_deck` aux/mic/sampler — one of the 81, and exactly the
kind of state-gated parameter the fixture was built for — plus `timecode_mode smart`.

Cross-check: **27 / 80 / 71**, with 9 verbs now confirmed by all three sources. The middle
column has moved only 90 → 80 across three fixture rounds, which is the honest measure of how
state-specific the remainder is.

Still to build: `broadcast_configured` (blocked — needs a server) and a karaoke fixture. The
**automix-list fixture landed 2026-09-07** as `automix_populated` (`playlist_add` in,
`playlist_clear` out) and brought one piece of harness with it: a fixture that restores by
*resetting* shared state rather than by putting back what it found now declares
`preconditions`, checked once before setup, and refuses to establish when they do not hold —
this one will not run unless the automix list is already empty. It refused for real during the
run. It did **not** unblock the verb it was built for: with the list demonstrably live
(`get_playlist_time` moving `error:1` → `04:30` → `09:01`), `get_automix_song` and
`get_automix_position` returned E_FAIL on every form including bare, because they want automix
actually *running*, which is audible. `get_playlist_time` is what the fixture confirmed. `browser_folder_deep` was deliberately *not* built: navigating the browser
tree has no verified way back, and an assert-only fixture that reads the user's current position
is worth more than a probe that leaves them somewhere else.

The rest of the 80 likely need an observable other than the verb's own value — the
`auto_bpm_transition` lesson. That is a different instrument, not another fixture.

**Confirmed, and made specific, 2026-09-07.** A pass that built *no* new fixture closed nine
verbs and then sorted what was left by the error code its **bare** query returns, which says
which instrument each remainder needs. Tracker: "Documented Parameters, 2026-09-07: Nine Verbs
Closed And A Triage Of The Rest".

- Closed with no state at all, because the verb *is* the state: `param_cast` — ten of thirteen
  types through a chained expression, including the documented `integer` 13 vs `int_trunc` 12
  split and the `text N` character limit — plus `param_equal` (a plain string compare, so its
  three "parameters" are the example's operands), `get_key musical` (by flipping `keyDisplay`
  rather than by building a deck state), `filter_label` name/clean (each in the knob position
  where it separates), and the sampler `siren` entries (the doc's example file; the NAME shape
  itself confirmed with a sample that is loaded).
- Closed by execute-with-readback and restored: `browser_window`, all six zones — with the
  structural by-product that `automix`, `sidelist` and `sampler` activate `sideview` as well,
  so they are panes inside it.
- Recognized where the floor is an error: `auto_cue` on/off, `cross_assign left`,
  `prelisten_output auto`, `search_options composer`, `show_splitpanel sideview`.
- **Ten of the remainder answer E_NOTIMPL to their own bare query** — `automix_editor_movetrack`,
  `browser_move`, `cue_color`, `effect_disable_all`, `effect_list_edit`, `invert_deck`,
  `karaoke_load`, `playlist_load`, `sidelist_load`, `stem_pad`. They have no query
  implementation at all, so no fixture can move them however good it is: they need execute plus
  an external observable. Three more (`get_automix_song`, `mix_and_load_next`, `padfx`) answer
  E_FAIL, which is the genuine fixture case; the fifteen that answer-but-cannot-discriminate are
  the rest of it.

Cross-check middle column: 80 → 56 across this session.

Two merge rules were fixed while doing this, both found by watching totals rather than by a
test: a re-probe must use a **superset** of the artifact's fixtures (a swapped fixture set
produces verdicts that are not comparable), and **separation is positive evidence while failure
to separate is not evidence of absence** — so a token recognized in any run stays recognized,
annotated `not_reproduced_in` when a later run's states could not show it. Taking the newer
verdict had silently deleted four confirmations.

### S1. Render-Test The Element-Specific Skin Attributes

Status: Ready

Note: Added 2026-09-08. [docs/Skin SDK.md](docs/Skin%20SDK.md) §"Element-Specific Attributes
Recovered From The Reader" landed with every row carrying its own Needs-test and **no Tier-1
evidence behind any of them**. The table is Tier 2 throughout: `tests/skin-classes.json`
establishes that a class references the name and which getter it reaches — presence, boolean,
string, or value comparison — which fixes the *shape* of each test but says nothing about
effect. Note also that the artifact's own `questions.Q2` records that class association includes
child-node and helper reads, so "read by this element's class" is an association, not an
outer-element schema; a canary is what settles which element actually accepts it.

Method is the one that worked twice already: `tests/Skins/clickthrough-probe/` and
`tests/Skins/reader-candidates-probe/` generate variants plus a nonsense control, load against a
live VirtualDJ, read the result, and run forward and reversed with identical rows both times.
Needs `just vdj-up`.

Read first: the Skin SDK section above; `just skin-classes --get CSkinPanel` (and `CSkinSlider`,
`CSkinTextGroup`, `CSkinVideo`) for each name's `attribute_reads` before designing its canary.

- The boolean-read pair is the cheapest start — the getter says boolean, so a two-value canary
  plus control is enough, and `clickthrough` proved the method on exactly that shape.
- The value-comparison one is the interesting case: shipped skins write both bare keywords and
  whole VDJScript actions in the same attribute, so the test is which values the reader compares
  and which fall through.
- The string-read rows each need a state where the value would visibly differ; the slider entry
  writes a query expression, so build the query true and false.
- **These no longer show up in `just element <name>`.** Documenting them moved every one out of
  the `!` column, so the tool will not remind anyone this work is outstanding — this task is the
  only record. Results go to the store (`just put-verb` does not apply; these are XML attributes)
  and to [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md), then
  the Skin SDK rows get their Needs-test replaced by the finding and a `Local test` label.

### S2. Triage The Reader Candidates No Shipped File Writes

Status: Ready

Note: Added 2026-09-08. `just skin-classes --unwritten` is the lead queue: attribute names the
bounded traversal recovered that **no shipped skin, pad, samplerbank or mapper writes**. This is
the `clickthrough` and `r` category — both were in exactly this position and both were later
confirmed by local test, so the list is not noise, and it is invisible to every corpus-based
method the repo has.

Two cheap desk filters before any live work, in this order:

1. **Cross-check against the docs.** A significant part of the queue is already written up in
   [docs/Skin SDK.md](docs/Skin%20SDK.md) — the shared-reader section names several. Filter those
   out with the same test `tools/element_summary.py` uses (`doc_mentions_attribute`) rather than
   by eye. Skipping this step is how a lead queue gets quoted as a discovery count; it happened
   on 2026-09-08 and the figure was wrong.
2. **Separate class-specific reads from inherited and child-node ones.** The artifact's
   `questions.Q2` states the overlap and `--unwritten` does not yet split it, so a name may be
   base-reader vocabulary appearing under every class. `attribute_reads` carries `function` and
   `scope` per read, so the projection exists in the data; see S3 if it is worth doing properly
   rather than per-query.

Only what survives both filters is worth a canary, and then it is S1's method. An unmatched or
unwritten name is not a rejected name — record negatives as negatives.

### S3. Give Recovered Attributes A Precision Field

Status: Conditional

Note: Added 2026-09-08. Trigger: S2 reaching step 2 and finding the per-query split too coarse
to work with. `tests/skin-classes.json` lists candidates per class, but the classes share a base
reader and the traversal follows helpers and child nodes, so a per-class list is not reliably
per-class — `just skin-classes --get CSkinPanel` returns names no `<panel>` in the shipped corpus
writes, several of which belong to other elements. The artifact says so in `questions.Q2` and
`tools/element_summary.py` was corrected on 2026-09-08 to call the flag a Tier-2 lead rather than
confirmed vocabulary.

The fix is a projection, not new analysis: `attribute_reads` already records `function` and
`scope` for every read, so each candidate can be labelled class-specific, inherited from the base
reader, or read on a child node. That would let `just element <name>` mark base-reader attributes
distinctly instead of folding them into the element's own, and would make S2 step 2 a filter
rather than a judgement call. Owner is whoever holds `tools/extract_skin_classes.py`; do not
re-run the binary traversal for it.

### H5. Establish remote parser mode through the `-remote` launch argument

Status: Ready

Note: Opened 2026-09-19 from a desk review after H4 closed with `remote-entry` as a named
limit. It was filed as `Parking lot` pending a second instance; the operator ran one the same
day and `-remote` worked on build 18.0.9628 (see "Observed" below), so the trigger fired. The
payoff is still narrow (Remote-skin authoring), so it sits after the per-verb work in queue
order. Steps 1 and 3 remain; step 2 is mostly answered. An agent never launches or drives a
second instance without the operator saying so in that session.

**What changed.** H4 recorded `IAction::isRemote` as untestable because nothing was known to
set it. A caller review on the unstripped 18.0.9246 x86_64 binary now supplies a candidate
switch. Everything in this block is a Tier-2 structural lead. None of it is behaviour.

- **The flag is a runtime static, not a build-time option.** Its writers and the `cmpb` in
  `IAction::create` are already captured in
  [tests/runtime-parser-branch-routes.json](tests/runtime-parser-branch-routes.json)
  (`remote_mode_writers`, `remote_entry`). A preprocessor constant would have left neither.
- **The desktop binary carries both Remote roles.** `CVDJRemote` is the host role
  (`uploadSkin`, `sendCues`, `sendFullWave`, `sendCover`, the `remotes` list).
  `CVDJRemoteClient` is the device role (`requestInit`, `activateQueries`, `getFakeDeck`,
  `requestSongPos`, `requestFolder`, and an `onMessage` handler that calls
  `CSkinEngine::changeSkin`). Every Remote-class writer of the flag is in `CVDJRemoteClient`.
- **So the flag marks the process that is acting as the Remote, not the host serving one.**
  This corrects the reading in the H4 limit record, which scoped the lead to "Remote-skin and
  skin-load contexts" without saying on which side. The consequence is practical: task 8
  observed this desktop connecting out to the phone as the host, so no probe through the
  host — HTTP, or a phone attached to this instance — can reach the remote route.
- **`-remote` starts the device role on the desktop.** A direct-call scan for
  `CVDJRemoteClient::start` (`0x100884028`) found two callers. `CMainWindow::handleCommandLine`
  (`[0x1003b9310, 0x1003b93c8)`) holds one string literal, `-remote`, and calls
  `CVDJRemoteClient::get` (`0x100883cbe`) then `start`. `ACTION_debug::onExecute`
  (`0x1002ca346`) reaches `getExisting`, `stop`, `start` under the literal
  `remote_init_status`; that restarts a client that already exists and does not create one.
  The scan covers E8 rel32 calls only, so indirect callers are not excluded.
- **Both literals are still present in the installed build.** `strings` finds `-remote` and
  `remote_init_status` in the arm64 and x86_64 slices of build 18.0.9628 (read 2026-09-19).
  A surviving string does not show that the code path is unchanged.
- **`Inference`, untested:** the checked heads that rejoin ordinary parsing are UI-local
  (`skin_panel`, `browser_zoom`, `font_size`, `skin_width`, `custom_button`, `load_skin`,
  `get_var`, `set_var`), which fits a device that runs those itself and wraps every other
  script as source text to send to the host.

**Observed 2026-09-19, build 18.0.9628 (`Local test`, operator-driven UI plus agent-read
system state).** Capture:
[tests/remote-mode-launch-initial-9628.json](tests/remote-mode-launch-initial-9628.json), with
the operator's screenshot under `tests/remote-mode-2026-09-19/`.

- The operator launched a second VirtualDJ with `-remote`, connected to it from the primary
  instance, and changed the Remote skin from the primary; the change took effect. The
  `-remote` instance is always fullscreen.
- Read independently while both ran: the second process carries the `-remote` argument,
  listens on `*:4243` and advertises `_vdjremote8._tcp`. The primary holds `*:80` and has an
  established connection **out** to port 4243 — the direction and port task 8 recorded with
  an iOS device.
- The device instance had no port-80 listener, but the host already held that port, so
  whether a device instance would serve HTTP on a free port is still open.
- **What this does not show:** that `IAction::isRemote` is set in that process (the flag is
  named only on b9246), or anything about how that process parses script. The b9246 lead and
  this observation agree; they are still separate claims.
- **What it gives the repo beyond H5:** a Remote-skin test bench with no phone, and both
  ends of the Remote protocol on one machine, where task 8 had to shim the phone side.

**Provenance gap.** The role listing and the caller scan were run ad hoc from an expanded
copy of `~/Downloads/install_virtualdj_2026_b9246_mac.pkg` and are not yet in any capture.
Until step 1 lands, cite this block as the lead, not as a recorded observation.

Work, in order:

1. **Persist the lead (desk).** Extend
   [tools/runtime_parser_branch_routes.py](tools/runtime_parser_branch_routes.py), which
   already scans direct callers for the evaluator helpers, to record the callers of
   `CVDJRemoteClient::start` and `::get` with the bounded, hashed `handleCommandLine` body
   and its literal. Then update the `remote-entry` limit in
   [tests/runtime-grammar-obligations.json](tests/runtime-grammar-obligations.json) —
   `scope`, `why_not_testable_now` and `unblock` — and the matching paragraph under
   "Named limits at H4 closure" in
   [docs/Runtime Argument Grammar Tests.md](docs/Runtime%20Argument%20Grammar%20Tests.md).
   The audit asserts the limit's fields, so keep their shape.
2. **Finish characterising `-remote` on the installed build.** Answered 2026-09-19: it
   starts the device role, advertises, accepts the host, and takes a skin change. Still open:
   how the host UI initiates the connection, whether the device instance reads or writes the
   shared settings folder, and whether it serves HTTP when port 80 is free. Operator-driven
   or operator-approved only; save screenshots under `tests/` beside the capture. The
   confirmed capture name `tests/remote-mode-launch-9628.json` is written by the run that
   answers these, not before.
3. **Build `parser_remote_mode`.** It needs an observable on the device side. HTTP on the
   device instance is unproven, so the likely observable is a Remote skin written for the
   purpose: `<text>` elements whose actions are the checked heads and their nonsense
   controls, read from screenshots of the fullscreen device instance. Pair the checked heads against
   nonsense controls in local and remote runs. Restoration is quitting the device instance;
   verify the host instance is unchanged afterwards.

Stop conditions: if `-remote` does not start the device role on the installed build, record
the negative with its build and leave the H4 limit standing. Do not run
`debug 'remote_init_status'` on the operator's instance; `debug` is outside every allowlist,
and "harmless without an existing client" is a reading of b9246, not a test.

Start here:

- [HISTORY.md](HISTORY.md#h4-runtime-argument-parsing-from-the-named-iactioncreate) — the closed H4 block and its limits
- `just runtime-grammar --audit` — the `remote-entry` obligation and its `limit` record
- [docs/Application Internals.md](docs/Application%20Internals.md) (Remote Skins) and task 8 in HISTORY.md — the observed transport

## Blocked Or Hardware-Gated

- Controller display helpers: `controllerscreen_deck`, `controller_battery`.
- Gemini display helper: `gemini_waveform_zoomlevel`.
- Phase helpers: `phase_movement`, `phase_position`, `phase_active`.
- Numark V7 helper: `v7_status`.
- Pioneer RZX helpers: `rzx_touch`, `rzx_touch_x`, `rzx_touch_y`.
- DJC-family helpers: `djc_shift`, `djc_button`, `djc_button_popup`, `djc_button_slider`, `djc_button_select`, `djc_panel`.
- Denon platter/display helper: `denon_platter`.

## Parking Lot

- **Crossfader-curve serialization format** (from the 2026-09-06 excavation): named
  `CSettingCrossfaderCustom::serialize`/`unserialize` survive on 18.0.9246. Recover a narrow
  format description only if configuration tooling ever needs it; validate with app-produced
  samples and isolated round trips. Serializer symbols alone establish nothing about delimiters
  or field meaning.
- **Category-index mapping for the historical x86_64 verb tables**: the older extractions carry
  category names but no index mapping, and none was guessed. Resolve only if a compatibility
  question needs per-category history; the current build's mapping is not evidence for them.
- **Plain-group `class` crash hypothesis** (H2): the recorded `<group class="…">` crash may be the
  plain-group construction path applying a template to no object. Test only with a disposable
  instance and a saved configuration, never on the operator's running app.
- **HTML reference export for humans** (requested 2026-07-29, deliberately deferred until the
  contract data exists): generate a static, browsable HTML reference from the verb store +
  verb table + contracts artifact — one page per verb plus category/alias indexes. Generation
  only, from the JSON stores (never hand-written HTML copies, same rule as Markdown); becomes
  worthwhile once task 10 gives the pages real content beyond names.
- `system`: revisit only if an official example, bundled-resource context, or clearly harmless parameter appears.
- Skin `visual type` canaries: **partly overtaken** (2026-08-22). The placeholder half is answered
  for a plugin-panel surface by the runtime-skin loop (task 10a) — starred is required, and works
  in conditions. What is left is the same canary run against a *real deck skin*, to say whether
  the plugin panel and a deck skin share the rule; the fixtures are ready in
  `tests/Skins/runtime-probe/`. Do that with the waveform questions, since both now want the same
  fixture.
