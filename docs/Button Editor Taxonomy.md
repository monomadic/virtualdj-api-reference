# Button Editor Taxonomy

Local extraction of the compiled VDJScript category mapping used by VirtualDJ's Button Editor.

Source app: `/Applications/VirtualDJ.app`

Observed on 2026-05-30:

- VirtualDJ app version: `8.5.9307`
- VirtualDJ bundle build: `18.0.9336`
- Main executable SHA-256: `233f36a8d454d0fe90e7bb1c57b9550a4ea8aa3ee0a9f219624c24aa8aaa59f1`

## Purpose

This file records the action-to-category taxonomy used by the Button Editor UI. It is separate from the language-description catalog in `Resources/languages.zip`: the language files provide prose descriptions, while the category mapping is compiled into the executable.

Treat this as `Binary compiled table` evidence. It is good evidence for how VirtualDJ groups actions in the Button Editor, but it is not by itself behavior evidence for parameters, return values, or public support.

## Extraction

The mapping is read from three arm64 Mach-O data areas referenced by `DLGActionWizard`:

| Table | Address | Meaning |
| --- | ---: | --- |
| Category names | `0x10457a880` | Null-terminated pointer list; `defines` is present but skipped when the UI category list is populated. |
| Action items | `0x104576830` | 16-byte entries: action-name pointer, action id, and four flag bytes; ends at action id `0x3bb`. |
| Category ids | `0x103d43974` | Signed-byte category id lookup indexed by action id. |

Reproduce with:

```sh
python3 tools/extract_vdjscript_taxonomy.py
```

Useful focused outputs:

```sh
python3 tools/extract_vdjscript_taxonomy.py --category plugins --format names
python3 tools/extract_vdjscript_taxonomy.py --category rane --include-hidden --format csv
python3 tools/extract_vdjscript_taxonomy.py --format csv > /tmp/vdjscript-button-editor-taxonomy.csv
```

The joined metadata matrix combines the compiled taxonomy with official audit membership, bundled language-catalog membership, and exact `ACTION_*` method-symbol matches:

```sh
python3 tools/extract_vdjscript_metadata.py
python3 tools/extract_vdjscript_metadata.py --include-hidden --include-external --format csv > /tmp/vdjscript-metadata.csv
python3 tools/extract_vdjscript_metadata.py --flag1-hidden --format names
python3 tools/extract_vdjscript_metadata.py --flag1-hidden --language-described-only --format csv
```

The metadata CSV includes an `english_description` column read from `Resources/languages.zip` / `English.xml`. Keep this distinct from the multilingual language-catalog union: the union can contain names that are not present in the English action-description file.

## Counts

| Source | Count |
| --- | ---: |
| Compiled category ids | 38 |
| Displayed Button Editor categories | 37 |
| Compiled action items | 1028 |
| Visible Button Editor action items | 918 |
| Flag0-hidden items | 73 |
| Flag1-hidden items | 37 |
| Language-catalog names present in compiled table | 813 |
| Visible compiled names not in language catalog | 121 |
| Language-catalog compiled names not visible | 16 |

The Button Editor list is therefore larger than the language-description catalog. The description catalog has 813 action tags across bundled languages, while the compiled UI table has 918 visible actions and 1028 total entries.

## Metadata Matrix

The metadata join currently has no exact `ACTION_*` class outside the compiled taxonomy. In other words, every exact action class detected from the demangled symbol table maps back to a compiled Button Editor taxonomy row.

| Matrix | Rows | Official audit names | Language-catalog names | Exact `ACTION_*` class match |
| --- | ---: | ---: | ---: | ---: |
| Visible Button Editor rows | 918 | 918 | 797 | 770 |
| Full compiled taxonomy rows | 1028 | 991 | 813 | 800 |

The 148 visible rows without an exact `ACTION_*` class match are not evidence of unsupported verbs. They often look like aliases, factory-created actions, or dispatcher-backed names. For example, `effect_select` and `video_fx` are visible, official, and language-described, but do not have exact `ACTION_effect_select` or `ACTION_video_fx` class symbols.

