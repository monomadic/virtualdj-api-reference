# VirtualDJ Reference

Merged reference for this repo's VirtualDJ notes, examples, and preferred implementation patterns.

Last reviewed against live VirtualDJ documentation and forum sources on 2026-04-22.
Local repo links and example inventory audited on 2026-05-09.

For verb-by-verb API details, use [VDJScript Verbs](VDJScript%20Verbs.md).

## Scope

This document is the source-backed overview and policy layer above the older split reference pages, which are still being folded into a more reliable local reference set. It focuses on:

- Which methods to prefer
- Why those methods are preferable
- Where the working examples live in this repo
- Which notes come from official docs, official staff posts, or repo inference

Source labels used below:

- `Official`: current VirtualDJ manual or VDJPedia
- `Official forum`: post by VirtualDJ staff, Development Manager, CTO, or Support staff
- `Community`: forum moderators, non-staff forum users, Reddit posts, or other community examples
- `Published skin`: command or pattern observed in a working public skin
- `Local test`: behavior reproduced in VirtualDJ locally
- `Inference`: conclusion drawn from official docs plus this repo's build setup

## Quick Decisions

- Main deck filter or ColorFX:
  Prefer `filter_selectcolorfx` to choose the ColorFX and `filter` to drive it.
  Why: the current verbs list describes `filter` as the control that applies the selected ColorFX, with nothing applied at `50%`.
  Source: `Official`

- Extra ColorFX-style controls on custom knobs:
  Prefer `effect_colorfx <1-4>` with `effect_colorslider` or `colorfx_slider`.
  Why: the current verbs list exposes four custom ColorFX slots, and CTO guidance explains they exist for extra dedicated controls rather than replacing the main filter knob.
  Source: `Official`, `Official forum`

- Deterministic deck FX pads and buttons:
  Prefer `effect_select <slot>`, `effect_active <slot>`, and `effect_slider <slot> ...`.
  Why: the official effect verbs are slot-centric, and slot-based mappings avoid ambiguity that comes from global effect-name toggles. Name-based forms such as `effect_active 'Echo'` are valid VDJScript, but they are best treated as convenience shortcuts unless the mapping deliberately wants "whatever Echo instance exists."
  Source: `Official`

- Vocal/instrumental stem isolation:
  Prefer `stem_pad 'acapella' on` and `stem_pad 'instrumental' on` for button-style isolate pads.
  Why: official docs describe `stem_pad` as the stem-pad helper and local testing confirms the `on` argument forces these aggregate stem-pad states on in isolation. `only_stem <stem> on/off` also works, but it follows state-dependent button semantics and can require a second press from some starting states.
  Source: `Official`, `Local test`

- Page-aware sampler pads:
  Prefer `sampler_pad`, `sampler_color`, and `sampler_pad_page`.
  Why: `sampler_color` explicitly follows the visible sampler page, and the pads manual documents page cycling when a bank has more than eight samples.
  Source: `Official`

- Sampler drag-and-drop assignment inside pads:
  Prefer pad-page `drop="sampler_assign <absolute-slot>"` when you want a dragged file to populate a sampler slot from the Pads area.
  Why: `sampler_assign` is the official assignment verb, and the sampler manual documents dragging files onto unlocked sampler pads. The current skin button docs only document click-oriented handlers, while skin drag targets are handled with `<dropzone>` rather than a generic button drag state.
  Source: `Official`, `Inference`

- Absolute sampler slots:
  Prefer `sampler_play`, `sampler_stop`, `get_sample_name`, and `get_sample_color` when you do not want the action to follow the currently visible sampler page.
  Why: these verbs target fixed slots rather than the visible pad page.
  Source: `Official`

- Dynamic text color in skins:
  Prefer one `<text color="`...`">` over state-specific text color attributes when the color itself is dynamic.
  Why: the color docs distinguish between action-returning color values and literal colors, and Development Manager guidance recommends a single dynamic text color action.
  Source: `Official`, `Official forum`

- Dynamic button borders:
  Do not rely on dynamic `border=` colors.
  Why: CTO guidance says dynamic colors are not supported for button borders.
  Source: `Official forum`

- Time mode toggles:
  Prefer `display_time 'remain,elapsed'` with `get_time` instead of custom variables.
  Why: there is a dedicated verb for the job, and current forum guidance explicitly recommends using it instead of toggling your own skin vars for remain versus elapsed displays.
  Source: `Official`, `Official forum`

- Pitch reset pad status:
  For pad-page XML that colors a reset-pitch pad by distance from original BPM, use `get_pitch_value & param_bigger 125` / `param_smaller 75` with bare numeric thresholds, not `125%` / `75%`. Put the color thresholds in `color=""` and the blink/on/off state in `query=""`.
  Why: local testing showed percent literals made the red branch match incorrectly, while bare values match the `get_pitch_value` scale where original pitch is `100`.
  Source: `Official`, `Local test`

