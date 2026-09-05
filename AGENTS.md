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
- **Start a "how do I do X" task with `just topic X`.** It aggregates, for one term, the matching verbs, effects, and skin/pad XML elements, plus the *real example files that use them* (grep-verified, ranked by how much of the topic each demonstrates), the topical docs, and known local-test quirks. A working example often answers the task outright, leaving only per-verb detail to look up. `just topic sampler`, `just topic colorfx`, `--format=json` for structure. Drill in with `get-verb` / `get-fx` / `get-xml-element` afterward.
- **Look verbs up through the tooling, not the monolith.** `just verb <name>` is the one-screen summary — store record, vendor description, real usages, argument shapes with return evidence, every tail candidate by source, vocabulary groups, probe state, each labelled with its evidence tier (`--format=json` for structure). `just get-verb <name>` is the bare store record — it follows aliases and suggests near matches on a miss. `just find-verbs <term>` when you do not know the name. Open `VDJScript Verbs.md` only at the specific lines a search hit points to.
- **Record a settled verb fact with `just put-verb`, not by hand-editing tables.** A per-verb conclusion — status, confidence, evidence — goes into the store once (`just put-verb <name> test_status=Pass confidence=local_test evidence="…"`), not promoted into the tracker and topical docs by hand. The tracker is for the *run narrative* that does not reduce to one verb (see the Live probe section); the store is the authoritative per-verb record. A tested status without evidence fails `just check`.
- **Effect controls come from the FX catalog, not prose tables.** `just get-fx Echo` gives the full slider/button map with normalized defaults (spelling-tolerant: `BeatGrid` resolves to `Beat Grid`, `Shader` to its canonical `Visuals`); `just find-fx --category=video_fx`, `--has-button=quant`, `--min-sliders=6`, `--has-length`, `--format=json` answer the rest. Do not hand-transcribe the catalog into Markdown.
- **Introspect effects by name, without loading them.** Every `get_effect_*` helper accepts an effect name where the docs show a slot number — `just vdj-query "get_effect_slider_count 'Echo'"`, `get_effect_slider_default 'Echo' 3` — so a live question about an effect needs no `effect_select` and changes no state. `get_effect_title '<name>'` returns `'<Canonical> - Deck N'` or `''`, which resolves spellings and probes existence in one call.
- **Query the store instead of reading listings.** `just find-verbs` filters — `--surface`, `--section`, `--tier`, `--status`, `--kind`, `--needs-test` — and `--format=json` for structured output. Ask for the verbs you need (`just find-verbs --surface=SkinQuery --section=Sampler`); do not pull a category listing and filter it yourself. `just next-incomplete-verb` gives the next active (non-hardware-blocked) work item, `just verb-stats` the breakdown.
- **Planning docs are frozen.** `docs/VDJScript Reference Consolidation Plan.md` and `docs/Completeness Roadmap.md` are design references, not active state. Do not refresh, reorder, or re-scope them; do not spend turns rewriting planning prose or reordering the TODO queue. `TODO.md` is the only active planning state, and it changes when a task completes or the user asks.
- **Probe over HTTP first, fixtures second.** When VirtualDJ is running with the network interface enabled (`just vdj-up` to check), read values with `just vdj-query` instead of pad readback. Pad/skin fixtures remain necessary only for surface-specific behavior (rendering, pad context, skin runtime). Batch every probe a live session can carry, and prefer dump-style sweeps over one-question rounds.
- **Delegate mechanical passes.** Transcribing observed values into tables, promoting settled tracker rows, and lint fixes are cheap-model subagent work; keep the main context for evidence interpretation and ambiguous calls.
- Prefer `INDEX.yml`, `just next-task`, `just grep-verb-docs <name>`, and path-scoped `rg` over repo-wide discovery; broaden only after the task route proves insufficient or contradictory.
- **Never write a bare count.** Every number in this repo is either a measurement of one build or a total derived from a regenerable artifact, and each has its own rule. The test is: *would this sentence become false if a binary were updated or an artifact regenerated?* If yes, it is not written as a bare figure.
  - **Build-anchored counts are stamped, not refreshed.** Write `1,032 records on build 18.0.9598 (arm64, extracted 2026-09-05)`, never `1,032 records`. A stamped figure is permanent evidence about that build and must never be silently updated — a newer build gets a *new* stamped line, and the old one stays as the record of what the old build held. **Copy the stamp, never recall it:** `just verb-table-stamp` prints the exact phrase from the artifact's own summary. Recalling it is how `README.md` came to attribute one extraction's counts to a build the commit message disagreed with.
  - **Derived totals are not written at all.** Corpus size, fixture count, probe/form totals, cross-check set sizes: name the command and the field that answers (`just action-catalog --cross-check` → `documented_but_not_probe_confirmed`), not the number. These have no build to anchor them and go wrong on the next regeneration — usually in a commit that never opened the file.
  - **Dated observations keep their numbers, frozen.** "A 32,000-query sweep on build 9598 established the two-token grammar" is evidence; it describes a past run and stays true. A date alone does not license a count — `(2026-07-27): the verb table is the complete verb set — 1,028 records` reads as dated but asserts *current* state, and that is the shape to avoid.
  - The two counts in `docs/Official VDJScript Coverage Audit.md` are the exception: `tools/check_reference_status.py` enforces them, so they may be written plainly.

