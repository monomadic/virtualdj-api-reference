# VDJScript Local Test Tracker

Focused manual-test log for verbs marked **Needs local test** in [Official VDJScript Coverage Audit](Official%20VDJScript%20Coverage%20Audit.md). Keep rows practical: one reproducible check, the VirtualDJ build, hardware/context, result, and any follow-up notes.

Result values: `Untested`, `Pass`, `Partial`, `Fail`, `N/A`.

## Evidence Snapshot

Last sparse-prose spot-check: 2026-05-21 against the [official VDJScript verbs appendix](https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html) and local official/published skin examples.

- Current coverage cross-check: the 2026-06-30 official appendix refresh parses to 991 official verb/alias names; `VDJScript Verbs.md` contains all 991, missing names are 0, and the compact official remainder is empty. The formal `Needs local test` gap is 19 official names: `system`, `dualdeckmode_decks`, and the 17 hardware-specific controller helpers below. `dualdeckmode_decks` now has a build-recorded pad-page observation, but still needs a dual-deck pair/controller-context repeat before promotion to `Pass`.
- `Untested` means behavior has not been observed in VirtualDJ locally, even if the verb is official.
- `Pass` means a specific VirtualDJ build, hardware/context, action, and observed result were recorded.
- `connect` has local skin evidence: [official Lite](../examples/Skins/Built-In/Lite/Lite.xml) uses `<button action="connect">`. Local testing on VirtualDJ `v2026-m b9336` confirmed action/query behavior for logged-in and logged-out states.
- `karaoke_venue_name` was locally tested on VirtualDJ `v2026-m b9336`; it returns blank when the karaoke venue name is empty and updates to the configured venue name from the Karaoke > Venue Name dialog.
- `system` was locally tested on VirtualDJ `v2026-m b9336`; in the sparse helper pad context it returned blank text and pressing it produced no visible UI or log result. This is still too sparse to promote beyond a conservative note. Do not infer `system` behavior from unrelated parameter values such as `get_vu_meter 'system'` or from `system_volume`.
- `open_stem_creator` was locally tested on VirtualDJ `v2026-m b9336`; pressing it opened the Stem Creator dialog. Treat it as a workflow opener, not a selected-track automation helper.
- `get_mixfx_active` was locally tested on VirtualDJ `v2026-m b9336`; in a pad-page text/query context, it mirrored `effect_mixfx_activate` off/on for Filter and Echo after a track was loaded.
- `deck_has_error` was locally tested on VirtualDJ `v2026-m b9336`; it stayed off for normal load/unload states, turned on after loading a deliberately missing file, scoped to deck 1 in the tested context, and cleared after a later successful selected-track load.
- `dualdeckmode_decks` has a local pad-page result on VirtualDJ `v2026-m b9336`: in the pad-page context it remained false/red for current and deck-scoped readbacks even after `dualdeckmode` toggled on; repeated on deck 2 with the same reported behavior.
- The VDJScript grammar battery ran on VirtualDJ `v2026-m b9482` (2026-07-14 log entry): trailing `&` chains bind to the ternary false branch, leading chains split off normally, nested ternaries associate standard, and backtick-computed arguments work for `set` but are ignored by `loop`, `beatjump`, and `phrase_sync`. Side findings: `beatjump` needs a signed argument (`+4` jumps, `4` is a no-op), and string values read back blank via `get_var` in pad labels.
- Controller-display, Phase, RZX, DJC, V7, Gemini, and Denon rows are hardware-dependent; keep them `Untested` unless the named target device or an equivalent controller mapping environment was used.

Suggested test order:

1. No-hardware sparse helpers: revisit `system` only if official examples or harmless parameters are found.
2. Optional controller/deck setup: repeat/expand `dualdeckmode_decks` with [Reference - Dual Deck Mode Test.xml](../tests/Pads/Reference%20-%20Dual%20Deck%20Mode%20Test.xml), especially in any context where dual-deck pair routing is visible.
3. Hardware-only batches: controller displays, Phase, RZX, DJC, V7, Gemini, Denon
4. Non-official Button Editor hidden probes: use [Reference - Hidden Button Editor Tests.xml](../tests/Pads/Reference%20-%20Hidden%20Button%20Editor%20Tests.xml), then record results in the dedicated hidden-candidate section below without promoting them to official guidance.

## Test Run Template

Before changing a row result from `Untested`, capture enough context to reproduce it:

```text
Date:
VirtualDJ build:
Test asset:
Account/deck/hardware state:
Steps:
Observed result:
Tracker rows updated:
Follow-up:
```

## Test Run Log

```text
Date: 2026-07-22
VirtualDJ build: 2026 (get_version)
Test asset: HTTP control interface (http://localhost/), tools/sweep_fx_introspection.py -> tests/fx-introspection-dump.json
Account/deck/hardware state: no hardware; interface enabled; sweep drives deck-FX slot 1
Steps: Pass A cycled effect_select 1 +1 until the name wrapped (enabled/favorites list). Pass B selected each documented catalog name plus every cycled name by name, using a 'Dump' sentinel park to detect non-loads, and read the introspection helpers (get_effect_name, get_effect_slider_count/button_count, effect_has_slider/button, get_effect_slider_label/label_full/name/text, get_effect_button_shortname) per position.
Observed result: 95 effects reachable into deck-FX slot 1 and fully mapped (slider/button counts, short+full labels, live value text); 63 of them are in the +1 cycle (enabled list), the rest are name-only. The +1 cycle is a SUBSET of installed effects: Reverb/Flanger/Phaser and others are absent from the cycle but selectable by name. Slot 1 also accepts VIDEO effects by name — `Blinds`, `Cube`, and `Camera` all load and report controls — so the 95 mix audio and video, and "reachable into slot 1" must not be read as "is an audio effect". Names that did not load at all: `BeatGrid` (wrong spelling; the installed selector name is `Beat Grid`), `Brake` (no spelling loaded), `Shader`. Their reason is unresolved — NOT "video-only", which the loading video effects above rule out; most likely not installed, or not the selector name. Spot-check reproduced the prior hand-built map exactly for Backspin, Flanger (incl. the LEN/Speed pair), Echo, Reverb, Beat Grid, and Cut, confirming the HTTP channel matches pad-fixture readback.
Tracker rows updated: FX introspection sweep (this entry)
Follow-up: Structural map (labels/counts) captured for all 95 in the dump and queryable via `just get-fx / find-fx / fx-stats`. NOT yet captured: normalized slider defaults (get_effect_slider_default) and reset-value text, which need a per-slider reset pass; and an audio-vs-video classification for the 95 (the sweep cannot currently tell them apart). No hand-transcription into Effects Engines.md — query the dump instead.
```

```text
Date: 2026-05-23
VirtualDJ build: v2026-m b9336
Test asset: Reference - Sparse Helper Tests.xml; shown in VirtualDJ as "Reference - Sparse Helper Tests"
Account/deck/hardware state: tested logged in and logged out; no dedicated hardware
Steps: load the sparse helper pad page, observe Pad 1, press Pad 1 while logged in, log out, observe Pad 1 again, press Pad 1 while logged out
Observed result: logged in shows green "CONNECT: on"; pressing opens a small menu with "Log out". Logged out shows red "CONNECT: off"; pressing opens the VirtualDJ CONNECT login dialog.
Tracker rows updated: connect
Follow-up: none for basic action/query behavior
```

```text
Date: 2026-05-23
VirtualDJ build: v2026-m b9336
Test asset: Reference - Sparse Helper Tests.xml; shown in VirtualDJ as "Reference - Sparse Helper Tests"
Account/deck/hardware state: no dedicated hardware
Steps: observe the purple KARAOKE pad with no venue set, press it to open the Karaoke menu, choose Venue Name, set a venue value, observe the pad label, clear the venue value, observe the pad label again
Observed result: empty venue shows "KARAOKE:" with no value. Pressing the pad opens the Karaoke menu with Venue Name. Setting the venue updates the pad label to include the configured venue name. Clearing the venue returns the label to "KARAOKE:".
Tracker rows updated: karaoke_venue_name
Follow-up: none for venue-name query and empty-state behavior
```