- Panel visibility and persistent panel switching:
  Prefer `<panel visibility="...">` for pure query-driven UI and `name=""`, `group=""`, `visible=""`, plus `skin_panelgroup` when you want manual switching that persists across sessions.
  Why: this is exactly how the panel SDK page distinguishes the two patterns.
  Source: `Official`

- Modular skins:
  Prefer build-time includes that flatten to one installed `skin.xml`.
  Why: the official SDK still describes skins as a flat package, while extra XML includes remain a forum wish rather than an official runtime feature. This repo already uses `xmllint --xinclude` to flatten modules before install.
  Source: `Official`, `Inference`

- Published skin findings:
  Preserve unfamiliar commands from working public skins in [Published Skin Findings](Published%20Skin%20Findings.md), then reconcile them against live official docs, forum context, and local tests.
  Why: local docs can lag behind VirtualDJ's live manual, and users need searchable explanations for aliases and skin idioms they encounter in real skins.
  Source: `Published skin`, `Official`, `Community`, `Inference`

## Real Examples In This Repo

Recommended runnable pad-page examples:

- [Reference - Slot FX.xml](../Pads/Reference%20-%20Slot%20FX.xml)
  Canonical slot-based audio FX pads.

- [Reference - ColorFX.xml](../Pads/Reference%20-%20ColorFX.xml)
  Canonical filter and ColorFX selection patterns using the current verbs.

- [Reference - Page Aware Sampler.xml](../Pads/Reference%20-%20Page%20Aware%20Sampler.xml)
  Page-aware sampler labels, colors, and actions.

- [Reference - Sparse Helper Tests.xml](../Pads/Reference%20-%20Sparse%20Helper%20Tests.xml)
  Manual-test harness for sparse official helpers such as `connect`, `system`, `open_stem_creator`, `karaoke_venue_name`, and `dualdeckmode_decks`.

Additional pad pages currently present in `Pads/`:

- [32 Samples.xml](../Pads/32%20Samples.xml)
  Four-page 32-slot sampler layout using an internal `sam_page` variable.

- [AUTO CUES.xml](../Pads/AUTO%20CUES.xml)
  Remix cue page with cue-name-driven pad labels and colors.

- [COLOR FX.xml](../Pads/COLOR%20FX.xml)
  ColorFX selection with stems context; demonstrates the same `filter_selectcolorfx` pattern as Reference - ColorFX.

- [CUE.xml](../Pads/CUE.xml)
  Hotcue page using `cue_display`, `has_cue`, and cue-color feedback.

- [CUE 16.xml](../Pads/CUE%2016.xml)
  Sixteen-pad hotcue page using `cue_display` and `cue_color`.

- [CUE SCAN.xml](../Pads/CUE%20SCAN.xml)
  Cue-name scanner for sections such as intro, build, cut, and drop.

- [PLAY 16.xml](../Pads/PLAY%2016.xml)
  Sixteen-pad performance transport/stems page.

- [PUSH FX.xml](../Pads/PUSH%20FX.xml)
  Momentary `padfx` performance page with explicit stem-targeted variants.

- [SAMPLER.xml](../Pads/SAMPLER.xml)
  Sixteen-pad page-aware sampler page with explicit drop-slot mapping across sampler pages.

- [SAMPLER SIMPLE.xml](../Pads/SAMPLER%20SIMPLE.xml)
  Simple fixed-slot sampler page demonstrating `drop="sampler_assign <slot>"`.

- [TRANSPORT.xml](../Pads/TRANSPORT.xml)
  Beat/bar navigation and transport utility pad page.

Skin examples:

- [ModularSkeleton README](../Skins/ModularSkeleton/README.md)
  Build-time XInclude workflow, `<define class>` system, and named color patterns.

- [ModularSkeleton built skin](../Skins/ModularSkeleton/build/skin.xml)
  Flat installed output showing real `<define>`, `<panel>`, `<deck>`, and `<visual>` usage.

- [GraveRaver Build Demo](../Skins/GraveRaver/README.md)
  Minimal XInclude source tree that exists only to demonstrate the build system. Do not treat it as a polished skin reference.

## Skin SDK

### Root Skin Structure

The official SDK still describes a skin package as a `.zip` containing:

- `image_name.png`
- `skincode_name.xml`
- `preview_image.png` optionally
- optional window image files

That makes two things worth keeping straight:

- VirtualDJ expects a flat installed skin package.
- Modularity is a build concern, not a runtime skin feature.

Minimal root pattern:

```xml
<skin
  name="My Skin"
  version="8"
  width="1600"
  height="900"
  image="skin.png"
  preview="preview.png"
  author="Your Name"
  breakline="900"
  breakline2="900">
  ...
</skin>
```

Conditional deck-count pattern:

```xml
<nbdecks value="2" condition="var_equal '@$4decks' 0"/>
<nbdecks value="4" condition="var_not_equal '@$4decks' 0"/>
```

