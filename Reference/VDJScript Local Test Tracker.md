# VDJScript Local Test Tracker

Focused manual-test log for verbs marked **Needs local test** in [Official VDJScript Coverage Audit](Official%20VDJScript%20Coverage%20Audit.md). Keep rows practical: one reproducible check, the VirtualDJ build, hardware/context, result, and any follow-up notes.

Result values: `Untested`, `Pass`, `Partial`, `Fail`, `N/A`.

## Evidence Snapshot

Last sparse-prose spot-check: 2026-05-21 against the [official VDJScript verbs appendix](https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html) and local official/published skin examples.

- Current coverage cross-check: the 2026-06-30 official appendix refresh parses to 991 official verb/alias names; `VDJScript Verbs.md` contains all 991, missing names are 0, and the compact official remainder is empty. The formal `Needs local test` gap is 19 official names: `system`, `dualdeckmode_decks`, and the 17 hardware-specific controller helpers below. `dualdeckmode_decks` now has a build-recorded pad-page observation, but still needs a dual-deck pair/controller-context repeat before promotion to `Pass`.
- `Untested` means behavior has not been observed in VirtualDJ locally, even if the verb is official.
- `Pass` means a specific VirtualDJ build, hardware/context, action, and observed result were recorded.
- `connect` has local skin evidence: [official Lite](../examples/skins/official/Lite.xml) uses `<button action="connect">`. Local testing on VirtualDJ `v2026-m b9336` confirmed action/query behavior for logged-in and logged-out states.
- `karaoke_venue_name` was locally tested on VirtualDJ `v2026-m b9336`; it returns blank when the karaoke venue name is empty and updates to the configured venue name from the Karaoke > Venue Name dialog.
- `system` was locally tested on VirtualDJ `v2026-m b9336`; in the sparse helper pad context it returned blank text and pressing it produced no visible UI or log result. This is still too sparse to promote beyond a conservative note. Do not infer `system` behavior from unrelated parameter values such as `get_vu_meter 'system'` or from `system_volume`.
- `open_stem_creator` was locally tested on VirtualDJ `v2026-m b9336`; pressing it opened the Stem Creator dialog. Treat it as a workflow opener, not a selected-track automation helper.
- `get_mixfx_active` was locally tested on VirtualDJ `v2026-m b9336`; in a pad-page text/query context, it mirrored `effect_mixfx_activate` off/on for Filter and Echo after a track was loaded.
- `deck_has_error` was locally tested on VirtualDJ `v2026-m b9336`; it stayed off for normal load/unload states, turned on after loading a deliberately missing file, scoped to deck 1 in the tested context, and cleared after a later successful selected-track load.
- `dualdeckmode_decks` has a local pad-page result on VirtualDJ `v2026-m b9336`: in the pad-page context it remained false/red for current and deck-scoped readbacks even after `dualdeckmode` toggled on; repeated on deck 2 with the same reported behavior.
- Controller-display, Phase, RZX, DJC, V7, Gemini, and Denon rows are hardware-dependent; keep them `Untested` unless the named target device or an equivalent controller mapping environment was used.

Suggested test order:

1. No-hardware sparse helpers: revisit `system` only if official examples or harmless parameters are found.
2. Optional controller/deck setup: repeat/expand `dualdeckmode_decks` with [Reference - Dual Deck Mode Test.xml](../Test/Pads/Reference%20-%20Dual%20Deck%20Mode%20Test.xml), especially in any context where dual-deck pair routing is visible.
3. Hardware-only batches: controller displays, Phase, RZX, DJC, V7, Gemini, Denon
4. Non-official Button Editor hidden probes: use [Reference - Hidden Button Editor Tests.xml](../Test/Pads/Reference%20-%20Hidden%20Button%20Editor%20Tests.xml), then record results in the dedicated hidden-candidate section below without promoting them to official guidance.

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
Test asset: Local FX slot/stem slot setup; `Pads/FX-SLOTS.xml` is the nearest repo fixture
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

## Button Editor Hidden Candidate Probes

These rows are not official `Needs local test` rows. They track flag1-hidden Button Editor taxonomy candidates that are absent from the official appendix but have one or more local evidence streams: bundled language descriptions, compiled taxonomy placement, runtime strings, or exact `ACTION_*` method-symbol hints.

