# VirtualDJ Development Environment

This folder is a local reference and development environment for VirtualDJ skinning, pad pages, and VDJScript.
VirtualDJ does not publish comprehensive developer documentation; this repo fills that gap.

## Where to start

```
README.md                     — human-facing project overview
Reference/README.md          — index of all reference docs, source label policy, current status
Reference/VirtualDJ Reference.md — Quick Decisions guide: preferred methods, rationale, examples
Reference/VDJScript Verbs.md — curated API reference: canonical names, aliases, surfaces
Reference/Official VDJScript Coverage Audit.md — names-only parity audit for the 991 official verb/alias names, plus promotion targets
Reference/Completeness Roadmap.md — ordered backlog for closing behavior, fixture, and hardware gaps
Pads/README.md                — pad page inventory, status labels, and maintenance checklist
Test/README.md                — documentation test harnesses and reproducible fixtures
```

## What is here

```
Pads/                        — working/reference pad page XML files plus copied built-in pad pages
Test/                        — documentation test harnesses, including pad XML fixtures
Skins/                       — skin source trees, reference skins, and copied built-in skins
Reference/                   — Markdown documentation
```

## Key facts for AI agents

- VirtualDJ skins are XML. The scripting language inside attributes is **VDJScript**.
- `action=""` attributes take VDJScript actions. `query=""` takes a boolean/value expression.
- `&` chains actions in XML attributes and must be written `&amp;` inside XML.
- Backtick-wrapped expressions (`` `verb` ``) evaluate and return a value in string/color contexts.
- Working/reference pad pages live in `Pads/*.xml`; copied built-in app-bundle pages live in `Pads/Built-In/`; documentation test harnesses live under `Test/`. See `Pads/README.md` before choosing a reference page. Skins live in `Skins/*/`; copied built-in app-bundle skins live in `Skins/Built-In/`.
- `Skins/GraveRaver/src/` is intentionally minimal and demonstrates the build system only. Do not use it as a polished skin reference.
- The official VDJScript verb appendix currently parses to 991 verb/alias names. The local VDJScript reference has 991/991 names present, with 20 official names still marked `Needs local test`.
- Source labels (`Official`, `Official forum`, `Community`, `Published skin`, `Built-in skin`, `Published pad page`, `Built-in pad page`, `Local test`, `Inference`) appear throughout the reference docs and indicate how reliable each claim is.
- Run `python3 tools/check_reference_status.py` after changing coverage counts, fixture inventories, or local reference links.

## Preferred patterns (quick version)

- **Slot FX**: `effect_select <slot> 'Name'`, `effect_slider <slot> <param> <value>`, `effect_active <slot>` — not name-based toggling.
- **ColorFX**: `filter_selectcolorfx 'Name'` + `filter` for the main deck filter knob. `effect_colorfx <1-4>` + `effect_colorslider` for extra dedicated controls.
- **Sampler (page-aware)**: `sampler_pad <n>`, `sampler_color <n> 'auto'`; compare `sampler_pad_page` to text ranges like `"9 to 16"` and use absolute `sampler_loaded <slot>` guards for empty checks (`sampler_loaded 16` for page 2 pad 8), since `sampler_loaded <n> 'auto'` tested unreliable.
- **Sampler (fixed slot)**: `sampler_play <n>`, `get_sample_name <n>`, `get_sample_color <n>`.
- **Panels**: `<panel visibility="...">` for query-driven; `name=""` + `skin_panelgroup` for persistent manual switching.
- **Dynamic text color**: one `<text color="`action`">`, not per-state color attributes.
- **Dynamic border color**: not supported (CTO confirmed). Use fill or background instead.
- **Time mode**: `display_time 'remain,elapsed'` + `get_time`, not custom skin vars.

## Working examples in this repo

| File | Demonstrates |
| --- | --- |
| [Pads/Reference - Slot FX.xml](Pads/Reference%20-%20Slot%20FX.xml) | Canonical slot-based audio FX pads |
| [Pads/Reference - ColorFX.xml](Pads/Reference%20-%20ColorFX.xml) | Canonical filter + ColorFX selection |
| [Pads/Reference - Page Aware Sampler.xml](Pads/Reference%20-%20Page%20Aware%20Sampler.xml) | Page-aware sampler labels, colors, actions |
| [Pads/SAMPLER READ ONLY.xml](Pads/SAMPLER%20READ%20ONLY.xml) | Confirmed read-only multi-page sampler with absolute empty-slot guards |
| [Pads/Built-In/README.md](Pads/Built-In/README.md) | Copied VirtualDJ app-bundle pad pages; semi-official executable examples |
| [Pads/COLOR FX.xml](Pads/COLOR%20FX.xml) | ColorFX selection with stems context |
| [Skins/Built-In/README.md](Skins/Built-In/README.md) | Copied VirtualDJ app-bundle skins; semi-official executable examples |
| [Skins/ModularSkeleton/build/skin.xml](Skins/ModularSkeleton/build/skin.xml) | Minimal modular skin scaffold |
| [Skins/GraveRaver/src/skin.xml](Skins/GraveRaver/src/skin.xml) | Minimal XInclude build-system demo, not a skin design reference |

## macOS paths

| Path | Content |
| --- | --- |
| `~/Library/Application Support/VirtualDJ/Pads/` | Installed pad pages |
| `~/Library/Application Support/VirtualDJ/Skins/` | Installed skins |
| `~/Library/Application Support/VirtualDJ/Mappers/` | Controller/keyboard mappings |
| `~/Library/Application Support/VirtualDJ/database.xml` | Main track database |

See [Reference/Application Internals.md](Reference/Application%20Internals.md) for the full path map, database structure, and stem sidecar layout.
