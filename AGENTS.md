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

- **Writing VDJScript? Read the summary of [docs/VDJScript Grammar.md](docs/VDJScript%20Grammar.md) first.** Its "Read this much" section is the whole language in about a dozen lines; the Contents list jumps to a section when you need detail. Grammar is the one thing lookup cannot save you on — the parser reports no syntax errors, so wrong script silently does something else. Not writing script (skin layout, XML structure, file format work)? Skip it.
- **Never read the large docs end-to-end.** `docs/VDJScript Verbs.md` (~6,300 lines), `docs/Skin SDK.md` (~2,700 lines), `docs/Effects Engines.md`, `docs/VirtualDJ Reference.md`, and `docs/VDJScript Local Test Tracker.md` are section-addressed references. Read only the section a task names, or extract it with path-scoped `rg`/`awk`.
- **Look verbs up through the tooling, not the monolith.** `just get-verb <name>` is the lookup — it follows aliases and suggests near matches on a miss. `just find-verbs <term>` when you do not know the name. Open `VDJScript Verbs.md` only at the specific lines a search hit points to.
- **Record a settled verb fact with `just put-verb`, not by hand-editing tables.** A per-verb conclusion — status, confidence, evidence — goes into the store once (`just put-verb <name> test_status=Pass confidence=local_test evidence="…"`), not promoted into the tracker and topical docs by hand. The tracker is for the *run narrative* that does not reduce to one verb (see the Live probe section); the store is the authoritative per-verb record. A tested status without evidence fails `just check`.
- **Effect controls come from the FX catalog, not prose tables.** `just get-fx Echo` gives the full slider/button map with normalized defaults (spelling-tolerant: `BeatGrid` resolves to `Beat Grid`, `Shader` to its canonical `Visuals`); `just find-fx --category=video_fx`, `--has-button=quant`, `--min-sliders=6`, `--has-length`, `--format=json` answer the rest. Do not hand-transcribe the catalog into Markdown.
- **Introspect effects by name, without loading them.** Every `get_effect_*` helper accepts an effect name where the docs show a slot number — `just vdj-query "get_effect_slider_count 'Echo'"`, `get_effect_slider_default 'Echo' 3` — so a live question about an effect needs no `effect_select` and changes no state. `get_effect_title '<name>'` returns `'<Canonical> - Deck N'` or `''`, which resolves spellings and probes existence in one call.
- **Query the store instead of reading listings.** `just find-verbs` filters — `--surface`, `--section`, `--tier`, `--status`, `--kind`, `--needs-test` — and `--format=json` for structured output. Ask for the verbs you need (`just find-verbs --surface=SkinQuery --section=Sampler`); do not pull a category listing and filter it yourself. `just next-incomplete-verb` gives the next active (non-hardware-blocked) work item, `just verb-stats` the breakdown.
- **Planning docs are frozen.** `docs/VDJScript Reference Consolidation Plan.md` and `docs/Completeness Roadmap.md` are design references, not active state. Do not refresh, reorder, or re-scope them; do not spend turns rewriting planning prose or reordering the TODO queue. `TODO.md` is the only active planning state, and it changes when a task completes or the user asks.
- **Probe over HTTP first, fixtures second.** When VirtualDJ is running with the network interface enabled (`just vdj-up` to check), read values with `just vdj-query` instead of pad readback. Pad/skin fixtures remain necessary only for surface-specific behavior (rendering, pad context, skin runtime). Batch every probe a live session can carry, and prefer dump-style sweeps over one-question rounds.
- **Delegate mechanical passes.** Transcribing observed values into tables, promoting settled tracker rows, and lint fixes are cheap-model subagent work; keep the main context for evidence interpretation and ambiguous calls.
- Prefer `INDEX.yml`, `just next-task`, `just grep-verb-docs <name>`, and path-scoped `rg` over repo-wide discovery; broaden only after the task route proves insufficient or contradictory.
- Keep volatile coverage counts sourced from `docs/Official VDJScript Coverage Audit.md`; do not repeat exact count summaries in entrypoint docs unless the checker intentionally enforces them.

Direction of travel: verb facts live in a structured record store (`docs/vdjscript-verbs.json`) reached only through flat `just` data commands — `get-verb`, `find-verbs`, `put-verb`, `next-incomplete-verb`, `verb-stats` (and `get-fx`, `find-fx`, `fx-stats` for effects). The command name is always a command and the argument is always data, so a verb called `search` or `get` can never be mistaken for a subcommand. Treat the JSON layout as private — go through the commands so storage can change (e.g. to one file per verb) without breaking your usage. Reports are queries on stdout: **do not add a generator that writes a Markdown copy of store data.** The store is seeded from the existing index, coverage audit, and tracker via `python3 tools/verbdb.py bootstrap`.

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
- Recording a result has two destinations, and they hold different things. The **verb store is authoritative for per-verb conclusions**: `just put-verb <name> test_status=… confidence=local_test evidence="…"` — one verb, one settled fact, with the build in the evidence string. The **tracker holds the run narrative** for a session that does not reduce to a single verb: a fixture setup, a negative result, a multi-verb probe, cross-verb interactions. A tested status in the store with no evidence now fails `just check`, so record the evidence at the same time as the status, not later. Note the channel (HTTP vs pad) in the evidence, since some behavior is surface-specific.

## Key facts for AI agents

- VirtualDJ skins are XML. The scripting language inside attributes is **VDJScript**.
- `action=""` attributes take VDJScript actions. `query=""` takes a boolean/value expression.
- `&` chains actions in XML attributes and must be written `&amp;` inside XML.
- Backtick-wrapped expressions (`` `verb` ``) evaluate and return a value in string/color contexts.
- Working/reference pad pages live in `examples/Pads/*.xml`; copied built-in app-bundle pages live in `examples/Pads/Built-In/`; documentation test harnesses live under `tests/`. See `examples/Pads/README.md` before choosing a reference page. Skins live in `examples/Skins/*/`; copied built-in app-bundle skins live in `examples/Skins/Built-In/`.
- The pad-page container format is specified in `docs/Pad Page XML.md`; skin waveforms in `docs/Skin Waveforms.md`; the mapper format in `docs/Mapper XML.md` with real mappers in `examples/Mappers/Local/`. `just inventory` refreshes the element-coverage data `docs/skin-xml-inventory.json`; query it with `just get-xml-element <name>` / `just find-xml-elements --undocumented`.
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
