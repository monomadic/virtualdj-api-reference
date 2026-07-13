# VirtualDJ Skin SDK Reference

> **Reliability note**: This file is raw reference material that has not been normalized to the same standard as `VirtualDJ Reference.md`. It does not use source labels and some entries may be incomplete or use element names that differ from the current official SDK. Use `VirtualDJ Reference.md` and `VDJScript Verbs.md` as the authoritative layer. This file is useful for broad scanning but verify specific details against the live SDK docs.

Broad reference for VirtualDJ 8+ skin elements and attributes.

Local-test notes promoted from skin project experiments live in
[Skin Runtime Findings](Skin%20Runtime%20Findings.md). This file folds those
findings into the broader SDK reference when they become stable enough to use as
guidance.

## Overview

A VirtualDJ skin is a `.zip` file containing:
- `skin.xml` - The XML file defining the skin structure
- `skin.png` - The graphics file (or same name as XML)
- `window_images.png` - Optional graphics for window elements

## The `<skin>` Element

The root element of every skin with these attributes:

| Attribute | Description | Values |
|-----------|-------------|--------|
| `name` | Skin name (can differ from filename) | text |
| `version` | SDK version | 8 for VirtualDJ 8+ |
| `width` | Skin width in pixels | number |
| `height` | Skin height in pixels | number |
| `nbdecks` | Number of decks | 2, 4, etc (optional) |
| `comment` | Extra information | text (optional) |
| `author` | Author name | text (optional) |
| `image` | Graphics filename | filename (optional if matches XML name) |
| `preview` | Preview screenshot | filename (optional) |

Built-in plugin UI XML is a narrower surface than a desktop or Remote skin. The shipped BeatGrid plugin UI at `examples/Skins/Built-In/Plugin-UI/AFX_beatgrid.xml` begins with `?<skin width="341" height="139" version="8">`, has no `name`, `image`, `preview`, `nbdecks`, `<deck>`, `<panel>`, browser, or `<oninit>` scaffolding, and pairs with `AFX_BeatGrid.png` beside it rather than declaring an `image=""` attribute. It is useful for studying small plugin-owned GUI layout and control idioms, but do not use it as the package/root template for full skins.

Source: `Built-in skin` (`examples/Skins/Built-In/Plugin-UI/AFX_beatgrid.xml`), `Inference`

### Runtime Deck Count

In addition to the root `nbdecks` attribute, working skins can set the exposed deck count with child `<nbdecks>` elements. These can be conditional, which lets a skin switch between two-deck and four-deck structures from stored skin state:

```xml
<nbdecks value="2" condition="var_equal '@$4decks' 0"/>
<nbdecks value="4" condition="var_not_equal '@$4decks' 0"/>
```

When a button or menu changes a variable that controls structural XML like this, pair the state change with `load_skin` so VirtualDJ reparses the skin:

```vdjscript
set '@$4decks' 1 & load_skin
```

### Breaklines

Static skin breaklines can be declared as root `<skin>` attributes:

```xml
<skin ... breakline="1000" breakline2="1000">
```

Layout-dependent breaklines can be declared as top-level `<breaklines>` child
elements. This is useful when the loaded skin has mutually exclusive structural
layouts that need different vertical stretch regions:

```xml
<breaklines breakline1="675" breakline2="1000" condition="var_equal '@$skin_mode' 0"/>
<breaklines breakline1="980" breakline2="1070" condition="var_equal '@$skin_mode' 1"/>
```

When the controlling variable changes from a button or menu, pair that state
change with `load_skin` so VirtualDJ reparses the structural skin state.

Source: `Official`, `Official forum`, `Community`, `Local test`

## Skin Children Elements

Available elements as children of `<skin>`:

### Containers
- `<deck>` - Groups elements for a specific deck
- `<panel>` - Container for show/hide element groups
- `<group>` - Generic container for organizing elements
- `<stack>` - Container with fadein/fadeout effects

### Interactive Elements
- `<button>` - Clickable button
- `<slider>` - Movable slider control (rotary knobs are `<slider orientation="round">`, not a separate element)
- `<menu>` - Clickable custom menu object
- `<dropzone>` - Drag-and-drop target area for loading tracks

> `<icon>` is not a direct `<skin>` child: it is an overlay child of `<button>`,
> `<define>`, and `<menu>`. See the `<icon>` section under Element Details.

> There is no `<switch>` or `<knob>` element. Neither name appears in the
> official Skin SDK element list or in any built-in skin. Multi-state toggles
> are buttons driven by `query=""`/`action=""`; knobs are round sliders.
> Source: `Official` (Skin SDK element list), `Built-in skin` (zero uses).

### Display Elements
- `<visual>` - Static/dynamic graphics display
- `<textzone>` - Text display area
- `<video>` - Video output display
- `<led>` - LED indicator
- `<equalizer>` - Spectrum analyzer (`Official` element; not used by any built-in skin, which draw spectra with `<visual>` instead)
- `<cover>` - Album-art display for a deck, the browser, automix, or karaoke

> The waveform display family — `<rhythmzone>`, `<scratchwave>`, `<wave>`,
> `<songpos>`, `<blockwave>`, `<beattunnel>`, `<scratch>` — is covered
> separately in [Skin Waveforms](Skin%20Waveforms.md).

### Window Elements
- `<window>` - Popup/separate window
- `<browser>` - File browser interface

### Browser Elements
- `<folderlist>` - Browser folder tree without the vertical toolbar
- `<browsertoolbartree>` - Vertical toolbar for the folder tree
- `<fileview>` - Combined song list area with list, coverflow, and search/edit toolbar
- `<browsertoolbar>` - Horizontal browser search/edit toolbar
- `<coverflow>` - Coverflow browser list
- `<filelist>` - Song or sideview list without coverflow/search controls
- `<sideview>` - Full sideview area
- `<browserinfo>` - Selected-track info and prelisten area
- `<pluginzone>` - Docked effect GUI area
- `<sampler>` - Sampler trigger-pad view
- `<prelisten>` - Standalone prelisten player (also a `<browser><colors>` styling child)

### Simple Shapes
- `<square>` - Rectangle/rounded rectangle
- `<circle>` - Circle/ellipse
- `<line>` - Line drawing

### Special Elements
- `<define>` - Define reusable element templates

### Root-Level Support Elements
Non-visual or window-level elements placed directly under `<skin>`
(see "Root-Level Support Elements" below for details):
- `<oninit>` / `<onload>` - Run a VDJScript action once when the skin loads
- `<font>` - Default skin font, plus browser variants `<fonttoolbar>`, `<fontsearch>`, `<fontheader>`, `<fontgridtitle>`, `<fontplugins>`
- `<customicons>` - Replace/override the default icon sprite
- `<background>` - Window background fill or tile
- `<dialogs>` - Dark/light mode for native VirtualDJ dialogs
- `<copyright>` - Copyright text metadata
- `<logo>` - Placement of the VirtualDJ logo
- `<grabzone>` - Area that drags the whole window
- `<resizezone>` - Area that resizes the window

---

## Element Details

### `<deck>`

Groups elements for a specific deck without adding `deck="x"` to each child.

**Syntax:** `<deck deck="">`

**Attributes:**
- `deck` - Define the deck: `"1|2|3|4"`, `"left|right"`, `"leftvideo|rightvideo"`, `"master"`, `"default"`

**Children:** Any skin element

**Example:**
```xml
<deck deck="left">
    <button action="play_pause">
        <pos x="100" y="100"/>
        <size width="80" height="45"/>
    </button>
</deck>
```

---

### `<panel>`

Container for grouping elements that can be shown/hidden together. Panels are very useful for switching between groups on the same screen position with buttons or shortcuts.

**Syntax:** `<panel visible="" name="" group="" visibility="">`

**Attributes:**
- `visible=""` or `visibility=""` - Initial visibility: `"yes"` (shown at start) or `"no"` (hidden). Can also be a VDJScript action returning true/false for dynamic visibility
- `name=""` - Panel identifier. Elements with matching `panel=""` attribute belong to this panel. Name also stores visibility state across sessions
- `group=""` - (optional) Group name. Only one panel from a common group can be shown at a time. Showing a panel hides others in the same group

**Children:** Any skin element

**Usage Patterns:**

**1. Visibility-based (Automatic):**
Elements automatically show/hide based on VDJScript conditions.
```xml
<panel visibility="loop">
    <!-- Displayed only when deck is in loop -->
    <button action="loop_exit">
        <pos x="100" y="100"/>
        <size width="80" height="45"/>
    </button>
</panel>

<panel visibility="not loop">
    <!-- Displayed when deck is not in loop -->
    <button action="loop 4">
        <pos x="100" y="100"/>
        <size width="80" height="45"/>
    </button>
</panel>
```

**2. Name/Group-based (Manual):**
User manually switches between panels using buttons or shortcuts. Current state persists across sessions.
```xml
<panel group="loops" name="autoloops" visible="yes">
    <!-- Auto loop buttons (shown by default) -->
    <button action="loop 1">
        <pos x="100" y="100"/>
    </button>
    <button action="loop 2">
        <pos x="180" y="100"/>
    </button>
</panel>

<panel group="loops" name="manualloops" visible="no">
    <!-- Manual loop buttons (hidden by default) -->
    <button action="loop_in">
        <pos x="100" y="100"/>
    </button>
    <button action="loop_out">
        <pos x="180" y="100"/>
    </button>
</panel>

<!-- Button to toggle between panels -->
<button action="skin_panelgroup 'loops' 'autoloops'">
    <pos x="100" y="50"/>
    <text text="Auto"/>
</button>
<button action="skin_panelgroup 'loops' 'manualloops'">
    <pos x="180" y="50"/>
    <text text="Manual"/>
</button>
```

**3. Remote full-screen view toggle:**
Bundled Remote skins commonly switch between deck and browser views with a global skin variable, then leave deck-side subpanels as normal named panels:

```xml
<button action="toggle '$rmbrowser'"/>

<panel name="rmdecksview" visibility="var '$rmbrowser' 0">
    ...
</panel>

<panel name="rmbrowserview" visibility="var '$rmbrowser' 1" breakline1="90" breakline2="1476-20">
    <browser>
        <pos x="25" y="102"/>
        <size width="781" height="1272"/>
    </browser>
</panel>
```

Settings overlays in the same bundled Remote files use the same idea with `$rmsettings`:

```xml
<oninit action="set '$rmsettings' 0"/>
<button action="toggle '$rmsettings'"/>
<panel name="rmsettingsview" visibility="var '$rmsettings' 1">
    ...
</panel>
```

Source: `Built-in skin` (`examples/Skins/Built-In/Remote/9x16P.xml`, `9x16T.xml`, `3x4T.xml`, `4x3T.xml`, `16x9T.xml`, `16x10T.xml`)

**Performance Tip:** If multiple elements share the same visibility condition, nest them in a single `<panel>` instead of adding `visibility=""` to each element individually.

### Conditional Structure vs Visibility

`visibility=""` and `condition=""` are both VDJScript-driven gates, but they are useful for different jobs:

- `visibility=""` controls whether an existing element is displayed. Use it for live UI state that can change without rebuilding the skin, such as loop state, deck assignment, browser focus, or a panel that should appear and disappear.
- `condition=""` selects whether an element, group, browser, or define variant participates in the loaded skin structure. Use it for mutually exclusive layout branches, conditional color/class definitions, conditional `<nbdecks>` entries, and other choices that are normally refreshed with `load_skin`.

Operational rules:

- `condition=""` takes a VDJScript action/query that returns true or false.
- `condition=""` is evaluated when the skin is loaded or reloaded. It does not live-update when its source action changes later.
- A false `condition=""` branch is ignored/not loaded; it is not merely hidden.
- Staff guidance says `condition=""` can be added to all skin elements and most nested children. Built-in/staff examples include OS-specific groups, conditional `<nbdecks>`, conditional `customicons`, conditional vector-state children, and conditional background variants.
- Use `condition=""` for structural choices: layout family, OS-specific buttons, color-scheme asset branches, root/deck count, breakline selection, and heavy UI branches where saving loaded elements matters.
- Use `visibility=""` or panel `visible=""` / `visibility=""` for live choices: `masterdeck`, loaded/play state, loop state, `skin_panel` state, browser focus/zoom, and panels that should appear or disappear while performing.
- If a button or menu changes a variable that is read by `condition=""`, include `load_skin` in that action so VirtualDJ reparses the branch.
- If many elements share one live visibility predicate, put them in one wrapper `<panel>` or `<group>` with that `visibility=""`; this is both cleaner and cheaper than repeating the same predicate on every child.
- `visibility=""` can be a boolean action or a numeric opacity. For ternaries that return opacity, use `constant` so the branch returns a number: `visibility="deck 1 loaded ? constant 0.5 : constant 0.0"`.

