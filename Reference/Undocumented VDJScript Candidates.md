# Undocumented VDJScript Candidates

Local notes for VDJScript-looking names that are not in the official VDJScript
appendix, but do appear in one or more bundled VirtualDJ evidence streams.

These are candidates, not recommendations. Keep them out of normal user-facing
verb guidance until a manual run records VirtualDJ build, setup, exact action or
query text, observed result, and follow-up notes in
[VDJScript Local Test Tracker](VDJScript%20Local%20Test%20Tracker.md).

## Evidence Baseline

Source app: `/Applications/VirtualDJ.app`

Observed locally on 2026-06-08:

- VirtualDJ app version: `8.5.9307`
- VirtualDJ bundle build: `18.0.9336`
- Main executable SHA-256: `233f36a8d454d0fe90e7bb1c57b9550a4ea8aa3ee0a9f219624c24aa8aaa59f1`

Reproduce the current inventory:

```sh
python3 tools/extract_vdjscript_metadata.py --flag1-hidden --format summary
python3 tools/extract_vdjscript_metadata.py --flag1-hidden --format csv
python3 tools/extract_vdjscript_metadata.py --flag1-hidden --language-described-only --format csv
```

Current extraction summary:

| Measure | Count |
| --- | ---: |
| Flag1-hidden compiled taxonomy rows | 37 |
| Official appendix names in this set | 0 |
| Bundled language-catalog descriptions in this set | 14 |
| Exact `ACTION_*` method-symbol matches in this set | 30 |
| `execute+query` capability hints | 14 |
| `execute-only` capability hints | 5 |
| `query-only` capability hints | 11 |
| No exact action-class match | 7 |

Important distinction: this flag1-hidden compiled-taxonomy inventory is not the
same list as the 14 Button Editor catalog-only names plus 21 runtime-string-only
names in [Button Editor Catalog Audit](Button%20Editor%20Catalog%20Audit.md).
Those streams overlap, but the compiled taxonomy is a separate source.

## Online Cross-Check

Checked on 2026-06-08:

- The live official appendix still parsed to the same 991 public verb/alias
  names after excluding category header cells. None of the 37 flag1-hidden
  candidates below was present in the public appendix.
- The public `stem` documentation and Stems 2.0 manual support the stem-control
  context for `stem_volume`: stems can be controlled from pads and EQ/stem
  controls, and the public `stem` verb documents individual and aggregate stem
  names. They do not make `stem_volume` a public verb.
- Public VirtualDJ forum/manual searches found user-facing context for
  Serato-Flip-style workflows, including Track Cleaner and the community
  Routine pad page/plugin, but not public VDJScript documentation for the
  hidden `flip_*` candidates. Keep those candidates in the manual-test track.
- `remote_action` has direct official-forum evidence from VirtualDJ staff/CTO
  in Remote skin contexts. Treat it as Remote-specific until locally verified
  in a current Remote skin.
- `pad_page_favorite` has official changelog/forum context and published-skin
  usage, even though it is absent from the official verbs appendix. It should be
  tested against the current pad-page favorite UI before promotion.
- `get_pad_page_name` and `setting_if_unchanged` have public forum examples or
  discussion, but not enough current local behavior evidence to become normal
  reference entries.
- `masterbpm`, `master_beat_num`, and `all_decks` only had weak public context
  in the search pass: mentions as hidden/internal-ish features or user attempts,
  not reliable behavior descriptions.

Sources:

- [Official VDJScript verbs appendix](https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html)
- [Official Stems 2.0 manual](https://www.virtualdj.com/manuals/virtualdj/interface/stems2.html)
- [VirtualDJ forum: Serato flip feature in VDJ 2020?](https://virtualdj.com/forums/236900/General_Discussion/Serato_flip_feature_in_VDJ_2020_.html)
- [VirtualDJ forum: Remote App custom buttons](https://virtualdj.com/forums/257572/VirtualDJ_Technical_Support/Remote_App__Saving_location_of_the_custom_buttons.html)
- [VirtualDJ forum: Remote dynamic text and variables](https://virtualdj.com/forums/264747/VirtualDJ_Skins/Dynamic_text_in_%22Textzone%22.html)
- [VirtualDJ forum: `get_pad_page_name` discrepancy](https://virtualdj.com/forums/227511/VirtualDJ_Technical_Support/get_pad_page_name_discrepency.html)
- [VirtualDJ forum: pad-page script question](https://virtualdj.com/forums/238929/General_Discussion/Pad_Page_Script_Question.html)
- [VirtualDJ forum: `setting_if_unchanged` coverflow example](https://virtualdj.com/forums/234495/VirtualDJ_Technical_Support/Album_Art_not_showing_in_search.html)
- [VirtualDJ changelog: Build 4918 pad-page favorites](https://www.virtualdj.com/products/virtualdj/changelog.html)

## Promotion Rules

- `Built-in app resource` evidence can describe a bundled Button Editor action
  hint, but it does not prove runtime behavior.
- `Binary compiled table` evidence can place a candidate in a category and show
  it is hidden from the visible Button Editor list, but it does not prove public
  support.
- `Binary symbol table` evidence can hint whether an exact implementation class
  has execute/query/text methods, but aliases and dispatchers can break one-to-
  one assumptions.
- `Binary string-table` evidence is discovery-only.
- `Local test` is required before a candidate becomes normal VDJScript guidance.

## First Probe Queue

Use [Reference - Hidden Button Editor Tests.xml](../Test/Pads/Reference%20-%20Hidden%20Button%20Editor%20Tests.xml)
for the current low-risk pad-page probes.

| Candidate group | Why it is first | Minimal result to record |
| --- | --- | --- |
| `stem_volume` | Bundled prose distinguishes it from ordinary public `stem`, and no hardware should be required for stems-ready decks. A first partial run exists, but stems readiness was not recorded. | Readback, visible stem-level change, and audible result for direct names plus `Melody`, `Rhythm`, and `MeloVocal`; test `MeloRhythm` separately before treating it as supported for this hidden helper. |
| `sampler_inputgain` | Bundled prose and exact execute/query symbols exist. | Query value before/after setting 50%, and whether any hardware/input sampler path changes audibly. |
| `get_pad_page_name`, `pad_page_insplit`, `pad_page_favorite`, `pad_page_split` | Pad-page state helpers are low-risk and may improve page tooling. | Normal page, split page, and favorite page readbacks with the exact page names shown in VirtualDJ. |
| `is_colorfx`, `effect_beats_sliderindex` | Query-only plugin helpers should be safe to observe. | Readbacks while switching normal FX, ColorFX, and beat-length controls. |
| `masterbpm`, `master_beat_num` | Exact execute/query symbols suggest useful master-deck diagnostics. | Readbacks across master-deck changes, tempo changes, and beatgrid movement; compare with `get_bpm` and `get_beat_num`. |

## Deferred Probe Queue

| Candidate group | Reason to defer | Safer next step |
| --- | --- | --- |
| `flip_arm`, `flip_get_status`, `flip_load`, `flip_loop`, `flip_play`, `flip_record` | Requires a known Flip feature state and saved or recordable Flip content. | Build a focused Flip harness after confirming Flip availability and how recording is gated. |
| `setting_if_unchanged` | Settings mutation tests can be noisy or profile-specific. | Start with a harmless custom-button query against a known setting before any mutation. |
| `all_decks`, `combine_query` | These may be grammar/combinator helpers, not ordinary actions. | Test bare readbacks and tiny harmless boolean expressions in custom buttons before adding pad fixtures. |
| `browser_colorfilter_edit`, `load_security_shown` | Browser UI/security state depends on context. | Observe query-only `load_security_shown` first; use a throwaway profile before trying color-filter editor actions. |
| `remote_action` | Official forum evidence ties it to VirtualDJ Remote. | Test only in a current Remote skin, with desktop-vs-remote variable/action state visible. |

## Hardware And Context Queue

| Candidate group | Needed context |
| --- | --- |
| `assign_related_controller` | Controller relationship/layer setup. |
| `controllerscreen_action` | Display-capable controller mapping. |
| `motorwheel2`, `motorwheel3`, `ns7_get_drift` | Motorized controller or Numark NS7-style context. |
| `pad_pressure_switch` | Pressure-capable pad hardware. |
| `rane_motor_enable`, `rane_timecode`, `rane_timecode_enable`, `rane_screen_input`, `rane_screen_output` | Matching Rane or Rane-like controller/timecode/display context. |
| `send_nothing` | Controller output/feedback context. |

## Watch-Only Rows

| Candidate | Reason |
| --- | --- |
| `crash` | Bundled description and execute symbol make it look intentionally destructive or diagnostic. Do not run in a live session. |
| `hot_cue_stutter` | Hidden taxonomy row only; no language, official, shipped XML, or exact action-class evidence yet. |
| `timecode_no_jump` | Hidden taxonomy row only; no behavior source yet. |

## Candidate Detail Notes

### `stem_volume`

Evidence: `Built-in app resource`, `Binary compiled table`; no exact
`ACTION_*` class detected.

The bundled English action description says `stem_volume` changes stem amount
for individual names `HiHat`, `Vocal`, `Instru`, `Bass`, and `Kick`, plus
aggregate names `Melody`, `Rhythm`, and `MeloVocal`. It also distinguishes the
candidate from the public `stem` verb: `stem_volume` is described as a
0-100%-style slider helper, while `stem` defaults at the middle and isolates
above the middle.

Do not copy the public `stem` verb's full stem-name set onto this candidate
without testing. The live official appendix documents `MeloRhythm` for `stem`,
but this build's hidden `stem_volume` language string does not list it.

Current local status: `Partial`. On 2026-06-08 in VirtualDJ `v2026-m b9336`,
Pads 1-3 of the hidden-candidate harness read back `1`, but pressing
`stem_volume 'Vocal' 50%`, `stem_volume 'Vocal' 100%`, and
`stem_volume 'Instru' 50%` produced no recorded audible or label change.
Stems readiness and visible stem controls were not recorded, so this is not a
fail result. Next run should load a confirmed stems-ready deck, show or compare
public stem controls, and record direct plus aggregate names.

### `sampler_inputgain`

Evidence: `Built-in app resource`, `Binary compiled table`,
`Binary symbol table`.

The language description and exact `onExecute`/`onQuery` method hints both
point to hardware sampler input gain. Treat any no-hardware readback as
diagnostic only; a useful pass should separate query value changes from audible
or input-path behavior.

### Pad-Page State Candidates

Evidence: `Binary compiled table`, `Binary symbol table`; `pad_page_insplit`
also has `Built-in app resource` prose.

`get_pad_page_name`, `pad_page_insplit`, `pad_page_favorite`, and
`pad_page_split` are promising low-risk probes for pad-page tooling. Because
local pad XML selector labels are filename stems, record both the selector
label and XML `<page name="">` when testing page-name helpers.

Public context is uneven:

- `get_pad_page_name` appears in public forum discussion as a pad-page label
  helper and as something that did not save cleanly into a variable in one 2020
  community test. A 2018 forum note describes it as added for an index-padpage
  use case.
- `pad_page_favorite` is stronger than a plain runtime-string candidate:
  VirtualDJ's public changelog says Build 4918 added favorite pad pages and the
  `pad_page_favorite` action; a staff forum reply uses it for cycling favorite
  pages; local installed published skins use it as `action=`, `textaction=`, and
  `visibility=` material. It is still absent from the copied built-in/official
  XML roots scanned by `tools/extract_vdjscript_catalogs.py`, so keep the local
  test row active.
- `pad_page_split` and `pad_page_insplit` still need current UI-state
  observation in normal, split, and favorite page contexts.

### Plugin Query Candidates

Evidence: `Binary compiled table`, `Binary symbol table`.

`is_colorfx` and `effect_beats_sliderindex` have exact query symbols and are
safe readback candidates. They should be compared against already documented
public helpers such as `filter_label 'name'`, `effect_beats`,
`effect_has_beats`, and selected normal deck FX state before promotion.

### `flip_*`

Evidence varies by candidate: most have bundled language descriptions, and
`flip_get_status`, `flip_load`, `flip_play`, and `flip_record` have exact
method-symbol hints.

Public web context currently points users toward Track Cleaner or community
Routine-style workflows for Serato-Flip-like behavior, not toward public
`flip_*` VDJScript verbs. Build a focused Flip harness only after confirming
the feature state, saved Flip content, and expected licensing/build gates.

### `remote_action`

Evidence: `Official forum`, `Binary compiled table`, `Binary symbol table`.

VirtualDJ staff/CTO posts describe Remote custom buttons and variables as
independent from the main desktop context, and use `remote_action` when a
Remote skin needs to trigger or query desktop-side actions such as custom
buttons or variables. Examples in those threads include desktop custom-button
access, desktop variable readback, and toggling a desktop variable from Remote.

Do not treat `remote_action` as a generic skin helper yet. The evidence is
Remote-specific, and one 2025 thread had syntax/version caveats before the user
reported success. A useful local pass needs a current Remote skin, a desktop
custom button or variable, a Remote-local variable with the same name, and
before/after readbacks from both sides.

### `setting_if_unchanged`

Evidence: `Community`, `Binary compiled table`, `Binary symbol table`.

Public forum examples use `setting_if_unchanged` in skin `oninit` actions for
layout defaults such as `coverflow`. A Greek forum snippet explains it as a
setting change that only applies if the user has not changed that setting.

This candidate is a good reminder that exact symbol capability is only a hint:
the exact `ACTION_setting_if_unchanged` symbol currently looks query-only, while
the public examples use the name in action slots. Test with a harmless setting
and a throwaway skin or custom button before documenting it as a defaulting
helper.

### Master And Flow Candidates

Evidence: `Binary compiled table`, `Binary symbol table`, weak `Community`
mentions.

`masterbpm` and `master_beat_num` have exact execute/query symbols and may be
useful for master-deck diagnostics, but public web evidence found so far only
mentions them as hidden/internal-ish features. Compare them with public
`masterdeck`, `get_bpm`, `get_beat_num`, and visible beatgrid/BPM state before
using them in docs.

`all_decks` and `combine_query` have the broadest exact method-surface hints
(`onExecute`, `onQuery`, `onQueryBool`, and `onQueryText`). The syntax evidence
tracker already has `all_decks play` as a grammar test shape, and a public LED
thread shows a user trying `all_decks ? ...` unsuccessfully. Start with bare
readbacks and parser/highlighter behavior in the Button Editor before adding
runtime pad fixtures.

## Full Flag1-Hidden Inventory

Evidence abbreviations:

- `lang`: bundled language action description.
- `ACTION`: exact `ACTION_*` implementation method symbols.
- `taxonomy`: hidden compiled Button Editor taxonomy row.
- `forum`: public forum evidence; see source label in the detail notes before
  treating it as staff-backed.
- `changelog`: official VirtualDJ changelog mention.
- `published-skin`: installed public skin XML evidence outside the copied
  built-in/official XML roots.
- `syntax`: parser/highlighter test target in [VDJScript Syntax Evidence](VDJScript%20Syntax%20Evidence.md).

| Candidate | Category | Evidence | Method hint | Next action |
| --- | --- | --- | --- | --- |
| `all_decks` | flow | taxonomy, ACTION, syntax, forum | execute/query/bool/text | Custom-button grammar probe only; do not infer behavior from failed community LED attempts. |
| `assign_related_controller` | controllers | taxonomy, lang, ACTION | execute | Controller relationship test. |
| `browser_colorfilter_edit` | browser | taxonomy, ACTION | execute | Throwaway browser color-filter context. |
| `combine_query` | flow | taxonomy, ACTION | execute/query/bool/text | Custom-button grammar probe only. |
| `controllerscreen_action` | controllers | taxonomy, ACTION | execute | Display controller mapping test. |
| `crash` | system | taxonomy, lang, ACTION | execute | Do not run. |
| `effect_beats_sliderindex` | plugins | taxonomy, ACTION | query | Observe selected FX beat controls. |
| `flip_arm` | macro | taxonomy, lang | none | Flip-specific harness. |
| `flip_get_status` | macro | taxonomy, ACTION | query | Flip status readback. |
| `flip_load` | macro | taxonomy, lang, ACTION | execute/query | Saved Flip load test. |
| `flip_loop` | macro | taxonomy, lang | none | Flip loop test after known Flip state. |
| `flip_play` | macro | taxonomy, lang, ACTION | text query | Verify action behavior before assuming execute semantics. |
| `flip_record` | macro | taxonomy, lang, ACTION | execute/query/text | Controlled Flip record test. |
| `get_pad_page_name` | pads | taxonomy, ACTION, forum | query | Normal/split/favorite page readbacks; compare with selector labels and variable-capture attempts. |
| `hot_cue_stutter` | cues | taxonomy | none | Watch for another source first. |
| `is_colorfx` | plugins | taxonomy, ACTION | query | Compare ColorFX vs normal FX selection. |
| `load_security_shown` | browser | taxonomy, ACTION | query | Observe when VirtualDJ shows load security. |
| `master_beat_num` | get | taxonomy, ACTION, forum | execute/query | Compare with master deck, `get_beat_num`, and visible beatgrid position. |
| `masterbpm` | get | taxonomy, ACTION, forum | execute/query | Compare with master deck, `get_bpm`, and visible BPM/tempo changes. |
| `motorwheel2` | controllers | taxonomy, ACTION | execute/query | Motorized controller context. |
| `motorwheel3` | controllers | taxonomy, ACTION | execute/query | Motorized controller context. |
| `ns7_get_drift` | controllers | taxonomy, ACTION | query/text | Numark NS7-style context. |
| `pad_page_favorite` | pads | taxonomy, ACTION, changelog, forum, published-skin | execute/query/text | Favorite page action/query/text test across the current four favorite slots. |
| `pad_page_insplit` | pads | taxonomy, lang, ACTION | query | Split page state test. |
| `pad_page_split` | pads | taxonomy, ACTION | execute/query | Split page action/query test. |
| `pad_pressure_switch` | pads | taxonomy, lang | none | Pressure-capable pad hardware. |
| `rane_motor_enable` | controllers | taxonomy, lang, ACTION | execute | Rane motorized hardware context. |
| `rane_screen_input` | rane | taxonomy, ACTION | execute/query | Rane display/input context. |
| `rane_screen_output` | rane | taxonomy, ACTION | query | Rane display/output context. |
| `rane_timecode` | controllers | taxonomy, lang, ACTION | execute/query | Rane timecode input context. |
| `rane_timecode_enable` | controllers | taxonomy, lang | none | Rane timecode mapping context. |
| `remote_action` | skin | taxonomy, ACTION, forum | execute/query/bool/text | Current Remote skin test with desktop-vs-remote variable/action state visible. |
| `sampler_inputgain` | sampler | taxonomy, lang, ACTION | execute/query | Hardware sampler input gain test. |
| `send_nothing` | controllers | taxonomy, ACTION | query | Controller feedback context. |
| `setting_if_unchanged` | config | taxonomy, ACTION, forum | query | Harmless setting defaulting probe; verify action-slot behavior despite query-only symbol hint. |
| `stem_volume` | equalizer | taxonomy, lang | none | Repeat with confirmed stems-ready deck; test direct names plus `Melody`, `Rhythm`, and `MeloVocal`; keep `MeloRhythm` separate until observed. |
| `timecode_no_jump` | timecode | taxonomy | none | Watch for another source first. |
