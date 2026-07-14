# Completeness Roadmap

This repo is already complete for official VDJScript name searchability. The remaining work is behavior depth: turning official names, bundled-resource hints, shipped XML examples, and local observations into reproducible, source-labeled guidance.

Use this file to choose the next evidence pass. Record detailed run results in [VDJScript Local Test Tracker](VDJScript%20Local%20Test%20Tracker.md), then promote stable conclusions into [VDJScript Verbs](VDJScript%20Verbs.md), [VirtualDJ Reference](VirtualDJ%20Reference.md), or the relevant topical file.

## Current Snapshot

| Area | Current state | Next completeness move |
| --- | --- | --- |
| Official VDJScript names | See [Official VDJScript Coverage Audit](Official%20VDJScript%20Coverage%20Audit.md) for current counts. | Keep count consistency automated and refresh when the official appendix changes. |
| Official behavior depth | See [Official VDJScript Coverage Audit](Official%20VDJScript%20Coverage%20Audit.md) for the current formal `Needs local test` gap. | Test no-hardware helpers first, then hardware helpers when matching devices are available. |
| Button Editor hidden candidates | 14 catalog-only names, 21 stricter runtime-string candidates, and 37 flag1-hidden compiled taxonomy rows outside the official appendix | Use [Undocumented VDJScript Candidates](Undocumented%20VDJScript%20Candidates.md) to keep them discovery-only until local behavior or stronger source evidence exists. |
| VDJScript grammar | Resolved: ternary/`&` precedence, nested-ternary associativity, and backtick-argument rules were tested via the Grammar Battery on v2026-m b9482 (2026-07-14) and promoted into [VDJScript Syntax Evidence](VDJScript%20Syntax%20Evidence.md) | Re-run [Reference - Grammar Battery Test](../tests/Pads/Reference%20-%20Grammar%20Battery%20Test.xml) only if a new VirtualDJ build changes parsing behavior. |
| Pad-page examples | Canonical pad pages exist for slot FX, ColorFX, and read-only sampler behavior; container schema documented in [Pad Page XML](Pad%20Page%20XML.md) | Resolve that doc's Open Questions (menu-DSL semantics, `custompadsmode` trigger, `pressure`/`right_click`) with small local probes. |
| Skin SDK | Broad coverage incl. the waveform family ([Skin Waveforms](Skin%20Waveforms.md)), root-level support elements, and browser styling children; the generated [Skin XML Inventory](Skin%20XML%20Inventory.md) reports zero undocumented elements | Finish `visual type` passes with small canary skins; verify the `Inference`-labeled browser-styling semantics (`<active>` trigger, `<buttons>` under `<plugins>`) with canaries. |
| Mappers | Format rewritten from real files; four working mappers in [examples/Mappers/Local](../examples/Mappers/README.md) gated by `tools/lint_mappers.py`; device-definition schema official-doc-derived | Author a minimal custom MIDI device definition + mapper pair and load-test it (a `SIMPLE_MIDI` device context already exists locally); probe the factory-mapper verb candidates (`browser_filter`, `browser_search`, `none`). |
| FX behavior | Good slot, ColorFX, PadFX, and stem-FX model notes | Add repeatable FX introspection, bank save/load, release-FX, and plugin-command passes; goal is a per-effect slider table for the native effects catalog. |
| Application internals and stems | Useful macOS-first notes and stem sidecar format documentation | Convert known unknowns into fixture-backed checks when safe. |

## Completion Tiers

Use these labels when deciding whether a topic is ready to promote:

| Tier | Meaning | Good destination |
| --- | --- | --- |
| Searchable | Name or topic is present with conservative source labels | `VDJScript Verbs.md` compact section or topical note |
| Fixture-ready | A safe local repro asset or clear manual script exists | `tests/` plus tracker row |
| Locally observed | Build, setup, steps, and observed result are recorded | `VDJScript Local Test Tracker.md` |
| Curated | Behavior is useful enough for copyable examples and caveats | `VirtualDJ Reference.md`, topical docs, canonical pads |
| Hardware verified | Device-specific helper tested on matching hardware | Mapper/controller docs and hardware-specific rows |

## Immediate No-Hardware Queue

These are the best next tests because they do not require new controller hardware.