Examples:

```xml
<group condition="var_equal '@$skin_mode' 0">
    <panel class="pro_decks_above" visibility="not browser_zoom"/>
    <panel class="browser_zoom_decks_above" visibility="browser_zoom"/>
</group>

<panel class="pro_2decks" condition="var_equal '@$layout_4deck' 0"/>
<panel class="pro_4decks" condition="var_equal '@$layout_4deck' 1"/>
```

Deck-state example:

```xml
<!-- Good: live masterdeck display state. -->
<textzone visibility="masterdeck">
    <text color="color_masterdeck" action="get_bpm"/>
</textzone>

<!-- Good: one live element when only the color changes. -->
<textzone>
    <text color="`deck [DECK] masterdeck ? color 'orange' : color 'white'`"
          action="get_bpm"/>
</textzone>

<!-- Avoid for live deck state: this is structural and reload-bound. -->
<text color="color_masterdeck" action="get_bpm" condition="masterdeck"/>
```

Source: `Official`, `Official forum`, `Community`, `Local test`, `Inference`

---

### `<stack>`

Container that displays multiple items with smooth fade transitions. The official docs say it shows only the last N visible items based on number of slots, but local testing did not reproduce that queueing behavior — see the caveat below. Perfect for temporary notifications and context-sensitive UI panels that appear/disappear with visual feedback.

**Syntax:** `<stack fadein="" fadeout="">`

**Attributes:**
- `fadein=""` - (optional) Time in ms for items to fade in from nothing to full display. Example: `fadein="200ms"`
- `fadeout=""` - (optional) Time in ms for items to fade out from full display to nothing. Example: `fadeout="500ms"`

**Children:**
- `<size width="" height=""/>` - Define width and height of each slot
- `<slot x="" y="">` - Multiple slots allowed. Each slot has x/y position parameters defining where items appear
- `<item>` - Multiple items allowed (typically more items than slots)
  - `visibility=""` - VDJScript condition determining when item should be visible
  - `class=""` - Reference to a defined class
  - Any skin element can be nested inside `<item></item>`

**How it Works:**
- Stack displays only the last N "visible" items (where N = number of slots)
- Items appear in slots based on their visibility conditions
- When an item becomes visible, it fades in
- When an item becomes invisible, it fades out
- Perfect for stacking temporary UI feedback messages

**Example:**
```xml
<stack fadein="200ms" fadeout="500ms">
    <size width="370" height="170"/>
    
    <!-- Define 3 slots (bottom to top) -->
    <slot x="-370" y="170+20+170+20+170" />  <!-- Bottom slot -->
    <slot x="-370" y="170+20+170"/>          <!-- Middle slot -->
    <slot x="-370" y="170"/>                 <!-- Top slot -->
    
    <!-- Define items (panels that can appear in slots) -->
    <item class="looppanel" visibility="is_using 'loop' 8000ms"></item>
    <item class="eqpanel" visibility="is_using 'equalizer' 1000ms"></item>
    <item class="filterpanel" visibility="is_using 'filter' 1000ms"></item>
    <item class="cuepanel" visibility="is_using 'cue' 1000ms"></item>
    <item class="samplerpanel" visibility="is_using 'sample' 1000ms 8000ms"></item>
    <item class="fxpanel" visibility="is_using 'effect' 1000ms 8000ms"></item>
    <item class="padspanel" visibility="is_using 'pads' 1000ms"></item>
    <item class="nexttrackpanel" visibility="is_using 'load' 5000ms"></item>
</stack>
```

**Common Use Cases:**
- Temporary feedback panels ("Loop Active", "Effect Engaged", "Track Loading")
- Context-sensitive control panels that appear when using specific features
- Status notifications that stack and auto-dismiss
- Progressive disclosure UI where multiple contextual panels may be visible simultaneously

