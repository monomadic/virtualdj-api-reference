# VDJScript Local Test Tracker

Focused manual-test log for verbs marked **Needs local test** in [Official VDJScript Coverage Audit](Official%20VDJScript%20Coverage%20Audit.md). Keep rows practical: one reproducible check, the VirtualDJ build, hardware/context, result, and any follow-up notes.

Result values: `Untested`, `Pass`, `Partial`, `Fail`, `N/A`.

## Evidence Snapshot

Last sparse-prose spot-check: 2026-05-21 against the [official VDJScript verbs appendix](https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html) and local official/published skin examples.

- Current coverage cross-check: the 2026-05-26 official appendix refresh parses to 991 official verb/alias names; `VDJScript Verbs.md` contains all 991, missing names are 0, and the compact official remainder is empty. The formal `Needs local test` gap is 20 official names: `deck_has_error`, `system`, `dualdeckmode_decks`, and the 17 hardware-specific controller helpers below.
- `Untested` means behavior has not been observed in VirtualDJ locally, even if the verb is official.
- `Pass` means a specific VirtualDJ build, hardware/context, action, and observed result were recorded.
- `connect` has local skin evidence: [official Lite](../examples/skins/official/Lite.xml) uses `<button action="connect">`. Local testing on VirtualDJ `v2026-m b9336` confirmed action/query behavior for logged-in and logged-out states.
- `karaoke_venue_name` was locally tested on VirtualDJ `v2026-m b9336`; it returns blank when the karaoke venue name is empty and updates to the configured venue name from the Karaoke > Venue Name dialog.
- `system` was locally tested on VirtualDJ `v2026-m b9336`; in the sparse helper pad context it returned blank text and pressing it produced no visible UI or log result. This is still too sparse to promote beyond a conservative note. Do not infer `system` behavior from unrelated parameter values such as `get_vu_meter 'system'` or from `system_volume`.
- `open_stem_creator` was locally tested on VirtualDJ `v2026-m b9336`; pressing it opened the Stem Creator dialog. Treat it as a workflow opener, not a selected-track automation helper.
- `get_mixfx_active` was locally tested on VirtualDJ `v2026-m b9336`; in a pad-page text/query context, it mirrored `effect_mixfx_activate` off/on for Filter and Echo after a track was loaded.
- `dualdeckmode_decks` is tied to `dualdeckmode` official prose for deck pairs 1/3 and 2/4, but the helper itself still needs an observed deck-context result.
- Controller-display, Phase, RZX, DJC, V7, Gemini, and Denon rows are hardware-dependent; keep them `Untested` unless the named target device or an equivalent controller mapping environment was used.

Suggested test order:

