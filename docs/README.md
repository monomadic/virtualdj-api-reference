# Reference Documentation

This folder is moving toward a reliable local API reference for the VirtualDJ scripting environment.

Start here:

- [Evidence Standards](Evidence%20Standards.md)
  **Governs every claim in this repository.** What counts as proof (the four live-observation channels) versus a lead (forums, unbacked binary analysis, official example files); the existence/kind/behavior distinction; why a channel's own return value is not a result; and how the existing source labels map onto the tiers. Read before recording a finding.

- [VirtualDJ Reference](VirtualDJ%20Reference.md)
  Method choices, source policy, quirks, and preferred patterns.

- [Active Task Queue](../TODO.md)
  Current startable maintenance and evidence-pass tasks.

- [Routing Index](../INDEX.yml)
  Topic-to-file map for cheaper navigation.

- [VDJScript Verbs](VDJScript%20Verbs.md)
  Curated API reference for high-frequency verbs, alias handling, and scripting surfaces.

- [Official VDJScript Coverage Audit](Official%20VDJScript%20Coverage%20Audit.md)
  Names-only audit comparing the live official VDJScript appendix against this repo's local verb reference.

- [Completeness Roadmap](Completeness%20Roadmap.md)
  Evidence backlog for turning searchable names and source hints into locally observed, curated guidance.

- [Button Editor Catalog Audit](Button%20Editor%20Catalog%20Audit.md)
  Local cross-check of the VDJScript action descriptions bundled in VirtualDJ's Button Editor language resources, plus binary string-table counts.

- [Button Editor Taxonomy](Button%20Editor%20Taxonomy.md)
  Extracted Button Editor category mapping from the compiled executable tables, including visible/hidden counts and symbol-capability joins.

- [Undocumented VDJScript Candidates](Undocumented%20VDJScript%20Candidates.md)
  Where the **verb table** lives: VirtualDJ's own serialised verb set (1,032 records on build 18.0.9598, arm64, extracted 2026-09-05 — name, id, flags, Button Editor category; `just verb-table-stamp`), which decides existence and non-existence outright (`just verb-table <name>`, Evidence Standards rule 1). Also the hidden-verb notes, probe order, and promotion rules.

- [VDJScript Grammar](VDJScript%20Grammar.md)
  The language itself: chaining, conditionals, quoting, scope prefixes, and the traps. Read its summary before writing VDJScript; jump via its Contents for detail. Per-verb argument rules are not here — those are `just get-verb <name>`.

- **Verb arguments live in artifacts, not prose.** What a verb's *tail* accepts is answered by
  four independent sources under `tests/`, deliberately kept apart because they fail in
  different places: `action-catalog.json` (the vendor's own descriptions, shipped in the app
  bundle — what a parameter *means*), `attested-tails.json` (tails Atomix wrote into shipped
  skins, pad pages and the app's own compiled menu scripts — that a token is *used* — and
  argument shapes with return evidence for value-taking verbs),
  `binary-vocabularies.json` (shared enumerations recovered as binary structures — the *rest*
  of a vocabulary a verb draws from, as leads), and `verb-arg-forms.json` (probed against
  nonsense controls in 10 named fixtures — that a token is *not nonsense*). Read them all at once with
  `just verb <name>`, or one at a time with `just action-catalog --get <name>`,
  `just attested-tails --verb <name>`, `just binary-vocab --verb <name>`,
  `just verb-arg-forms <name>`, and diff catalog, corpus and probe with
  `just action-catalog --cross-check`.
  See [../tests/README.md](../tests/README.md) for what each artifact proves and does not.

- [VDJScript Syntax Evidence](VDJScript%20Syntax%20Evidence.md)
  Local notes on Button Editor syntax highlighting, hover tokenization, parser symbols, and conditional grammar test targets.

- [VDJScript Local Test Tracker](VDJScript%20Local%20Test%20Tracker.md)
  Manual verification matrix for sparse, hardware-specific, and environment-dependent official verbs.

- [Published Skin Findings](Published%20Skin%20Findings.md)
  Source-backed notes from working public skins, including undocumented-looking commands, provenance, and local test plans.

- [Lyrics AI and Skins](Lyrics%20AI%20and%20Skins.md)
  Focused notes on VirtualDJ 2026 AI lyric detection, skin styling limits, lyric queries, filters, and forum-observed quirks.

- [Mapper XML](Mapper%20XML.md)
  Controller and keyboard mapper file format: the `<mapper>`/`<map value="">` split model, special control names (`ONINIT`, `SHIFT_*`, `LED_*`), device-definition XML (MIDI and HID), and the relationship to pad pages. Ground truth in [examples/Mappers/Local/](../examples/Mappers/README.md).