Direction of travel: verb facts live in a structured record store (`docs/vdjscript-verbs.json`) reached only through flat `just` data commands — `get-verb`, `find-verbs`, `put-verb`, `next-incomplete-verb`, `verb-stats` (and `get-fx`, `find-fx`, `fx-stats` for effects). The command name is always a command and the argument is always data, so a verb called `search` or `get` can never be mistaken for a subcommand. Treat the JSON layout as private — go through the commands so storage can change (e.g. to one file per verb) without breaking your usage. Reports are queries on stdout: **do not add a generator that writes a Markdown copy of store data.** The store is seeded from the existing index, coverage audit, and tracker via `python3 tools/verbdb.py bootstrap`.

## What is here

```
examples/Pads/                    — working/reference pad page XML files plus copied built-in pad pages
examples/Skins/                   — skin source trees, reference skins, and copied built-in skins
examples/Mappers/                 — real working controller/keyboard mapper XML (ground truth for the mapper format)
examples/Samplerbanks/            — copied built-in sampler-bank XML (third XML format)
tests/                       — documentation test harnesses, pad XML fixtures, and the evidence artifacts
                                  (verb-table, action-contracts, action-catalog, verb-arg-forms,
                                   attested-tails, vdjscript-corpus — see tests/README.md)
docs/                   — Markdown documentation
```

## Live probe channel: VirtualDJ HTTP interface

When VirtualDJ is running with its network interface enabled, VDJScript can be executed and queried over plain HTTP on `http://localhost/` — no pad fixture or manual readback needed. This is the preferred channel for local-test probes. Full contract, verified behavior, and gotchas: [docs/HTTP Control Interface.md](docs/HTTP%20Control%20Interface.md).

