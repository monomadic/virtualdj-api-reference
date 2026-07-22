# VirtualDJ Development Environment

This folder is a local reference and development environment for VirtualDJ skinning, pad pages, and VDJScript.
VirtualDJ does not publish comprehensive developer documentation; this repo fills that gap.

## Where to start

```
README.md                     — human-facing project overview
TODO.md                       — active operational queue for open-ended work
INDEX.yml                     — topic-to-file routing map
docs/README.md          — index of all reference docs, source label policy, current status
docs/VirtualDJ Reference.md — Quick Decisions guide: preferred methods, rationale, examples
docs/VDJScript Verbs.md — curated API reference: canonical names, aliases, surfaces
docs/Official VDJScript Coverage Audit.md — authoritative names-only parity audit and local-test gap count
docs/Completeness Roadmap.md — ordered backlog for closing behavior, fixture, and hardware gaps
examples/Pads/README.md            — pad page inventory, status labels, and maintenance checklist
tests/README.md               — documentation test harnesses and reproducible fixtures
```

## Open-ended work

For “what should I do next?”, maintenance, documentation cleanup, or evidence-pass work, read `TODO.md` first. Treat `TODO.md` as the canonical active queue and start with the first `Ready` task unless the user names another task.

## Session efficiency rules

Context load is the dominant cost in this repo. These rules outrank thoroughness:

- **Never read the large docs end-to-end.** `docs/VDJScript Verbs.md` (~6,300 lines), `docs/Skin SDK.md` (~2,700 lines), `docs/Effects Engines.md`, `docs/VirtualDJ Reference.md`, and `docs/VDJScript Local Test Tracker.md` are section-addressed references. Read only the section a task names, or extract it with path-scoped `rg`/`awk`.
- **Look verbs up through the tooling, not the monolith.** Use the verb record store — `just verb get <name>`, `just verb search <term>` — and `just find-verb <name>` first. Open `VDJScript Verbs.md` only at the specific lines a search hit points to.
- **Record verb facts with `just verb put`, not by hand-editing tables.** A local-test result, confidence, or evidence note goes into the record once (`just verb put <name> test_status=Pass confidence=local_test evidence="…"`) instead of being promoted into the tracker and topical docs by hand.
- **Effect controls come from `just fx`, not prose tables.** `just fx get Echo` gives the full slider/button map (spelling-tolerant); `just fx search --has-button=quant`, `--min-sliders=6`, `--name-only`, `--format=json` answer the rest. Do not hand-transcribe the catalog into Markdown.
- **Query the store instead of reading listings.** `just verb search` filters — `--surface`, `--section`, `--tier`, `--status`, `--kind`, `--needs-test` — and `--format=json` for structured output. Ask for the verbs you need (`just verb search --surface=SkinQuery --section=Sampler`); do not pull a category listing and filter it yourself. `just verb next-incomplete` gives the next active (non-hardware-blocked) work item, `just verb stats` the breakdown.
- **Planning docs are frozen.** `docs/VDJScript Reference Consolidation Plan.md` and `docs/Completeness Roadmap.md` are design references, not active state. Do not refresh, reorder, or re-scope them; do not spend turns rewriting planning prose or reordering the TODO queue. `TODO.md` is the only active planning state, and it changes when a task completes or the user asks.
- **Probe over HTTP first, fixtures second.** When VirtualDJ is running with the network interface enabled (`just vdj-up` to check), read values with `just vdj-query` instead of pad readback. Pad/skin fixtures remain necessary only for surface-specific behavior (rendering, pad context, skin runtime). Batch every probe a live session can carry, and prefer dump-style sweeps over one-question rounds.
- **Delegate mechanical passes.** Transcribing observed values into tables, promoting settled tracker rows, and lint fixes are cheap-model subagent work; keep the main context for evidence interpretation and ambiguous calls.
- Prefer `INDEX.yml`, `just next-task`, `just find-verb <name>`, and path-scoped `rg` over repo-wide discovery; broaden only after the task route proves insufficient or contradictory.
- Keep volatile coverage counts sourced from `docs/Official VDJScript Coverage Audit.md`; do not repeat exact count summaries in entrypoint docs unless the checker intentionally enforces them.

Direction of travel: verb facts live in a structured record store (`docs/vdjscript-verbs.json`) fronted by the `just verb` data API (`get`/`put`/`next-incomplete`/`stats`/`search`). The store is authoritative and hand-editable through `put`; treat the JSON layout as private — go through the `just verb` commands so it can change (e.g. to one file per verb) without breaking your usage. Markdown views are being migrated to generate from it, per `docs/VDJScript Reference Consolidation Plan.md` (frozen design). The store is seeded from the existing index, coverage audit, and tracker via `python3 tools/verbdb.py bootstrap`.

## What is here

```
examples/Pads/                    — working/reference pad page XML files plus copied built-in pad pages
examples/Skins/                   — skin source trees, reference skins, and copied built-in skins
examples/Mappers/                 — real working controller/keyboard mapper XML (ground truth for the mapper format)
examples/Samplerbanks/            — copied built-in sampler-bank XML (third XML format)
tests/                       — documentation test harnesses, including pad XML fixtures
docs/                   — Markdown documentation
```