| Priority | Topic | Fixture or source | Promotion target |
| ---: | --- | --- | --- |
| 1 | `dualdeckmode_decks` | [Reference - Dual Deck Mode Test.xml](../tests/Pads/Reference%20-%20Dual%20Deck%20Mode%20Test.xml) | Test any visible dual-deck pair/controller context. |
| 2 | `stem_volume`, `sampler_inputgain`, pad-page split/favorite helpers | [Reference - Hidden Button Editor Tests.xml](../tests/Pads/Reference%20-%20Hidden%20Button%20Editor%20Tests.xml) | Decide which catalog-only names deserve normal user-facing guidance. |
| 3 | `is_colorfx`, `effect_beats_sliderindex` | [Reference - Hidden Button Editor Tests.xml](../tests/Pads/Reference%20-%20Hidden%20Button%20Editor%20Tests.xml) | Improve effect selected-state and beat-slider docs if behavior is useful. |
| 4 | FX introspection sweep: remaining native effects plus `video`/`transition` targets | [Reference - FX Introspection Test.xml](../tests/Pads/Reference%20-%20FX%20Introspection%20Test.xml) | Partially complete: the fixture passed on v2026-m b9482 (deck FX slot 1, Backspin), both overloaded `get_effect_slider_default` forms are resolved, and a per-effect map has started in `Effects Engines.md` (Backspin done). Remaining: sweep the rest of the native effects catalog and repeat for `video` and `transition` targets; see the FX Helpers rows in `VDJScript Local Test Tracker.md`. |
| 5 | `effect_bank_save` / `effect_bank_load` | [Reference - FX Bank Test.xml](../tests/Pads/Reference%20-%20FX%20Bank%20Test.xml) | Document restored effect names, active state, sliders, and deck scope. |
| 6 | `effect_releaseslider*`, `is_releasefx` | [Reference - Release FX Test.xml](../tests/Pads/Reference%20-%20Release%20FX%20Test.xml) | Separate release-FX behavior from normal deck FX. |
| 7 | `effect_command` for BeatGrid only | [Reference - BeatGrid Command Test.xml](../tests/Pads/Reference%20-%20BeatGrid%20Command%20Test.xml) | Keep plugin-command examples plugin-specific. |
| 8 | `flip_*`, `setting_if_unchanged`, `masterbpm`, `master_beat_num`, `all_decks`, `combine_query` | [Undocumented VDJScript Candidates](Undocumented%20VDJScript%20Candidates.md) and hidden-candidate tracker rows | Add careful probes before any user-facing recommendation. |

`system` is intentionally not in the normal no-hardware queue. Revisit it only if an official example, bundled-resource context, or clearly harmless parameter appears.

## Hardware Queue

These should remain compact and conservative until the matching device or stock mapper context is available.

| Hardware/context | Helpers |
| --- | --- |
| Display-capable controller | `controllerscreen_deck`, `controller_battery` |
| Gemini controller display | `gemini_waveform_zoomlevel` |
| Phase hardware | `phase_movement`, `phase_position`, `phase_active` |
| Numark V7 | `v7_status` |
| Pioneer RZX | `rzx_touch`, `rzx_touch_x`, `rzx_touch_y` |
| DJC-family controller | `djc_shift`, `djc_button`, `djc_button_popup`, `djc_button_slider`, `djc_button_select`, `djc_panel` |
| Denon platter/display hardware | `denon_platter` |
| Rane or related hidden candidates | `assign_related_controller`, `rane_motor_enable`, `rane_timecode`, `rane_timecode_enable`, Rane screen helpers |

## Skin SDK Gaps

The broad skin docs are useful, but the next completeness pass should be fixture-led:

| Area | Next fixture |
| --- | --- |
| `visual type` variants | Small canary skin covering `color`, `waveform`, `spectrum`, `cover`, and documented source/action rules. |
| Placeholder substitution | Extend the existing placeholder condition canary only when a new rule is suspected. |
| Dynamic colors | Keep color, border, text, and skin-defined-color behavior in separate canaries. |
| Menus and dropzones | Add minimal canaries before documenting any trigger or drag behavior beyond official surfaces. |
| Built-in skin parser quirks | Keep raw built-in skins as shipped; normalize only separate fixtures. |

## Automation

Run these after documentation or fixture edits:

```sh
just check   # pads/skins/mappers linters, verb-index + inventory staleness gates,
             # reference status checker, git whitespace check
```

After adding or documenting skin/pad XML elements, regenerate the coverage report:

```sh
just inventory    # rewrites docs/Skin XML Inventory.md
just verb-index   # rewrites docs/vdjscript-verb-index.json after verb-doc edits
```

See [tools/README.md](../tools/README.md) for the full tool matrix and the new-VirtualDJ-build refresh procedure.

The status checker is intentionally offline. Use the live official appendix only when intentionally refreshing the coverage audit.