Capability buckets are derived only from exact `ACTION_*` method symbols:

| Bucket | Meaning |
| --- | --- |
| `execute+query` | Exact class has `onExecute` plus at least one query method. |
| `execute-only` | Exact class has `onExecute` and no detected query method. |
| `query-only` | Exact class has at least one query method and no detected `onExecute`. |
| `tooltip-only` | Exact class has `onTooltip` only among the tracked methods. |
| `no-action-class` | No exact class/method match; usually alias, dispatcher, or generated-path territory. |

Visible Button Editor capability buckets:

| Bucket | Visible rows |
| --- | ---: |
| `execute+query` | 282 |
| `execute-only` | 160 |
| `query-only` | 318 |
| `tooltip-only` | 10 |
| `no-action-class` | 148 |

Full compiled taxonomy capability buckets:

| Bucket | Rows |
| --- | ---: |
| `execute+query` | 296 |
| `execute-only` | 165 |
| `query-only` | 329 |
| `tooltip-only` | 10 |
| `no-action-class` | 228 |

Hidden-row split:

| Hidden group | Count | Notes |
| --- | ---: | --- |
| Flag0-hidden official names | 73 | All flag0-hidden rows are official audit names; 2 also have language descriptions. |
| Flag1-hidden non-official names | 37 | All flag1-hidden rows are outside the official audit; 14 still have language descriptions. |
| Hidden rows outside both official and language catalogs | 23 | Mostly internal, hardware-specific, or discovery-only-looking names. |

Representative joined rows:

| Name | Category | Visible | Official | Language | Capability bucket | Methods |
| --- | --- | --- | --- | --- | --- | --- |
| `effect_active` | `plugins` | yes | yes | yes | `execute+query` | `onExecute`, `onQuery` |
| `effect_select` | `plugins` | yes | yes | yes | `no-action-class` | none detected |
| `effect_slider` | `plugins` | yes | yes | yes | `execute+query` | `onExecute`, `onQuery`, `onTooltip` |
| `get_mixfx_active` | `plugins` | yes | yes | no | `query-only` | `onQuery` |
| `auto_crossfader` | `audio_volumes` | no | yes | no | `no-action-class` | none detected |
| `all_decks` | `flow` | no | no | no | `execute+query` | `onExecute`, `onQuery`, `onQueryBool`, `onQueryText` |

## Displayed Categories

`defines` is category id `0`, but `DLGActionWizard::link` skips it when populating the category list. The remaining 37 category ids are displayed.

**The Examples column is hand-written and was partly wrong — the count columns are not.**
Noted 2026-07-29. The two kinds of column have different pedigree and must not be trusted
equally:

- **Counts are extraction output.** All 37 rows reproduce exactly under
  [tools/extract_verb_table.py](../tools/extract_verb_table.py), which reads the same tables by
  anchor rather than by pinned address on a later build (bundle `18.0.9482`).
- **Examples were typed by hand.** `category_summary()` emits `visible_examples[:8]` over an
  alphabetically sorted table, yet every row below has exactly 4 entries and several are not in
  alphabetical order at all (rows 9, 10, 18). So these are an author's illustrative picks, and
  four of them named the wrong category. Struck through and corrected below; the verb table is
  authoritative per rule 1c2 of [Evidence Standards.md](Evidence%20Standards.md).