```text
Date: 2026-05-24
VirtualDJ build: v2026-m b9336
Test asset: Reference - Sparse Helper Tests.xml; shown in VirtualDJ as "Reference - Sparse Helper Tests"
Account/deck/hardware state: logged in; no dedicated hardware; tested with a browser track selected and with an empty browser result set
Steps: load the sparse helper pad page, observe Pad 3, press Pad 3, press Pad 4 with a browser track selected, close the opened dialog, filter the browser to 0 files, press Pad 4 again, close the dialog, then clear the browser filter
Observed result: Pad 3 showed "SYSTEM:" with no returned value from `system`; pressing it produced no visible UI change and no new Log Report entry. Pad 4 `open_stem_creator` opened the Stem Creator dialog with Bass, Kick (Drums), HiHat (Optional), Vocals (Optional), Instruments, Instru2 (Optional), Output, Headroom set to 6dB, and Create controls. The selected browser track was not auto-filled into the dialog. With 0 browser results, the same blank dialog opened. No export/create action was attempted.
Tracker rows updated: system, open_stem_creator
Follow-up: `system` remains too sparse to promote beyond the blank/no-visible-effect observation; `open_stem_creator` still needs separate testing for full stem-file creation, file-picker behavior, and license/build gating.
```

```text
Date: 2026-05-26
VirtualDJ build: v2026-m b9336
Test asset: Reference - Mix FX Query Test.xml; shown in VirtualDJ as "MIX FX QUERY TEST"
Account/deck/hardware state: no dedicated hardware; deck 1 loaded with a local browser track; selected Mix FX tested with Filter and Echo
Steps: load a track to deck 1, open the Mix FX query pad page, observe Filter selected with Mix FX inactive, press Pad 7 to toggle `effect_mixfx_activate` on/off, press Pad 6 to select Echo, then repeat the Pad 7 toggle and compare Pad 8 `` `get_mixfx_active` `` text/query/color against Pad 7.
Observed result: With Filter selected, Pad 8 showed "GET: off" when Pad 7 `effect_mixfx_activate` was off; pressing Pad 7 changed it to green "GET: on"; pressing Pad 7 again returned it to red "GET: off". After selecting Echo, direct and indirect Echo selected-state pads turned blue while Filter pads turned red, and Pad 8 again followed `effect_mixfx_activate` off/on. The page needed a loaded deck before the pad labels/state rendered clearly in the active skin.
Tracker rows updated: get_mixfx_active
Follow-up: repeat in a skin text/custom-button context if documenting non-pad surfaces, but pad text/query behavior is confirmed.
```

```text
Date: 2026-05-26
VirtualDJ build: user-provided local result, build not recorded
Test asset: User-provided pad XML fragment with two `FX-VOCALS` pads
Account/deck/hardware state: vocal stem FX slot available; exact deck/hardware state not recorded
Steps: create two pads that both call `effect_select_multi 'vocals'`, one for `echo out` and one for `reverb`; use `effect_active 'vocals' '<effect>'` as each pad query and action target
Observed result: Echo Out and Reverb light independently according to their selected/active effect state, while both play through the same `vocals` stem FX slot.
Tracker rows updated: effect_select_multi, effect_active
Follow-up: repeat on a recorded VirtualDJ build and add a minimal test pad page if this pattern becomes a canonical fixture.
```

```text
Date: 2026-05-26
VirtualDJ build: user-provided local result, build not recorded
Test asset: User-provided pad XML fragments for a vocal `padfx` chain
Account/deck/hardware state: vocal stem pad FX available; exact deck/hardware state not recorded
Steps: compare a pad that starts with `effect_disable_all 'padfx'` followed by `padfx 'echo out' ... 'stemfx:vocal'` and `padfx 'reverb' ... 'stemfx:vocal'` against the same pad without the inline `effect_disable_all`; then compare with other pads that use the same effect/stem targets with different parameter values.
Observed result: The inline `effect_disable_all 'padfx'` version did nothing visible and did not light; removing the inline clear made the chained pad FX work. Separate pads using the same effect/stem target can alter or "steal" one or more effects from another pad-FX chain by changing the active parameters.
Tracker rows updated: padfx, effect_disable_all
Follow-up: repeat on a recorded VirtualDJ build with a minimal fixture that logs visible pad state, `effects_used 'padfx'`, and audible behavior for same-event cleanup versus separate cleanup.
```

```text
Date: 2026-06-01
VirtualDJ build: user-provided local result, build not recorded
Test asset: Local FX slot/stem slot setup; `examples/Pads/FX-SLOTS.xml` is the nearest repo fixture
Account/deck/hardware state: normal deck FX slots and named stem FX slots available; exact deck/hardware state not recorded
Steps: load/select effects into FX1-FX8 and named stem FX slots such as `vocals` and `rhythm`; verify persistence across track loads/current session; close and reopen VirtualDJ; compare loaded effect names after restart
Observed result: FX1-FX6 kept their loaded effect across a VirtualDJ restart. FX7, FX8 and higher, plus named stem FX slots such as `vocals` and `rhythm`, kept their loaded effect during the current session and across track loads, but reset/cleared after restart. Working interpretation: FX1-FX6 behave like persistent rack state, while FX7+ and named stem FX slots behave like volatile performance state.
Tracker rows updated: effect_select, get_effect_name
Follow-up: repeat on a recorded VirtualDJ build and capture whether active state, slider values, and `effect_select_multi` contents follow the same persistence boundary.
```

```text
Date: 2026-06-08
VirtualDJ build: v2026-m b9336
Test asset: Reference - Deck Error Test.xml; shown in VirtualDJ as "REF: DECK ERROR TEST"
Account/deck/hardware state: no dedicated hardware; deck 1/current deck had a valid selected browser track available
Steps: load the deck error test page, load a valid track, observe state, press LOAD SEL, press UNLOAD, press LOAD MISS, then press LOAD SEL again.
Observed result: After the initial valid load, ERR was off, LOAD was on, D1ERR was off, and D2ERR was off. Pressing LOAD SEL caused no visible state change. After UNLOAD, ERR stayed off, LOAD turned off, and D1ERR/D2ERR stayed off. Pressing LOAD MISS turned ERR on/red, left LOAD off/gray, turned D1ERR on/red, and left D2ERR off/green. Pressing LOAD SEL with a valid selected track cleared ERR and D1ERR back off/green and set LOAD on/blue.
Tracker rows updated: deck_has_error
Follow-up: optional repeat from deck 2/current-deck context to further confirm scoped error behavior.
```

```text
Date: 2026-06-08
VirtualDJ build: v2026-m b9336
Test asset: Reference - Dual Deck Mode Test.xml; shown in VirtualDJ as "REF: DUAL DECKMODE TEST"
Account/deck/hardware state: no dedicated hardware; tested from deck 1/current context and repeated on deck 2
Steps: load the dual deck mode test page, observe MODE/CUR/D1-D4 states with dual-deck mode off, press MODE to toggle `dualdeckmode` on, then repeat from deck 2.
Observed result: With mode off, MODE was off/gray and CUR, D1, D2, D3, and D4 were false/red. Pressing MODE toggled MODE on/blue, but CUR and all deck-scoped `dualdeckmode_decks` pads stayed false/red. Repeating on deck 2 produced the same reported behavior.
Tracker rows updated: dualdeckmode_decks
Follow-up: test any deck layout/controller context where dual-deck pair routing is visibly active; current pad-page evidence suggests `dualdeckmode_decks` may not be a simple boolean query for "dual-deck mode is enabled."
```

