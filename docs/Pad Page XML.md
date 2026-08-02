# Pad Page XML

Container-format reference for VirtualDJ pad-page XML files.

This document describes the XML schema: elements, attributes, and the `<menu>` mini-DSL. It does not repeat behavior guidance. For pad *behavior* (page-aware vs absolute sampler methods, empty-slot guards, generic `pad <n>` verbs), see:

- [VirtualDJ Reference — Pads and Sampler Pages](VirtualDJ%20Reference.md#pads-and-sampler-pages)
- [Example Pad XML Pages](Example%20Pad%20XML%20Pages.md)
- [Pad Page Inventory](../examples/Pads/README.md) (status labels and per-file notes)
- [Mapper XML](Mapper%20XML.md) (the separate controller/keyboard mapper format)

## Evidence Base and Official Documentation Status

The XML container format is not documented by Atomix. The official pads manual page ([manuals/.../pads.html](https://www.virtualdj.com/manuals/virtualdj/interface/decks/decksadvanced/pads.html), fetched 2026-07-12) describes the pads UI, the Pads Editor, "up to 2 configurable parameters", the pad menu, shift actions, 16-pad mode, and Split Pages — but never the file format. The wiki URLs `virtualdj.com/wiki/Pads.html` and `virtualdj.com/wiki/PadPages.html` were checked on 2026-07-12 and both resolve to wiki-search pages with no pad-page documentation (effectively 404).

Everything below is therefore reverse-engineered from:

- 17 shipped pages in [examples/Pads/Built-In/](../examples/Pads/Built-In/) (`Built-in pad page`, VirtualDJ 8.5.9307 / bundle 18.0.9336)
- 18 curated/working pages in [examples/Pads/](../examples/Pads/) and 10 test fixtures in [tests/Pads/](../tests/Pads/) (`Local test` where noted in their docs, otherwise working local examples)
- the official manual for UI-level semantics (`Official`)

45 XML files were surveyed for the attribute tables below. Semantics that no source states directly are labeled `Inference`.

## File Placement and Page Identity

- User pages live in the VirtualDJ home folder's `Pads/` directory — `~/Library/Application Support/VirtualDJ/Pads/*.xml` on this macOS install (`Local test`); older official docs cite `Documents/VirtualDJ/Pads/`. Shipped pages live in the app bundle (`/Applications/VirtualDJ.app/Contents/Resources/pads_*.xml` on macOS). Source: `Official`, `Built-in pad page`, `Local test`.
- For local files, the pad-page selector generally shows the *filename stem*, not `<page name="">`. The `name=""` value still matters as the `pad_page` scripting target. Source: [examples/Pads/README.md](../examples/Pads/README.md), `Local test`.
- `tools/lint_pads.py` enforces: root element `<page>`, non-empty unique `name=""` (for `examples/Pads/*.xml` and `tests/Pads/**` only — shipped `Built-In/` copies are exempt and often omit `name`), and that every literal `pad_page '...'` target matches a known page name.

## Root Element: `<page>`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<page name="MY PAGE" shortname="MP">
  ...
</page>
```

Attribute survey across all 45 files found exactly two root attributes. No other attribute occurs on `<page>` anywhere in the repo (in particular, `autodim` appears only on pad elements, never on the root).

| Attribute | Observed values | Files | Semantics | Source |
| --- | --- | --- | --- | --- |
| `name` | Free text, e.g. `CUE 16`, `scratchbank` | 29/45: all 18 curated, all 10 test, and only [pads_scratchbank.xml](../examples/Pads/Built-In/pads_scratchbank.xml) among built-ins | Page identity; the target string for the `pad_page` verb. | `Built-in pad page`, `Local test` |
| `shortname` | Short text, e.g. `HC`, `Roll`, `Man.Loop`, `S.Loop`, `scr.bank`, `Remix`, `PHRASE` | 8/45 | Compact display label, presumably for narrow page-button layouts; not officially documented. | `Built-in pad page`, `Inference` |

Distribution details:

- Both attributes together: [AUTO CUES.xml](../examples/Pads/Quarantine/AUTO%20CUES.xml) (`name="AUTO CUES" shortname="Remix"`), [Phrase Jump.xml](../examples/Pads/Quarantine/Phrase%20Jump.xml), [pads_scratchbank.xml](../examples/Pads/Built-In/pads_scratchbank.xml) — attribute order is not significant.
- `shortname` only: [pads_hotcues.xml](../examples/Pads/Built-In/pads_hotcues.xml) (`shortname="HC"`), pads_loop_roll, pads_manual_loop, pads_remix_points, pads_saved_loops.
- No attributes at all: 10 of the 17 built-in pages (e.g. [pads_sampler.xml](../examples/Pads/Built-In/pads_sampler.xml), [pads_stems.xml](../examples/Pads/Built-In/pads_stems.xml)). Shipped pages get their display name from VirtualDJ's own resources, so they can omit both. Custom local pages should always set `name`. Source: `Built-in pad page`, `Inference`.

## Pad Elements: `<pad1>` … `<pad16>`

One element per pad position. Element **text content is the VDJScript action** executed on press. Observed index range is exactly 1-16: no `pad0`, no `pad17+` anywhere in the 45 files. 8-pad pages simply stop at `<pad8>`; pages may also skip positions (e.g. [pads_manual_loop.xml](../examples/Pads/Built-In/pads_manual_loop.xml) defines pad1-5 and pad7 but not pad6). Every pad element in the repo has non-empty action text.

```xml
<pad1 name="`cue_display 1`" color="cue_color 1" autodim="false">hot_cue 1</pad1>
```

(from [pads_hotcues.xml](../examples/Pads/Built-In/pads_hotcues.xml))

| Attribute | Value type | Semantics | Example (file) | Source |
| --- | --- | --- | --- | --- |
| `name` | Text; backtick segments are evaluated as VDJScript | Pad label. | `name="`cue_display 1`"` ([pads_hotcues.xml](../examples/Pads/Built-In/pads_hotcues.xml)) | `Built-in pad page` |
| `color` | VDJScript color expression | Pad color. See [Color Values](#color-values). | `color="sampler_color 1"` ([pads_sampler.xml](../examples/Pads/Built-In/pads_sampler.xml)) | `Built-in pad page` |
| `query` | VDJScript query | Lit/active state, separate from `color`; resolves to on/off/blink states. | `query="not masterdeck ? is_sync ? true : blink 500ms"` ([TRANSPORT.xml](../examples/Pads/Quarantine/TRANSPORT.xml)); `query="... ? blink 1bt : on : off"` ([SAMPLER READ ONLY.xml](../examples/Pads/SAMPLER%20READ%20ONLY.xml)) | `Built-in pad page`, `Local test` |
| `autodim` | `false`, `true`, `query` | Controls automatic dimming of inactive pads; see below. | `autodim="query"` ([pads_stems.xml](../examples/Pads/Built-In/pads_stems.xml)) | `Built-in pad page`, `Inference` |
| `drop` | VDJScript action | Executed when a file is dragged and dropped onto the pad. Only assignment verbs observed. | `drop="sampler_assign 1"` ([pads_sampler.xml](../examples/Pads/Built-In/pads_sampler.xml)); `drop="scratchbank_assign 1"` ([pads_scratchbank.xml](../examples/Pads/Built-In/pads_scratchbank.xml)) | `Built-in pad page` |
| `pressure` | VDJScript action receiving a value | Velocity/pressure handler for pressure-capable controller pads. | `pressure="sampler_velocity 1"` ([pads_sampler_velocity.xml](../examples/Pads/Built-In/pads_sampler_velocity.xml)); `pressure="... sampler_volume_nogroup 1 '4x4x1'"` ([32 Samples.xml](../examples/Pads/Quarantine/32%20Samples.xml)) | `Built-in pad page` |
| `right_click` | VDJScript action | Explicit right-click action. Observed **only** in the local page [FX-SLOTS.xml](../examples/Pads/Quarantine/FX-SLOTS.xml) (`right_click="effect_select 1"`), never in a built-in page. The stock right-click/shift behavior is the `<shift_padN>` layer (the manual describes right-click as the shift trigger), so treat this attribute as unverified until locally tested. | `right_click="effect_select 1"` ([FX-SLOTS.xml](../examples/Pads/Quarantine/FX-SLOTS.xml)) | `Inference` |

No other pad attributes exist in the surveyed files.

### `autodim`

Observed values and distribution:

- `autodim="false"` — 9 files, both shipped and curated (all 32 pad entries of [pads_hotcues.xml](../examples/Pads/Built-In/pads_hotcues.xml); most of [TRANSPORT.xml](../examples/Pads/Quarantine/TRANSPORT.xml), [PLAY 16.xml](../examples/Pads/Quarantine/PLAY%2016.xml), [AUTO CUES.xml](../examples/Pads/Quarantine/AUTO%20CUES.xml), [SAMPLER READ ONLY.xml](../examples/Pads/SAMPLER%20READ%20ONLY.xml), [CUE-EDIT.xml](../examples/Pads/Quarantine/CUE-EDIT.xml), [Phrase Jump.xml](../examples/Pads/Quarantine/Phrase%20Jump.xml)).
- `autodim="query"` — 3 built-in files only: [pads_stems.xml](../examples/Pads/Built-In/pads_stems.xml), [pads_stems+fx.xml](../examples/Pads/Built-In/pads_stems+fx.xml), [pads_cueloop.xml](../examples/Pads/Built-In/pads_cueloop.xml). In the stems pages it accompanies static colors (`color="color 'green'"`) on toggle-style actions (`stem_pad 'vocal'`).
- `autodim="true"` — one file: [TRANSPORT.xml](../examples/Pads/Quarantine/TRANSPORT.xml) pads 9-11 (KEY/BEAT/PHRASE sync pads, which also define `query=""`).

Interpretation (`Inference`, unconfirmed): by default VirtualDJ dims a pad whose state reads inactive; `false` disables dimming so the `color` expression shows at full brightness, and `query` ties the dim state to the pad's `query=""` result rather than the action's own state. Exact default behavior is an [open question](#open-questions).

## Shift Layer: `<shift_pad1>` … `<shift_pad16>`

Same shape as `<padN>`: text content is the action, triggered by shift or right-click (`Official` manual: right-clicking pads triggers the alternate function). Observed range 1-16.

Attributes observed on shift pads: `name`, `color`, `autodim`, `query`, `right_click` (the last again only in [FX-SLOTS.xml](../examples/Pads/Quarantine/FX-SLOTS.xml)). `drop` and `pressure` were never observed on a shift pad.

```xml
<shift_pad1 name="DELETE" color="has_cue 1 ? color 'white'" autodim="false">delete_cue 1</shift_pad1>
```

(from [pads_hotcues.xml](../examples/Pads/Built-In/pads_hotcues.xml); note the one-armed conditional in `color` — the false branch is simply omitted)

Give shifted pads their own `color=""`; skins may read shifted colors separately (see [VirtualDJ Reference — Sampler Empty-Slot Guards and Shifted Colors](VirtualDJ%20Reference.md#sampler-empty-slot-guards-and-shifted-colors)). Source: `Local test`.

## Parameters: `<param1>`, `<param2>`

The two per-page parameter slots shown next to the pads ("Each pad page offers up to 2 configurable parameters" — `Official`). Text content is the action; on encoder-style use the incoming value is testable with `param_bigger 0 ? ... : ...` for direction (many files, e.g. [AUTO CUES.xml](../examples/Pads/Quarantine/AUTO%20CUES.xml): `param_bigger 0 ? goto_cue +1 remix : goto_cue -1 remix`).

**No `<param3>` or higher exists in any of the 45 files.**

| Attribute | Observed on | Semantics | Example (file) | Source |
| --- | --- | --- | --- | --- |
| `name` | param1 (33/34), param2 (28/29) | Label; backtick expressions common. | `name="`get_sampler_bank`"` ([pads_sampler.xml](../examples/Pads/Built-In/pads_sampler.xml)) | `Built-in pad page` |
| `visible` | param1 (1), param2 (4) | `false` only. Hides the parameter control while keeping the action mappable. | `<param2 visible="false">goto</param2>` ([pads_hotcues.xml](../examples/Pads/Built-In/pads_hotcues.xml)) | `Built-in pad page`, `Inference` |
| `query` | param2 (1) | Separate query expression; single occurrence. | `<param2 name="`sampler_pad_page`" query="sampler_pad_page">sampler_pad_page</param2>` ([pads_sampler.xml](../examples/Pads/Built-In/pads_sampler.xml)) | `Built-in pad page` |
| `tooltip` | param1 (1) | Tooltip text; `[value]` appears to substitute the current value. Single occurrence. | `<param1 name="..." tooltip="[value]">...</param1>` ([pads_stems.xml](../examples/Pads/Built-In/pads_stems.xml)) | `Built-in pad page`, `Inference` |

A parameter can be empty: [AUTO CUES.xml](../examples/Pads/Quarantine/AUTO%20CUES.xml) has `<param1></param1>` with no attributes, matching the manual's note that some pages leave Parameter 1 empty.

## Menu: `<menu>`

Optional, at most one per `<page>` (also allowed inside `<custompadsmode>`? — never observed there). No attributes anywhere. The text content is a newline-delimited mini-DSL; 24 menu blocks exist across the repo. XML entities apply as usual (`&gt;&gt;` in the raw file is `>>`, `&apos;` is `'`).

Observed line forms:

| Form | Meaning | Evidence | Source |
| --- | --- | --- | --- |
| `` `verb` `` (whole menu is one backtick line) | Delegate the entire menu to a built-in options verb. | `` `sampler_options` `` in 7 sampler pages ([pads_sampler.xml](../examples/Pads/Built-In/pads_sampler.xml), [SAMPLER READ ONLY.xml](../examples/Pads/SAMPLER%20READ%20ONLY.xml), …); `` `loop_pad_mode` `` in [pads_loop.xml](../examples/Pads/Built-In/pads_loop.xml) | `Built-in pad page`, `Inference` |
| `Label =[action]` | Plain menu item: click executes the action. Labels ending in `...` open editors/dialogs. | `Edit CUEs and POIs... =[edit_poi]` ([pads_hotcues.xml](../examples/Pads/Built-In/pads_hotcues.xml)); `Info... =[os2l_info]` ([pads_dmx.xml](../examples/Pads/Built-In/pads_dmx.xml)); `PUSH FX =[pad_page "PUSH FX"]` ([COLOR FX.xml](../examples/Pads/Quarantine/COLOR%20FX.xml)) | `Built-in pad page`, `Inference` |
| `Label +[action]` | Checkable menu item: the action is both *queried* for the checked state and *executed* on click. | `Read-only (Lock) +[lock_cues]`, `Smart Cue +[smart_cue]` ([pads_hotcues.xml](../examples/Pads/Built-In/pads_hotcues.xml)); `Auto Sync +[cue_loop_autosync]` ([pads_cueloop.xml](../examples/Pads/Built-In/pads_cueloop.xml)) | `Built-in pad page`, `Inference` |
| `Parent >> Child +[action]` | Submenu: repeated `Parent >>` prefixes group children under one submenu. Behaves like a radio group when the children are variants of one setting. | `Display mode >> Name +[cue_display 'name']` and four siblings ([pads_hotcues.xml](../examples/Pads/Built-In/pads_hotcues.xml), [pads_saved_loops.xml](../examples/Pads/Built-In/pads_saved_loops.xml)); `Quantize >> Bar +[quantize_setcue on & setting 'globalQuantize' 4]` ([CUE.xml](../examples/Pads/Quarantine/CUE.xml)) | `Built-in pad page`, `Inference` |
| `-` (alone on a line) | Separator. | [pads_hotcues.xml](../examples/Pads/Built-In/pads_hotcues.xml), [pads_saved_loops.xml](../examples/Pads/Built-In/pads_saved_loops.xml), [CUE.xml](../examples/Pads/Quarantine/CUE.xml) | `Built-in pad page` |

Additional observations:

- **Labels can be dynamic.** [pads_keycue.xml](../examples/Pads/Built-In/pads_keycue.xml) uses a backtick expression as the label of a checkable item:

  ```text
  `get_text "Hot Cue Mode: `setting 'hotcueMode'`"` +[setting 'hotcueMode']
  ```

- **`+[...]` bodies can be full scripts.** [pads_loop_roll.xml](../examples/Pads/Built-In/pads_loop_roll.xml) implements a three-state cycle where the leading branch result (`on`/`off`) reads as the checked state and the `&` chain performs the transition:

  ```text
  Quantize +[quantize_all ? on & quantize_all off & quantize_loop off : quantize_loop ? on & quantize_loop off : off & quantize_loop on]
  ```

  This is the strongest evidence that `+[...]` is queried for checked state and executed on click. Source: `Built-in pad page`, `Inference`.

- **Leading whitespace appears tolerated:** [COLOR FX.xml](../examples/Pads/Quarantine/COLOR%20FX.xml) indents its second menu line (`    SELECT =[filter_selectcolorfx]`) and the page works as a local page.
- Only one submenu level (`A >> B`) is ever observed; deeper nesting is untested.

## Alternate Layout: `<custompadsmode nb="4">`

A container element holding a *replacement* pad set, observed in 8 built-in files (pads_beatjump, pads_keycue, pads_loop, pads_loop_roll, pads_manual_loop, pads_slicer, pads_stems, pads_stems+fx) and nowhere in curated or test pages. Observable facts (`Built-in pad page`):

- The only attribute is `nb`, and the only observed value is `"4"`.
- Children are `<pad1>`-`<pad4>` and/or `<shift_pad1>`-`<shift_pad4>` with the normal pad attribute surface (`name`, `color`, `autodim`). Two files (pads_beatjump, pads_manual_loop) provide only shift pads.
- It appears after the main pad/param/menu elements, and its pads may differ from the main set (in [pads_stems+fx.xml](../examples/Pads/Built-In/pads_stems+fx.xml) the main page mixes stems and `padfx` pads while the `custompadsmode` block is a clean 4-stem layout).

Interpretation (`Inference`): an alternate definition used when the host UI/controller exposes only `nb` custom pads (4-pad views such as split pages or small controller layouts), replacing the first pads rather than truncating them. The exact trigger condition is an [open question](#open-questions).

```xml
<custompadsmode nb="4">
  <pad1 name="Vocal" color="color 'green'" autodim="query">stem_pad 'vocal'</pad1>
  ...
  <shift_pad1 name="Vocal" color="color 'green'" autodim="query">stem_pad isolate 'vocal'</shift_pad1>
  ...
</custompadsmode>
```

(from [pads_stems+fx.xml](../examples/Pads/Built-In/pads_stems+fx.xml))

## Color Values

`color=""` and `query=""` take ordinary VDJScript expressions; the distinct value forms observed across the 45 files are listed here. For `color` verb semantics see the entry in [VDJScript Verbs — Parameters & Constants](VDJScript%20Verbs.md) (the `color` row documents `color "red"`, `color "#C08040"`, and `color 0.8 0.5 0.25`).

| Form | Example | Files | Source |
| --- | --- | --- | --- |
| `color 'name'` / `color "name"` | `color 'green'`, `color "red"` | 29 files | `Built-in pad page` |
| `color name` (unquoted argument) | `color white`, `color pink` | [PLAY 16.xml](../examples/Pads/Quarantine/PLAY%2016.xml), [TRANSPORT.xml](../examples/Pads/Quarantine/TRANSPORT.xml) | `Local test` (working local pages) |
| Bare name as the whole attribute | `color="blue"` | [TRANSPORT.xml](../examples/Pads/Quarantine/TRANSPORT.xml) pad15 | `Local test` |
| `color '#RRGGBB'` (hex, both cases) | `color '#FF3B30'`, `color '#2bd976'` | 8 files | `Built-in pad page` ([pads_stems+fx.xml](../examples/Pads/Built-In/pads_stems+fx.xml) uses `color '#3D619C'`), `Local test` |
| `dim` | `sampler_loaded 1 ? sampler_color 1 : dim` | 5 sampler pages | `Local test` (equivalent to `constant 0.1` per the verbs table) |
| `blink <interval>` wrapper | `blink 1bt ? cue_color 1 : color 'black'` ([CUE.xml](../examples/Pads/Quarantine/CUE.xml)); `blink 500ms` in `query` ([TRANSPORT.xml](../examples/Pads/Quarantine/TRANSPORT.xml)) | 2 color files + query uses | `Built-in pad page` ([pads_manual_loop.xml](../examples/Pads/Built-In/pads_manual_loop.xml) uses bare `blink ?`), `Local test` |
| `on` / `off` / `true` | terminal branches in `query=""` | many | `Built-in pad page`, `Local test` |
| State verbs returning colors | `cue_color 1`, `cue_color 1 remix`, `sampler_color 1`, `sampler_color 1 "auto"`, `get_sample_color 1`, `loop_color 1`, `stem_color 'vocal'`, `keycue_pad_color 1`, `beatjump_pad 1 'color'`, `effect_stems_color`, `scratchbank_load_to_deck 1` | most built-ins | `Built-in pad page` |

Named colors observed as arguments to the `color` verb: `red`, `green`, `blue`, `cyan`, `magenta`, `yellow`, `orange`, `white`, `black`, `gray`, `purple`, `pink`. (Strings like `'vocal'`, `'instru'`, `'bass'`, `'rhythm'`, `'melody'`, `'kick'`, `'hihat'` appear only as `stem_color` arguments — stem identifiers, not color names.)

The float-triple form `color 0.8 0.5 0.25` from the verbs reference is **not** used in any pad XML in this repo.

## Multi-Page Patterns

The `pad_page 'NAME'` verb switches the deck's active pad page; the target string is matched against page names (for local files, the selector name derives from the filename stem — keep `name=""` and the filename stem aligned to avoid ambiguity). `tools/lint_pads.py` cross-references every literal `pad_page '...'` in `examples/Pads/*.xml` and `tests/Pads/` against known `<page name="">` values.

Observed switching idioms:

- From a **menu item**: `PUSH FX =[pad_page "PUSH FX"]` ([COLOR FX.xml](../examples/Pads/Quarantine/COLOR%20FX.xml))
- From a **parameter**: `<param1 name="PAD FX">pad_page "COLOR FX"</param1>` ([FX-SLOTS.xml](../examples/Pads/Quarantine/FX-SLOTS.xml))

Generic two-page pattern using only these observed idioms:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- File: MY TOOLS A.xml -->
<page name="MY TOOLS A">
  <pad1 name="PLAY" color="color 'green'">play_pause</pad1>
  <param1 name="MORE">pad_page "MY TOOLS B"</param1>
  <menu>More tools =[pad_page "MY TOOLS B"]</menu>
</page>
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- File: MY TOOLS B.xml -->
<page name="MY TOOLS B">
  <pad1 name="SYNC" color="color 'cyan'">sync</pad1>
  <param1 name="BACK">pad_page "MY TOOLS A"</param1>
  <menu>Back =[pad_page "MY TOOLS A"]</menu>
</page>
```

For paging *within* one file (a single page that shows different content per sub-page), the observed patterns are internal variables ([32 Samples.xml](../examples/Pads/Quarantine/32%20Samples.xml): `cycle 'sam_page' 4` with `var 'sam_page' N ? ...` branches; [PLAY 16.xml](../examples/Pads/Quarantine/PLAY%2016.xml): `var_equal 'hcpage' ...`) or, for the sampler, the official `sampler_pad_page` pager (see [VirtualDJ Reference — Read-Only Multi-Page Sampler Pages](VirtualDJ%20Reference.md#read-only-multi-page-sampler-pages)). Source: `Local test`, `Built-in pad page`.

## Samplerbank XML (Related Third Format)

Sampler *banks* use a separate, simpler XML format — not a pad page. Four shipped banks are copied in [examples/Samplerbanks/Built-In/](../examples/Samplerbanks/Built-In/) ([AUDIO FX.xml](../examples/Samplerbanks/Built-In/AUDIO%20FX.xml) 6 samples, [FAMOUS.xml](../examples/Samplerbanks/Built-In/FAMOUS.xml) 5, [INSTRUMENTS.xml](../examples/Samplerbanks/Built-In/INSTRUMENTS.xml) 13, [VIDEO & SCRATCH.xml](../examples/Samplerbanks/Built-In/VIDEO%20&%20SCRATCH.xml) 3); see that folder's [README](../examples/Samplerbanks/Built-In/README.md) for provenance and refresh instructions.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<samplerbank>
  <sample path="Audio\Air Horn.vdjsample" col="0" row="0" />
  <sample path="Audio\Siren.vdjsample" col="1" row="0" />
</samplerbank>
```

- Root: `<samplerbank>`, no attributes observed.
- Child: `<sample path="" col="" row="" />` — `path` is a backslash-separated path to a `.vdjsample` relative to the sampler content root; `col`/`row` are the zero-based grid position.

Source: `Built-in app resource`.

## Open Questions

- **`autodim` semantics.** Values `false` (9 files), `query` (3 built-ins), `true` (1 file) are observed, but no source states the default dimming rule or what exactly `query` binds to. Needs a local A/B test with a static-color pad. Raw evidence: `autodim="false"` beside `color="cue_color 1"` throughout [pads_hotcues.xml](../examples/Pads/Built-In/pads_hotcues.xml); `autodim="query"` beside static `color="color 'green'"` toggles in [pads_stems.xml](../examples/Pads/Built-In/pads_stems.xml).
- **`=[...]` vs `+[...]` exact rendering.** The toggle-vs-plain interpretation is `Inference` from item content (editors use `=`, toggleable settings use `+`). Whether `+` items show a checkmark, a radio dot inside `>>` groups, or both, is unverified. Raw examples: `Edit CUEs and POIs... =[edit_poi]` vs `Read-only (Lock) +[lock_cues]` ([pads_hotcues.xml](../examples/Pads/Built-In/pads_hotcues.xml)).
- **Whole-menu backtick lines.** `` `sampler_options` `` and `` `loop_pad_mode` `` replace the entire menu body. Whether any verb can expand to a menu this way, or only dedicated options verbs, is unknown.
- **`>>` nesting depth.** Only one level (`Display mode >> Name`) is observed; `A >> B >> C` is untested.
- **`<custompadsmode>` trigger.** Only `nb="4"` observed, only in built-ins. When VirtualDJ selects this block over the main pad set (4-pad controller layouts? split pages?) and whether other `nb` values are honored is unverified.
- **`right_click=""` attribute support.** Present only in the local [FX-SLOTS.xml](../examples/Pads/Quarantine/FX-SLOTS.xml), alongside `shift_padN` elements in the same file. Whether VirtualDJ actually reads this attribute (vs. it being inert author intent) needs a local test.
- **`tooltip="[value]"` substitution.** Single occurrence ([pads_stems.xml](../examples/Pads/Built-In/pads_stems.xml)); the `[value]` placeholder semantics are assumed, not verified.
- **`shortname` display context.** Which layouts prefer `shortname` over the filename stem / `name` is not documented.
- **Pad index ceiling.** 16 is the maximum observed and matches the manual's 16-pad mode; whether indexes above 16 parse is untested.
- **`color 0.8 0.5 0.25` in pad context.** Documented for the `color` verb but never used in pad XML here; untested in `color=""`.
