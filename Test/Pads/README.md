# Pad Test Harnesses

These XML files are documentation test assets. They exist to reproduce and record specific VDJScript behavior, not to serve as polished pad-page examples.

VirtualDJ's installed pad folder is flat, so copy the specific harness XML into `~/Library/Application Support/VirtualDJ/Pads/` when running a test, then record the build, setup, result, and follow-up in [VDJScript Local Test Tracker](../../Reference/VDJScript%20Local%20Test%20Tracker.md).

| File | Page name | Purpose |
| --- | --- | --- |
| [Reference - Deck Error Test.xml](Reference%20-%20Deck%20Error%20Test.xml) | `REF: DECK ERROR TEST` | Exercise `deck_has_error` before/after valid loads, unloads, and a deliberately missing file. |
| [Reference - Dual Deck Mode Test.xml](Reference%20-%20Dual%20Deck%20Mode%20Test.xml) | `REF: DUAL DECKMODE TEST` | Compare current and deck-scoped `dualdeckmode_decks` behavior with dual-deck mode off/on. |
| [Reference - Hidden Button Editor Tests.xml](Reference%20-%20Hidden%20Button%20Editor%20Tests.xml) | `REF: HIDDEN TAXONOMY TEST` | Probe low-risk flag1-hidden Button Editor taxonomy rows such as `stem_volume`, `sampler_inputgain`, pad-page helpers, `is_colorfx`, and `effect_beats_sliderindex`. |
| [Reference - Mix FX Query Test.xml](Reference%20-%20Mix%20FX%20Query%20Test.xml) | `MIX FX QUERY TEST` | Compare direct/indirect `effect_mixfx_select` selected-state queries and `get_mixfx_active` against `effect_mixfx_activate`. Used with [MixFxQueryTest](../Skins/MixFxQueryTest/). |
| [Reference - Sampler Loaded Test.xml](Reference%20-%20Sampler%20Loaded%20Test.xml) | `REF: SAMPLER LOADED TEST` | Verify whether `sampler_loaded <n> 'auto'` follows the visible sampler page. |
| [Reference - Sparse Helper Tests.xml](Reference%20-%20Sparse%20Helper%20Tests.xml) | `REF: SPARSE TEST` | Exercise sparse official helper verbs such as `connect`, `system`, `open_stem_creator`, `karaoke_venue_name`, and `dualdeckmode_decks`. |