```text
Date: 2026-06-08
VirtualDJ build: v2026-m b9336
Test asset: Reference - Hidden Button Editor Tests.xml; selector label "Reference - Hidden Button Editor Tests"; XML page name `REF: HIDDEN TAXONOMY TEST`
Account/deck/hardware state: no dedicated hardware
Steps: look for "Reference - Hidden Button Editor Tests" in the VirtualDJ pad-page selector.
Observed result: Page was not found in the pad-page selector during the user run. A later local filesystem check showed the XML installed at `~/Library/Application Support/VirtualDJ/Pads/Reference - Hidden Button Editor Tests.xml` with XML page name `REF: HIDDEN TAXONOMY TEST`, and repo pad lint passed. Follow-up testing confirmed VirtualDJ's selector uses the filename stem for local pad XML files rather than the XML `<page name="">` value.
Tracker rows updated: hidden Button Editor candidate probes
Follow-up: reload/restart VirtualDJ or recopy the XML, then look for selector label `Reference - Hidden Button Editor Tests`; if it still does not appear, inspect VirtualDJ logs/loading behavior for that pad file.
```

```text
Date: 2026-06-08
VirtualDJ build: v2026-m b9336
Test asset: Reference - Hidden Button Editor Tests.xml; shown in VirtualDJ as "Reference - Hidden Button Editor Tests"
Account/deck/hardware state: no dedicated hardware; deck/stems readiness not recorded
Steps: load the hidden Button Editor test page, observe Pads 1-3, press Pad 1 `stem_volume 'Vocal' 50%`, press Shift+Pad 1 debug readback, press Pad 2 `stem_volume 'Vocal' 100%`, then press Pad 3 `stem_volume 'Instru' 50%`.
Observed result: Initial labels/readbacks showed "VOC 50: 1", "VOC 100: 1", and "INSTRU 50: 1". Pressing Pad 1 produced no audible change and no pad-label change. Pressing Shift+Pad 1 opened a popup with text `` `stem_volume 'Vocal'` `` rather than an obvious evaluated value; no audible change and no label change followed. Pressing Pads 2 and 3 also produced no audible change and no pad-label change.
Tracker rows updated: stem_volume
Follow-up: repeat with a confirmed stems-ready loaded deck and visible stem controls; compare ordinary `stem 'vocal'` or `stem_pad 'vocal'` behavior in the same deck context before deciding whether `stem_volume` is nonfunctional, context-gated, or only a query/readback helper.
```

```text
Date: 2026-06-08
VirtualDJ build: v2026-m b9336
Test asset: Reference - FX Introspection Test.xml; shown in VirtualDJ as "REF: FX INTROSPECT"
Account/deck/hardware state: no dedicated hardware; Flanger loaded in deck FX slot 1
Steps: load the FX introspection page, load Flanger, and open the effect GUI.
Observed result: The Flanger GUI opened and displayed Strength 50%, Speed 8bt, Tone n/a, Feedback 50%, and LFO AMP 40%.
Tracker rows updated: effect_has_slider/effect_has_button/get_effect_slider_* probes, native effect parameter examples
Follow-up: press the count/label/text/default/name/shortname/button shift-log pads for Flanger, then repeat for Echo, Reverb, and BeatGrid to compare returned helper values against visible GUI controls.
```

```text
Date: 2026-07-05
VirtualDJ build: user-provided local result, build not recorded
Test asset: User-provided skin `<button>` with action `sync & phrase_sync <arg>`, driven by a global `$phrase_len` variable
Account/deck/hardware state: not recorded
Steps: compare a working clamped form against two interpolated forms that pass the variable value as the `phrase_sync` argument:
  1. sync & var_equal '$phrase_len' 16 ? phrase_sync 16 : phrase_sync 32   (clamped literal)
  2. sync & phrase_sync '`$phrase_len`'                                     (bare $var in backticks, quoted)
  3. sync & phrase_sync `get_var '$phrase_len'`                             (documented get_var query in backticks)
Observed result: Form 1 works and was kept. Form 3 (`phrase_sync `get_var '$phrase_len'`) did NOT work either, despite `get_var` being the documented way to read a variable value inside backticks. Form 2 also does not work as written. Working interpretation: `phrase_sync` does not accept a backtick-interpolated/computed argument in this context and requires a literal beat count; select the literal with a conditional instead.
Tracker rows updated: phrase_sync (see FX/Deck note below)
Follow-up: repeat on a recorded VirtualDJ build; test whether other numeric-argument action verbs (e.g. beatjump, loop) accept `` `get_var '...'` `` interpolation, to determine whether this is a `phrase_sync`-specific limit or a general rule that action arguments must be literals rather than backtick-substituted values. RESOLVED 2026-07-14: see the grammar battery entry below; the failure generalizes to `loop` and `beatjump`.
```

```text
Date: 2026-07-14
VirtualDJ build: v2026-m b9482
Test asset: Reference - Grammar Battery Test.xml; shown in VirtualDJ as "Reference - Grammar Battery Test"
Account/deck/hardware state: no dedicated hardware; A/B/C1/C3 ran with no track needed; deck 1 loaded and playing for C2/C4 and the literal control pads
Steps: pressed SETUP (pad 1) before every test pad, then read the blue result pads (a-b-c, r, dst, src/n); for C2/C4 compared against the yellow literal control pads on a playing deck. Mid-run fixture fixes: B1/B2 switched from string result codes ('X'/'Y'/'Z') to numeric codes (1/2/3) after string values displayed blank; the beatjump control pad switched to the signed form after unsigned `beatjump 4` proved to be a no-op; C4 switched to interpolating a stored '+4' string so the sign could not confound the backtick test.
Observed result:
  A1 (true cond, trailing & after false branch): a-b-c = 1-0-0. The trailing "& set c" did not run when the condition was true, so a trailing & chain binds inside the ternary false branch, not at statement level.
  A2 (false cond, same statement): a-b-c = 0-1-1. The false branch ran together with its trailing & chain. (A first press without SETUP read 1-1-1 from leftover A1 state; rerun cleanly after SETUP.)
  A3 (leading "set a &" then ternary, true cond): a-b-c = 1-1-0. The leading chain executed as its own statement and the ternary then evaluated independently.
  B1 (nested ternary, outer true / inner false): r = 2 ('Y'). Standard inner-binds-tightest nesting.
  B2 (nested ternary, outer false): r = 3 ('Z'). Standard nesting confirmed.
  C1 (set '$gb_dst' `get_var '$gb_src'`): dst = 42. `set` accepts a backtick-computed argument.
  C2 (loop `get_var '$gb_n'` with n=4 confirmed on the readout): no loop engaged; the literal `loop 4` control engaged a 4-beat loop on the same playing deck.
  C3 (get_var '$gb_src' & param_multiply 2 & set '$gb_dst'): dst = 84. Implicit param chaining works as the alternative pattern.
  C4 (beatjump `get_var '$gb_n'` with $gb_n set to the string '+4'): no jump; the literal `beatjump +4` control jumped on the same playing deck.
  Side findings: unsigned `beatjump 4` is a no-op on this build while `beatjump +4` jumps; string values written by `set` read back blank via `get_var` in pad labels, while numeric values display normally.
Tracker rows updated: phrase_sync follow-up (2026-07-05) resolved as a general rule, not verb-specific: `loop`, `beatjump`, and `phrase_sync` all ignore backtick-computed arguments even when the identical literal works, while `set` accepts them and param chaining works.
Follow-up: derived rules promoted to VDJScript Syntax Evidence.md and VirtualDJ Reference.md; optional later pass: map which other value-consumer verbs besides `set` accept backtick-computed arguments, and whether the signed-argument requirement applies to other relative-jump verbs.
```

```text
Date: 2026-07-14
VirtualDJ build: v2026-m b9482
Test asset: Reference - Grammar Battery Test.xml; shown in VirtualDJ as "Reference - Grammar Battery Test"
Account/deck/hardware state: no dedicated hardware; no track needed for A/B/C1/C3
Steps: pressed SETUP before each test pad, read blue result pads after each press
Observed result:
  SETUP: 000 (a-b-c) / r= / dst=0 / src=42 n=0
  A1 (true-cond trailing &): a-b-c = 1-0-0 -> a=1, b=0, c=0 - The trailing
  "& set '$gb_c' 1" did NOT run when the condition was true, so the trailing & chain
  binds inside the ternary false branch, not at statement level.
  Side note: SETUP sets $gb_r to 'none' but the r= pad displayed blank.
  A2 (false-cond trailing &): 0-1-1
