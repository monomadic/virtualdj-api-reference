# Reference Documentation

This folder is moving toward a reliable local API reference for the VirtualDJ scripting environment.

Start here:

- [VirtualDJ Reference](VirtualDJ%20Reference.md)
  Method choices, source policy, quirks, and preferred patterns.

- [VDJScript Verbs](VDJScript%20Verbs.md)
  Curated API reference for high-frequency verbs, alias handling, and scripting surfaces.

- [Official VDJScript Coverage Audit](Official%20VDJScript%20Coverage%20Audit.md)
  Names-only audit comparing the live official VDJScript appendix against this repo's local verb reference.

- [Button Editor Catalog Audit](Button%20Editor%20Catalog%20Audit.md)
  Local cross-check of the VDJScript action descriptions bundled in VirtualDJ's Button Editor language resources, plus binary string-table counts.

- [Button Editor Taxonomy](Button%20Editor%20Taxonomy.md)
  Extracted Button Editor category mapping from the compiled executable tables, including visible and hidden action counts.

- [VDJScript Syntax Evidence](VDJScript%20Syntax%20Evidence.md)
  Local notes on Button Editor syntax highlighting, hover tokenization, parser symbols, and conditional grammar test targets.

- [VDJScript Local Test Tracker](VDJScript%20Local%20Test%20Tracker.md)
  Manual verification matrix for sparse, hardware-specific, and environment-dependent official verbs.

- [Published Skin Findings](Published%20Skin%20Findings.md)
  Source-backed notes from working public skins, including undocumented-looking commands, provenance, and local test plans.

- [Lyrics AI and Skins](Lyrics%20AI%20and%20Skins.md)
  Focused notes on VirtualDJ 2026 AI lyric detection, skin styling limits, lyric queries, filters, and forum-observed quirks.

- [Mapper XML](Mapper%20XML.md)
  Controller and keyboard mapper file format: `<map>`, `<button>`, `<slider>`, `<knob>`, shift layers, LED feedback, device-definition boundaries, and the relationship to pad pages.

- [Pad Page Inventory](../Pads/README.md)
  Current `Pads/*.xml` status labels, canonical examples, built-in pad-page copies, and maintenance checklist.

- [Skin Inventory](../Skins/README.md)
  Local skin examples, copied built-in skins, and build-system demos.

- [Skin Runtime Findings](Skin%20Runtime%20Findings.md)
  Local-test notes for skin placeholder substitution, conditional placement,
  and other runtime behavior promoted from skin project experiments.

- [Documentation Tests](../Test/README.md)
  Reproducible local test harnesses used to support reference claims.

- [Application Internals](Application%20Internals.md)
  Low-level macOS-first notes on VirtualDJ paths, databases, caches, stem sidecars, linked tracks, and shell tooling.

- [Resources](Resources.md)
  Useful official, staff, community, and local sources for follow-up research.

Current status:

- `VirtualDJ Reference.md` is the policy and architecture layer.
- `VDJScript Verbs.md` is the first API-focused pass.
- `Official VDJScript Coverage Audit.md` tracks official verb coverage depth, missing-name status, and the remaining local-test gap.
- `Button Editor Catalog Audit.md` tracks the bundled Button Editor action-description catalog and runtime string-table cross-checks.
- `Button Editor Taxonomy.md` tracks the compiled Button Editor category mapping: 37 displayed categories, 918 visible actions, and 1028 compiled action items.
- `VDJScript Syntax Evidence.md` tracks the separate parser/highlighter evidence stream for grammar and conditional semantics.
- `VDJScript Local Test Tracker.md` is the default place to record manual VirtualDJ verification runs for `Needs local test` verbs.
- `Published Skin Findings.md` tracks empirical commands and skin idioms before they are fully folded into the curated reference.
- `Skin Runtime Findings.md` tracks local skin runtime behavior that should be shared across projects rather than kept in one skin repo.
- `Lyrics AI and Skins.md` is the focused lyric/autodetection reference.
- `Application Internals.md` is the low-level file/database/stem architecture reference.
- `Resources.md` is the source index.
- Current VDJScript coverage is 991/991 official verb/alias names present, 0 missing, and an empty compact official remainder; 20 official names remain in the formal `Needs local test` gap.
- The bundled Button Editor action-description catalog currently has 813 unique action tags across all language files in the local VirtualDJ app, including 14 catalog-only names outside the official appendix; the richer runtime string block adds 21 stricter runtime-only names outside both official and Button Editor catalogs. None of those 35 non-official candidates currently has shipped XML evidence in the copied built-in/official XML roots.
- The compiled Button Editor taxonomy has 37 displayed categories, 918 visible action items, and 1028 total compiled action items; it is useful as category metadata but not as behavior proof.
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
- `Binary string-table`: command-looking string observed in the VirtualDJ executable; use for discovery only, not as behavior evidence.
- `Local test`: behavior reproduced in VirtualDJ locally.
- `Inference`: conclusion drawn from official docs plus repo testing or architecture.