- `just vdj-up` — reachability check; run it before planning any live-test work.
- `just vdj-query 'get_effect_name 1'` — evaluate any VDJScript query; exact result string back. Read-only, use freely for sweeps.
- `just vdj-execute 'effect_active 1'` — run an action; the body is the verb's own `true`/`false` result (not transport success — `nothing` returns `false`).
- Unknown verbs return HTTP 200 with an `error:<code>` body; check the body, not the status.
- Execute only verbs the current task names; never `system` or file/database-touching verbs through this channel.
- **Before probing a verb's arguments, read what is already known.** `just action-catalog --get
  <name>` gives the vendor's own description and its documented parameters; `just attested-tails
  --verb <name>` gives tails Atomix wrote in shipped scripts **and the argument shapes with
  their return evidence** (`` fadeout DUR DUR `BOOL` ``, seen in `visibility=`), which is the only
  record for the 167 verbs whose arguments are values rather than keywords; `just binary-vocab --verb <name>`
  gives the shared enumeration the verb draws from (stem names, colours, settings pages) with
  the members no other source names; `just verb-arg-forms <name>` gives what has already been
  probed. `get_song_event`'s two-token grammar was established by a 32,000
  query sweep and had been documented in the app bundle the whole time.
- **Probing arguments needs prepared state and nonsense controls.** An unrecognized argument is
  silently ignored, so a verb answering proves nothing: `just fixtures` lists the 10 named
  states, and `tools/probe_arg_forms.py` compares every candidate against two junk tokens inside
  each. Separation is positive evidence; failing to separate means the state did not
  discriminate, *not* that the token is unreal.
- **Time-varying verbs manufacture false positives.** `get_cpu`, `get_time` and `record_vu`
  separate from a control by drift alone. `--repeat N` catches fast drift; only two independent
  runs catch slow drift.
- **Executing verbs to test them writes to a live instance.** `tools/probe_execute_forms.py`
  shows the shape that is acceptable: an allowlist, a round-trip test before probing, restore
  and verify after every form, and abort on a failed restore. `timecode_cd_mode` is why — it can
  be set from script and only a restart clears it.
- **A second live channel exists: the read-only introspection plugin.** Where HTTP flattens a
  result to a string, the plugin sees the native call — `GetInfo` → `double`,
  `GetStringInfo` → text, **and the `HRESULT` separately from the value**, which is the only way
  to tell a recognized keyword from a silently-ignored one, and it needs no prepared state.
  `just plugin-status` / `just plugin-probe <name>` read the existing captures
  (`tests/plugin-introspection*.json`); `just plugin-build` then `just plugin-collect` take a new
  one. Two method rules learned the hard way: an `E_INVALIDARG` from a load-time probe means
  "not available now", not "no such form" — re-take negatives from the delayed sweep
  (`just plugin-collect-late`); and VirtualDJ writes `0.0` to `*result` even on failure, so the
  HRESULT is the answer, not the value. Full evidence table: the tracker's "Plugin Channel
  (VDJIntrospect)" section.
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
- **[docs/Evidence Standards.md](docs/Evidence%20Standards.md) governs every claim in this repo — read it before recording a finding.** Three tiers: only direct observation of the running app (network protocol, HTTP interface, live pad tests, agent driving the window) proves that something *works*; forums, unbacked binary analysis, and official example files are *leads*; everything else is not recorded. Existence, kind, and behavior are separate claims. A channel's own return value is not a result. The binary can disprove a name even though it cannot prove behavior.
- Source labels (`Official`, `Official forum`, `Community`, `Published skin`, `Built-in skin`, `Published pad page`, `Built-in pad page`, `Action catalog`, `Vendor script`, `Local test`, `Inference`) appear throughout the reference docs; Evidence Standards maps each onto its tier.
- **The official verbs appendix ships inside the app.** `Resources/languages.zip` → `English.xml`
  → `<Actions>` is the same prose virtualdj.com publishes, so 816 verb descriptions — including
  parameter lists — are readable offline via `just action-catalog`. Do not fetch the manual for
  something the bundle already answers.
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

| File | Status | Demonstrates |
| --- | --- | --- |
| [examples/Pads/Quarantine/Reference - Slot FX.xml](examples/Pads/Quarantine/Reference%20-%20Slot%20FX.xml) | Quarantined (personal) | Slot-based audio FX pads |
| [examples/Pads/Quarantine/Reference - ColorFX.xml](examples/Pads/Quarantine/Reference%20-%20ColorFX.xml) | Quarantined (personal) | Filter + ColorFX selection |
| [examples/Pads/Quarantine/SAMPLER READ ONLY.xml](examples/Pads/Quarantine/SAMPLER%20READ%20ONLY.xml) | Quarantined (personal) | Confirmed read-only multi-page sampler with absolute empty-slot guards |
| [examples/Pads/Built-In/README.md](examples/Pads/Built-In/README.md) | Built-in | Copied VirtualDJ app-bundle pad pages; semi-official executable examples |
| [examples/Skins/Built-In/README.md](examples/Skins/Built-In/README.md) | Built-in | Copied VirtualDJ app-bundle skins; semi-official executable examples |
| [examples/Skins/ModularSkeleton/build/skin.xml](examples/Skins/ModularSkeleton/build/skin.xml) | Unofficial (project-authored) | Minimal modular skin scaffold |
| [examples/Skins/GraveRaver/src/skin.xml](examples/Skins/GraveRaver/src/skin.xml) | Unofficial (project-authored) | Minimal XInclude build-system demo, not a skin design reference |
| [examples/Pads/Quarantine/Reference - Page Aware Sampler.xml](examples/Pads/Quarantine/Reference%20-%20Page%20Aware%20Sampler.xml) | Quarantined (personal, superseded) | Page-aware sampler labels, colors, actions — see [examples/Pads/README.md](examples/Pads/README.md) before citing |
| [examples/Pads/Quarantine/COLOR FX.xml](examples/Pads/Quarantine/COLOR%20FX.xml) | Quarantined (personal) | ColorFX selection with stems context |

**No pad page in this repo is `Canonical` any more** (2026-09-04): the three `Reference - *` pages were quarantined, so `Built-in` rows — Atomix's own shipped pages — are now the only pad source to copy patterns from or cite as evidence. `Quarantined` rows are real personal working files kept as usage examples only; **never cite one as evidence that a verb exists or behaves a given way**, because a personal page legitimately contains experiments that were never claimed to work. See [examples/Pads/README.md](examples/Pads/README.md) and [examples/Mappers/README.md](examples/Mappers/README.md) for the full provenance tables.

## macOS paths

| Path | Content |
| --- | --- |
| `~/Library/Application Support/VirtualDJ/Pads/` | Installed pad pages |
| `~/Library/Application Support/VirtualDJ/Skins/` | Installed skins |
| `~/Library/Application Support/VirtualDJ/Mappers/` | Controller/keyboard mappings |
| `~/Library/Application Support/VirtualDJ/database.xml` | Main track database |

See [docs/Application Internals.md](docs/Application%20Internals.md) for the full path map, database structure, and stem sidecar layout.
