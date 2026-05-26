# Documentation Tests

This folder contains small reproducible assets used to verify claims in the reference documentation.

Test assets are important evidence for the documentation project. They are kept outside the normal example folders so a test page, skin, mapper, or other repro fixture is not mistaken for a polished reference implementation.

| Area | Contents |
| --- | --- |
| [Pads/](Pads/) | Pad-page XML harnesses used by the VDJScript local test tracker and related source notes. |
| [Skins/](Skins/) | Skin fixtures used with local pad/controller/script tests. |

## Pad Fixtures

| File | Purpose |
| --- | --- |
| [Pads/Reference - Sparse Helper Tests.xml](Pads/Reference%20-%20Sparse%20Helper%20Tests.xml) | Sparse official helper checks such as `connect`, `system`, `open_stem_creator`, and `dualdeckmode_decks`. |
| [Pads/Reference - Sampler Loaded Test.xml](Pads/Reference%20-%20Sampler%20Loaded%20Test.xml) | Page-aware sampler loaded-state checks. |
| [Pads/Reference - Mix FX Query Test.xml](Pads/Reference%20-%20Mix%20FX%20Query%20Test.xml) | Mix FX selected-state and active-state query checks. |
| [Pads/Reference - Deck Error Test.xml](Pads/Reference%20-%20Deck%20Error%20Test.xml) | Deck load-error state checks for `deck_has_error`. |
| [Pads/Reference - Dual Deck Mode Test.xml](Pads/Reference%20-%20Dual%20Deck%20Mode%20Test.xml) | Current and deck-scoped `dualdeckmode_decks` checks. |
| [Pads/Reference - FX Introspection Test.xml](Pads/Reference%20-%20FX%20Introspection%20Test.xml) | Deck FX slider/button label, count, default, and `effect_has_*` checks. |