| ID | Category | Total | Visible | Flag0 Hidden | Flag1 Hidden | Examples |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `flow` | 6 | 4 | 0 | 2 | `down`, `isrepeat`, `nothing`, `up` |
| 2 | `param` | 32 | 26 | 6 | 0 | `blink`, `color`, `param_bigger`, `param_equal` |
| 3 | `repeat` | 7 | 7 | 0 | 0 | `doubleclick`, `holding`, `repeat`, `wait` |
| 4 | `skin` | 31 | 26 | 4 | 1 | `custom_button`, `get_skin_color`, `skin_panel` |
| 5 | `system` | 21 | 18 | 2 | 1 | `debug`, `get_cpu`, `get_date`, `system` |
| 6 | `variables` | 13 | 13 | 0 | 0 | `get_var`, `set_var`, `toggle`, `var_equal` |
| 7 | `window` | 5 | 5 | 0 | 0 | `close`, `maximize`, `show_window` |
| 8 | `audio` | 24 | 24 | 0 | 0 | `beatjump`, `clone_deck`, `dualdeckmode`, ~~`mute`~~ (`mute` is `audio_volumes`; `stems_split` belongs here) |
| 9 | `audio_controls` | 15 | 13 | 2 | 0 | `play`, `pause`, `stop`, ~~`silent_cue`~~ (`silent_cue` is `cues`) |
| 10 | `audio_inputs` | 11 | 10 | 1 | 0 | `mic`, `linein`, `aux_volume`, `mic_eq_high` |
| 11 | `audio_scratch` | 26 | 18 | 8 | 0 | `jogwheel`, `motorwheel`, `scratch`, `touchwheel` |
| 12 | `audio_volumes` | 55 | 47 | 8 | 0 | `crossfader`, `gain`, `level`, `master_volume` |
| 13 | `automix` | 31 | 30 | 1 | 0 | `automix`, `mix_now`, `playlist_add` |
| 14 | `browser` | 89 | 82 | 5 | 2 | `add_list`, `browser_scroll`, `search`, `sideview_options` |
| 15 | `config` | 29 | 25 | 3 | 1 | `setting`, `setting_reset`, `save_config`, `settings` |
| 16 | `controllers` | 75 | 66 | 0 | 9 | `action_deck`, `djc_button`, `os2l_cmd` |
| 17 | `cues` | 31 | 28 | 2 | 1 | `cue`, `cue_color`, `hot_cue`, `set_cue` |
| 18 | `deck_select` | 11 | 11 | 0 | 0 | `leftdeck`, `rightdeck`, `masterdeck`, `pfl` |
| 19 | `equalizer` | 37 | 29 | 7 | 1 | `eq_high`, `eq_kill_low`, `stem`, ~~`stems_split`~~ (`stems_split` is `audio`) |
| 20 | `get` | 118 | 115 | 1 | 2 | `get_album`, `get_bpm`, `get_title`, ~~`loaded`~~ (`loaded` is `browser`) |
| 21 | `karaoke` | 9 | 9 | 0 | 0 | `karaoke`, `karaoke_options`, `karaoke_show` |
| 22 | `key` | 18 | 17 | 1 | 0 | `get_key`, `key_lock`, `key_match_button`, `set_key` |
| 23 | `loop` | 40 | 40 | 0 | 0 | `loop`, `loop_roll`, `reloop`, `saved_loop` |
| 24 | `macro` | 8 | 2 | 0 | 6 | `macro_play`, `macro_record` |
| 25 | `pads` | 31 | 24 | 2 | 5 | `pad`, `pad_color`, `pad_page_select`, `padfx` |
| 26 | `pitch` | 19 | 15 | 4 | 0 | `pitch`, `pitch_bend`, `pitch_reset` |
| 27 | `plugins` | 95 | 87 | 6 | 2 | `effect_active`, `effect_select`, `effect_slider`, `video_fx` |
| 28 | `poi` | 11 | 11 | 0 | 0 | `adjust_cbg`, `edit_bpm`, `edit_poi`, `set_bpm` |
| 29 | `prelisten` | 6 | 5 | 1 | 0 | `prelisten`, `prelisten_output`, `prelisten_stop` |
| 30 | `rane` | 2 | 0 | 0 | 2 | none visible |
| 31 | `record` | 6 | 6 | 0 | 0 | `broadcast`, `record`, `record_config` |
| 32 | `sampler` | 56 | 50 | 5 | 1 | `sampler_pad`, `sampler_play`, `sampler_volume` |
| 33 | `sandbox` | 2 | 2 | 0 | 0 | `can_sandbox`, `sandbox` |
| 34 | `sync` | 22 | 19 | 3 | 0 | `beatlock`, `is_sync`, `sync`, `sync_hint` |
| 35 | `text` | 5 | 5 | 0 | 0 | `countdown`, `get_text`, `stopwatch` |
| 36 | `timecode` | 13 | 12 | 0 | 1 | `timecode_active`, `timecode_config`, `timecode_pitch` |
| 37 | `video` | 18 | 17 | 1 | 0 | `is_video`, `leftvideo`, `video_crossfader`, `video_transition` |

