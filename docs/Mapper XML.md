# VirtualDJ Mapper XML

Reference for VirtualDJ controller and keyboard mapper files, and the device-definition XML they bind to.

Ground truth for this doc: four real working mappers copied into [examples/Mappers/Local/](../examples/Mappers/README.md) (two factory Atomix mappings, one Atomix keyboard mapping, one user-authored controller mapping), plus the official VDJPedia pages `ControllerMappingFile_v8.html`, `ControllerDefinitionMIDIv8.html`, and `ControllerDefinitionHIDv8.html`.

> An earlier revision of this document described an inline schema (`<button note="36" action="..."/>` directly inside `<mapper>`). That schema does not match any real mapper file and has been removed. Real mappers bind *named controls* to VDJScript with `<map value="" action=""/>`; the hardware I/O lives in a separate device definition.

Source labels match the rest of this repo:
`Official`, `Official forum`, `Community`, `Built-in app resource`, `Local test`, `Inference`.

---

## The Two-Layer Model

VirtualDJ splits controller support into two XML layers:

1. **Device definition** (`<device>` root) — declares the hardware: which MIDI notes/CCs or HID byte offsets exist, what they are named, LEDs, encoders, value ranges. No VDJScript is evaluated here.
2. **Mapper** (`<mapper>` root) — binds each named control from the definition to a VDJScript action: `<map value="PLAY" action="play_pause"/>`.

Most shipped controllers have a *compiled* built-in definition: the app bundle contains `Resources/controllers.dat` (binary, not XML) and no `Resources/Mappers/` or `Resources/Devices/` folders (`Local test`, bundle 18.0.9482). You only write a device definition XML for hardware VirtualDJ does not already know; you write or edit a mapper whenever you want custom behavior on any controller.

Mapper actions are VDJScript. Device definitions are not — do not expect variables, conditionals, backticks, or actions to be evaluated inside definition elements such as `<button>`, `<led>`, `cc=""`, `value=""`, or `zero=""` (`Official forum`, staff reply in "Sending MIDI CC Commands"). Put dynamic behavior in the mapper:

```xml
<!-- Device definition: static hardware output declarations -->
<led name="LED_CC_000" cc="0x00" channel="0"/>
<led name="LED_CC_001" cc="0x01" channel="0"/>

<!-- Mapper: VDJScript decides which output is active -->
<map value="LED_CC_000" action="var_equal 'CCOut' 0"/>
<map value="LED_CC_001" action="var_equal 'CCOut' 1"/>
```

---

## Mapper Files

### Root `<mapper>` element

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mapper device="DDJXP2" author="Atomix Productions" version="850" date="2025-11-09">
  <info>http://www.virtualdj.com/manuals/hardware/pioneer/ddjxp2/index.html</info>
  <map value="SHIFT" action="shift" />
  <map value="PLAY" action="play_pause" />
