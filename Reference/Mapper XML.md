# VirtualDJ Mapper XML

Reference for VirtualDJ controller and keyboard mapper files.

Mappers live in `~/Library/Application Support/VirtualDJ/Mappers/` on macOS.
Each mapper is an XML file targeting a specific controller, MIDI device, or keyboard.

Source labels used below match the rest of this repo:
`Official`, `Official forum`, `Community`, `Published skin`, `Built-in skin`, `Published pad page`, `Built-in pad page`, `Local test`, `Inference`.

---

## File Structure

A mapper file is a single XML document with a root `<mapper>` element.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mapper>
  <map .../>
  <button .../>
  <slider .../>
  <knob .../>
  <fader .../>
  ...
</mapper>
```

VirtualDJ ships built-in mappers for supported controllers inside the application bundle at:
`/Applications/VirtualDJ.app/Contents/Resources/Mappers/`

User mappers override or extend built-in ones.

For controller devices with a separate device definition, mapper files commonly use `<map value="CONTROL_NAME" action="..."/>` entries that target the named controls declared by the definition. In that split, the device definition declares the hardware I/O and the mapper supplies the VDJScript.

Source: `Official`, `Local observation`

---

## Mapper XML vs Device Definition XML

Mapper actions are VDJScript. Device definitions are not.

Use the device definition XML to declare how VirtualDJ talks to the hardware: input buttons, sliders, MIDI notes, CC numbers, LED outputs, bars, channels, and static value ranges. Do not expect VDJScript variables, conditionals, backticks, or actions to be evaluated inside device definition elements such as `<button>`, `<led>`, `cc=""`, `value=""`, `ccoff=""`, or `zero=""`.

Put dynamic behavior in the mapper instead:

```xml
<!-- Device definition: static hardware output declarations -->
<led name="LED_CC_000" cc="0x00" channel="0"/>
<led name="LED_CC_001" cc="0x01" channel="0"/>

<!-- Mapper: VDJScript decides which output is active -->
<map value="LED_CC_000" action="var_equal 'CCOut' 0"/>
<map value="LED_CC_001" action="var_equal 'CCOut' 1"/>
```

Source: `Official forum`

---

## Root `<mapper>` Attributes

| Attribute | Description | Example | Source |
| --- | --- | --- | --- |
| `name` | Display name shown in the controller setup UI | `name="DDJ-FLX4"` | `Official` |
| `author` | Mapper author name | `author="monomadic"` | `Official` |
| `version` | Mapper version string | `version="1.0"` | `Official` |
| `device` | Target device name (must match the connected device name) | `device="DDJ-FLX4"` | `Official` |
| `class` | Device class: `controller`, `keyboard`, `midi` | `class="controller"` | `Official` |
| `channel` | Default MIDI channel (0-15; 0 = any) | `channel="0"` | `Official` |

---

## Input Elements

### `<button>`

Maps a button, pad, or key press to one or more VDJScript actions.

```xml
<button note="36" channel="1" deck="1" action="cue_stop"/>
```

| Attribute | Description | Source |
| --- | --- | --- |
| `note` | MIDI note number (0-127) | `Official` |
| `channel` | MIDI channel (1-16; overrides mapper default) | `Official` |
| `deck` | Target deck: `1`, `2`, `3`, `4`, `left`, `right`, `master`, `active` | `Official` |
| `action` | VDJScript action to run on press | `Official` |
| `shift` | Action to run when the shift modifier is held | `Official` |
| `type` | Button type: `trigger` (default), `toggle`, `hold` | `Official` |

**`type` values:**

- `trigger` — fires once on press
- `toggle` — alternates between on and off states
- `hold` — fires while held, releases on up

### `<slider>`

Maps a continuous controller (CC) to a VDJScript action that accepts a percentage.

```xml
<slider cc="48" channel="1" deck="1" action="volume"/>
```

| Attribute | Description | Source |
| --- | --- | --- |
| `cc` | MIDI continuous controller number (0-127) | `Official` |
| `channel` | MIDI channel | `Official` |
| `deck` | Target deck | `Official` |
| `action` | VDJScript action — must accept a `%` parameter | `Official` |
| `shift` | Shift-action | `Official` |
| `min` | Minimum output value (default `0%`) | `Official` |
| `max` | Maximum output value (default `100%`) | `Official` |
| `invert` | `yes` to flip the direction | `Official` |

### `<knob>`

Maps a relative or absolute encoder to a VDJScript action.

```xml
<knob cc="54" channel="1" deck="1" action="eq_high" relative="yes"/>
```

| Attribute | Description | Source |
| --- | --- | --- |
| `cc` | MIDI CC number | `Official` |
| `channel` | MIDI channel | `Official` |
| `deck` | Target deck | `Official` |
| `action` | VDJScript action | `Official` |
| `shift` | Shift-action | `Official` |
| `relative` | `yes` for relative (jogwheel/encoder) CC messages | `Official` |
| `sensitivity` | Multiplier for relative movement | `Official` |

### `<fader>`

Alias for `<slider>` with common default settings for crossfader and channel faders.

```xml
<fader cc="14" channel="1" action="crossfader"/>
```

### `<jogwheel>`

Dedicated element for jog wheel control. Handles scratch vs. pitch-bend mode.

```xml
<jogwheel cc="33" channel="1" deck="1" scratch="yes" scratchcc="34"/>
```

| Attribute | Description | Source |
| --- | --- | --- |
| `cc` | CC for pitch-bend (touch-off) movement | `Official` |
| `scratchcc` | CC for scratch (touch-on) movement | `Official` |
| `scratch` | `yes` to enable scratch mode when touched | `Official` |
| `channel` | MIDI channel | `Official` |
| `deck` | Target deck | `Official` |

---

## Deck Targeting

The `deck=""` attribute on any input element sets which deck the action targets.

| Value | Meaning |
| --- | --- |
| `1` / `2` / `3` / `4` | Fixed deck |
| `left` | Left deck in the current layout |
| `right` | Right deck in the current layout |
| `master` | Master deck |
| `active` | The deck currently in focus / last touched |

Source: `Official`

---

## Shift Modifier

VirtualDJ mappers support a global shift button. When the shift button is held,
`shift=""` attribute values fire instead of `action=""` values.

Declare the shift button:

```xml
<button note="63" channel="1" action="shift"/>
```

Use it on other elements:

```xml
<button note="36" channel="1" deck="1" action="cue_stop" shift="cue_loop"/>
```

Multiple shift layers can be named:

```xml
<button note="63" channel="1" action="shift 'layer2'"/>
<button note="36" channel="1" deck="1" action="play" shift_layer2="loop 4bt"/>
```

Source: `Official`, `Inference`

---

## LED Feedback

Controller buttons with LEDs are driven by a `query=""` attribute.
VirtualDJ evaluates the query continuously and sends a Note On/Off to the same note when it changes.

```xml
<button note="36" channel="1" deck="1" action="cue_stop" query="cue_stop"/>
```

The query follows the same VDJScript rules as skin `query=""` attributes.

For multi-color LEDs (e.g. cue point color feedback):

```xml
<button note="40" channel="1" deck="1"
        action="goto_cue 1"
        query="cue_pos 1 ? cue_color 1 : off"/>
