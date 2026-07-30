# Documentation Tests

This folder contains small reproducible assets used to verify claims in the reference documentation.

Test assets are important evidence for the documentation project. They are kept outside the normal example folders so a test page, skin, mapper, or other repro fixture is not mistaken for a polished reference implementation.

| Area | Contents |
| --- | --- |
| [Pads/](Pads/) | Pad-page XML harnesses used by the VDJScript local test tracker and related source notes. |
| [Skins/](Skins/) | Skin fixtures used with local pad/controller/script tests. |
| `verb-table.json` | **Authoritative.** VirtualDJ's own verb table, extracted from a serialised record array in `__DATA,__data` (`{const char *name; uint32 id; uint32 flags;}`): 1,028 records, 955 ids, 61 alias groups, 37 editor-hidden names, and every verb's **Button Editor category** (38 categories, from a `const char *[38]` name array plus a `uint8` category-per-id array indexed by `id+1`). Membership proves a name is a verb and absence disproves it; records sharing an `id` are the same verb, `flags==1` marking the alias spelling, `flags==256` the hidden bit. Written by `tools/extract_verb_table.py`; query with `just verb-table <name>`. |
| `action-contracts.json` | **Structural contract per verb**, read from the surviving ACTION_ class RTTI: name string → `std::type_info` → vtable. Gives every one of the 955 distinct verbs its implementation class (a checked 955/955 bijection), base-class family (`toggle`/`slider`/plain), context mixins (`IActionPlugin`, `IActionSampler`), vtable length, and the override matrix — execute, generic query, specialized text query — with slot meanings calibrated from HTTP-proven verbs, not hard-coded. Also carries method-body fingerprints: `arg_demand_slots` (E_INVALIDARG materialization — 114/116 agreement with sweep needs-args, plus 301 bare-answering query verbs flagged as taking optional args) and `method_strings` (per-slot string refs: formats, enum keywords like `loaded`'s `opposite`). Agreement with the Tier-1 sweep: 652/652 on query verbs, 181/186 on action-only (the 5 outliers are the menu-verb slot-7 lead). Tier-2 structural evidence: predicts capability, not concrete type or behavior. Written by `tools/extract_action_contracts.py`; query with `just verb-contract <name>`. |
| `verb-return-types.json` | **Observed return type per query verb** (Tier 1, HTTP): all 652 query verbs sampled in three read-only contexts and classified — 334 bool, 145 int, 68 float, 4 percent, 72 text, 29 untyped. The authority for a verb's concrete rendered type (proves *can return*, not *always returns*); 0 capability conflicts against `action-contracts.json`. Written by `tools/sweep_return_types.py` (needs live VirtualDJ); query with `just verb-return-type <name>`. |
| `binary-verbs.json` | The **structured** verb list extracted from the app itself, unioning three sources: 1,012 mangled `ACTION_<name>` implementation classes, 812 `languages.zip` catalog entries, and the parser's 967-entry alphabetically sorted name table (which is where **aliases** live). 1,076 names, covering 998 of the 1,007 the HTTP sweep proved real; flags 63 `alias_candidate` names (in the table with no implementation class of their own). Membership proves a name is real; absence is NOT a disproof. Written by `tools/extract_binary_verbs.py`; query with `just binary-verb <name>`. |
| `verb-existence-sweep.json` | HTTP existence probe for every verb-store name plus candidates-doc names: status (`exists`/`unresolved`), kind (`query`/`action-only`/`needs-args`/`context-gated`/`false-here`), the HRESULT, and a live sample value for query verbs. Written by `tools/sweep_verb_existence.py`; query with `just verb-probe <name>`. Proves existence and kind only, never behavior. |
| `vdjremote-opener.bin` | Raw opening handshake captured from a real VirtualDJ Remote device (app build 8515), the reference input for `tools/vdjremote_dial.py --decode` and the prefix reused by `tools/vdjremote_subscribe.py`. Backs [docs/Remote Protocol.md](../docs/Remote%20Protocol.md). |
| `vdjremote-actions.log` | Decoded device→desktop action frames captured while a real device's controls were touched, including the timed press sequence that maps play/cue/crossfader/volume to control ids. |
| [Stems/](Stems/) | Stem-file generators for `docs/Stem File Format.md` claims. `make-diagnostic-stems.zsh` builds probe files where the master is white noise and each stem a distinct sine tone (100/200/400/800/1600 Hz = kick/bass/vocal/instruments/hihat), so pad→stream routing and master↔stems switching are verifiable by ear; includes a stamped vs unstamped writing-application sidecar A/B. |

## Pad Fixtures

| File | Purpose |
| --- | --- |
| [Pads/Reference - Sparse Helper Tests.xml](Pads/Reference%20-%20Sparse%20Helper%20Tests.xml) | Sparse official helper checks such as `connect`, `system`, `open_stem_creator`, and `dualdeckmode_decks`. |
| [Pads/Reference - Sampler Loaded Test.xml](Pads/Reference%20-%20Sampler%20Loaded%20Test.xml) | Page-aware sampler loaded-state checks. |
| [Pads/Reference - Hidden Button Editor Tests.xml](Pads/Reference%20-%20Hidden%20Button%20Editor%20Tests.xml) | Low-risk flag1-hidden Button Editor taxonomy probes such as `stem_volume`, `sampler_inputgain`, pad-page helpers, and plugin query helpers. |
| [Pads/Reference - Mix FX Query Test.xml](Pads/Reference%20-%20Mix%20FX%20Query%20Test.xml) | Mix FX selected-state and active-state query checks. |
| [Pads/Reference - Deck Error Test.xml](Pads/Reference%20-%20Deck%20Error%20Test.xml) | Deck load-error state checks for `deck_has_error`. |
| [Pads/Reference - Dual Deck Mode Test.xml](Pads/Reference%20-%20Dual%20Deck%20Mode%20Test.xml) | Current and deck-scoped `dualdeckmode_decks` checks. |
| [Pads/Reference - FX Introspection Test.xml](Pads/Reference%20-%20FX%20Introspection%20Test.xml) | Deck FX slider/button label, count, default, and `effect_has_*` checks. |
| [Pads/Reference - Grammar Battery Test.xml](Pads/Reference%20-%20Grammar%20Battery%20Test.xml) | VDJScript grammar checks: ternary/`&` precedence, nested-ternary associativity, and backtick-computed arguments vs `param_*` chaining. |
| [Pads/Reference - FX Bank Test.xml](Pads/Reference%20-%20FX%20Bank%20Test.xml) | FX bank save/load restore checks for slot names, active state, slider values, and deck scope. |
| [Pads/Reference - Release FX Test.xml](Pads/Reference%20-%20Release%20FX%20Test.xml) | Release-FX slider and `is_releasefx` checks against normal slot slider behavior. |
| [Pads/Reference - BeatGrid Command Test.xml](Pads/Reference%20-%20BeatGrid%20Command%20Test.xml) | BeatGrid-specific `effect_command` probes based on the built-in plugin UI XML. |

## Skin Fixtures

| Folder | Purpose |
| --- | --- |
| [Skins/MixFxQueryTest/](Skins/MixFxQueryTest/) | Skin-side Mix FX query checks used with the Mix FX pad fixture. |
| [Skins/PlaceholderConditionTest/](Skins/PlaceholderConditionTest/) | Define-placeholder `visibility=""` / `condition=""` canary for skin XML. |