## Hidden Flags

The UI hides entries when either of the first two flag bytes has bit 0 set.

- Flag0-hidden entries mostly look like non-displayed aliases, old spellings, or alternate spellings: examples include `auto_crossfader`, `browser`, `config`, `hotcue`, `microphone`, `pitchlock`, `skin_pannel`, and `volume_slider`.
- Flag1-hidden entries mostly look internal, hardware-specific, or discovery-only: examples include `all_decks`, `combine_query`, `controllerscreen_action`, `flip_*`, `rane_*`, `remote_action`, `send_nothing`, and `timecode_no_jump`.

Those labels are interpretive. The extractor keeps the fields literal as `flag0_hidden` and `flag1_hidden`.

## Flag1 Hidden Rows

Flag1-hidden rows are the most interesting unpublished group: all 37 are absent from the official appendix, 14 have bundled Button Editor language descriptions, and 30 have exact `ACTION_*` method-symbol evidence. They should stay out of ordinary user-facing recommendations until locally tested, but several are good same-day probes.

See [Undocumented VDJScript Candidates](Undocumented%20VDJScript%20Candidates.md) for the full candidate inventory, promotion rules, and prioritized test queues.

| Area | Hidden rows | Evidence | Exploration angle |
| --- | --- | --- | --- |
| Browser | `browser_colorfilter_edit`, `load_security_shown` | Exact symbols: execute-only / query-only. | Color-filter editor and load-security state internals. |
| Config | `setting_if_unchanged` | Exact query symbol. | May test whether setting mutations are conditional or dirty-state aware. |
| Controller hardware | `assign_related_controller`, `controllerscreen_action`, `motorwheel2`, `motorwheel3`, `ns7_get_drift`, `rane_motor_enable`, `rane_timecode`, `rane_timecode_enable`, `send_nothing` | Several exact symbols; `assign_related_controller`, `rane_motor_enable`, `rane_timecode`, and `rane_timecode_enable` also have language descriptions. | Mostly controller/hardware context. Do not generalize without matching device or mapper evidence. |
| Cues | `hot_cue_stutter` | No official, language, or exact-class evidence. | Watch-only candidate unless another source appears. |
| Stems | `stem_volume` | Language description, no exact class. | Promising: description distinguishes slider-style stem volume from `stem` knob/isolate behavior. |
| Flow | `all_decks`, `combine_query` | Exact execute/query/bool/text symbols. | Potential grammar or multi-deck query combinators. Test carefully in readback contexts first. |
| Master deck values | `master_beat_num`, `masterbpm` | Exact execute/query symbols. | Compare with `get_bpm`, `masterdeck`, beatgrid, and sync helpers. |
| Flip macros | `flip_arm`, `flip_get_status`, `flip_load`, `flip_loop`, `flip_play`, `flip_record` | `flip_arm`, `flip_load`, `flip_loop`, `flip_play`, `flip_record` have language descriptions; several also have exact query/execute symbols. | Likely tied to saved Flip state; good candidate group if Flip functionality is available. |
| Pads | `get_pad_page_name`, `pad_page_favorite`, `pad_page_insplit`, `pad_page_split`, `pad_pressure_switch` | Exact symbols for all except `pad_pressure_switch`; `pad_page_insplit` and `pad_pressure_switch` have language descriptions. | Good pad-page state probes; likely useful for split/favorite page tooling. |
| Plugins | `effect_beats_sliderindex`, `is_colorfx` | Exact query symbols. | Low-risk readback candidates for effect UI state. |
| Rane screen | `rane_screen_input`, `rane_screen_output` | Exact execute/query and query symbols. | Hardware/display integration; not a general VDJScript surface yet. |
| Sampler | `sampler_inputgain` | Language description and exact execute/query symbols. | Promising hardware sampler input gain probe. |
| Remote skin | `remote_action` | Exact execute/query/bool/text symbols. | VirtualDJ Remote or remote-skin integration candidate. |
| System | `crash` | Language description and exact execute symbol. | Diagnostic/destructive-looking; do not run in a live session. |
| Timecode | `timecode_no_jump` | No official, language, or exact-class evidence. | Watch-only candidate unless timecode behavior suggests a safe probe. |

