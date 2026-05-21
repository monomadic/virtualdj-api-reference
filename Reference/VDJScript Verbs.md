# VirtualDJ VDJScript API Reference

Curated API-oriented reference for VDJScript used in skins, pad pages, custom buttons, and controller mappings.

This file now has two layers:

- The curated API layer at the top: canonical names, aliases, scripting surfaces, and reliability notes.
- The broad catalog below: wide coverage tables that are still being normalized.

## Status

This is the first API pass, not the final exhaustive pass.

The highest-confidence material in this file is the curated layer at the top. It is intentionally biased toward the verbs and patterns that matter most for:

- skin XML
- pad page XML
- custom button actions
- controller mappings
- small inline query and text scripts

Current curated coverage includes:

- flow and timing verbs
- variables and deck targeting
- skin panels and settings
- browser, search, and sideview actions
- transport, cue, loop, and sync controls
- filter and FX selection
- FX stems routing, release controls, and controller-oriented armed FX helpers
- sampler page-aware helpers
- deck assignment and crossfader routing

## Reliability Labels

- `Official`: current VirtualDJ manual or VDJPedia
- `Official forum`: VirtualDJ staff, Development Manager, CTO, or Support staff forum guidance
- `Community`: forum guidance from non-staff users
- `Published skin`: observed in a working public skin; use as provenance and a prompt for testing, not as sole semantic authority
- `Local test`: behavior reproduced in VirtualDJ locally
- `Inference`: a conclusion drawn from official behavior plus repo usage

## Surface Legend

- `Map`: controller mapping
- `Button`: custom button action
- `Pad`: pad page action or query
- `SkinAction`: skin `action=""`, inline button body, or interactive element action
- `SkinQuery`: skin `query=""`, `visibility=""`, `condition=""`, or equivalent boolean/value query slot
- `Text`: skin `text`, `format`, color backticks, or other string/value-returning query usage

These are practical surfaces, not hard type-check guarantees. When a surface is listed, read it as "commonly useful and normally safe there", not "the only place the verb can run".

## Alias Policy

- Use the primary name shown in the current official verbs page as the canonical heading.
- List official aliases explicitly.
- Prefer canonical names in examples unless the alias is the name people are most likely to search for.
- If a synonym is only found in community posts and not in the official manual, label it as community-only rather than treating it as an official alias.

## Published-Skin Evidence Policy

- Preserve commands observed in working public skins even when older local docs do not mention them.
- Always record the skin path, skin metadata, and exact line references before promoting a finding into the curated layer.
- Search the current official manual and VirtualDJ forums for each term; the local Markdown files can lag behind the live docs.
- Mark untested behavior as `Needs local test` instead of deleting or normalizing it away.
- Keep empirical source notes in [Published Skin Findings](Published%20Skin%20Findings.md) so future edits can see why an unfamiliar verb is present.

## Official Appendix Coverage

The local reference now has names-only coverage for all official names tracked in [Official VDJScript Coverage Audit](Official%20VDJScript%20Coverage%20Audit.md). Use that audit before removing or dismissing any unfamiliar command.

Coverage depth is tiered:

