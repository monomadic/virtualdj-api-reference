# Mappers

Real, working VirtualDJ mapper XML files used as ground truth for the mapper file format.

## What a mapper is (and is not)

VirtualDJ splits controller support into two layers:

1. **Device definition** — declares the hardware: MIDI notes/CCs or HID offsets, LEDs, encoders, value ranges. Built-in definitions ship *compiled* inside the app (`Resources/controllers.dat` and `Devices/controllers.dat`, a non-XML binary), so they cannot be copied here as XML. Custom definitions are XML; the official schema lives on the wiki (`ControllerDefinitionMIDIv8.html`, `ControllerDefinitionHIDv8.html`).
2. **Mapper** — binds named controls from a device definition to VDJScript. This folder contains real mappers. Root element: `<mapper device="" author="" version="" date="">`; every binding is `<map value="CONTROL_NAME" action="vdjscript" />`.

See [Reference/Mapper XML.md](../../Reference/Mapper%20XML.md) for the format reference.

## Local/

Copies of mapper XML from a working local VirtualDJ install (`~/Library/Application Support/VirtualDJ/Mappers/`, VirtualDJ 8.5.9307 / bundle 18.0.9482, copied 2026-07-12). Files whose `author` attribute is `Atomix Productions` are factory mappings saved out by the app — treat those as `Built-in app resource`-grade evidence for format and idiom. Files without an `author` attribute are user-authored — treat as `Local test` working examples.

| File | Device | Maps | Author | Notes |
| --- | --- | --- | --- | --- |
| [Pioneer DDJ-XP2 - Pioneer DDJ-XP2.xml](Local/Pioneer%20DDJ-XP2%20-%20Pioneer%20DDJ-XP2.xml) | `DDJXP2` | 617 | Atomix | Factory mapping for a pad controller; `ONINIT`, `SHIFT`, `LED_*`, `DNC_*` idioms |
| [AKAI APC Mini MK2 - Custom Mapping.xml](Local/AKAI%20APC%20Mini%20MK2%20-%20Custom%20Mapping.xml) | `APCMINI2` | 301 | Atomix | Grid controller; mode switching via global variables + `refresh_controller` |
| [KEYBOARD - DeathDisco Keybindings v2025.12.xml](Local/KEYBOARD%20-%20DeathDisco%20Keybindings%20v2025.12.xml) | `KEYBOARD` | 204 | Atomix | Keyboard mapper; key names as `value=""` (`ALT+1`, `RIGHT ALT`), `UNMAPPED` fallback |
| [AlphaTheta DDJ-GRV6 - DeathDisco DDJ-GRV6 v1.xml](Local/AlphaTheta%20DDJ-GRV6%20-%20DeathDisco%20DDJ-GRV6%20v1.xml) | `DDJGRV6` | 293 | (user) | User-authored; heavy `ONINIT`/`ONEXIT` setup, `setting_setsession`, `effect_clone` |

Observed special `value=""` names across these files: `ONINIT`, `ONEXIT`, `UNMAPPED`, `SHIFT`, `DNC_MODE`, `DNC_LOADED`, plus `SHIFT_`-prefixed and `LED_`-prefixed control names.

Do not hand-edit these copies. Refresh from the live Mappers folder when useful, then review the diff.
