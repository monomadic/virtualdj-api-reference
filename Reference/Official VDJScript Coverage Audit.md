# Official VDJScript Coverage Audit

Fetched from the current VirtualDJ VDJScript verbs appendix on 2026-05-26.

Purpose: keep this repo honest about official verb coverage. This is a names-only audit, not a copy of the official manual. Use it to decide what still needs curated local documentation in `VDJScript Verbs.md`.

Source: https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html

Official verb/alias names parsed: 991
Names already present in local VDJScript reference: 991
Names not yet present in local VDJScript reference: 0

Related local cross-check: [Button Editor Catalog Audit](Button%20Editor%20Catalog%20Audit.md). The local VirtualDJ app's bundled Button Editor language catalog has 813 unique `<Actions>` tags across all language files, and the richer runtime-looking executable string block has 967 names. These sources overlap with, but do not exactly match, the official appendix.

## Immediate Rule

- Do not delete a VDJScript command only because it appears unfamiliar. Check this audit and the official appendix first.
- Promote compact official entries into curated sections as they become relevant to skins, pads, mappings, or local tests.
- Keep discovered published-skin usage in `Published Skin Findings.md` even after the command is confirmed official.

## Coverage Tiers

- **Curated**: documented in dedicated sections of `VDJScript Verbs.md` with surfaces, examples, notes, and source labels.
- **Broad catalog**: documented in compact tables by functional area.
- **Compact official remainder**: currently empty; the section remains in `VDJScript Verbs.md` only as an audit marker.
- **Needs local test**: official names whose behavior is sparse, hardware-specific, or environment-dependent.

## Current Readiness Snapshot

- **Official-name coverage is complete**: 991/991 official verb and alias names are present in `VDJScript Verbs.md`; missing official names are at 0.
- **Searchability is complete**: the compact official remainder is empty, so every tracked official name now lives in a functional section rather than only in a holding table.
- **Behavior confidence is not uniform**: high-frequency skin, pad, sampler, browser, loop, cue, FX, stems, timecode, video, config, and mixer helpers now have useful local notes or examples, while low-frequency hardware/developer helpers remain compact and conservative.
- **The formal local-test gap is 21 official names**, about 2.1% of the official list. Three no-dedicated-hardware sparse helpers (`deck_has_error`, `get_mixfx_active`, and `system`) still need better behavior evidence, one is optional deck/controller setup (`dualdeckmode_decks`), and the rest are hardware-specific controller helpers.
- **Reasonably complete for everyday documentation** means official-name coverage and searchability are complete. The earlier no-hardware sparse-helper pass is recorded for prior sparse names, but `deck_has_error` and `get_mixfx_active` still need lightweight local checks. Fully verified coverage would require target controller hardware for controller-screen, Phase, RZX, DJC, V7, Gemini, and Denon-specific helpers.
- **Bundled app-resource evidence now exists**: the Button Editor action-description catalog is stored in the local app bundle's `Resources/languages.zip`. It is useful for descriptions and discovery, but it omits some official sparse helpers and includes a small number of catalog/runtime candidates outside the official appendix.

What still sticks out:

- `deck_has_error` and `get_mixfx_active` are official sparse helpers added in the 2026-05-26 appendix refresh; they are present in functional sections but still need local behavior checks.
- `system` is official but still too sparse to promote: local testing only showed blank text return and no visible action result in the sparse-helper pad context.
- `dualdeckmode_decks` has official context through `dualdeckmode`; the bundled Button Editor language catalog also includes it in several non-English files, but its direct helper behavior still needs observation.
- Hardware-specific helpers are the largest remaining blind spot; they are probably fine as compact official entries unless this repo gains access to the matching devices.

## Next Promotion Targets

- No compact-remainder names currently remain.
- Next depth pass: locally test `deck_has_error` and `get_mixfx_active`, revisit `system` only if official examples or harmless parameters are found, then test `dualdeckmode_decks` in an appropriate deck/controller context.
- Next hardware pass: verify controller-specific helpers such as `controllerscreen_deck`, `controller_battery`, `phase_*`, `rzx_*`, `djc_*`, and `denon_platter` on target hardware.
- Promotion rule: do not remove a verb from **Needs local test** until [VDJScript Local Test Tracker](VDJScript%20Local%20Test%20Tracker.md) has a build, context/hardware, observed result, and notes.