This is useful when a skin has a user-facing two-deck/four-deck mode. If the controlling variable changes from a button or menu, pair that state change with `load_skin` so VirtualDJ reparses the structural XML.

Source: `Official`, `Local test`, `Inference`

### Containers

The core containers worth using first are:

- `<deck>` for deck-scoped UI
- `<panel>` for grouped visibility and panel persistence
- `<group>` for shared positioning and organization
- `<stack>` when only the last visible items should occupy shared slots
- `<define>` for reusable classes and placeholders

Preferred pattern:

- Nest elements inside containers instead of repeating `deck=""` and `panel=""` everywhere.
- Use `<define>` early for repeated button, text, and frame shapes.

Why:

- The SDK explicitly supports nested containers.
- The common element properties page says nesting is preferred over repeating `panel=""`.

Source: `Official`, `Local test`, `Inference`

### Defines and Placeholders

Reusable class defines can use named placeholders:

```xml
<define class="LABELED_BUTTON" placeholders="*label,width=160,color=textoff">
  <size width="[WIDTH]" height="24"/>
  <text text="[LABEL]" color="[COLOR]"/>
</define>

<button class="labeled_button" label="SYNC" width="220" action="sync"/>
```

Practical conventions:

- use uppercase class names in `<define>` and lower-case class calls for readability
- keep placeholder tokens uppercase inside brackets
- use `*name` for required placeholders and `name=value` for defaults
- use conditional defines when one class needs different implementations per skin mode or color scheme

Example conditional define:

```xml
<define class="PADBUTTON" placeholders="*source" condition="var_equal '@$color_scheme' 4">
  ...
</define>
```

Source: `Local test`, `Inference`

### Panels

There are two useful panel modes:

- Query-driven:

```xml
<panel visibility="loop">
  ...
</panel>
```

- Persistent manual switching:

```xml
<panel group="rack" name="fx" visible="yes">
  ...
</panel>
```

Driven with:

```vdjscript
skin_panelgroup 'rack' 'fx'
skin_panelgroup 'rack' +1
skin_panel 'my_panel' on
```

Use query-driven panels when state should follow live deck conditions.
Use named groups when the user is choosing a mode and you want it remembered.

Source: `Official`

### Conditional Structure

Use `visibility=""` for live display state and `condition=""` for structural selection.

```xml
<panel class="main_decks" visibility="not browser_zoom"/>
<panel class="browser_zoom_decks" visibility="browser_zoom"/>

<panel class="pro_2decks" condition="var_equal '@$layout_4deck' 0"/>
<panel class="pro_4decks" condition="var_equal '@$layout_4deck' 1"/>
```

Useful rule of thumb:

- `visibility=""` can follow frequently changing state without a skin reload.
- `condition=""` is better for mutually exclusive layout branches, conditional define/color variants, and conditional `<nbdecks>` entries. When user actions change those controlling variables, reload the skin.

Source: `Local test`, `Inference`

### Buttons, State, and Query

The current button SDK page is explicit: `query=""` enables the `<on>` graphics when true.

That means:

- Use `query=""` to drive the button's on-state.
- Do not assume `query=""` selects `<selected>` graphics.
- If the element is informational only, `action="nothing"` is a valid way to make it non-destructive.

Example:

```xml
<button action="nothing" query="play">
  <off color="#1C1F24" border="white" border_size="1" radius="10"/>
  <on color="#1C1F24" border="orange" border_size="1" radius="10"/>
  <text text="PLAYING" color="`masterdeck ? color 'orange' : color 'white'`"/>
</button>
```

Source: `Official`, `Official forum`

### Colors and Visuals

The safest dynamic-color rules are:

- `source=` on `<visual type="color">` expects an action that returns a color.
- `color=` expects a color value, so a script action must be wrapped in backticks.

Examples:

```xml
<visual type="color" source="pad_color 1">
  <pos x="0" y="0"/>
  <size width="24" height="2"/>
</visual>
```

```xml
<text color="`get_key_color`" action="get_key"/>
```

Preferred methods:

- Use `<visual type="color">` for colored underlines, fills, and status bars.
- Use a single dynamic `<text color="`...`">` when only the text color changes.

Avoid:

- Dynamic `border=` colors on button vector states. CTO guidance says this is not supported.

Source: `Official`, `Official forum`

### `<visual type="...">` — Full Type Reference

The `type=""` attribute on `<visual>` determines what the element renders and how its `source=""` is interpreted.