1. No-hardware sparse helpers: `deck_has_error` with [Reference - Deck Error Test.xml](../Test/Pads/Reference%20-%20Deck%20Error%20Test.xml); revisit `system` only if official examples or harmless parameters are found.
2. Optional controller/deck setup: `dualdeckmode_decks` with [Reference - Dual Deck Mode Test.xml](../Test/Pads/Reference%20-%20Dual%20Deck%20Mode%20Test.xml)
3. Hardware-only batches: controller displays, Phase, RZX, DJC, V7, Gemini, Denon

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
| `effect_has_slider` / `effect_has_button` and `get_effect_slider_*` / `get_effect_button_*` | Built-in skins use these heavily, but the exact return shapes and context scoping need a focused local fixture. | Skin controls, pad text/query, custom button display; deck FX, video FX, transition FX. | Load [Reference - FX Introspection Test.xml](../Test/Pads/Reference%20-%20FX%20Introspection%20Test.xml), press each LOAD pad, observe slider/button counts, labels, defaults, text, and `effect_has_*` states; repeat separately for `video` and `transition` targets. | TBD | None required | Untested | Built-in skin evidence is strong enough for documentation patterns, but local result values should be recorded before writing a complete behavior table. |
| Native effect parameter examples | Existing pad pages provide working presets, but the repo does not yet have a systematic effect-by-effect slider/button map. | Pad XML and skin/custom button controls for selected native effects. | Use [Reference - FX Introspection Test.xml](../Test/Pads/Reference%20-%20FX%20Introspection%20Test.xml) as a starter fixture; for each native effect, load it in slot 1, record counts, labels, defaults, button count, and tested `effect_slider`/`padfx` presets with VirtualDJ build/effect version. | Partial local examples; full pass TBD | None required | Partial | `Pads/Reference - Slot FX.xml`, `Pads/PUSH FX.xml`, and built-in `pads_stems+fx.xml` document several working forms. This is not a complete parameter map. |
| `get_mixfx_active` | Official sparse Mix FX helper; return value and relationship to `effect_mixfx_activate` needed confirmation. | Skin text/query, pad query/color, custom button display. | Load [Reference - Mix FX Query Test.xml](../Test/Pads/Reference%20-%20Mix%20FX%20Query%20Test.xml), select Filter/Echo, toggle Pad 7 `effect_mixfx_activate` off/on, then compare Pad 8 and shift-pad debug output for `` `get_mixfx_active` ``. | v2026-m b9336 | None required | Pass | In pad text/query/color, `` `get_mixfx_active` `` returned `off`/`on` and matched `effect_mixfx_activate` for Filter and Echo once a track was loaded on deck 1. |
| `effect_select_multi` with `effect_active <slot> '<effect>'` | Multi-effect-per-slot behavior is official by name/summary but easy to miss in pad design. | Pad XML, numeric deck FX slot, named stem FX slot. | Build a two-pad page for slot 1 and `vocals`: Echo Out pad uses `effect_select_multi ... 'echo out'`; Reverb pad uses `effect_select_multi ... 'reverb'`; query each with `effect_active ... '<effect>'`; verify independent LED state and simultaneous audio. | User-provided local result, build not recorded | None recorded | Partial | User-provided vocal-slot pads confirmed Echo Out and Reverb light independently while both play on the `vocals` stem FX slot. Needs repeat on a recorded build for fixture-grade `Pass`. |
| `padfx` shared identity and `effect_disable_all 'padfx'` ordering | `padfx` is useful for quick triggers, but deterministic chained presets can be affected by shared effect/stem targets and cleanup timing. | Pad XML with stem-targeted pad FX. | Create Pad A with `effect_disable_all 'padfx' & padfx 'echo out' ... 'stemfx:vocal' & padfx 'reverb' ... 'stemfx:vocal'`; create Pad B with the same chain but no inline clear; create Pad C using one of the same effect/stem targets at different values; observe pad light/audible behavior and parameter changes. | User-provided local result, build not recorded | None recorded | Partial | Inline `effect_disable_all 'padfx'` before new padfx calls did not activate/light; removing it worked. Another pad using the same effect/stem target can alter the active pad-FX parameters. Treat `effect_disable_all 'padfx'` as separate cleanup and do not treat `padfx` as private per-pad state. |
| `effect_bank_save` / `effect_bank_load` | Official rack snapshot helpers; persistence, scope, and active-state recall need a reproducible note. | Pad XML or custom buttons on a deck with 1-6 FX slots. | Load three known effects with distinct active states and slider values, save bank 1, change all slots, load bank 1, then record restored effect names, active states, sliders, and whether bank is deck-specific. | TBD | None required | Untested | Useful everyday helper, but not yet locally characterized beyond official summary. |
| `effect_releaseslider_active` / `is_releasefx` | Release-FX path is separate from normal slot sliders; selection and query behavior need a fixture. | Skin/custom button with a selected release FX. | Select a known release-capable effect if required, display `is_releasefx`, run `effect_releaseslider_active 50%`, and compare with `effect_active` / audible behavior. | TBD | None required | Untested | Keep examples conservative until release-FX target selection is recorded. |
| `effect_fxsendreturn*` helpers | Routing depends on mixer/send-return context and may be hardware-sensitive. | Skin/custom button, controller with software/hardware FX send-return path. | Toggle `effect_fxsendreturnenable`, select master/mic/deck sources with `effect_fxsendreturndeck_multi`, and record available/visible routing changes. | TBD | Optional hardware | Untested | Official names are present; practical behavior is context-dependent. |
| `effect_command` plugin commands | Command strings are plugin-specific; built-in BeatGrid UI provides evidence but not a universal command map. | Built-in BeatGrid plugin UI or a test skin targeting BeatGrid. | Open BeatGrid, run `effect_command 'get 00'`, `effect_command 'set 00'`, and `effect_command 'cur 0'`; compare visual state to built-in plugin UI. | TBD | None required | Untested | Built-in plugin UI XML uses these command strings; needs a recorded VirtualDJ result before promoting to `Local test`. |
| Video FX slot controls | Built-in skins expose video FX panels, but a focused behavior pass would improve examples. | Built-in skin or test skin with video output enabled. | Select a video FX, toggle `video_fx`, move `video_fx_slider 1`, test `video_fx_clear`, then repeat with `deck master video_fx...`; record text/query behavior. | TBD | None required | Untested | Built-in skin evidence exists for controls and labels; audio-only/video-source edge cases need notes. |

## Deck And Mode Helpers

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `deck_has_error` | Official sparse loading/deck helper; error states and reset behavior are undocumented locally. | Deck skin query/text, load workflow, custom button display. | Load [Reference - Deck Error Test.xml](../Test/Pads/Reference%20-%20Deck%20Error%20Test.xml), compare current/deck-scoped `` `deck_has_error` `` before load, after a valid selected-track load, after unload, after loading the deliberately missing file, and after a subsequent valid load. | TBD | None required | Untested | Official name only as of the 2026-05-26 appendix refresh. |
| `dualdeckmode_decks` | Official prose ties it to dual-deck pairs 1/3 or 2/4, but mapping behavior is sparse. | Controller mapping, deck assignment logic, dual-deck mode. | Load [Reference - Dual Deck Mode Test.xml](../Test/Pads/Reference%20-%20Dual%20Deck%20Mode%20Test.xml), toggle `dualdeckmode`, compare current and `deck 1`-`deck 4` `` `dualdeckmode_decks` `` labels/queries/logs, then repeat from deck-pair contexts 1/3 and 2/4 if available. | TBD | Optional controller | Untested | Official pair relationship documented; helper return/action behavior unobserved. |

## Karaoke

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `karaoke_venue_name` | Sparse karaoke helper; source of value and empty-state behavior need confirmation. | Karaoke skin text/query, karaoke options/config. | Set/clear the venue name in karaoke options, display `` `karaoke_venue_name` ``, and record value, fallback text, and whether changes update live. | v2026-m b9336 | None required | Pass | Empty venue returns blank after `KARAOKE:`. Pressing the pad opens the Karaoke menu; Venue Name dialog sets the value; clearing the venue returns to blank. |