Tracker rows updated: none yet (grammar evidence, not a verb row)
Follow-up: complete A2, A3, B1, B2, C1-C4; then promote derived precedence rules to
  VDJScript Syntax Evidence.md and VirtualDJ Reference.md
```

## Button Editor Hidden Candidate Probes

These rows are not official `Needs local test` rows. They track flag1-hidden Button Editor taxonomy candidates that are absent from the official appendix but have one or more local evidence streams: bundled language descriptions, compiled taxonomy placement, runtime strings, or exact `ACTION_*` method-symbol hints.

Do not promote these into ordinary user-facing verb guidance until a row has a concrete VirtualDJ build, setup, observed result, and notes. Use [Undocumented VDJScript Candidates](Undocumented%20VDJScript%20Candidates.md) as the evidence inventory, and use [Reference - Hidden Button Editor Tests.xml](../tests/Pads/Reference%20-%20Hidden%20Button%20Editor%20Tests.xml) for the low-risk pad probes.

| Candidate | Evidence | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `stem_volume` | `Built-in app resource`; `Binary compiled table`; no exact class. | Stem controls, pad text/actions, stems-ready deck. | Load a stems-ready track and the hidden taxonomy test page; compare Pads 1-3 and shift-pad readbacks for `stem_volume 'Vocal'` / `'Instru'` at 50% and 100%; compare against ordinary `stem 'vocal'` behavior and audible output. | v2026-m b9336 | None required | Partial | First run: Pads 1-3 read back `1`, but pressing `stem_volume 'Vocal' 50%`, `stem_volume 'Vocal' 100%`, and `stem_volume 'Instru' 50%` produced no audible or label change; Shift+Pad 1 opened a popup with literal-looking `` `stem_volume 'Vocal'` `` text. Repeat with confirmed stems-ready deck/visible stem controls before promoting or failing. The hidden language string lists `HiHat`, `Vocal`, `Instru`, `Bass`, `Kick`, `Melody`, `Rhythm`, and `MeloVocal`; keep `MeloRhythm` separate until observed for this hidden helper. |
| `sampler_inputgain` | `Built-in app resource`; `Binary compiled table`; exact `onExecute` / `onQuery`. | Hardware sampler input gain, sampler input path. | On the hidden taxonomy test page, observe Pad 4 and shift-pad 3 before/after `sampler_inputgain 50%`; if an input sampler path is available, compare audible/input gain. | TBD | Optional input path | Untested | May return a value even when no matching input path is active; record both readback and audible effect separately. |
| `get_pad_page_name` / `pad_page_insplit` / `pad_page_favorite` / `pad_page_split` | `Binary compiled table`; exact symbols for all; `pad_page_insplit` also has a language description; `get_pad_page_name` has public forum examples; `pad_page_favorite` has changelog/forum/published-skin evidence. | Pad-page state, split/favorite page UI. | Load the hidden taxonomy test page in normal pad mode and any split/favorite pad-page context; log shift pads 4-7 and observe Pad 6 query/color. For `pad_page_favorite`, also test action/query/text behavior across the current favorite slots and compare with `pad_page_favorite_select`. | TBD | None required | Untested | Good first pass for understanding split/favorite pad-page internals. Record selector label and XML `<page name="">` because local pad-page selectors use filename stems. |
| `pad_pressure_switch` | `Built-in app resource`; `Binary compiled table`; no exact class. | Pressure-capable pad controller mappings. | On pressure-capable hardware, bind a spare control to `pad_pressure_switch`, toggle it, and compare velocity/pressure-sensitive pad behavior. | TBD | Pressure-capable controller | Untested | Not included in the starter harness because no-hardware behavior may be meaningless. |
| `is_colorfx` / `effect_beats_sliderindex` | `Binary compiled table`; exact `onQuery` symbols. | Effect and ColorFX selected-state/readback. | On the hidden taxonomy test page, select a ColorFX and a normal deck FX with beat controls; observe Pad 7, Pad 8, and shift-pad 8 while changing effect selection and beat length. | TBD | None required | Untested | Low-risk query probes; useful if they expose ColorFX/beat-slider UI state more directly than documented helpers. |
| `flip_arm` / `flip_load` / `flip_loop` / `flip_play` / `flip_record` / `flip_get_status` | Language descriptions for most `flip_*`; exact symbols for `flip_get_status`, `flip_load`, `flip_play`, and `flip_record`. | Saved Flip / macro playback state. | Confirm Flip functionality is available; create or load a simple Flip, then use the hidden taxonomy test page param controls plus a custom button/log for `flip_get_status`; record state transitions for record, arm, load, loop, and play. | TBD | None required if Flip available | Untested | Keep separate from normal cue/macro docs until the feature state and licensing/build assumptions are clear. |
| `setting_if_unchanged` | `Community`; `Binary compiled table`; exact `onQuery`. | Settings/config change guards, skin `oninit` defaults. | Build a harmless throwaway-skin or custom-button probe around one known reversible setting; compare `setting_if_unchanged` before changing the setting, after changing it, and after restoring it. | TBD | None required | Untested | Public forum examples use it in action slots, while the exact symbol hint looks query-only. Verify action-slot behavior before documenting it as a defaulting helper. |
| `masterbpm` / `master_beat_num` | `Binary compiled table`; exact `onExecute` / `onQuery`. | Master deck BPM and beatgrid readback. | With two loaded decks and a known master deck, log both helpers while switching `masterdeck`, changing tempo, and moving across beatgrid positions; compare with `get_bpm`, `get_beat_num`, and visible master state. | TBD | None required | Untested | Promising for sync/master diagnostics, but not language-described. |
| `all_decks` / `combine_query` | `Binary compiled table`; exact `onExecute`, `onQuery`, `onQueryBool`, and `onQueryText`; `all_decks` is also a syntax-evidence test shape. | Query grammar, multi-deck combinators. | Start in custom buttons only: log bare readbacks, then test with tiny harmless boolean expressions if bare readback is accepted. | TBD | None required | Untested | Potential grammar-level helpers; do not use in pad fixtures until syntax and side effects are understood. A public LED thread shows `all_decks ? ...` as a user attempt, not as a validated pattern. |
| `remote_action` | `Official forum`; `Binary compiled table`; exact `onExecute`, `onQuery`, `onQueryBool`, and `onQueryText`. | VirtualDJ Remote skins; desktop-vs-remote action/variable state. | In a current Remote skin, create a Remote-local variable and a desktop variable/custom button with clear labels; compare direct Remote action/query against `remote_action "..."` for readback and action side effects. | TBD | Remote skin/device or simulator context | Untested | Staff/CTO posts say Remote custom buttons and variables are independent from desktop state and use `remote_action` for desktop-side actions. Keep this Remote-specific until a local Remote test records syntax and version behavior. |
| Hardware-only hidden candidates | `Built-in app resource` and/or exact symbols for `assign_related_controller`, `controllerscreen_action`, `motorwheel2`, `motorwheel3`, `ns7_get_drift`, `rane_motor_enable`, `rane_timecode`, `rane_timecode_enable`, `rane_screen_input`, `rane_screen_output`, `send_nothing`. | Matching controller, Rane screen/timecode, motorized platter, or controller-screen mapping context. | Test only with matching hardware or a known stock mapper context; record exact device, mapper, deck assignment, and observed display/motor/timecode behavior. | TBD | Required | Untested | Keep out of general docs unless hardware-specific behavior is reproduced. |

## Sampler

| Verb / Pattern | Why local test | Likely surface/context | Repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `sampler_loaded 8 'auto'` | Forum examples and older local examples use `"auto"`, but official docs only document fixed-slot `sampler_loaded 1`. | Pad XML sampler page with `sampler_pad_page`. | Load [Reference - Sampler Loaded Test.xml](../tests/Pads/Reference%20-%20Sampler%20Loaded%20Test.xml); use a bank with slot 8 loaded and slot 16 empty; switch to sampler page `9-16`. | 8.5.9307 / 18.0.9336 | None required | Fail | On page `9-16`, `sampler_loaded 8 'auto'` returned true while explicit `sampler_loaded 16` returned false. Treat `sampler_loaded` as absolute for empty-slot checks. |
| `sampler_loaded 8 auto` | Installed/public `Loop Recorder.xml` uses unquoted `auto`; check whether omitting quotes changes page-aware behavior. | Pad XML sampler page with `sampler_pad_page`. | Same diagnostic page; compare `AUTO8`, `AUTO8RAW`, `SLOT16`, and `AUTO16RAW` pads on page `9-16`. | 8.5.9307 / 18.0.9336 | None required | Fail | On page `9-16`, `sampler_loaded 8 auto` returned true while `sampler_loaded 16 auto` returned false. Unquoted `auto` matched quoted behavior and did not make `sampler_loaded 8` page-aware. |
| Read-only multi-page sampler guards | Need a page-aware sampler page that plays loaded samples but does not record or show slot-number fallbacks for empty slots. | Pad XML sampler page with `sampler_pad_page`, 8-pad and 16-pad controller layouts. | Load [SAMPLER READ ONLY.xml](../examples/Pads/SAMPLER%20READ%20ONLY.xml); use a bank with more than 8 presets; switch to page `9 to 16`; verify loaded slots show/play and empty slots stay blank/off/nothing. | 8.5.9307 / 18.0.9336 | XP2-style 16-pad layout observed | Pass | Working pattern: branch on text ranges like `"9 to 16"`, guard with absolute `sampler_loaded` slots, use `sampler_pad <visible-pad>` for loaded actions, `nothing` for empty actions, and `get_text ' '` for blank labels. Pads 9-16 map to the next eight visible sampler positions, so page `"9 to 16"` plus pad16 maps to slot 24. |

## Controller Display

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `controllerscreen_deck` | Sparse official prose; likely depends on controller screen routing and deck assignment. | Controller mapping with display-capable device; possibly screen page/action context. | Map a spare button/display action to `deck 1 controllerscreen_deck`, then repeat on deck 2 and observe whether the controller screen follows or reports the selected deck. | TBD | TBD | Untested | Official name only; needs display-capable controller context. |
| `controller_battery` | Hardware/environment dependent; useful only on devices that expose battery state. | Controller mapping, wireless/battery-capable controller display or LED feedback. | With a battery-capable controller connected, bind/display `` `controller_battery` `` and compare against the device/OS battery indicator while plugged and unplugged. | TBD | TBD | Untested | Official name only; requires battery-capable controller. |
| `gemini_waveform_zoomlevel` | Gemini-specific helper; behavior likely only visible on supported Gemini displays. | Gemini controller display/waveform mapping. | On supported Gemini hardware, bind `gemini_waveform_zoomlevel +1` and `-1`; verify waveform zoom changes and persists/display updates as expected. | TBD | TBD | Untested | Official name only; Gemini display helper. |

## Phase, RZX, DJC, And Hardware Helpers

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `phase_movement` | Phase-specific motion helper; no meaningful result without Phase hardware. | Phase controller/timecode-style deck mapping. | Connect Phase, load a track, display/log `` `phase_movement` `` while rotating and stopping the remote; record value range and idle behavior. | TBD | TBD | Untested | Official name only; requires Phase hardware. |
| `phase_position` | Phase-specific position helper; expected units/range need confirmation. | Phase controller display/query feedback. | Display/log `` `phase_position` `` while rotating slowly through one full turn; note wrap point, scale, and deck scoping. | TBD | TBD | Untested | Official name only; requires Phase hardware. |
| `phase_active` | Phase active-state helper; needs hardware and deck assignment confirmation. | Phase controller mapping or skin query. | Toggle Phase control/connection while displaying `` `phase_active` ``; confirm true/false states for connected, assigned, and disconnected cases. | TBD | TBD | Untested | Official name only; requires Phase hardware. |
| `v7_status` | Numark V7-specific helper; behavior depends on motor/display state. | Numark V7 mapping or status display. | On a V7, display/log `` `v7_status` `` while switching play, cue, platter touch, and motor states; capture observed status values. | TBD | TBD | Untested | Official name only; requires Numark V7. |
| `rzx_touch` | Pioneer RZX touchscreen helper; requires RZX touch surface. | Pioneer RZX mapping, touch/display context. | On RZX hardware, display/log `` `rzx_touch` `` while touching and releasing the screen; confirm boolean/timing behavior. | TBD | TBD | Untested | Official name only; requires Pioneer RZX. |
| `rzx_touch_x` | RZX-specific X coordinate helper; coordinate range is unknown locally. | Pioneer RZX touch/display mapping. | Touch left, center, and right of the RZX screen while logging `` `rzx_touch_x` ``; record min/max and origin. | TBD | TBD | Untested | Official name only; requires Pioneer RZX. |
| `rzx_touch_y` | RZX-specific Y coordinate helper; coordinate range is unknown locally. | Pioneer RZX touch/display mapping. | Touch top, center, and bottom of the RZX screen while logging `` `rzx_touch_y` ``; record min/max and origin. | TBD | TBD | Untested | Official name only; requires Pioneer RZX. |
| `djc_shift` | DJC-family helper; shift behavior may be controller/mapping specific. | DJC controller mapping. | On supported DJC hardware, bind/display `` `djc_shift` `` and press/release the hardware shift; confirm scope and latch/hold behavior. | TBD | TBD | Untested | Official name only; requires matching DJC-family context. |
| `djc_button` | DJC-family button helper; argument/value behavior is sparse. | DJC controller mapping/button feedback. | Bind `djc_button` to a test control and observe UI/LED/display response; repeat with likely button indexes if the mapping exposes them. | TBD | TBD | Untested | Official name only; requires matching DJC-family context. |
| `djc_button_popup` | DJC popup helper; expected popup/menu target needs confirmation. | DJC controller mapping with screen/menu controls. | Trigger `djc_button_popup` from a spare mapping button; note whether it opens a menu, affects a selected DJC button, or requires parameters. | TBD | TBD | Untested | Official name only; requires matching DJC-family context. |
| `djc_button_slider` | DJC slider-button helper; hardware control semantics need confirmation. | DJC controller mapping with slider/button controls. | Bind `djc_button_slider` to an encoder/slider test control and observe any display or selection changes. | TBD | TBD | Untested | Official name only; requires matching DJC-family context. |
| `djc_button_select` | DJC selection helper; likely navigates or commits a hardware-menu choice. | DJC controller mapping/menu context. | Open any DJC-related menu/popup, trigger `djc_button_select`, and record whether it selects, cycles, or toggles an item. | TBD | TBD | Untested | Official name only; requires matching DJC-family context. |
| `djc_panel` | DJC panel helper; target panel names/states are not locally verified. | DJC controller display/panel mapping. | Trigger `djc_panel` from a spare button and, if needed, try known panel identifiers from the stock mapping; record visible panel changes. | TBD | TBD | Untested | Official name only; requires matching DJC-family context. |
| `denon_platter` | Denon-specific platter action/helper; platter LED/display behavior depends on device family. | Denon controller/player mapping; platter display feedback. | On supported Denon hardware, bind `denon_platter` and compare with `` `get_denon_platter` `` while playing, cueing, scratching, and changing deck assignment. | TBD | TBD | Untested | Official name only; requires Denon platter/display hardware. |

## System And Config Helpers

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `connect` | Official skins use it, but action/query behavior varies by account connection state. | Skin button, custom button, config/account UI. | Test logged out and logged in: run `connect`, then display/query `` `connect` `` if accepted; record opened UI and returned state. | v2026-m b9336 | None required | Pass | Logged in: green `CONNECT: on`; pressing opens menu with `Log out`. Logged out: red `CONNECT: off`; pressing opens CONNECT login dialog. |
| `system` | Sparse official system helper; parameters and return behavior are unclear. | Custom button, skin query/text, possible system integration context. | Run `system` with no parameter in a custom button; then try a harmless known/obvious parameter only if official examples are found; record UI/log output. | v2026-m b9336 | None required | Partial | In the sparse helper pad context, `` `system` `` returned blank text and pressing `system` produced no visible UI change or new Log Report entry. Still too sparse to promote beyond a conservative note; do not infer from `system_volume` or system VU labels. |
| `open_stem_creator` | Opens a workflow that may depend on license/build/stem features. | Skin/custom button, config/workflow action. | Run `open_stem_creator` with a track selected and with no track selected; note opened window, gating, and any error/status message. | v2026-m b9336 | None required | Pass | Pressing it opened the Stem Creator dialog with per-stem input pickers, Output, Headroom, and Create controls. A selected browser track did not auto-fill; 0 browser results opened the same blank dialog. Full export/create and license gating not tested. |

## FX Helpers

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `effect_has_slider` / `effect_has_button` and `get_effect_slider_*` / `get_effect_button_*` | Built-in skins use these heavily, but the exact return shapes and context scoping need a focused local fixture. | Skin controls, pad text/query, custom button display; deck FX, video FX, transition FX. | Load [Reference - FX Introspection Test.xml](../tests/Pads/Reference%20-%20FX%20Introspection%20Test.xml), press each LOAD pad, observe slider/button counts, labels, defaults, text, and `effect_has_*` states; read Shift-layer pads 5-14 (exact strings via `name=`); repeat separately for `video` and `transition` targets. | v2026-m b9482 | None required | Pass | Deck FX slot 1, Backspin (2 sliders / 0 buttons). Reliable and GUI-matching: `get_effect_name`=`Backspin`; `get_effect_slider_count`=2, `get_effect_button_count`=0; `effect_has_slider`/`effect_has_button` lit correctly per position; `get_effect_slider_text`=`0%`/`4 bt` (matches GUI values). Label family splits: `get_effect_slider_label`=`get_effect_slider_shortname`=`STR` (short), while `get_effect_slider_label_full`=`get_effect_slider_name`=`Strength` (full, matches GUI). `get_effect_slider_default` has two working forms (resolved by a follow-up probe plus shipped-skin evidence): the effect-name form `get_effect_slider_default 'Backspin' 1` returned `0.5` — a genuine normalized 0-1 default, distinct from the current `0%`, and not the trailing `1` (which is a fallback, not a slider index). The slot form `get_effect_slider_default 1 1 0.5` returned `off` in the same pad `name=` text context. Built-in skins ship both: deck skins use `<slot> <index> <fallback>` 300+ times inside `<slider frommiddle=…>` (numeric-value) contexts, and the Broadcast video skin uses the effect-name form `frommiddle="get_effect_slider_default 'active' 0.5"` — where `0.5` is the fallback — confirming the target-name signature (`examples/VideoSkins/Built-In/broadcast/broadcast.xml:241`). So the slot form is context-sensitive, not broken; my initial "broken" conclusion was a wrong-argument call (slot `1` passed where the form wanted a target name). Separate finding: `debug` logs the literal backtick expression instead of evaluating it (same computed-argument behavior as loop/beatjump/phrase_sync), so exact strings must be read via `name=` interpolation. **Follow-up sweep (VirtualDJ 2026, HTTP interface, 2026-07-22):** every one of these helpers accepts an effect *name* where the docs show a slot number — `get_effect_slider_count 'Echo'`, `get_effect_slider_default 'Echo' 3` — returning the same values as the slot form for all 119 title-resolvable effects, with no `effect_select` and no state change. That makes introspecting an effect you have not loaded a read-only operation. `get_effect_title '<name>'` returns `'<Canonical> - Deck N'` or `''`, so it resolves names and probes existence (case-insensitive, not space-insensitive; blind to `Stems`/`Vocals`, which still introspect through a slot). The `*_skip_length` variants **re-index** rather than blank: index *i* is the *i*-th slider of the list with the length slider removed, so the last index is always empty — verified on all 47 length-bearing effects, where the length slider is not always index 2 (`Loop Out`, `Slideshow` put it first) and not always labelled `LEN` (`Phaser`, `Wahwah` label it `SPD`). |
| Native effect parameter examples | Existing pad pages provide working presets, but the repo does not yet have a systematic effect-by-effect slider/button map. | Pad XML and skin/custom button controls for selected native effects. | Use [Reference - FX Introspection Test.xml](../tests/Pads/Reference%20-%20FX%20Introspection%20Test.xml) as a starter fixture; for each native effect, load it in slot 1, record counts, labels, defaults, button count, and tested `effect_slider`/`padfx` presets with VirtualDJ build/effect version. | v2026-m b9482; full pass TBD | None required | Partial | Per-effect map (deck FX slot 1, v2026-m b9482) started in `docs/Effects Engines.md`: **Backspin** — 2 sliders, 0 buttons: S1 `Strength`/`STR` (%, e.g. `0%`), S2 `Length`/`LEN` (beats, e.g. `4 bt`). **Flanger** — 4 sliders, 2 buttons: S1 `Strength`/`STR` (`50%` reset), S2 `Speed`/`LEN` (`8 bt` reset), S3 `Feedback`/`FBCK` (`50%` reset), S4 `LFO Amp`/`LFO` (`50%` reset); B1 `Tone`/`TONE`, B2 `Phase`/`PHASE`. **Echo** — 6 sliders, 4 buttons: S1 `Strength`/`STR` (`52%` reset), S2 `Length`/`LEN` (`1/2 bt` reset), S3 `Feedback`/`FB` (`52%` reset), S4 `Filter`/`FILT` (`OFF` reset), S5 `Lowpass`/`LP` (`20 Hz` reset), S6 `Highpass`/`HP` (`20000 Hz` reset); B1 `Reverse`/`REV`, B2 `Freeze`/`FRZ`, B3 `Mute Source`/`MUTE`, B4 `Lock On Max`/`LCK`. **Reverb** — 4 sliders, 2 buttons: S1 `Strength`/`STR` (`50%` reset), S2 `Decay`/`DEC` (`50%` reset), S3 `Room Size`/`SIZE` (`50%` reset), S4 `Brightness`/`BRI` (`50.0%` reset); B1 `Low Cut`/`LOW`, B2 `Hi Cut`/`HI`. **Beat Grid** — 1 slider, 2 buttons: S1 `Slot`/`SLOT` (`Slot 1` reset); B1 `Mode`/`>>`, B2 `Video`/`VIDEO`. Reset changed the slot readback from `Slot 3` to `Slot 1`; the GUI showed the mode choices as `SNGL` and `CONT`. The canonical selector is `'Beat Grid'`: the earlier `'BeatGrid'` loader left the previous effect selected, so affected fixtures/examples were corrected. **Beat Brake** — 4 sliders, 1 button: S1 `Strength`/`STR` (`50%` reset), S2 `Pattern`/`PAT` (`Pat 1` reset), S3 `Bars`/`BARS` (`2 bars` reset), S4 `HPF`/`HPF` (`Off` reset); B1 `Quantize`/`QUANT`. **BrakeStart** — 1 slider, 1 button: S1 `Length`/`LEN` (`2.76 s` reset); B1 `Restart Play`/`RESTART`. The live name corrected the stale catalog spelling `Break Start`. **Choppa** — 3 sliders, 1 button: S1 `Strength`/`STR` (`100%` reset), S2 `Length`/`LEN` (`Pat 1` reset), S3 `Invert`/`INV` (`Off` reset); B1 `Quantize`/`QUANT`. **Cut** — 4 sliders, 4 buttons: S1 `Strength`/`STR` (`52%` reset), S2 `Length`/`LEN` (`1/2 bt` reset), S3 `Duty`/`DUTY` (`50%` reset), S4 `Swing`/`SWING` (`0%` reset); B1 `Low Cut`/`LOW`, B2 `High Cut`/`HIGH`, B3 `Mute Beats`/`INV`, B4 `Video`/`VIDEO`. **Cyclone** — 3 sliders, 0 buttons: S1 `Strength`/`STR` (`50%` reset), S2 `Length`/`LEN` (`1/2 bt` reset), S3 `Delay`/`DELAY` (`203 ms` reset). **Delay** — 4 sliders, 2 buttons: S1 `Strength`/`STR` (`52%` reset), S2 `Length`/`LEN` (`1/2 bt` reset), S3 `Swing`/`SWING` (`0%` reset), S4 `LR Ratio`/`LR` (`0%` reset); B1 `Low Cut`/`LC`, B2 `High Cut`/`HC`. Counts and `effect_has_*` positions matched the visible controls. The by-name default pad remained hardcoded to Backspin, so its `0.5` was excluded for the other effects. **Superseded by the full sweep (VirtualDJ 2026, HTTP interface, 2026-07-22):** [tools/sweep_fx_introspection.py](../tools/sweep_fx_introspection.py) captured counts, short+full labels, normalized defaults, live value text, and length/beats flags for all **119** installed effects into [tests/fx-introspection-dump.json](../tests/fx-introspection-dump.json). Query it with `just get-fx <effect>` / `just find-fx` rather than reading either the dump or the prose above; the hand-written entries here are kept only as the provenance of the original method. Spot-checked identical to the hand map. |
| `get_mixfx_active` | Official sparse Mix FX helper; return value and relationship to `effect_mixfx_activate` needed confirmation. | Skin text/query, pad query/color, custom button display. | Load [Reference - Mix FX Query Test.xml](../tests/Pads/Reference%20-%20Mix%20FX%20Query%20Test.xml), select Filter/Echo, toggle Pad 7 `effect_mixfx_activate` off/on, then compare Pad 8 and shift-pad debug output for `` `get_mixfx_active` ``. | v2026-m b9336 | None required | Pass | In pad text/query/color, `` `get_mixfx_active` `` returned `off`/`on` and matched `effect_mixfx_activate` for Filter and Echo once a track was loaded on deck 1. |
| `effect_select_multi` with `effect_active <slot> '<effect>'` | Multi-effect-per-slot behavior is official by name/summary but easy to miss in pad design. | Pad XML, numeric deck FX slot, named stem FX slot. | Build a two-pad page for slot 1 and `vocals`: Echo Out pad uses `effect_select_multi ... 'echo out'`; Reverb pad uses `effect_select_multi ... 'reverb'`; query each with `effect_active ... '<effect>'`; verify independent LED state and simultaneous audio. | User-provided local result, build not recorded | None recorded | Partial | User-provided vocal-slot pads confirmed Echo Out and Reverb light independently while both play on the `vocals` stem FX slot. Conservative guidance is promoted to the `effect_select_multi` and `effect_active` entries; repeat on a recorded build for fixture-grade `Pass`. |
| `padfx` shared identity and `effect_disable_all 'padfx'` ordering | `padfx` is useful for quick triggers, but deterministic chained presets can be affected by shared effect/stem targets and cleanup timing. | Pad XML with stem-targeted pad FX. | Create Pad A with `effect_disable_all 'padfx' & padfx 'echo out' ... 'stemfx:vocal' & padfx 'reverb' ... 'stemfx:vocal'`; create Pad B with the same chain but no inline clear; create Pad C using one of the same effect/stem targets at different values; observe pad light/audible behavior and parameter changes. | User-provided local result, build not recorded | None recorded | Partial | Inline `effect_disable_all 'padfx'` before new padfx calls did not activate/light; removing it worked. Another pad using the same effect/stem target can alter the active pad-FX parameters. Conservative guidance is promoted to the `padfx` notes and `effect_disable_all 'padfx'` example: treat cleanup as a separate broad reset, not as private per-pad state or an inline initializer. Repeat with `effects_used 'padfx'` before promoting to fixture-grade `Pass`. |
| Numeric and named FX slot selected-effect restart persistence | Official docs emphasize deck FX slots 1-6; user observation suggests restart persistence follows that same boundary. | Pad XML or custom buttons using `effect_select`, `effect_select <slot>`, and `get_effect_name`; normal deck FX slots 1-8 and named stem FX slots. | Use [FX-SLOTS.xml](../examples/Pads/FX-SLOTS.xml) or equivalent controls; select visible effects for FX1-FX8 and named stem FX slots such as `vocals`/`rhythm`; load tracks; close/reopen VirtualDJ; compare returned loaded effect names. | User-provided local result, build not recorded | None recorded | Partial | FX1-FX6 kept their loaded effect across restart. FX7+ and named stem FX slots kept loaded effects across track loads/current session but reset after restart. This is selected-effect persistence only; active state, slider values, and multi-effect contents need separate testing. |
| `effect_bank_save` / `effect_bank_load` | Official rack snapshot helpers; persistence, scope, and active-state recall need a reproducible note. | Deck FX slots 1-6, HTTP or pad. | Read-only recon first (`effect_bank_load N` + restore) to find an empty bank; save/load a round-trip into it; test active-state and slider recall and deck scope. | VirtualDJ 2026 (HTTP interface, 2026-07-26) | None required | Pass | A bank is a rack of effect **selections** (slots 1-6), nothing more. `effect_bank_save N` writes the selection; `effect_bank_load N` restores it. **Round-trip:** scrambled slots via one bank, loaded another, exact selection returned. **Return value is an existence probe:** load returns `true` for a populated bank, `false` for an empty one (banks 1-3 held user racks → true; 4-8 empty → false); save always returns `true`. **Active state NOT recalled:** saved with slot 1 active, deactivated, loaded → stayed inactive. **Slider values NOT recalled:** slider left at its changed value after load (effect was already selected). **Global, not per-deck:** a rack saved on deck 1 loaded intact onto deck 2. Safe-testing method confirmed: pick an empty bank via the load-return probe rather than writing over an occupied one. |
| `effect_releaseslider` / `effect_releaseslider_active` / `is_releasefx` | Release-FX path is separate from normal slot sliders; selection and query behavior need a recorded result. | Pad/custom button/momentary control with a selected release FX. | Compare `is_releasefx` with various effects in deck slots; test the release sliders against normal `effect_slider`. | VirtualDJ 2026 (HTTP interface, 2026-07-26) | None required | Partial | Confirmed **separate from deck-FX slots 1-6**: `is_releasefx` stayed `no` with every effect loaded into slot 1, release-type effects included (Backspin, BrakeStart, VinylBrake, Beat Brake) — loading into a numbered slot never arms it. Forms `is_releasefx`, `is_releasefx <slot>`, `is_releasefx '<effect>'` all `no`. `effect_releaseslider` / `effect_releaseslider_active` are accepted (execute `true`) but **inert** without an armed release FX: `effect_releaseslider 50%` left the readback at `0` and did not flip `is_releasefx`. Arming a release FX needs a momentary press/release this channel cannot drive, so activation and slider behavior still need a pad or mapper surface. |
| `effect_fxsendreturn*` helpers | Routing depends on mixer/send-return context and may be hardware-sensitive. | Skin/custom button, controller with software/hardware FX send-return path. | Toggle `effect_fxsendreturnenable`, select master/mic/deck sources with `effect_fxsendreturndeck_multi`, and record available/visible routing changes. | TBD | Optional hardware | Untested | Official names are present; practical behavior is context-dependent. |
| `effect_command` plugin commands | Command strings are plugin-specific; built-in BeatGrid UI provides evidence but not a universal command map. | BeatGrid plugin in a deck FX slot, track loaded. | Load `Beat Grid` into slot 1 with a track on the deck; probe `get RC` / `set RC` / `cur N` per the built-in `Plugin-UI/AFX_beatgrid.xml`. | VirtualDJ 2026 (HTTP interface, 2026-07-26) | None required | Pass | **Plugin-instance-scoped, not generic.** `effect_command 'get 00'` returned `no` with Phaser in slot 1 and `yes` after loading `Beat Grid` there. Two forms: bare `effect_command '<cmd>'` targets the loaded plugin; `effect_command <slot> '<cmd>'` takes an **unquoted** slot number (`effect_command 1 'get 00'` → yes; quoted `effect_command '1' …` → no). BeatGrid vocabulary, confirmed live against the built-in UI: `get RC` queries the grid cell at row R, col C (hex); `set RC` toggles it (verified reversible on an editable cell: off→set→on→set→off, grid left pristine); `cur N` is the current-playback-column indicator. Needs a loaded track for grid content. Do **not** document as generic plugin control. |
| Video FX slot controls | Built-in skins expose video FX panels, but a focused behavior pass would improve examples. | Built-in skin or test skin with video output enabled. | Select a video FX, toggle `video_fx`, move `video_fx_slider 1`, test `video_fx_clear`, then repeat with `deck master video_fx...`; record text/query behavior. | VirtualDJ 2026 (HTTP interface, 2026-07-22) | None required | Partial | Selection and enumeration are characterized; rendering behavior is not. `video_fx_select +1` cycles the enabled video-FX list (**17** entries here) with readback via `get_videofx_name`; `video_transition_select +1` cycles transitions (**35** entries, including `None`) with readback via `get_videotrans_name`. The three `+1` cycles — deck FX, video FX, transition — are **disjoint**, which is the app's own category assignment and the only working audio-vs-video discriminator found: **loadability is not one**, because all three selectors accept any installed effect name by name (`video_fx_select 'Echo'` really does set the video slot to Echo). Each cycle is the *enabled/favorites* subset, so an installed effect in no cycle (here `Lottery`, `Sweep`, `Title`, `Vocals`) is category-unknown rather than uncategorised. Both readback verbs ignore their argument. Still untested: `video_fx_slider`, `video_fx_clear`, `deck master` scoping, and what any of these actually render. |

## Deck And Mode Helpers

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `deck_has_error` | Official sparse loading/deck helper; error state and reset behavior are now locally characterized in a pad-page load workflow. | Deck skin query/text, load workflow, custom button display. | Load [Reference - Deck Error Test.xml](../tests/Pads/Reference%20-%20Deck%20Error%20Test.xml), compare current/deck-scoped `` `deck_has_error` `` before load, after a valid selected-track load, after unload, after loading the deliberately missing file, and after a subsequent valid load. | v2026-m b9336 | None required | Pass | In the pad-page run, `deck_has_error` stayed off for normal load/unload states, turned on/red after a deliberately missing file load, scoped to deck 1 while deck 2 stayed off, and cleared after a later successful selected-track load. |
| `dualdeckmode_decks` | Official prose ties it to dual-deck pairs 1/3 or 2/4, but mapping behavior remains sparse. | Controller mapping, deck assignment logic, dual-deck mode. | Load [Reference - Dual Deck Mode Test.xml](../tests/Pads/Reference%20-%20Dual%20Deck%20Mode%20Test.xml), toggle `dualdeckmode`, compare current and `deck 1`-`deck 4` `` `dualdeckmode_decks` `` labels/queries/logs, then repeat from deck-pair contexts 1/3 and 2/4 if available. | v2026-m b9336 | Optional controller | Partial | In the pad-page run, `dualdeckmode` toggled on/blue but current and deck-scoped `dualdeckmode_decks` readbacks stayed false/red; repeating on deck 2 gave the same result. Test a visible dual-deck pair/controller context before promotion. |

## Karaoke

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `karaoke_venue_name` | Sparse karaoke helper; source of value and empty-state behavior need confirmation. | Karaoke skin text/query, karaoke options/config. | Set/clear the venue name in karaoke options, display `` `karaoke_venue_name` ``, and record value, fallback text, and whether changes update live. | v2026-m b9336 | None required | Pass | Empty venue returns blank after `KARAOKE:`. Pressing the pad opens the Karaoke menu; Venue Name dialog sets the value; clearing the venue returns to blank. |

## Grammar Battery Over HTTP

VirtualDJ 2026, HTTP control interface, 2026-07-22. Global variables (`$zz_*`) as
observable side effects: reset to 0, execute the script, read back with `get_var`. This
reproduces the pad [Grammar Battery](../tests/Pads/Reference%20-%20Grammar%20Battery%20Test.xml)
without a fixture or manual reading. Settled rules are written up in
[VDJScript Grammar](VDJScript%20Grammar.md); this table is the run record.

| Question | Script | Observed | Result |
| --- | --- | --- | --- |
| Branch extent, chains both sides | `on ? set a & set b : set c & set d` | `a=1 b=1 c=0 d=0`; with `off`, `0011` | Pass — each branch takes its whole chain |
| Trailing `&` binding (cross-surface check) | `on ? set a : set b & set c` | `1000`; with `off`, `0110` | Pass — reproduces the pad result exactly, so the rule is parser-level not surface-level |
| Leading `&` split (cross-surface check) | `set a & on ? set b : set c` | `1100`; with `off`, `1010` | Pass — reproduces the pad result |
| `&&` in action position | `off && set a` | `a=1` | **Fail as a guard** — action runs regardless; same for a false `var_equal`. `&&` behaves as `&` here |
| Correct action guard | `var_equal '$x' 999 ? set a : nothing` | `a=0` when false, `1` when true | Pass — ternary is the only guard; `nothing` is a valid action-position null branch |
| Constants in value position | `set '$v' on` / `off` / `true` / `false` | `yes` / `no` / `''` / `''` | Pass — `on`/`off` are constants, `true`/`false` are not |
| String variable readback | `set '$v' 'apple'` then `get_var`/`var_equal` | `get_var`=`''`; `var_equal` = `yes` vs `'apple'`, `'banana'`, bare `banana` | **Fail** — string variables are write-only: unreadable and uncomparable; `var_equal` matches anything |
| Numeric variable readback | `set '$v' 5` | `var_equal '$v' 5`=yes, `'5'`=no, `7`=no | Pass — quoting is type-significant |
| Comment syntax | `set a 1 // set b 1`, and `#`, `;`, `--`, `/*x*/` | `a=1 b=0` in all five | Pass (negative) — no comment syntax; every marker silently discards the rest of the statement |
| Chain length ceiling | 142 vs 152 `set` statements; 302 vs 402 cheap statements | 142 and 302 all ran; 152 and 402 ran **nothing at all**, `execute` still `true` | Partial — a ceiling exists and failure is total, not truncating; boundary moves with statement content. Identical on GET and POST, so not a URL artefact |
| `while_pressed` placement | `set a 1 while_pressed & set b 1` | `a=1 b=1` | Partial — accepted trailing and mid-chain, does not block the chain; release behavior untestable over HTTP |