**Caveat (`Local test`, 2026-07-14):** The "last N visible items" queueing described above was not reproduced locally — when more items are visible than there are slots, items render overlapping in the slots rather than the newest N winning. Keep item visibility mutually exclusive per stack (e.g. a selector variable with `var_equal`-gated items) and use `fadein`/`fadeout` for cross-fades. See [Skin Runtime Findings](Skin%20Runtime%20Findings.md#stack-slot-assignment-is-not-a-queue).

Source: `Official` (Skin SDK element list and `Skin Stack.html` wiki page), `Local test` (StackRaver, slot-assignment caveat above).

---

### `<define>`

Define reusable element templates to avoid repetition.

**Syntax:** `<define class="" classdeck="" placeholders="" condition="" [element attributes]>`

**Attributes:**
- `class` - Template name (e.g., `"small_button"`)
- `classdeck` - Optional deck specification
- `placeholders` - Optional named placeholder contract for attributes passed by the call site
- `condition` - Optional VDJScript query controlling whether this definition variant is available
- Plus any attributes of the element being defined

**Children:** Children of the element being defined

**Example:**
```xml
<!-- Define a button template -->
<define class="mybutton" classdeck="left">
    <size height="45" width="80"/>
    <on x="100" y="125"/>
    <off x="100" y="170"/>
    <over x="100" y="215"/>
</define>

<!-- Use the template -->
<button class="mybutton" action="play_pause">
    <pos x="100" y="50"/>
</button>
```

**Class Name Casing:**

- In practice, skin class matching is case-insensitive, so `class="SAMPLER_ROW"` and `class="sampler_row"` will resolve to the same define.
- A useful house style is to write define names in uppercase when declaring them and lowercase when implementing them, because it makes the definition/call sites easier to visually distinguish.
- This casing convention applies to the `class` name itself. Placeholder tokens should still stay uppercase inside brackets, e.g. `[WIDTH]`, because that is the established placeholder style shown in the SDK/forum examples.

**Color Defines:**
```xml
<define color="deckcolorbright" value="#1e7b96" deck="1"/>
<define color="deckcolorbright" value="#b73841" deck="2"/>
```

**Named Placeholders:** Modern working skins commonly declare named placeholders with `placeholders=""`, then use bracketed uppercase tokens inside the define body.

- `*name` marks a placeholder for math/expression substitution. Atomix examples describe this as needed for simple math, but the exact boundary of "math" is not fully documented. Boolean operations, `condition=""`, and other VDJScript expression contexts may be part of that boundary.
- `name=value` supplies a default.
- Tokens are referenced as `[NAME]` in the template body.
- Call sites pass values as normal XML attributes, usually lower-case.

```xml
<define class="LABELED_BUTTON" placeholders="*label,width=160,color=textoff">
    <size width="[WIDTH]" height="24"/>
    <text text="[LABEL]" color="[COLOR]"/>
</define>

<button class="labeled_button" label="SYNC" width="220" action="sync"/>
```

Do not list pass-through element attributes such as `action` or `query` in a visual class's `placeholders=""` contract unless the define body forwards them, usually onto an inner `<button action="[ACTION]" query="[QUERY]">`. In local Remote skin testing, declaring `action`/`query` as placeholders on a base button style consumed those attributes: the button still showed its down visual state, but no command fired.

Official built-in skins also use many unstarred placeholders in ordinary pass-through contexts, including `action="[ACTION]"`, `text="[TEXT]"`, `source="[SOURCECOLOR]"`, `visibility="[ACTION1]"`, and `scroll="[ACTION2]"`. Do not assume every placeholder inside a VDJScript-bearing attribute must be starred.

**Starred placeholders in conditions:** The official SDK describes starred placeholders primarily around math. Local canary tests suggest some condition/boolean-expression uses also need starred placeholders, but the exact behavior is still unclear and should be tested per pattern.

Unstarred string placeholder values may not substitute in some text or condition forms:

```xml
<!-- Observed fragile/non-working in local runtime tests: [SIDE] stayed literal -->
<define class="STRING_CONDITION_CANARY" placeholders="side=false">
    <text text="[SIDE]"/>
    <group condition="param_equal '[SIDE]' 'true'"/>
</define>
```

The starred form substituted correctly:

```xml
<define class="STRING_CONDITION_CANARY" placeholders="*side=false">
    <text text="[SIDE]"/>
    <group condition="param_equal '[SIDE]' 'true'"/>
</define>
```

For boolean-like placeholders, direct boolean conditions worked when the placeholder was starred and values were exactly `true` / `false`:

```xml
<define class="TRACK_MODIFIERS_PANEL" placeholders="*mirror=false">
    <group x="+0" y="+5" condition="not [MIRROR]"/>
    <group x="+265" y="+5" condition="[MIRROR]"/>
</define>

<panel class="track_modifiers_panel" mirror="false"/>
<panel class="track_modifiers_panel" mirror="true"/>
```

String comparisons also worked when the substituted placeholder was quoted:

```xml
condition="param_equal '[MIRROR]' 'true'"
```

Numeric starred placeholders work in the usual expression style:

```xml
<define class="EXAMPLE" placeholders="*flip=0">
    <group condition="param_equal [FLIP] 0"/>
    <group condition="param_equal [FLIP] 1"/>
</define>
```

Current working guidance:

- Use unstarred placeholders for simple pass-through values that match the official skin examples.
- Use starred placeholders where placeholder values participate in arithmetic, coordinate/size formulas, boolean conditions, `param_equal` comparisons, or other expression-like contexts.
- Record build-specific canary results before treating any narrower rule as definitive.

**Legacy Positional Placeholders:** Some SDK/forum examples use `$1`, `$2`, etc. and pass values as `$1=""`, `$2=""` attributes:
```xml
<define class="mytext">
    <text text="$1 - $2" color="$3"/>
</define>

<textzone class="mytext" $1="Artist" $2="Title" $3="white">
    <pos x="100" y="50"/>
</textzone>
```

**Conditional Define Variants:** Multiple definitions can share the same class name when their `condition=""` expressions are mutually exclusive. This is useful when a theme or layout mode needs a different internal implementation while keeping the call sites stable.

```xml
<define class="PADBUTTON" placeholders="*source" condition="var_not_equal '@$color_scheme' 4">
    <off color="button_background"/>
    <text action="pad_param [SOURCE]"/>
</define>

<define class="PADBUTTON" placeholders="*source" condition="var_equal '@$color_scheme' 4">
    <off color="black"/>
    <text action="pad_param [SOURCE]"/>
</define>

<button class="padbutton" source="1" action="pad 1"/>
```

---

### `<button>`

Clickable button with multiple states and support for image graphics or vector shapes. Buttons can have text/icon overlays and support various mouse interactions.

**Syntax:** `<button action="" leftclick="" middleclick="" rightclick="" dblclick="" query="">`

**Attributes:**
- `action=""` - VDJScript action performed on button press (default click)
- `leftclick=""` - Different action for left mouse button
- `middleclick=""` - Different action for middle mouse button  
- `rightclick=""` - Different action for right mouse button
- `dblclick=""` - Different action for double-click
- `query=""` - VDJScript query that enables `<on>` graphics when true (alternative to `action` for state determination)

**Confirmed Behavior Notes:**
- `query=""` drives the button's `<on>` graphics, not `<selected>`. If a button should change appearance when a VDJScript condition is true, use `<off>`/`<on>` for the graphics state. Official reference: [VirtualDJ Skin Button](https://www.virtualdj.com/wiki/Skin%20Button.html)
- For generic pad banks in skins, follow the bundled/default skin pattern: `action="pad <n>"`, shifted/right-click action `padshift <n>`, label `textaction="pad <n>"`, and color source `pad_color <n>` or `pad_button_color <n>`. This keeps the skin independent of the selected pad page; the page may be hot cues, FX, loops, sampler, custom buttons, or controller-specific actions. Use `pad_has_action <n>` only when the skin needs to hide or disable a pad with no current-page push action. Official references: [Pads Editor](https://www.virtualdj.com/manuals/virtualdj/editors/padseditor.html), [VDJScript verbs](https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs/). Built-in references: [Pro.xml](../examples/Skins/Built-In/Desktop/Pro.xml), [Performance.xml](../examples/Skins/Built-In/Desktop/Performance.xml), [16x9T.xml](../examples/Skins/Built-In/Remote/16x9T.xml).
- `rightclick=""` can run any VDJScript action, including built-in menu/popup actions such as `key_match_menu`, `deck_options`, `loop_options`, `browser_options`, `search_options`, `pad_page_select 1`, `effect_select 1`, `effect_select_popup 1`, and `sampler_options`. This is the normal pattern for making a right-click open an existing VirtualDJ menu.
- Custom skin `<menu>` elements are different: they open when their own menu hit area is clicked. The official `<menu>` element has no documented name/id trigger that lets another button open that exact custom menu from `rightclick=""`. If you need a custom right-click panel, use `rightclick="skin_panel 'my_context_panel' on"` and build the panel with normal buttons, or place a `<menu>` object where the user clicks. Placing a `<menu>` object there makes that area a normal menu click target, not a right-click-only target.
- Dynamic button border colors are not currently supported. Even though `border=""` is documented as a color field, official clarification from VirtualDJ CTO Adion says dynamic colors are not supported for border color. Use `visual type="color"` overlays or underlays when a border needs to follow `cue_color`, `sampler_color`, etc. Official reference: [Border Color using placeholder](https://virtualdj.com/forums/242871/VirtualDJ_Skins/Border_Color_using_placeholder.html)
- For dynamic text colors, the most reliable documented pattern is to use a single `<text>` element with a backticked VDJScript expression in `color`, rather than relying on `colorselected=""` or other state-specific color attributes to evaluate VDJScript. Official references: [Skin Default Colors](https://www.virtualdj.com/wiki/Skin%20Default%20Colors.html), [Skin text action; visibility or visual?](https://www.virtualdj.com/forums/267953/VirtualDJ_Skins/Skin_text_action%3B_visibility_or_visual%3F.html)
- The current documented `<button>` API is click-oriented: `action`, `leftclick`, `middleclick`, `rightclick`, `dblclick`, and `query`. No generic drag/drop callback is documented for `<button>`. If you need a drag target in a skin, use `<dropzone>` instead of inventing a button "dragged" state. For sampler slot assignment inside custom pad pages, current working XML uses pad `drop="sampler_assign <slot>"` rather than a skin button callback; see [SAMPLER SIMPLE.xml](../examples/Pads/SAMPLER%20SIMPLE.xml). Official references: [VirtualDJ Skin Button](https://www.virtualdj.com/wiki/Skin%20Button.html), [Skin SDK Dropzone](https://www.virtualdj.com/wiki/Skin%20SDK%20Dropzone.html), [VDJScript verbs](https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html), [Sampler manual](https://www.virtualdj.com/manuals/virtualdj/interface/browser/sideview/sampler.html)

**Children:**
- `<tooltip>` - Tooltip text (supports `\n` for multiple lines)
- `<pos x="" y=""/>` - Position on screen
- `<size width="" height=""/>` - Button dimensions

**Graphics States (Image-based):**
Reference coordinates in skin.png file:
- `<up x="" y=""/>` - Default up state  
- `<down x="" y=""/>` - Pressed state
- `<on x="" y=""/>` - Active/enabled state
- `<off x="" y=""/>` - Inactive/disabled state
- `<over x="" y=""/>` - Mouse hover state
- `<selected x="" y=""/>` - Selected state
- `<downselected x="" y=""/>` - Pressed while selected
- `<overselected x="" y=""/>` - Hover while selected

**Graphics States (Vector-based):**
Draw buttons with code instead of referencing PNG coordinates. Attributes:
- `shape=""` - `"square"` (default) or `"circle"`
- `color=""` - Fill color (hex, RGB, or named)
- `border=""` - Border color
- `border_size=""` - Border thickness in pixels
- `radius=""` - Corner radius for rounded corners
- `gradient=""` - `"horizontal"`, `"vertical"`, or `"circular"` (requires `color2`)
- `color2=""` - End color for gradient (start color is `color`)

**Transparent / Hover-only Buttons:**
Omitting `<up>` (and `<off>` for action buttons) leaves the button fully transparent at rest — the hit area defined by `<size>` still exists, so hover and click work normally. Only define the states you want to be visible. This is useful for invisible overlay buttons or contextual controls that should only reveal themselves on hover.

**Drawing and Mouse Masks:**
- `<clipmask x="" y=""/>` - B&W graphic used as clip mask (avoid if possible - use transparent PNG)
- `<mousemask x="" y=""/>` - B&W graphic mask to determine if mouse is over button

**Text Overlays:**
- `<text>` - Text overlay on button (see textzone for full attributes)
- `<textover>` - Text when mouse is over
- `<textdown>` - Text when button is pressed
- `<textselected>` - Text when button is selected

**Icon Overlays:**
- `<icon>` - Icon overlay (can use custom or system icons)

**Example 1: Image-based Button**
```xml
<button action="loop">
    <pos x="125" y="220"/>
    <size width="70" height="44"/>
    <up x="120" y="1890" />
    <over x="120" y="1990" />
    <down x="120" y="2090" />
    <selected x="120" y="2190" />
    <tooltip>Loop 4 beats</tooltip>
</button>
```

**Example 2: Vector Graphics Button**
```xml
<button action="loop">
    <pos x="125" y="220"/>
    <size width="70" height="44"/>
    <up radius="6" border_size="2" border="black" color="#2F3034" />
    <over radius="6" border_size="2" border="black" color="#2C3B47" />
    <down radius="6" border_size="2" border="black" color="#1287E0"/>
    <selected radius="6" border_size="2" border="black" color="#1287E0"/>
    <text size="15" color="#909090" align="center" weight="bold" text="LOOP"/>
    <textover size="15" color="#BBBBBB" align="center" weight="bold" text="LOOP"/>
    <textdown size="15" color="white" align="center" weight="bold" text="LOOP"/>
    <textselected size="15" color="white" align="center" weight="bold" text="LOOP"/>
</button>
```

**Example 3: Button with Gradient**
```xml
<button action="play_pause">
    <pos x="100" y="100"/>
    <size width="80" height="45"/>
    <off radius="4" border="black" border_size="1" 
         color="#404040" color2="#202020" gradient="vertical"/>
    <on radius="4" border="black" border_size="1" 
        color="#00FF00" color2="#008800" gradient="vertical"/>
</button>
```

**Example 4: Transparent / Hover-only Button**

Omitting `<up>` makes the button invisible at rest. It appears only when hovered or pressed. The invisible hit area remains fully interactive.

```xml
<button action="some_action">
    <pos x="100" y="100"/>
    <size width="80" height="40"/>
    <!-- no <up> = fully transparent at rest -->
    <over color="#ffffff" radius="4" border="#aaaaaa" border_size="1"/>
    <down color="#cccccc" radius="4"/>
    <textover text="LABEL" color="black" align="center"/>
</button>
```

> **Note:** The hit area defined by `<size>` is always active regardless of visual transparency, so clicks still register even when the button is invisible. If you need to restrict interactivity to a specific shape, use `<mousemask>`.

**Example 5: Right-click to Open a Menu/Popup**

Use `rightclick=""` when the menu is exposed by a VDJScript action.

```xml
<button action="key_match_button" rightclick="key_match_menu">
    <pos x="100" y="100"/>
    <size width="80" height="24"/>
    <text action="get_key" align="center"/>
</button>

<button action="pad_page btn1" rightclick="pad_page_select 1">
    <pos x="100" y="130"/>
    <size width="100" height="24"/>
    <text action="pad_page btn1"/>
</button>

<button action="select" rightclick="select &amp; deck_options">
    <pos x="10" y="10"/>
    <size width="34" height="465"/>
</button>
```

---

### `<icon>`

Glyph overlay drawn on top of a `<button>`, `<define>`, or `<menu>`. This is
the standard built-in-skin way to put a recolorable arrow, chevron, settings
gear, close cross, etc. on a vector or transparent button without baking the
glyph into each button graphic.

`<icon>` is not in the official Skin SDK element list; the only official
appearance is a usage example on the CustomIcons wiki page
(`<icon sysicon="arrowleft" width="32" height="32"/>`). Everything below is
reverse-engineered from bundled skins: 750 uses across 17 built-in skin files
(Desktop `Vertical.xml` 136, `Performance.xml` 128, `Pro.xml` 110, plus the
Remote and Lite skins).

**Syntax:** `<icon sysicon="" x="" y="" width="" height="" color="" colorover="" colordown="" colorselected="" align="" dx="" dy=""/>`

Always self-closing. No closing `</icon>` tag or element children appear
anywhere in the built-in skins.

**Glyph source (pick one):**

| Attribute | Description | Source |
| --- | --- | --- |
| `sysicon=""` | Name of a system icon (see [Explicit `sysicon` Names](#explicit-sysicon-names) below). Most common source: 515 of 750 uses. Defines often forward it as a placeholder, e.g. `sysicon="[SYSICON]"` | `Built-in skin`, `Official` (CustomIcons page example) |
| `x=""` `y=""` | Coordinates of a glyph cropped from the skin image instead of a system icon (226 uses). The crop is used as a recolorable mask: the same state-color attributes apply, e.g. `<icon x="288" y="101" width="11" height="11" coloroff="textdark" colorover="textover" coloron="texton"/>` (`Performance.xml`) | `Built-in skin` |

No `file=""` attribute is observed on `<icon>`; a separate icon image file is
declared via root-level `<customicons file=""/>`, not per icon.

**Size and placement:**

| Attribute | Description | Source |
| --- | --- | --- |
| `width=""` `height=""` | Rendered size in pixels (on ~740 of 750 uses). Icons scale freely; common sizes are 12-40 px | `Built-in skin` |
| `align=""` | Horizontal alignment inside the parent button: `"center"` (112 uses) or `"left"` (36 uses) | `Built-in skin` |
| `dx=""` `dy=""` | Pixel offset from the default/aligned position; accepts signed values like `dx="+160"` `dy="-1"` | `Built-in skin` |
| `iconsize=""` | Rare (3 uses, all `<icon sysicon="headphones" width="65" height="65" iconsize="65"/>` in Remote skins). Presumably the source cell size, matching the `customicons` attribute of the same name; exact semantics not yet confirmed | `Built-in skin` |

**State colors:**

Mirrors the button graphic states. All values are normal skin color values
(predefined names, defines, hex):

| Attribute | Button state | Built-in uses |
| --- | --- | --- |
| `color=""` | Base/default | 406 |
| `coloroff=""` | Off | 224 |
| `colorup=""` | Up | 14 |
| `coloron=""` | On (`query=""` true) | 3 |
| `colorover=""` | Mouse over | 477 |
| `colordown=""` | Pressed | 505 |
| `colorselected=""` | Selected | 354 |
| `coloroverselected=""` | Hover while selected | 12 |

**Other observed attributes:**

- `important=""` - 52 uses, values `"important"` (44) and `"true"` (8), always
  on icons that share a button with text or sit in dense toolbars. Its exact
  effect is not yet confirmed locally; do not rely on it until tested.

**Children:** None.

**Example (system icon on a menu button, `examples/Skins/Built-In/Lite/Lite.xml`):**
```xml
<menu tooltip="SKIN LAYOUT\nSelect the layout adapted to your mixing style">
    <pos x="+50" y="+0"/>
    <size width="123" height="27"/>
    <text dx="10" width="90" fontsize="11" color="textoff3" colorover="textover"
          align="left" text="VDJ LITE" localize="true" important="true"/>
    <icon dx="45" dy="-1" sysicon="chevrondown" height="17" width="17"
          color="textdark" colorover="textover" colordown="texton"/>
</menu>
```

**Example (skin-image glyph with state colors, `examples/Skins/Built-In/Desktop/Performance.xml`):**
```xml
<button ...>
    <off shape="circle" color="darker" border_size="1" border="bordercolor3"/>
    <over shape="circle" color="dark" border_size="1" border="bordercolor3"/>
    <selected shape="circle" color="dark" border_size="1" border="bordercolor3"/>
    <icon x="288" y="101" width="11" height="11"
          coloroff="textdark" colorover="textover" coloron="texton"/>
</button>
```

See also [Default Icons](#default-icons) for the `sysicon` name table and
action-name icon behavior, and `<customicons>` under Root-Level Support
Elements for overriding the icon sprite.

Source: `Built-in skin` (attribute set and usage counts), `Official` (CustomIcons page example only)

---

### `<dropzone>`

Interactive area where files can be dragged and dropped to load them onto a
deck. Since VirtualDJ 2020 it can draw visual feedback (an `<over>` overlay)
while a drag is hovering.

**Syntax:** `<dropzone deck="" panel="" visibility="" os="">`

**Attributes:**
- `deck=""` - Target deck for the dropped file (global attribute). Built-in
  skins use `"1"`-`"4"` and `"left"`/`"right"`, or omit it entirely inside a
  `<deck>` container so the zone follows the enclosing deck
- `panel=""`, `visibility=""`, `os=""` - Standard global attributes

**Children:**
- `<pos x="" y=""/>` - Position (required)
- `<size width="" height=""/>` - Dimensions (required)
- `<over color="" border="" border_size="" shape=""/>` - Visual feedback while
  a drag hovers the zone (VirtualDJ 2020+). Accepts normal color values;
  `shape=""` is `"square"` or `"circle"`. Built-in skins typically use a
  transparent fill with a deck-colored border
- `<mousemask x="" y=""/>` - Optional B&W graphic mask for hit detection (`Official`; not used by any built-in skin)
- `<mouserect x="" y="" width="" height=""/>` - Optional rectangular hit zone (`Official`; not used by any built-in skin)
- `<mousecircle x="" y="" r=""/>` - Optional circular hit zone (`Official`; not used by any built-in skin)

**Example (`examples/Skins/Built-In/Desktop/Vertical.xml`):**
```xml
<dropzone deck="1">
    <pos x="+22-20" y="+0"/>
    <size width="159" height="342-2"/>
    <over color="transparent" border_size="1" border="deckcolor"/>
</dropzone>
```

Conditional `<pos>`/`<size>` children work inside dropzones like elsewhere:
the same `Vertical.xml` zones carry alternate `<pos ... condition="var_not_equal '@$4decks' 0"/>`
rows for the four-deck layout.

Built-in cross-check: 66 uses across 10 built-in skin files
(`Performance.xml` 20, `Pro.xml` 16, `Vertical.xml` 10, Lite/Starter 4 each).
Only `deck=""`, `<pos>`, `<size>`, and `<over>` appear in practice; the mouse
mask/rect/circle children are official-doc-only so far.

Source: `Official` ([Skin SDK Dropzone](https://www.virtualdj.com/wiki/Skin%20SDK%20Dropzone.html)), `Built-in skin`

---

### `<slider>` and `<knob>`

Movable slider control for faders, knobs, and other continuous value adjustments. Sliders can be horizontal, vertical, or circular (knobs).

**Syntax:** `<slider action="" dblclick="" rightclick="" orientation="" direction="" frommiddle="" relative="">`

**Attributes:**
- `action=""` - VDJScript action performed by the slider
- `leftclick=""` - Different action for left mouse button
- `rightclick=""` - Different action for right mouse button
- `dblclick=""` - Different action for double-click
- `orientation=""` - Slider type:
  - `"horizontal"` - Horizontal slider (default)
  - `"vertical"` - Vertical slider
  - `"circle"` or `"round"` - Circular slider/knob
- `direction=""` - Movement direction: `"normal"` or `"reversed"`
- `frommiddle=""` - `"true"` to split graphics at midpoint (useful for EQ knobs that go ±)
- `relative=""` - `"yes"` for relative movement, `"no"` for absolute positioning

**Children:**
- `<pos x="" y=""/>` - Position on screen
- `<size width="" height=""/>` - Slider dimensions (defines range)

**Linear Slider Graphics:**
- `<off>` or `<background>` - Background/track graphics (image or vector)
- `<on>` or `<fill>` - Fill/progress indicator (image or vector)
- `<fader>` or `<cursor>` - Moving handle/cursor (image or vector)
  - Has its own `<size>` if different from slider size
  - Can have `<off>`, `<over>` states
- `<over>` - Slider background when mouse is over

**Round Slider/Knob Graphics:**
- `<off>` - Knob background (circle shape with vector graphics)
- `<fader>` - Moving indicator/pointer
  - `anglemin=""` - Start angle in degrees (e.g., `-150`)
  - `anglemax=""` - End angle in degrees (e.g., `150`)
  - `color=""` - Indicator color
  - `width=""` - Indicator width
  - `height=""` - Indicator length/height
  - `radius=""` - Corner radius for indicator
- `<fill>` - (for round sliders only) Ring that shows value
  - `<off x="" y=""/>` - Ring graphic at 0%
  - `<on x="" y=""/>` - Ring graphic at 100%

**Mouse Control:**
- `<mouserect x="" y="" width="" height=""/>` - Define mouse-sensitive area (if different from slider size)

**Example 1: Vertical Fader (Vector Graphics)**
```xml
<slider action="level" rightclick="temporary" orientation="vertical">
    <pos x="23" y="100"/>
    <size width="6" height="124"/>
    <!-- Background track -->
    <off height="-21" color="faderinoff" shape="square" 
         border="darker" border_size="1" radius="3"/>
    <!-- Fill indicator -->
    <on height="-21" color="faderin" shape="square" 
        border="darker" border_size="1" radius="3"/>
    <!-- Mouse sensitive area (wider than visual) -->
    <mouserect x="-20" y="0" width="40" height="120"/>
    <!-- Moving fader handle -->
    <fader>
        <size width="40" height="21"/>
        <off x="236" y="266"/>
    </fader>
</slider>
```

**Example 2: Horizontal Fader (Image Graphics)**
```xml
<slider action="crossfader" orientation="horizontal">
    <pos x="400" y="600"/>
    <size width="300" height="30"/>
    <background x="0" y="800"/>
    <cursor>
        <size width="40" height="40"/>
        <off x="340" y="800"/>
        <over x="380" y="800"/>
    </cursor>
</slider>
```

**Example 3: Round Knob (EQ-style)**
```xml
<slider action="eq_high" frommiddle="true" orientation="round" relative="no">
    <pos x="400" y="200"/>
    <size width="48" height="48"/>
    <!-- Knob body (vector circle) -->
    <off width="40" height="40" shape="circle" 
         color="#3a3b3e" color2="#252628" gradient="vertical" 
         border="#1e1e20" border_size="2"/>
    <!-- Rotating indicator line -->
    <fader color="#aaaaaa" width="3" height="17" radius="2" 
           anglemin="-150" anglemax="150"/>
</slider>
```

**Example 4: Round Knob with Ring Fill**
```xml
<slider action="filter" orientation="round">
    <pos x="500" y="200"/>
    <size width="60" height="60"/>
    <!-- Knob background -->
    <off width="50" height="50" shape="circle" color="#333333"/>
    <!-- Moving indicator -->
    <fader color="white" width="4" height="20" 
           anglemin="-140" anglemax="140"/>
    <!-- Progress ring -->
    <fill>
        <off x="0" y="900"/>   <!-- Empty ring graphic -->
        <on x="60" y="900"/>   <!-- Full ring graphic -->
    </fill>
</slider>
```

**Notes:**
- **Knobs** are just sliders with `orientation="round"` or `orientation="circle"`
- Use `frommiddle="true"` for EQ-style knobs that adjust from center position
- `anglemin` and `anglemax` define the rotation range (typically -150° to +150° for 300° total rotation)
- Linear sliders can use vector graphics (`shape`, `color`, `border`) or image references (`x`, `y`)
- For better mouse control, use `<mouserect>` to define a larger hit area than the visual slider

---

### `<visual>`

Display zone for static graphics or dynamic visual feedback. Visuals change their display based on various data sources to reflect deck status, volume levels, position, etc.

**Syntax:** `<visual source="" type="" orientation="" direction="" granularity="">`

**Attributes:**
- `source=""` - Data source driving the visual:
  - `"beat"` - Beat intensity
  - `"rotation"` - Disc rotation angle (depends on position and RPM speed)
  - `"arm"` - Turntable arm position (moves on PLAY and PAUSE)
  - `"volume"` - Volume level (depends on crossfader and level values)
  - `"position"` - Position in song
  - Any `get_*` VDJScript action that returns a numeric value (e.g., `"get_level"`, `"get_bpm"`)

- `type=""` - Display mode:
  - `"onoff"` - Binary on/off display (shows `<on>` graphic if source≥2048, `<off>` if source<2048)
  - `"linear"` - Smooth progression between `<off>` and `<on>` graphics
  - `"color"` - Solid color display (no graphics files needed)
  - `"custom"` - Custom display mode

- `orientation=""` - Direction of progression:
  - `"horizontal"` - Left to right
  - `"vertical"` - Bottom to top

- `direction=""` - Alternative specification for progression:
  - `"left"` - Progress from left
  - `"right"` - Progress from right
  - `"up"` - Progress from bottom up
  - `"down"` - Progress from top down

- `granularity=""` - (for type=linear) Number of sections to divide visual into instead of smooth progression. Useful for VU-meters with discrete segments

**Children:**
- `<pos x="" y=""/>` - Position on screen
- `<size width="" height=""/>` - Visual dimensions
- `<clipmask x="" y=""/>` - (optional) B&W graphic used as clip mask for drawing
- `<off x="" y=""/>` - (all types except "custom") Graphic for low/minimum value state
- `<on x="" y=""/>` - (all types except "custom") Graphic for high/maximum value state

**How Linear Visuals Work:**
The visual progressively reveals the `<on>` graphic as the source value increases, creating smooth transitions for meters and progress indicators.

**Example 1: Volume Meter (Vertical Linear)**
```xml
<visual source="volume" type="linear" orientation="vertical">
    <pos x="100" y="100"/>
    <size width="30" height="200"/>
    <off x="0" y="300"/>   <!-- Empty/low volume graphic -->
    <on x="30" y="300"/>   <!-- Full/high volume graphic -->
</visual>
```

**Example 2: Beat Intensity Indicator (On/Off)**
```xml
<visual source="beat" type="onoff">
    <pos x="50" y="50"/>
    <size width="40" height="40"/>
    <off x="0" y="100"/>   <!-- No beat graphic -->
    <on x="40" y="100"/>   <!-- Beat active graphic -->
</visual>
```

**Example 3: Song Position (Horizontal Linear)**
```xml
<visual source="position" type="linear" orientation="horizontal">
    <pos x="100" y="500"/>
    <size width="800" height="20"/>
    <off x="0" y="600"/>   <!-- Start position graphic -->
    <on x="0" y="620"/>    <!-- End position graphic -->
</visual>
```

**Example 4: VU Meter with Discrete Segments**
```xml
<visual source="get_vu_meter" type="linear" orientation="vertical" granularity="10">
    <pos x="50" y="100"/>
    <size width="20" height="200"/>
    <off x="0" y="400"/>
    <on x="20" y="400"/>
</visual>
```

**Example 5: Rotation Disc Visual**
```xml
<visual source="rotation" type="linear" orientation="horizontal">
    <pos x="200" y="200"/>
    <size width="300" height="300"/>
    <off x="0" y="800"/>   <!-- Disc at 0° rotation -->
    <on x="300" y="800"/>  <!-- Full rotation graphic -->
</visual>
```

**Example 6: Using VDJScript Query as Source**
```xml
<visual source="`get_level`" type="linear" orientation="vertical">
    <pos x="100" y="100"/>
    <size width="40" height="150"/>
    <off x="0" y="500"/>
    <on x="40" y="500"/>
</visual>
```

**Common Use Cases:**
- VU meters showing audio levels
- Progress bars for song position
- Beat flash indicators
- Vinyl rotation displays
- Crossfader position indicators
- Volume level meters
- Effect wet/dry indicators

**Notes:**
- For `type="onoff"`, the threshold value is 2048 (half of 4096, the typical maximum)
- `type="linear"` provides smooth transitions proportional to the source value
- `granularity` creates stepped/segmented displays instead of smooth
- Can use clipmasks for complex shaped meters
- Additional types not listed here (`waveform`, `spectrum`, `cover`) are documented with examples in [VirtualDJ Reference.md — visual type reference](VirtualDJ%20Reference.md#visual-type----full-type-reference)

---

### `<textzone>`

Display area for static or dynamic text.

**Syntax:** `<textzone deck="" resetcounter="" action="" group="horizontal">`

**Attributes:**
- `deck` - Deck number
- `resetcounter` - `"true"` to reset counter on click
- `action` - VDJScript action on click
- `group` - `"horizontal"` to display nested texts inline

**Children:**
- `<pos x="" y=""/>` - Position
- `<size width="" height=""/>` - Dimensions
- `<background color=""/>` or `<background x="" y=""/>` - Background
- `<text>` - Text elements (see below)

**Text Element Attributes:**
- `font` - Font name (default: Arial)
- `weight` - Font weight: `"bold"`, `"normal"`
- `fontsize` - Size in pixels. `size` is also accepted as a synonym: built-in skins overwhelmingly use `fontsize=` (~1,600 uses vs 5), but `size=` appears in shipped skins and is `Local test` confirmed working (see `Skin Runtime Findings.md`). Prefer `fontsize` to match built-in convention.
- `color` - Text color
- `align` - `"left"`, `"center"`, `"right"`
- `valign` - `"top"`, `"center"`, `"bottom"`
- `text` - Static text or VDJScript query in backticks
- `format` - Format string for dynamic text
- `width` - Max width before wrapping
- `multiline` - `"true"` for multi-line text
- `action` - VDJScript action for clickable text

**Example:**
```xml
<textzone>
    <pos x="100" y="50"/>
    <size width="300" height="30"/>
    <text font="Arial" fontsize="18" color="white" 
          text="`get_artist` - `get_title`" align="center"/>
</textzone>
```

---

## Lyrics AI In Skins

VirtualDJ 2026's AI lyrics are mainly controlled by the application engine and options, not by a skin-owned lyric text renderer.

Skin-safe signals and actions:

- `has_lyrics` - boolean query for whether the loaded deck has lyrics.
- `get_lyrics_language` - text query for the detected lyric language on the loaded deck.
- `edit_lyrics` - opens the Lyrics Editor for the loaded deck.
- `setting 'showLyrics'` - toggle/query the built-in waveform lyric overlay.
- `setting 'lyricsWaveformSize'` - adjust/query the waveform lyric text size multiplier.

Important styling limit:

- Skins can style lyric badges, editor buttons, language indicators, and waveform lyric option controls.
- Skins do not appear to expose the current lyric line, per-word timing, AI confidence, censor matches, extraction progress, or independent colors/fonts for the built-in lyric renderer.

Example:

```xml
<button action="setting 'showLyrics'" query="setting 'showLyrics'">
  <size width="70" height="24"/>
  <off color="#181818" border="#333333" radius="4"/>
  <on color="#243246" border="#78a8ff" radius="4"/>
  <text text="LYRICS" color="#eeeeee" fontsize="11" align="center"/>
</button>

<text action="has_lyrics ? get_lyrics_language : get_text ''"
      color="#d8d8d8"
      fontsize="11"
      align="center"/>
```

See [Lyrics AI and Skins](Lyrics%20AI%20and%20Skins.md) for the focused reference, including AI cache behavior, stems requirements, browser-filter quirks, and low-documentation script verbs worth testing.

---

### `<group>`

Generic container for organizing elements.

**Syntax:** `<group name="" x="" y="">`

**Attributes:**
- `name` - Group identifier
- `x`, `y` - Position offset for all children

**Conditional positioning note:** For conditional group placement, prefer putting `x` / `y` and `condition` directly on separate `<group>` branches:

```xml
<group x="+0" y="+5" condition="not [MIRROR]">
    ...
</group>
<group x="+265" y="+5" condition="[MIRROR]">
    ...
</group>
```

Avoid relying on conditional child `<pos>` elements to move a `<group>`:

```xml
<!-- Observed fragile/non-working in local runtime tests -->
<group>
    <pos x="+0" y="+5" condition="not [MIRROR]"/>
    <pos x="+265" y="+5" condition="[MIRROR]"/>
    ...
</group>
```

In local tests, the child-`<pos>` group rendered but did not move horizontally, while equivalent conditional branches with direct group `x` / `y` behaved correctly.

**Children:** Any skin element

**Example:**
```xml
<group name="Deck Controls" x="100" y="50">
    <button action="play_pause">
        <pos x="+0" y="+0"/>
    </button>
    <button action="cue">
        <pos x="+90" y="+0"/>
    </button>
</group>
```

---

### `<square>`

Vector graphics rectangle with optional rounded corners.

**Syntax:** `<square color="" radius="" visibility="">`

**Attributes:**
- `color` - Fill color (hex or predefined)
- `radius` - Corner radius in pixels
- `visibility` - VDJScript visibility condition

**Children:**
- `<pos x="" y=""/>` - Position
- `<size width="" height=""/>` - Dimensions

**Example:**
```xml
<square color="#1e7b96" radius="10">
    <pos x="100" y="50"/>
    <size width="200" height="100"/>
</square>

<!-- Dynamic visibility -->
<square color="red" radius="20" visibility="not play">
    <pos x="100" y="50"/>
    <size width="100" height="50"/>
</square>

<square color="green" radius="20" visibility="play">
    <pos x="100" y="50"/>
    <size width="100" height="50"/>
</square>
```

---

### `<circle>`

Vector graphics circle or ellipse.

**Syntax:** `<circle color="" visibility="">`

**Attributes:**
- `color` - Fill color (hex or predefined)
- `visibility` - VDJScript visibility condition

**Children:**
- `<pos x="" y=""/>` - Position
- `<size width="" height=""/>` - Dimensions (equal for circle, different for ellipse)

**Example:**
```xml
<circle color="#ffffff">
    <pos x="100" y="100"/>
    <size width="50" height="50"/>
</circle>
```

---

### `<line>`

Vector graphics line drawing.

**Syntax:** `<line color="" width="" visibility="">`

**Attributes:**
- `color` - Line color
- `width` - Line thickness in pixels
- `visibility` - VDJScript visibility condition

**Children:**
- `<pos x="" y=""/>` - Start position
- `<pos2 x="" y=""/>` - End position

**Example:**
```xml
<line color="white" width="2">
    <pos x="100" y="100"/>
    <pos2 x="200" y="150"/>
</line>
```

---

### `<video>`

Display video output.

**Syntax:** `<video source="" canstretch="">`

**Attributes:**
- `source` - Video source:
  - `"deck"` - Current deck
  - `"master"` - Master output
  - `"1"`, `"2"`, etc. - Specific deck
- `canstretch` - `"true"` to allow resizing

**Children:**
- `<pos x="" y=""/>` - Position
- `<size width="" height=""/>` - Dimensions

**Example:**
```xml
<video source="master" canstretch="true">
    <pos x="100" y="100"/>
    <size width="640" height="480"/>
</video>
```

---

### `<cover>`

Displays album art. Defaults to the calling deck's cover; `source=""` can pull
art from the browser selection, automix, karaoke, or background-music track
instead.

**Syntax:** `<cover source="" shape="" rotate="" linkdrop="" visibility="" os="" panel="" deck="">`

**Attributes:**
- `source=""` - Art source: `"browser"` (selected browser track), `"automix"`
  (track playing in the automix deck), `"automix 1"` (next automix track),
  `"karaoke"` / `"karaoke 1"` (karaoke deck / next karaoke track),
  `"backgroundmusic"`. Default: the calling deck's cover. (`Official`; no
  built-in skin uses `source=""` — they all show the enclosing deck's cover)
- `shape=""` - `"circle"` for circular art
- `rotate=""` - `"yes"` to spin the art while the deck plays (default no).
  With `rotate="yes"` and no explicit shape, the cover renders circular. This
  is the dominant built-in pattern (28 of 54 uses, jog-wheel center art)
- `linkdrop=""` - `"yes|no"`: whether dropping a video file on the cover links
  it to the loaded track. Falls back to the `videoCreateLinkOnDrop` setting
  when unspecified
- Global attributes: `visibility=""` (built-ins use both queries and constant
  opacities such as `visibility="0.7"`), `os=""`, `panel=""`, `deck=""`

**Children:**
- `<pos x="" y=""/>` - Position
- `<size width="" height=""/>` - Dimensions
- `<clipmask x="" y="" width="" height=""/>` - B&W mask image for custom shapes (`Official`)
- `<default x="" y="" width="" height=""/>` - Observed in built-in skins only:
  coordinates of a skin-image graphic, by all appearances the placeholder art
  shown when the track has no cover. Semantics not yet confirmed locally

**Example (`examples/Skins/Built-In/Lite/Lite.xml`, jog-wheel center):**
```xml
<cover rotate="yes">
    <pos x="+19" y="+26"/>
    <size width="184" height="184"/>
    <default x="1628" y="26" width="184" height="184"/>
</cover>
```

Built-in cross-check: 54 uses across 16 built-in skin files; observed
attributes are `rotate` (28), `visibility` (26), `shape="circle"` (2), and
relative `x`/`y` offsets (2).

Source: `Official` ([Skin Cover](https://virtualdj.com/wiki/Skin%20Cover.html)), `Built-in skin`, `Inference` (meaning of `<default>`)

---

### `<led>`

LED indicator that changes based on conditions.

**Syntax:** `<led brightness="">`

**Attributes:**
- `brightness` - VDJScript query for brightness level

**Children:**
- `<pos x="" y=""/>` - Position
- `<size width="" height=""/>` - Dimensions
- `<off x="" y=""/>` - Off state graphics
- `<on x="" y=""/>` - On state graphics

**Example:**
```xml
<led brightness="`get_level`">
    <pos x="100" y="100"/>
    <size width="20" height="20"/>
    <off x="0" y="400"/>
    <on x="20" y="400"/>
</led>
```

---

### `<equalizer>`

Spectrum analyzer visualization.

**Syntax:** `<equalizer nb="" type="" color="" width="" offset="" slow="" bass="" mirror="" canstretch="" visibility="" os="" panel="" deck="">`

**Attributes:**
- `nb` - Number of equalizer bars/bands
- `type` - Layout type:
  - `"horizontal"` - Linear bar layout
  - `"circle"` - Circular layout
- `color` - Equalizer graphics color
- `width` - Bar width as a fraction (`0.0`-`1.0`)
- `offset` - Circle end position (`0.0`-`1.0`, default `0.7`; circle type)
- `slow` - `"true"|"false"` smoother visual rendering
- `bass` - Bass frequency position: `"top"|"bottom"|"left"|"outside"|"middle"`
- `mirror` - `"false"|"true"` mirror from center
- `canstretch` - `"false"|"true"` maintain aspect ratio on resize
- Inherited common attributes: `visibility=""`, `os=""`, `panel=""`, `deck=""`

**Children:**
- `<pos x="" y=""/>` - Position
- `<size width="" height=""/>` - Dimensions

**Example:**
```xml
<equalizer type="horizontal" nb="32" color="#00ff00" deck="master">
    <pos x="100" y="500"/>
    <size width="800" height="100"/>
</equalizer>
```

Source: `Official` (`Skin Equalizer.html` wiki page). Not observed in any built-in skin; built-in skins draw spectra with `<visual>` types instead. An earlier revision of this section listed `type="bar|line"` and a `source=""` attribute — neither exists in the official element reference.

---

### `<browser>`

File browser interface element displaying VirtualDJ's folder tree, song list, sideview, and info panels. Browsers can be nested in panels and have customizable visibility and appearance.

**Syntax:** `<browser panel="" visibility="" toolbar="" sideview="" folders="" infos="" effects="" searchbar="" lineheight="" showzoom="">`

**Attributes:**
- `visibility=""` - Define transparency (0-100%) or VDJScript action returning true/false for conditional display
- `panel=""` - Name of panel this browser belongs to (browser only shown when panel visible). Recommended to nest browser inside `<panel>` container instead
- `toolbar=""` - Show left toolbar: `"yes"` (default) or `"no"`
- `sideview=""` - Show sideview panel: `"yes"` (default) or `"no"`
- `folders=""` - Show folder list: `"yes"` (default) or `"no"`
- `infos=""` - Show info panel: `"yes"` (default) or `"no"`
- `effects=""` - Show effects section: `"yes"` (default) or `"no"`
- `searchbar=""` - Show search toolbar above file list: `"yes"` (default) or `"no"`
- `lineheight=""` - Height multiplier between browser lines (default: 1.0). Example: `lineheight="2.0"` for double height
- `showzoom=""` - Show zoom toggle button in folder toolbar: `"yes"` or `"no"`

**Browser Zoom / Mini Layouts:**

`showzoom="yes"` exposes VirtualDJ's built-in browser zoom control in the browser toolbar. Skin XML can also react to that zoom state with the `browser_zoom` query/action. A common "mini" layout is simply a normal deck layout hidden while a browser-zoom layout is shown:

```xml
<button action="browser_zoom" query="browser_zoom">
    <size width="32" height="32"/>
</button>

<panel class="main_decks" visibility="not browser_zoom"/>
<panel class="browser_zoom_decks" visibility="browser_zoom"/>
```

Some skins also combine `browser_zoom` with `browser_isactive` for an automatic browser-focused mode:

```xml
<panel class="browser_zoom_decks" visibility="browser_zoom ? true : browser_isactive ? true : false"/>
```

Bundled Remote tablet skins use a related but separate pattern: a dedicated browser view toggled by `$rmbrowser`, with compact deck/mixer controls duplicated around the browser instead of using `browser_zoom`:

```xml
<button action="toggle '$rmbrowser'"/>
<panel name="rmdecksview" visibility="var '$rmbrowser' 0"/>
<panel name="rmbrowserview" visibility="var '$rmbrowser' 1" breakline1="432+2+2" breakline2="432+2+975-4-2">
    <browser>
        <pos x="25" y="344"/>
        <size width="2409" height="1061"/>
    </browser>
</panel>
```

Source: `Built-in skin` (`examples/Skins/Built-In/Remote/16x9T.xml`, `16x10T.xml`, `4x3T.xml`)

**Children:**
- `<pos x="" y=""/>` - Position on screen
- `<size width="" height=""/>` - Browser dimensions
- `<colors background="">` - Color customization (see below)

**Color Customization:**
The `<colors>` element has these child elements:
- `background=""` - Background color (use `"transparent"` for transparent background)
  - **Note:** With transparent background, strongly recommended to set skin `breakline` and `breakline2` to prevent stretching issues

Browser color children (all optional, VirtualDJ uses defaults if not specified):
- Various color properties for text, highlights, borders, etc. (see example)

**Example 1: Basic Browser**
```xml
<browser>
    <pos x="50" y="50"/>
    <size width="600" height="400"/>
</browser>
```

**Example 2: Browser with Custom Options**
```xml
<browser toolbar="yes" sideview="yes" folders="yes" 
         infos="yes" searchbar="yes" lineheight="1.2">
    <pos x="50" y="50"/>
    <size width="700" height="500"/>
</browser>
```

**Example 3: Browser in Panel with Visibility**
```xml
<panel name="browserpanel" visible="yes">
    <browser>
        <pos x="50" y="50"/>
        <size width="600" height="400"/>
    </browser>
</panel>
```

**Example 4: Minimal Browser (No Sidebars)**
```xml
<browser toolbar="no" sideview="no" folders="yes" 
         infos="no" effects="no" searchbar="yes">
    <pos x="100" y="100"/>
    <size width="500" height="600"/>
</browser>
```

**Example 5: Browser with Transparent Background**
```xml
<browser>
    <pos x="50" y="50"/>
    <size width="600" height="400"/>
    <colors background="transparent"/>
</browser>

<!-- In <skin> element, add breaklines: -->
<skin ... breakline="100" breakline2="550">
```

**Example 6: Browser with Custom Line Height**
```xml
<browser lineheight="1.5">
    <pos x="50" y="50"/>
    <size width="600" height="400"/>
</browser>
```

**Custom Browsers with `<split>` Panels:**
Advanced skins can replace the single `<browser>` element with smaller browser components, usually arranged with nested `<split>` panels. This is useful when the folder tree, song list, sideview, info panel, sampler, or effect GUI dock need to live in separate regions of the skin.

**Browser Sections:**
- **Folder List** - Tree view of folders and playlists
- **Song List** - Main file list with columns
- **Sideview** - Context panel showing recommendations, similar tracks, etc.
- **Info Panel** - Track information and waveform preview
- **Toolbar** - Left sidebar with navigation buttons
- **Search Bar** - Search input at top of file list
- **Effects Section** - Effect selection area

**Custom Browser Component Elements:**

| Element | Provides |
|---------|----------|
| `<folderlist>` | Folder list/tree, without the vertical folder toolbar |
| `<browsertoolbartree>` | Vertical toolbar for the folder list |
| `<fileview>` | Full songs area: file list, coverflow, and horizontal search/edit toolbar |
| `<browsertoolbar>` | Horizontal search/edit toolbar for the songs area |
| `<coverflow>` | Covers flow list |
| `<filelist>` | Songs list without coverflow and search controls |
| `<sideview>` | Full sideview area, including Automix, Sidelist, Karaoke, Sampler, Remixes, Shortcuts, list info, and bottom navigation |
| `<browserinfo>` | Default browser info area for the selected song, including the prelisten player |
| `<pluginzone>` | Dock for effect plugin GUIs |
| `<sampler>` | Sampler trigger-pad view, without the top bank/mode menu |

**Useful Decompositions:**

- `<fileview>` is the compact official element for the whole songs area.
- Replace `<fileview>` with `<browsertoolbar>`, `<coverflow>`, and `<filelist>` when you need to control the search bar, coverflow, and file list layout separately.
- Use `<filelist source="sideview">` to show the currently selected sideview list without the top menu or bottom navigation.
- Use `<filelist source="automix">`, `<filelist source="karaoke">`, `<filelist source="sidelist">`, or `<filelist source="sampler">` to pin a specific sideview list in a dedicated area.
- If a `<pluginzone>` should resize automatically when an effect GUI is docked, put it in a split named `effects`.

**Custom Browser Attributes:**

These are documented for the browser list components above:

- `attachX="left|right|both"` and `attachY="up|down|both"` - Anchor behavior when the element is inside a `<split>` panel.
- `resizeX="yes|no"` and `resizeY="yes|no"` - Whether the element resizes with its split panel area.
- `grid="yes"` - Force grid view. Without this, list elements follow the current Grid/List view selection.
- `lineheight=""` - Browser list line-height multiplier. Example: `lineheight="1.5"` is 150% of normal row height.
- `visibility=""` - `true`, `false`, or a VDJScript query controlling whether the element is displayed.

**Custom Browser Children:**

All custom browser components require only position and size children:

```xml
<pos x="" y=""/>
<size width="" height=""/>
```

They can also use optional browser colors like `<browser>`.

**Minimal Custom Browser Pattern:**

```xml
<split name="folders" type="horizontal" position="25%" grab="10">
    <pos x="0" y="0"/>
    <size width="1200" height="420"/>
    <left>
        <browsertoolbartree resizeX="no" attachX="left">
            <pos x="0" y="0"/>
            <size width="35" height="420"/>
        </browsertoolbartree>
        <folderlist resizeX="yes" attachX="both">
            <pos x="37" y="0"/>
            <size width="1200-37" height="420"/>
        </folderlist>
    </left>
    <right>
        <fileview attachX="both" attachY="both">
            <pos x="0" y="0"/>
            <size width="1200" height="420"/>
        </fileview>
    </right>
    <separator close="left" size="16" closed="no"/>
</split>
```

Official reference: [Custom Browser](https://virtualdj.com/wiki/custombrowser.html)

**Skin Breaklines:**
When using browser in skins, define breaklines in the `<skin>` element to specify where browser can stretch vertically when resizing:
```xml
<skin breakline="100" breakline2="550">
```

- **breakline** - Y-coordinate where stretching begins (top of browser)
- **breakline2** - Y-coordinate where stretching ends (bottom of browser)
- Area between breaklines will stretch; ensure no fixed-position buttons in this area
- Browser cannot be resized smaller than breakline 1 position

For desktop skins with multiple structural layouts, use top-level conditional
`<breaklines>` children when each layout needs a different stretch region:

```xml
<skin ...>
    <breaklines breakline1="675" breakline2="1000" condition="var_equal '@$skin_mode' 0"/>
    <breaklines breakline1="980" breakline2="1070" condition="var_equal '@$skin_mode' 1"/>
    ...
</skin>
```

This pattern was reported in VirtualDJ community skin-engine notes for build
7438+ and was locally confirmed in the GraveRaver desktop skin. Treat the
controlling variable as structural state: update it with `load_skin` when the
selected breakline should change.

Source: `Community`, `Local test`

Bundled Remote skins also use panel-local `breakline1` / `breakline2` attributes on full-screen browser and settings panels. This keeps the stretch region tied to the active view rather than only the root skin:

```xml
<panel name="rmbrowserview" visibility="var '$rmbrowser' 1" breakline1="90" breakline2="1476-20">
    <browser>
        <pos x="25" y="102"/>
        <size width="781" height="1272"/>
    </browser>
</panel>

<panel name="rmsettingsview" visibility="var '$rmsettings' 1" breakline1="90" breakline2="1476-10">
    ...
</panel>
```

Source: `Built-in skin` (`examples/Skins/Built-In/Remote/9x16P.xml`, `9x16T.xml`, `9x19P.xml`, `3x4T.xml`)

**Notes:**
- Browser automatically handles scrolling, sorting, filtering
- Most skins have one main browser, but multiple browsers are supported
- Use `visibility=""` attribute or nest in `<panel>` for conditional display
- Transparent backgrounds require careful breakline setup
- Custom browser colors rarely needed - VirtualDJ defaults work well

---

### `<prelisten>`

Standalone prelisten player. The prelisten controls normally live inside the
browser info area, but this element lets a skin position and style the player
anywhere.

**Syntax:** `<prelisten>`

**Attributes:** None documented.

**Children:**
- `<pos x="" y=""/>` - Position
- `<size width="" height=""/>` - Dimensions
- `<colors background="" border="" selected="" cursor="" button="" buttonbackground="" buttonselected=""/>` -
  Optional styling; when omitted, inherits from `<browser><colors><prelisten>`
  or the defaults

**Example (official wiki):**
```xml
<prelisten>
    <pos x="0" y="50"/>
    <size width="280" height="30"/>
    <colors background="#1F1F1F" border="#7A7A7A" selected="#136024"
            cursor="#18A639" button="#CBCBCB" buttonbackground="#5C5C5C"
            buttonselected="#18A639"/>
</prelisten>
```

**Do not confuse with the browser color child of the same name.** All six
built-in uses of `<prelisten>` are one-line styling children inside
`<browser><colors>`, next to `<scrollbars>`, `<info>`, and `<search>`:

```xml
<colors>
    ...
    <search background="browserback" text="textbrowser"/>
    <prelisten background="background2"/>
</colors>
```

No built-in skin uses the standalone element, so treat the standalone form as
official-doc-derived rather than locally verified.

Source: `Official` ([Skin Prelisten](https://virtualdj.com/wiki/Skin%20Prelisten.html)), `Built-in skin` (colors-child form)

---

### `<menu>`

Clickable skin object that opens a custom menu at its own hit area.

**Syntax:** `<menu>`

The official syntax has no menu-specific attributes. In normal skin code, position and size are defined with child elements, and shared skin attributes such as `visibility`, `deck`, `panel`, and `class` can be used in the same style as other skin objects.

**Children:**
- `<pos x="" y=""/>` - Position of the menu hit area
- `<size width="" height=""/>` - Width and height of the menu hit area
- `<item text="" action="" check="" hascheck="" visibility=""/>` - Menu item
- `<separator/>` - Separator line
- `<submenu text="">` - Nested menu containing `<item>`, `<separator>`, or more `<submenu>` elements

**Menu Item Attributes:**
- `text=""` - Displayed item label. `text="-"` is also accepted by the official docs as a separator-style item, though `<separator/>` is clearer.
- `action=""` - VDJScript action executed when the item is clicked
- `check=""` - VDJScript query that controls the check mark
- `hascheck=""` - Set to `"false"` to suppress check marks
- `visibility=""` - VDJScript query that shows/hides the item

**Graphics States:**
- `<up>` / `<off>` - Normal state graphic
- `<over>` - Mouse hover graphic
- `<down>` / `<selected>` - Graphic while the menu is open
- `<icon>` and `<text>` can be used for simple overlays, following the same general button/text conventions used elsewhere in skins.

**Confirmed Behavior Notes:**
- `<menu>` opens when its own area is clicked. It is not opened by a separate VDJScript action by name, and it is not a right-click-only object.
- To open a built-in VirtualDJ menu from right-click, use a button or slider with `rightclick=""` and the relevant built-in action, for example `deck_options`, `browser_options`, `info_options`, `loop_options`, `pad_menu`, `pad_page_select 1`, `effect_select 1`, or `sampler_options`.
- To make a custom right-click UI, use `rightclick="skin_panel 'panel_name' on"` and implement the custom popup as a panel with buttons. This is a skin-level workaround, not the same as the native menu object.

**Example: Custom Menu Object**
```xml
<menu tooltip="Waveform Options">
    <pos x="140" y="4"/>
    <size width="22" height="24"/>
    <icon sysicon="settings" height="24" width="24" color="textoff" colorover="needle" colordown="needle"/>

    <submenu text="Waveform Type" localize="true">
        <item text="Colors" localize="true" action="setting 'skinwaveformScratchType' 'colors'" check="setting 'skinwaveformScratchType' 'colors'"/>
        <item text="Shapes" localize="true" action="setting 'skinwaveformScratchType' 'shapes'" check="setting 'skinwaveformScratchType' 'shapes'"/>
    </submenu>
    <separator/>
    <item text="Show Gridlines" localize="true" action="setting 'showGridlines'" check="setting 'showGridlines'"/>
</menu>
```

**Example: Right-click to Built-in Menu**
```xml
<button action="search" rightclick="search_options">
    <pos x="350" y="2"/>
    <size width="30" height="28"/>
    <icon sysicon="search" width="24" height="24"/>
</button>
```

Official reference: [Skin menu](https://www.virtualdj.com/wiki/Skin%20menu.html)

---

### `<window>`

Create a separate popup window.

**Syntax:** `<window name="" visible="">`

**Attributes:**
- `name` - Window identifier
- `visible` - Initial visibility: `"yes"` or `"no"`

**Children:** Any skin element

**Example:**
```xml
<window name="effects" visible="no">
    <size width="400" height="300"/>
    <!-- Window contents -->
</window>
```

---

## Root-Level Support Elements

Non-visual, window-level, or one-line elements placed directly under `<skin>`.
Built-in skins put `<copyright>` and `<font>` immediately after the `<skin>`
open tag and the `<oninit>` block at the very end of the file, but position in
the file is a convention, not a requirement.

### `<oninit>` / `<onload>`

Runs a VDJScript action once when the skin initializes (loads or reloads).
`onload` is the official alias of `oninit`; built-in skins use both names
interchangeably.

**Syntax:** `<oninit action=""/>`

**Attributes:**
- `action=""` - VDJScript action to perform. Chain multiple actions with `&`,
  or simply declare several `<oninit>` elements (built-in skins do the latter)
- `condition=""` - Observed on built-in `<onload>` elements only: standard
  structural condition evaluated at load time, e.g. layout-variable checks
  (`Built-in skin`, `examples/Skins/Built-In/Desktop/Vertical.xml`)

**Children:** None.

**Built-in patterns.** Desktop skins end with a block of `setting_setdefault`
calls so the skin can express its preferred defaults without overwriting the
user's explicit choices (`examples/Skins/Built-In/Desktop/Pro.xml`, end of file):

```xml
<oninit action="setting_setdefault skinWaveformType 'shapes'"/>
<oninit action="setting_setdefault coverflow 'no'"/>
<oninit action="setting_setdefault browserPadding 25%"/>
<oninit action="setting_setdefault EqMode 'modernEQ'"/>
<oninit action="setting_setdefault autoBPMMatch 'smart'"/>
<oninit action="setting_setdefault autoKey on"/>
<oninit action="setting_setdefault smartPlay off"/>
<oninit action="setting_setdefault autoPitchLock off"/>
```

Remote skins reset view variables (`<oninit action="set '$rmsettings' 0"/>`),
and `Vertical.xml` uses conditional `<onload>` rows to derive one variable
from others at load time:

```xml
<onload action="set '$singlerack' 0"/>
<onload action="set '$singlerack' 1"
        condition="var_equal '@$decklayout' 1 && var_not_equal '@$4decks' 0"/>
```

Built-in cross-check: 42 `<oninit>` uses in 13 files plus 27 `<onload>` uses
in 3 files.

Source: `Official` ([Skin OnInit](https://virtualdj.com/wiki/Skin%20OnInit.html)), `Built-in skin`

### `<font>` and Browser Font Variants

Sets the default typeface for the skin, or for the browser area when nested
inside `<browser>` (built-in skins put the variants inside their browser
define, next to `<colors>`).

**Syntax:** `<font name="Arial" size="20" weight="bold"/>`

**Attributes:**
- `name=""` (or `font=""`) - Typeface name
- `size=""` - Font size
- `weight=""` - `"bold"` for bold

**Children:** None.

**Variants.** The official docs list specialized elements with the same
attributes, except they use `font=""` instead of `name=""` for the typeface:

| Element | Scope | Built-in uses |
| --- | --- | --- |
| `<font>` | Skin default / browser list text | 22 |
| `<fontsearch>` | Browser search box and edit controls | 6 |
| `<fontheader>` | Browser header text | 6 |
| `<fontgridtitle>` | Browser grid titles | 6 |
| `<fonttoolbar>` | Browser toolbar labels | 6 |
| `<fontplugins>` | Plugin-related text | 0 |

**Built-in pattern.** Every bundled desktop skin declares
`<font name="Arial"/>` as the second or third root element, then sizes the
browser fonts inside its browser define:

```xml
<font name="Arial" size="20"/>
<fontsearch size="18"/>
<fontheader size="16"/>
<fontgridtitle size="18"/>
<fonttoolbar size="14"/>
```

Built-in skins only ever set `name="Arial"` and `size=""`; `weight=""` and the
variants' `font=""` attribute are official-doc-only so far.

Source: `Official` ([Skin Font](https://virtualdj.com/wiki/Skin%20Font.html)), `Built-in skin`

### `<customicons>`

Overrides the default icon sprite with a grid of custom icons, either from a
separate PNG in the skin zip or from a region of the main skin image.

**Syntax:** `<customicons file="" x="" y="" iconsize="" nb="" nbx=""/>`

**Attributes:**
- `file=""` - Optional image filename inside the skin zip; when omitted, the
  icons are read from the skin image
- `x=""` `y=""` - Top-left corner of the icon grid in the image
- `iconsize=""` - Width/height of each icon cell in pixels (default 64)
- `nb=""` - Total number of icons in the grid
- `nbx=""` - Number of columns (rows are computed as `nb/nbx`)
- `condition=""` - Structural condition (built-in pattern below)

**Children:** None.

To override only some icons, supply a grid with transparent cells for the
icons you want to keep; missing icons fall back to the defaults. Icons
referenced by `sysicon` name stay recolorable and resizable (see
[Default Icons](#default-icons)).

**Built-in pattern.** The four big desktop skins each ship one conditional
override that swaps the icon sprite for the light "daylight" color scheme:

```xml
<customicons file="icons_daylight.png" nb="64" nbx="16"
             condition="var_equal '@$colorscheme' 2"/>
```

Note the built-ins omit `x=""`, `y=""`, and `iconsize=""` when using a
dedicated file, even though the official page marks the coordinates as
required; the file's grid evidently starts at the origin with the default cell
size.

Source: `Official` ([Skin CustomIcons](https://virtualdj.com/wiki/Skin%20CustomIcons.html)), `Built-in skin`

### `<background>` (root level)

Fills the skin window background, either by tiling a region of the skin image
or with a flat color. No official wiki page is known for this element; the
details below are derived from built-in skins (24 root-level uses across 16
files).

**Tiling form (the standard desktop-skin window background):**

```xml
<background x="1817" y="0" width="100" height="100" repeat="true"/>
```

- `x=""` `y=""` `width=""` `height=""` - Region of the skin image to use as the tile
- `repeat=""` - `"true"` to tile the region across the window
- `condition=""` - Structural condition; `Pro.xml` selects one of four tiles
  by color scheme:

```xml
<background x="1817" y="0"   width="100" height="100" repeat="true" condition="var_equal '@$colorscheme' 0"/>
<background x="1817" y="210" width="100" height="100" repeat="true" condition="var_equal '@$colorscheme' 1"/>
<background x="1817" y="106" width="100" height="100" repeat="true" condition="var_equal '@$colorscheme' 2"/>
<background x="1817" y="312" width="100" height="100" repeat="true" condition="var_equal '@$colorscheme' 3"/>
```

**Color/border form (nested):** inside container defines, `<background>` acts
as a flat fill with optional borders. Every bundled desktop skin's browser
define starts with:

```xml
<background color="browserback" bordercolortop="bordercolor"
            bordercolor="bordercolor" bordersize="1"/>
```

Observed nested attributes: `color=""`, `shape="square"`, `bordercolor=""`,
`bordercolortop=""`, `bordersize=""`. Most nested uses (81) are inside
waveform `<overlay>` blocks — see [Skin Waveforms](Skin%20Waveforms.md) for
that family.

Attribute semantics beyond the patterns above are not yet confirmed; no
official page has been found to cross-check against.

Source: `Built-in skin`

### `<dialogs>`

Selects whether native VirtualDJ dialogs and popups follow a dark or light
style to match the skin. No official wiki page is known; derived from 10 uses
in 6 built-in skins.

**Syntax:** `<dialogs darkmode="true|false"/>`

**Attributes:**
- `darkmode=""` - `"true"` or `"false"`
- `condition=""` - Structural condition; the desktop skins pair two
  declarations with the color-scheme variable:

```xml
<dialogs darkmode="true"  condition="var_not_equal '@$colorscheme' 2"/>
<dialogs darkmode="false" condition="var_equal '@$colorscheme' 2"/>
```

**Children:** None.

Source: `Built-in skin`

### `<copyright>`

Copyright metadata for the skin. Unlike most skin elements it takes text
content, not attributes, and every built-in skin declares it as the first
child of `<skin>`:

```xml
<skin name="VirtualDJ • Lite" version="2020" ...>
<copyright>Atomix Productions</copyright>
<font name="Arial"/>
```

No attributes are observed (16 uses in 16 built-in files, all identical in
form). No official wiki page is known; where the text surfaces in the UI is
not yet confirmed.

Source: `Built-in skin`

### `<logo>`

Places the VirtualDJ logo. Note the official warning: the logo has a minimum
size defined by the skin resolution, so a size that looks fine at high
resolution can cause issues at lower resolutions.

**Syntax:** `<logo circle="" os="">`

**Attributes:**
- `circle=""` - `"true"` renders the logo inside a red circular boundary
  (default `"false"`)
- Global attributes: `visibility=""`, `os=""`, `panel=""`

**Children:**
- `<pos x="" y=""/>` - Position
- `<size width="" height=""/>` - Dimensions

**Built-in pattern.** 23 uses in 16 files, all plain `<logo>` with `<pos>` and
`<size>`; the desktop skins declare one per OS-specific top bar so the logo
sits opposite the window buttons (`examples/Skins/Built-In/Desktop/Pro.xml`):

```xml
<group name="applicationbuttons" condition="is_mac">
    <logo>
        <pos x="1920-115" y="8"/>
        <size width="115" height="27"/>
    </logo>
    ...
</group>
<group name="applicationbuttons" condition="is_pc">
    <logo>
        <pos x="10" y="8"/>
        <size width="115" height="27"/>
    </logo>
    ...
</group>
```

`circle=""` is official-doc-only so far (no built-in use).

Source: `Official` ([Skin Logo](https://virtualdj.com/wiki/Skin%20Logo.html)), `Built-in skin`

### `<grabzone>`

Area the user can drag to move the VirtualDJ window when it is not maximized.
If no grabzone is defined, any area not covered by a defined element acts as
one — so skins that cover the whole window with elements need explicit
grabzones to stay movable.

**Syntax:** `<grabzone>`

**Attributes:** None.

**Children:**
- `<pos x="" y=""/>` - Position
- `<size width="" height=""/>` - Dimensions

**Built-in pattern.** 28 uses in 7 files. Desktop skins declare four thin
zones along the window edges (`examples/Skins/Built-In/Desktop/Pro.xml`):

```xml
<grabzone>
    <pos x="0" y="0"/>
    <size width="1920" height="48"/>
</grabzone>
<grabzone>
    <pos x="0" y="0"/>
    <size width="15" height="1080"/>
</grabzone>
<grabzone>
    <pos x="0" y="1080-15"/>
    <size width="1920" height="15"/>
</grabzone>
<grabzone>
    <pos x="1920-15" y="0"/>
    <size width="15" height="1080"/>
</grabzone>
```

Source: `Official` ([Skin GrabZone](https://virtualdj.com/wiki/Skin%20GrabZone.html)), `Built-in skin`

### `<resizezone>`

Area that resizes the VirtualDJ window when it is not maximized, typically a
small square in the bottom-right corner.

**Syntax:** `<resizezone>`

**Attributes:** None.

**Children:**
- `<pos x="" y=""/>` - Position
- `<size width="" height=""/>` - Dimensions

**Example (official wiki):**
```xml
<resizezone>
    <pos x="1920-20" y="1080-20"/>
    <size width="20" height="20"/>
</resizezone>
```

No built-in skin uses `<resizezone>` (0 uses), so treat it as
official-doc-derived rather than locally verified.

Source: `Official` ([Skin ResizeZone](https://virtualdj.com/wiki/Skin%20ResizeZone.html))

---

## Global Element Attributes

These attributes can be applied to most elements:

| Attribute | Description | Values |
|-----------|-------------|--------|
| `visibility` | Show/hide based on condition | VDJScript query |
| `deck` | Target deck | `"1"`, `"2"`, `"left"`, `"right"`, `"master"` |
| `panel` | Parent panel name | panel name |
| `os` | OS-specific display | `"windows"`, `"mac"` |
| `canstretch` | Allow stretching on resize | `"true"`, `"false"` |

---

## Position & Size

### Position Element: `<pos>`

```xml
<pos x="100" y="200"/>
```

- Absolute: `x="100"` `y="200"`
- Relative: `x="+50"` `y="-25"` (relative to parent)
- Calculated: `x="1920-330"` `y="1080/2"`

### Size Element: `<size>`

```xml
<size width="300" height="150"/>
```

- Fixed: `width="300"` `height="150"`
- Calculated: `width="1920-50"` `height="1080/2"`

---

## Graphics References

Graphics are referenced by coordinates in the PNG file:

### Button States
- `<up x="" y=""/>` - Default up state
- `<down x="" y=""/>` - Pressed state
- `<on x="" y=""/>` - Active/on state
- `<off x="" y=""/>` - Inactive/off state
- `<over x="" y=""/>` - Mouse hover state
- `<selected x="" y=""/>` - Selected state

### Visual States
- `<off x="" y=""/>` - Low/minimum value
- `<on x="" y=""/>` - High/maximum value

---

## Predefined Colors

Colors can be specified as:
- Hex: `"#FF0000"` or alpha-first ARGB `"#40FF0000"` for semi-transparent red
- RGB: `"255,0,0"`
- Named: `"red"`, `"white"`, `"blue"`, etc.
- Defined: Use `<define color="" value="">` to create custom color names. Add `deck=""` when the same color name should resolve differently by deck in direct XML color fields.

### Dynamic Color Rules

Human-friendly rule of thumb:
- `source=` is for actions that return a color. Example: `<visual type="color" source="cue_color 1"/>`
- `color=` is for a color value. If you want to run VDJScript there, wrap the action in backticks. Example: ``<text color="`get_key_color`"/>``
- `border=` behaves like a static color field in practice. Dynamic border colors are not currently supported, so do not rely on `border="cue_color 1"` or `border="`cue_color 1`"` working on buttons.
- `query=` changes the button's `on/off` graphics state. It does not automatically use the `selected` state.
- Skin-defined color names are replaced only in XML fields that directly expect color values. They are not available inside VDJScript color actions.
- In reusable classes, explicitly deck-scope deck-sensitive dynamic color predicates, for example `deck [DECK] masterdeck ? ...`.

What we know for sure from official docs and staff replies:
- `visual type="color"` is specifically designed to render a color returned by its `source=` action. Official reference: [VirtualDJ Skin SDK Visual](https://virtualdj.com/wiki/skinsdkvisual.html)
- The official color docs distinguish between attributes that expect an action and attributes that expect a color value. `source=` expects an action that returns a color; `color=` expects a value and needs backticks around any action. Official reference: [Skin Default Colors](https://www.virtualdj.com/wiki/Skin%20Default%20Colors.html)
- Button `border=` does not support dynamic colors according to VirtualDJ CTO Adion. Official reference: [Border Color using placeholder](https://virtualdj.com/forums/242871/VirtualDJ_Skins/Border_Color_using_placeholder.html)
- VirtualDJ Development Manager djdad recommends a single `<text>` with dynamic `color` when the text color itself needs to change. Official reference: [Skin text action; visibility or visual?](https://www.virtualdj.com/forums/267953/VirtualDJ_Skins/Skin_text_action%3B_visibility_or_visual%3F.html)
- VirtualDJ staff says defined skin colors can be used in XML color fields, but not inside scripts such as `` color="`play ? color 'green' : color 'my_defined_color'`" ``. Official forum reference: [On the use of colour defines](https://virtualdj.com/forums/265321/VirtualDJ_Skins/On_the_use_of_colour_defines.html)

Practical implication for hot cue colors:
- If `cue_color` works in a `visual type="color"` but fails on a button border, that is expected behavior based on the official implementation notes above.
- If a dynamic color appears black where a cue color was expected, that usually means the attribute accepted a literal color value but did not evaluate the action in that location. This is an inference from the documented behavior above, not an explicit SDK statement.
- If a dynamic text color needs a custom skin color, either use the literal/predefined color value inside the script or split the element into `visibility=""` branches so each branch can use `color="my_defined_color"` directly.

Verified locally in this workspace:
- ``<text color="`cue_color [INDEX]`">`` renders the current cue color correctly inside a button.
- `<visual type="color" source="cue_color [INDEX]">` renders the current cue color correctly, including when used inside a reusable class instantiated via `<panel class="..."/>`.
- Button `border=` still does not render the cue color dynamically in the same mini-cue tests, which matches the official limitation above.
- In GraveRaver's `SYNC_INFO_EXTENDED` class, ``<text color="`deck [DECK] masterdeck ? color 'orange' : color 'white'`" .../>`` works for masterdeck-aware BPM text.

Examples:

```xml
<!-- Direct color-returning action; color= needs backticks. -->
<text color="`get_key_color`" action="get_key"/>

<!-- Dynamic text color with explicit deck scope inside a reusable class. -->
<text color="`deck [DECK] masterdeck ? color 'orange' : color 'white'`"
      action="get_bpm"/>

<!-- Literal hex values are fine inside the color action. -->
<text color="`loaded ? color '#FF7F00' : color '#FFFFFF'`"
      action="get_bpm"/>

<!-- Do not do this; defined color names are not script variables. -->
<text color="`masterdeck ? color 'color_masterdeck' : color 'white'`"
      action="get_bpm"/>
```

Recommended workaround for mini hot cue buttons:
- If you want a cue-colored mini button, use a `visual type="color"` as the color layer and place a transparent or semi-transparent button on top for click handling, hover state, and text.

Example:
```xml
<define class="MINI_CUE_BUTTON" placeholders="*index,*width=20,*height=20">
  <visual type="color" source="cue_color [INDEX]" visibility="has_cue [INDEX] ? constant 0.6">
    <size width="[WIDTH]" height="[HEIGHT]"/>
  </visual>
  <button action="hot_cue [INDEX]" rightclick="cue_name [INDEX]">
    <size width="[WIDTH]" height="[HEIGHT]"/>
    <off color="#99000000" border="transparent" border_size="1" radius="5"/>
    <over color="#99000000" border="transparent" border_size="1" radius="5"/>
    <text fontsize="12" color="`cue_color [INDEX]`" align="center" text="[INDEX]"/>
  </button>
</define>
```

This example is based on local verification in this workspace, not on an official SDK sample.

---

## Default Icons

VirtualDJ provides built-in icons for common functions. Some are available through an explicit `sysicon` name on an `<icon>` element or on a skin class that forwards a `sysicon` placeholder. Others are only reachable indirectly: VirtualDJ chooses the icon from the button's action name. Do not assume every icon shown on the official default-icons sprite has a usable `sysicon` string.

```xml
<button action="play_pause">
    <pos x="100" y="100"/>
    <size width="40" height="40"/>
    <!-- VirtualDJ can infer the default play/pause icon from the action. -->
</button>

<button action="settings">
    <pos x="150" y="100"/>
    <size width="40" height="40"/>
    <icon sysicon="settings" width="24" height="24"/>
</button>
```

Source: [VirtualDJ Skin Default Icons](https://www.virtualdj.com/wiki/Skin%20Default%20Icons.html), plus local skin examples.

### Explicit `sysicon` Names

The official default-icons page lists these names as explicit `sysicon` values:

| `sysicon` | Icon |
| --- | --- |
| `search` | Browser search |
| `headphones` | Browser prelisten / headphones |
| `settings` | Settings |
| `arrowleft` | Left arrow |
| `arrowright` | Right arrow |
| `add_favoritefolder` | Add favorite folder |
| `add_virtualfolder` | Add virtual folder |
| `add_filterfolder` | Add filter folder |
| `sampler_drop` | Sampler drop sample |
| `sampler_loop` | Sampler loop sample |
| `sampler_mic` | Sampler mic record sample |
| `chevronup` | Chevron up |
| `chevrondown` | Chevron down |
| `chevronleft` | Chevron left |
| `chevronright` | Chevron right |
| `minimize` | Minimize |
| `maximize` | Maximize / fullscreen / windowed maximize |
| `close` | Close |
| `stop` | Stop |
| `stop_button` | Stop button |
| `play_pause` | Play / pause |
| `play` | Play / stutter |

Local official-skin examples also use `play_button`, which is not listed as a separate `sysicon` on the wiki but appears in bundled skin XML.

### Action-Name Icons

Some default icons are reached by using the action itself, either as the button `action` or, in tested skins, as the `sysicon` value. The official page lists these as action-backed icons:

| Action | Icon |
| --- | --- |
| `browser_options 'le'` | Info / question |
| `sampler_bank -1` | Left arrow |
| `sampler_bank +1` | Right arrow |
| `sampler_mode -1` | Left arrow |
| `sampler_mode +1` | Right arrow |
| `goto_last_folder` | Previous folder / back |
| `grid_view` | Browser grid view |
| `show_splitpanel 'sideview'` | Show sideview |
| `show_splitpanel 'info'` | Show info browser |
| `show_splitpanel 'effects'` | Show FX browser |
| `view_options 'showmusic'` | Show / hide audio files |
| `view_options 'showvideo'` | Show / hide video files |
| `view_options 'showkaraoke'` | Show / hide karaoke files |
| `font_size -` | Browser font smaller |
| `font_size +` | Browser font larger |
| `effect_dock_gui` | Pin FX GUI |
| `effect_show_gui` | Close / show FX GUI |
| `browser_zoom` | Browser zoom |
| `sideview 'automix'` | Sideview automix |
| `sideview 'sidelist'` | Sideview sidelist |
| `sideview 'sampler'` | Sideview sampler |
| `sideview 'karaoke'` | Sideview karaoke |
| `sideview 'clone'` | Sideview clone |
| `sideview 'remixes'` | Sideview remixes |
| `quick_filter` | Quick filter |
| `automix` | Automix on/off |
| `karaoke` | Karaoke on/off |
| `sampler_bank` | Sampler bank |
| `sideview_triggerpad` | Sampler trigger pad view |
| `sampler_mode` | Sampler trigger mode |
| `sampler_mode 'on/off'` | Sampler trigger mode on/off |
| `sampler_mode 'hold'` | Sampler trigger mode hold |
| `sampler_mode 'stutter'` | Sampler trigger mode stutter |
| `sampler_mode 'unmute'` | Sampler trigger mode unmute |

Many rows in the default-icons table are browser file/folder state icons or overlays and are marked `N/A`; those should be treated as internal browser icons, not reachable skin `sysicon` names.

---

## Best Practices

### Organization
- Use `<define>` for repeated elements
- Group related elements in `<deck>` or `<group>` containers
- Use descriptive `name` attributes for debugging

### Graphics
- Use transparent PNG with alpha channel
- Organize graphics efficiently in sprite sheet
- Use vector shapes (`<square>`, `<circle>`) to reduce file size

### Performance
- Minimize use of complex visuals
- Use vector shapes where possible
- Keep image file size reasonable

### Visibility
- Use `visibility` attribute for conditional display
- Use `<panel>` for show/hide groups
- Use `<stack>` for smooth transitions

---

## Example: Complete Button Definition

```xml
<define class="playbutton">
    <size width="80" height="45"/>
    <off x="0" y="200"/>
    <on x="80" y="200"/>
    <over x="160" y="200"/>
    <text font="Arial" fontsize="12" color="white" text="PLAY" align="center"/>
</define>

<deck deck="left">
    <button class="playbutton" action="play_pause">
        <pos x="100" y="100"/>
    </button>
</deck>

<deck deck="right">
    <button class="playbutton" action="play_pause">
        <pos x="900" y="100"/>
    </button>
</deck>
```

---

## Additional Resources

- **VirtualDJ Manual**: https://www.virtualdj.com/manuals/virtualdj.html
- **VDJScript Reference**: See VDJScript Verbs document
- **Skin Examples**: Extract default skin from Settings > Interface
- **Forums**: https://www.virtualdj.com/forums/

---

## Notes

- Skin files must be zipped with `.zip` extension
- XML file and PNG file should have matching names (or use `image=""` attribute)
- Test on multiple screen resolutions
- Backup original skin before modifying
- Use VirtualDJ's skin creator for visual editing