</mapper>
```

| Attribute | Description | Source |
| --- | --- | --- |
| `device` | Unique string identifying the controller; must match the device definition's `name` | `Official`, `Local test` |
| `author` | Optional author name; factory mappings saved by the app carry `Atomix Productions` | `Official`, `Local test` |
| `version` | Minimum VirtualDJ version, e.g. `850` | `Official`, `Local test` |
| `date` | Optional creation/update date | `Official`, `Local test` |
| `priority` | Optional precedence: `-1` higher, `1` lower | `Official` |

Children:

| Element | Description | Source |
| --- | --- | --- |
| `<info>` | Optional URL documenting the mapping | `Official`, `Local test` |
| `<map value="" action="" />` | One binding per named control | `Official`, `Local test` |

`<map>` may also carry a `name=""` attribute (seen empty in factory keyboard mappings; purpose unconfirmed) (`Local test`).

### `<map>` semantics

> **End-to-end firing verified** (`Local test`, VirtualDJ 2026, AlphaTheta DDJ-GRV6, 2026-07-27). A minimal two-line mapper for `device="DDJGRV6"` — `<map value="ONINIT" …>` plus `<map value="PLAY_PAUSE" action="set '$v' 1"/>` — was loaded on the real controller; pressing the physical play button set the global, read back `1` over the [HTTP interface](HTTP%20Control%20Interface.md). This is the first local confirmation that the `<map value action>` schema binds and fires on hardware, not just that the format parses.

- `value=""` is the control name declared by the device definition (`PLAY_PAUSE`, `CUE`, `BROWSE`, `LED_PLAY_PAUSE`, …). **The name must match the device definition exactly.** A wrong name binds nothing and fails *silently* — `value="PLAY"` on the DDJ-GRV6 (whose control is `PLAY_PAUSE`) loaded without error and simply never fired (`Local test`, 2026-07-27), consistent with VDJScript's no-error parsing. Crib the exact names from a working mapper for that device (`rg -o 'value="[^"]*"'`), never guess.
- `action=""` is VDJScript. For buttons it runs on press; for sliders/encoders the moved value is passed to the action implicitly (e.g. `action="volume"`); for LED-out controls the action is evaluated as a *query* whose result drives the LED.
- The same query rules as skin/pad `query=""` apply to LED bindings, including `blink` (`Local test`: `<map value="DNC_MODE" action="blink 150ms"/>` in the factory DDJ-XP2 mapping).

### Special `value=""` names

Observed in factory and user mappings (`Local test`, [examples/Mappers/Local/](../examples/Mappers/README.md)):

| Name | Fires |
| --- | --- |
| `ONINIT` | When the mapper loads — on controller connect, on app start, and on mapping-select — used for setup chains (`effect_3slots_layout on`, `setting_setsession …`). Firing HTTP-verified (`Local test`, DDJ-GRV6, 2026-07-27): its action set a global read back as `1`. Note that loading a mapping also **resets `$` session globals**, so `ONINIT` is the right place to seed controller state rather than assuming a prior value survives. |
| `ONEXIT` | When the controller disconnects — used to undo `ONINIT` state |
| `UNMAPPED` | Fallback for controls with no explicit `<map>` (factory keyboard maps it to `search`) |
| `SHIFT` | Declares the shift modifier: `<map value="SHIFT" action="shift" />` |
| `SHIFT_<NAME>` | Binding for `<NAME>` while shift is held (a separate `<map>` row, not an attribute) |
| `LED_<NAME>` | Output binding driving an LED; action evaluated as query |
| `DNC_MODE`, `DNC_LOADED` | Display/notification controls on supported hardware (e.g. `blink 150ms`, `load_pulse`) |

Shift layers are therefore expressed as parallel `SHIFT_`-prefixed control names, not as a `shift=""` attribute:

```xml
<map value="BROWSE" action="browser_scroll" />
<map value="SHIFT_BROWSE" action="browser_scroll" />
<map value="BROWSE_PUSH" action="browser_window 'folders' ? browser_enter : browser_window 'folders'" />
```

### Keyboard mappers

Keyboard mappers use the **same** `<mapper>`/`<map>` schema with `device="KEYBOARD"`. Key identifiers are the `value=""` names — there is no `key=""` attribute (`Local test`, factory keyboard mapping):

```xml
<mapper device="KEYBOARD" author="Atomix Productions" version="850" date="2026-03-14">
  <map value="UNMAPPED" action="search" />
  <map value="ALT" action="keyboard_shortcuts" name="" />
  <map value="RIGHT ALT" action="keyboard_shortcuts" name="" />
  <map value="ALT+1" action="deck 1 select" />
  <map value="ALT+Q" action="deck 1 play_pause" />
</mapper>
```

Observed key-name forms: bare keys (`A`, `1`, `SPACE`-style names), positional modifiers (`RIGHT ALT`), and `MOD+KEY` combos (`ALT+1`, `ALT+Q`). Full key-name enumeration has not been captured locally; harvest more names from a saved keyboard mapping before relying on unobserved ones (`Inference`).

### Deck targeting

Deck scoping happens *inside the VDJScript action*, not via a `deck=""` attribute on `<map>`:

```xml
<map value="DECK_LEFT" action="deck 3 leftdeck ? deck 1 leftdeck : deck 3 leftdeck" />
<map value="LED_DECK_LEFT" action="deck 3 leftdeck" />
```

(`Local test`, factory DDJ-XP2 mapping. Device definitions may declare per-control `deck=""` so a control name is deck-scoped before the mapper sees it — see below.)

---

## Device Definition Files

Summary of the official schema (`Official`: `ControllerDefinitionMIDIv8.html`, `ControllerDefinitionHIDv8.html`). No local device-definition XML has been tested yet; treat details below as official-doc-derived, not locally verified.

### Root `<device>` (MIDI)

```xml
<device name="DDJSX" author="Atomix Productions"
        description="Pioneer DDJ-SX" version="800"
        type="MIDI" vid="0x08E4" pid="0x0171"
        decks="4" padColumns="4" padRows="2" padSides="2">
  <audio description="Pioneer DDJ-SX" input="1" output="2"
         mixer="yes" vid="0x08E4" pid="0x0171"
         asio="Pioneer DDJ_SX ASIO" />
  <button note="0x34" name="PLAY_PAUSE" deck="1" channel="1" />
  <slider ccmsb="0x08" cclsb="0x28" name="LEVEL" deck="1" channel="0"/>
  <init sendsysex="F00001020304057F" />
