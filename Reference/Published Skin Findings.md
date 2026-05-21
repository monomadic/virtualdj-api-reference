# Published Skin Findings

Working public skins are useful source material for VirtualDJ development. They expose real skin-engine and VDJScript usage that users may copy, encounter, or ask about before our local reference has caught up.

This file is the holding area for commands and patterns mined from published skins. Do not remove a command from this file only because it is unfamiliar or absent from older local docs. Instead, record its provenance, search status, and test status.

## Source Labels

- `Published skin`: observed in a working skin distributed through VirtualDJ's skin ecosystem or installed from such a package.
- `Published pad page`: observed in a working pad page distributed through VirtualDJ's pad ecosystem or installed from such a package.
- `Official`: current VirtualDJ manual, VDJPedia, hardware manual, or other Atomix-authored documentation.
- `Official forum`: VirtualDJ staff, Development Manager, CTO, or Support staff giving scripting guidance.
- `Community`: forum moderators or non-staff users giving examples that still need verification.
- `Local test`: behavior reproduced in VirtualDJ locally.
- `Inference`: conclusion drawn from the above sources. Keep these narrow and easy to retest.
- `Needs test`: observed or source-backed, but not yet verified locally.

## Workflow For New Skin Findings

1. Record the skin identity: local path, skin name/version/author from the root `<Skin>` tag, and exact file/line references for each command.
2. Extract all command-like tokens from `action`, `query`, `visibility`, `source`, `textaction`, `rightclick`, `scroll`, `dblclick`, and similar script-bearing attributes.
3. Compare against `Reference/VDJScript Verbs.md` and the current official VDJScript verbs appendix.
4. Search exact terms on virtualdj.com first, then broader web/code search if needed.
5. Add a row here with the status: `Official`, `Official forum`, `Community`, `Published skin`, `Published pad page`, `Local test`, `Needs test`, or a combination.
6. Promote stable, user-facing entries into `VDJScript Verbs.md`, keeping this file as provenance and test notes.

## Denon Prime 4 Deluxe Skin

Local source:

- `/Users/nom/Library/Application Support/VirtualDJ/Skins/Denon Prime 4 Deluxe Skin/PRIME 4.xml`

Skin metadata:

- Root tag: `<Skin name="Denon DJ Prime 4" version="2020" width="1920" height="1080" nbdecks="4" image="gfx-prime.png" preview="skinprevieww.png" author="Alex RD Zaik" ...>`
- Source class: `Published skin`

### Mix FX Commands

The Denon skin uses Mix FX buttons in the master panel:

```xml
<panel class="deck_button_mn"
       action="effect_mixfx_activate &amp; effect_mixfx_select 'FILTER'"
       query="effect_mixfx_select 'FILTER' ? effect_mixfx_activate"/>
```

Observed at lines 1149-1153 for `FILTER`, `ECHO`, `LOOP ROLL`, `REVERB`, and `NOISE`.

| Command | Current understanding | Sources | Test status |
| ------- | --------------------- | ------- | ----------- |
| `effect_mixfx` | Associates an effect with the crossfader / opens or selects Mix FX depending on context. | `Official`; `Official forum`; `Published skin` from the former local `Haunting Pro Edit/Touch.xml` capture | Needs local behavior matrix |
| `effect_mixfx_activate` | Toggles Mix FX globally on/off. Current official docs say to use `effect_mixfx_select` to choose the effect. Forum testing from 2019 says specific effect names are not parameters to this command. | `Official`; `Community`; `Published skin`; `Local test` | Local test confirmed global on/off query; named-parameter behavior still needs retest |
| `effect_mixfx_select` | Selects the Mix FX used while moving the crossfader. Used without a parameter, it returns the selected Mix FX name for display/comparison. Direct boolean queries and indirect `param_equal` queries both tracked the selected Mix FX in current pad XML and skin-query contexts. | `Official`; `Community`; `Published skin`; `Local test` | Local test passed for direct/indirect pad XML query/color and skin button query/visibility on VirtualDJ 8.5.9307 / 850.9336.mac.2224 |

Notes:

- The current official VDJScript verbs appendix contains `effect_mixfx`, `effect_mixfx_activate`, and `effect_mixfx_select`.
- A VirtualDJ hardware manual for the AlphaTheta DDJ-FLX2 says Mix FX can be selected from Starter/Essentials skins and suggests assigning `effect_mixfx_select` to a custom button when another skin lacks Mix FX controls.
- A 2019 forum thread reports that direct boolean queries like `effect_mixfx_select 'echo' ? ...` did not work reliably in that user's testing, and recommends `param_equal "\`effect_mixfx_select\`" "echo" ? ...` for pad LED/color logic. Local testing on May 12, 2026 did not reproduce that limitation in current VirtualDJ.
- The Denon skin uses the direct query form `effect_mixfx_select 'FILTER' ? effect_mixfx_activate`. Current local testing confirms the direct selected-state query is valid in skin XML; the Denon action order remains a published-skin pattern, not a preferred order.

Local test, May 12, 2026:

- Build: VirtualDJ 8.5.9307 / `850.9336.mac.2224`.
- Runnable pad page: [Pads/Reference - Mix FX Query Test.xml](../Pads/Reference%20-%20Mix%20FX%20Query%20Test.xml).
- Runnable skin: [Skins/MixFxQueryTest/skin.xml](../Skins/MixFxQueryTest/skin.xml).
- Setup: installed the pad page into the local VirtualDJ Pads folder, loaded the test skin, switched between `FILTER` and `ECHO`, and read the pad XML state through `pad_button_color`.

