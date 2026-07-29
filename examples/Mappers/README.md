# Mappers

Real, working VirtualDJ mapper XML files used as ground truth for the mapper file format.

## What a mapper is (and is not)

VirtualDJ splits controller support into two layers:

1. **Device definition** — declares the hardware: MIDI notes/CCs or HID offsets, LEDs, encoders, value ranges. Built-in definitions ship *compiled* inside the app (`Resources/controllers.dat` and `Devices/controllers.dat`, a non-XML binary), so they cannot be copied here as XML. Custom definitions are XML; the official schema lives on the wiki (`ControllerDefinitionMIDIv8.html`, `ControllerDefinitionHIDv8.html`).
2. **Mapper** — binds named controls from a device definition to VDJScript. This folder contains real mappers. Root element: `<mapper device="" author="" version="" date="">`; every binding is `<map value="CONTROL_NAME" action="vdjscript" />`.

See [docs/Mapper XML.md](../../docs/Mapper%20XML.md) for the format reference.

## Local/

Copies of mapper XML from a working local VirtualDJ install (`~/Library/Application Support/VirtualDJ/Mappers/`, VirtualDJ 8.5.9307 / bundle 18.0.9482, copied 2026-07-12).

> **`author` does NOT indicate provenance. Do not use it to grade evidence.** (Corrected
> 2026-07-27.) The attribute records where the file *started*, not who wrote its current
> contents: customize VirtualDJ's default keyboard mapping and the file keeps
> `author="Atomix Productions"` while every binding in it may be yours. Two facts on this
> install settle it — `KEYBOARD - DeathDisco Keybindings v2025.12.xml` is entirely
> user-authored yet carries the Atomix tag, while `AlphaTheta DDJ-GRV6 - Factory Default.xml`
> is genuinely shipped content and carries **no** author tag at all. The attribute is
> therefore inverted as often as not.
>
> **Grade these files by their name and content instead**, and default to `Local test`
> working example, never `Built-in app resource`. In particular, **never treat a verb name
> found only in one of these files as evidence that the verb exists** — a personal mapping
> legitimately contains experiments and guesses that were never claimed to work. Verb
> existence is settled by the binary symbol/string test and the HTTP error-code sweep (see
> [Undocumented VDJScript Candidates.md](../../docs/Undocumented%20VDJScript%20Candidates.md)),
> not by appearing in a mapping.

The DDJ-GRV6 **Factory Default** file below is genuinely factory content and carries no `author` attribute, because it was produced via Settings → Controllers → **Factory default → Save** (VirtualDJ 2026, bundle 18.0.9482, 2026-07-27) rather than being an app-saved factory file. It is still `Built-in app resource`-grade — it is VirtualDJ's shipped mapping (e.g. `PLAY_PAUSE → pioneer_play`), distinct from the user-customized DeathDisco version — but the save did not stamp the author tag, and it contains only the `<mapper>`, never the compiled `<device>` definition. See [Mapper XML.md](../../docs/Mapper%20XML.md) §`<map>` semantics for the export procedure and its save quirk.

| File | Device | Maps | Author | Notes |
| --- | --- | --- | --- | --- |
| [Pioneer DDJ-XP2 - Pioneer DDJ-XP2.xml](Local/Pioneer%20DDJ-XP2%20-%20Pioneer%20DDJ-XP2.xml) | `DDJXP2` | 617 | Atomix | Factory mapping for a pad controller; `ONINIT`, `SHIFT`, `LED_*`, `DNC_*` idioms |
| [AKAI APC Mini MK2 - Custom Mapping.xml](Local/AKAI%20APC%20Mini%20MK2%20-%20Custom%20Mapping.xml) | `APCMINI2` | 301 | (unreliable tag) | Grid controller, named "Custom Mapping"; mode switching via global variables + `refresh_controller`. Treat as user-authored. |
| [KEYBOARD - DeathDisco Keybindings v2025.12.xml](Local/KEYBOARD%20-%20DeathDisco%20Keybindings%20v2025.12.xml) | `KEYBOARD` | 204 | (user; stale Atomix tag) | **User-authored personal keybindings**, started from the default keyboard mapping so the Atomix tag persisted. Useful for key-name idiom (`ALT+1`, `RIGHT ALT`, `UNMAPPED` fallback) — NOT for verb evidence; it contains experimental bindings such as `browser_filter`/`browser_search`, which are not verbs. |
| [AlphaTheta DDJ-GRV6 - DeathDisco DDJ-GRV6 v1.xml](Local/AlphaTheta%20DDJ-GRV6%20-%20DeathDisco%20DDJ-GRV6%20v1.xml) | `DDJGRV6` | 293 | (user) | User-authored; heavy `ONINIT`/`ONEXIT` setup, `setting_setsession`, `effect_clone` |
| [AlphaTheta DDJ-GRV6 - Factory Default.xml](Local/AlphaTheta%20DDJ-GRV6%20-%20Factory%20Default.xml) | `DDJGRV6` | 293 | Atomix (factory, no tag) | Shipped factory mapping, exported via Factory default → Save (see note above); `PLAY_PAUSE → pioneer_play`, `pioneer_*`/`padshift`/`touchwheel`/`wheel_mode` hardware idioms; mapper firing HTTP-verified on this hardware (`docs/VDJScript Local Test Tracker.md` §Mapper Firing) |

Observed special `value=""` names across these files: `ONINIT`, `ONEXIT`, `UNMAPPED`, `SHIFT`, `DNC_MODE`, `DNC_LOADED`, plus `SHIFT_`-prefixed and `LED_`-prefixed control names.

Do not hand-edit these copies. Refresh from the live Mappers folder when useful, then review the diff.
