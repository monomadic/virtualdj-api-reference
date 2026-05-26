# VirtualDJ Resources

Useful source links for maintaining this repo's VirtualDJ skin, pad, effect, and scripting notes.

## Source Policy

- Prefer current VirtualDJ manual and VDJPedia pages for syntax and supported behavior.
- Treat VirtualDJ forum posts as official only when the answer is from VirtualDJ staff, Development Manager, CTO, or Support staff.
- Treat Adion/CTO posts as high-authority implementation notes for scripting, audio-engine, and feature-behavior questions. VirtualDJ forum badges identify Adion as CTO, and Atomix's press archive confirms Atomix Productions acquired AdionSoft in 2011.
- Treat community skins, forum replies, Reddit posts, and GitHub snippets as examples to verify locally, not as authority.
- Treat working public skins as valuable provenance for discovery and searchability; record the exact skin, path, and line references before inferring semantics.
- Keep local conclusions labeled as `Inference` when they combine official docs with repo testing.

## Official Documentation

- [VirtualDJ Manual](https://www.virtualdj.com/manuals/virtualdj.html) - Current user manual.
- [VDJPedia](https://www.virtualdj.com/wiki/) - Wiki-style documentation and SDK pages.
- [Developer SDK](https://virtualdj.com/wiki/developers.html) - Entry point for skin, plugin, controller, and tool development.
- [Skin SDK](https://virtualdj.com/wiki/skin%20sdk%20.html) - Official skin package and element overview.
- [Skin Browser](https://www.virtualdj.com/wiki/Skin%2BBrowser.html) - `<browser>` element reference.
- [Custom Browser](https://virtualdj.com/wiki/custombrowser.html) - Official decomposition of the default browser into custom skin elements.
- [Split Panel](https://www.virtualdj.com/wiki/Split%20Panel.html) - `<split>` layout panels.
- [Skin Button](https://www.virtualdj.com/wiki/Skin%20Button.html) - Button actions, mouse handlers, and state graphics.
- [Skin SDK Dropzone](https://www.virtualdj.com/wiki/Skin%20SDK%20Dropzone.html) - Drag/drop target element.
- [Skin Panel](https://www.virtualdj.com/wiki/Skin%20SDK%20Panel.html) - Query-driven and named panels.
- [Skin Default Colors](https://virtualdj.com/wiki/Skin%20Default%20Colors.html) - Static and dynamic color handling.
- [Skin SDK Visual](https://virtualdj.com/wiki/skinsdkvisual.html) - Dynamic visuals, including color visuals.
- [VDJScript](https://www.virtualdj.com/wiki/VDJ%20Script.html) - Language overview.
- [VDJScript Verbs](https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html) - Current verb reference.
- [VDJScript Examples](https://www.virtualdj.com/wiki/VDJScript%20Examples) - Official example scripts.
- [Deck Effects Manual](https://www.virtualdj.com/manuals/virtualdj/interface/decks/decksadvanced/effects/) - Current deck FX layouts, including FX x6, stems FX, and effect-list behavior.
- [Options List](https://www.virtualdj.com/manuals/virtualdj/appendix/optionslist/) - Settings/options appendix.
- [Lyrics Editor](https://www.virtualdj.com/manuals/virtualdj/editors/lyricseditor.html) - AI-generated lyric editing, re-analysis, and censoring UI.
- [Stems Help](https://de.virtualdj.com/help/stems.html) - Official stems overview, stem controls, preparation behavior, and five-stem terminology.
- [VDJPedia Lists](https://de.virtualdj.com/wiki/Lists.html) - XML list and virtual folder structure for VirtualDJ 2024 and onwards.
- [Native Effects](https://www.virtualdj.com/manuals/virtualdj/appendix/nativeeffects/) - Built-in effect reference.
- [Pads Manual](https://www.virtualdj.com/manuals/virtualdj/interface/decks/decksadvanced/pads.html) - Pad pages and pad behavior.
- [Sampler Manual](https://www.virtualdj.com/manuals/virtualdj/interface/browser/sideview/sampler.html) - Sampler sideview, banks, pages, and drag/drop behavior.
- [How to Install Plugins and Addons](https://virtualdj.zendesk.com/hc/en-us/articles/360004467797-How-do-I-download-and-install-new-skins-effects-samples-etc) - Official support article for extensions.

## Official Forums And Staff Guidance

- [VirtualDJ Skins forum](https://www.virtualdj.com/forums/13/VirtualDJ_Skins.html) - Best place to search for skin engine behavior, staff clarifications, and examples.
- [VirtualDJ Technical Support forum](https://www.virtualdj.com/forums/2/VirtualDJ_Technical_Support.html) - Good for scripting, browser, sampler, and effect behavior questions.
- [Atomix Productions acquires AdionSoft](https://www.virtualdj.com/press/adionsoft.html) - Atomix press archive context for why Adion/CTO forum replies are treated as close implementation authority.
- [VirtualDJ 2020 - Additions in Skin Engine](https://www.virtualdj.com/forums/230926/VirtualDJ_Skins/VirtualDJ_2020_-_Additions_in_Skin_Engine.html) - Staff-maintained thread for skin engine additions.
- [Border Color using placeholder](https://virtualdj.com/forums/242871/VirtualDJ_Skins/Border_Color_using_placeholder.html) - Staff clarification that dynamic button border colors are not supported.
- [Skin text action; visibility or visual?](https://www.virtualdj.com/forums/267953/VirtualDJ_Skins/Skin_text_action%3B_visibility_or_visual%3F.html) - Staff guidance for dynamic skin text color.
- [effect_colorfx & effect_stems_color ?](https://www.virtualdj.com/forums/241078/VirtualDJ_Technical_Support/effect_colorfx___effect_stems_color__.html) - Staff discussion of extra ColorFX controls.
- [BUILD 7403 - Multiple stems fx can be used at the same time?](https://virtualdj.com/forums/250499/VirtualDJ_Technical_Support/BUILD_7403_____-Multiple_stems_fx_can_be_used_at_the_same_time__.html) - Adion/CTO guidance that stem FX targets can be treated as separate slots for `effect_*` actions.
- [Default filter and color fx filter](https://virtualdj.com/forums/252675/VirtualDJ_Technical_Support/Default_filter_and_color_fx_filter.html) - Staff guidance on filter and ColorFX behavior.
- [Aditional xml for Skins](https://virtualdj.com/forums/248589/Wishes_and_new_features/Aditional_xml_for_Skins.html) - Staff/forum context for runtime XML includes versus build-time composition.
- [Virtual DJ 2026](https://www.virtualdj.com/forums/266311/VirtualDJ_Technical_Support/Virtual_DJ_2026.html) - Staff launch-thread guidance on AI lyrics, prepared stems, re-analysis, and long-track limits.
- [How Lyrics are analyzed???](https://virtualdj.com/forums/267223/VirtualDJ_Technical_Support/How_Lyrics_are_analyzed%3F%3F%3F.html) - Staff explanation of lyric audio signatures, stems requirement, server cache, and local edits.
- [Lyrics issues with stems VDJ 2026](https://virtualdj.com/forums/266347/VirtualDJ_Technical_Support/Lyrics_issues_with_stems_VDJ_2026.html) - Early lyric/stems behavior reports and censor matching discussion.
- [Stems 2.0](https://virtualdj.com/forums/266488/VirtualDJ_Technical_Support/Stems_2.0.html) - Forum guidance around the Stems 2.0 requirement message for lyric extraction.
- [Where can I find the database.xml file on MacOS?](https://www.virtualdj.com/forums/261193/VirtualDJ_Technical_Support/Where_can_I_find_the_database_xml_file_on_MacOS_.html) - CTO reply plus user-confirmed macOS `database.xml` path under `~/Library/Application Support/VirtualDJ`.
- [Machine specific settings.xml and licence.dat?](https://www.virtualdj.com/forums/223863/VirtualDJ_Technical_Support/Machine_specific_settings_xml_and_licence_dat_.html) - Staff explanation of the VirtualDJ home folder, master database, and per-drive local databases.
- [XML Variables in Skin and Database](https://virtualdj.com/forums/230097/VirtualDJ_Technical_Support/XML_Variables_in_Skin_and_Database.html) - Staff clarification that local and global variables are separate names, and global variables must be queried with the `$` prefix.
- [Sending MIDI CC Commands](https://virtualdj.com/forums/249829/VirtualDJ_Technical_Support/Sending_MIDI_CC_Commands.html) - Staff clarification that device definitions do not evaluate VDJScript; dynamic behavior belongs in mapper actions.
- [Script/Param/Variable Maths](https://virtualdj.com/forums/251658/General_Discussion/Script_Param_Variable_Maths.html) - Adion/CTO clarification that `pitch` accepts beats parameters such as `pitch 128bt` to match a target BPM, plus a moderator example using `param_multiply` and `param_cast 'beats'`.
- [Bug in Instant Filters > Has Lyrics](https://virtualdj.com/forums/267592/VirtualDJ_Technical_Support/Bug_in_Instant_Filters_%3E_Has_Lyrics.html) - Forum workaround for "Has Lyrics" filter state matching.
- [Undocumented scripts](https://virtualdj.com/forums/213099/VirtualDJ_Technical_Support/Undocumented_scripts.html) - Staff clarification of old `effect X active` and `var 'name' X` syntax.
- [VDJ Script Verbs update](https://www.virtualdj.com/forums/205590/VirtualDJ_Skins/VDJ_Script_Verbs_update.html) - Staff clarification that skins and controllers share verbs, with the in-app editor as a discovery source.
- [Where can I find a VDJ script reference?](https://virtualdj.com/forums/264082/VirtualDJ_Technical_Support/Where_can_I_find_a_VDJ_script_reference%253F.html) - Staff/community discussion of VDJScript's intentionally concise reference style and debugging approaches.
- [How to map specific Fx?](https://virtualdj.com/forums/259342/VirtualDJ_Technical_Support/How_to_map_specific_Fx%3F.html) - Moderator examples for `padfx ... 'stemfx:vocal'` and `effect_show_gui vocals echo`.
- [Legacy Echo's Name?](https://virtualdj.com/forums/266350/VirtualDJ_Technical_Support/Legacy_Echo%27s_Name%3F.html) - Community/staff troubleshooting examples for stem-slot effect sliders and effect-name ambiguity.
- [Mix Assist in other skins](https://www.virtualdj.com/forums/231581/General_Discussion/Mix_Assist__in_other_skins.html) - Staff/community context for Mix FX, including the crossfader-linked effect behavior.
- [Saving 'PluginPage' Settings between sessions](https://www.virtualdj.com/forums/232382/General_Discussion/Saving__PluginPage__Settings_between_sessions.html) - Community/moderator Mix FX scripting examples, including `effect_mixfx_select`, `effect_mixfx_activate`, and indirect `param_equal` query patterns.
- [How to find the scripts behind a skin?](https://virtualdj.com/forums/261775/VirtualDJ_Technical_Support/How_to_find_the_scripts_behind_a_skin%3F.html) - Forum thread identifying the Mix FX verb family used by skins.
- [DDJ-FLX2 Advanced Setup](https://www.virtualdj.com/manuals/hardware/alphatheta/ddjflx2/advanced/index.html) - Official hardware manual note that Mix FX can be selected from Starter/Essentials skins or assigned with `effect_mixfx_select`.
- [DDJ-REV5 Effects](https://www.virtualdj.com/manuals/hardware/pioneer/ddjrev5/layout/effects.html) - Official hardware manual language for six VirtualDJ FX slots and selecting multiple slots.
- [DJM-S5 Effects](https://www.virtualdj.com/manuals/hardware/pioneer/djms5/layout/effects.html) - Official hardware manual language for the 6 FX Slots layout and bank controls.

## Community And Unofficial Sources

- [VirtualDJ Extensions](https://www.virtualdj.com/addons/) - Officially hosted but community-contributed skins, effects, pads, samples, and mappings. Useful for studying patterns; verify syntax before copying.
- [set local variable on init](https://www.virtualdj.com/forums/258819/General_Discussion/set_local_variable_on_init.html) - Community/moderator discussion of setting local variables during controller init and why numbered decks are safer than logical `deck left` for this job.
- [VirtualDJ Skins forum, non-staff posts](https://www.virtualdj.com/forums/13/VirtualDJ_Skins.html) - Useful examples and troubleshooting, but source-label as `Community` unless staff confirms the behavior.
- [r/virtualdj](https://www.reddit.com/r/virtualdj/) - Broad community troubleshooting. Useful for symptoms and user workflows, low authority for SDK details.
- [GitHub code search: VirtualDJ skin XML](https://github.com/search?q=VirtualDJ+skin.xml&type=code) - Occasional public examples and tooling. Check licenses and verify against current official docs.
- [Matroska Stem Files Internet-Draft](https://www.ietf.org/archive/id/draft-swhited-mka-stems-06.html) - External container-format context for multi-track stem files.

## Local Repo References

- [VirtualDJ Reference](VirtualDJ%20Reference.md) - Source-backed overview and preferred local patterns.
- [Lyrics AI and Skins](Lyrics%20AI%20and%20Skins.md) - AI lyrics, skin styling surface, filters, and useful script quirks.
- [Application Internals](Application%20Internals.md) - Low-level macOS paths, file formats, databases, stem sidecars, and shell examples.
- [Skin SDK](Skin%20SDK.md) - Local skin SDK reference.
- [Built-in skins](../Skins/Built-In/README.md) - App-bundle skin XML and assets used as semi-official executable examples.
- [VDJScript Verbs](VDJScript%20Verbs.md) - Curated verb notes.
- [Official VDJScript Coverage Audit](Official%20VDJScript%20Coverage%20Audit.md) - Names-only comparison against the live official VDJScript appendix.
- [Built-in pad pages](../Pads/Built-In/README.md) - App-bundle `pads_*.xml` copies used as semi-official executable examples.
- [Published Skin Findings](Published%20Skin%20Findings.md) - Provenance log for commands and patterns mined from working public skins.
- [Filter Syntax](Filter%20Syntax.md) - Browser filter notes.
- [Example Skin XML Objects](Example%20Skin%20XML%20Objects.md) - Local skin XML examples.
- [GraveRaver build demo](../Skins/GraveRaver/README.md) - Minimal XInclude source tree for the build workflow; not a polished skin reference.
- [GraveRaver build file](../Skins/GraveRaver/justfile) - Build-time XInclude workflow.
- [ModularSkeleton build skin](../Skins/ModularSkeleton/build/skin.xml) - Minimal modular skin scaffold output.