- [Pad Page XML](Pad%20Page%20XML.md)
  Formal pad-page container schema: `<page>` attributes, `<padN>`/`<shift_padN>` attribute surface, `<param1>`/`<param2>`, the `<menu>` mini-DSL, `<custompadsmode>`, color forms, and samplerbank XML.

- [Skin Waveforms](Skin%20Waveforms.md)
  The waveform/rhythm skin element family: `<rhythmzone>`, `<scratchwave>`, `<songpos>`, `<scratch>`, `<blockwave>`, `<beattunnel>`, their children (`<colors>`, `<grid>`, `<cue>`, `<overlay>`, ...), and how they differ from `visual type="waveform"`.

- [Plugin SDK](Plugin%20SDK.md)
  VirtualDJ's C++ native-code extension point — and the boundary where VDJScript return values are still typed (`GetInfo` → `double`, `GetStringInfo` → text, `SendCommand` → execute). Interface hierarchy, `VDJPARAM_*` parameter model and the `[autoparams]` manifest that all 173 built-in plugins use, plugin UI models, loading, and the interfaces present in the binary that the public headers never declare. The headers themselves are third-party and deliberately not vendored here.

- [Skin XML Inventory (JSON)](skin-xml-inventory.json)
  Element×attribute usage data across built-in/curated skin, pad, samplerbank, video-skin, and mapper XML, cross-checked against the docs. Refresh with `just inventory`; query with `just get-xml-element <name>`, `just find-xml-elements --undocumented`, `just xml-stats`. Do not hand-edit and do not generate a Markdown copy.

- [VDJScript Verb Index (JSON)](vdjscript-verb-index.json)
  Generated machine-readable verb index: every official name with tier (curated/catalog/alias/official-name-only), kind, aliases, and surfaces, parsed from `VDJScript Verbs.md` plus the coverage audit. Regenerate with `just verb-index`; consumed by `tools/lint_mappers.py` and by the verb store bootstrap.

- [VDJScript Verb Record Store (JSON)](vdjscript-verbs.json)
  **Start every per-verb question with `just get-verb <name>`** — it now joins the store record with the verb table (id, category, aliases, hidden flag, or the rule-1b disproof), the structural contract (class, family, capability, arg demands, keyword candidates), the HTTP existence probe, and the observed return type, at read time. `--raw` returns the bare store record. Authoritative, hand-editable per-verb records: tier, aliases, surfaces, kind, doc coverage, plus local-test status, confidence, and evidence. Query and edit through the `just verb` API — do not hand-edit the JSON and do not generate Markdown copies of it. `search` filters (`--surface`, `--section`, `--tier`, `--status`, `--kind`, `--needs-test`) with `--format=json`, so reports come out of a query on demand rather than a stored listing. Seeded from the index, coverage audit, and tracker via `python3 tools/verbdb.py bootstrap`; validated by `just check`.

- [Tools](../tools/README.md)
  Validator/generator suite (`just check` gates) and the version-pinned binary-extraction pipeline, including the new-VirtualDJ-build refresh procedure.

- [Pad Page Inventory](../examples/Pads/README.md)
  Current `examples/Pads/*.xml` status labels, canonical examples, built-in pad-page copies, and maintenance checklist.

- [Skin Inventory](../examples/Skins/README.md)
  Local skin examples, copied built-in skins, and build-system demos.

- [Skin Runtime Findings](Skin%20Runtime%20Findings.md)
  Local-test notes for skin placeholder substitution, conditional placement,
  and other runtime behavior promoted from skin project experiments.

- [Documentation Tests](../tests/README.md)
  Reproducible local test harnesses used to support reference claims.

- [HTTP Control Interface](HTTP%20Control%20Interface.md)
  Local HTTP execute/query channel for VDJScript: endpoints, verified request/response behavior, gotchas, and the `just vdj-query` / `just vdj-execute` probe workflow. The preferred channel for local-test probes.

- [Remote Protocol](Remote%20Protocol.md)
  Wire protocol for the VirtualDJ Remote companion app: `_vdjremote8._tcp` discovery, inverted client/server roles, `8JDV` framing, and the VDJScript query-subscription push model. Distinct from the HTTP interface.

- [Application Internals](Application%20Internals.md)
  Low-level macOS-first notes on VirtualDJ paths, databases, caches, stem sidecars, linked tracks, and shell tooling.

- [VirtualDJ Stem File Format](Stem%20File%20Format.md)
  Focused `.vdjstems` sidecar format notes: Matroska container, five-stream order, stream-title metadata, inspection commands, and MP4/standalone caveats.

- [Resources](Resources.md)
  Useful official, staff, community, and local sources for follow-up research.