## Recently Promoted

- Saved loops: `saved_loop_prepare`, `saved_loop_autotrigger`, `loop_load_prepare`, `saved_loop_display`, `loop_color`
- Sampler groups and sampler-to-deck: `sampler_group_color`, `sampler_group_name`, `sampler_group_mute`, `sampler_has_group`, `sampler_load_to_deck`
- Mix points: `goto_mixpoint`, `set_mixpoint`, `set_loadpoint`
- Timecode and video: `timecode_config`, `timecode_pitch`, `timecode_cd_mode`, `timecode_options`, `video_crossfader_link`, `video_crossfader_auto`, `video_delay`, `video_level`
- Pitch, jog, and motor behavior: `pitch_relative`, `pitch_motorized`, `pitch_lock`, `startupspeed`, `brakespeed`, `backspin`, `scratch_wheel`, `motor_switch`, `motorwheel_instant_play`
- Controller display and hardware helpers: `controller_mapping`, `controllerscreen_deck`, `controller_battery`, `menu`, `menu_button`, `denon_platter`, `phase_*`, `djc_*`
- Mixer/EQ helpers: `cross_assign`, `eq_crossfader_high`, `eq_crossfader_mid`, `eq_crossfader_low`, `high_label`, `mid_label`, `low_label`, `mixer_order`
- Config and browser workflow helpers: `auto_pitch_lock`, `auto_sync_settings`, `keyboard_shortcuts`, `mark_linked_tracks`, `browsed_song`, `loaded_song`
- Final compact remainder sweep: `beat_juggle`, `dualdeckmode_decks`, `shift_all_cues`, `sort_cues`, `repeat_song`, `get_beat`, `key_match_button`, `key_match_menu`, `sampler_default`, `sampler_rapidfire`, `os2l_scene`, `open_stem_creator`, `handshake`, `is_using`, `system`, `debug`, `connect`
- 2026-05-26 appendix refresh: `deck_has_error`, `get_mixfx_active`
- Local-tested sparse helpers: `connect`, `karaoke_venue_name`, `open_stem_creator`

## Needs Local Test

Manual verification lives in [VDJScript Local Test Tracker](VDJScript%20Local%20Test%20Tracker.md).

- `deck_has_error`, `get_mixfx_active`, `system`, `controllerscreen_deck`, `controller_battery`, `gemini_waveform_zoomlevel`
- `phase_movement`, `phase_position`, `phase_active`, `v7_status`, `rzx_touch`, `rzx_touch_x`, `rzx_touch_y`
- `djc_shift`, `djc_button`, `djc_button_popup`, `djc_button_slider`, `djc_button_select`, `djc_panel`
- `denon_platter`, `dualdeckmode_decks`

## Missing Official Names

None currently. All official verb/alias names parsed in this audit are present in the local VDJScript reference.

## Covered Official Names

Former missing names closed in the latest coverage pass:

- `auto_pitch_lock`, `auto_sync_settings`, `backspin`, `beat_juggle`, `brakespeed`, `broadcast_message`
- `controller_battery`, `controller_mapping`, `controllerscreen_deck`, `cross_assign`, `djc_button`, `djc_button_popup`
- `djc_button_select`, `djc_button_slider`, `djc_panel`, `djc_shift`, `dualdeckmode_decks`, `eq_crossfader_high`
- `eq_crossfader_low`, `eq_crossfader_med`, `eq_crossfader_mid`, `fader_start`, `gemini_waveform_zoomlevel`, `goto_mixpoint`
- `handshake`, `high_label`, `invert_timecode`, `is_audioonlyvisualisation`, `jog_wheel`, `karaoke_options`
- `karaoke_venue_name`, `key_match_button`, `key_match_menu`, `keyboard_shortcuts`, `leftvideo_button`, `low_label`
- `mark_linked_tracks`, `mark_related_tracks`, `mid_label`, `midiclock_active`, `miditovst_active`, `mixer_order`
- `mixermode`, `motor_switch`, `motorwheel_instant_play`, `open_stem_creator`, `os2l_scene`, `over_video`
- `overvideo`, `phase_active`, `phase_movement`, `phase_position`, `pitch2`, `pitch2_slider`
- `pitch_lock`, `pitch_motorized`, `pitch_relative`, `pitchlock`, `record_config`, `record_vu`
- `repeat_song`, `rightvideo_button`, `rzx_touch`, `rzx_touch_x`, `rzx_touch_y`, `sampler_default`
- `sampler_group_color`, `sampler_group_mute`, `sampler_group_name`, `sampler_has_group`, `sampler_load_to_deck`, `sampler_rapidfire`
- `saved_loop_autotrigger`, `saved_loop_prepare`, `saveregistryconfig`, `scratch_wheel`, `scratch_wheel_touch`, `scratchwheel_touch`
- `select_master_output`, `set_loadpoint`, `set_mixpoint`, `setting_ismodified`, `setting_reset`, `setting_setdefault`
- `setting_setsession`, `setting_setsession_deck`, `shift_all_cues`, `smart_scratch`, `sort_cues`, `speedwheel_touch`
- `startupspeed`, `stopwatch_reset`, `switch_skin_variation`, `timecode_cd_mode`, `timecode_config`, `timecode_motor_enable`
- `timecode_options`, `timecode_pitch`, `timecode_reset_pitch`, `v7_status`, `video_crossfader_auto`, `video_crossfader_link`
- `video_delay`, `video_fadetoblack`, `video_level`

