# Pad Test Harnesses

These XML files are documentation test assets. They exist to reproduce and record specific VDJScript behavior, not to serve as polished pad-page examples.

VirtualDJ's installed pad folder is flat, so copy the specific harness XML into `~/Library/Application Support/VirtualDJ/Pads/` when running a test, then record the build, setup, result, and follow-up in [VDJScript Local Test Tracker](../../Reference/VDJScript%20Local%20Test%20Tracker.md).

| File | Page name | Purpose |
| --- | --- | --- |
| [Reference - Deck Error Test.xml](Reference%20-%20Deck%20Error%20Test.xml) | `REF: DECK ERROR TEST` | Exercise `deck_has_error` before/after valid loads, unloads, and a deliberately missing file. |
| [Reference - BeatGrid Command Test.xml](Reference%20-%20BeatGrid%20Command%20Test.xml) | `REF: BEATGRID CMD TEST` | Probe BeatGrid-specific `effect_command` strings observed in the built-in plugin UI XML. |
| [Reference - Dual Deck Mode Test.xml](Reference%20-%20Dual%20Deck%20Mode%20Test.xml) | `REF: DUAL DECKMODE TEST` | Compare current and deck-scoped `dualdeckmode_decks` behavior with dual-deck mode off/on. |
| [Reference - FX Bank Test.xml](Reference%20-%20FX%20Bank%20Test.xml) | `REF: FX BANK TEST` | Check `effect_bank_save` / `effect_bank_load` restore behavior for deck FX slots 1-6. |
| [Reference - FX Introspection Test.xml](Reference%20-%20FX%20Introspection%20Test.xml) | `REF: FX INTROSPECTION TEST` | Exercise deck FX slider/button counts, labels, defaults, text readbacks, and `effect_has_*` states. |
| [Reference - Hidden Button Editor Tests.xml](Reference%20-%20Hidden%20Button%20Editor%20Tests.xml) | `REF: HIDDEN TAXONOMY TEST` | Probe low-risk flag1-hidden Button Editor taxonomy rows such as `stem_volume`, `sampler_inputgain`, pad-page helpers, `is_colorfx`, and `effect_beats_sliderindex`. |
| [Reference - Mix FX Query Test.xml](Reference%20-%20Mix%20FX%20Query%20Test.xml) | `MIX FX QUERY TEST` | Compare direct/indirect `effect_mixfx_select` selected-state queries and `get_mixfx_active` against `effect_mixfx_activate`. Used with [MixFxQueryTest](../Skins/MixFxQueryTest/). |
| [Reference - Release FX Test.xml](Reference%20-%20Release%20FX%20Test.xml) | `REF: RELEASE FX TEST` | Compare `effect_releaseslider*` and `is_releasefx` behavior against normal slot FX controls. |
| [Reference - Sampler Loaded Test.xml](Reference%20-%20Sampler%20Loaded%20Test.xml) | `REF: SAMPLER LOADED TEST` | Verify whether `sampler_loaded <n> 'auto'` follows the visible sampler page. |
| [Reference - Sparse Helper Tests.xml](Reference%20-%20Sparse%20Helper%20Tests.xml) | `REF: SPARSE TEST` | Exercise sparse official helper verbs such as `connect`, `system`, `open_stem_creator`, `karaoke_venue_name`, and `dualdeckmode_decks`. |