Current status:

- `VirtualDJ Reference.md` is the policy and architecture layer.
- `VDJScript Verbs.md` is the first API-focused pass.
- `Official VDJScript Coverage Audit.md` tracks official verb coverage depth, missing-name status, and the remaining local-test gap.
- `Button Editor Catalog Audit.md` tracks the bundled Button Editor action-description catalog and runtime string-table cross-checks.
- `Button Editor Taxonomy.md` tracks the compiled Button Editor category mapping and metadata join: 37 displayed categories, 918 visible actions, 1028 compiled action items, and exact `ACTION_*` method-symbol coverage.
- `Undocumented VDJScript Candidates.md` hosts the authoritative verb table (existence, aliases, hidden flag, categories) and tracks the 37 hidden verbs separately from the normal VDJScript API reference.
- `VDJScript Syntax Evidence.md` tracks the separate parser/highlighter evidence stream for grammar and conditional semantics.
- `VDJScript Local Test Tracker.md` is the default place to record manual VirtualDJ verification runs for `Needs local test` verbs.
- `Completeness Roadmap.md` is a frozen snapshot of evidence tiers and hardware gates; the active queue is `TODO.md`.
- `Published Skin Findings.md` tracks empirical commands and skin idioms before they are fully folded into the curated reference.
- `Skin Runtime Findings.md` tracks local skin runtime behavior that should be shared across projects rather than kept in one skin repo.
- `Lyrics AI and Skins.md` is the focused lyric/autodetection reference.
- `Application Internals.md` is the low-level file/database/stem architecture reference.
- `Stem File Format.md` is the focused file-format reference for `.vdjstems` sidecars.
- `Resources.md` is the source index.
- Current official coverage and local-test gap counts are tracked in `Official VDJScript Coverage Audit.md`.
- **Existence is settled** (method established 2026-07-27): the verb table in the binary is the complete verb set for the build it was read from — 1,032 records / 958 distinct verbs / 62 alias groups / 38 editor-hidden on build 18.0.9598 (arm64, extracted 2026-09-05), every one categorised. Quote that stamp from `just verb-table-stamp`; the July figures (1,028 / 955 / 61 / 37) were an earlier build's and are superseded, not corrected. `just verb-table <name>` answers membership, aliasing, hidden flag, and category in one query. Absence from the table is disproof on the inspected build. The older catalog/string-table counts below it in the history are corroboration only.
- The compiled Button Editor taxonomy doc remains useful as category *metadata* (and its example column has been corrected against the verb table), but the verb table is the authority; neither is behavior proof.
- Button Editor syntax highlighting and hover tokenization are now tracked as parser evidence, with `DLGActionWizard::STree`, `customDraw`, `getCurrentWord`, and related symbols as the current binary anchors.
- The other topical files still contain useful raw material, but they are not yet normalized to the same reliability standard.

Source labels used in the curated docs:

- `Official`: current VirtualDJ manual or VDJPedia.
- `Official forum`: VirtualDJ staff, Development Manager, CTO, or Support staff forum guidance. Treat Adion/CTO replies as high-authority implementation notes when they answer scripting, audio-engine, or feature-behavior questions; VirtualDJ forum badges identify Adion as CTO, and Atomix's own press archive confirms Atomix Productions acquired AdionSoft in 2011.
- `Community`: forum moderators, non-staff forum users, Reddit posts, or other community examples.
- `Published skin`: command or pattern observed in a working public skin.
- `Built-in skin`: command or pattern observed in skin XML shipped inside the VirtualDJ app bundle.
- `Published pad page`: command or pattern observed in a working public pad page.
- `Built-in pad page`: command or pattern observed in pad-page XML shipped inside the VirtualDJ app bundle.
- `Built-in app resource`: command name, description, or UI catalog entry observed in non-skin/non-pad resources shipped inside the VirtualDJ app bundle, such as `Resources/languages.zip`.
- `Binary compiled table`: structured command metadata observed in compiled executable tables; useful for UI taxonomy and visibility evidence, not behavior evidence by itself.
- `Binary symbol table`: demangled implementation symbols observed in the VirtualDJ executable; useful for action-class and method-surface hints such as `onExecute`/`onQuery`, not behavior evidence by itself.
- `Binary string-table`: command-looking string observed in the VirtualDJ executable; use for discovery only, not as behavior evidence.
- `Local test`: behavior reproduced in VirtualDJ locally.
- `Inference`: conclusion drawn from official docs plus repo testing or architecture.

## Dated review records

- [Repository assessment, 2026-09-05](Repository%20Assessment%20and%20Prioritized%20Tasks.md) — diagnosis and review decisions; accepted work is maintained only in TODO.md.