- `action_deck`, `add_favoritefolder`, `add_filterfolder`, `add_list`, `add_to_list`, `add_virtualfolder`
- `adjust_cbg`, `apply_audio_config`, `assign_controller`, `auto_bpm_transition`, `auto_bpm_transition_options`, `auto_crossfade`
- `auto_crossfader`, `auto_cue`, `auto_match_bpm`, `auto_match_key`, `auto_sync`, `auto_sync_options`
- `automix`, `automix_add_next`, `automix_dualdeck`, `automix_editor`, `automix_editor_movetrack`, `automix_skip`
- `aux_volume`, `beat_tap`, `beatjump`, `beatjump_pad`, `beatjump_page`, `beatjump_select`
- `beatlock`, `blink`, `blink_play`, `booth_volume`, `bpm_stabilizer`, `broadcast`
- `browsed_file_analyze`, `browsed_file_color`, `browsed_file_info`, `browsed_file_prepare_stems`, `browsed_file_reload_tag`, `browsed_file_rename`
- `browsed_file_reveal`, `browsed_song`, `browsed_song_hashtag`, `browser`, `browser_enter`, `browser_export`
- `browser_folder`, `browser_geniusdj`, `browser_gotofolder`, `browser_isactive`, `browser_move`, `browser_open_folder`
- `browser_options`, `browser_padding`, `browser_remove`, `browser_scroll`, `browser_shortcut`, `browser_sort`
- `browser_window`, `browser_zoom`, `can_sandbox`, `clear_search`, `clone_deck`, `clone_from_deck`
- `close`, `color`, `color_mix`, `colorfx_prefader`, `colorfx_slider`, `config`
- `connect`, `constant`, `controllervar`, `countdown`, `create_list_from_playlist`, `create_virtualfolder_from_playlist`
- `crossfader`, `crossfader_curve`, `crossfader_disable`, `crossfader_hamster`, `crossfader_slider`, `cue`
- `cue_3button`, `cue_action`, `cue_button`, `cue_color`, `cue_countdown`, `cue_counter`
- `cue_countup`, `cue_cup`, `cue_display`, `cue_loop`, `cue_loop_autosync`, `cue_loop_hold`
- `cue_name`, `cue_play`, `cue_pos`, `cue_select`, `cue_stop`, `cues_options`
- `custom_button`, `custom_button_edit`, `custom_button_name`, `cycle`, `debug`, `deck_has_error`, `deck_options`
- `delete_cue`, `denon_platter`, `device_side`, `dim`, `display_time`, `djc_mic`
- `doubleclick`, `down`, `dualdeckmode`, `dump`, `edit_bpm`, `edit_comment`
- `edit_lyrics`, `edit_poi`, `edit_search`, `edit_singer`, `effect_3slots_layout`, `effect_activate`
- `effect_active`, `effect_arm_active`, `effect_arm_beats`, `effect_arm_bpm`, `effect_arm_deck`, `effect_arm_select`
- `effect_arm_select_popup`, `effect_arm_slider`, `effect_arm_slider_label`, `effect_arm_slider_name`, `effect_arm_slider_text`, `effect_arm_slot`
- `effect_arm_stem`, `effect_bank_load`, `effect_bank_save`, `effect_beats`, `effect_beats_all`, `effect_bpm_deck`
- `effect_bpm_deck_tap`, `effect_button`, `effect_clone`, `effect_colorfx`, `effect_colorslider`, `effect_command`
- `effect_disable_all`, `effect_dock_gui`, `effect_fxsendreturndeck`, `effect_fxsendreturndeck_multi`, `effect_fxsendreturnenable`, `effect_has_beats`
- `effect_has_button`, `effect_has_length`, `effect_has_slider`, `effect_list`, `effect_list_edit`, `effect_mixfx`
- `effect_mixfx_activate`, `effect_mixfx_select`, `effect_releaseslider`, `effect_releaseslider_active`, `effect_select`, `effect_select_multi`
- `effect_select_popup`, `effect_select_toggle`, `effect_show_gui`, `effect_slider`, `effect_slider_activate`, `effect_slider_active`
- `effect_slider_reset`, `effect_slider_skip_length`, `effect_slider_slider`, `effect_stems`, `effect_stems_color`, `effect_string`
- `effects_used`, `emergency_play`, `eq_high`, `eq_high_freq`, `eq_high_slider`, `eq_kill_high`
- `eq_kill_low`, `eq_kill_med`, `eq_kill_mid`, `eq_low`, `eq_low_freq`, `eq_low_slider`
- `eq_med`, `eq_mid`, `eq_mid_freq`, `eq_mid_slider`, `eq_mode`, `eq_reset`
- `eventscheduler`, `eventscheduler_start`, `fadeout`, `fader_curve`, `fake_eq`, `fake_filter`
- `fake_gain`, `fake_hp`, `fake_hpmix`, `fake_master`, `fake_mixer`, `fake_pfl`
- `false`, `file_count`, `file_info`, `filter`, `filter_activate`, `filter_label`
- `filter_resonance`, `filter_selectcolorfx`, `filter_slider`, `font_size`, `gain`, `gain_label`
- `gain_relative`, `gain_slider`, `get_active_loop`, `get_activedeck`, `get_album`, `get_arm`
- `get_artist`, `get_artist_before_feat`, `get_artist_title`, `get_artist_title_separator`, `get_askthedj`, `get_askthedj_unread`
- `get_automix`, `get_automix_position`, `get_automix_song`, `get_bar`, `get_battery`, `get_beat`
- `get_beat2`, `get_beat_bar`, `get_beat_counter`, `get_beat_num`, `get_beatdiff`, `get_beatgrid`
- `get_beatpos`, `get_bpm`, `get_bpm_match`, `get_browsed_album`, `get_browsed_artist`, `get_browsed_artist_title`
- `get_browsed_bpm`, `get_browsed_color`, `get_browsed_comment`, `get_browsed_composer`, `get_browsed_filepath`, `get_browsed_folder`
- `get_browsed_folder_icon`, `get_browsed_folder_path`, `get_browsed_folder_scrollpos`, `get_browsed_folder_scrollsize`, `get_browsed_folder_selection_index`, `get_browsed_folder_tab`
- `get_browsed_genre`, `get_browsed_header`, `get_browsed_key`, `get_browsed_scrollpos`, `get_browsed_scrollsize`, `get_browsed_selection_index`
- `get_browsed_song`, `get_browsed_title`, `get_browsed_title_artist`, `get_build`, `get_clock`, `get_comment`
- `get_composer`, `get_constant`, `get_controller_image`, `get_controller_name`, `get_controller_screen`, `get_cpu`
- `get_crossfader_result`, `get_cue`, `get_custom_text`, `get_date`, `get_deck`, `get_deck_analysis`
- `get_deck_color`, `get_deck_letter`, `get_decks`, `get_defaultdeck`, `get_denon_cuepoints`, `get_denon_platter`
- `get_display`, `get_effect_button_count`, `get_effect_button_name`, `get_effect_button_shortname`, `get_effect_name`, `get_effect_slider_count`
- `get_effect_slider_default`, `get_effect_slider_label`, `get_effect_slider_label_full`, `get_effect_slider_label_skip_length`, `get_effect_slider_name`, `get_effect_slider_name_skip_length`
- `get_effect_slider_shortname`, `get_effect_slider_text`, `get_effect_slider_text_skip_length`, `get_effect_string`, `get_effect_string_name`, `get_effect_title`
- `get_effects_used`, `get_featuring_after_artist`, `get_filename`, `get_filepath`, `get_filesize`, `get_firstbeat`
- `get_firstbeat_local`, `get_gemini_display`, `get_gemini_waveform`, `get_genre`, `get_harmonic`, `get_hasheadphone`
- `get_hasheadphones`, `get_hasinput`, `get_haslinein`, `get_hasmaster`, `get_hasmic`, `get_hastimecode`
- `get_hwnd`, `get_karaoke_background_song`, `get_key`, `get_key_color`, `get_key_modifier`, `get_key_modifier_text`
- `get_leftdeck`, `get_lemode`, `get_level`, `get_level_left`, `get_level_left_peak`, `get_level_log`
- `get_level_peak`, `get_level_right`, `get_level_right_peak`, `get_license`, `get_limiter`, `get_loaded_song`
- `get_loaded_song_color`, `get_loop`, `get_loop_in_time`, `get_loop_out_time`, `get_lyrics_language`, `get_membership`
- `get_mixfx_active`, `get_nb_multicam`, `get_next_karaoke_song`, `get_ns7_platter`, `get_numark_beatgrid`, `get_numark_songpos`, `get_numark_waveform`
- `get_peak_audio`, `get_phrase_num`, `get_pioneer_display`, `get_pioneer_loop_display`, `get_pitch`, `get_pitch_value`
- `get_pitch_zero`, `get_playlist_time`, `get_plugindeck`, `get_position`, `get_record_message`, `get_record_min`
- `get_record_ms`, `get_record_msf`, `get_record_sec`, `get_record_size`, `get_record_time`, `get_remix_after_title`
- `get_rightdeck`, `get_rotation`, `get_rotation_cue`, `get_rotation_slip`, `get_sample_color`, `get_sample_info`
- `get_sample_name`, `get_sample_slot_name`, `get_sampler_bank`, `get_sampler_bank_count`, `get_sampler_bank_id`, `get_sampler_count`
- `get_sampler_slot`, `get_sampler_used`, `get_saved_loop`, `get_scratch_direction`, `get_skin_color`, `get_slip_active`
- `get_slip_time`, `get_song_event`, `get_songlength`, `get_spectrum_band`, `get_status`, `get_text`
- `get_time`, `get_time_hour`, `get_time_min`, `get_time_ms`, `get_time_msf`, `get_time_sec`
- `get_time_sign`, `get_timecode_quality`, `get_title`, `get_title_artist`, `get_title_before_remix`, `get_title_remix`
- `get_totaltime_min`, `get_totaltime_ms`, `get_totaltime_msf`, `get_totaltime_sec`, `get_username`, `get_var`
- `get_vdj_folder`, `get_version`, `get_video_fx_slider_label`, `get_videofx_name`, `get_videotrans_name`, `get_volume`
- `get_vu_meter`, `get_vu_meter_left`, `get_vu_meter_left_peak`, `get_vu_meter_peak`, `get_vu_meter_right`, `get_vu_meter_right_peak`
- `get_year`, `getfood`, `goto`, `goto_bar`, `goto_cue`, `goto_first_beat`
- `goto_last_folder`, `goto_start`, `grid_view`, `has_aux`, `has_battery`, `has_cover`
- `has_cue`, `has_custom_button`, `has_karaoke_next`, `has_linked_tracks`, `has_logo`, `has_lyrics`
- `has_notch`, `has_quick_filter`, `has_stems`, `has_system_volume`, `has_variable_bpm`, `has_video_mix`
- `headphone_crossfader`, `headphone_gain`, `headphone_mix`, `headphone_volume`, `hold`, `holding`
- `hot_cue`, `hotcue`, `info_options`, `infos_options`, `invert_controllers`, `invert_deck`
- `is_audible`, `is_battery`, `is_fluid`, `is_karaoke_idle`, `is_karaoke_playing`, `is_mac`
- `is_macos`, `is_pc`, `is_releasefx`, `is_sync`, `is_using`, `is_video`
- `is_windows`, `isrepeat`, `jog`, `jogwheel`, `karaoke`, `karaoke_add`
- `karaoke_load`, `karaoke_show`, `key`, `key_lock`, `key_move`, `key_smooth`
- `keycue_pad`, `keycue_pad_color`, `keycue_pad_jump`, `keycue_pad_page`
- `keylock`, `leftcross`, `leftdeck`, `leftvideo`, `level`, `level_slider`
- `levelfader_curve`, `linein`, `linein_rec`, `load`, `load_deck_set`, `load_next`
- `load_previous`, `load_pulse`, `load_pulse_active`, `load_skin`, `loaded`, `loaded_song`
- `loaded_song_hashtag`, `lock_cues`, `lock_panel`, `lock_pannel`, `log_search`, `loop`
- `loop_adjust`, `loop_back`, `loop_button`, `loop_double`, `loop_exit`, `loop_half`
- `loop_color`, `loop_delete`, `loop_load_prepare`
- `loop_in`, `loop_length`, `loop_load`, `loop_move`, `loop_options`, `loop_out`
- `loop_pad`, `loop_pad_mode`, `loop_pad_page`, `loop_position`, `loop_roll`, `loop_roll_mode`
- `loop_save`, `loop_select`, `macro_play`, `macro_record`, `master_balance`, `master_tempo`
- `master_volume`, `masterdeck`, `masterdeck_auto`, `match_bpm`, `match_gain`, `match_key`
- `maximize`, `menu`, `menu_button`, `menu_cycledisplay`, `mic`, `mic2_volume`
- `mic_eq_high`, `mic_eq_low`, `mic_eq_mid`, `mic_rec`, `mic_talkover`, `mic_volume`
- `microphone`, `minimize`, `mix_and_load_next`, `mix_next`, `mix_next_sidelist`, `mix_now`
- `mix_now_nosync`, `mix_selected`, `mono_mix`, `motorwheel`, `move_deck`, `multibutton`
- `multibutton_select`, `mute`, `mute_stem`, `no`, `not_played`, `nothing`
- `ns7_platter`, `nudge`, `numark_waveform_zoom`, `off`, `on`, `only_stem`
- `open_help`, `pad`, `pad_bank2`, `pad_button_color`, `pad_color`, `pad_edit`
- `os2l_button`, `os2l_cmd`, `os2l_info`
- `pad_has_16pads`, `pad_has_action`, `pad_has_color`, `pad_has_menu`, `pad_has_param`, `pad_has_pressure`
- `pad_menu`, `pad_page`, `pad_page_favorite_select`, `pad_page_select`, `pad_pages`, `pad_param`
- `pad_param2`, `pad_param_visible`, `pad_pressure`, `pad_pushed`, `padfx`, `padfx_single`
- `padshift`, `padshift_button_color`, `padshift_pressure`, `page`, `param_1_x`, `param_add`
- `param_bigger`, `param_cast`, `param_contains`, `param_delta`, `param_equal`, `param_greater`
- `param_invert`, `param_lowercase`, `param_make_discrete`, `param_mod`, `param_multiply`, `param_pingpong`
- `param_pow`, `param_smaller`, `param_ucfirst`, `param_uppercase`, `pause`, `pause_stop`
- `pfl`, `phrase_sync`, `pioneer_cue`, `pioneer_loop`, `pioneer_loop_in`, `pioneer_loop_out`
- `pioneer_play`, `pitch`, `pitch_bend`, `pitch_range`, `pitch_reset`, `pitch_slider`
- `pitch_zero`, `play`, `play_3button`, `play_button`, `play_mode`, `play_onbeat`
- `play_options`, `play_pause`, `play_stutter`, `play_sync`, `play_sync_onbeat`, `playlist_add`
- `playlist_clear`, `playlist_load`, `playlist_load_and_keep`, `playlist_load_and_remove`, `playlist_options`, `playlist_randomize`
- `playlist_randomize_once`, `playlist_remove_duplicates`, `playlist_remove_played`, `playlist_repeat`, `playlist_save`, `pluginsongpos`
- `power_gain`, `prelisten`, `prelisten_info`, `prelisten_options`, `prelisten_output`, `prelisten_pos`
- `prelisten_stop`, `preview`, `pulse`, `quantize_all`, `quick_filter`, `rack`
- `quantize_loop`, `quantize_setcue`
- `rack_prioritize`, `rack_solo`, `rating`, `reanalyze`, `record`, `record_cut`
- `recurse_folder`, `refresh_controller`, `reinit_controller`, `relay_play`, `reloop`, `reloop_exit`
- `repeat`, `repeat_start`, `repeat_start_instant`, `repeat_stop`, `rescan_controllers`, `reverse`
- `rightcross`, `rightdeck`, `rightvideo`, `sampler_abort_rec`, `sampler_assign`, `sampler_bank`
- `sampler_color`, `sampler_edit`, `sampler_group_volume`, `sampler_loaded`, `sampler_loop`, `sampler_mode`
- `sampler_mute`, `sampler_options`, `sampler_output`, `sampler_pad`, `sampler_pad_page`, `sampler_pad_shift`
- `sampler_pad_volume`, `sampler_pfl`, `sampler_play`, `sampler_play_stop`, `sampler_play_stutter`, `sampler_position`
- `sampler_rec`, `sampler_rec_delete`, `sampler_select`, `sampler_start_rec`, `sampler_stop`, `sampler_stop_rec`
- `sampler_unload_from_deck`, `sampler_used`, `sampler_volume`, `sampler_volume_master`, `sampler_volume_nogroup`, `sandbox`
- `sampler_velocity`
- `save_config`, `save_deck_set`, `saved_loop`, `scratch`, `scratch_dna`, `scratch_dna_editor`
- `saved_loop_display`
- `scratch_dna_option`, `scratch_hold`, `scratchbank_unload`, `scratchwheel`, `search`, `search_add`
- `scratchbank_assign`, `scratchbank_edit`, `scratchbank_load`, `scratchbank_load_to_deck`
- `search_delete`, `search_folder`, `search_folder_options`, `search_options`, `search_playlists`, `seek`
- `select`, `set`, `set_bpm`, `set_browsed_file_bpm`, `set_cue`, `set_deck`
- `set_firstbeat`, `set_fluid`, `set_gain`, `set_key`, `set_var`, `set_var_dialog`
- `set_variable_bpm`, `setting`, `settings`, `shift`, `show_keyboard`, `show_pluginpage`
- `show_splitpanel`, `show_text`, `show_window`, `sidelist_add`, `sidelist_clear`, `sidelist_load`
- `sidelist_load_and_keep`, `sidelist_load_and_remove`, `sidelist_options`, `sidereco_options`, `sidereco_song`, `sidereco_source`
- `sideview`, `sideview_options`, `sideview_sort`, `sideview_title`, `sideview_triggerpad`, `silent_cue`
- `skin_empty_buttons`, `skin_height`, `skin_panel`, `skin_panelgroup`, `skin_panelgroup_available`, `skin_pannel`
- `skin_pannelgroup`, `skin_starter_tip`, `skin_width`, `slicer`, `slip`, `slip_mode`
- `smart_cue`, `smart_fader`, `smart_loop`, `smart_play`, `song_pos`, `songpos_remain`
- `songpos_warning`, `speedwheel`, `stem`, `stem_color`, `stem_pad`, `stems_split`
- `stems_bleed`
- `stems_split_unlink`, `stop`, `stop_3button`, `stop_button`, `stopwatch`, `swap_decks`
- `switch_sidelist_playlist`, `sync`, `sync_hint`, `sync_nocbg`, `system`, `system_volume`
- `timecode_active`, `timecode_bypass`, `timecode_mode`, `toggle`, `touchwheel`, `touchwheel_touch`
- `true`, `undo_load`, `unload`, `up`, `var`, `var_equal`
- `var_greater`, `var_list`, `var_not_equal`, `var_smaller`, `video`, `video_crossfader`
- `video_fx`, `video_fx_button`, `video_fx_clear`, `video_fx_select`, `video_fx_slider`, `video_fx_slider_slider`
- `video_output`, `video_source`, `video_source_select`, `video_transition`, `video_transition_button`, `video_transition_select`
- `video_transition_slider`, `video_transition_slider_slider`, `view_options`, `vinyl_mode`, `virtualfolder_add`, `volume`
- `volume_slider`, `wait`, `wheel_mode`, `yes`, `zoom`, `zoom_scratch`
- `zoom_vertical`