Do not promote these into ordinary user-facing verb guidance until a row has a concrete VirtualDJ build, setup, observed result, and notes. Use [Undocumented VDJScript Candidates](Undocumented%20VDJScript%20Candidates.md) as the evidence inventory, and use [Reference - Hidden Button Editor Tests.xml](../Test/Pads/Reference%20-%20Hidden%20Button%20Editor%20Tests.xml) for the low-risk pad probes.

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
| `sampler_loaded 8 'auto'` | Forum examples and older local examples use `"auto"`, but official docs only document fixed-slot `sampler_loaded 1`. | Pad XML sampler page with `sampler_pad_page`. | Load [Reference - Sampler Loaded Test.xml](../Test/Pads/Reference%20-%20Sampler%20Loaded%20Test.xml); use a bank with slot 8 loaded and slot 16 empty; switch to sampler page `9-16`. | 8.5.9307 / 18.0.9336 | None required | Fail | On page `9-16`, `sampler_loaded 8 'auto'` returned true while explicit `sampler_loaded 16` returned false. Treat `sampler_loaded` as absolute for empty-slot checks. |
| `sampler_loaded 8 auto` | Installed/public `Loop Recorder.xml` uses unquoted `auto`; check whether omitting quotes changes page-aware behavior. | Pad XML sampler page with `sampler_pad_page`. | Same diagnostic page; compare `AUTO8`, `AUTO8RAW`, `SLOT16`, and `AUTO16RAW` pads on page `9-16`. | 8.5.9307 / 18.0.9336 | None required | Fail | On page `9-16`, `sampler_loaded 8 auto` returned true while `sampler_loaded 16 auto` returned false. Unquoted `auto` matched quoted behavior and did not make `sampler_loaded 8` page-aware. |
| Read-only multi-page sampler guards | Need a page-aware sampler page that plays loaded samples but does not record or show slot-number fallbacks for empty slots. | Pad XML sampler page with `sampler_pad_page`, 8-pad and 16-pad controller layouts. | Load [SAMPLER READ ONLY.xml](../Pads/SAMPLER%20READ%20ONLY.xml); use a bank with more than 8 presets; switch to page `9 to 16`; verify loaded slots show/play and empty slots stay blank/off/nothing. | 8.5.9307 / 18.0.9336 | XP2-style 16-pad layout observed | Pass | Working pattern: branch on text ranges like `"9 to 16"`, guard with absolute `sampler_loaded` slots, use `sampler_pad <visible-pad>` for loaded actions, `nothing` for empty actions, and `get_text ' '` for blank labels. Pads 9-16 map to the next eight visible sampler positions, so page `"9 to 16"` plus pad16 maps to slot 24. |

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
| `effect_has_slider` / `effect_has_button` and `get_effect_slider_*` / `get_effect_button_*` | Built-in skins use these heavily, but the exact return shapes and context scoping need a focused local fixture. | Skin controls, pad text/query, custom button display; deck FX, video FX, transition FX. | Load [Reference - FX Introspection Test.xml](../Test/Pads/Reference%20-%20FX%20Introspection%20Test.xml), press each LOAD pad, observe slider/button counts, labels, defaults, text, and `effect_has_*` states; press Shift+Pads 1-16 to log count/default/label/text/name/shortname/button helpers; repeat separately for `video` and `transition` targets. | v2026-m b9336 | None required | Partial | Flanger GUI opened from the fixture and showed Strength 50%, Speed 8bt, Tone n/a, Feedback 50%, and LFO AMP 40%. Helper readbacks are still not recorded: slider/button counts, labels, names, short names, defaults, formatted text, skip-length variants, and `effect_has_*` states are unknown. Do not infer helper behavior from the visible GUI alone. |
| Native effect parameter examples | Existing pad pages provide working presets, but the repo does not yet have a systematic effect-by-effect slider/button map. | Pad XML and skin/custom button controls for selected native effects. | Use [Reference - FX Introspection Test.xml](../Test/Pads/Reference%20-%20FX%20Introspection%20Test.xml) as a starter fixture; for each native effect, load it in slot 1, record counts, labels, defaults, button count, and tested `effect_slider`/`padfx` presets with VirtualDJ build/effect version. | v2026-m b9336; full pass TBD | None required | Partial | Flanger GUI values recorded: Strength 50%, Speed 8bt, Tone n/a, Feedback 50%, LFO AMP 40%. `Pads/Reference - Slot FX.xml`, `Pads/PUSH FX.xml`, and built-in `pads_stems+fx.xml` document several working forms, but this is not a complete parameter map. |
| `get_mixfx_active` | Official sparse Mix FX helper; return value and relationship to `effect_mixfx_activate` needed confirmation. | Skin text/query, pad query/color, custom button display. | Load [Reference - Mix FX Query Test.xml](../Test/Pads/Reference%20-%20Mix%20FX%20Query%20Test.xml), select Filter/Echo, toggle Pad 7 `effect_mixfx_activate` off/on, then compare Pad 8 and shift-pad debug output for `` `get_mixfx_active` ``. | v2026-m b9336 | None required | Pass | In pad text/query/color, `` `get_mixfx_active` `` returned `off`/`on` and matched `effect_mixfx_activate` for Filter and Echo once a track was loaded on deck 1. |
| `effect_select_multi` with `effect_active <slot> '<effect>'` | Multi-effect-per-slot behavior is official by name/summary but easy to miss in pad design. | Pad XML, numeric deck FX slot, named stem FX slot. | Build a two-pad page for slot 1 and `vocals`: Echo Out pad uses `effect_select_multi ... 'echo out'`; Reverb pad uses `effect_select_multi ... 'reverb'`; query each with `effect_active ... '<effect>'`; verify independent LED state and simultaneous audio. | User-provided local result, build not recorded | None recorded | Partial | User-provided vocal-slot pads confirmed Echo Out and Reverb light independently while both play on the `vocals` stem FX slot. Conservative guidance is promoted to the `effect_select_multi` and `effect_active` entries; repeat on a recorded build for fixture-grade `Pass`. |
| `padfx` shared identity and `effect_disable_all 'padfx'` ordering | `padfx` is useful for quick triggers, but deterministic chained presets can be affected by shared effect/stem targets and cleanup timing. | Pad XML with stem-targeted pad FX. | Create Pad A with `effect_disable_all 'padfx' & padfx 'echo out' ... 'stemfx:vocal' & padfx 'reverb' ... 'stemfx:vocal'`; create Pad B with the same chain but no inline clear; create Pad C using one of the same effect/stem targets at different values; observe pad light/audible behavior and parameter changes. | User-provided local result, build not recorded | None recorded | Partial | Inline `effect_disable_all 'padfx'` before new padfx calls did not activate/light; removing it worked. Another pad using the same effect/stem target can alter the active pad-FX parameters. Treat `effect_disable_all 'padfx'` as separate cleanup and do not treat `padfx` as private per-pad state. |
| Numeric and named FX slot selected-effect restart persistence | Official docs emphasize deck FX slots 1-6; user observation suggests restart persistence follows that same boundary. | Pad XML or custom buttons using `effect_select`, `effect_select <slot>`, and `get_effect_name`; normal deck FX slots 1-8 and named stem FX slots. | Use [FX-SLOTS.xml](../Pads/FX-SLOTS.xml) or equivalent controls; select visible effects for FX1-FX8 and named stem FX slots such as `vocals`/`rhythm`; load tracks; close/reopen VirtualDJ; compare returned loaded effect names. | User-provided local result, build not recorded | None recorded | Partial | FX1-FX6 kept their loaded effect across restart. FX7+ and named stem FX slots kept loaded effects across track loads/current session but reset after restart. This is selected-effect persistence only; active state, slider values, and multi-effect contents need separate testing. |
| `effect_bank_save` / `effect_bank_load` | Official rack snapshot helpers; persistence, scope, and active-state recall need a reproducible note. | Pad XML on a deck with 1-6 FX slots. | Load [Reference - FX Bank Test.xml](../Test/Pads/Reference%20-%20FX%20Bank%20Test.xml); press SET RACK A, record slot names/active states/sliders, press SAVE BANK 1, press SET RACK B, press LOAD BANK 1, then compare restored names, active states, sliders, and whether behavior is deck-specific. | TBD | None required | Untested | Fixture writes to effect bank 1, so run in a throwaway profile/session or edit the bank number before testing if bank 1 contains user presets. |
| `effect_releaseslider_active` / `is_releasefx` | Release-FX path is separate from normal slot sliders; selection and query behavior need a recorded result. | Pad XML or custom button with a selected release FX. | Load [Reference - Release FX Test.xml](../Test/Pads/Reference%20-%20Release%20FX%20Test.xml); select or configure a release effect if the build requires it, compare `is_releasefx` before/after setup, then test `effect_releaseslider` and `effect_releaseslider_active` against normal `effect_slider` controls. | TBD | None required | Untested | Keep examples conservative until release-FX target selection and active-state behavior are recorded. |
| `effect_fxsendreturn*` helpers | Routing depends on mixer/send-return context and may be hardware-sensitive. | Skin/custom button, controller with software/hardware FX send-return path. | Toggle `effect_fxsendreturnenable`, select master/mic/deck sources with `effect_fxsendreturndeck_multi`, and record available/visible routing changes. | TBD | Optional hardware | Untested | Official names are present; practical behavior is context-dependent. |
| `effect_command` plugin commands | Command strings are plugin-specific; built-in BeatGrid UI provides evidence but not a universal command map. | Built-in BeatGrid plugin UI or a pad page targeting BeatGrid in slot 1. | Load [Reference - BeatGrid Command Test.xml](../Test/Pads/Reference%20-%20BeatGrid%20Command%20Test.xml), press LOAD BEATGRID and SHOW GUI, then compare `set`, `get`, and `cur` command pads against the visible BeatGrid UI and any slot/plugin-focus requirements. | TBD | None required | Untested | Built-in plugin UI XML uses these command strings; needs a recorded VirtualDJ result before promoting to `Local test`. Do not generalize beyond BeatGrid. |
| Video FX slot controls | Built-in skins expose video FX panels, but a focused behavior pass would improve examples. | Built-in skin or test skin with video output enabled. | Select a video FX, toggle `video_fx`, move `video_fx_slider 1`, test `video_fx_clear`, then repeat with `deck master video_fx...`; record text/query behavior. | TBD | None required | Untested | Built-in skin evidence exists for controls and labels; audio-only/video-source edge cases need notes. |