## Live probe channel: VirtualDJ HTTP interface

When VirtualDJ is running with its network interface enabled, VDJScript can be executed and queried over plain HTTP on `http://localhost/` — no pad fixture or manual readback needed. This is the preferred channel for local-test probes. Full contract, verified behavior, and gotchas: [docs/HTTP Control Interface.md](docs/HTTP%20Control%20Interface.md).

- `just vdj-up` — reachability check; run it before planning any live-test work.
- `just vdj-query 'get_effect_name 1'` — evaluate any VDJScript query; exact result string back. Read-only, use freely for sweeps.
- `just vdj-execute 'effect_active 1'` — run an action; the body is the verb's own `true`/`false` result (not transport success — `nothing` returns `false`).
- Unknown verbs return HTTP 200 with an `error:<code>` body; check the body, not the status.
- Execute only verbs the current task names; never `system` or file/database-touching verbs through this channel.
- Record HTTP-channel results in the tracker with the build, noting the channel.

## Key facts for AI agents

- VirtualDJ skins are XML. The scripting language inside attributes is **VDJScript**.
- `action=""` attributes take VDJScript actions. `query=""` takes a boolean/value expression.
- `&` chains actions in XML attributes and must be written `&amp;` inside XML.
- Backtick-wrapped expressions (`` `verb` ``) evaluate and return a value in string/color contexts.
- Working/reference pad pages live in `examples/Pads/*.xml`; copied built-in app-bundle pages live in `examples/Pads/Built-In/`; documentation test harnesses live under `tests/`. See `examples/Pads/README.md` before choosing a reference page. Skins live in `examples/Skins/*/`; copied built-in app-bundle skins live in `examples/Skins/Built-In/`.
- The pad-page container format is specified in `docs/Pad Page XML.md`; skin waveforms in `docs/Skin Waveforms.md`; the mapper format in `docs/Mapper XML.md` with real mappers in `examples/Mappers/Local/`. `just inventory` regenerates the element-coverage report `docs/Skin XML Inventory.md`.
- `examples/Skins/GraveRaver/src/` is intentionally minimal and demonstrates the build system only. Do not use it as a polished skin reference.
- The official VDJScript appendix coverage and local-test gap are tracked in `docs/Official VDJScript Coverage Audit.md`.
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
- **Computed arguments**: transport-style verbs (`loop`, `beatjump`, `phrase_sync`) ignore backtick-computed arguments even when the literal works — branch to literals (`var_equal '$n' 16 ? loop 16 : loop 32`) or chain params (`get_var '$src' & param_multiply 2 & set '$dst'`); `set` does accept backticks. Tested rules: `docs/VirtualDJ Reference.md` §Tested Grammar Rules.
- **beatjump**: argument must be signed (`beatjump +4`; bare `beatjump 4` is a no-op).

## Working examples in this repo

| File | Demonstrates |
| --- | --- |
| [examples/Pads/Reference - Slot FX.xml](examples/Pads/Reference%20-%20Slot%20FX.xml) | Canonical slot-based audio FX pads |
| [examples/Pads/Reference - ColorFX.xml](examples/Pads/Reference%20-%20ColorFX.xml) | Canonical filter + ColorFX selection |
| [examples/Pads/Reference - Page Aware Sampler.xml](examples/Pads/Reference%20-%20Page%20Aware%20Sampler.xml) | Page-aware sampler labels, colors, actions |
| [examples/Pads/SAMPLER READ ONLY.xml](examples/Pads/SAMPLER%20READ%20ONLY.xml) | Confirmed read-only multi-page sampler with absolute empty-slot guards |
| [examples/Pads/Built-In/README.md](examples/Pads/Built-In/README.md) | Copied VirtualDJ app-bundle pad pages; semi-official executable examples |
| [examples/Pads/COLOR FX.xml](examples/Pads/COLOR%20FX.xml) | ColorFX selection with stems context |
| [examples/Skins/Built-In/README.md](examples/Skins/Built-In/README.md) | Copied VirtualDJ app-bundle skins; semi-official executable examples |
| [examples/Skins/ModularSkeleton/build/skin.xml](examples/Skins/ModularSkeleton/build/skin.xml) | Minimal modular skin scaffold |
| [examples/Skins/GraveRaver/src/skin.xml](examples/Skins/GraveRaver/src/skin.xml) | Minimal XInclude build-system demo, not a skin design reference |

## macOS paths

| Path | Content |
| --- | --- |
| `~/Library/Application Support/VirtualDJ/Pads/` | Installed pad pages |
| `~/Library/Application Support/VirtualDJ/Skins/` | Installed skins |
| `~/Library/Application Support/VirtualDJ/Mappers/` | Controller/keyboard mappings |
| `~/Library/Application Support/VirtualDJ/database.xml` | Main track database |

See [docs/Application Internals.md](docs/Application%20Internals.md) for the full path map, database structure, and stem sidecar layout.
