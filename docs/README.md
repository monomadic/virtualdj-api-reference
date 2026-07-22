# Reference Documentation

This folder is moving toward a reliable local API reference for the VirtualDJ scripting environment.

Start here:

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
  Conservative notes for non-official hidden Button Editor taxonomy rows, including evidence streams, probe order, and promotion rules.

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

- [Skin XML Inventory](Skin%20XML%20Inventory.md)
  Generated element×attribute usage report across built-in/curated skin, pad, samplerbank, and mapper XML, cross-checked against the docs. Regenerate with `just inventory`; do not hand-edit.

- [VDJScript Verb Index (JSON)](vdjscript-verb-index.json)
  Generated machine-readable verb index: every official name with tier (curated/catalog/alias/official-name-only), kind, aliases, and surfaces, parsed from `VDJScript Verbs.md` plus the coverage audit. Regenerate with `just verb-index`; consumed by `tools/lint_mappers.py` and by the verb store bootstrap.

- [VDJScript Verb Record Store (JSON)](vdjscript-verbs.json)
  Authoritative, hand-editable per-verb records: tier, aliases, surfaces, kind, doc coverage, plus local-test status, confidence, and evidence. Query and edit through the `just verb` API — do not hand-edit the JSON and do not generate Markdown copies of it. `search` filters (`--surface`, `--section`, `--tier`, `--status`, `--kind`, `--needs-test`) with `--format=json`, so reports come out of a query on demand rather than a stored listing. Seeded from the index, coverage audit, and tracker via `python3 tools/verbdb.py bootstrap`; validated by `just check`.

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
- `Undocumented VDJScript Candidates.md` tracks the 37 flag1-hidden non-official compiled taxonomy rows separately from the normal VDJScript API reference.
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
- The bundled Button Editor action-description catalog currently has 813 unique action tags across all language files in the local VirtualDJ app, including 14 catalog-only names outside the official appendix; the richer runtime string block adds 21 stricter runtime-only names outside both official and Button Editor catalogs. None of those 35 non-official candidates currently has shipped XML evidence in the copied built-in/official XML roots.
- The compiled Button Editor taxonomy has 37 displayed categories, 918 visible action items, and 1028 total compiled action items. All 918 visible rows are official audit names; 797 have bundled language descriptions; 770 have exact `ACTION_*` method-symbol matches. The taxonomy is useful as category metadata, but not as behavior proof.
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
