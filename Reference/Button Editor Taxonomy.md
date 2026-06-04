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
```

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

| ID | Category | Total | Visible | Flag0 Hidden | Flag1 Hidden | Examples |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `flow` | 6 | 4 | 0 | 2 | `down`, `isrepeat`, `nothing`, `up` |
| 2 | `param` | 32 | 26 | 6 | 0 | `blink`, `color`, `param_bigger`, `param_equal` |
| 3 | `repeat` | 7 | 7 | 0 | 0 | `doubleclick`, `holding`, `repeat`, `wait` |
| 4 | `skin` | 31 | 26 | 4 | 1 | `custom_button`, `get_skin_color`, `skin_panel` |
| 5 | `system` | 21 | 18 | 2 | 1 | `debug`, `get_cpu`, `get_date`, `system` |
| 6 | `variables` | 13 | 13 | 0 | 0 | `get_var`, `set_var`, `toggle`, `var_equal` |
| 7 | `window` | 5 | 5 | 0 | 0 | `close`, `maximize`, `show_window` |
| 8 | `audio` | 24 | 24 | 0 | 0 | `beatjump`, `clone_deck`, `dualdeckmode`, `mute` |
| 9 | `audio_controls` | 15 | 13 | 2 | 0 | `play`, `pause`, `stop`, `silent_cue` |
| 10 | `audio_inputs` | 11 | 10 | 1 | 0 | `mic`, `linein`, `aux_volume`, `mic_eq_high` |
| 11 | `audio_scratch` | 26 | 18 | 8 | 0 | `jogwheel`, `motorwheel`, `scratch`, `touchwheel` |
| 12 | `audio_volumes` | 55 | 47 | 8 | 0 | `crossfader`, `gain`, `level`, `master_volume` |
| 13 | `automix` | 31 | 30 | 1 | 0 | `automix`, `mix_now`, `playlist_add` |
| 14 | `browser` | 89 | 82 | 5 | 2 | `add_list`, `browser_scroll`, `search`, `sideview_options` |
| 15 | `config` | 29 | 25 | 3 | 1 | `setting`, `setting_reset`, `save_config`, `settings` |
| 16 | `controllers` | 75 | 66 | 0 | 9 | `action_deck`, `djc_button`, `os2l_cmd` |
| 17 | `cues` | 31 | 28 | 2 | 1 | `cue`, `cue_color`, `hot_cue`, `set_cue` |
| 18 | `deck_select` | 11 | 11 | 0 | 0 | `leftdeck`, `rightdeck`, `masterdeck`, `pfl` |
| 19 | `equalizer` | 37 | 29 | 7 | 1 | `eq_high`, `eq_kill_low`, `stem`, `stems_split` |
| 20 | `get` | 118 | 115 | 1 | 2 | `get_album`, `get_bpm`, `get_title`, `loaded` |
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

## Documentation Use

Use this taxonomy as a fourth lens alongside:

- `Official`: public appendix coverage.
- `Built-in app resource`: language-description tags from `Resources/languages.zip`.
- `Binary string-table`: discovery-only runtime-looking names.
- `Binary compiled table`: Button Editor category placement and visibility.
- `Binary symbol table`: exact `ACTION_*` class and method-surface hints.

The Button Editor taxonomy is useful for category labels and broad grouping, but it should not become the whole documentation taxonomy. Some UI categories are very broad (`get`, `plugins`, `browser`), while some are implementation-oriented (`flow`, `macro`, `rane`). The curated docs should preserve domain-oriented groupings where they are clearer, and use Button Editor category as a source-backed metadata field.