| Type | What it renders | `source=` expects | Notes | Source |
| --- | --- | --- | --- | --- |
| `linear` | Progressively reveals `<on>` over `<off>` graphic | Numeric action (`volume`, `position`, `get_level`, etc.) | Use `orientation="vertical"` / `"horizontal"` and `direction="up"` / `"down"` / `"left"` / `"right"`. Add `granularity="N"` for a segmented VU meter. | `Official` |
| `onoff` | Shows `<on>` or `<off>` graphic based on a threshold | Numeric action; `≥ 2048` triggers `<on>` | Use for beat flash, status indicators. | `Official` |
| `color` | Solid filled rectangle in the color returned by source | Action returning a color value (`cue_color 1`, `pad_color 1`, `get_key_color`, etc.) | No `<on>` / `<off>` children needed. Width/height set the fill area. | `Official` |
| `waveform` | Deck waveform display | Implicit (always the current deck's waveform) | Must be inside a `<deck>` container. `source=""` is not used. | `Official` |
| `spectrum` | Frequency spectrum analyzer | Implicit (current deck's audio) | Displays frequency bands as a bar graph. | `Official` |
| `cover` | Album art for the loaded track | Implicit (loaded track cover art) | Scales to `<size>`. Use `<off>` to show a placeholder when no art is available. | `Official` |
| `custom` | Raw graphic tile from skin image | Numeric action | Low-level; use when none of the above types fit. | `Official` |

#### `type="linear"` — level meter

```xml
<visual source="get_level" type="linear" orientation="vertical" direction="up">
  <pos x="680" y="220"/>
  <size width="16" height="560"/>
  <off color="#23303C"/>
  <on  color="accent_1"/>
</visual>
```

When using named colors (`<define color="...">`) instead of a skin image, omit `x=""` / `y=""` from `<off>` and `<on>` and use the `color=""` attribute instead.

#### `type="color"` — cue point color stripe

```xml
<visual type="color" source="cue_color 1">
  <pos x="0" y="0"/>
  <size width="4" height="48"/>
</visual>
```

#### `type="waveform"` — deck waveform

```xml
<deck deck="1">
  <visual type="waveform">
    <pos x="0" y="0"/>
    <size width="800" height="80"/>
  </visual>
</deck>
```

#### `type="cover"` — album art

```xml
<visual type="cover">
  <pos x="24" y="24"/>
  <size width="128" height="128"/>
  <off color="#1A2129"/>
</visual>
```

Source: `Official`

### Positioning

The positioning SDK page allows both nested `<pos>` and inline `x="" y="" width="" height=""` forms.
For larger skins, use `<pos>` and `<size>` consistently because:

- it is easier to scan
- it matches this repo's style
- it makes class placeholders easier to reason about

Source: `Official`

### Custom Browser Layouts

Use `<browser>` when the default browser arrangement is enough.
Use the smaller browser elements when the skin needs custom placement:

- `<folderlist>` plus `<browsertoolbartree>` for the folder tree and its vertical toolbar
- `<fileview>` for the full songs area
- `<browsertoolbar>`, `<coverflow>`, and `<filelist>` when the songs area needs custom composition
- `<sideview>` or `filelist source="sideview"` for sideview layouts
- `<filelist source="automix">`, `source="karaoke"`, `source="sidelist"`, or `source="sampler"` for pinned sideview lists
- `<browserinfo>` for selected-track info and prelisten
- `<pluginzone>` for docked effect GUIs
- `<sampler>` for sampler trigger-pad view

When composing these pieces inside `<split>` panels, use `attachX`, `attachY`, `resizeX`, and `resizeY` for anchoring/resizing. Use `grid="yes"` only when a list should always stay in grid view instead of following the user's current Grid/List selection.

If the skin docks effect GUIs, put `<pluginzone>` in a split named `effects` so VirtualDJ can resize that area automatically when a plugin GUI appears.

Browser zoom / "mini" layouts are usually not separate VirtualDJ layout types. They are skin branches driven by the `browser_zoom` state, sometimes combined with `browser_isactive` for automatic browser-focused behavior:

```xml
<panel class="main_decks" visibility="not browser_zoom"/>
<panel class="browser_zoom_decks" visibility="browser_zoom ? true : browser_isactive ? true : false"/>
```

The `<browser showzoom="yes">` attribute shows VirtualDJ's built-in zoom control in the browser toolbar; custom buttons can also use `action="browser_zoom"` and `query="browser_zoom"`.

Source: `Official`, `Local test`, `Inference`

## VDJScript Patterns

### Core Syntax Worth Reaching For

- `action1 & action2`
  Sequential actions

- `condition ? when_true : when_false`
  Branching

- `query1 && query2`
  Query-only conjunction. Official VDJScript docs describe this as the way to make a chained query return true only when both commands are true.

- Backticks around action-returning values
  Use when a value consumer needs the result of another action

- `param_*`
  Use for live parameter comparisons and transforms

- `var_*`
  Use when you truly need stored state

Examples:

```vdjscript
param_equal `get_browsed_song 'type'` 'audio' ? load : nothing
```

```vdjscript
down ? filter 75% : filter 50%
```

```vdjscript
repeat_start 'fxpulse' 1bt & effect_active 1
```

Source: `Official`

### Prefer Built-ins Over Skin Vars

If VirtualDJ already has a dedicated action for a behavior, prefer that over inventing a variable.

Good examples:

- `display_time 'remain,elapsed'` instead of a custom elapsed/remain toggle var
- `skin_panelgroup` instead of a custom var that emulates grouped panels
- `setting 'optionName' value` when you are intentionally changing a setting

Reason:

- less state drift
- fewer hidden dependencies
- behavior lines up better with controllers and the default UI

Source: `Official`, `Official forum`

### Skin Vars For Structural State

Prefer built-in state when VirtualDJ already has it. When the skin truly needs its own layout state, use custom variables such as `@$layout_4deck`, `@$skin_mode`, or `@$show_zoom_racks` and keep their purpose narrow.

```vdjscript
set '@$layout_4deck' 1 & load_skin
var_equal '@$layout_4deck' 1 ? action1 : action2
```

Use `load_skin` when the variable controls structural XML, such as conditional `<nbdecks>`, conditional defines, or mutually exclusive layout branches. Avoid reloading for simple live visibility toggles unless the skin actually needs to rebuild.

Source: `Local test`, `Inference`

### Write Queries With an Explicit Else

Prefer:

```vdjscript
effect_active 1 ? blink 500ms : off
```

Over:

```vdjscript
effect_active 1 ? blink 500ms
```

Why:

- explicit `off` avoids empty or ambiguous UI states
- it is easier to debug later

Source: `Inference`

### Pitch Reset Pad With Color and Blink

Use this pad-page XML pattern when a reset-pitch pad should be green near original tempo, yellow when moderately shifted, and blinking red when far from original tempo:

```xml
<pad13 name="RESET PITCH `get_text '%Ppitch%'`" autodim="false" color="loaded ? get_pitch_value &amp; param_bigger 125 ? color 'red' : get_pitch_value &amp; param_smaller 75 ? color 'red' : get_pitch_value &amp; param_bigger 105 ? color 'yellow' : get_pitch_value &amp; param_smaller 95 ? color 'yellow' : color 'green' : color 'black'" query="loaded ? get_pitch_value &amp; param_bigger 125 ? blink 500ms : get_pitch_value &amp; param_smaller 75 ? blink 500ms : on : off">pitch_reset 4bt</pad13>
```

Rules from the working version:

- `get_pitch_value` is centered on `100` for the original track BPM.
- Use bare thresholds: `95`, `105`, `75`, `125`.
- In XML, write chained VDJScript `&` as `&amp;`.
- Put color selection in the pad `color=""` attribute.
- Put blinking only in `query=""`: `... ? blink 500ms : on : off`.

Source: `Official`, `Local test`

## Effects

### Deck FX Slots

The official verbs and the current deck FX UI are slot-based.

Preferred slot workflow:

1. Select the effect into a slot
2. Activate the slot
3. Move the slot's sliders or buttons

Example:

```vdjscript
effect_select 1 'Echo' &
effect_slider 1 1 75% &
effect_slider 1 2 1bt &
effect_active 1 on
```

Why this is the safest reference pattern:

- it mirrors the actual deck FX rack model
- it behaves predictably across skins and controllers
- it avoids name-based ambiguity when several effects are loaded
- it lets a pad own both the effect choice and the parameter preset

Use [Reference - Slot FX.xml](../Pads/Reference%20-%20Slot%20FX.xml) for a working repo example.

Source: `Official`

#### Slot Pads vs Name-Based Pads

`effect_active 'Echo'` is legal and useful for quick personal mappings. It asks VirtualDJ to toggle an effect by name, wherever that effect is currently represented.

For documented pad pages, prefer one of these slot-based designs:

- Dedicated slot pads:
  A pad owns a specific slot, for example Echo on slot 1 and Reverb on slot 2. This works well when the page should allow several effects to remain active at once.

- Shared slot preset pads:
  Many pads program the same slot, usually slot 1. Pressing Echo Out replaces whatever is in that slot with Echo Out, sets known parameters, and activates it. This works well for performance pages where the pad row is an effect picker rather than a multi-effect rack.

Avoid mixing the two designs without documenting it. A pad labeled `ECHO` with only `query="effect_active 1"` can blink when slot 1 is active with a different effect. If the pad state is meant to mean "slot 1 contains Echo and is active," query `get_effect_name <slot>` first, then nest the slot active check:

```vdjscript
get_effect_name 1 & param_lowercase & param_equal 'echo' ?
  effect_active 1 ? blink 500ms : off :
  off
```

To turn the effect off, use the slot activation verb: `effect_active 1 off`. Reference pages can expose that as a dedicated `S1 OFF`/`KILL` pad, or make the preset pad itself toggle only when the same effect is already loaded and active:

```vdjscript
get_effect_name 1 & param_lowercase & param_equal 'echo' ?
  effect_active 1 ?
    effect_active 1 off :
    effect_slider 1 1 75% & effect_slider 1 2 50% & effect_active 1 on :
  effect_select 1 'Echo' & effect_slider 1 1 75% & effect_slider 1 2 50% & effect_active 1 on
```

Do not use bare `effect_select 1` as that state check. In pad actions, it can open the selector popup. Use `effect_select 1 'Echo'` only when you are deliberately loading a named effect into the slot.

Official VDJScript documents `&&` for query chains, for example "true only when both commands are true." That is different from using `&&` inside a complex pad action body that also branches and performs load/set/on actions. Use nested conditionals for same-pad toggle actions, and reserve `&&` for simple query expressions you have verified in the target surface.

Source: `Official`, `Inference`

### Filter and ColorFX

Current official behavior:

- `filter` applies the selected ColorFX to the sound
- nothing is applied at `50%`
- more effect is applied the farther the control moves from center
- `filter_selectcolorfx` selects which ColorFX the filter knob controls
- `filter_label` returns the label under the filter knob
- `filter_resonance` changes filter resonance

Preferred method for the main deck filter:

```vdjscript
filter_selectcolorfx 'Echo' &
filter 75%
```

Preferred method for a dedicated select-only button:

```vdjscript
filter_selectcolorfx 'Flanger'
```

Preferred method for an extra custom ColorFX control:

```vdjscript
effect_colorfx 1 'Echo'
effect_colorslider 1
```

Notes:

- `effect_colorslider` is the center-off ColorFX-style slider action.
- `effect_colorfx` exposes up to four extra custom ColorFX slots.
- CTO guidance says that the dedicated `colorfx` slot only exposes approved ColorFX-compatible effects, while extra slots are more flexible.

Use [Reference - ColorFX.xml](../Pads/Reference%20-%20ColorFX.xml) for a working repo example.

Source: `Official`, `Official forum`

### Which ColorFX Method To Use

- If you are emulating the standard deck filter knob:
  use `filter_selectcolorfx` + `filter`

- If you are building extra ColorFX-like controls that should not steal the deck's main filter:
  use `effect_colorfx <1-4>` + `effect_colorslider`

- If you are building a deterministic pad page for normal audio effects:
  use regular slot FX instead of ColorFX

Source: `Official`, `Official forum`

### Stems FX

The official verbs list includes `effect_stems`, `effect_arm_stem`, and `effect_stems_color`.

Use `effect_stems` when you intentionally want FX targeting to follow selected stems.

Caution:

- Older official forum posts from 2021 reported inconsistencies between regular slot FX and special slots such as `colorfx`.
- Treat any ColorFX-plus-stems behavior as build-sensitive and test it on the exact VirtualDJ build you use.

That caution is intentionally dated because the forum guidance is older than the current manual.

Source: `Official`, `Official forum`

### Native Effects

The current native effects appendix is the authoritative list for built-in effects, video effects, and transitions.

High-frequency audio effects to design around first:

- Echo
- Echo Out
- Reverb
- Beat Grid
- Flanger
- Filter
- Noise
- Phaser
- Loop Roll
- VinylBrake
- Stutter Out

For the current full list, use the official appendix instead of hard-coding old plugin menus into your docs.

Source: `Official`

## Sampler and Pads

### Default Page Behavior

The current pads manual says:

- the Sampler page shows the first eight pads of the active bank
- Parameter 2 cycles samples in the bank when there are more than eight
- right-click or shift stops a triggered sample

Source: `Official`

### Page-Aware vs Absolute Sampler Methods

Use page-aware methods when the UI should follow the visible `1-8`, `9-16`, `17-24`, and later pages:

- `sampler_pad`
- `sampler_color`
- `sampler_pad_page`
- `sampler_pad_volume`

Use absolute-slot methods when the UI should always target the same underlying sample slots:

- `sampler_play`
- `sampler_stop`
- `sampler_loaded`
- `get_sample_name`
- `get_sample_color`
- `sampler_volume`

Practical rule:

- visible pad UI: page-aware
- fixed utility controls: absolute

Use [SAMPLER READ ONLY.xml](../Pads/SAMPLER%20READ%20ONLY.xml) for the current confirmed read-only multi-page pattern. [Reference - Page Aware Sampler.xml](../Pads/Reference%20-%20Page%20Aware%20Sampler.xml) is retained as a legacy page-aware sampler example, but it uses the now-unreliable `sampler_loaded <n> 'auto'` guard.

Source: `Official`, `Local test`, `Inference`

### `sampler_loaded` and `auto`

The current verbs page documents `sampler_loaded <n>` as a fixed slot query.
VirtualDJ forum examples and older local examples use `sampler_loaded <n> 'auto'` beside `sampler_pad <n> 'auto'`. The installed/public `Loop Recorder.xml` pad page uses the unquoted form `sampler_loaded <n> auto`. Neither form is documented as official behavior.

Local diagnostic testing showed this pattern is not reliable for page-aware empty-slot checks:

- Test page: [Reference - Sampler Loaded Test.xml](../Pads/Reference%20-%20Sampler%20Loaded%20Test.xml)
- Build: VirtualDJ 8.5.9307 / 18.0.9336
- Date: 2026-05-21
- Setup: sampler bank page 2 (`9-16`), slot 8 loaded, slot 16 empty
- Result: `sampler_loaded 8 'auto'` and `sampler_loaded 8 auto` returned true while `sampler_loaded 16` and `sampler_loaded 16 auto` returned false

Use `sampler_loaded` with the absolute slot behind the visible pad. Page 2 pad 8 should be guarded by `sampler_loaded 16`; keep `sampler_pad 8` for the visible page-aware action/label. Quoting `auto` does not change this behavior in the tested build.

Source: `Official`, `Community`, `Published pad page`, `Local test`

### Read-Only Multi-Page Sampler Pages

For sampler pages that must never record into empty slots, use `sampler_pad_page` to branch by the visible text range and then guard with the absolute slot behind the pad:

- `sampler_pad_page & param_equal "1 to 8"` with pad 8 checks `sampler_loaded 8`
- `sampler_pad_page & param_equal "9 to 16"` with pad 8 checks `sampler_loaded 16`
- in a 16-pad layout, pad 16 on `"9 to 16"` checks `sampler_loaded 24`

Use `sampler_pad <pad>` for loaded actions and `nothing` for empty actions. Do not include `sampler_rec`, `sampler_assign`, or `drop=` on a read-only page. For intentionally blank names, return `get_text ' '` rather than an empty string; local testing showed empty strings can fall back to visible slot numbers on later pages.

Working example: [SAMPLER READ ONLY.xml](../Pads/SAMPLER%20READ%20ONLY.xml)

Source: `Local test`, `Inference`

### Empty Sampler Pads and Shifted Colors

When a sampler pad slot is empty, nullify the action with an explicit false branch instead of leaving the conditional incomplete:

```xml
<pad10 name="`sampler_loaded 10 ? sampler_pad 10 : ''`" color="sampler_loaded 10 ? sampler_color 10 : dim" query="sampler_loaded 10 ? sampler_play 10 ? blink 1bt : on : off">sampler_loaded 10 ? sampler_pad 10 : nothing</pad10>
```

If the page defines `shift_pad<n>` entries, give the shifted pads their own `color=""` expression. Skin frameworks that render shifted pad state may read the shifted pad color separately; without a shifted color, empty or shifted sampler pads can fall back to the skin/default button color instead of matching the normal pad.

```xml
<shift_pad10 name="`sampler_loaded 10 ? sampler_pad 10 : ''`" color="sampler_loaded 10 ? sampler_color 10 : dim">sampler_loaded 10 ? sampler_edit 10 : nothing</shift_pad10>
```

Source: `Local test`, `Inference`

### Sampler Options That Matter

Current official options worth knowing:

- `samplerSpanAcrossDecks`
  When set to `yes`, a 16-sample bank makes deck 2 automatically show `9-16`

- `samplerIndependentDeckBanks`
  Each deck and master can have their own sample bank

- `displayTime`
  Selects elapsed, remain, or total display mode

Source: `Official`

### 2025 Sampler Note

A forum thread published on 2025-09-23 reported inconsistent sampler sync behavior on controller pads in VirtualDJ 2025 builds, especially when the triggering deck was not the master deck. The same thread shows:

- a workaround suggested by CTO Adion on 2025-09-26: try `deck master sampler_pad <n>`
- the original poster later reporting on 2025-10-04 that support resolved the issue in an Early Access update

Practical takeaway:

- treat master-deck sampler workarounds as build-specific
- do not document them as timeless behavior

Source: `Official forum`

## Browser Filter Syntax

Useful filter building blocks:

- comparison operators
- logical operators
- date and time filters
- tag filters
- mixing and library filters

Typical patterns:

```text
genre contains house
```

```text
bpm > 120 and bpm < 130
```

```text
year >= 2020
```

```text
type = video
```

The official appendix remains the best exhaustive source here, so keep repo docs focused on patterns you actually use instead of copying the whole appendix into local markdown.

Source: `Official`

## Options Worth Knowing

High-value official options for skin and pad authors:

- `filterDefaultResonance`
  Sets the amount of resonance applied by the filter

- `fxProcessing`
  Chooses whether effects are processed pre-fader or post-fader

- `resetFXOnLoad`
  Stops all effects when a new song loads

- `globalQuantize`
  Sets beat, measure, or quarter quantization

- `smartLoop`
  Auto-adjusts loop points for seamless loops

- `quantizeSetCue`
  Auto-aligns newly set cues according to quantization

Script note:

```vdjscript
setting 'filterDefaultResonance' 75%
setting 'fxProcessing' 'post-fader'
```

Source: `Official`

## Modular Skin Workflow

### What VirtualDJ Officially Describes

The SDK still documents a flat skin package:

- `skin.xml`
- image file
- optional preview file

It does not document runtime support for loading arbitrary extra XML modules from the main skin file.

Source: `Official`

### What This Repo Should Prefer

Use build-time modularity:

- keep source XML split into `defs/` and `panels/`
- compose with XInclude or another XML preprocessor locally
- build one flattened `skin.xml` before install

This is the pattern demonstrated by [ModularSkeleton](../Skins/ModularSkeleton/README.md). Its flattened `build/skin.xml` output is the installed-form reference.

Why:

- easier maintenance
- reusable classes and panel slices
- installed output still matches the official flat package model

Source: `Inference`

### Skeleton In This Repo

Use [ModularSkeleton](../Skins/ModularSkeleton/README.md) as the starting point.

It demonstrates:

- build-time XInclude flattening with `xmllint --xinclude`
- named color defines and reusable class defines with placeholders
- `<panel>`, `<deck>`, and `<visual>` composition patterns
- a flat `build/skin.xml` output ready for installation

## Sources

Official docs:

- [VirtualDJ Skin SDK](https://www.virtualdj.com/wiki/Skin_SDK.html)
- [Custom Browser](https://virtualdj.com/wiki/custombrowser.html)
- [Skin Button](https://virtualdj.com/wiki/Skin-Button.html)
- [Skin SDK Dropzone](https://www.virtualdj.com/wiki/Skin%20SDK%20Dropzone.html)
- [Skin Panel](https://www.virtualdj.com/wiki/Skin%20SDK%20Panel.html)
- [Skin Default Colors](https://virtualdj.com/wiki/Skin%20Default%20Colors.html)
- [Skin SDK Visual](https://virtualdj.com/wiki/skinsdkvisual.html)
- [List of VDJScript verbs](https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html)
- [List of Options](https://www.virtualdj.com/manuals/virtualdj/appendix/optionslist/)
- [List of Native Effects](https://www.virtualdj.com/manuals/virtualdj/appendix/nativeeffects/)
- [Pads manual](https://www.virtualdj.com/manuals/virtualdj/interface/decks/decksadvanced/pads.html)
- [Sampler manual](https://www.virtualdj.com/manuals/virtualdj/interface/browser/sideview/sampler.html)

Official forum guidance cited for method choices:

- [Border Color using placeholder](https://virtualdj.com/forums/242871/VirtualDJ_Skins/Border_Color_using_placeholder.html)
- [effect_colorfx & effect_stems_color ?](https://www.virtualdj.com/forums/241078/VirtualDJ_Technical_Support/effect_colorfx___effect_stems_color__.html)
- [Default filter and color fx filter](https://virtualdj.com/forums/252675/VirtualDJ_Technical_Support/Default_filter_and_color_fx_filter.html)
- [Skin text action; visibility or visual?](https://www.virtualdj.com/forums/267953/VirtualDJ_Skins/Skin_text_action%3B_visibility_or_visual%3F.html)
- [Virtual Dj 2025 Sampler Sync](https://www.virtualdj.com/forums/265522/VirtualDJ_Technical_Support/Virtual_Dj_2025_Sampler_Sync.html)
- [No longer possible to access 16 samples from controllers with 8 x 2 pads?](https://www.virtualdj.com/forums/261416/VirtualDJ_Technical_Support/No_longer_possible_to_access_16_samples_from_controllers_with_8_x_2_pads_.html)
- [Aditional xml for Skins](https://virtualdj.com/forums/248589/Wishes_and_new_features/Aditional_xml_for_Skins.html)

Repo examples:

- [32 Samples.xml](../Pads/32%20Samples.xml)
- [AUTO CUES.xml](../Pads/AUTO%20CUES.xml)
- [COLOR FX.xml](../Pads/COLOR%20FX.xml)
- [CUE.xml](../Pads/CUE.xml)
- [CUE 16.xml](../Pads/CUE%2016.xml)
- [CUE SCAN.xml](../Pads/CUE%20SCAN.xml)
- [PLAY 16.xml](../Pads/PLAY%2016.xml)
- [PUSH FX.xml](../Pads/PUSH%20FX.xml)
- [Reference - Slot FX.xml](../Pads/Reference%20-%20Slot%20FX.xml)
- [Reference - ColorFX.xml](../Pads/Reference%20-%20ColorFX.xml)
- [Reference - Page Aware Sampler.xml](../Pads/Reference%20-%20Page%20Aware%20Sampler.xml)
- [SAMPLER.xml](../Pads/SAMPLER.xml)
- [SAMPLER SIMPLE.xml](../Pads/SAMPLER%20SIMPLE.xml)
- [TRANSPORT.xml](../Pads/TRANSPORT.xml)
- [ModularSkeleton README](../Skins/ModularSkeleton/README.md)
- [ModularSkeleton built skin](../Skins/ModularSkeleton/build/skin.xml)
- [GraveRaver Build Demo](../Skins/GraveRaver/README.md)
