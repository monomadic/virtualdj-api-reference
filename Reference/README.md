# Reference Documentation

This folder is moving toward a reliable local API reference for the VirtualDJ scripting environment.

Start here:

- [VirtualDJ Reference](VirtualDJ%20Reference.md)
  Method choices, source policy, quirks, and preferred patterns.

- [VDJScript Verbs](VDJScript%20Verbs.md)
  Curated API reference for high-frequency verbs, alias handling, and scripting surfaces.

- [Official VDJScript Coverage Audit](Official%20VDJScript%20Coverage%20Audit.md)
  Names-only audit comparing the live official VDJScript appendix against this repo's local verb reference.

- [VDJScript Local Test Tracker](VDJScript%20Local%20Test%20Tracker.md)
  Manual verification matrix for sparse, hardware-specific, and environment-dependent official verbs.

- [Published Skin Findings](Published%20Skin%20Findings.md)
  Source-backed notes from working public skins, including undocumented-looking commands, provenance, and local test plans.

- [Lyrics AI and Skins](Lyrics%20AI%20and%20Skins.md)
  Focused notes on VirtualDJ 2026 AI lyric detection, skin styling limits, lyric queries, filters, and forum-observed quirks.

- [Mapper XML](Mapper%20XML.md)
  Controller and keyboard mapper file format: `<button>`, `<slider>`, `<knob>`, shift layers, LED feedback, and the relationship to pad pages.

- [Application Internals](Application%20Internals.md)
  Low-level macOS-first notes on VirtualDJ paths, databases, caches, stem sidecars, linked tracks, and shell tooling.

- [Resources](Resources.md)
  Useful official, staff, community, and local sources for follow-up research.

Current status:

- `VirtualDJ Reference.md` is the policy and architecture layer.
- `VDJScript Verbs.md` is the first API-focused pass.
- `Official VDJScript Coverage Audit.md` tracks official verb names that still need local curated documentation.
- `VDJScript Local Test Tracker.md` is the default place to record manual VirtualDJ verification runs for `Needs local test` verbs.
- `Published Skin Findings.md` tracks empirical commands and skin idioms before they are fully folded into the curated reference.
- `Lyrics AI and Skins.md` is the focused lyric/autodetection reference.
- `Application Internals.md` is the low-level file/database/stem architecture reference.
- `Resources.md` is the source index.
- The other topical files still contain useful raw material, but they are not yet normalized to the same reliability standard.

Source labels used in the curated docs:

- `Official`
- `Official forum`
- `Community`
- `Published skin`
- `Published pad page`
- `Local test`
- `Inference`