Language-backed flag1 hints from `Resources/languages.zip`:

Reproduce this group with:

```sh
python3 tools/extract_vdjscript_metadata.py --flag1-hidden --language-described-only --format csv
```

| Hidden row | Bundled description hint | Test implication |
| --- | --- | --- |
| `assign_related_controller` | Assigns a related controller to a deck while leaving the current controller untouched. | Requires a controller relationship/layer context. |
| `flip_arm` | Armed Flip playback starts when the playhead reaches the beginning of the Flip. | Needs an existing Flip and moving playhead. |
| `flip_load` | Loads a saved Flip for playback. | Needs saved Flip content. |
| `flip_loop` | Loops Flip playback when it reaches the end. | Test after loading or recording a Flip. |
| `flip_play` | Starts playback from the recorded Flip start. | Compare with `flip_get_status` readback. |
| `flip_record` | Prepares Flip recording; recording begins at the first cue point and stops when record is pressed again. | Needs cue points; record state must be observed carefully. |
| `pad_page_insplit` | Tests whether a referenced pad page belongs to a split, top or bottom. | Try normal pad view and split pad-page view. |
| `pad_pressure_switch` | Toggles pad pressure use. | Requires pressure-capable pad hardware to be meaningful. |
| `rane_motor_enable` | Reports/sends hardware motor state so software and controller motor state agree. | Requires matching Rane/motorized hardware context. |
| `rane_timecode` | Enables the controller-indexed timecode input and disables conflicting deck inputs from the same input. | Requires Rane/timecode input context. |
| `rane_timecode_enable` | Sets this deck to MIDI-controlled timecode play-state mode. | Requires compatible Rane/timecode mapping context. |
| `sampler_inputgain` | Sets gain for a hardware sampler input. | May need a hardware/input sampler path for audible effect. |
| `stem_volume` | Sets stem mix amount with direct stem names and aggregate groups; intended for 0-100% slider-style control rather than `stem` knob/isolate behavior. | First low-risk probe: compare `Vocal`, `Instru`, and aggregate names against visible stem levels and audio output. |
| `crash` | Bundled description presents it as an intentional crash/debug action. | Do not run in a live session; keep as diagnostic-only evidence. |

Same-day low-risk shortlist:

1. `stem_volume`: compare `stem_volume 'Vocal' 0%/50%/100%` with `stem 'vocal'`, visible stem levels, and audio output.
2. `sampler_inputgain`: check readback and whether values affect a hardware/input sampler path.
3. `get_pad_page_name`, `pad_page_insplit`, `pad_page_favorite`, `pad_page_split`: observe current/split/favorite pad-page state.
4. `is_colorfx`, `effect_beats_sliderindex`: observe ColorFX/effect beat-index state in labels and debug logs.
5. `flip_*`: only after confirming Flip is available; record whether `flip_get_status` changes across record/load/play/loop/arm actions.

## Documentation Use

Use this taxonomy as a fourth lens alongside:

- `Official`: public appendix coverage.
- `Built-in app resource`: language-description tags from `Resources/languages.zip`.
- `Binary string-table`: discovery-only runtime-looking names.
- `Binary compiled table`: Button Editor category placement and visibility.
- `Binary symbol table`: exact `ACTION_*` class and method-surface hints.

The Button Editor taxonomy is useful for category labels and broad grouping, but it should not become the whole documentation taxonomy. Some UI categories are very broad (`get`, `plugins`, `browser`), while some are implementation-oriented (`flow`, `macro`, `rane`). The curated docs should preserve domain-oriented groupings where they are clearer, and use Button Editor category as a source-backed metadata field.