```

Source: `Official`, `Inference`

---

## Keyboard Mappers

Keyboard mappers use `key=""` instead of `note=""` / `cc=""`.

```xml
<mapper class="keyboard">
  <button key="space" action="play_pause" deck="active"/>
  <button key="left"  action="pitch -1%" deck="active"/>
  <button key="right" action="pitch +1%" deck="active"/>
  <button key="up"    action="eq_high +10%" deck="active"/>
</mapper>
```

Key names are standard keyboard identifiers: `space`, `return`, `escape`, `left`, `right`, `up`, `down`,
`a`–`z`, `0`–`9`, `f1`–`f12`.

Modifiers: prefix with `ctrl+`, `shift+`, `alt+`, `cmd+` (macOS).

```xml
<button key="ctrl+left" action="loop_half" deck="active"/>
```

Source: `Official`, `Inference`

---

## Common Patterns

### Deck-paired layout (two-deck controller)

```xml
<mapper name="Example Two-Deck" class="controller">

  <!-- Deck 1 (left side, channel 1) -->
  <button note="11" channel="1" deck="1" action="play_pause" query="play"/>
  <button note="12" channel="1" deck="1" action="cue_stop"   query="cue_stop"/>
  <slider cc="19"   channel="1" deck="1" action="volume"/>
  <knob   cc="21"   channel="1" deck="1" action="eq_high" relative="yes"/>
  <knob   cc="22"   channel="1" deck="1" action="eq_mid"  relative="yes"/>
  <knob   cc="23"   channel="1" deck="1" action="eq_low"  relative="yes"/>

  <!-- Deck 2 (right side, channel 2) -->
  <button note="11" channel="2" deck="2" action="play_pause" query="play"/>
  <button note="12" channel="2" deck="2" action="cue_stop"   query="cue_stop"/>
  <slider cc="19"   channel="2" deck="2" action="volume"/>
  <knob   cc="21"   channel="2" deck="2" action="eq_high" relative="yes"/>
  <knob   cc="22"   channel="2" deck="2" action="eq_mid"  relative="yes"/>
  <knob   cc="23"   channel="2" deck="2" action="eq_low"  relative="yes"/>

  <!-- Crossfader (channel 1) -->
  <fader cc="14" channel="1" action="crossfader"/>

</mapper>
```

### Hot cue pads (8 pads, one deck)

```xml
<button note="36" channel="1" deck="1"
        action="cue_pos 1 ? goto_cue 1 : cue_select 1 &amp; cue"
        shift="cue_select 1 &amp; cue_delete"
        query="cue_pos 1 ? cue_color 1 : off"/>
<button note="37" channel="1" deck="1"
        action="cue_pos 2 ? goto_cue 2 : cue_select 2 &amp; cue"
        shift="cue_select 2 &amp; cue_delete"
        query="cue_pos 2 ? cue_color 2 : off"/>
```

---

## Relationship to Pad Pages

Pad pages (`Pads/*.xml`) and mapper files are separate systems with a shared scripting language.

| | Pad pages | Mapper files |
| --- | --- | --- |
| **Triggered by** | On-screen pads in VirtualDJ UI | Physical controller hardware |
| **File location** | `Pads/*.xml` | `Mappers/*.xml` |
| **Root element** | `<page>` | `<mapper>` |
| **Input elements** | `<pad1>` … `<pad16>`, `<param1>`, `<param2>` | `<button>`, `<slider>`, `<knob>`, `<fader>` |
| **Scripting** | VDJScript in element content and attributes | VDJScript in `action=`, `shift=`, `query=` |
| **LED feedback** | `query=""` drives pad color and blink | `query=""` drives MIDI Note On/Off to LED |

A physical pad grid controller typically needs both:
- a **mapper** to receive MIDI from the hardware and send VDJScript actions
- a **pad page** displayed in the VirtualDJ UI for visual feedback (optional but common)

Source: `Official`, `Inference`

---

## macOS Install Paths

| Path | Purpose |
| --- | --- |
| `~/Library/Application Support/VirtualDJ/Mappers/` | User mappers (override built-ins) |
| `/Applications/VirtualDJ.app/Contents/Resources/Mappers/` | Built-in controller mappers (read-only) |

Source: `Local observation`