| Context | Direct pattern | Indirect pattern | Result |
| ------- | -------------- | ---------------- | ------ |
| Pad XML color/query, selected `FILTER` | `effect_mixfx_select 'FILTER' ? ...` | `param_equal "\`effect_mixfx_select\`" "FILTER" ? ...` | Pad 1 and pad 2 both on/green |
| Pad XML color/query, selected `ECHO` | `effect_mixfx_select 'ECHO' ? ...` | `param_equal "\`effect_mixfx_select\`" "ECHO" ? ...` | Pad 3 and pad 4 both on/blue |
| Skin button `query` | Direct selected effect on; other effect off | Indirect selected effect on; other effect off | Matched |
| Skin `visibility` | Direct selected panel visible; other panel hidden | Indirect selected panel visible; other panel hidden | Matched |

Recommendation: prefer direct `effect_mixfx_select '<name>' ? ...` for selected-state tests in current skins and pad pages. Keep the indirect `param_equal "\`effect_mixfx_select\`" "<name>" ? ...` form for older-build compatibility notes or when the returned name needs to be compared as a value.

## Published Pad Pages

### Loop Recorder

Local source:

- `/Users/nom/Library/Application Support/VirtualDJ/Pads/Loop Recorder.xml`

Observed pattern:

```vdjscript
sampler_loaded 1 auto
sampler_play 1 auto
sampler_stop 1 auto
sampler_select 1 auto
```

The installed `Loop Recorder.xml` pad page uses unquoted `auto` with `sampler_loaded` across pads 1-8 and shifted clear buttons. This is evidence that the form exists in a published/installed pad page, but local diagnostic testing showed it does not make `sampler_loaded 8` page-aware on sampler page `9-16`.

| Pattern | Current understanding | Sources | Test status |
| ------- | --------------------- | ------- | ----------- |
| `sampler_loaded <n> auto` | Used by the published/installed Loop Recorder pad page for the first eight recording pads. Official docs still only document fixed-slot `sampler_loaded <n>`. | `Published pad page`; `Local test` | Unquoted `auto` matched quoted behavior: `sampler_loaded 8 auto` returned true on page `9-16` while slot 16 was empty |

### Other Commands To Reconcile

These were observed in the Denon skin and should be reconciled against the current official appendix and tested where behavior matters.

| Command or family | Denon usage | Current source status | Notes |
| ----------------- | ----------- | --------------------- | ----- |
| `get_effect_slider_label_full`, `get_effect_slider_shortname`, `get_effect_button_shortname`, `effect_has_button` | FX slot display labels and button fallback text around lines 1220-1257 | Official appendix now lists this family | Promoted to broad `VDJScript Verbs.md` Effects catalog |
| `padshift`, `pad_pushed`, `pad_has_param` | Pad grid buttons and pad color/param state around lines 1289-1326 and 205-236 | Official appendix now lists this family | Promoted to broad `VDJScript Verbs.md` Pads catalog |
| `eventscheduler`, `eventscheduler_start` | Event Scheduler button and active state around lines 1188-1195 | Official appendix now lists both | Promoted to broad `VDJScript Verbs.md` Configuration catalog |
| `get_rotation_slip`, `pioneer_cue` | Jog/slip display and cue behavior around lines 54-62 and 765 | Official appendix lists both | Promoted to broad Scratch/Jogwheel and Play/Controller catalogs |
| `booth_volume`, `headphone_crossfader`, `match_gain`, `is_sync` | Mixer and sync controls around lines 346, 1454-1507 | Official appendix lists all four | Promoted to broad Volume/Mixing and Sync catalogs |
| `filter_activate '<name>'` | Master row toggles named ColorFX/filter effects on all decks around lines 1522-1547 | Official/local docs already use `filter_activate`; named parameter behavior needs clearer notes | Test exact names and deck scoping |
| `get_title_before_remix`, `get_harmonic`, `get_loop`, `get_slip_active` | Track title, key, loop, and slip display around lines 925-981 and 552-564 | Official appendix lists this family | Promoted to broad Get, Loops, and Scratch/Jogwheel catalogs |

## External Sources Found For Mix FX

- [Official VDJScript verbs appendix](https://virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html): lists `effect_mixfx`, `effect_mixfx_activate`, and `effect_mixfx_select`.
- [AlphaTheta DDJ-FLX2 hardware manual, Advanced Setup](https://www.virtualdj.com/manuals/hardware/alphatheta/ddjflx2/advanced/index.html): says Mix FX is selected from Starter/Essentials skins and recommends `effect_mixfx_select` for custom buttons in skins without Mix FX controls.
- [VirtualDJ forum, "Saving 'PluginPage' Settings between sessions"](https://www.virtualdj.com/forums/232382/General_Discussion/Saving__PluginPage__Settings_between_sessions.html): community/moderator examples for `effect_mixfx_select`, `effect_mixfx_activate`, and indirect `param_equal` query patterns.
- [VirtualDJ forum, "How to find the scripts behind a skin?"](https://virtualdj.com/forums/261775/VirtualDJ_Technical_Support/How_to_find_the_scripts_behind_a_skin%3F.html): moderator/community replies identify `effect_mixfx`, `effect_mixfx_select`, and `effect_mixfx_activate` as the Mix FX verbs.
- [VirtualDJ forum, "Mix Assist in other skins"](https://www.virtualdj.com/forums/231581/General_Discussion/Mix_Assist__in_other_skins.html): staff/community context for Mix FX behavior.