Side effect: this run leaves `$zz_*` session globals set. They are session-scoped and clear
on VirtualDJ restart.

## Mapper Firing (Real Hardware)

VirtualDJ 2026, HTTP interface + AlphaTheta DDJ-GRV6, 2026-07-27. A minimal test
mapper for `device="DDJGRV6"` bound `ONINIT` and `PLAY_PAUSE` to `set '$var' 1`;
probes read back over HTTP. Confirms the mapper `<map value action>` schema fires
on real hardware, and surfaces three operational facts.

| What | Script / step | Observed | Result |
| --- | --- | --- | --- |
| `<map>` binding fires on button press | `<map value="PLAY_PAUSE" action="set '$vdj_maptest_fired' 1"/>`, press play | `$vdj_maptest_fired` 0 → 1 over HTTP | Pass — first local proof a mapper binding executes on hardware |
| `ONINIT` fires on load | `<map value="ONINIT" action="set '$vdj_maptest_init' 1"/>` | `$vdj_maptest_init` = 1 after load and after restart | Pass |
| Control name must match exactly | `value="PLAY"` (real name is `PLAY_PAUSE`) | loaded without error, never fired | Pass (negative) — wrong name binds nothing, silently (no-error parsing) |
| Loading a mapping resets `$` globals | HTTP-set `$vdj_maptest_fired`=0, then select mapping | read back blank afterward | Pass — seed state in `ONINIT`, not before |
| Edited mapper file needs a restart | edit active mapper, re-select it | monitor still showed the pre-edit binding; **restart** picked it up | Pass — re-select does not reload; switching between different mappings does |

Not covered: the custom **device-definition** (`<device>`) schema. The DDJ-GRV6 is
factory-recognized (compiled `controllers.dat`), so a custom `<device>` XML is not
exercised. Testing that needs unrecognized hardware or a virtual MIDI port + injection.