</device>
```

Key root attributes: `name` (the string mappers reference via `device=""`), `type="MIDI"`, `description`, `version`, `author`, `decks`, detection ids (`vid`/`pid`, `sysexid`, `drivername`), and optional `singledeck`, `motor`, `platform="pc|mac"`, `padColumns`/`padRows`/`padSides`.

MIDI input elements: `<button>` (`note` or `cc`, `value`/`off`, `inverted`, `autoled`, `channel`, `deck`, `nbdecks`), `<toggle>`, `<slider>` (`cc`/`ccmsb` 14-bit, `note` for velocity, `pitch` for pitch-bend, `min`/`max`/`zero`/`zerorange`, `inverted`, `ghost` soft-takeover, `nozero`), `<jog>`/`<fulljog>` (incremental `zero`/`full` vs absolute `max`/`mask`), `<encoder>`/`<fullencoder>`, `<touchstrip>`, `<sysexin>`.

MIDI output elements: `<led>` (note- or CC-based, `noteoff`/`ccoff`, `default` linked button), `<color>` (RGB CCs or velocity→color `values="0x00=#000000,0x01=#FF0000"`), `<bar>` (VU/progress), `<digit>` (LCD digits), `<text>` (CC- or SysEx-based character displays, `encoding`), `<init>`/`<exit>`/`<ledsysex>`/`<sysex>`.

Relative encoders are handled by the definition layer (`<encoder zero="">`, `<jog zero="0x40">`), so the mapper only ever sees clean movement values — encoder two's-complement handling never appears in mapper XML.

### Root `<device>` (HID)

`type="HID"` with `reportsize`/`outreportsize`, then `<page type="in|out|init|wait|exit">` blocks containing the same logical elements positioned by `bit`/`byte`/`word`/`dword` + `nbbits`/`size` + `endian` instead of notes/CCs.

### Built-in definitions

Built-in definitions are compiled into `controllers.dat` (app bundle and `~/Library/Application Support/VirtualDJ/Devices/`); they are not inspectable XML (`Local test`). Custom definition XML files go in the `Devices/` folder of the VirtualDJ home directory.

---

## Relationship to Pad Pages

Pad pages (`examples/Pads/*.xml`) and mapper files are separate systems with a shared scripting language.

| | Pad pages | Mapper files |
| --- | --- | --- |
| **Triggered by** | On-screen pads in VirtualDJ UI | Physical controller hardware |
| **File location** | `Pads/` in the VirtualDJ home folder | `Mappers/` in the VirtualDJ home folder |
| **Root element** | `<page>` | `<mapper>` |
| **Input elements** | `<pad1>` … `<pad16>`, `<param1>`, `<param2>` | `<map value="" action="" />` |
| **LED feedback** | `query=""` drives pad color and blink | `LED_*` map bindings; action evaluated as query |

A physical pad-grid controller typically pairs a mapper (hardware → VDJScript) with a pad page shown in the UI. Factory pad-controller mappings drive mode switching with global variables plus `refresh_controller` (`Local test`, APC Mini MK2: `set '$apclivemode' 0 & wait 300ms & refresh_controller`).

---

## Install Paths (macOS, `Local test`)

| Path | Purpose |
| --- | --- |
| `~/Library/Application Support/VirtualDJ/Mappers/` | User and factory-saved mappers (XML) |
| `~/Library/Application Support/VirtualDJ/Devices/` | Custom device definitions (XML) + compiled `controllers.dat` |

**Edit/reload cycle** (`Local test`, 2026-07-27): editing a mapper file that is already the active mapping does **not** hot-reload, and *re-selecting the same mapping does not pick up the change* — VirtualDJ serves a cached copy (the MIDI-learn monitor kept showing the pre-edit binding). A **full VirtualDJ restart** was required to load the edited file. Switching *between different* mappings does apply live; only in-place file edits need the restart. Plan controller-mapping iteration around a restart per change, or edit through the in-app mapper editor instead of the file.
| `/Applications/VirtualDJ.app/Contents/Resources/controllers.dat` | Compiled built-in definitions (binary) |

The v8-era official docs reference `Documents/VirtualDJ/Mappers/`; on this Mac install the live folder is under `Application Support` (`Local test`, 2026-07-12).

---

## Open Questions

- `<map name="">` attribute purpose (always empty in observed factory files).
- Full keyboard key-name enumeration.
- Whether `priority` interacts with multiple mappers for one device.
- No custom device-definition XML has been authored and load-tested locally yet; the definition schema above is official-doc-derived.