## Deck And Mode Helpers

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `deck_has_error` | Official sparse loading/deck helper; error state and reset behavior are now locally characterized in a pad-page load workflow. | Deck skin query/text, load workflow, custom button display. | Load [Reference - Deck Error Test.xml](../Test/Pads/Reference%20-%20Deck%20Error%20Test.xml), compare current/deck-scoped `` `deck_has_error` `` before load, after a valid selected-track load, after unload, after loading the deliberately missing file, and after a subsequent valid load. | v2026-m b9336 | None required | Pass | In the pad-page run, `deck_has_error` stayed off for normal load/unload states, turned on/red after a deliberately missing file load, scoped to deck 1 while deck 2 stayed off, and cleared after a later successful selected-track load. |
| `dualdeckmode_decks` | Official prose ties it to dual-deck pairs 1/3 or 2/4, but mapping behavior remains sparse. | Controller mapping, deck assignment logic, dual-deck mode. | Load [Reference - Dual Deck Mode Test.xml](../Test/Pads/Reference%20-%20Dual%20Deck%20Mode%20Test.xml), toggle `dualdeckmode`, compare current and `deck 1`-`deck 4` `` `dualdeckmode_decks` `` labels/queries/logs, then repeat from deck-pair contexts 1/3 and 2/4 if available. | v2026-m b9336 | Optional controller | Partial | In the pad-page run, `dualdeckmode` toggled on/blue but current and deck-scoped `dualdeckmode_decks` readbacks stayed false/red; repeating on deck 2 gave the same result. Test a visible dual-deck pair/controller context before promotion. |

## Karaoke

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `karaoke_venue_name` | Sparse karaoke helper; source of value and empty-state behavior need confirmation. | Karaoke skin text/query, karaoke options/config. | Set/clear the venue name in karaoke options, display `` `karaoke_venue_name` ``, and record value, fallback text, and whether changes update live. | v2026-m b9336 | None required | Pass | Empty venue returns blank after `KARAOKE:`. Pressing the pad opens the Karaoke menu; Venue Name dialog sets the value; clearing the venue returns to blank. |
