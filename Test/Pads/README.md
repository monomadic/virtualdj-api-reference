# Pad Test Harnesses

These XML files are documentation test assets. They exist to reproduce and record specific VDJScript behavior, not to serve as polished pad-page examples.

VirtualDJ's installed pad folder is flat, so copy the specific harness XML into `~/Library/Application Support/VirtualDJ/Pads/` when running a test, then record the build, setup, result, and follow-up in [VDJScript Local Test Tracker](../../Reference/VDJScript%20Local%20Test%20Tracker.md).

| File | Page name | Purpose |
| --- | --- | --- |
| [Reference - Mix FX Query Test.xml](Reference%20-%20Mix%20FX%20Query%20Test.xml) | `MIX FX QUERY TEST` | Compare direct and indirect `effect_mixfx_select` selected-state queries. Used with [MixFxQueryTest](../Skins/MixFxQueryTest/). |
| [Reference - Sampler Loaded Test.xml](Reference%20-%20Sampler%20Loaded%20Test.xml) | `REF: SAMPLER LOADED TEST` | Verify whether `sampler_loaded <n> 'auto'` follows the visible sampler page. |
| [Reference - Sparse Helper Tests.xml](Reference%20-%20Sparse%20Helper%20Tests.xml) | `REF: SPARSE TEST` | Exercise sparse official helper verbs such as `connect`, `system`, `open_stem_creator`, `karaoke_venue_name`, and `dualdeckmode_decks`. |