- Curated entries near the top are the highest-confidence API notes.
- Broad catalog sections below cover common usage in a compact form.
- The [Official Appendix Remainder](#official-appendix-remainder) section is kept as an audit marker; all tracked official names are currently searchable in functional sections.

Promote compact official entries into curated sections when they become relevant to skins, pads, mappings, published-skin findings, or local tests.

## High-Frequency Alias Index

| Canonical | Official aliases | Notes |
| --------- | ---------------- | ----- |
| `param_bigger` | `param_greater` | Same official entry |
| `skin_panel` | `skin_pannel` | Keep the official spelling as canonical |
| `skin_panelgroup` | `skin_pannelgroup` | Same note as above |
| `lock_panel` | `lock_pannel` | Acts on `<split>`, not `<panel>` |
| `settings` | `config` | Opens the configuration window |
| `filter` | `filter_slider` | Main deck filter / ColorFX amount control |
| `pad_page` | `pad_pages` | Page activation / page menu |
| `pad_page_select` | `pad_page_favorite_select` | Favorite pad-page slot selection |
| `effect_active` | `effect_activate` | Slot activation |
| `effect_slider` | `effect_slider_slider` | Slot slider control |
| `play_button` | `play_3button` | Behavior depends on `playMode` |
| `stop_button` | `stop_3button` | Behavior depends on `playMode` |
| `cue_button` | `cue_3button` | Behavior depends on `cueMode` |
| `smart_play` | `auto_sync` | Startup auto-sync behavior, not the same as `play_sync` |
| `play_sync_onbeat` | `sync_nocbg` | Local-beat sync variant |
| `is_fluid` | `has_variable_bpm` | Fluid-grid query |
| `set_fluid` | `set_variable_bpm` | Fluid-grid toggle |
| `get_sample_name` | `get_sample_slot_name` | Absolute sample-slot label |
| `add_list` | `add_virtualfolder` | Virtual folder creation |
| `info_options` | `infos_options` | Browser info-panel context menu |
| `browser_zoom` | `browser` | Browser zoom control |
| `sampler_unload_from_deck` | `scratchbank_unload` | Unload sample/scratchbank deck and restore previous song |

## Core Execution Model

### Action vs Query vs Dual Verbs

- `Action` verbs primarily do something: `play_pause`, `load`, `skin_panel`
- `Query` verbs primarily return information: `get_browsed_song`, `get_time`, `sampler_loaded`
- `Dual` verbs are often used both ways: `filter`, `setting`, `var`

When a verb is documented here as `Dual`, that means it is commonly used in both action chains and value/query contexts.

### Deck Scoping

VDJScript actions can be prefixed with deck context:

```vdjscript
deck 1 play
deck 2 volume 50%
deck master get_level
```

Use deck scoping whenever the result should be explicit instead of depending on the current focused deck.

Notes:

- `deck master` means "run this in the current master deck context".
- In sampler title and text paths, explicit `deck 1 ... : deck 2 ...` resolution can be more reliable than raw `deck master ...`.

Sources:

- `Official`: current VDJScript verbs appendix, deck examples
- `Official forum`: sampler sync/build-specific discussion around master-deck sampler routing

## Curated High-Frequency Entries

### `up`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Branch on press versus release

Typical forms:

```vdjscript
up ? action_on_press : action_on_release
```

Use when:

- you need separate press/release logic in controller mappings
- you want momentary behavior without relying on vars

Sources:

- `Official`: VDJScript verbs appendix

### `down`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Branch on press versus release

Typical forms:

```vdjscript
down ? action_on_press : action_on_release
```

Preferred usage:

- use for hold-style momentary effects and pad behaviors
- pair with `filter 50%` or another neutral reset on the release side when the control is momentary

Sources:

- `Official`: VDJScript verbs appendix

### `holding`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Branch based on whether the control was held long enough

Typical forms:

```vdjscript
holding ? long_press_action : short_press_action
holding 1000ms ? long_press_action : short_press_action
```

Notes:

- The default threshold is documented as `500ms`.
- Prefer this over hand-rolled timer vars when you only need short-press versus long-press behavior.

Sources:

- `Official`: VDJScript verbs appendix

### `doubleclick`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Branch based on whether the control was pressed twice within the allowed window

Typical forms:

```vdjscript
doubleclick ? double_action : single_action
doubleclick 1000ms ? double_action : single_action
```

Notes:

- The default interval is documented as `300ms`.

Sources:

- `Official`: VDJScript verbs appendix

### `repeat_start`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Start a named repeating task after the first interval passes

Typical forms:

```vdjscript
repeat_start 'scroll' 1000ms & browser_scroll +1
repeat_start 'pulse' 1bt
repeat_start 'name' `get_var interval_ms`
```

Preferred usage:

- use named repeats for background animation, repeated browser movement, and timed FX patterns
- always pair long-lived repeats with a clear `repeat_stop`

Sources:

- `Official`: VDJScript verbs appendix

### `repeat_start_instant`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Start a named repeating task immediately, then keep repeating on the chosen interval

Typical forms:

```vdjscript
repeat_start_instant 'scroll' 250ms & browser_scroll +1
```

Preferred usage:

- use when the first action should happen right away rather than after the first delay

Sources:

- `Official`: VDJScript verbs appendix

### `repeat_stop`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Stop a repeat created with `repeat_start` or `repeat_start_instant`

Typical forms:

```vdjscript
repeat_stop 'scroll'
```

Sources:

- `Official`: VDJScript verbs appendix

### `wait`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Delay the next action in a chain

Typical forms:

```vdjscript
wait 1bt & pause
wait 500ms & play
```

Notes:

- Use it for simple timed chains.
- If you need a persistent process, prefer named repeats instead of stacking many waits.

Sources:

- `Official`: VDJScript verbs appendix

### `blink`

Aliases: none

Kind: `Dual`

Typical surfaces: `Map`, `Pad`, `SkinQuery`

Official summary:

- Toggle LED or visual state on and off at a configurable rate

Typical forms:

```vdjscript
blink
blink 1000ms
blink 1bt
blink 1bt 25%
```

Preferred usage:

- use as the true branch in queries: `effect_active 1 ? blink 1bt : off`

Sources:

- `Official`: VDJScript verbs appendix

### `param_bigger`

Aliases: `param_greater`

Kind: `Dual`

Typical surfaces: `Map`, `Pad`, `SkinQuery`, `Text`

Official summary:

- Compare the caller value against a value or another action result

Typical forms:

```vdjscript
param_bigger 0 ? action1 : action2
param_bigger pitch pitch_slider
```

Preferred usage:

- use the canonical manual name `param_bigger` in docs
- mention `param_greater` when helping users search or migrate older scripts

Sources:

- `Official`: VDJScript verbs appendix

### `param_equal`

Aliases: none

Kind: `Dual`

Typical surfaces: `Map`, `Pad`, `SkinQuery`, `Text`

Official summary:

- Compare the caller value or the first parameter value against another value

Typical forms:

```vdjscript
param_equal `get_browsed_song 'type'` "audio"
param_equal 0.5 filter ? on : off
```

Preferred usage:

- use backticks when the compared value comes from another action
- prefer this over brittle string slicing or var mirrors when the source action already returns the value you need

Sources:

- `Official`: VDJScript verbs appendix

### `var`

Aliases: none

Kind: `Dual`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinQuery`, `Text`

Official summary:

- Test whether a variable is true

Typical forms:

```vdjscript
var "my_var" ? action1 : action2
```

Notes:

- Use vars when you truly need stored state across events.
- Do not reach for vars when a built-in query verb already answers the question directly.

Sources:

- `Official`: VDJScript verbs appendix
- `Community`: experienced skin scripters repeatedly caution against overusing vars when a built-in UI/query path already exists

### `set`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Set a variable to a value

Typical forms:

```vdjscript
set 'varname' 5
set 'page_fx_active' 1
set 'remembered_filter' `filter`
```

Notes:

- Use for stored state, not as a substitute for native UI or deck state queries.

Sources:

- `Official`: VDJScript verbs appendix, variable section

### `toggle`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Toggle a variable between true and false

Typical forms:

```vdjscript
toggle "my_var"
```

Preferred usage:

- good for explicit user modes
- avoid using it when the target should mirror a built-in state such as `play`, `loop`, or `masterdeck`

Sources:

- `Official`: VDJScript verbs appendix

### `get_var`

Aliases: none

Kind: `Query`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinQuery`, `Text`

Official summary:

- Return the value of a named variable

Typical forms:

```vdjscript
get_var 'varname'
```

Sources:

- `Official`: VDJScript verbs appendix

### `set_deck`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Use a script result or implicit value to decide which deck the following action applies to

Typical forms:

```vdjscript
set_deck `get_var target_deck` & play
```

Preferred usage:

- use in mappings when the target deck is computed at runtime
- prefer explicit `deck 1 ...`, `deck 2 ...`, or `deck master ...` when the target is already known

Sources:

- `Official`: VDJScript verbs appendix

### `skin_panel`

Aliases: `skin_pannel`

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Show or hide a named panel

Typical forms:

```vdjscript
skin_panel 'my_panel' on
skin_panel 'my_panel' off
```

Preferred usage:

- use for explicit panel toggles
- if panel visibility should simply follow a live condition, prefer panel `visibility=""` or other query-driven skin logic instead of setting extra vars only to call `skin_panel`

Sources:

- `Official`: VDJScript verbs appendix
- `Official`: Skin SDK panel documentation

### `skin_panelgroup`

Aliases: `skin_pannelgroup`

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Switch which panel in a named group is shown

Typical forms:

```vdjscript
skin_panelgroup 'rack' 'fx'
skin_panelgroup 'rack' +1
skin_panelgroup 'rack' 0.75
```

Preferred usage:

- use when the user is deliberately switching between remembered panel modes
- use `skin_panelgroup_available` to keep unavailable panels out of cycles

Sources:

- `Official`: VDJScript verbs appendix
- `Official`: Skin SDK panel documentation

### `lock_panel`

Aliases: `lock_pannel`

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Despite the name, this acts on `<split>` elements rather than `<panel>`

Notes:

- Document this quirk explicitly wherever the verb is mentioned.

Sources:

- `Official`: VDJScript verbs appendix

### `setting`

Aliases: none

Kind: `Dual`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`, `SkinQuery`, `Text`

Official summary:

- Read or write a specific VirtualDJ setting

Typical forms:

```vdjscript
setting "jogSensitivityScratch" 80%
setting "videoRandomTransition" on
setting "filterDefaultResonance"
```

Preferred usage:

- prefer it for actual program settings such as `filterDefaultResonance`
- do not use settings as a substitute for temporary UI state that belongs in a script variable or a panel selection

Sources:

- `Official`: VDJScript verbs appendix
- `Official forum`: `setting filterDefaultResonance` recommended by CTO Adion for filter resonance scripting

### `settings`

Aliases: `config`

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Open the configuration window

Sources:

- `Official`: VDJScript verbs appendix

### `display_time`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Set the displayed time mode to `total`, `remain`, `elapsed`, `+1`, or `-1`

Typical forms:

```vdjscript
display_time 'remain'
display_time 'remain,elapsed'
display_time +1
```

Preferred usage:

- prefer this over custom elapsed/remain vars when the goal is simply to switch the time-display mode

Sources:

- `Official`: VDJScript verbs appendix
- `Inference`: prefer the built-in time-display mode before inventing a parallel time-mode variable

### `get_time`

Aliases: none

Kind: `Query`

Typical surfaces: `SkinQuery`, `Text`, `Map`, `Button`

Official summary:

- Return elapsed, remaining, or total time, with optional unit and target-point arguments

Typical forms:

```vdjscript
get_time
get_time 'remain'
get_time 'remain' 'short'
get_time 1000
get_time 'absolute'
```

Notes:

- `get_time` follows the current `display_time` mode unless you explicitly pass `elapsed`, `remain`, or `total`.
- The official verbs appendix also lists target-point forms such as `get_time 'to_lyrics'`. Treat `to_lyrics` as useful but lightly documented; verify exact return behavior in the target skin/build before designing around it.

Sources:

- `Official`: VDJScript verbs appendix

### Time Component Queries

Use these when a skin needs separate time fields instead of the formatted string from `get_time`.

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `get_time_sign` | `Text`, `SkinQuery` | Return `-1` or `+1` for elapsed/remain/total time according to `display_time`. | `get_time_sign 'remain'` |
| `get_time_hour` | `Text`, `SkinQuery` | Hour component of elapsed/remain/total time. | `get_time_hour 'elapsed'` |
| `get_time_min` | `Text`, `SkinQuery` | Minute component of elapsed/remain/total time. | `get_time_min 'remain'` |
| `get_time_sec` | `Text`, `SkinQuery` | Second component of elapsed/remain/total time. | `get_time_sec 'remain'` |
| `get_time_ms` | `Text`, `SkinQuery` | Hundredth-second component of elapsed/remain/total time. | `get_time_ms 'elapsed'` |
| `get_time_msf` | `Text`, `SkinQuery` | Frame component of elapsed/remain/total time. | `get_time_msf 'elapsed'` |
| `get_totaltime_min` | `Text`, `SkinQuery` | Minute component of total track length. | `get_totaltime_min` |
| `get_totaltime_sec` | `Text`, `SkinQuery` | Second component of total track length. | `get_totaltime_sec` |
| `get_totaltime_ms` | `Text`, `SkinQuery` | Hundredth-second component of total track length. | `get_totaltime_ms` |
| `get_totaltime_msf` | `Text`, `SkinQuery` | Frame component of total track length. | `get_totaltime_msf` |
| `get_songlength` | `Text`, `SkinQuery` | Total track length in seconds. | `get_songlength` |

Notes:

- Most `get_time_*` verbs follow `display_time`; pass `elapsed`, `remain`, or `total` to bypass the current display mode.
- Use the broader `get_time` entry for formatted text and arbitrary unit conversion.

Sources:

- `Official`: VDJScript verbs appendix

### Loaded Track Metadata Queries

These query the track loaded on the current deck, unlike `get_browsed_*`, which follows the browser selection.

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `get_filepath` | `Text`, `SkinQuery` | Full file path of the loaded song. | `get_filepath` |
| `get_filename` | `Text`, `SkinQuery` | File name of the loaded song. | `get_filename` |
| `get_filesize` | `Text`, `SkinQuery` | File size of the loaded song. | `get_filesize` |
| `get_composer` | `Text`, `SkinQuery` | Composer tag of the loaded song. | `get_composer` |
| `get_year` | `Text`, `SkinQuery` | Year tag of the loaded song. | `get_year` |
| `get_artist_title` | `Text`, `SkinQuery` | Combined artist-title text for the loaded song. | `get_artist_title` |
| `get_title_artist` | `Text`, `SkinQuery` | Combined title-artist text for the loaded song. | `get_title_artist` |
| `get_title_remix` | `Text`, `SkinQuery` | Title plus remix in parentheses. | `get_title_remix` |
| `get_artist_before_feat` | `Text`, `SkinQuery` | Artist text before a featuring separator. | `get_artist_before_feat` |
| `get_featuring_after_artist` | `Text`, `SkinQuery` | Featuring text after the artist. | `get_featuring_after_artist` |
| `get_artist_title_separator` | `Text`, `SkinQuery` | Separator used in combined artist/title display. | `get_artist_title_separator` |
| `get_loaded_song_color` | `Text`, `SkinQuery` | Color of the loaded track, including color filters. | `get_loaded_song_color 'white'` |
| `has_cover` | `SkinQuery`, `Button` | True when cover art is available. | `has_cover` |
| `has_linked_tracks` | `SkinQuery`, `Button` | True when the track has links to other tracks. | `has_linked_tracks` |

Notes:

- `get_loaded_song_color` includes color filters; use `get_loaded_song color` when you specifically want the manually selected track color.
- `has_linked_tracks browsed` checks the browsed track; it can also take a script that returns a full file path.

Sources:

- `Official`: VDJScript verbs appendix

### Beatgrid And Position Queries

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `get_firstbeat` | `Text`, `SkinQuery` | Position of the first beat in milliseconds. | `get_firstbeat` |
| `get_firstbeat_local` | `Text`, `SkinQuery` | First beat of the current 16-beat phrase, in milliseconds. | `get_firstbeat_local` |
| `get_beat` | `Text`, `SkinQuery` | Beat intensity at the current playback position, from `0%` to `100%`. | `get_beat` |
| `get_beatgrid` | `Text`, `SkinQuery` | Beat intensity from the beatgrid. | `get_beatgrid` |
| `get_beatdiff` | `Text`, `SkinQuery` | Beat distance between this deck and the active deck. | `get_beatdiff` |
| `get_beat2` | `Text`, `SkinQuery` | Beat helper variant from the official beat query family. | `get_beat2` |
| `get_beat_counter` | `Text`, `SkinQuery` | Current beat-counter position. | `get_beat_counter` |
| `get_beat_num` | `Text`, `SkinQuery` | Current beat number in the measure, or phrase-position query with parameters. | `get_beat_num 1` |
| `get_phrase_num` | `Text`, `SkinQuery` | Current measure number inside the phrase. | `get_phrase_num` |
| `get_bar` | `Text`, `SkinQuery` | Current bar number. | `get_bar` |
| `get_beat_bar` | `Text`, `SkinQuery` | Percentage position inside the bar. | `get_beat_bar 16` |

Sources:

- `Official`: VDJScript verbs appendix

Notes:

- Use `get_beat` for a live beat-intensity value at the current position.
- Use `get_beatgrid` when the value should be tied to the beatgrid position: `100%` on beat, `0%` halfway between beats.

### Deck And Environment Queries

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `get_activedeck` | `Text`, `SkinQuery` | Number of the active deck. | `get_activedeck` |
| `get_deck_letter` | `Text`, `SkinQuery` | Letter of the current deck. | `get_deck_letter` |
| `get_decks` | `Text`, `SkinQuery` | Number of visible/available decks. | `get_decks` |
| `get_defaultdeck` | `Text`, `SkinQuery` | Number of the default deck. | `get_defaultdeck` |
| `get_leftdeck` | `Text`, `SkinQuery` | Number of the deck assigned to the left side. | `get_leftdeck` |
| `get_rightdeck` | `Text`, `SkinQuery` | Number of the deck assigned to the right side. | `get_rightdeck` |
| `get_plugindeck` | `Text`, `SkinQuery` | Plugin context deck number, with special values for master/sampler/mic. | `get_plugindeck` |
| `get_display` | `Text`, `SkinQuery` | Display identifier for the current skin or screen context. | `get_display` |
| `get_version` | `Text`, `SkinQuery` | VirtualDJ version text. | `get_version` |
| `get_build` | `Text`, `SkinQuery` | VirtualDJ build number. | `get_build` |
| `get_vdj_folder` | `Text`, `SkinQuery` | VirtualDJ home folder. | `get_vdj_folder` |
| `get_username` | `Text`, `SkinQuery` | Current VirtualDJ account username. | `get_username` |
| `get_membership` | `Text`, `SkinQuery` | Current VirtualDJ membership text. | `get_membership` |
| `get_license` | `Text`, `SkinQuery` | Current VirtualDJ license text. | `get_license` |
| `get_lemode` | `SkinQuery`, `Text` | True when VirtualDJ is running in Limited Edition mode. | `get_lemode` |
| `get_hwnd` | `Text`, `SkinQuery` | Windows handle for the VirtualDJ window. | `get_hwnd` |
| `get_skin_color` | `Text`, `SkinQuery` | Skin theme/default color helper. | `get_skin_color` |
| `skin_width` | `Text`, `SkinQuery` | Current skin width. | `skin_width` |
| `skin_height` | `Text`, `SkinQuery` | Current skin height. | `skin_height` |
| `skin_starter_tip` | `Text`, `SkinQuery` | Starter-skin tip helper. | `skin_starter_tip` |
| `has_logo` | `SkinQuery`, `Button` | True when the current skin/logo context exposes a logo. | `has_logo` |
| `getfood` | `Action` | Official joke/helper entry; do not build serious workflow logic around it. | `getfood` |

Sources:

- `Official`: VDJScript verbs appendix

### Input And Output Availability Queries

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `get_hasheadphone` | `SkinQuery`, `Text` | Headphone-output availability helper. | `get_hasheadphone` |
| `get_hasheadphones` | `SkinQuery`, `Text` | Headphone-output availability helper. | `get_hasheadphones` |
| `get_hasinput` | `SkinQuery`, `Text` | Input availability helper. | `get_hasinput` |
| `get_haslinein` | `SkinQuery`, `Text` | Line-input availability helper. | `get_haslinein` |
| `get_hasmaster` | `SkinQuery`, `Text` | Master-output availability helper. | `get_hasmaster` |
| `get_hasmic` | `SkinQuery`, `Text` | Microphone availability helper. | `get_hasmic` |
| `has_aux` | `SkinQuery`, `Button` | True when an aux input/path is available. | `has_aux` |
| `has_video_mix` | `SkinQuery`, `Button` | True when video mixing is available or active. | `has_video_mix` |

Sources:

- `Official`: VDJScript verbs appendix

### Recording Queries

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `get_record_message` | `Text`, `SkinQuery` | Message displayed on the record page. | `get_record_message` |
| `get_record_size` | `Text`, `SkinQuery` | Current size of the recording file. | `get_record_size` |
| `get_record_min` | `Text`, `SkinQuery` | Minute component of recording time. | `get_record_min` |
| `get_record_sec` | `Text`, `SkinQuery` | Second component of recording time. | `get_record_sec` |
| `get_record_ms` | `Text`, `SkinQuery` | Millisecond/hundredth component of recording time. | `get_record_ms` |
| `get_record_msf` | `Text`, `SkinQuery` | Frame component of recording time. | `get_record_msf` |

Sources:

- `Official`: VDJScript verbs appendix

### Audio Analysis And Visualization Queries

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `get_arm` | `Text`, `SkinQuery` | Position of the turntable arm. | `get_arm` |
| `get_peak_audio` | `Text`, `SkinQuery` | Peak audio helper for skin/system displays. | `get_peak_audio` |
| `get_spectrum_band` | `Text`, `SkinQuery` | Level of a single spectrum band. | `get_spectrum_band 1 32 vocals` |
| `get_volume` | `Text`, `SkinQuery` | Effective volume after volume sliders and crossfader. | `get_volume` |
| `get_deck_analysis` | `Text`, `SkinQuery` | Analysis helper for current or upcoming song events. | `get_deck_analysis` |
| `get_song_event` | `Text`, `SkinQuery` | Current or next song-event data for visualization plugins. | `get_song_event current volume` |
| `get_custom_text` | `Text`, `SkinQuery` | Custom text helper. | `get_custom_text` |

Notes:

- `get_spectrum_band` defaults to 32 bands; pass a second parameter for a different band count.
- The third `get_spectrum_band` parameter can request a stem-aware spectrum such as `vocals`.
- `get_song_event` accepts `current` or `next`, then an event field such as `hasbeats`, `volume`, `volume_end`, or `remaining`.

Sources:

- `Official`: VDJScript verbs appendix

### Controller Display And Platter Queries

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `get_controller_screen` | `Text`, `SkinQuery` | Controller-screen helper for mappings and controller display scripts. | `get_controller_screen` |
| `get_ns7_platter` | `Text`, `SkinQuery` | NS7 platter display/helper query. | `get_ns7_platter` |
| `ns7_platter` | `Action` | NS7 platter helper for controller mappings. | `ns7_platter` |
| `get_nb_multicam` | `Text`, `SkinQuery` | Number of multicam sources/helper value. | `get_nb_multicam` |
| `get_scratch_direction` | `Text`, `SkinQuery` | Current scratch direction helper. | `get_scratch_direction` |

Sources:

- `Official`: VDJScript verbs appendix

### AskTheDJ And Karaoke Queries

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `get_askthedj` | `Text`, `SkinQuery` | Latest Ask The DJ request, or an indexed older request. | `get_askthedj 2` |
| `get_askthedj_unread` | `Text`, `SkinQuery` | Count of unread Ask The DJ requests. | `get_askthedj_unread` |
| `get_karaoke_background_song` | `Text`, `SkinQuery` | Karaoke background song helper. | `get_karaoke_background_song` |
| `has_karaoke_next` | `SkinQuery`, `Button` | True when there is another karaoke song queued. | `has_karaoke_next` |

Notes:

- AskTheDJ queries require the Ask The DJ monitoring setting to be active.

Sources:

- `Official`: VDJScript verbs appendix

### Key And Cue Helper Queries

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `get_key_modifier` | `Text`, `SkinQuery` | Semitone shift currently applied to the song. | `get_key_modifier` |
| `get_key_modifier_text` | `Text`, `SkinQuery` | Text display of the current semitone shift. | `get_key_modifier_text` |
| `get_cue` | `Text`, `SkinQuery` | Current cue helper value. | `get_cue` |
| `get_saved_loop` | `Text`, `SkinQuery` | Saved-loop helper value. | `get_saved_loop` |
| `keycue_pad` | `Pad`, `SkinAction`, `Text` | Key-cue pad action/display helper. | `keycue_pad 1`, `` `keycue_pad 1` `` |
| `keycue_pad_color` | `Pad`, `SkinQuery` | Color for a key-cue pad slot. | `keycue_pad_color 1` |
| `keycue_pad_page` | `Pad`, `Text` | Change or query the key-cue pad page/window. | `keycue_pad_page` |
| `keycue_pad_jump` | `Pad`, `SkinAction` | Key-cue option for jumping to the cue while applying the key cue. | `keycue_pad_jump` |
| `get_timecode_quality` | `Text`, `SkinQuery` | Timecode signal quality helper. | `get_timecode_quality` |

Notes:

- The official Keycue pad page uses `keycue_pad <n>` as both pad action and backtick label, `keycue_pad_color <n>` for pad color, `keycue_pad_page` as Parameter 1, and `keycue_pad_jump` in the page menu.

Sources:

- `Official`: VDJScript verbs appendix
- `Official`: `examples/pads/official/pads_keycue.xml`

### `get_browsed_song`

Aliases: none

Kind: `Query`

Typical surfaces: `Button`, `Pad`, `SkinQuery`, `Text`

Official summary:

- Return a property from the currently browsed file

Typical forms:

```vdjscript
get_browsed_song 'title'
get_browsed_song 'type'
```

Preferred usage:

- pair with `param_equal` when branching on browsed-file metadata

Sources:

- `Official`: VDJScript verbs appendix

### `has_lyrics`

Aliases: none

Kind: `Query`

Typical surfaces: `SkinQuery`, `Text`, `Button`, `Pad`

Official summary:

- Return true when the song loaded on the deck has lyrics.

Typical forms:

```vdjscript
has_lyrics
deck 1 has_lyrics
has_lyrics ? edit_lyrics : nothing
```

Notes:

- This is deck-scoped. Do not assume it tests the browsed browser row.
- For browser filtering, use the browser/filter field such as the "Has Lyrics" instant filter.
- In skins, this is the safest styling hook for lyric availability badges.

Sources:

- `Official`: VDJScript verbs appendix
- `Official forum`: "Has Lyrics" browser filter quirks in VirtualDJ 2026 forum thread

### `get_lyrics_language`

Aliases: none

Kind: `Query`

Typical surfaces: `SkinQuery`, `Text`

Official summary:

- Return the language of the lyrics loaded on the deck.

Typical forms:

```vdjscript
get_lyrics_language
param_equal `get_lyrics_language` "en" ? action1 : action2
```

Notes:

- Good for a compact language chip or conditional color.
- It does not expose AI confidence, source, edited status, or translation details.

Sources:

- `Official`: VDJScript verbs appendix

### `edit_lyrics`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Open the Lyrics Editor for the track loaded on the deck.

Typical forms:

```vdjscript
edit_lyrics
```

Notes:

- The editor can be useful even when lyrics are missing or wrong, so do not automatically hide every editor control behind `has_lyrics`.
- There is no documented separate "reanalyze lyrics" verb in the checked sources; re-analysis is exposed in the editor UI.

Sources:

- `Official`: VDJScript verbs appendix
- `Official`: Lyrics Editor manual

### `get_status`

Aliases: none

Kind: `Query`

Typical surfaces: `Text`, `SkinQuery`

Official summary:

- Return information about background tasks.

Typical forms:

```vdjscript
get_status
```

Notes:

- Probe this in the target build before displaying it. It may be useful for generic analysis/stems status, but no checked source guarantees a stable lyrics-specific status string.

Sources:

- `Official`: VDJScript verbs appendix

### `var_list`

Aliases: none

Kind: `Action`

Typical surfaces: `Button`, `Pad`, `Map`

Official summary:

- Show a window listing current variables and values.

Typical forms:

```vdjscript
var_list
```

Notes:

- A forum debugging pattern is to scatter temporary `set` calls through a complicated script, then inspect `var_list` to see which path ran.

Sources:

- `Official`: VDJScript verbs appendix
- `Community`: scripting-reference forum debugging guidance

### `load`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Load the selected song, or a specified full path, onto the deck

Typical forms:

```vdjscript
load
load "/path/to/file.mp3"
```

Sources:

- `Official`: VDJScript verbs appendix

### `play`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Start the deck

Typical forms:

```vdjscript
play
```

Sources:

- `Official`: VDJScript verbs appendix

### `play_stutter`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- If paused, start the deck. If playing, restart from the last stutter point.

Typical forms:

```vdjscript
play_stutter
```

Preferred usage:

- use when the control should deliberately retrigger from the stutter point
- for ordinary transport start behavior, prefer plain `play` or `play_pause`

Sources:

- `Official`: VDJScript verbs appendix

### `play_pause`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Start the deck if paused; pause it if playing

Typical forms:

```vdjscript
play_pause
```

Sources:

- `Official`: VDJScript verbs appendix

### `pause`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Pause the deck

Typical forms:

```vdjscript
pause
```

Sources:

- `Official`: VDJScript verbs appendix

### `stop`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Stop to the last cue point, then on second press to the beginning of the song, then cycle through the cue points

Typical forms:

```vdjscript
stop
```

Important note:

- This is not a simple synonym for `pause`.
- For deterministic documentation, spell out `stop`, `pause`, or `pause_stop` based on the behavior you actually want.

Sources:

- `Official`: VDJScript verbs appendix

### `cue_stop`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- If playing, pause and go to the last cue point. If paused, set the current position as cue and preview while pressed.

Typical forms:

```vdjscript
cue_stop
cue_stop 1
cue_stop 57
```

Sources:

- `Official`: VDJScript verbs appendix

### `pitch_reset`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Slowly bring the deck pitch back to zero/original speed

Typical forms:

```vdjscript
pitch_reset
pitch_reset 5%
pitch_reset 500ms
pitch_reset 4bt
```

Pad-page status pattern:

```xml
<pad13 name="RESET PITCH `get_text '%Ppitch%'`" autodim="false" color="loaded ? get_pitch_value &amp; param_bigger 125 ? color 'red' : get_pitch_value &amp; param_smaller 75 ? color 'red' : get_pitch_value &amp; param_bigger 105 ? color 'yellow' : get_pitch_value &amp; param_smaller 95 ? color 'yellow' : color 'green' : color 'black'" query="loaded ? get_pitch_value &amp; param_bigger 125 ? blink 500ms : get_pitch_value &amp; param_smaller 75 ? blink 500ms : on : off">pitch_reset 4bt</pad13>
```

Notes:

- For `get_pitch_value` comparisons in pad-page XML, use bare numeric thresholds such as `125`, `75`, `105`, and `95`.
- Do not write these thresholds as `125%` / `75%` in this pattern; local testing showed that can make the red branch match incorrectly.
- Keep colors in `color=""` and blink state in `query=""`.

Sources:

- `Official`: VDJScript verbs appendix
- `Local test`: 16-pad reset-pitch pad XML

### `get_pitch`

Aliases: none

Kind: `Query`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinQuery`, `Text`

Official summary:

- Return the current deck pitch value

Typical forms:

```vdjscript
get_pitch
get_pitch & param_multiply -1
```

Full pad-page reset pattern with inverse-pitch label:

```xml
<pad13 name="`get_pitch_zero ? get_text 'RESET BPM (0%)' : get_pitch &amp; param_smaller 0 ? get_text 'RESET BPM (+`get_pitch &amp; param_multiply -1`%)' : get_text 'RESET BPM (-`get_pitch`%)'`" autodim="false" color="loaded ? get_pitch_value &amp; param_bigger 125 ? color 'red' : get_pitch_value &amp; param_smaller 75 ? color 'red' : get_pitch_value &amp; param_bigger 105 ? color 'yellow' : get_pitch_value &amp; param_smaller 95 ? color 'yellow' : color 'green' : color 'black'" query="loaded ? get_pitch_value &amp; param_bigger 125 ? blink 500ms : get_pitch_value &amp; param_smaller 75 ? blink 500ms : on : off">pitch_reset 4bt</pad13>
```

This displays the inverse pitch with an explicit positive sign when needed:

```text
get_pitch = +18   -> RESET BPM (-18%)
get_pitch = -15.7 -> RESET BPM (+15.7%)
get_pitch = 0     -> RESET BPM (0%)
```

Notes:

- `get_pitch` returns pitch points suitable for display/math such as `18` or `15.7`; it is not a normalized decimal ratio.
- Do not run `get_pitch & param_cast "percentage"` when you only want a pitch label. Local pad-label testing showed it scales the value again, producing outputs such as `2146%` or `-2018.45%`.
- `get_pitch & param_multiply -1` flips the numeric sign, but it will not add a visible `+` for positive results and can display `-0`; use a separate sign expression and `get_pitch_zero` when the label must be polished.
- In pad page XML and skin XML attributes, write chain separators as `&amp;`; raw `&` is only for plain VDJScript outside XML.

Sources:

- `Official`: VDJScript verbs appendix
- `Local test`: pad-label output samples for inverse reset-BPM text

### `get_pitch_value`

Aliases: none

Kind: `Query`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinQuery`, `Text`

Official summary:

- Return pitch on a `0` to `200` scale, centered on `100` for original speed

Typical forms:

```vdjscript
get_pitch_value
get_pitch_value & param_bigger 125 ? action1 : action2
get_pitch_value & param_smaller 75 ? action1 : action2
```

Preferred usage:

- Use `get_pitch_value` rather than raw BPM math when the question is "how far is this deck from the track's original tempo?"
- In pad-page XML comparisons, pair it with bare numeric thresholds and escape `&` as `&amp;`.

Sources:

- `Official`: VDJScript verbs appendix
- `Local test`: 16-pad reset-pitch pad XML

### `pad_page`

Aliases: `pad_pages`

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Activate a pad page, override a page slot, or show the pad-page selector menu

Typical forms:

```vdjscript
pad_page 1
pad_page 1 hotcues
pad_page btn1
pad_page
```

Preferred usage:

- use the canonical singular name `pad_page` in docs
- call out `pad_pages` as the official alias for searchability

Sources:

- `Official`: VDJScript verbs appendix

### `filter`

Aliases: `filter_slider`

Kind: `Dual`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`, `SkinQuery`, `Text`

Official summary:

- Apply the selected ColorFX to the sound; nothing is applied at `50%`, and more is applied the farther from center

Typical forms:

```vdjscript
filter
filter 50%
filter 75%
down ? filter 75% : filter 50%
```

Preferred usage:

- for the main deck filter path, pair it with `filter_selectcolorfx`
- document `50%` as neutral; do not normalize docs around `0%` as if it were the center-off value

Sources:

- `Official`: VDJScript verbs appendix

### `filter_selectcolorfx`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Select the ColorFX controlled by the filter knob

Typical forms:

```vdjscript
filter_selectcolorfx 'Echo'
filter_selectcolorfx +1
filter_selectcolorfx -1
```

Preferred usage:

- use this as the main documented way to choose the deck's ColorFX
- prefer it over ad-hoc `effect_show_gui 'colorfx'` workflows when the goal is simply to set the selected ColorFX

Quirk:

- CTO Adion explicitly recommends `filter_selectcolorfx` to avoid duplicated filter states when switching ColorFX/filter behaviors.

Sources:

- `Official`: VDJScript verbs appendix
- `Official forum`: "Default filter and color fx filter", Adion, 2023-05-19

### `filter_label`

Aliases: none

Kind: `Query`

Typical surfaces: `SkinQuery`, `Text`, `Button`, `Pad`

Official summary:

- Return the label shown under the filter knob

Typical forms:

```vdjscript
filter_label
filter_label 'clean'
filter_label 'name'
```

Preferred usage:

- use `filter_label 'name'` when you specifically want the ColorFX name rather than the value-style label

Sources:

- `Official`: VDJScript verbs appendix

### `filter_resonance`

Aliases: none

Kind: `Dual`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`, `SkinQuery`

Official summary:

- Change the filter resonance

Typical forms:

```vdjscript
filter_resonance 50%
filter_resonance +5%
filter_resonance -5%
```

Preferred usage:

- use for live control of resonance
- use `setting 'filterDefaultResonance' ...` when what you really want is the program setting, not a one-off movement

Sources:

- `Official`: VDJScript verbs appendix
- `Official`: options list
- `Official forum`: filter resonance discussion in the ColorFX/filter thread

### `effect_select`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Select an effect in a slot and deactivate the previous effect in that slot

Typical forms:

```vdjscript
effect_select 1 "echo"
effect_select 1 -1
effect_select +1
effect_select 1 0.2
```

Preferred usage:

- use slot-based effect selection for deterministic pad pages and skins
- prefer this over name-only global assumptions when you care which slot owns the effect
- for pad presets, pair `effect_select <slot> '<name>'` with explicit `effect_slider <slot> ...` values before activating the slot
- do not use bare `effect_select <slot>` as a harmless selected-name query in pad actions; it can open the effect selector. Use `get_effect_name <slot>` for labels and state checks.

Sources:

- `Official`: VDJScript verbs appendix

### `effect_active`

Aliases: `effect_activate`

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`, `SkinQuery`

Official summary:

- Activate or deactivate the effect on a specific slot

Typical forms:

```vdjscript
effect_active 1
effect_active 1 on
effect_active 1 off
effect_active 1 'flanger' on
```

Preferred usage:

- keep docs slot-centric when describing normal deck FX behavior
- mention the alias, but keep `effect_active` as canonical
- name-based forms such as `effect_active 'echo'` are valid shortcuts, but reference pad pages should use slots when they need predictable LED state and parameter ownership
- if a pad label names a specific effect, query both `get_effect_name <slot>` and `effect_active <slot>` so a different active effect in the same slot does not light the wrong pad
- turn a slot effect off with `effect_active <slot> off`
- for same-pad preset toggles, query `get_effect_name <slot>` first, then nest `effect_active <slot>` so pressing the same active effect turns the slot off while pressing a different effect loads/sets/activates it
- `&&` is documented for query chains, but use nested conditionals for action branches that combine effect-name checks, `? :`, and load/set/on side effects

Sources:

- `Official`: VDJScript verbs appendix

### `effect_slider`

Aliases: `effect_slider_slider`

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Move a specific slider on the effect loaded in a given slot

Typical forms:

```vdjscript
effect_slider 1 2 50%
effect_slider 1 0%
```

Preferred usage:

- use explicit slot and slider numbers in docs and examples
- pair with `effect_select` and `effect_active` for deterministic FX presets
- avoid setting sliders by effect name in reference examples unless the example intentionally targets any active instance of that named effect

Sources:

- `Official`: VDJScript verbs appendix

### `effect_colorfx`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Select an effect for one of up to four custom ColorFX slots

Typical forms:

```vdjscript
effect_colorfx 1 "echo"
```

Preferred usage:

- use when building extra ColorFX-like controls that should not hijack the main deck filter path

Quirk:

- This is not the same thing as selecting the standard deck filter ColorFX. For that, prefer `filter_selectcolorfx`.

Sources:

- `Official`: VDJScript verbs appendix
- `Official forum`: ColorFX/filter guidance from staff and CTO posts

### `effect_colorslider`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Control an effect from a center-off position to full on left or right

Typical forms:

```vdjscript
effect_colorslider 1
```

Preferred usage:

- pair it with `effect_colorfx` for custom ColorFX-style controls

Sources:

- `Official`: VDJScript verbs appendix

### `colorfx_slider`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Adjust the ColorFX parameter

Typical forms:

```vdjscript
colorfx_slider
colorfx_slider 50%
```

Preferred usage:

- use `filter` for the normal deck filter / selected ColorFX amount path
- use `colorfx_slider` when mapping a dedicated ColorFX parameter control exposed by a controller or skin

Sources:

- `Official`: VDJScript verbs appendix

### `effect_releaseslider`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Control the effect release-specific slider

Typical forms:

```vdjscript
effect_releaseslider
effect_releaseslider 50%
```

Preferred usage:

- treat this as a release-FX-specific control path, separate from normal slot sliders
- use `is_releasefx` when the UI needs to know whether the current effect is in the release-FX slot

Sources:

- `Official`: VDJScript verbs appendix

### `effect_releaseslider_active`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Control the effect release-specific slider and automatically activate the effect

Typical forms:

```vdjscript
effect_releaseslider_active
effect_releaseslider_active 50%
```

Preferred usage:

- use for momentary-style release-FX controls that should activate while the slider is being moved
- keep normal effect-slot controls on `effect_slider` / `effect_slider_active`

Sources:

- `Official`: VDJScript verbs appendix

### `effect_stems`

Aliases: none

Kind: `Dual`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`, `SkinQuery`, `Text`

Official summary:

- Apply effects only to selected stems

Typical forms:

```vdjscript
effect_stems vocal on
effect_stems 'melody'
effect_stems off
effect_stems ? on : off
```

Preferred usage:

- use when a pad page or skin intentionally routes audio FX to part of the track instead of the full deck signal
- use `effect_stems off` to return FX routing to the full track
- in skin and pad state, query `effect_stems '<stem>'` when you need a specific route and query bare `effect_stems` when any stem-FX route should count as active

Notes:

- Official stem names are `Vocal`, `HiHat`, `Bass`, `Instru`, `Kick`, `Melody`, `Rhythm`, `MeloVocal`, and `MeloRhythm`.
- Existing local pad pages use lowercase names such as `vocal`, `melody`, and `rhythm`; keep that style when matching nearby pad XML.

Sources:

- `Official`: VDJScript verbs appendix
- `Local test`: existing pad pages in this repo use `effect_stems` for ColorFX / push-FX routing

### `effect_stems_color`

Aliases: none

Kind: `Query`

Typical surfaces: `SkinQuery`, `Text`, `Pad`

Official summary:

- Return the color for the `effect_stems` button

Typical forms:

```vdjscript
effect_stems_color
```

Preferred usage:

- use for a generic "FX to stems" indicator when the UI should follow VirtualDJ's own stems-FX color
- use `stem_color '<stem>'` instead when a control is explicitly tied to one stem

Sources:

- `Official`: VDJScript verbs appendix

### `stem_color`

Aliases: none

Kind: `Query`

Typical surfaces: `SkinQuery`, `Text`, `Pad`

Official summary:

- Return the default color of a specific stem

Typical forms:

```vdjscript
stem_color 'Vocal'
stem_color 'Melody'
stem_color 'Rhythm'
```

Preferred usage:

- use for per-stem pad colors and skin indicators
- use `effect_stems_color` for a generic effect-stems button color that should follow VirtualDJ's own `effect_stems` state

Sources:

- `Official`: VDJScript verbs appendix

### `stems_bleed`

Aliases: none

Kind: `Dual`

Typical surfaces: `Pad`, `Button`, `SkinAction`, `SkinQuery`, `Text`

Official summary:

- Adjust or query the stems bleed control when the loaded track has compatible stems

Typical forms:

```vdjscript
stems_bleed
has_stems '1.0' ? stems_bleed : nothing
`has_stems '1.0' ? stems_bleed : has_stems 'ready'`
```

Preferred usage:

- expose it behind a guarded stem-control parameter so decks without 1.0 stems can fall back to `has_stems 'ready'`

Sources:

- `Official`: VDJScript verbs appendix
- `Official`: `examples/pads/official/pads_stems.xml`

### `effect_arm_stem`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Select or unselect a stem to be used with `stems` as the slot for `effect_*` actions

Typical forms:

```vdjscript
effect_arm_stem Vocal
effect_arm_stem Vocal+Bass
```

Preferred usage:

- use for controller mappings that expose a stem-selection layer before operating on effect actions
- use `effect_stems` for ordinary pad-page or skin controls that directly route current deck effects to stems

Sources:

- `Official`: VDJScript verbs appendix

### `effect_bpm_deck`

Aliases: none

Kind: `Dual`

Typical surfaces: `Map`, `Button`, `SkinAction`, `SkinQuery`, `Text`

Official summary:

- Set or get a custom BPM for plugins activated on this deck

Typical forms:

```vdjscript
effect_bpm_deck 120
effect_bpm_deck off
effect_bpm_deck
```

Preferred usage:

- use only when an effect plugin should run against a custom BPM that differs from the loaded song
- reset with `effect_bpm_deck off` to return plugins to the song BPM

Sources:

- `Official`: VDJScript verbs appendix

### `effect_bpm_deck_tap`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Tap a custom BPM for plugins activated on this deck

Typical forms:

```vdjscript
effect_bpm_deck_tap
effect_bpm_deck off
```

Preferred usage:

- use for hardware or skin tap controls that set effect-plugin BPM independently of the song BPM
- pair with `effect_bpm_deck off` as the reset affordance

Sources:

- `Official`: VDJScript verbs appendix

### Armed FX Helpers

These verbs are primarily for controllers with deck/effect selection switches. They build an intermediate "armed" target, then `effect_arm_active` activates the selected effect on the selected deck.

| Verb | Kind | Summary | Example |
| --- | --- | --- | --- |
| `effect_arm_deck` | `Action` | Select the deck, master, sampler, mic, or aux target for armed FX. | `effect_arm_deck master` |
| `effect_arm_select` | `Action` | Select the effect that `effect_arm_active` will activate. | `effect_arm_select 'echo'` |
| `effect_arm_select_popup` | `Action` | Open/select from the armed-effect selection popup. | `effect_arm_select_popup` |
| `effect_arm_slot` | `Action` | Toggle whether a slot is activated by `effect_arm_active`. | `effect_arm_slot 1` |
| `effect_arm_active` | `Dual` | Activate the armed effect on the armed deck. | `effect_arm_active` |
| `effect_arm_slider` | `Action` | Move a parameter for the armed effect/deck selection. | `effect_arm_slider 1 2` |
| `effect_arm_slider_name` | `Text` | Return a parameter name for the armed effect/deck selection. | `effect_arm_slider_name 1 short` |
| `effect_arm_slider_text` | `Text` | Return parameter value text for the armed effect/deck selection. | `effect_arm_slider_text 1` |
| `effect_arm_slider_label` | `Text` | Return a parameter label for the armed effect/deck selection. | `effect_arm_slider_label 1 short` |
| `effect_arm_beats` | `Action` | Change the speed of the armed effect/deck selection. | `effect_arm_beats 1` |
| `effect_arm_bpm` | `Text` | Return the BPM of the deck selected by `effect_arm_deck`. | `effect_arm_bpm` |

Notes:

- `effect_arm_deck single` limits arming to one deck at a time.
- `effect_arm_deck master`, `effect_arm_deck sampler`, `effect_arm_deck mic`, and `effect_arm_deck aux` target non-deck effect paths.
- Prefer direct slot verbs such as `effect_select`, `effect_slider`, and `effect_active` in skins and pad pages unless you are intentionally modeling a hardware armed-FX workflow.

Sources:

- `Official`: VDJScript verbs appendix

### FX Send/Return Helpers

These verbs are for hardware-style FX send/return routing. The official appendix currently gives detailed examples for the multi-source selector and lists the other two names with minimal description.

| Verb | Kind | Summary | Example |
| --- | --- | --- | --- |
| `effect_fxsendreturndeck` | `Action` | Select the source deck for an FX send/return path. | `deck 1 effect_fxsendreturndeck` |
| `effect_fxsendreturndeck_multi` | `Action` | Select which source to apply FX to for a specific send/return channel when multiple channels exist. | `deck 2 effect_fxsendreturndeck_multi mic` |
| `effect_fxsendreturnenable` | `Dual` | Enable or query the FX send/return path. | `effect_fxsendreturnenable` |

Examples:

```vdjscript
deck 1 effect_fxsendreturndeck_multi master
deck 2 effect_fxsendreturndeck_multi mic
deck 2 effect_fxsendreturndeck_multi 4
```

Sources:

- `Official`: VDJScript verbs appendix

### `effect_mixfx`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Associate an effect with the crossfader

Typical forms:

```vdjscript
effect_mixfx
```

Preferred usage:

- use `effect_mixfx_select` when the goal is to choose a specific Mix FX by name
- use `effect_mixfx_activate` when the goal is to toggle Mix FX on/off

Notes:

- Community/forum guidance describes Mix FX as applying an effect to both decks with strength linked to crossfader movement.
- Older forum examples sometimes discuss Mix FX under the name "Mix Assist"; document both terms in prose for searchability.

Sources:

- `Official`: current VDJScript verbs appendix
- `Official forum`: "Mix Assist in other skins", staff context for crossfader-linked behavior
- `Community`: Mix FX examples from forum users and moderators
- `Published skin`: the former local `Haunting Pro Edit/Touch.xml` capture used `effect_mixfx`

### `effect_mixfx_activate`

Aliases: none

Kind: `Dual`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`, `SkinQuery`

Official summary:

- Toggle Mix FX on or off; use `effect_mixfx_select` to choose the Mix FX

Typical forms:

```vdjscript
effect_mixfx_activate
effect_mixfx_activate ? on : off
effect_mixfx_select 'echo' & effect_mixfx_activate
```

Preferred usage:

- use as the Mix FX on/off state, not as the effect selector
- pair with `effect_mixfx_select '<name>'` when building a named Mix FX button

Quirks:

- A 2019 forum test reports that `effect_mixfx_activate '<name>'` behaves as a global on/off query rather than selecting or querying that named Mix FX. Keep that form out of examples until locally retested.
- The Denon Prime 4 Deluxe skin uses `effect_mixfx_activate & effect_mixfx_select 'FILTER'` for named buttons. A local 2026 test confirmed direct selected-state queries for `effect_mixfx_select`, but did not retest order-dependent activation behavior, so keep `effect_mixfx_select '<name>' & effect_mixfx_activate` as the clearer example order.

Sources:

- `Official`: current VDJScript verbs appendix
- `Community`: Mix FX forum examples and behavior notes
- `Published skin`: Denon Prime 4 Deluxe skin, `PRIME 4.xml` lines 1149-1153
- `Local test`: `Pads/Reference - Mix FX Query Test.xml` and `Skins/MixFxQueryTest/skin.xml`, VirtualDJ 8.5.9307 / 850.9336.mac.2224, May 12, 2026

### `effect_mixfx_select`

Aliases: none

Kind: `Dual`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`, `SkinQuery`, `Text`

Official summary:

- Select the Mix FX used when moving the crossfader

Typical forms:

```vdjscript
effect_mixfx_select
effect_mixfx_select 'filter'
effect_mixfx_select 'filter' ? on : off
param_equal "`effect_mixfx_select`" "filter" ? on : off
```

Preferred usage:

- use the parameter form to select a named Mix FX
- use the no-parameter form as a display/query value for the currently selected Mix FX
- use direct `effect_mixfx_select '<name>' ? ...` for named selected-state tests in current VirtualDJ pad pages and skins
- keep the indirect `param_equal "\`effect_mixfx_select\`" "<name>" ? ...` form when comparing the returned display value or documenting older-build-compatible examples

Runnable pad XML example:

```xml
<pad1 name="DIRECT FILTER"
      color="effect_mixfx_select 'FILTER' ? color '#31D67B' : color '#7A3038'"
      query="effect_mixfx_select 'FILTER' ? on : off">
  effect_mixfx_select 'FILTER'
</pad1>
<pad2 name="INDIRECT FILTER"
      color="param_equal &quot;`effect_mixfx_select`&quot; &quot;FILTER&quot; ? color '#31D67B' : color '#7A3038'"
      query="param_equal &quot;`effect_mixfx_select`&quot; &quot;FILTER&quot; ? on : off">
  effect_mixfx_select 'FILTER'
</pad2>
```

Minimal skin query fragment:

```xml
<button x="0" y="0"
        action="effect_mixfx_select 'FILTER'"
        query="effect_mixfx_select 'FILTER' ? on : off">
  <size width="120" height="32"/>
  <off shape="square" color="#6E2F35"/>
  <on shape="square" color="#1E8E5A"/>
  <text text="FILTER" color="#FFFFFF" align="center"/>
</button>
<panel visibility="param_equal &quot;`effect_mixfx_select`&quot; &quot;FILTER&quot; ? true : false">
  <square color="#1E8E5A">
    <pos x="0" y="40"/>
    <size width="120" height="32"/>
  </square>
</panel>
```

Quirks:

- Older forum testing reported that direct queries such as `effect_mixfx_select 'echo' ? ...` did not return reliable boolean results in pad-page logic. A local test on VirtualDJ 8.5.9307 / 850.9336.mac.2224 confirmed direct and indirect queries both work in pad XML `query`/`color`, skin button `query`, and skin `visibility` contexts.
- The no-parameter display form returned lowercase names such as `filter` and `echo` in the local test, while `param_equal` still matched uppercase comparison strings such as `FILTER` and `ECHO`.
- The Denon Prime 4 Deluxe skin uses direct skin queries such as `effect_mixfx_select 'FILTER' ? effect_mixfx_activate`; current local skin testing is consistent with that selected-state query pattern.

Sources:

- `Official`: current VDJScript verbs appendix
- `Official`: DDJ-FLX2 hardware manual recommends assigning `effect_mixfx_select` to custom buttons when a skin lacks Mix FX controls
- `Community`: Mix FX scripting examples and indirect query guidance
- `Published skin`: Denon Prime 4 Deluxe skin, `PRIME 4.xml` lines 1149-1153
- `Local test`: `Pads/Reference - Mix FX Query Test.xml` and `Skins/MixFxQueryTest/skin.xml`, VirtualDJ 8.5.9307 / 850.9336.mac.2224, May 12, 2026

### `effect_show_gui`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Show the control window for an effect

Typical forms:

```vdjscript
effect_show_gui 1
effect_show_gui 'colorfx'
```

Notes:

- Treat GUI access as separate from canonical selection logic. Opening a GUI does not make it the preferred API path for selection or activation.

Sources:

- `Official`: VDJScript verbs appendix

### `sampler_play`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Play the default sample or a specified absolute sample slot

Typical forms:

```vdjscript
sampler_play
sampler_play 4
```

Preferred usage:

- use for absolute-slot sampler control

Sources:

- `Official`: VDJScript verbs appendix

### `sampler_stop`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Stop one sample or all playing samples

Typical forms:

```vdjscript
sampler_stop 4
sampler_stop all
```

Preferred usage:

- use for absolute-slot stop logic or global cleanup actions

Sources:

- `Official`: VDJScript verbs appendix

### `sampler_pad`

Aliases: none

Kind: `Dual`

Typical surfaces: `Pad`, `Button`, `SkinAction`, `SkinQuery`, `Text`

Official summary:

- Trigger the sample in the visible sampler pad position; in display contexts it can also return the visible pad label

Typical forms:

```vdjscript
sampler_pad 1
sampler_pad 1 "auto"
`sampler_pad 1`
```

Preferred usage:

- use this for page-aware sampler UI, not fixed absolute slot control

Quirk:

- In display contexts, `sampler_pad <n>` is often the safest way to show the visible sample label on the current page.

Sources:

- `Official`: VDJScript verbs appendix
- `Official`: pads manual
- `Inference`: current repo examples and current page-aware sampler usage patterns

### `sampler_pad_page`

Aliases: none

Kind: `Dual`

Typical surfaces: `Pad`, `Button`, `SkinAction`, `SkinQuery`, `Text`

Official summary:

- Change or query the current 8-pad sampler window

Typical forms:

```vdjscript
sampler_pad_page +1
sampler_pad_page -1
sampler_pad_page
```

Preferred usage:

- treat this as the official pager behind sampler `1-8`, `9-16`, `17-24`, and later windows

Sources:

- `Official`: VDJScript verbs appendix
- `Official`: pads manual

### `sampler_velocity`

Aliases: none

Kind: `Query`

Typical surfaces: `Pad`, `SkinQuery`

Official summary:

- Return the velocity/pressure value for a sampler pad slot

Typical forms:

```vdjscript
sampler_velocity 1
```

Preferred usage:

- use in pad XML `pressure=""` on velocity-sensitive sampler pages, paired with the matching `sampler_pad <n> "auto"` trigger

```xml
<pad1 pressure="sampler_velocity 1">sampler_pad 1 "auto"</pad1>
```

Sources:

- `Official`: VDJScript verbs appendix
- `Official`: `examples/pads/official/pads_sampler_velocity.xml`

### `sampler_assign`

Aliases: none

Kind: `Action`

Typical surfaces: `Pad`, `Map`, `Button`, `SkinAction`

Official summary:

- Assign a `.vdjsample` file to a slot

Typical forms:

```vdjscript
sampler_assign 1 "/Samples/horn.vdjsample"
```

Preferred usage:

- use for explicit slot assignment when the destination slot is known
- on custom pad pages, pair it with pad XML `drop=` to accept dragged files:

```xml
<pad1 drop="sampler_assign 1">...</pad1>
```

Quirk:

- treat the target slot as absolute unless you have build-specific proof otherwise. The current official docs show fixed slot numbers and do not document a page-aware `"auto"` form for `sampler_assign`.
- The current stock/local sampler page in this repo uses `drop="sampler_assign <slot>"`; see [SAMPLER SIMPLE.xml](../Pads/SAMPLER%20SIMPLE.xml).

Sources:

- `Official`: VDJScript verbs appendix
- `Official`: sampler manual
- `Inference`: current repo sampler pad XML pattern

### `sampler_loaded`

Aliases: none

Kind: `Query`

Typical surfaces: `Pad`, `SkinQuery`, `Text`

Official summary:

- Return true when a sample is loaded in the target slot

Typical forms:

```vdjscript
sampler_loaded 1
sampler_loaded 1 "auto"
```

Quirk:

- The manual explicitly documents fixed-slot behavior.
- The page-aware `sampler_loaded <n> "auto"` pattern is widely used in practice and works with current custom sampler pad patterns, but it should still be labeled as build-sensitive rather than silently promoted to timeless official behavior.

Sources:

- `Official`: VDJScript verbs appendix
- `Inference`: repo usage plus current custom-page practice

### `sampler_color`

Aliases: none

Kind: `Query`

Typical surfaces: `Pad`, `SkinQuery`, `Text`

Official summary:

- Return the sample color for the visible sampler pad slot

Typical forms:

```vdjscript
sampler_color 1
sampler_color 1 "auto"
```

Important note:

- The official manual explicitly says the sample number takes `sampler_pad_page` into account, which makes `sampler_color` one of the safest documented page-aware helpers.

Sources:

- `Official`: VDJScript verbs appendix

### `get_sample_name`

Aliases: `get_sample_slot_name`

Kind: `Query`

Typical surfaces: `Text`, `Pad`, `SkinQuery`

Official summary:

- Return the name of a specified absolute sample slot

Typical forms:

```vdjscript
get_sample_name 9
```

Preferred usage:

- use this for absolute-slot sampler UI
- do not substitute it for `sampler_pad <n>` when the label should follow the currently visible page

Sources:

- `Official`: VDJScript verbs appendix

### `swap_decks`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Swap deck 1 and deck 2

Typical forms:

```vdjscript
swap_decks
```

Preferred usage:

- use as an explicit global deck-management command, not as a substitute for `leftdeck` or `rightdeck`

Sources:

- `Official`: VDJScript verbs appendix

### `clone_deck`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Clone the current deck to the other deck, keeping song and position aligned

Typical forms:

```vdjscript
clone_deck
```

Preferred usage:

- useful for beat-juggling or quick A/B duplication

Sources:

- `Official`: VDJScript verbs appendix

### `clone_from_deck`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Clone from the other deck into the current deck

Typical forms:

```vdjscript
clone_from_deck
```

Sources:

- `Official`: VDJScript verbs appendix

### `move_deck`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Move the song from the called deck into the target deck and unload it from the caller

Typical forms:

```vdjscript
move_deck 2
```

Notes:

- treat this as a content-transfer action, not a cosmetic deck-side switch

Sources:

- `Official`: VDJScript verbs appendix

### `get_deck`

Aliases: none

Kind: `Query`

Typical surfaces: `Map`, `Button`, `SkinQuery`, `Text`

Official summary:

- Get the number of the deck

Typical forms:

```vdjscript
get_deck
```

Preferred usage:

- use for deck-aware text and conditions when the action should follow the current deck context instead of a hard-coded deck number

Sources:

- `Official`: VDJScript verbs appendix

### `masterdeck`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Select or unselect this deck as the master deck

Typical forms:

```vdjscript
masterdeck
deck 3 masterdeck
```

Important note:

- When a master deck is set, synchronization operations use it as the reference deck.

Sources:

- `Official`: VDJScript verbs appendix

### `leftdeck`

Aliases: none

Kind: `Dual`

Typical surfaces: `Map`, `Button`, `SkinAction`, `SkinQuery`

Official summary:

- Select this deck to be the left deck

Typical forms:

```vdjscript
deck 3 leftdeck
leftdeck +1
```

Skin query form:

```vdjscript
deck 3 leftdeck
not deck 3 leftdeck
```

Preferred usage:

- most useful in skins and mappings that expose more than two decks at once
- in skin `visibility=""` and `condition=""` expressions, `deck N leftdeck` can be used as a predicate to choose which physical deck occupies the left-side UI

Sources:

- `Official`: VDJScript verbs appendix
- `Local test`: working skin XML uses `deck N leftdeck` as a visibility predicate

### `rightdeck`

Aliases: none

Kind: `Dual`

Typical surfaces: `Map`, `Button`, `SkinAction`, `SkinQuery`

Official summary:

- Select this deck to be the right deck

Typical forms:

```vdjscript
deck 3 rightdeck
rightdeck +1
```

Skin query form:

```vdjscript
deck 4 rightdeck
not deck 4 rightdeck
```

Preferred usage:

- most useful in skins and mappings that expose more than two decks at once
- in skin `visibility=""` and `condition=""` expressions, `deck N rightdeck` can be used as a predicate to choose which physical deck occupies the right-side UI

Sources:

- `Official`: VDJScript verbs appendix
- `Local test`: working skin XML uses `deck N rightdeck` as a visibility predicate

### `invert_deck`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Switch the left or right deck assignment

Typical forms:

```vdjscript
invert_deck
invert_deck 'left'
invert_deck 'right'
```

Sources:

- `Official`: VDJScript verbs appendix

### `leftcross`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Assign this deck to the left of the crossfader

Typical forms:

```vdjscript
deck 3 leftcross
deck 3 leftcross 'only'
leftcross 'none'
```

Sources:

- `Official`: VDJScript verbs appendix

### `rightcross`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Assign this deck to the right of the crossfader

Typical forms:

```vdjscript
deck 3 rightcross
```

Sources:

- `Official`: VDJScript verbs appendix

### `pfl`

Aliases: none

Kind: `Dual`

Typical surfaces: `Map`, `Button`, `SkinAction`, `SkinQuery`

Official summary:

- Select whether this deck is sent to the headphones

Typical forms:

```vdjscript
pfl
pfl 75%
```

Important note:

- The official manual also documents slider or percent use for headphone level control.

Sources:

- `Official`: VDJScript verbs appendix

### `get_deck_color`

Aliases: none

Kind: `Query`

Typical surfaces: `SkinQuery`, `Text`, `Button`

Official summary:

- Return blue or red if the deck is the left or right deck, and gray otherwise

Typical forms:

```vdjscript
get_deck_color
get_deck_color 50%
get_deck_color "absolute"
get_deck_color "absolute" 50%
```

Important note:

- Use `"absolute"` when you want color based on the actual deck number rather than the current left/right assignment.

Sources:

- `Official`: VDJScript verbs appendix

### `play_button`

Aliases: `play_3button`

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Act like `play_stutter` or `play_pause` depending on the `playMode` setting

Typical forms:

```vdjscript
play_button
```

Preferred usage:

- use only when you intentionally want behavior that follows the user's `playMode`
- for documentation and fixed examples, prefer `play_pause` or `play_stutter` explicitly

Sources:

- `Official`: VDJScript verbs appendix

### `pause_stop`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- If playing, pause the deck. If already stopped, rewind to the beginning, then cycle cues on repeated presses.

Typical forms:

```vdjscript
pause_stop
```

Preferred usage:

- use when you intentionally want the classic Numark-style stop behavior
- do not document it as interchangeable with plain `stop`

Sources:

- `Official`: VDJScript verbs appendix

### `stop_button`

Aliases: `stop_3button`

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Act like `pause_stop` or `stop` depending on the `playMode` setting

Typical forms:

```vdjscript
stop_button
```

Preferred usage:

- use only when the mapping should follow `playMode`
- for deterministic docs and examples, prefer `stop` or `pause_stop` explicitly

Sources:

- `Official`: VDJScript verbs appendix

### `cue_play`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Like `cue_stop`, but if held long enough it continues playing when released

Typical forms:

```vdjscript
cue_play
cue_play 1 1000ms
```

Notes:

- The manual documents the hold behavior and allows an explicit time argument.

Sources:

- `Official`: VDJScript verbs appendix

### `cue`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- If playing, jump to the last cue point and keep playing. If paused, set the cue and preview while pressed.

Typical forms:

```vdjscript
cue
cue 1
cue 57
```

Notes:

- In loops, the manual says `cue` changes `loop_in` to the cue point while keeping the loop length.

Sources:

- `Official`: VDJScript verbs appendix

### `cue_select`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Select the default cue point used by cue-related actions without jumping to it

Typical forms:

```vdjscript
cue_select 1
cue_select +1
```

Preferred usage:

- use when you need cue-target selection separate from transport movement

Sources:

- `Official`: VDJScript verbs appendix

### `cue_cup`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- If playing, rewind to the last cue and restart on release. If paused, set the current position as cue.

Typical forms:

```vdjscript
cue_cup
```

Sources:

- `Official`: VDJScript verbs appendix

### `cue_button`

Aliases: `cue_3button`

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Act like `cue_stop`, `cue_play`, or `cue_cup` depending on the `cueMode` setting

Typical forms:

```vdjscript
cue_button
```

Preferred usage:

- use when you intentionally want the mapping to follow `cueMode`
- for deterministic examples, document `cue_stop`, `cue_play`, or `cue_cup` directly

Sources:

- `Official`: VDJScript verbs appendix

### `goto_first_beat`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Jump to the first beat in the song

Typical forms:

```vdjscript
goto_first_beat
```

Sources:

- `Official`: VDJScript verbs appendix

### `goto_start`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Go to the start of the song

Typical forms:

```vdjscript
goto_start
```

Sources:

- `Official`: VDJScript verbs appendix

### `loop`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Set or remove a loop

Typical forms:

```vdjscript
loop 4
loop 0.5
loop 10ms
loop 200%
loop
```

Preferred usage:

- use when one control should create, resize, or toggle a loop directly
- use `loop_in`, `loop_out`, `loop_length`, and `loop_move` when the UI has separate controls for loop lifecycle and loop size

Sources:

- `Official`: VDJScript verbs appendix

### `loop_in`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- If not in loop, set the beginning of a loop. If already in loop, jump back to the loop start.

Typical forms:

```vdjscript
loop_in
```

Sources:

- `Official`: VDJScript verbs appendix

### `loop_out`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- If not in loop, enter a loop using the last `loop_in` point or stutter point. If already in loop, exit it.

Typical forms:

```vdjscript
loop_out
```

Sources:

- `Official`: VDJScript verbs appendix

### `loop_length`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Change the loop length in milliseconds, beats, or percentage of the current length

Typical forms:

```vdjscript
loop_length 0.5
loop_length 15ms
loop_length +100%
```

Preferred usage:

- use for deterministic loop-size controls and encoders

Sources:

- `Official`: VDJScript verbs appendix

### `loop_move`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Move the loop while keeping its current length

Typical forms:

```vdjscript
loop_move +2
loop_move +10ms
loop_move +50%
```

Sources:

- `Official`: VDJScript verbs appendix

### `loop_double`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Double the current loop length

Typical forms:

```vdjscript
loop_double
```

Sources:

- `Official`: VDJScript verbs appendix

### `loop_half`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Halve the current loop length

Typical forms:

```vdjscript
loop_half
```

Sources:

- `Official`: VDJScript verbs appendix

### `loop_exit`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Remove the loop

Typical forms:

```vdjscript
loop_exit
```

Sources:

- `Official`: VDJScript verbs appendix

### `reloop`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Jump to the stored `loop_in` point

Typical forms:

```vdjscript
reloop
```

Sources:

- `Official`: VDJScript verbs appendix

### `reloop_exit`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- If in loop, remove it. Otherwise, reactivate the last used loop.

Typical forms:

```vdjscript
reloop_exit
```

Notes:

- The official text also notes that it highlights when a loop had been used.

Sources:

- `Official`: VDJScript verbs appendix

### `loop_roll`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Trigger a loop roll of the specified size

Typical forms:

```vdjscript
loop_roll 0.25
loop_roll video
```

Sources:

- `Official`: VDJScript verbs appendix

### Saved Loop Pad Helpers

| Verb | Kind | Surfaces | Summary | Example |
| --- | --- | --- | --- | --- |
| `saved_loop_display` | `Dual` | `Pad`, `Text`, `SkinQuery` | Display a saved-loop slot label or choose the saved-loop display mode. | `` `saved_loop_display 1` ``, `saved_loop_display 'length'` |
| `loop_color` | `Query` | `Pad`, `SkinQuery`, `Text` | Return the color for a saved-loop slot. | `loop_color 1` |
| `loop_delete` | `Action` | `Pad`, `SkinAction` | Delete a saved-loop slot. | `loop_delete 1` |
| `loop_load_prepare` | `Dual` | `Pad`, `SkinAction`, `SkinQuery` | Prepare/load a saved-loop slot and query whether that slot is prepared. | `loop_load 1 ? loop_load_prepare 1 : loop_save 1` |

Notes:

- The official Saved Loops pad page uses `loop_load_prepare <n>` as a query for blink state and as the action after an existing `loop_load <n>` test; holding a populated pad runs `loop_delete <n>`.

Sources:

- `Official`: VDJScript verbs appendix
- `Official`: `examples/pads/official/pads_saved_loops.xml`

### `pad_page_select`

Aliases: `pad_page_favorite_select`

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Select the pad page assigned to a favorite slot

Typical forms:

```vdjscript
pad_page_select 1
```

Sources:

- `Official`: VDJScript verbs appendix

### `sync`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`

Official summary:

- Smoothly synchronize the song with the other deck

Typical forms:

```vdjscript
sync
```

Preferred usage:

- use when you want standard sync behavior that follows the current sync engine rather than an immediate start-and-play action

Sources:

- `Official`: VDJScript verbs appendix

### `match_bpm`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Set the pitch to match the BPM of the other deck

Typical forms:

```vdjscript
match_bpm
```

Sources:

- `Official`: VDJScript verbs appendix

### `play_sync`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Play the song instantly synchronized with the other deck

Typical forms:

```vdjscript
play_sync
```

Preferred usage:

- use when the action should both sync and start playback immediately
- do not confuse this with the `smart_play` setting/action

Sources:

- `Official`: VDJScript verbs appendix

### `play_sync_onbeat`

Aliases: `sync_nocbg`

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Instantly synchronize using local beat information instead of the global beatgrid

Typical forms:

```vdjscript
play_sync_onbeat
```

Preferred usage:

- call out the alias because older scripts and forum posts often reference `sync_nocbg`

Sources:

- `Official`: VDJScript verbs appendix

### `beatlock`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`, `SkinAction`, `SkinQuery`

Official summary:

- Keep songs synchronized even while moving pitch, scratching, and similar manipulations

Typical forms:

```vdjscript
beatlock
beatlock on
beatlock off
```

Sources:

- `Official`: VDJScript verbs appendix

### `smart_fader`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Synchronize songs while using the crossfader and gradually move tempo toward the target side

Typical forms:

```vdjscript
smart_fader
```

Sources:

- `Official`: VDJScript verbs appendix

### `smart_play`

Aliases: `auto_sync`

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- When enabled, songs are automatically synchronized when started

Typical forms:

```vdjscript
smart_play
smart_play on
smart_play off
```

Important note:

- This is a setting-like behavior toggle, not the same thing as the `play_sync` transport action.

Sources:

- `Official`: VDJScript verbs appendix

### `phrase_sync`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `Pad`

Official summary:

- Shift by a number of beats to match the phrase of the other deck

Typical forms:

```vdjscript
phrase_sync
phrase_sync 16
```

Sources:

- `Official`: VDJScript verbs appendix

### `quantize_all`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Set all quantize options

Typical forms:

```vdjscript
quantize_all
```

Sources:

- `Official`: VDJScript verbs appendix

### Quantize Pad Helpers

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `quantize_loop` | `Pad`, `Button`, `SkinAction`, `SkinQuery` | Toggle/query loop and loop-roll quantization. | `quantize_loop on`, `quantize_loop ? on : off` |
| `quantize_setcue` | `Pad`, `Button`, `SkinAction`, `SkinQuery` | Toggle/query quantization when setting cues. | `quantize_setcue` |

Sources:

- `Official`: VDJScript verbs appendix
- `Official`: `examples/pads/official/pads_manual_loop.xml`
- `Official`: `examples/pads/official/pads_loop_roll.xml`
- `Official`: `examples/pads/official/pads_hotcues.xml`

### `is_fluid`

Aliases: `has_variable_bpm`

Kind: `Query`

Typical surfaces: `Map`, `Button`, `SkinQuery`, `Text`

Official summary:

- Return true if the song uses a fluid grid

Typical forms:

```vdjscript
is_fluid
```

Sources:

- `Official`: VDJScript verbs appendix

### `set_fluid`

Aliases: `set_variable_bpm`

Kind: `Action`

Typical surfaces: `Map`, `Button`

Official summary:

- Switch between fluid and rigid grids

Typical forms:

```vdjscript
set_fluid
```

Sources:

- `Official`: VDJScript verbs appendix

### `goto_last_folder`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Go back to the last browsed folder

Typical forms:

```vdjscript
goto_last_folder
```

Preferred usage:

- use when a mapping or skin action needs deterministic browser back-navigation without simulating repeated scrolls

Sources:

- `Official`: VDJScript verbs appendix

### `browser_scroll`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Scroll through the songs or folders

Typical forms:

```vdjscript
browser_scroll +1
browser_scroll -1
browser_scroll 'top'
browser_scroll 'bottom'
```

Preferred usage:

- use for encoders, list navigation buttons, and timed repeat browsing
- pair with `repeat_start` or `repeat_start_instant` when the control should keep scrolling while held

Sources:

- `Official`: VDJScript verbs appendix

### `browser_move`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Move the currently selected song inside a playlist

Typical forms:

```vdjscript
browser_move +1
browser_move 'top'
browser_move 'bottom'
```

Important note:

- Treat this as playlist reordering, not general browser navigation.

Sources:

- `Official`: VDJScript verbs appendix

### `browser_folder`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- If focus is on songs, change focus to folders. If focus is on folders, open or close the subfolders of the selected folder.

Typical forms:

```vdjscript
browser_folder
```

Preferred usage:

- use when you want a single control to hand off focus from song list to folder tree

Sources:

- `Official`: VDJScript verbs appendix

### `browser_enter`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- If focus is on songs, load the selected song. If focus is on folders, change focus to songs.

Typical forms:

```vdjscript
browser_enter
```

Important note:

- This is focus-sensitive. If you need a guaranteed load action regardless of browser focus, prefer `load`.

Sources:

- `Official`: VDJScript verbs appendix
- `Inference`: deterministic API guidance based on the documented focus-dependent behavior

### `browser_open_folder`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Expand the selected folder when closed, or close it when opened

Typical forms:

```vdjscript
browser_open_folder
browser_open_folder on
browser_open_folder off
```

Preferred usage:

- use this when you need explicit folder-tree open or close behavior without also switching song focus

Sources:

- `Official`: VDJScript verbs appendix

### `browser_remove`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Remove the selected song from playlist

Typical forms:

```vdjscript
browser_remove
```

Important note:

- The documented behavior is playlist removal, not deletion from the library or filesystem.

Sources:

- `Official`: VDJScript verbs appendix

### `browser_window`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Change the active browser zone

Typical forms:

```vdjscript
browser_window 'folders'
browser_window 'songs'
browser_window 'sideview'
browser_window 'automix'
browser_window +1
browser_window 'folders,songs'
```

Preferred usage:

- use this to move focus between browser panes
- use `sideview` when the goal is to choose which sideview is shown, not just move focus to the sideview pane

Sources:

- `Official`: VDJScript verbs appendix

### `search`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Put keyboard focus on the search zone, or, if a text parameter is specified, search for this text

Typical forms:

```vdjscript
search
search 'house'
```

Preferred usage:

- use `search 'text'` when you want deterministic scripted search input
- use `edit_search` when you want keyboard focus without replacing the current query

Sources:

- `Official`: VDJScript verbs appendix

### `search_add`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Add the specified text to the search query

Typical forms:

```vdjscript
search_add 'acapella'
```

Preferred usage:

- use when a button should append a token or fragment without discarding the existing search string

Sources:

- `Official`: VDJScript verbs appendix

### `search_delete`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Remove the last character from the search query

Typical forms:

```vdjscript
search_delete
```

Sources:

- `Official`: VDJScript verbs appendix

### `clear_search`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Clear the search string

Typical forms:

```vdjscript
clear_search
```

Sources:

- `Official`: VDJScript verbs appendix

### `edit_search`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Put keyboard focus in the search zone but keep the actual search string

Typical forms:

```vdjscript
edit_search
```

Preferred usage:

- prefer this over plain `search` when the current query must be preserved

Sources:

- `Official`: VDJScript verbs appendix

### `file_count`

Aliases: none

Kind: `Query`

Typical surfaces: `Text`, `SkinQuery`, `Button`

Official summary:

- Get the number of files currently shown in browser

Typical forms:

```vdjscript
`file_count`
`file_count automix`
```

Important note:

- The official verbs page also documents `automix`, `sideview`, `karaoke`, and `sidelist` as valid count targets.

Sources:

- `Official`: VDJScript verbs appendix

### `sideview`

Aliases: none

Kind: `Action`

Typical surfaces: `Map`, `Button`, `SkinAction`

Official summary:

- Show a specific folder in the sideview

Typical forms:

```vdjscript
sideview automix
sideview sampler
sideview +1
sideview -1
```

Important note:

- Use `sideview` to select the sideview content.
- Use `browser_window 'sideview'` when the goal is to move focus to the sideview pane.

Sources:

- `Official`: VDJScript verbs appendix

### `sideview_title`

Aliases: none

Kind: `Query`

Typical surfaces: `Text`, `SkinQuery`

Official summary:

- Show the title of the folder selected in sideview

Typical forms:

```vdjscript
`sideview_title`
```

Preferred usage:

- useful for skin labels and browser helper text that should reflect the active sideview source

Sources:

- `Official`: VDJScript verbs appendix

### `rating`

Aliases: none

Kind: `Dual`

Typical surfaces: `Map`, `Button`, `SkinAction`, `Text`

Official summary:

- Get or set the rating for the current song

Typical forms:

```vdjscript
`rating`
rating 4
```

Preferred usage:

- use the query form for display
- use the action form for explicit rating controls on the current song

Sources:

- `Official`: VDJScript verbs appendix

### `add_list`

Aliases: `add_virtualfolder`

Kind: `Action`

Typical surfaces: `Button`, `SkinAction`

Official summary:

- Create a new list (virtual folder)

Typical forms:

```vdjscript
add_list
```

Sources:

- `Official`: VDJScript verbs appendix

### Browser Folder And List Helpers

These actions create or modify browser folders, lists, and list shortcuts. Most are useful in skin buttons and controller mappings, but several are destructive enough to avoid wiring to accidental gestures.

| Verb | Aliases | Surfaces | Summary | Example |
| --- | --- | --- | --- | --- |
| `add_favoritefolder` | — | `Button`, `SkinAction` | Make the selected folder a favorite / monitored folder. | `add_favoritefolder` |
| `add_filterfolder` | — | `Button`, `SkinAction` | Create a new filter folder. | `add_filterfolder` |
| `add_to_list` | `virtualfolder_add` | `Button`, `SkinAction` | Add selected browser songs to the specified list. | `add_to_list 'Warmup'` |
| `create_list_from_playlist` | `create_virtualfolder_from_playlist` | `Button`, `SkinAction` | Save the automix playlist as a MyLists entry. | `create_list_from_playlist` |

Sources:

- `Official`: VDJScript verbs appendix

### Browser File Actions

These actions operate on the currently selected browser file or files, not necessarily the loaded deck.

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `browsed_file_info` | `Button`, `SkinAction` | Open the Tag Editor for the browsed song. | `browsed_file_info` |
| `browsed_file_reveal` | `Button`, `SkinAction` | Reveal the browsed song in the OS file manager. | `browsed_file_reveal` |
| `browsed_file_reload_tag` | `Button`, `SkinAction` | Reload the selected file's tag from the source file. | `browsed_file_reload_tag` |
| `browsed_file_rename` | `Button`, `SkinAction` | Rename the selected browser file. | `browsed_file_rename` |
| `set_browsed_file_bpm` | `Button`, `SkinAction` | Set the BPM of selected browser songs. | `set_browsed_file_bpm 129.3` |
| `browsed_song` | `Button`, `SkinAction` | Set a property on the currently browsed file. | `browsed_song 'rating' 5` |
| `loaded_song` | `Button`, `SkinAction` | Set a property on the track loaded on the deck. | `loaded_song 'rating' 5` |
| `browsed_song_hashtag` | `Button`, `SkinAction` | Add or remove a hashtag from a browsed-song field. | `browsed_song_hashtag 'user 1' '#high_energy'` |
| `loaded_song_hashtag` | `Button`, `SkinAction` | Add or remove a hashtag from a loaded-song field. | `loaded_song_hashtag 'user 1' '#warmup'` |
| `edit_comment` | `Button`, `SkinAction` | Open a window to edit the selected track's comment. | `edit_comment` |

Important notes:

- `browsed_file_reload_tag` overwrites VirtualDJ database changes with values saved in the file tag.
- `set_browsed_file_bpm` follows the same value style as `set_bpm`, including absolute and relative values.
- Prefer `get_browsed_song` / `get_loaded_song` for read-only display; use `browsed_song` / `loaded_song` only when a control should write metadata.

Sources:

- `Official`: VDJScript verbs appendix

### Browser Search And View Helpers

| Verb | Kind | Surfaces | Summary | Example |
| --- | --- | --- | --- | --- |
| `log_search` | `Action` | `Button`, `SkinAction` | Log the current search to `SearchLog.txt`. | `log_search` |
| `search_playlists` | `Action` | `Button`, `SkinAction` | Open a dialog to find lists containing a song. | `search_playlists deck` |
| `search_folder` | `Action` | `Button`, `SkinAction` | Show/hide folder/list search, or open it as a dialog. | `search_folder dialog` |
| `search_options` | `Action` | `Button`, `SkinAction` | Open or set search field options. | `search_options 'composer'` |
| `search_folder_options` | `Action` | `Button`, `SkinAction` | Open folder-search options. | `search_folder_options` |
| `view_options` | `Action` | `Button`, `SkinAction` | Open or set browser view options. | `view_options 'showkaraoke' on` |
| `browser_isactive` | `Query` | `SkinQuery`, `Button` | True when the browser was recently used by a controller. | `browser_isactive` |
| `browser_zoom` | `Dual` | `Button`, `SkinAction`, `SkinQuery` | Toggle/query browser zoom state, commonly used by mini-deck or browser-focused skin layouts. | `browser_zoom` |
| `browser_geniusdj` | `Action` | `Button`, `SkinAction` | Lookup recommendations from the selected or playing track. | `browser_geniusdj playing` |
| `browser_shortcut` | `Action` | `Button`, `SkinAction` | Assign current folder as shortcut, or jump to shortcut by index. | `browser_shortcut 1` |
| `recurse_folder` | `Action` | `Button`, `SkinAction` | Show selected folder and subfolders in the browser list. | `recurse_folder` |
| `font_size` | `Action` | `Button`, `SkinAction` | Change browser font size. | `font_size +1` |
| `has_quick_filter` | `Query` | `SkinQuery`, `Button` | Return true if a quick filter exists at the given index. | `has_quick_filter 1` |
| `sideview_options` | `Action` | `Button`, `SkinAction` | Show sideview shortcut options. | `sideview_options` |
| `sideview_triggerpad` | `Action` | `Button`, `SkinAction` | Toggle sideview sampler between triggerpad and list modes. | `sideview_triggerpad` |
| `sideview_sort` | `Action` | `Button`, `SkinAction` | Sort the sideview by a column. | `sideview_sort 'artist'` |
| `sidereco_options` | `Action` | `Button`, `SkinAction` | Show options for the sideview recommendation panel. | `sidereco_options` |
| `sidereco_song` | `Dual` | `Button`, `SkinAction`, `Text` | Recommendation-panel song helper. | `sidereco_song` |
| `sidereco_source` | `Dual` | `Button`, `SkinAction`, `Text` | Recommendation-panel source helper. | `sidereco_source` |
| `mark_linked_tracks` | `Action` | `Button`, `SkinAction` | Mark the tracks on decks 1 and 2 as linked/related. | `mark_linked_tracks` |
| `mark_related_tracks` | `Action` | `Button`, `SkinAction` | Official alias of `mark_linked_tracks`. | `mark_related_tracks` |
| `has_linked_tracks` | `Query` | `SkinQuery`, `Button` | Check whether a track has linked/related tracks. | `has_linked_tracks browsed` |
| `page` | `Dual` | `Button`, `SkinAction`, `Text` | Browser/page helper from the official appendix. | `page` |

Skin pattern:

```vdjscript
browser_zoom ? true : browser_isactive ? true : false
```

This is useful when a skin has a browser-zoom or "mini deck" layout that should appear either when the browser is explicitly zoomed or when controller/browser focus is active.

Track relationship pattern:

```vdjscript
deck 1 loaded ? deck 2 loaded ? mark_linked_tracks : nothing
has_linked_tracks browsed ? sideview 'remixes' : nothing
```

Sources:

- `Official`: VDJScript verbs appendix
- `Local test`: working skin XML uses `browser_zoom` and `browser_isactive` in layout visibility queries
- `Inference`: the combined query pattern is a skin-layout convention built from those queries

### Automix, Playlist, And Sidelist Helpers

| Verb | Aliases | Surfaces | Summary | Example |
| --- | --- | --- | --- | --- |
| `automix_dualdeck` | — | `Button`, `SkinAction`, `SkinQuery` | Enable/disable automix using both decks. | `automix_dualdeck` |
| `automix_add_next` | — | `Button`, `SkinAction` | Add selected browser songs right after the currently playing automix song. | `automix_add_next` |
| `automix_editor` | — | `Button`, `SkinAction` | Open the Automix Editor. | `automix_editor` |
| `automix_editor_movetrack` | — | `Map`, `Button`, `SkinAction` | Move the selected Automix Editor track. | `automix_editor_movetrack 'current' +10` |
| `get_automix` | — | `Text`, `SkinQuery` | Return the automix crossfader position. | `get_automix` |
| `get_automix_song` | — | `Text`, `SkinQuery` | Return a property from the next automix song or a later queued song. | `get_automix_song 'title' 2` |
| `get_automix_position` | — | `Text`, `SkinQuery` | Return the position of the currently playing song in the automix list. | `get_automix_position` |
| `get_playlist_time` | — | `Text`, `SkinQuery` | Return time left before the end of the automix playlist. | `get_playlist_time` |
| `playlist_options` | — | `Button`, `SkinAction` | Show playlist options. | `playlist_options` |
| `playlist_add` | — | `Button`, `SkinAction` | Add selected browser songs to the automix list. | `playlist_add` |
| `playlist_load` | — | `Button`, `SkinAction` | Load selected folder/playlist into the automix playlist. | `playlist_load 'append'` |
| `playlist_load_and_remove` | — | `Button`, `SkinAction` | Load first automix-list song and remove it from the list. | `playlist_load_and_remove` |
| `playlist_load_and_keep` | — | `Button`, `SkinAction` | Load first automix-list song without removing it. | `playlist_load_and_keep` |
| `playlist_randomize_once` | — | `Button`, `SkinAction` | Shuffle playlist order once. | `playlist_randomize_once` |
| `playlist_save` | — | `Button`, `SkinAction` | Save the playlist to a file. | `playlist_save` |
| `playlist_remove_played` | — | `Button`, `SkinAction` | Remove already-played songs from the playlist. | `playlist_remove_played` |
| `playlist_remove_duplicates` | — | `Button`, `SkinAction` | Remove duplicate songs from the playlist. | `playlist_remove_duplicates` |
| `switch_sidelist_playlist` | — | `Button`, `SkinAction` | Exchange automix-list and sidelist contents. | `switch_sidelist_playlist` |
| `mix_next_sidelist` | — | `Button`, `SkinAction` | Mix to the next deck using a new song from the sidelist if needed. | `mix_next_sidelist` |
| `relay_play` | — | `Button`, `SkinAction`, `SkinQuery` | Auto-start the opposite deck when the current deck reaches the end. | `relay_play` |
| `sidelist_options` | — | `Button`, `SkinAction` | Show sidelist options. | `sidelist_options` |
| `sidelist_clear` | — | `Button`, `SkinAction` | Clear the sidelist. | `sidelist_clear` |
| `sidelist_add` | — | `Button`, `SkinAction` | Add selected browser songs to the sidelist. | `sidelist_add` |
| `sidelist_load` | — | `Button`, `SkinAction` | Load selected folder/playlist into the sidelist. | `sidelist_load 'append'` |
| `sidelist_load_and_remove` | — | `Button`, `SkinAction` | Load first sidelist song and remove it from the sidelist. | `sidelist_load_and_remove` |
| `sidelist_load_and_keep` | — | `Button`, `SkinAction` | Load first sidelist song without removing it. | `sidelist_load_and_keep` |

Sources:

- `Official`: VDJScript verbs appendix

### Karaoke Browser Helpers

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `karaoke_load` | `Button`, `SkinAction` | Load selected folder/playlist into the karaoke list. | `karaoke_load 'append'` |
| `karaoke_add` | `Button`, `SkinAction` | Add selected browser songs to the karaoke list. | `karaoke_add` |
| `edit_singer` | `Button`, `SkinAction` | Edit the singer for the selected karaoke-list song. | `edit_singer` |

Sources:

- `Official`: VDJScript verbs appendix

### Deck Set Helpers

| Verb | Surfaces | Summary | Example |
| --- | --- | --- | --- |
| `save_deck_set` | `Button`, `SkinAction` | Save the current loaded-deck configuration to a file. | `save_deck_set` |
| `load_deck_set` | `Button`, `SkinAction` | Reload a previously saved deck-set file. | `load_deck_set` |

Sources:

- `Official`: VDJScript verbs appendix

### Prelisten Helpers

| Verb | Kind | Surfaces | Summary | Example |
| --- | --- | --- | --- | --- |
| `prelisten` | `Action` | `Button`, `SkinAction` | Pre-listen the selected track. | `prelisten` |
| `preview` | `Action` | `Button`, `SkinAction` | Official alias of `prelisten`. | `preview` |
| `prelisten_info` | `Text` | `Text`, `SkinQuery` | Prelisten-player information helper. | `prelisten_info` |
| `prelisten_options` | `Action` | `Button`, `SkinAction` | Show prelisten-player options. | `prelisten_options` |
| `prelisten_output` | `Action` | `Map`, `Button`, `SkinAction` | Assign a deck as the prelisten player or reset to auto. | `deck 1 prelisten_output` |
| `prelisten_pos` | `Action` | `Map`, `Button`, `SkinAction` | Move the prelisten-player position. | `prelisten_pos 50%` |
| `prelisten_stop` | `Action` | `Button`, `SkinAction` | Stop the prelisten player. | `prelisten_stop` |

Sources:

- `Official`: VDJScript verbs appendix

### `info_options`

Aliases: `infos_options`

Kind: `Action`

Typical surfaces: `Button`, `SkinAction`

Official summary:

- Show the context menu about the info panel fields and prelisten behavior

Typical forms:

```vdjscript
info_options
```

Sources:

- `Official`: VDJScript verbs appendix

### `browser_options`

Aliases: none

Kind: `Action`

Typical surfaces: `Button`, `SkinAction`

Official summary:

- Show the context menu about browser filters, root folders, database, and related browser settings

Typical forms:

```vdjscript
browser_options
```

Sources:

- `Official`: VDJScript verbs appendix

### `browser_export`

Aliases: none

Kind: `Action`

Typical surfaces: `Button`, `SkinAction`

Official summary:

- Export the current list of files to a CSV or HTML file

Typical forms:

```vdjscript
browser_export
```

Sources:

- `Official`: VDJScript verbs appendix

### EQ

VirtualDJ's three-band EQ. Each band operates on the full deck signal.
The numeric scale for `eq_high`, `eq_mid`, `eq_low` runs from `0%` (cut) to `100%` (unity) to `200%` (boost).
EQ values are center-off: `100%` is unity, below cuts, above boosts.

| Canonical | Aliases | Surfaces | Description |
| --- | --- | --- | --- |
| `eq_high` | — | `Map`, `SkinAction`, `SkinQuery` | High-frequency EQ band. Read returns current value; write sets it. | `Official` |
| `eq_mid` | `eq_med` | `Map`, `SkinAction`, `SkinQuery` | Mid-frequency EQ band. | `Official` |
| `eq_low` | — | `Map`, `SkinAction`, `SkinQuery` | Low-frequency EQ band. | `Official` |
| `eq_kill_high` | — | `Map`, `SkinAction`, `SkinQuery` | Toggle high-band kill (cut to zero). Query returns `on` when killed. | `Official` |
| `eq_kill_mid` | `eq_kill_med` | `Map`, `SkinAction`, `SkinQuery` | Toggle mid-band kill. | `Official` |
| `eq_kill_low` | — | `Map`, `SkinAction`, `SkinQuery` | Toggle low-band kill. | `Official` |
| `eq_reset` | — | `Map`, `SkinAction` | Reset all three EQ bands to unity (100%). | `Official` |
| `eq_high_freq` | — | `Map`, `SkinAction` | Set the crossover frequency of the high band. | `Official` |
| `eq_mid_freq` | — | `Map`, `SkinAction` | Set the crossover frequency of the mid band. | `Official` |
| `eq_low_freq` | — | `Map`, `SkinAction` | Set the crossover frequency of the low band. | `Official` |
| `eq_high_slider` | — | `Map`, `SkinAction` | Center-off slider form of `eq_high` (50% = unity). Use on physical sliders. | `Official` |
| `eq_mid_slider` | `eq_med_slider` | `Map`, `SkinAction` | Center-off slider form of `eq_mid`. | `Official` |
| `eq_low_slider` | — | `Map`, `SkinAction` | Center-off slider form of `eq_low`. | `Official` |
| `eq_mode` | — | `Map`, `SkinAction` | Cycle or set EQ mode. Values: `standard`, `stem`. | `Official` |
| `fake_eq` | — | `Map`, `SkinAction` | EQ that only affects the preview/headphone signal, not master output. | `Official` |

Examples:

```vdjscript
eq_high 75%
eq_low 0%
eq_kill_high
eq_reset
```

Kill button pattern for a skin button:

```xml
<button action="eq_kill_high" query="eq_kill_high">
  <off color="#1C1F24" border="#444"/>
  <on  color="#FF4444" border="#FF4444"/>
  <text text="HI KILL" color="white"/>
</button>
```

Source: `Official`

---

### `get_browsed_*` — Browsed Track Metadata

These verbs return metadata for the track currently highlighted in the browser,
not for the loaded deck. Use them in `<textzone>` format strings or skin `query=` color expressions
to build an info panel that updates as the user browses.

All are Text-surface verbs (read-only). None take a deck scope — they always reflect the browser selection.

| Verb | Returns | Source |
| --- | --- | --- |
| `get_browsed_title` | Track title | `Official` |
| `get_browsed_artist` | Artist name | `Official` |
| `get_browsed_artist_title` | `Artist - Title` combined | `Official` |
| `get_browsed_title_artist` | `Title - Artist` combined | `Official` |
| `get_browsed_album` | Album name | `Official` |
| `get_browsed_bpm` | BPM as a string | `Official` |
| `get_browsed_key` | Musical key | `Official` |
| `get_browsed_genre` | Genre tag | `Official` |
| `get_browsed_comment` | Comment tag | `Official` |
| `get_browsed_composer` | Composer tag | `Official` |
| `get_browsed_filepath` | Full file path | `Official` |
| `get_browsed_color` | Track color (returns a color value) | `Official` |
| `get_browsed_header` | Column header label for sorting context | `Official` |
| `get_browsed_scrollpos` | Current browser scroll position (numeric) | `Official` |
| `get_browsed_scrollsize` | Total browser scroll range (numeric) | `Official` |
| `get_browsed_selection_index` | Index of the selected row | `Official` |
| `get_browsed_folder` | Name of the currently open folder | `Official` |
| `get_browsed_folder_path` | Full path of the currently open folder | `Official` |
| `get_browsed_folder_icon` | Icon identifier for the current folder | `Official` |
| `get_browsed_folder_tab` | Active browser tab | `Official` |
| `get_browsed_folder_scrollpos` | Folder list scroll position | `Official` |
| `get_browsed_folder_scrollsize` | Folder list scroll range | `Official` |
| `get_browsed_folder_selection_index` | Selected row in the folder list | `Official` |

Contrast with deck metadata verbs (loaded track, not browsed):
`get_artist`, `get_title`, `get_bpm`, `get_key`, `get_genre`, `get_comment`.

Browser info panel example (skin XML):

```xml
<group x="0" y="0">
  <textzone>
    <pos x="0" y="0"/><size width="400" height="20"/>
    <text fontsize="13" weight="bold" color="white" action="get_browsed_artist_title"/>
  </textzone>
  <textzone>
    <pos x="0" y="22"/><size width="200" height="18"/>
    <text fontsize="11" color="#93A1B1" format="`get_browsed_bpm` BPM  `get_browsed_key`"/>
  </textzone>
  <textzone>
    <pos x="0" y="42"/><size width="400" height="18"/>
    <text fontsize="11" color="#93A1B1" action="get_browsed_genre"/>
  </textzone>
  <visual type="color" source="get_browsed_color">
    <pos x="0" y="60"/><size width="400" height="3"/>
  </visual>
</group>
```

Source: `Official`

---

### Cue Points

#### Core cue verbs

| Canonical | Aliases | Surfaces | Description | Source |
| --- | --- | --- | --- | --- |
| `cue` | — | `Map`, `SkinAction` | Set or jump to the main cue point. Hold to set while stopped; press during play to jump. | `Official` |
| `cue_stop` | — | `Map`, `SkinAction`, `SkinQuery` | Jump to cue and stop. Query: returns `on` when at cue position. | `Official` |
| `cue_play` | — | `Map`, `SkinAction` | Jump to cue and play. Releases to cue position on up if held. | `Official` |
| `cue_button` | — | `Map`, `SkinAction` | Hold-to-preview cue behavior: plays from cue while held, returns on release. | `Official` |
| `cue_cup` | — | `Map`, `SkinAction` | CUP (Cue Up and Play): jump to cue and immediately start playing. | `Official` |
| `cue_3button` | — | `Map`, `SkinAction` | Three-button cue mode (Cue / Play / Stop). | `Official` |
| `cue_select` | — | `Map`, `SkinAction` | Select the active cue point by number. | `Official` |
| `cue_color` | — | `Text`, `SkinQuery` | Returns the color of the specified cue point. | `Official` |
| `cue_name` | — | `Text` | Returns the name of the specified cue point. | `Official` |
| `cue_pos` | — | `Text`, `SkinQuery` | Returns the position of the specified cue point. | `Official` |
| `cue_action` | — | `Map`, `SkinAction` | Perform a cue-specific action (context-dependent). | `Official` |
| `cue_loop` | — | `Map`, `SkinAction` | Set a loop at the cue point. | `Official` |
| `cue_loop_hold` | — | `Map`, `SkinAction` | Hold-triggered cue loop. | `Official` |
| `cue_loop_autosync` | — | `Map`, `SkinAction` | Auto-sync cue loop to beat grid. | `Official` |
| `cue_display` | — | `SkinQuery`, `Text` | Returns display state of the cue panel or cue overlay. | `Official` |
| `cue_countdown` | — | `Text` | Returns countdown to the next cue point. | `Official` |
| `cue_countup` | — | `Text` | Returns time elapsed since the last cue point. | `Official` |
| `cue_counter` | — | `Text` | Returns the total number of cue points set on the loaded track. | `Official` |
| `cues_options` | — | `SkinAction` | Open the cue options menu. | `Official` |
| `goto_cue` | — | `Map`, `SkinAction` | Jump to a cue point by number: `goto_cue 1`, `goto_cue +1` (next). | `Official` |
| `auto_cue` | — | `Map`, `SkinAction` | Toggle auto-cue (jump to first beat on load). | `Official` |

#### Cue point numbering

Cue points are numbered from `1`. Most verbs accept a literal slot number or `+1`/`-1` to step through them.

#### `cue_pos` and position format

`cue_pos` returns position in the unit determined by the current `display_time` setting.
When used in a `query=""` or condition, it returns `on` if that cue slot is set, `off` if empty.

```vdjscript
cue_pos 1
cue_pos 1 ? on : off
```

#### Pad page pattern: 8 hot cues with color

```xml
<pad1 name="`cue_name 1`" color="cue_pos 1 ? cue_color 1 : dim"
      query="cue_pos 1 ? on : off">
  cue_pos 1 ? goto_cue 1 : cue_select 1 &amp; cue
</pad1>
```

Breakdown:
- `color=` uses `cue_color 1` when the cue is set, falls back to `dim`
- `query=` lights the pad only when the cue is set
- action: if set, jump to it; if not, select slot 1 and set a cue there

Source: `Official`

---

## Broad Verb Index

The sections below remain useful as a wide local inventory. They are still being normalized to the same API standard used above, especially around aliases, surface notes, and source-status markers.

## Flow Control

| Verb       | Description                         | Example                         |
| ---------- | ----------------------------------- | ------------------------------- |
| `nothing`  | Do nothing                          | `nothing`                       |
| `up`       | Execute action on key press/release | `up ? action1 : action2`        |
| `down`     | Execute action on key press/release | `down ? action1 : action2`      |
| `isrepeat` | Check if key is auto-repeating      | `isrepeat ? nothing : goto_cue` |

## Parameters & Constants

| Verb                        | Description                    | Example                                                |
| --------------------------- | ------------------------------ | ------------------------------------------------------ |
| `true` / `on` / `yes`       | Returns true                   | `true`                                                 |
| `false` / `no` / `off`      | Returns false                  | `false`                                                |
| `constant` / `get_constant` | Return specified value         | `get constant 75%`                                     |
| `dim`                       | Equivalent to `constant 0.1`   | `dim`                                                  |
| `color_mix`                 | Mix two colors based on action | `color_mix white red \`get_limiter\``                  |
| `color`                     | Return color value             | `color "red"`, `color "#C08040"`, `color 0.8 0.5 0.25` |

## Parameter Comparison & Math

| Verb                             | Description                     | Example                                           |
| -------------------------------- | ------------------------------- | ------------------------------------------------- |
| `param_bigger` / `param_greater` | Check if value is bigger        | `param_bigger 0 ? action1 : action2`              |
| `param_equal`                    | Check if value equals something | `param_equal \`get_browsed_song 'type'\` "audio"` |
| `param_contains`                 | Check if value contains string  | `param_contains`                                  |
| `param_smaller`                  | Check if value is smaller       | `param_smaller 0 ? action1 : action2`             |
| `param_add`                      | Add values                      | `param_add \`get_var a\` \`get_var b\``           |
| `param_multiply`                 | Multiply value                  | `param_multiply 300% & effect slider`             |
| `param_1_x`                      | Invert value (1/x)              | `param_1_x & effect slider`                       |
| `param_pow`                      | Power calculation               | `param_pow 0.5` (square root)                     |
| `param_invert`                   | Invert value (1-x)              | `param_invert & pitch_slider`                     |
| `param_mod`                      | Wrap value                      | `param_mod`                                       |
| `param_pingpong`                 | Linear to forth-and-back scale  | `param_pingpong`                                  |
| `param_cast`                     | Cast to new type                | `param_cast "percentage"`                         |
| `param_delta`                    | Transform absolute to relative  | `param_delta`                                     |
| `param_uppercase`                | Convert to uppercase            | `param_uppercase`                                 |
| `param_lowercase`                | Convert to lowercase            | `param_lowercase`                                 |
| `param_ucfirst`                  | First letter uppercase          | `param_ucfirst`                                   |

### Cast Types

- `integer`, `float`, `percentage`, `ms`, `boolean`, `beats`, `text`
- `int_trunc` - integer part without rounding
- `frac` - decimal part
- `relative`, `absolute` - change parameter type

## Timing & Animation

| Verb                  | Description                              | Example                               |
| --------------------- | ---------------------------------------- | ------------------------------------- |
| `blink`               | Toggle LED on/off                        | `blink 1000ms`, `blink 1bt`           |
| `fadeout`             | Fade out when condition ends             | `fadeout 10000ms 3000ms \`loop\``     |
| `pulse`               | True for duration when action turns true | `is_using 'equalizer' & pulse 2000ms` |
| `param_make_discrete` | Make smooth encoder discrete             | `param_make_discrete 0.1`             |

## Repeat & Delay

| Verb                   | Description                 | Example                                 |
| ---------------------- | --------------------------- | --------------------------------------- |
| `repeat`               | Repeat action while pressed | `repeat 1000ms & browser_scroll +1`     |
| `repeat_start`         | Start repeating action      | `repeat_start 'name' 1000ms 5 & action` |
| `repeat_start_instant` | Start repeating immediately | `repeat_start_instant 'name' 1000ms`    |
| `repeat_stop`          | Stop repeat                 | `repeat_stop 'name'`                    |
| `wait`                 | Wait between actions        | `wait 1bt & pause`                      |
| `holding`              | Execute if held long        | `holding ? automix : mix_now`           |
| `doubleclick`          | Execute if double-clicked   | `doubleclick ? automix : mix_now`       |

## Skin Control

| Verb                        | Description             | Example                                   |
| --------------------------- | ----------------------- | ----------------------------------------- |
| `skin_panel`                | Show/hide panel         | `skin_panel 'my_panel' on`                |
| `skin_panelgroup`           | Change panel in group   | `skin_panelgroup 'groupname' 'panelname'` |
| `skin_panelgroup_available` | Set panel availability  | `skin_panelgroup_available`               |
| `lock_panel`                | Acts on split elements  | `lock_panel`                              |
| `show_splitpanel`           | Show/hide split panel   | `show_splitpanel 'sidelist'`              |
| `rack`                      | Open/close rack unit    | `rack 'rack1' 'unit1'`                    |
| `rack_solo`                 | Open unit full size     | `rack_solo 'rack1' 'unit1'`               |
| `rack_prioritize`           | Prioritize unit         | `rack_prioritize 'rack1' 'unit1'`         |
| `zoom` / `zoom_scratch`     | Zoom horizontal         | `zoom`                                    |
| `zoom_vertical`             | Zoom vertical           | `zoom_vertical`                           |
| `load_skin`                 | Load new skin/variation | `load_skin ':newvariation'`               |
| `skin_empty_buttons`        | Query/toggle empty custom button space | `skin_empty_buttons`          |
| `is_using`                  | Query whether a feature was recently used | `is_using 'filter' 1000ms`   |

### Skin Context Notes

- `is_using` is built for temporary context panels and stacked feedback. Official feature names include `filter`, `equalizer`, `loop`, `cue`, `sample`, `pads`, `effect`, and `load`.
- Optional timing parameters keep the state true long enough for UI feedback, for example `is_using 'sample' 1000ms 8000ms`.

## Custom Buttons & Multi-buttons

| Verb                 | Description          | Example                          |
| -------------------- | -------------------- | -------------------------------- |
| `custom_button`      | Custom button action | `custom_button`                  |
| `custom_button_name` | Get/set button name  | `custom_button_name`             |
| `has_custom_button`  | Check if has action  | `has_custom_button`              |
| `custom_button_edit` | Open editor          | `custom_button_edit`             |
| `multibutton`        | Click multibutton    | `multibutton "my_button"`        |
| `multibutton_select` | Open selection menu  | `multibutton_select "my_button"` |

## System Info

| Verb                   | Description              | Example                             |
| ---------------------- | ------------------------ | ----------------------------------- |
| `get_cpu`              | CPU activity             | `get_cpu`                           |
| `get_clock`            | Current time             | `get_clock`, `get_clock 12` (AM/PM) |
| `get_date`             | Current date             | `get_date "%Y/%m/%d"`               |
| `is_pc` / `is_windows` | Check if PC              | `is_pc`                             |
| `is_mac` / `is_macos`  | Check if Mac             | `is_mac`                            |
| `has_notch`            | Check for display notch  | `has_notch`                         |
| `get_battery`          | Battery level            | `get_battery`                       |
| `is_battery`           | Running on battery       | `is_battery`                        |
| `has_battery`          | Has batteries            | `has_battery`                       |
| `system`               | Sparse official system helper | `system`                       |
| `debug`                | Display the incoming parameter value | `debug`                    |
| `show_keyboard`        | Show onscreen keyboard   | `show_keyboard`                     |
| `system_volume`        | Change system volume     | `system_volume`                     |
| `has_system_volume`    | Can modify system volume | `has_system_volume`                 |
| `handshake`            | Developer plugin environment handshake | `handshake 'nonce'`        |

### System Notes

- `debug` is mainly useful while developing mappings because it displays the parameter value a controller or script path is sending.
- `handshake` is for plugin developers. Pass a string, then verify the encrypted response using VirtualDJ's public key before trusting that the caller is a real VirtualDJ environment.
- `system` is official but currently has sparse public prose; keep usage behind local testing.

## Variables

| Verb             | Description                   | Example                                     |
| ---------------- | ----------------------------- | ------------------------------------------- |
| `var`            | Conditional based on variable | `var "my_var" ? action1 : action2`          |
| `var_equal`      | Check equality                | `var_equal "my_var" 42 ? action1 : action2` |
| `var_not_equal`  | Check inequality              | `var_not_equal "my_var" 42`                 |
| `var_smaller`    | Check less than               | `var_smaller "my_var" 42`                   |
| `var_greater`    | Check greater than            | `var_greater "my_var" 42`                   |
| `set_var_dialog` | Dialog to set var             | `set_var_dialog 'varname'`                  |
| `set`            | Set variable value            | `set 'varname' 5`                           |
| `toggle`         | Toggle true/false             | `toggle "my_var"`                           |
| `cycle`          | Increment with wrap           | `cycle "my_var" 42`                         |
| `get_var`        | Get variable value            | `get_var "varname"`                         |
| `set_var`        | Set variable value            | `set_var`                                   |
| `var_list`       | Show variables window         | `var_list`                                  |
| `controllervar`  | Controller-unique variable    | `controllervar`                             |

### Skin Variables and Reloading

Working skins commonly use custom variable names like `@$layout_4deck`, `@$skin_mode`, or `@$show_zoom_racks` for skin-local layout state:

```vdjscript
toggle '@$show_zoom_racks'
set '@$layout_4deck' 1
var_equal '@$layout_4deck' 1 ? action1 : action2
```

If a variable only drives live `visibility=""`, a reload is usually unnecessary. If it drives structural XML such as conditional `<nbdecks>`, mutually exclusive layout branches, or conditional define/color variants, pair the state change with `load_skin` so VirtualDJ reparses the skin:

```vdjscript
set '@$layout_4deck' 1 & load_skin
```

## Window Control

| Verb          | Description                  | Example                 |
| ------------- | ---------------------------- | ----------------------- |
| `close`       | Close application            | `close`                 |
| `minimize`    | Minimize to taskbar          | `minimize`              |
| `maximize`    | Maximize/fullscreen/windowed | `maximize 'fullscreen'` |
| `show_window` | Show/hide window             | `show_window`           |
| `open_stem_creator` | Open the Stem Creator workflow | `open_stem_creator` |

## Audio Playback

| Verb              | Description                 | Example                             |
| ----------------- | --------------------------- | ----------------------------------- |
| `song_pos`        | Position in song (slider)   | `song_pos`                          |
| `goto`            | Change position             | `goto +10ms`, `goto -4`, `goto 20%` |
| `goto_bar`        | Jump to beat after downbeat | `goto_bar 4`                        |
| `songpos_remain`  | Remaining time              | `songpos_remain 500ms ? blink`      |
| `songpos_warning` | Last 30s warning            | `songpos_warning`                   |
| `seek`            | Move while pressed          | `seek +2`, `seek +420ms`            |
| `reverse`         | Play backward               | `reverse`                           |
| `dump`            | Reverse temporarily         | `dump`, `dump quantized`            |
| `goto_first_beat` | Jump to first beat          | `goto_first_beat`                   |
| `goto_start`      | Go to start                 | `goto_start`                        |

## Deck Management

| Verb                 | Description             | Example                    |
| -------------------- | ----------------------- | -------------------------- |
| `swap_decks`         | Swap deck 1 and 2       | `swap_decks`               |
| `clone_deck`         | Clone deck              | `clone_deck`               |
| `clone_from_deck`    | Clone from other deck   | `clone_from_deck`          |
| `move_deck`          | Move song to other deck | `move_deck`                |
| `stems_split`        | Split stems to decks    | `stems_split vocal target` |
| `stems_split_unlink` | Unlink split stems      | `stems_split_unlink`       |
| `dualdeckmode`       | Toggle dual deck mode   | `dualdeckmode`             |
| `dualdeckmode_decks` | Dual-deck pair helper for decks 1/3 or 2/4 | `dualdeckmode_decks` |
| `mixermode`          | Query internal vs external mixer mode | `mixermode 'internal'` |
| `beat_juggle`        | Alternate beat jumps forward and backward | `beat_juggle 0.5` |
| `beatjump`           | Jump beats              | `beatjump +1`              |
| `beatjump_select`    | Set jump size           | `beatjump_select 4`        |
| `beatjump_page`      | Change jump offset      | `beatjump_page`            |
| `beatjump_pad`       | Execute jump            | `beatjump_pad`             |

### Deck Management Notes

- `mixermode` returns true for internal mixer mode and false for external mixer mode; pass `internal` or `external` to test explicitly.
- `beat_juggle` alternates direction each time it runs. Pass a beat amount such as `0.5` for half-beat juggling.
- `dualdeckmode_decks` is official but sparsely documented; official prose ties it to dual-deck mode applying to deck pairs 1/3 or 2/4, so test controller mappings that depend on it.

## Play Controls

| Verb             | Description           | Example          |
| ---------------- | --------------------- | ---------------- |
| `play`           | Start deck            | `play`           |
| `play_stutter`   | Start or restart      | `play_stutter`   |
| `play_pause`     | Toggle play/pause     | `play_pause`     |
| `pause_stop`     | Pause or stop         | `pause_stop`     |
| `stop`           | Stop to cue/beginning | `stop`           |
| `pause`          | Pause deck            | `pause`          |
| `play_button`    | Depends on play_mode  | `play_button`    |
| `stop_button`    | Depends on play_mode  | `stop_button`    |
| `pioneer_play`   | Pioneer-style play LED/helper state | `pioneer_play` |
| `pioneer_cue`    | Pioneer-style cue button/LED helper state | `pioneer_cue` |
| `emergency_play` | Play something        | `emergency_play` |

## Audio Inputs

| Verb                  | Description               | Example                   |
| --------------------- | ------------------------- | ------------------------- |
| `mic` / `microphone`  | Toggle microphone         | `mic`                     |
| `mic_talkover`        | Lower decks, activate mic | `mic_talkover 20% 1000ms` |
| `mic_eq_low`          | Microphone low EQ         | `mic_eq_low`              |
| `mic_eq_mid`          | Microphone mid EQ         | `mic_eq_mid`              |
| `mic_eq_high`         | Microphone high EQ        | `mic_eq_high`             |
| `mic_volume`          | Set mic volume            | `mic_volume`              |
| `aux_volume`          | Set aux input volume      | `aux_volume`              |
| `linein`              | Activate line input       | `deck 1 linein 2 on`      |
| `linein_rec`          | Record line input         | `linein_rec`              |
| `mic_rec`             | Record microphone         | `mic_rec`                 |
| `mic2_volume`         | Set second microphone volume | `mic2_volume`          |
| `djc_mic`             | Controller/mic helper     | `djc_mic`                 |

## Scratch & Jogwheel

| Verb                          | Description            | Example                  |
| ----------------------------- | ---------------------- | ------------------------ |
| `touchwheel` / `scratchwheel` | Jogwheel with touch    | `touchwheel +1.0`        |
| `touchwheel_touch`            | Touch detection        | `touchwheel_touch`       |
| `jogwheel` / `jog`            | Jogwheel without touch | `jogwheel +1.0`          |
| `motorwheel`                  | Motorized jogwheel     | `motorwheel "move" +1.0` |
| `speedwheel`                  | Position and speed     | `speedwheel +1.0 1.5`    |
| `vinyl_mode`                  | Set vinyl/CD mode      | `vinyl_mode`             |
| `wheel_mode`                  | Change wheel mode      | `wheel_mode +1`          |
| `hold` / `scratch_hold`       | Stop for scratching    | `hold on`                |
| `scratch`                     | Scratch forward/back   | `scratch +120ms`         |
| `nudge`                       | Nudge position         | `nudge +120ms`           |
| `slip_mode`                   | Slip mode              | `slip_mode`              |
| `slip`                        | Global slip mode       | `slip`                   |
| `get_slip_active`             | Slip currently active  | `get_slip_active`        |
| `get_slip_time`               | Time that will resume when slip exits | `get_slip_time "sec"` |
| `get_rotation_slip`           | Slip point jog angle, otherwise normal rotation | `get_rotation_slip` |
| `blink_play`                  | End-of-track/paused blink helper | `blink_play on`     |
| `scratch_dna`                 | Execute DNA scratch    | `scratch_dna`            |
| `scratch_dna_option`          | Configure Scratch DNA behavior | `scratch_dna_option "quantized"` |
| `scratch_dna_editor`          | Open DNA editor        | `scratch_dna_editor`     |
| `jog_wheel`                   | Official alias of `jogwheel` | `jog_wheel +1.0`    |
| `scratch_wheel`               | Official alias of `touchwheel` / `scratchwheel` | `scratch_wheel +1.0` |
| `scratch_wheel_touch` / `scratchwheel_touch` / `speedwheel_touch` | Official aliases of `touchwheel_touch` | `scratch_wheel_touch on` |
| `motor_switch`                | Assign deck to motorized wheel | `motor_switch`       |
| `motorwheel_instant_play`     | Start instantly on motorized-wheel decks | `motorwheel_instant_play on` |
| `scratchbank_assign`          | Assign dropped file to scratchbank slot | `scratchbank_assign 1` |
| `scratchbank_load`            | Scratchbank page load/helper | `scratchbank_load`     |
| `scratchbank_load_to_deck`    | Load scratchbank slot to deck, or return its label/color in pad contexts | `scratchbank_load_to_deck 1` |
| `scratchbank_edit`            | Open scratchbank editor/menu | `scratchbank_edit`       |

Scratchbank source note:

- The official Scratchbank pad page uses `drop="scratchbank_assign <n>"`, `scratchbank_load_to_deck <n>` for pad action/color/label, `scratchbank_load` as Parameter 1, and `scratchbank_edit` in the menu.

## Volume & Mixing

| Verb               | Description       | Example                      |
| ------------------ | ----------------- | ---------------------------- |
| `crossfader` / `crossfader_slider` | Move crossfader | `crossfader 50%` |
| `auto_crossfade` / `auto_crossfader` | Auto crossfade | `auto_crossfade 2000ms` |
| `level` / `level_slider` / `volume` / `volume_slider` | Set deck volume | `level` |
| `mute`             | Mute deck         | `mute`                       |
| `gain` / `gain_slider` / `power_gain` | Set gain | `gain`          |
| `gain_label`       | Gain label text   | `gain_label`                 |
| `gain_relative`    | Move gain relative to software position | `gain_relative +1%` |
| `set_gain`         | Set gain to dBA   | `set_gain 0`                 |
| `colorfx_prefader` | Make ColorFX prefader for controller compatibility | `colorfx_prefader` |
| `master_volume`    | Master volume     | `master_volume`              |
| `booth_volume`     | Booth volume      | `booth_volume 70%`           |
| `headphone_volume` | Headphone volume  | `headphone_volume`           |
| `headphone_mix`    | PFL mix           | `headphone_mix`              |
| `headphone_crossfader` | PFL left/right fader | `headphone_crossfader 50%` |
| `headphone_gain`   | PFL output gain   | `headphone_gain +1dB`        |
| `master_balance`   | Master left/right balance | `master_balance 50%`    |
| `mono_mix`         | Mix left/right channels together | `mono_mix`             |
| `fake_mixer`       | Tell VirtualDJ not to apply mixer volumes to sound output | `fake_mixer` |
| `fake_eq`          | Tell VirtualDJ not to apply EQ to sound output | `fake_eq` |
| `fake_gain`        | Tell VirtualDJ not to apply gain to sound output | `fake_gain` |
| `fake_filter`      | Tell VirtualDJ not to apply filter to sound output | `fake_filter` |
| `fake_hp`          | Tell VirtualDJ not to apply headphone volume to headphone output | `fake_hp` |
| `fake_hpmix`       | Tell VirtualDJ not to apply headphone mix to headphone output | `fake_hpmix` |
| `fake_pfl`         | Disable skin PFL switching when PFL is controlled elsewhere | `fake_pfl` |
| `fake_master`      | Tell VirtualDJ not to apply master volume to master output | `fake_master` |
| `crossfader_curve` | Crossfader curve  | `crossfader_curve "scratch"` |
| `crossfader_hamster` | Invert crossfader | `crossfader_hamster`       |
| `crossfader_disable` | Disable crossfader | `crossfader_disable`       |
| `levelfader_curve` / `fader_curve` | Level fader curve | `levelfader_curve 50%` |
| `get_limiter`      | Check compression | `get_limiter`                |
| `get_level`        | Signal level      | `get_level`                  |
| `get_level_log`    | Log-scaled signal level | `get_level_log`          |
| `get_level_peak`   | Peak level before master volume | `get_level_peak`        |
| `get_level_left`   | Left channel before master volume | `get_level_left 'master'` |
| `get_level_right`  | Right channel before master volume | `get_level_right 'master'` |
| `get_level_left_peak` | Left peak before master volume | `get_level_left_peak` |
| `get_level_right_peak` | Right peak before master volume | `get_level_right_peak` |
| `get_vu_meter`     | VU meter level    | `get_vu_meter`               |
| `get_vu_meter_peak` | VU peak after master volume | `get_vu_meter_peak`     |
| `get_vu_meter_left` | Left VU after master volume | `get_vu_meter_left 'master'` |
| `get_vu_meter_right` | Right VU after master volume | `get_vu_meter_right 'master'` |
| `get_vu_meter_left_peak` | Left VU peak after master volume | `get_vu_meter_left_peak` |
| `get_vu_meter_right_peak` | Right VU peak after master volume | `get_vu_meter_right_peak` |
| `get_crossfader_result` | Effective left/right deck mix after crossfader and levels | `get_crossfader_result` |
| `is_audible`       | Deck on-air       | `is_audible`                 |

## Automix

| Verb                   | Description            | Example                |
| ---------------------- | ---------------------- | ---------------------- |
| `automix`              | Start/stop automix     | `automix`              |
| `automix_dualdeck`     | Use both decks         | `automix_dualdeck`     |
| `automix_skip`         | Skip current song      | `automix_skip`         |
| `automix_add_next`     | Add selected songs after current automix song | `automix_add_next` |
| `automix_editor`       | Open Automix Editor    | `automix_editor`       |
| `automix_editor_movetrack` | Move selected Automix Editor track | `automix_editor_movetrack 'current' +10` |
| `get_automix`          | Automix crossfader position | `get_automix`      |
| `get_automix_song`     | Next automix song property | `get_automix_song 'title'` |
| `get_automix_position` | Current automix song position | `get_automix_position` |
| `get_playlist_time`    | Time left in automix playlist | `get_playlist_time` |
| `mix_now`              | Crossfade with sync    | `mix_now 4000ms`       |
| `mix_now_nosync`       | Crossfade without sync | `mix_now_nosync`       |
| `mix_selected`         | Mix to selected        | `mix_selected`         |
| `mix_next`             | Mix to next            | `mix_next`             |
| `mix_next_sidelist`    | Mix next using sidelist source | `mix_next_sidelist` |
| `mix_and_load_next`    | Mix and load next      | `mix_and_load_next`    |
| `playlist_options`     | Show playlist options  | `playlist_options`     |
| `playlist_add`         | Add selected songs to automix list | `playlist_add` |
| `playlist_load`        | Load folder/list into automix playlist | `playlist_load 'append'` |
| `playlist_load_and_remove` | Load first automix song and remove it | `playlist_load_and_remove` |
| `playlist_load_and_keep` | Load first automix song and keep it | `playlist_load_and_keep` |
| `playlist_randomize`   | Shuffle playlist       | `playlist_randomize`   |
| `playlist_randomize_once` | Shuffle playlist once | `playlist_randomize_once` |
| `playlist_repeat`      | Repeat playlist        | `playlist_repeat`      |
| `playlist_clear`       | Empty playlist         | `playlist_clear`       |
| `playlist_save`        | Save playlist to file  | `playlist_save`        |
| `playlist_remove_played` | Remove played songs from playlist | `playlist_remove_played` |
| `playlist_remove_duplicates` | Remove duplicate playlist songs | `playlist_remove_duplicates` |
| `switch_sidelist_playlist` | Exchange playlist and sidelist contents | `switch_sidelist_playlist` |
| `relay_play`           | Auto-start opposite deck at track end | `relay_play` |
| `sidelist_options`     | Show sidelist options  | `sidelist_options`     |
| `sidelist_clear`       | Clear sidelist         | `sidelist_clear`       |
| `sidelist_add`         | Add selected songs to sidelist | `sidelist_add` |
| `sidelist_load`        | Load folder/list into sidelist | `sidelist_load 'append'` |
| `sidelist_load_and_remove` | Load first sidelist song and remove it | `sidelist_load_and_remove` |
| `sidelist_load_and_keep` | Load first sidelist song and keep it | `sidelist_load_and_keep` |

## Browser

| Verb                   | Description                 | Example                      |
| ---------------------- | --------------------------- | ---------------------------- |
| `browser_scroll`       | Scroll songs/folders        | `browser_scroll +1`          |
| `browser_move`         | Move song in playlist       | `browser_move +1`            |
| `browser_folder`       | Focus folders               | `browser_folder`             |
| `browser_enter`        | Load or focus songs         | `browser_enter`              |
| `browser_open_folder`  | Expand/collapse folder      | `browser_open_folder`        |
| `browser_remove`       | Remove from playlist        | `browser_remove`             |
| `browser_window`       | Change browser zone         | `browser_window 'folders'`   |
| `browser_isactive`     | Recently used by controller | `browser_isactive`           |
| `browser_geniusdj`     | Lookup recommendations      | `browser_geniusdj playing`   |
| `browser_shortcut`     | Assign/jump browser shortcut | `browser_shortcut 1`        |
| `search`               | Focus search or search text | `search "text"`              |
| `search_add`           | Append to search query      | `search_add "house"`         |
| `search_delete`        | Remove last search character | `search_delete`             |
| `clear_search`         | Clear search                | `clear_search`               |
| `edit_search`          | Focus search without clearing | `edit_search`              |
| `log_search`           | Log current search          | `log_search`                 |
| `search_playlists`     | Find playlists containing song | `search_playlists deck`   |
| `search_folder`        | Search folders/lists        | `search_folder dialog`       |
| `search_options`       | Search field options        | `search_options 'composer'`  |
| `search_folder_options` | Folder-search options      | `search_folder_options`      |
| `browser_gotofolder`   | Go to folder                | `browser_gotofolder "/path"` |
| `recurse_folder`       | Include selected folder subfolders | `recurse_folder`       |
| `browser_sort`         | Sort browser                | `browser_sort "artist"`      |
| `sideview_sort`        | Sort sideview               | `sideview_sort "artist"`     |
| `grid_view`            | Grid view mode              | `grid_view`                  |
| `view_options`         | Browser view options        | `view_options`               |
| `sideview_options`     | Sideview shortcut options   | `sideview_options`           |
| `sideview_triggerpad`  | Toggle sideview sampler mode | `sideview_triggerpad`       |
| `file_info`            | Open tag editor             | `file_info`                  |
| `browsed_file_info`    | Open browsed-song Tag Editor | `browsed_file_info`         |
| `browsed_file_color`   | Set file color              | `browsed_file_color "red"`   |
| `browsed_file_reveal`  | Reveal browsed song in OS file manager | `browsed_file_reveal` |
| `browsed_file_analyze` | Reanalyze file              | `browsed_file_analyze`       |
| `browsed_file_prepare_stems` | Prepare stems for selected browser file(s) | `browsed_file_prepare_stems` |
| `browsed_file_reload_tag` | Reload browsed file tag from source file | `browsed_file_reload_tag` |
| `browsed_file_rename` | Rename browsed file          | `browsed_file_rename`        |
| `set_browsed_file_bpm` | Set BPM for selected browser songs | `set_browsed_file_bpm 129.3` |
| `browsed_song`       | Set browsed file property | `browsed_song 'rating' 5` |
| `loaded_song`        | Set loaded track property | `loaded_song 'rating' 5` |
| `browsed_song_hashtag` | Add/remove hashtag on browsed song | `browsed_song_hashtag 'user 1' '#tag'` |
| `loaded_song_hashtag` | Add/remove hashtag on loaded song | `loaded_song_hashtag 'user 1' '#tag'` |
| `edit_comment`        | Edit selected track comment | `edit_comment`               |
| `add_favoritefolder`  | Make folder a favorite/monitored folder | `add_favoritefolder` |
| `add_filterfolder`    | Create filter folder        | `add_filterfolder`           |
| `add_to_list` / `virtualfolder_add` | Add selected songs to list | `add_to_list 'Warmup'` |
| `create_list_from_playlist` / `create_virtualfolder_from_playlist` | Save automix list in MyLists | `create_list_from_playlist` |
| `quick_filter`         | Toggle browser quick filter | `quick_filter 'Has Lyrics is not ""'` |
| `has_quick_filter`     | Check if quick filter exists | `has_quick_filter 1`        |
| `browser_padding`      | Change browser line padding | `browser_padding 50%`        |
| `font_size`            | Change browser font size    | `font_size +1`               |
| `sidereco_options`     | Sideview recommendation panel options | `sidereco_options`    |
| `sidereco_song`        | Recommendation-panel song helper | `sidereco_song`          |
| `sidereco_source`      | Recommendation-panel source helper | `sidereco_source`      |
| `mark_linked_tracks` / `mark_related_tracks` | Link decks 1 and 2 as related tracks | `mark_linked_tracks` |
| `has_linked_tracks`    | Check linked/related tracks | `has_linked_tracks browsed` |
| `page`                 | Browser/page helper | `page`                     |

## Loading

| Verb            | Description         | Example               |
| --------------- | ------------------- | --------------------- |
| `load`          | Load song           | `load`, `load "path"` |
| `load_pulse`    | Brief pulse on load | `load_pulse`          |
| `load_pulse_active` | Pulse when a new song becomes audible | `load_pulse_active 1000ms 5000ms` |
| `loaded`        | Check if loaded     | `loaded`              |
| `not_played`    | Do not mark this deck's song as played | `not_played` |
| `undo_load`     | Reload previous     | `undo_load`           |
| `unload`        | Unload song         | `unload`              |
| `load_next`     | Load next track     | `load_next`           |
| `load_previous` | Load previous track | `load_previous`       |
| `save_deck_set` | Save current loaded-deck configuration | `save_deck_set` |
| `load_deck_set` | Load a saved deck-set file | `load_deck_set` |

## Cue Points

| Verb                 | Description              | Example                  |
| -------------------- | ------------------------ | ------------------------ |
| `cue_stop`           | Cue with preview         | `cue_stop`, `cue_stop 1` |
| `cue_play`           | Cue with hold-to-play    | `cue_play 1 1000ms`      |
| `cue`                | Jump to cue              | `cue`, `cue 1`           |
| `hot_cue` / `hotcue` | Set or jump to cue       | `hot_cue 1`              |
| `silent_cue`         | Mute until cue activated | `silent_cue`             |
| `cue_select`         | Select default cue       | `cue_select`             |
| `set_cue`            | Store cue position       | `set_cue 1 500ms`        |
| `goto_cue`           | Jump to cue              | `goto_cue 1`             |
| `delete_cue`         | Delete cue               | `delete_cue 1`           |
| `cue_pos`            | Get cue position         | `cue_pos 1`              |
| `cue_name`           | Get/set cue name         | `cue_name 1`             |
| `has_cue`            | Check if cue exists      | `has_cue 1`              |
| `cue_color`          | Get/set cue color        | `cue_color 1 'yellow'`   |
| `cue_loop`           | Jump and loop            | `cue_loop`               |
| `lock_cues`          | Lock/unlock cues         | `lock_cues`              |
| `shift_all_cues`     | Shift all cue points by a time offset | `shift_all_cues -10ms` |
| `sort_cues`          | Sort cue points chronologically | `sort_cues`        |
| `quantize_setcue`    | Quantize newly set cues  | `quantize_setcue`        |

### Cue Point Notes

- `cue_pos <n>` returns the position of cue point `<n>` as a percentage of the track, which makes it especially useful anywhere a skin element expects a progress-style value.
- `cue_pos` also supports alternate outputs such as `msec`, `sec`, `min`, `mseconly`, and `beats`.
- In skin XML, pair `cue_pos` with `has_cue <n>` when you want a marker or fill to appear only after that cue exists.
- `shift_all_cues <offset>` is a repair tool for tracks whose cue points are globally early or late, such as old imports that need `shift_all_cues -10ms`.
- `sort_cues` rewrites cue ordering chronologically; avoid putting it on an accidental one-tap control.

### Working `cue_pos` Examples

Basic queries:

```text
cue_pos 1
cue_pos 1 beats
cue_pos 1 mseconly
```

Custom progress bar up to Hot Cue 1:

```xml
<group name="cue_1_progress">
  <square color="#11161D">
    <pos x="40" y="200"/>
    <size width="300" height="6"/>
  </square>

  <visual source="cue_pos 1" type="linear" orientation="horizontal" visibility="has_cue 1">
    <pos x="40" y="200"/>
    <size width="300" height="6"/>
    <off shape="square" color="transparent"/>
    <on shape="square" color="`cue_color 1`"/>
  </visual>
</group>
```

This draws a thin bar from the start of the track up to Hot Cue 1. It is a simple way to turn `cue_pos` into a custom progress overlay above or below a `songpos` bar.

Read-only cue marker driven by a slider:

```xml
<slider action="cue_pos 1" orientation="horizontal" visibility="has_cue 1">
  <pos x="40" y="192"/>
  <size width="300" height="18"/>
  <fader>
    <size width="3" height="18"/>
    <off shape="square" color="`cue_color 1`"/>
  </fader>
</slider>
```

Here the slider range becomes a simple placement track, and the `fader` sits at the cue location. This works well as a thin overlay on top of a `songpos` bar when you want a marker instead of a fill.

## Deck Selection

| Verb              | Description                | Example              |
| ----------------- | -------------------------- | -------------------- |
| `select`          | Select working deck        | `select`             |
| `masterdeck`      | Select/unselect master     | `masterdeck`         |
| `masterdeck_auto` | Auto masterdeck            | `masterdeck_auto`    |
| `leftdeck`        | Select left deck           | `leftdeck +1`        |
| `rightdeck`       | Select right deck          | `rightdeck +1`       |
| `invert_deck`     | Swap left/right deck       | `invert_deck`        |
| `leftcross`       | Assign to left crossfader  | `leftcross`          |
| `rightcross`      | Assign to right crossfader | `rightcross`         |
| `cross_assign`    | Assign deck to crossfader side or through state | `deck 3 cross_assign 'left'` |
| `pfl`             | Send to headphones         | `pfl`, `pfl 75%`     |
| `get_deck_color`  | Get deck color             | `get_deck_color 50%` |

### Crossfader Assignment Notes

- `leftcross` and `rightcross` assign a deck to the left or right side of the audio crossfader.
- `cross_assign` is the more explicit side selector and supports values such as `left`, `right`, and `thru`.
- Use deck scoping when assigning a specific deck: `deck 3 cross_assign 'left'`.

## Equalizer & Stems

| Verb                   | Description           | Example                           |
| ---------------------- | --------------------- | --------------------------------- |
| `eq_mode`              | Select EQ behavior    | `eq_mode +1`, `eq_mode frequency` |
| `mute_stem`            | Mute stem             | `mute_stem vocal`                 |
| `only_stem`            | Isolate stem          | `only_stem vocal`                 |
| `stem_color`           | Get default stem color | `stem_color 'Vocal'`             |
| `stem_pad`             | Mute/isolate stem pad | `stem_pad 'acapella' on`          |
| `has_stems`            | Check if has stems    | `has_stems "ready"`               |
| `stems_bleed`          | Stem bleed control/query | `stems_bleed`                   |
| `eq_high`              | High EQ/HiHat/Vocal   | `eq_high`                         |
| `eq_mid`               | Mid EQ/Melody/Vocals  | `eq_mid`                          |
| `eq_low`               | Low EQ/Kick           | `eq_low`                          |
| `high_label`           | High EQ band label    | `` `high_label` ``                |
| `mid_label`            | Mid EQ band label     | `` `mid_label` ``                 |
| `low_label`            | Low EQ band label     | `` `low_label` ``                 |
| `eq_crossfader_high`   | Crossfade treble between decks | `eq_crossfader_high 50%` |
| `eq_crossfader_mid` / `eq_crossfader_med` | Crossfade mids between decks | `eq_crossfader_mid 50%` |
| `eq_crossfader_low`    | Crossfade bass between decks | `eq_crossfader_low 50%` |
| `stem`                 | Control stem amount   | `stem "vocal" 50%`                |
| `eq_kill_high/mid/low` | Kill EQ band          | `eq_kill_high`                    |
| `filter`               | Apply color FX        | `filter`                          |
| `filter_activate`      | Enable/disable deck filter/ColorFX | `filter_activate`         |
| `filter_selectcolorfx` | Select color effect   | `filter_selectcolorfx 'Reverb'`   |

`filter_selectcolorfx`: pops up a gui selector for colorfx effects
`filter_selectcolorfx 'Echo'`: selects the echo effect
`filter_selectcolorfx 'Filter'`: selects the filter effect

### Stem Names

- Individual: `Vocal`, `HiHat`, `Bass`, `Instru`, `Kick`
- Aggregate: `Melody` (Instru+Bass), `Rhythm` (HiHat+Kick), `MeloRhythm`, `Acapella`, `Instrumental`

### Stem Isolation Notes

- **Official**: `only_stem <stem>` isolates the named stem. `mute_stem <stem>` mutes the named stem.
- **Local test**: for common vocal/instrumental isolation, prefer the aggregate stem-pad states: `stem_pad 'acapella' on` and `stem_pad 'instrumental' on`. These force the selected aggregate state on in isolation, so they are cleaner than `only_stem <stem> on/off` for those two cases.
- **Local test**: `only_stem <stem> on` and `only_stem <stem> off` are accepted, but they are state-dependent rather than simple absolute setters.
- `only_stem 'vocal' on`: if vocal is already on, this turns the non-vocal stems off. If vocal is off, the first press turns vocal on and leaves the other stems untouched; a second press then isolates vocal.
- `only_stem 'vocal' off`: mirror behavior for the non-vocal side. If vocal is already off, this turns the non-vocal stems on. If vocal is on, the first press turns vocal off and leaves the other stems untouched; a second press then isolates the non-vocal stems.
- For arbitrary deterministic combinations beyond the aggregate stem-pad states, use `mute_stem <stem> on/off` and explicitly set the stems you want muted or unmuted.

### EQ Crossfader Notes

- `eq_crossfader_high`, `eq_crossfader_mid` / `eq_crossfader_med`, and `eq_crossfader_low` crossfade EQ bands between decks instead of changing one deck's EQ amount.
- Use the label helpers when a skin should display the active EQ mode's band names instead of hard-coded `HIGH`, `MID`, and `LOW`.

```text
eq_crossfader_high 50%
eq_crossfader_mid 50%
eq_crossfader_low 50%
`high_label`
```

## Get (Query Actions)

| Verb               | Description           | Example                       |
| ------------------ | --------------------- | ----------------------------- |
| `get_beatpos`      | Beat position         | `get_beatpos`                 |
| `get_beat`         | Beat intensity at current position | `get_beat`          |
| `get_bpm`          | Song BPM              | `get_bpm`, `get_bpm absolute` |
| `get_time`         | Elapsed time          | `get_time "remain" "short"`   |
| `get_rotation`     | Disc angle            | `get_rotation`                |
| `get_position`     | Song position         | `get_position`                |
| `get_deck`         | Deck number           | `get_deck`                    |
| `get_artist`       | Artist tag            | `get_artist`                  |
| `get_title`        | Title tag             | `get_title`                   |
| `get_title_before_remix` | Title with remix/bracket handling | `get_title_before_remix` |
| `get_remix_after_title` | Remix text split from title | `get_remix_after_title` |
| `get_album`        | Album tag             | `get_album`                   |
| `get_genre`        | Genre tag             | `get_genre`                   |
| `get_key`          | Song key              | `get_key "musical"`           |
| `get_harmonic`     | Harmonic key display  | `get_harmonic`                |
| `get_key_color`    | Color for current key | `get_key_color`               |
| `get_browsed_song` | Browsed file property | `get_browsed_song 'title'`    |
| `get_loaded_song`  | Loaded file property  | `get_loaded_song 'album'`     |
| `has_lyrics`       | Loaded deck has lyrics | `has_lyrics`                 |
| `get_lyrics_language` | Loaded deck lyric language | `get_lyrics_language`      |
| `get_status`       | Background task text  | `get_status`                  |

## Karaoke

| Verb                    | Description             | Example                             |
| ----------------------- | ----------------------- | ----------------------------------- |
| `karaoke`               | Start/stop karaoke      | `karaoke`                           |
| `karaoke_show`          | Show singer list        | `karaoke_show`                      |
| `karaoke_options`       | Open karaoke options    | `karaoke_options`                   |
| `karaoke_venue_name`    | Karaoke venue-name helper | `` `karaoke_venue_name` ``        |
| `get_next_karaoke_song` | Get upcoming track info | `get_next_karaoke_song "singer" +1` |
| `is_karaoke_idle`       | Karaoke idle check      | `is_karaoke_idle`                   |
| `is_karaoke_playing`    | Karaoke playing check   | `is_karaoke_playing`                |

## Key & Pitch

| Verb                   | Description            | Example                     |
| ---------------------- | ---------------------- | --------------------------- |
| `key`                  | Change key (semitones) | `key +1`                    |
| `key_smooth`           | Change key (smooth)    | `key_smooth +0.5`           |
| `key_move`             | Move key by semitones  | `key_move +1`               |
| `set_key`              | Match exact key        | `set_key "A#m"`             |
| `match_key`            | Match compatible key   | `match_key`                 |
| `key_match_button`     | Match the other deck's key on first press, or reset key on second press | `key_match_button` |
| `key_match_menu`       | Open key-match menu    | `key_match_menu`            |
| `keycue_pad`           | Key-cue pad helper     | `keycue_pad 1`              |
| `keycue_pad_color`     | Key-cue pad color      | `keycue_pad_color 1`        |
| `keycue_pad_page`      | Key-cue pad page/window | `keycue_pad_page`          |
| `keycue_pad_jump`      | Key-cue jump option    | `keycue_pad_jump`           |
| `key_lock` / `keylock` | Lock key               | `key_lock`                  |
| `pitch`                | Set pitch              | `pitch 112%`, `pitch +0.1%` |
| `pitch2` / `pitch2_slider` | Official aliases of `pitch` / `pitch_slider` | `pitch2 112%` |
| `pitch_relative`       | Relative pitch helper for controllers | `pitch_relative +0.1%` |
| `pitch_motorized`      | Motorized pitch helper | `pitch_motorized`           |
| `pitch_zero`           | Reset to 0%            | `pitch_zero`                |
| `pitch_reset`          | Slowly return to 0%    | `pitch_reset 5%`            |
| `pitch_range`          | Set pitch range        | `pitch_range 12%`           |
| `pitch_bend`           | Temporary bend         | `pitch_bend +3%`            |
| `pitch_lock` / `pitchlock` | Link pitch sliders between matched decks | `pitch_lock on` |
| `startupspeed`         | Vinyl-style start ramp | `startupspeed 2000ms`       |
| `brakespeed`           | Vinyl-style brake ramp | `brakespeed 2000ms`         |
| `backspin`             | Trigger backspin       | `backspin 4bt`              |
| `master_tempo`         | Toggle master tempo    | `master_tempo`              |
| `get_pitch`            | Get pitch value        | `get_pitch`                 |
| `get_pitch_value`      | Get pitch on 0-200 scale centered on 100 | `get_pitch_value` |
| `get_pitch_zero`       | Check whether pitch is zero/original | `get_pitch_zero 'absolute' 0.1%` |

### Key, Pitch And Motor Notes

- `key_match_button` matches the other deck's key on first press, then resets the key on second press.
- `key_match_menu` is the popup/menu partner and is a natural `rightclick=""` action for key displays.
- `pitch <number>` treats the value as pitch-slider position within the current `pitch_range`; `pitch <percent>` sets absolute playback speed, so `pitch 112%` means +12%.
- `pitch_relative` is for hardware controls that should move relative to the software pitch position instead of replacing it with an absolute hardware value.
- `pitch_lock` links matched deck pitch sliders so moving one keeps the match by moving the other.
- `startupspeed` and `brakespeed` control vinyl-style ramp behavior; larger values mean longer ramp times.
- `backspin` accepts explicit durations such as `5000ms` or beat lengths such as `4bt`.

```text
pitch 130 bpm
pitch_relative +0.1%
pitch_lock on
startupspeed 1500ms
brakespeed 2bt
backspin 4bt
```

## Loops

| Verb          | Description          | Example                            |
| ------------- | -------------------- | ---------------------------------- |
| `loop`        | Set/remove loop      | `loop 4`, `loop 10ms`, `loop 200%` |
| `loop_in`     | Set loop start       | `loop_in`                          |
| `loop_out`    | Set loop end         | `loop_out`                         |
| `loop_length` | Change loop length   | `loop_length 0.5`                  |
| `loop_move`   | Move loop            | `loop_move +2`                     |
| `loop_double` | Double loop          | `loop_double`                      |
| `loop_half`   | Halve loop           | `loop_half`                        |
| `loop_exit`   | Remove loop          | `loop_exit`                        |
| `reloop`      | Jump to loop start   | `reloop`                           |
| `reloop_exit` | Remove or reactivate | `reloop_exit`                      |
| `loop_save`   | Save loop            | `loop_save 1`, `loop_save "name"`  |
| `loop_load`   | Load saved loop      | `loop_load 1`                      |
| `saved_loop`  | Load or set loop     | `saved_loop 1`                     |
| `saved_loop_prepare` | Prepare/load saved loop or set it if missing | `saved_loop_prepare 1` |
| `saved_loop_display` | Saved-loop pad label/display mode | `` `saved_loop_display 1` `` |
| `saved_loop_autotrigger` | Auto-trigger saved loop when playhead reaches it | `saved_loop_autotrigger 1` |
| `loop_color`  | Saved-loop color     | `loop_color 1`                     |
| `loop_delete` | Delete saved loop    | `loop_delete 1`                    |
| `loop_load_prepare` | Prepare/load saved loop and query prepared state | `loop_load_prepare 1` |
| `loop_roll`   | Loop roll            | `loop_roll 0.25`                   |
| `quantize_loop` | Quantize loops/rolls | `quantize_loop`                   |
| `slicer`      | Slicer effect        | `slicer 1`                         |
| `loop_adjust` | Adjust loop with jog | `loop_adjust 'move'`               |
| `loop_button` | Smart one-button loop control | `loop_button`              |
| `pioneer_loop_in` | Pioneer-style loop in helper | `pioneer_loop_in`        |
| `pioneer_loop_out` | Pioneer-style loop out helper | `pioneer_loop_out`     |
| `pioneer_loop` | Pioneer-style loop helper | `pioneer_loop`               |
| `loop_select` | Select/default loop size | `loop_select 4`                |
| `loop_position` | Current position inside active loop | `loop_position`       |
| `get_active_loop` | Current active loop length | `get_active_loop`          |
| `get_loop` | Active loop length or default loop size | `get_loop`              |
| `get_loop_in_time` | Loop start time | `get_loop_in_time "sec"`       |
| `get_loop_out_time` | Loop end time | `get_loop_out_time "sec"`       |
| `loop_pad` | Trigger predefined loop pad | `loop_pad 1`                    |
| `loop_pad_page` | Cycle loop pad page | `loop_pad_page +1`             |
| `loop_pad_mode` | Cycle loop pad behavior | `loop_pad_mode +1`           |
| `loop_options` | Show loop options menu | `loop_options`                 |
| `loop_back` | Toggle loop-back mode | `loop_back`                      |
| `loop_roll_mode` | Toggle loop roll release behavior | `loop_roll_mode`     |
| `repeat_song` | Restart the current song when it reaches the end | `repeat_song on` |

### Loop Behavior Notes

- `repeat_song` restarts the whole loaded track at the end. It is separate from active loop state and saved-loop slots.

### Saved Loop Notes

- `loop_load <n>` jumps to and activates an existing saved loop.
- `loop_load_prepare <n>` activates/deactivates the saved loop without jumping to its start point.
- `saved_loop <n>` loads an existing saved loop, or stores the current loop in that slot if it does not exist.
- `saved_loop_prepare <n>` is the prepare-style equivalent: activate/deactivate an existing saved loop without jumping, or set it if missing.
- `saved_loop_display <n>` follows the `savedLoopDisplay` option and is suitable for pad labels. Use `saved_loop_display +1` or named menu entries to change the display mode.
- `loop_color <n>` can query or set the color of a saved loop, making it the right color source for saved-loop pads.
- `saved_loop_autotrigger <n>` toggles whether the saved loop should trigger automatically when playback reaches it.

### Saved Loop Examples

```text
loop_load 1
loop_load_prepare 1
saved_loop_prepare 1
saved_loop_autotrigger 1
saved_loop_display 'length'
loop_color 1 'yellow'
```

```xml
<pad1 name="`saved_loop_display 1`" color="loop_color 1"
      query="loop_load 1 ? loop_load_prepare 1 ? blink : on : off">
  holding ? loop_delete 1 : loop_load 1 ? loop_load_prepare 1 : loop_save 1
</pad1>
```

## Pads

| Verb               | Description             | Example                            |
| ------------------ | ----------------------- | ---------------------------------- |
| `pad`              | Activate pad            | `pad 1`                            |
| `pad_page`         | Activate page           | `pad_page 1`, `pad_page 'hotcues'` |
| `pad_edit`         | Edit page               | `pad_edit`                         |
| `pad_param`        | Change param 1          | `pad_param`                        |
| `pad_param2`       | Change param 2          | `pad_param2`                       |
| `pad_pressure`     | Pad pressure amount     | `pad_pressure 1`                   |
| `pad_has_param`    | Check whether pad page exposes a parameter | `pad_has_param 1`      |
| `pad_param_visible` | Check/display pad parameter visibility | `pad_param_visible 1` |
| `pad_color`        | Get pad color           | `pad_color 1`                      |
| `pad_button_color` | Controller button color | `pad_button_color 1`               |
| `pad_pushed`       | Check whether pad is currently pressed | `pad_pushed 1`            |
| `padshift`         | Force shifted pad action | `padshift 1`                      |
| `padshift_pressure` | Force shifted pad pressure action | `padshift_pressure 1` |
| `padshift_button_color` | Force shifted pad button color | `padshift_button_color 1` |
| `pad_menu`         | Open current pad page menu | `pad_menu`                      |
| `pad_has_action`   | Check whether pad has an action | `pad_has_action 1`          |
| `pad_has_pressure` | Check whether pad has pressure behavior | `pad_has_pressure 1` |
| `pad_has_color`    | Check whether pad has color behavior | `pad_has_color 1`       |
| `pad_has_menu`     | Check whether pad page has menu | `pad_has_menu`             |
| `pad_has_16pads`   | Controller exposes 4x4 pads | `pad_has_16pads`             |
| `pad_bank2`        | Switch skin display between pads 1-8 and 9-16 | `pad_bank2` |
| `padfx`            | Activate named effect   | `padfx "echo" 40% 90%`             |
| `padfx_single`     | Activate single padfx   | `padfx_single "reverb"`            |

## Effects

| Verb                  | Description                         | Example                           |
| --------------------- | ----------------------------------- | --------------------------------- |
| `effect_select`       | Select effect (deactivate previous) | `effect_select 1 "echo"`          |
| `effect_select_multi` | Select effect (keep previous)       | `effect_select_multi 2 "flanger"` |
| `effect_select_toggle` | Select effect and keep activation continuity | `effect_select_toggle 1 "echo"` |
| `effect_select_popup` | Select effect with temporary dropdown | `effect_select_popup 1` |
| `effect_list`         | Select/cycle effect list            | `effect_list 1 +1`                |
| `effect_list_edit`    | Edit an effect list                 | `effect_list_edit 1`              |
| `effect_active`       | Activate/deactivate                 | `effect_active 1 on`              |
| `effect_disable_all`  | Disable deck/master effects         | `effect_disable_all`              |
| `effect_slider`       | Move effect slider                  | `effect_slider 1 2 50%`           |
| `effect_slider_skip_length` | Move slider while skipping length slider | `effect_slider_skip_length 1 2 50%` |
| `effect_slider_active` / `effect_slider_activate` | Move slider while activating effect | `effect_slider_active 1` |
| `effect_slider_reset` | Reset effect slider to default      | `effect_slider_reset 1 2`         |
| `effect_button`       | Press effect button                 | `effect_button 1 2`               |
| `effect_colorfx`      | Select effect for a custom ColorFX slot | `effect_colorfx 1 "echo"`     |
| `colorfx_slider`      | Adjust ColorFX parameter            | `colorfx_slider 50%`              |
| `effect_colorslider`  | Center-off custom ColorFX-style control | `effect_colorslider 1`        |
| `effect_releaseslider` | Control release-FX slider          | `effect_releaseslider`            |
| `effect_releaseslider_active` | Control release-FX slider and activate | `effect_releaseslider_active` |
| `effect_mixfx`        | Associate effect with crossfader    | `effect_mixfx`                    |
| `effect_mixfx_select` | Select Mix FX                       | `effect_mixfx_select "filter"`    |
| `effect_mixfx_activate` | Toggle Mix FX                     | `effect_mixfx_activate`           |
| `effect_stems`        | Route effects to selected stems     | `effect_stems 'vocal'`            |
| `effect_stems_color`  | Get color for the `effect_stems` button | `effect_stems_color`          |
| `effect_arm_stem`     | Arm stems for `stems` slot effect actions | `effect_arm_stem Vocal+Bass` |
| `effect_bpm_deck`     | Set/get custom plugin BPM for this deck | `effect_bpm_deck 120`        |
| `effect_bpm_deck_tap` | Tap custom plugin BPM for this deck | `effect_bpm_deck_tap`             |
| `effect_arm_deck`     | Select target deck/path for armed FX | `effect_arm_deck master`         |
| `effect_arm_select`   | Select effect for armed FX          | `effect_arm_select "echo"`        |
| `effect_arm_select_popup` | Popup selector for armed FX     | `effect_arm_select_popup`         |
| `effect_arm_slot`     | Toggle armed FX slot participation  | `effect_arm_slot 1`               |
| `effect_arm_active`   | Activate selected armed effect      | `effect_arm_active`               |
| `effect_arm_slider`   | Move armed effect parameter         | `effect_arm_slider 1 2`           |
| `effect_arm_slider_name` | Get armed effect parameter name  | `effect_arm_slider_name 1 short`  |
| `effect_arm_slider_text` | Get armed effect parameter text  | `effect_arm_slider_text 1`        |
| `effect_arm_slider_label` | Get armed effect parameter label | `effect_arm_slider_label 1 short` |
| `effect_arm_beats`    | Change armed effect speed           | `effect_arm_beats 1`              |
| `effect_arm_bpm`      | Get BPM of armed deck target        | `effect_arm_bpm`                  |
| `effect_fxsendreturndeck` | Select FX send/return source deck | `effect_fxsendreturndeck`     |
| `effect_fxsendreturndeck_multi` | Select source for multi send/return | `effect_fxsendreturndeck_multi mic` |
| `effect_fxsendreturnenable` | Enable/query FX send/return path | `effect_fxsendreturnenable` |
| `effect_bank_save`    | Save deck FX slots 1-6 to bank      | `effect_bank_save 1`              |
| `effect_bank_load`    | Load deck FX slots 1-6 from bank    | `effect_bank_load 1`              |
| `effect_clone`        | Clone all three FX slots from another deck | `effect_clone`            |
| `effect_3slots_layout` | Toggle 1-slot/3-slot FX layout     | `effect_3slots_layout`            |
| `video_fx_select`     | Select video effect                 | `video_fx_select "my_plugin"`     |
| `video_fx`            | Activate/deactivate selected video effect | `video_fx`                |
| `video_fx_clear`      | Deactivate all video effects        | `video_fx_clear`                  |
| `video_fx_slider` / `video_fx_slider_slider` | Move video FX slider | `video_fx_slider 1 50%` |
| `video_fx_button`     | Press video FX button               | `video_fx_button 1`               |
| `video_source`        | Activate/select video source        | `video_source`                    |
| `video_source_select` | Select video source plugin          | `video_source_select "webcam"`    |
| `video_transition_select` | Select video transition plugin | `video_transition_select "fade"` |
| `video_transition_slider` / `video_transition_slider_slider` | Move transition slider | `video_transition_slider 1 50%` |
| `video_transition_button` | Press transition button         | `video_transition_button 1`       |
| `effect_beats`        | Set beat parameter                  | `effect_beats`                    |
| `effect_beats_all`    | Set beat parameter across slots/layouts | `effect_beats_all`          |
| `effect_has_beats`    | Check effect beat parameter support | `effect_has_beats`                |
| `effect_has_length`   | Check effect length parameter support | `effect_has_length`             |
| `is_releasefx`        | Query release-FX slot state         | `is_releasefx`                    |
| `get_effect_name`     | Get effect name                     | `get_effect_name`                 |
| `get_effect_title`    | Get effect title                    | `get_effect_title`                |
| `get_effect_string` / `effect_string` | Get/set effect string text | `get_effect_string`  |
| `get_effect_string_name` | Get effect string label         | `get_effect_string_name`          |
| `get_effect_button_name` | Get effect button name          | `get_effect_button_name 1`        |
| `get_effect_slider_label_full` | Get full effect slider label | `get_effect_slider_label_full 1` |
| `get_effect_slider_shortname` | Get compact effect slider label | `get_effect_slider_shortname 2` |
| `get_effect_slider_name` | Get effect slider name          | `get_effect_slider_name 1`        |
| `get_effect_slider_name_skip_length` | Get effect slider name while skipping length slider | `get_effect_slider_name_skip_length 1` |
| `get_effect_slider_label` | Get effect slider label        | `get_effect_slider_label 1`       |
| `get_effect_slider_label_skip_length` | Get effect slider label while skipping length slider | `get_effect_slider_label_skip_length 1` |
| `get_effect_slider_text` | Get effect slider value text    | `get_effect_slider_text 1`        |
| `get_effect_slider_text_skip_length` | Get slider text while skipping length slider | `get_effect_slider_text_skip_length 1` |
| `get_effect_slider_default` | Get effect slider default value | `get_effect_slider_default 1` |
| `get_effect_button_shortname` | Get compact effect button label | `get_effect_button_shortname 2` |
| `get_effect_button_count` | Get number of effect buttons     | `get_effect_button_count`         |
| `get_effect_slider_count` | Get number of effect sliders     | `get_effect_slider_count`         |
| `effect_has_button`   | Check if effect has button          | `effect_has_button 2`             |
| `effect_has_slider`   | Check if effect has slider          | `effect_has_slider 1 2`           |
| `effects_used`        | Query whether effects are active    | `effects_used "deck"`             |
| `get_effects_used`    | Count active effects                | `get_effects_used`                |
| `effect_dock_gui`     | Dock/undock effect GUI              | `effect_dock_gui 1`               |
| `show_pluginpage`     | Show/hide plugin control windows    | `show_pluginpage`                 |
| `pluginsongpos`       | Plugin song position helper         | `pluginsongpos`                   |
| `effect_command`      | Send command to effect/plugin       | `effect_command`                  |
| `get_videofx_name`    | Get selected video effect name      | `get_videofx_name`                |
| `get_videotrans_name` | Get selected video transition name  | `get_videotrans_name`             |
| `get_video_fx_slider_label` | Get video FX slider label     | `get_video_fx_slider_label 1`     |

## POI & BPM

| Verb            | Description      | Example                        |
| --------------- | ---------------- | ------------------------------ |
| `beat_tap`      | Tap to set BPM   | `beat_tap`                     |
| `edit_poi`      | Open POI editor  | `edit_poi`                     |
| `edit_bpm`      | Open BPM editor  | `edit_bpm`                     |
| `edit_lyrics`   | Open Lyrics Editor | `edit_lyrics`                 |
| `set_bpm`       | Set BPM          | `set_bpm 129.3`, `set_bpm 50%` |
| `adjust_cbg`    | Adjust beat grid | `adjust_cbg +2`                |
| `goto_mixpoint` | Jump to automix/mix point | `goto_mixpoint "StartCut"` |
| `set_mixpoint`  | Move automix/mix point to current position | `set_mixpoint "StartTempo"` |
| `set_loadpoint` | Set where the track starts when loaded | `set_loadpoint` |
| `set_firstbeat` | Set first beat   | `set_firstbeat`                |
| `reanalyze`     | Reanalyze file   | `reanalyze multi`              |

### Mix Point Notes

- Mix point names include `StartTempo`, `EndTempo`, `StartCut`, `EndCut`, `StartFade`, `EndFade`, `StartSound`, and `EndSound`.
- `goto_mixpoint` moves playback to a named mix point; `set_mixpoint` writes that named point at the current position.
- `set_loadpoint` controls the position where the track starts when loaded.

## Sampler

| Verb                         | Description                                                      | Example                                                   |
| ---------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------- |
| `sampler_play`               | Play the selected or specified sample slot                       | `sampler_play 4`                                          |
| `sampler_play_stutter`       | Play sample and restart it from the beginning if already playing | `sampler_play_stutter 4`                                  |
| `sampler_play_stop`          | Play sample if stopped, or stop it if already playing            | `sampler_play_stop 4`                                     |
| `sampler_stop`               | Stop one sample or all currently playing samples                 | `sampler_stop 4`, `sampler_stop all`                      |
| `sampler_pad`                | Trigger the currently exposed sampler pad slot; in display/name contexts it can also return the visible pad label | `sampler_pad 1`, `` `sampler_pad 1` `` |
| `sampler_pad_shift`          | Stop a sample if playing, delete it otherwise                    | `sampler_pad_shift 1`                                     |
| `sampler_pad_page`           | Change/query the current 8-pad sampler window                    | `sampler_pad_page +1`, `sampler_pad_page -1`              |
| `sampler_velocity`           | Velocity/pressure value for a sampler pad                        | `sampler_velocity 1`                                      |
| `sampler_assign`             | Assign a `.vdjsample` file to a slot                             | `sampler_assign 1 "/Samples/horn.vdjsample"`              |
| `sampler_loaded`             | Check whether the visible sampler pad slot currently has a sample loaded | `sampler_loaded 1`, `sampler_loaded 1 "auto"`     |
| `sampler_color`              | Get the color of the visible sampler pad slot                    | `sampler_color 1`                                         |
| `sampler_select` / `sampler_default` | Select the default sampler slot for the deck             | `sampler_select 5`, `sampler_default +1`                  |
| `sampler_position`           | Get the current playback position of the selected sample         | `sampler_position`                                        |
| `sampler_bank`               | Select or cycle sampler banks                                    | `sampler_bank "birthday"`, `sampler_bank +1`              |
| `sampler_mute`               | Mute or unmute a sample                                          | `sampler_mute 4`                                          |
| `sampler_edit`               | Open the Sample Editor for a sample                              | `sampler_edit 4`                                          |
| `sampler_mode` / `sampler_rapidfire` | Set global or per-sample trigger mode                    | `sampler_mode 1 'stutter'`, `sampler_rapidfire +1`        |
| `sampler_output`             | Route sampler output to master, trigger deck, headphones, etc.   | `sampler_output "headphones"`, `deck master sampler_output` |
| `sampler_options`            | Open or toggle sampler bank options                              | `sampler_options`, `sampler_options "locked"`             |
| `sampler_volume_master`      | Set the sampler master volume                                    | `sampler_volume_master +5%`                               |
| `sampler_pfl`                | Send sampler to headphones or set sampler PFL volume             | `sampler_pfl 75%`                                         |
| `sampler_volume`             | Set sample volume by absolute slot or sample name                | `sampler_volume 9 75%`, `sampler_volume "siren" 75%`      |
| `sampler_pad_volume`         | Set sample volume by visible sampler pad position                | `sampler_pad_volume 1 75%`                                |
| `sampler_volume_nogroup`     | Adjust one sample without also changing other samples in its group | `sampler_volume_nogroup 9 75%`                          |
| `sampler_group_volume`       | Adjust all samples in a sampler group                            | `sampler_group_volume "horns" 75%`                        |
| `sampler_group_color`        | Get the color of a sampler group                                 | `sampler_group_color "horns"`                             |
| `sampler_group_name`         | Get the name of a sampler group                                  | `sampler_group_name 1`                                    |
| `sampler_group_mute`         | Mute/unmute a sampler group                                      | `sampler_group_mute "horns"`                              |
| `sampler_has_group`          | Check whether a group exists in the current bank                 | `sampler_has_group "horns"`                               |
| `sampler_load_to_deck`       | Load the selected sampler slot to a deck                         | `sampler_load_to_deck`                                    |
| `sampler_loop`               | Change the loop length of a sample or set it explicitly          | `sampler_loop 1 1`, `sampler_loop +1`                     |
| `sampler_rec`                | Record a sample from the deck, mic, or master                    | `sampler_rec`, `sampler_rec "mic"`, `sampler_rec 1`       |
| `sampler_start_rec`          | Start recording a new sample                                     | `sampler_start_rec "master"`                              |
| `sampler_stop_rec`           | Stop recording and save the sample                               | `sampler_stop_rec`                                        |
| `sampler_abort_rec`          | Cancel recording and delete the unfinished sample                | `sampler_abort_rec`                                       |
| `sampler_rec_delete`         | Delete a sample from the Recordings bank                         | `sampler_rec_delete 3`                                    |
| `sampler_used` / `get_sampler_used` | Check whether any sample, or a specific count of samples, is playing | `sampler_used`, `sampler_used 4`                  |
| `get_sampler_slot`           | Get the sampler slot that currently has focus                    | `get_sampler_slot`                                        |
| `get_sampler_count`          | Get the number of slots in the current sampler bank              | `get_sampler_count`                                       |
| `get_sample_name`            | Get the name of an absolute sample slot                          | `get_sample_name 9`                                       |
| `get_sample_info`            | Read sample metadata such as `fullpath`, `group`, or `length`    | `get_sample_info 9 fullpath`                              |
| `get_sampler_bank`           | Get the name of the active sampler bank                          | `get_sampler_bank`                                        |
| `get_sampler_bank_id`        | Get the numeric id of the active sampler bank                    | `get_sampler_bank_id`                                     |
| `get_sampler_bank_count`     | Get the total number of sampler banks                            | `get_sampler_bank_count`                                  |
| `get_sample_color`           | Get the actual stored color of a sample slot                     | `get_sample_color 9`                                      |

### Sampler Modes

- `on/off` - One press starts the sample, the next press stops it, or it stops when it reaches the end.
- `hold` - The sample plays only while the pad is held.
- `stutter` - Each press restarts the sample from the beginning.
- `unmute` - The sample keeps running, but is only audible while the pad is held.

### Sampler Notes

- `sampler_pad_page` is the pager behind Parameter 2 on the default Sampler pad page and is the main way to reach `9-16`, `17-24`, and later sub-pages in banks with more than 8 samples.
- For drag-and-drop assignment on custom pad pages, use pad `drop="sampler_assign <absolute-slot>"`.
- Treat `sampler_assign` as an absolute-slot helper unless you have verified a build-specific page-aware variant; the current official docs do not show an `"auto"` form for it.
- `sampler_pad`, `sampler_loaded`, `sampler_color`, and `sampler_pad_volume` are the safest page-aware helpers when building sampler pad pages.
- In display contexts such as pad `name=` fields and skin/text `format=` fields, `sampler_pad 1` through `sampler_pad 8` are the safest way to show the current visible sample names on the active sampler page.
- For visibility and empty-slot checks in paged sampler UIs, `sampler_loaded 1` through `sampler_loaded 8` already follow the visible sampler page, so you usually do not need to infer emptiness from a blank `sampler_pad` label.
- `sampler_play`, `sampler_stop`, `sampler_volume`, `get_sample_name`, `get_sample_info`, and `get_sample_color` are best treated as absolute-slot helpers.
- `sampler_default` is the official alias of `sampler_select`; prefer `sampler_select` in new docs unless documenting older mappings.
- `sampler_rapidfire` is the official alias of `sampler_mode`; prefer `sampler_mode` for clarity.
- Use `sampler_color` when you want the color of the currently visible sampler pad. Use `get_sample_color` when you want the actual stored color of a specific bank slot.
- In skins, do not assume a normal `<button>` exposes a drag callback that mirrors pad `drop=`. The current skin docs describe click handlers on `<button>` and separate `<dropzone>` elements for drag targets.
- Samples triggered from a deck sync to that deck. If you want a pad page to follow a predictable sync source, trigger through an explicit deck:

```text
deck active sampler_pad 1 "auto"
deck master sampler_pad 1 "auto"
```

- `deck master` means the current master deck context, not a separate global sampler namespace.
- In skin XML, raw `deck master sampler_pad <n>` can be less reliable than an explicit deck number in some sampler title/query paths. If a paged sampler title shows the wrong slot, resolve the master deck explicitly:

```text
deck 1 masterdeck ? deck 1 sampler_pad 1 : deck 2 masterdeck ? deck 2 sampler_pad 1 : deck 3 masterdeck ? deck 3 sampler_pad 1 : deck 4 masterdeck ? deck 4 sampler_pad 1 : sampler_pad 1
```

- If you want the traditional left-deck `1-8` and right-deck `9-16` behavior, either page the second deck manually with `sampler_pad_page +1` or enable the `samplerSpanAcrossDecks` option.

### Sampler Group Notes

- Sampler group helpers accept a group name or group index where the official appendix says either form is valid.
- Use `sampler_group_mute` when the UI should mute a logical group instead of a single sample slot.
- Use `sampler_volume_nogroup` when one sample must change without also changing other samples in the same group.
- `sampler_has_group` is useful before showing group controls for banks that may not define that group.
- `sampler_load_to_deck` loads the selected sampler slot to a deck; for scratchbank-style workflows, prefer the dedicated `scratchbank_load_to_deck`.

### Working Sampler Examples

```text
sampler_pad 1
sampler_loaded 1 "auto" ? sampler_pad 1 "auto" : sampler_rec 1 "auto"
sampler_pad_page +1
sampler_bank +1
sampler_options "locked"
sampler_pad_volume 1 75%
sampler_volume 9 75%
sampler_has_group "horns" ? sampler_group_mute "horns" : nothing
sampler_group_volume "horns" 75%
sampler_load_to_deck
```

```xml
<pad1 drop="sampler_assign 1">...</pad1>
```

### Sampler Source Notes

- Official verbs: [VDJScript verbs](https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html)
- Default sampler page behavior: [Pads manual](https://www.virtualdj.com/manuals/virtualdj/interface/decks/decksadvanced/pads.html)
- Sampler bank drag-and-drop and unlocked-bank behavior: [Sampler manual](https://www.virtualdj.com/manuals/virtualdj/interface/browser/sideview/sampler.html)
- Skin drag targets: [Skin SDK Dropzone](https://www.virtualdj.com/wiki/Skin%20SDK%20Dropzone.html)
- Skin button API: [Skin Button](https://virtualdj.com/wiki/Skin-Button.html)
- Trigger modes and loop sync settings: [Sample Editor](https://www.virtualdj.com/manuals/virtualdj/editors/sampleeditor.html)
- Page-aware custom pad page examples: [Custom Sampler Pad Page](https://www.virtualdj.com/forums/253061/General_Discussion/Custom_Sampler_Pad_Page_%28Recording__Looping__Adjust_Beatgrid_and_more%29.html)
- Deck sync guidance: [problem with (pad pages) pads sampler sync](https://virtualdj.com/forums/224203/VirtualDJ_Technical_Support/problem_with_%28pad_pages%29_pads_sampler_sync%21_please_help___is_it_a_bug%3F%3F.html)
- Master-deck sampler quirks in newer builds: [Virtual Dj 2025 Sampler Sync](https://virtualdj.com/forums/265522/VirtualDJ_Technical_Support/Virtual_Dj_2025_Sampler_Sync.html)
- Paging and `9-16` behavior: [No longer possible to access 16 samples from controllers with 8 x 2 pads?](https://virtualdj.com/forums/261416/VirtualDJ_Technical_Support/No_longer_possible_to_access_16_samples_from_controllers_with_8_x_2_pads_.html)
- Explicit matrix/layout argument: [Using Xone K2 to control the sampler](https://www.virtualdj.com/forums/261102/VirtualDJ_Technical_Support/Using_Xone_K2_to_control_the_sampler.html)

## Sync

| Verb           | Description                 | Example          |
| -------------- | --------------------------- | ---------------- |
| `sync`         | Synchronize with other deck | `sync`           |
| `match_bpm`    | Match BPM only              | `match_bpm`      |
| `is_sync`      | Query synchronized BPM/phase state | `is_sync` |
| `match_gain`   | Match gain to the other deck | `match_gain` |
| `play_sync`    | Play synchronized           | `play_sync`      |
| `play_onbeat`  | Play synchronized to local beat | `play_onbeat` |
| `beatlock`     | Keep synchronized           | `beatlock`       |
| `smart_fader`  | Sync while crossfading      | `smart_fader`    |
| `phrase_sync`  | Match phrase                | `phrase_sync 16` |
| `quantize_all` | Set all quantize options    | `quantize_all`   |
| `auto_bpm_transition` | Gradually move BPM toward the other deck | `auto_bpm_transition` |
| `auto_bpm_transition_options` | Configure auto BPM transition features | `auto_bpm_transition_options "length"` |
| `get_bpm_match` | Return BPM match amount | `get_bpm_match` |
| `sync_hint` | Query sync hint such as pitch or phase | `sync_hint "phase"` |
| `bpm_stabilizer` | Lock fluid track to current BPM | `bpm_stabilizer` |

## Video

| Verb               | Description             | Example                   |
| ------------------ | ----------------------- | ------------------------- |
| `leftvideo`        | Assign left video       | `leftvideo +1`            |
| `rightvideo`       | Assign right video      | `rightvideo +1`           |
| `leftvideo_button` | Button helper for left video source | `deck 3 leftvideo_button` |
| `rightvideo_button` | Button helper for right video source | `deck 3 rightvideo_button` |
| `video`            | Open/close video window | `video`                   |
| `video_output`     | Select monitor          | `video_output 1`          |
| `video_crossfader` | Video crossfader        | `video_crossfader`        |
| `video_crossfader_link` | Link video crossfader to audio crossfader | `video_crossfader_link on` |
| `video_crossfader_auto` | Automatically move video crossfader based on deck activity | `video_crossfader_auto on` |
| `video_fadetoblack` | Fade video to black from volume sliders | `video_fadetoblack on` |
| `video_delay`      | Offset video/audio sync delay | `video_delay +100ms`     |
| `video_level`      | Independent fade-to-black video level | `video_level 50%`        |
| `video_transition` | Launch transition       | `video_transition 1000ms` |
| `is_video`         | Check if has video      | `is_video`                |
| `is_audioonlyvisualisation` | Check whether audio-only visualisation is running | `is_audioonlyvisualisation` |
| `over_video` / `overvideo` | Force this deck's video output to video master | `over_video on` |

### Video Notes

- `leftvideo` and `rightvideo` assign decks to the video crossfader sides; the `_button` variants are simple source-button helpers for skins or mappings.
- `video_crossfader_link` ties the video crossfader to the audio crossfader. Use `video_crossfader_auto` when VirtualDJ should move the video crossfader based on which side is playing, cueing, or scratching.
- `video_delay` accepts millisecond-style relative and reset values such as `+100ms`, `-100ms`, and `0ms`.
- `video_level` is separate from the main video crossfader and is used for fade-to-black style level control.
- `over_video` is forceful: it puts this deck's video output on the video master regardless of normal assignment logic.

### Video Examples

```text
deck 3 leftvideo
deck 4 rightvideo
video_crossfader_link on
video_crossfader_auto on
video_delay 0ms
is_video ? video_transition 1000ms : nothing
```

## Recording & Broadcasting

| Verb              | Description          | Example             |
| ----------------- | -------------------- | ------------------- |
| `record`          | Start recording      | `record`            |
| `record_cut`      | Cut to new file      | `record_cut`        |
| `record_config`   | Open record configuration | `record_config` |
| `record_vu`       | Recording signal level | `record_vu`       |
| `broadcast`       | Start/stop broadcast | `broadcast "video"` |
| `broadcast_message` | Set/query broadcast message | `broadcast_message 'Live now'` |
| `get_record_time` | Recording time       | `get_record_time`   |

## Controllers

| Verb                | Description               | Example                                  |
| ------------------- | ------------------------- | ---------------------------------------- |
| `action_deck`       | Check button deck         | `action_deck 1 ? actionA : actionB`      |
| `set_deck`          | Affect which deck         | `set_deck \`get_var varname\` & play`    |
| `device_side`       | Left/right device action  | `device_side 'left' ? action1 : action2` |
| `assign_controller` | Assign controller to deck | `deck 1 assign_controller "CDJ400" 2`    |
| `controller_mapping` | Assign a mapping to a controller | `controller_mapping "CDJ400" "My Mapping" 2` |
| `mixer_order`       | Four-deck controller mixer order | `mixer_order 3124`          |
| `controllerscreen_deck` | Controller-screen deck helper | `controllerscreen_deck` |
| `controller_battery` | Controller battery-state helper | `controller_battery` |
| `shift`             | Built-in shift variable   | `shift`                                  |
| `menu_button`       | Changeable button         | `menu_button 1 "hotcue,sampler"`         |
| `menu`              | Controller-screen menu for `menu_button` controls | `menu`             |
| `get_controller_name` | Controller name(s) assigned to deck | `get_controller_name`          |
| `get_controller_image` | Cover art for controller screens | `get_controller_image`          |
| `get_controller_screen` | Controller-screen helper | `get_controller_screen`          |
| `get_rotation_cue` | Cue point angle on jog display | `get_rotation_cue`                  |
| `get_pioneer_loop_display` | Pioneer-style loop display helper | `get_pioneer_loop_display` |
| `get_pioneer_display` | Pioneer-style display helper | `get_pioneer_display`              |
| `numark_waveform_zoom` | Numark waveform zoom level | `numark_waveform_zoom +1`        |
| `get_numark_waveform` | Numark waveform data helper | `get_numark_waveform`              |
| `get_numark_beatgrid` | Numark beatgrid display helper | `get_numark_beatgrid`          |
| `get_numark_songpos` | Numark song position display helper | `get_numark_songpos`          |
| `denon_platter` | Denon platter action/helper | `denon_platter`                    |
| `get_denon_platter` | Denon platter display helper | `get_denon_platter`                |
| `get_denon_cuepoints` | Denon cue point LED helper | `get_denon_cuepoints 100`         |
| `get_gemini_display` | Gemini display helper | `get_gemini_display`                  |
| `get_gemini_waveform` | Gemini waveform helper | `get_gemini_waveform`                |
| `gemini_waveform_zoomlevel` | Gemini waveform zoom helper | `gemini_waveform_zoomlevel` |
| `menu_cycledisplay` | Cycle single-line controller display | `menu_cycledisplay`          |
| `show_text` | Show temporary controller display text | `show_text 'Line 1|Line 2' 3000ms` |
| `invert_controllers` | Invert controller decks | `invert_controllers`                 |
| `rescan_controllers` | Rescan connected controllers | `rescan_controllers`             |
| `reinit_controller` | Reinitialize controller | `reinit_controller`                  |
| `refresh_controller` | Refresh controller displays | `refresh_controller`               |
| `midiclock_active` | Toggle MIDI clock output to a controller | `midiclock_active`       |
| `miditovst_active` | Toggle MIDI routing to deck VST instruments/effects | `miditovst_active` |
| `phase_movement` | Phase controller movement helper | `phase_movement`              |
| `phase_position` | Phase controller position helper | `phase_position`              |
| `phase_active` | Phase controller active-state helper | `phase_active`                    |
| `v7_status` | Numark V7 status helper | `v7_status`                              |
| `rzx_touch` | Pioneer RZX touch helper | `rzx_touch`                              |
| `rzx_touch_x` | Pioneer RZX touch X-position helper | `rzx_touch_x`                    |
| `rzx_touch_y` | Pioneer RZX touch Y-position helper | `rzx_touch_y`                    |
| `djc_shift` | DJC controller shift helper | `djc_shift`                            |
| `djc_button` | DJC controller button helper | `djc_button`                         |
| `djc_button_popup` | DJC controller popup-button helper | `djc_button_popup`          |
| `djc_button_slider` | DJC controller slider-button helper | `djc_button_slider`       |
| `djc_button_select` | DJC controller selection-button helper | `djc_button_select`    |
| `djc_panel` | DJC controller panel helper | `djc_panel`                            |
| `os2l_button` | Trigger named OS2L lighting button | `os2l_button 'blackout'`         |
| `os2l_scene` | Trigger or queue an OS2L scene when the deck is audible | `os2l_scene 'scene1'` |
| `os2l_cmd` | Trigger numbered OS2L command | `os2l_cmd 1 on while_pressed`         |
| `os2l_info` | Show/read OS2L lighting connection info | `os2l_info`                    |

### Controller Notes

- `assign_controller` assigns a physical controller to a deck. In a controller mapping, `deck 1 assign_controller` assigns the controller that sent the action.
- `controller_mapping` changes the mapping used by a controller. With one argument it targets the controller that ran the action; with controller name and optional instance number it can target a specific device family or unit.
- `mixer_order` is for 4-deck controller layouts; `mixer_order 3124` means the mixer strips appear left-to-right as decks 3, 1, 2, 4.
- `menu_button <n> "page,page,page"` defines controller buttons whose behavior can be changed by `menu`. Use `browser_scroll` to navigate the controller-screen menu.
- `show_text 'Line 1|Line 2' 3000ms` sends temporary text to controller displays that use `get_display`; `|` separates display lines.
- `reinit_controller` can target a specific controller and optional delay between exit/init. Use broad `reinit_controller` only when a full controller reinitialization is intended.
- `midiclock_active`, `miditovst_active`, `phase_*`, `rzx_*`, `v7_status`, `djc_*`, `controllerscreen_deck`, and `controller_battery` are official but hardware-specific or sparsely documented; keep them in mappings that can be tested on the target device.

### Controller Examples

```text
deck 1 assign_controller "CDJ400" 2
controller_mapping "CDJ400" "My Mapping" 2
mixer_order 3124
menu_button 1 "hotcue,sampler,effect,loop"
show_text 'Line 1|Line 2' 3000ms
reinit_controller "My Controller" 200ms
```

OS2L source note:

- The official DMX pad page uses `os2l_button` for named lighting buttons, `os2l_cmd <n> on while_pressed` for numbered commands, and `os2l_info` in the page menu.
- `os2l_scene` is similar to `os2l_button`, but the scene is only sent when the deck is audible; when the deck is not audible, it queues until the deck becomes audible.

## Configuration

| Verb                       | Description            | Example                               |
| -------------------------- | ---------------------- | ------------------------------------- |
| `settings` / `config`      | Open config window     | `settings`                            |
| `smart_loop`               | Auto-adjust loops      | `smart_loop`                          |
| `smart_play` / `auto_sync` | Auto-sync on play      | `smart_play`                          |
| `smart_cue`                | Auto-sync on cue       | `smart_cue`                           |
| `smart_scratch`            | Mute backward scratching | `smart_scratch`                    |
| `auto_match_bpm`           | Auto-match BPM on load | `auto_match_bpm`                      |
| `auto_match_key`           | Auto-match key on load | `auto_match_key`                      |
| `auto_pitch_lock`          | Engage pitch lock when BPMs are matched | `auto_pitch_lock`        |
| `auto_sync_settings`       | Apply automatic sync settings preset | `auto_sync_settings`      |
| `fader_start`              | Enable/disable fader start | `fader_start on`                 |
| `setting`                  | Read/write setting     | `setting "jogSensitivityScratch" 80%` |
| `setting_setsession`       | Force setting value for this session | `setting_setsession 'videoRandomTransition' on` |
| `setting_setsession_deck`  | Force deck-specific setting value for this session | `deck 1 setting_setsession_deck 'pitchRange' 12%` |
| `setting_setdefault`       | Change setting default for this session | `setting_setdefault 'jogSensitivityScratch' 80%` |
| `setting_reset`            | Reset setting to default | `setting_reset 'jogSensitivityScratch'` |
| `setting_ismodified`       | Query whether setting differs from default | `setting_ismodified 'jogSensitivityScratch'` |
| `save_config` / `saveregistryconfig` | Save config now | `save_config`                         |
| `open_help`                | Open user guide        | `open_help`                           |
| `keyboard_shortcuts`       | Show/control keyboard shortcuts overlay | `keyboard_shortcuts 500ms` |
| `select_master_output`     | Select computer/controller master output | `select_master_output` |
| `switch_skin_variation`    | Switch current skin variation | `switch_skin_variation`           |
| `play_options`             | Menu for play/cue/smart behavior | `play_options`              |
| `play_mode`                | Set play/stop/cue behavior family | `play_mode 'pioneer'`        |
| `auto_sync_options`        | Menu for auto-sync behavior | `auto_sync_options`                 |
| `deck_options`             | Open the built-in deck behavior/options popup; useful from skin `rightclick=""` when a right-click-only deck menu is needed | `deck_options`                    |
| `connect`                  | VirtualDJ account/connect action or query | `connect`                    |
| `eventscheduler`           | Open Event Scheduler   | `eventscheduler`                      |
| `eventscheduler_start`     | Start Event Scheduler  | `eventscheduler_start 'summer_wedding'` |
| `apply_audio_config`       | Apply current audio config | `apply_audio_config`              |

### Configuration Notes

- `setting_setsession` and `setting_setsession_deck` force temporary values for the current VirtualDJ session without treating them as ordinary persisted preferences.
- `setting_setdefault` and `setting_reset` are stronger controls than ordinary `setting`; avoid putting them on casual one-tap skin buttons unless the UI makes that intent clear.
- `auto_pitch_lock` ties into matched-BPM workflows: when enabled, pitch lock engages when BPMs are matched so moving one pitch slider moves the other to keep the match.
- `play_mode` controls play/stop/cue behavior families such as `numark` and `pioneer`.
- `saveregistryconfig` is the official alias of `save_config`.
- Official skins use `connect` as an account/connect button; published skins also query `connect` to show account connection state. Behavior is sparse enough to keep in local-test notes.

## Timecode

| Verb              | Description             | Example                 |
| ----------------- | ----------------------- | ----------------------- |
| `timecode_active` | Enable timecode control | `timecode_active 1 on`  |
| `invert_timecode` | Switch/invert timecode control across available decks | `invert_timecode` |
| `timecode_mode`   | Set mode                | `timecode_mode 'smart'` |
| `timecode_config` | Open timecode configuration | `timecode_config` |
| `timecode_bypass` | Use as line input       | `timecode_bypass`       |
| `timecode_reset_pitch` | Reset software pitch so deck pitch matches turntable pitch | `timecode_reset_pitch` |
| `timecode_pitch`  | Tell timecode engine a controller pitch-slider position | `timecode_pitch 100%` |
| `timecode_cd_mode` | Force timecode to CD mode | `timecode_cd_mode on` |
| `timecode_motor_enable` | Hybrid turntable motor-state helper | `timecode_motor_enable on` |
| `timecode_options` | Show timecode options  | `timecode_options`      |
| `get_hastimecode` | Check if has timecode   | `get_hastimecode`       |
| `get_timecode_quality` | Timecode signal quality | `get_timecode_quality` |

### Timecode Notes

- `timecode_active <source> on` can assign the same timecode source to multiple decks, for example `deck 1 timecode_active 1 on & deck 2 timecode_active 1 on`.
- `timecode_mode` accepts the official modes `smart`, `absolute`, and `relative`.
- Use `timecode_reset_pitch` when you need software pitch to match the turntable pitch exactly before absolute needle-drop work.
- `timecode_pitch` is for controllers that send pitch separately over MIDI while timecode controls position.
- `timecode_cd_mode` is for CD or digital devices using a vinyl-style timecode signal.

### Timecode Examples

```text
deck 1 timecode_active 1 on
timecode_mode 'relative'
timecode_reset_pitch
timecode_pitch 100%
get_hastimecode ? timecode_options : timecode_config
```

## Macros

| Verb           | Description  | Example        |
| -------------- | ------------ | -------------- |
| `macro_record` | Record macro | `macro_record` |
| `macro_play`   | Play macro   | `macro_play`   |

## Sandbox

| Verb          | Description          | Example       |
| ------------- | -------------------- | ------------- |
| `sandbox`     | Toggle sandbox mode  | `sandbox`     |
| `can_sandbox` | Check if can sandbox | `can_sandbox` |

## Text Queries

| Verb        | Description             | Example                                                       |
| ----------- | ----------------------- | ------------------------------------------------------------- |
| `get_text`  | Get formatted text      | `get_text 'You are listening to \`get loaded_song "title"\`'` |
| `stopwatch` | Stopwatch               | `stopwatch`                                                   |
| `stopwatch_reset` | Reset stopwatch     | `stopwatch_reset`                                             |
| `countdown` | Count down to date/time | `countdown '2025/01/01 00:00'`                                |

## Official Appendix Remainder

No compact entries currently remain. All official names tracked by the audit are present in functional sections above; sparse or hardware-specific entries remain marked for local testing in the audit.

Sources:

- `Official`: VDJScript verbs appendix

## Common Patterns

### Conditional Execution

```
condition ? action_if_true : action_if_false
```

### Backtick Queries

Use backticks to execute queries within actions:

```
set 'varname' `play`
param_equal `get_browsed_song 'type'` "audio"
```

### Time Units

- `ms` - milliseconds
- `bt` - beats
- `%` - percentage

### Deck Specification

Prefix action with deck number:

```
deck 1 play
deck 2 volume 50%
deck master get_level
```
