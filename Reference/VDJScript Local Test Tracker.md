# VDJScript Local Test Tracker

Focused manual-test log for verbs marked **Needs local test** in [Official VDJScript Coverage Audit](Official%20VDJScript%20Coverage%20Audit.md). Keep rows practical: one reproducible check, the VirtualDJ build, hardware/context, result, and any follow-up notes.

Result values: `Untested`, `Pass`, `Partial`, `Fail`, `N/A`.

## Evidence Snapshot

Last sparse-prose spot-check: 2026-05-21 against the [official VDJScript verbs appendix](https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html) and local official/published skin examples.

- `Untested` means behavior has not been observed in VirtualDJ locally, even if the verb is official.
- `Pass` means a specific VirtualDJ build, hardware/context, action, and observed result were recorded.
- `connect` has local skin evidence: [official Lite](../examples/skins/official/Lite.xml) uses `<button action="connect">`, and [Project X Slider](<../Skins/Project X Slider/ProjectXSlider.xml>) uses `source="not connect"` for an account icon. Keep the tracker row open until logged-in/logged-out behavior is recorded.
- `system` and `open_stem_creator` are official names, but the current public appendix gives no useful behavior prose for them. Do not infer `system` behavior from unrelated parameter values such as `get_vu_meter 'system'` or from `system_volume`.
- `dualdeckmode_decks` is tied to `dualdeckmode` official prose for deck pairs 1/3 and 2/4, but the helper itself still needs an observed deck-context result.
- Controller-display, Phase, RZX, DJC, V7, Gemini, and Denon rows are hardware-dependent; keep them `Untested` unless the named target device or an equivalent controller mapping environment was used.

Suggested test order:

1. No dedicated hardware: `connect`, `system`, `open_stem_creator`, `karaoke_venue_name`
2. Optional controller/deck setup: `dualdeckmode_decks`
3. Hardware-only batches: controller displays, Phase, RZX, DJC, V7, Gemini, Denon

## Sampler

| Verb / Pattern | Why local test | Likely surface/context | Repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `sampler_loaded 8 'auto'` | Forum examples and older local examples use `"auto"`, but official docs only document fixed-slot `sampler_loaded 1`. | Pad XML sampler page with `sampler_pad_page`. | Load [Reference - Sampler Loaded Test.xml](../Pads/Reference%20-%20Sampler%20Loaded%20Test.xml); use a bank with slot 8 loaded and slot 16 empty; switch to sampler page `9-16`. | 8.5.9307 / 18.0.9336 | None required | Fail | On page `9-16`, `sampler_loaded 8 'auto'` returned true while explicit `sampler_loaded 16` returned false. Treat `sampler_loaded` as absolute for empty-slot checks. |
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
| `connect` | Official skins use it, but action/query behavior varies by account connection state. | Skin button, custom button, config/account UI. | Test logged out and logged in: run `connect`, then display/query `` `connect` `` if accepted; record opened UI and returned state. | TBD | None required | Untested | Official Lite action evidence; Project X query evidence. |
| `system` | Sparse official system helper; parameters and return behavior are unclear. | Custom button, skin query/text, possible system integration context. | Run `system` with no parameter in a custom button; then try a harmless known/obvious parameter only if official examples are found; record UI/log output. | TBD | None required | Untested | Official name only; do not infer from `system_volume` or system VU labels. |
| `open_stem_creator` | Opens a workflow that may depend on license/build/stem features. | Skin/custom button, config/workflow action. | Run `open_stem_creator` with a track selected and with no track selected; note opened window, gating, and any error/status message. | TBD | None required | Untested | Official name only; likely build/license/selection dependent. |

## Deck And Mode Helpers

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `dualdeckmode_decks` | Official prose ties it to dual-deck pairs 1/3 or 2/4, but mapping behavior is sparse. | Controller mapping, deck assignment logic, dual-deck mode. | Enable `dualdeckmode`, load decks 1/3 and 2/4, then display/log `` `dualdeckmode_decks` `` from each deck context; record pair selection and false states. | TBD | Optional controller | Untested | Official pair relationship documented; helper return/action behavior unobserved. |

## Karaoke

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `karaoke_venue_name` | Sparse karaoke helper; source of value and empty-state behavior need confirmation. | Karaoke skin text/query, karaoke options/config. | Set/clear the venue name in karaoke options, display `` `karaoke_venue_name` ``, and record value, fallback text, and whether changes update live. | TBD | None required | Untested | Official name only; needs karaoke option/value observation. |
