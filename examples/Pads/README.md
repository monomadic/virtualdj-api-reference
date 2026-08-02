# VirtualDJ Pad Pages

This folder contains local working pad pages, focused reference pages, and copied built-in VirtualDJ pad pages.

Use root-level `Reference - *.xml` files when copying a pattern into documentation. Built-in pages live under [Built-In/](Built-In/) as provenance examples. Personal/local working pages live under [Quarantine/](Quarantine/) — real examples, but not official or curated. Documentation test harnesses live outside this folder in [tests/Pads/](../../tests/Pads/).

Format reference: [Pad Page XML](../../docs/Pad%20Page%20XML.md) — container schema for `<page>`, `<padN>`/`<shift_padN>`, `<param1>`/`<param2>`, `<menu>`, and `<custompadsmode>`.

## Status Labels

| Status | Meaning |
| --- | --- |
| Canonical | Preferred copyable reference pattern for docs and new examples. |
| Built-in | Copied as-is from VirtualDJ's application bundle; treat as semi-official executable examples, not curated copy/paste patterns. |
| Quarantined | Personal/local working or superseded page (formerly `Working`/`Legacy`); real usage evidence, not official or curated — see [Quarantine/](Quarantine/). |

## Reference Pages

For local pad XML files, VirtualDJ's pad-page selector generally shows the filename stem. The XML `<page name="">` remains useful for `pad_page` targets, internal metadata, and source documentation.

| File | XML `<page name="">` | Status | Notes |
| --- | --- | --- | --- |
| [Reference - Slot FX.xml](Reference%20-%20Slot%20FX.xml) | `REF: SLOT FX` | Canonical | Slot-based audio FX selection, sliders, and state. |
| [Reference - ColorFX.xml](Reference%20-%20ColorFX.xml) | `REF: COLOR FX` | Canonical | Main filter ColorFX plus extra custom ColorFX slots. Queries use `filter_label 'name'` for selected-state checks. |
| [SAMPLER READ ONLY.xml](SAMPLER%20READ%20ONLY.xml) | `SAMPLER READ ONLY` | Canonical | Confirmed read-only multi-page sampler with absolute empty-slot guards. |

## Quarantine/

Personal/local pad pages — real working examples from this repo's own VirtualDJ install, but not official/vendor content and not the first reference source. `tools/lint_pads.py` scans `examples/Pads/*.xml` non-recursively (matching how it already excludes `Built-In/`), so these are **not** linted as part of the canonical pad-page count.

| File | XML `<page name="">` | Former status | Notes |
| --- | --- | --- | --- |
| [Reference - Page Aware Sampler.xml](Quarantine/Reference%20-%20Page%20Aware%20Sampler.xml) | `REF: SAMPLER` | Legacy | Older page-aware sampler example; retained for comparison with the current read-only pattern. |
| [COLOR FX.xml](Quarantine/COLOR%20FX.xml) | `COLOR FX` | Working | ColorFX selector with stems context and read-only selected-state queries. |
| [PUSH FX.xml](Quarantine/PUSH%20FX.xml) | `PUSH FX` | Working | Momentary `padfx` performance page with stem-targeted variants. |
| [SAMPLER.xml](Quarantine/SAMPLER.xml) | `SAMPLER` | Working | Sixteen-pad page-aware sampler with explicit drop-slot mapping; still uses `sampler_loaded <n> 'auto'` for labels/actions, so retest before promoting. |
| [SAMPLER SIMPLE.xml](Quarantine/SAMPLER%20SIMPLE.xml) | `SAMPLER SIMPLE` | Working | Fixed-slot sampler page demonstrating `drop="sampler_assign <slot>"`. |
| [32 Samples.xml](Quarantine/32%20Samples.xml) | `Sampler 32` | Legacy | Internal `sam_page` variable pager predating the confirmed sampler-page findings. |
| [AUTO CUES.xml](Quarantine/AUTO%20CUES.xml) | `AUTO CUES` | Working | Remix cue page with cue-name-driven labels and colors. |
| [CUE.xml](Quarantine/CUE.xml) | `CUE` | Working | Hotcue page using `cue_display`, `has_cue`, and cue-color feedback. |
| [CUE 16.xml](Quarantine/CUE%2016.xml) | `CUE 16` | Working | Sixteen-pad hotcue page using `cue_display` and `cue_color`. |
| [CUE SCAN.xml](Quarantine/CUE%20SCAN.xml) | `CUE SCAN` | Working | Cue-name scanner for sections such as intro, build, cut, and drop. |
| [CUE-EDIT.xml](Quarantine/CUE-EDIT.xml) | `CUE-EDIT` | Working | Compact cue edit helpers. |
| [FX-SLOTS.xml](Quarantine/FX-SLOTS.xml) | `FX-SLOTS` | Working | Only known source for `right_click=""` pad attribute; see `docs/Pad Page XML.md`. |
| [Phrase Jump.xml](Quarantine/Phrase%20Jump.xml) | `PHRASE JUMP` | Working | Phrase-sized beat jump controls. |
| [PLAY 16.xml](Quarantine/PLAY%2016.xml) | `PLAY 16` | Working | Sixteen-pad performance transport and stems page. |
| [TRANSPORT.xml](Quarantine/TRANSPORT.xml) | `TRANSPORT` | Working | Beat/bar navigation and transport utility page. |

## Built-In Pad Pages

[Built-In/](Built-In/) contains 17 `pads_*.xml` files copied from `/Applications/VirtualDJ.app/Contents/Resources/` on VirtualDJ `8.5.9307` / bundle `18.0.9336`.

Use these as `Built-in pad page` evidence when a shipped page demonstrates a VDJScript idiom, helper verb, pad color/query pattern, or XML surface. They are intentionally kept separate from root-level working/reference pages so Atomix-shipped examples do not get mistaken for curated local recommendations.

## Maintenance Checklist

- Run `python3 tools/lint_pads.py` after editing pad XML.
- Keep each `<page name="...">` unique so VirtualDJ and `pad_page "..."` links are unambiguous.
- Keep literal `pad_page "..."` targets pointed at page names that exist in this folder.
- Keep `query=""` attributes read-only where possible. For ColorFX selected-state checks, prefer `filter_label 'name'` instead of selector actions such as `filter_selectcolorfx`.
- Promote a page to `Canonical` only after it has matching reference notes and either official/source-backed rationale or local VirtualDJ verification.
- Do not hand-edit files in [Built-In/](Built-In/); refresh them from the app bundle and review diffs when VirtualDJ is updated.
- Keep test harnesses in [tests/Pads/](../../tests/Pads/) unless the page is meant to remain installed as a normal working/reference pad page.
- New personal/local working pages go straight into [Quarantine/](Quarantine/), not the root — only promote to root `Canonical` status with source-backed rationale or local verification.
