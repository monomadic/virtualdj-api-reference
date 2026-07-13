# VirtualDJ Pad Pages

This folder contains local working pad pages, focused reference pages, and copied built-in VirtualDJ pad pages.

Use root-level `Reference - *.xml` files when copying a pattern into documentation. Built-in pages live under [Built-In/](Built-In/) as provenance examples. Documentation test harnesses live outside this folder in [tests/Pads/](../../tests/Pads/).

Format reference: [Pad Page XML](../../Reference/Pad%20Page%20XML.md) — container schema for `<page>`, `<padN>`/`<shift_padN>`, `<param1>`/`<param2>`, `<menu>`, and `<custompadsmode>`.

## Status Labels

| Status | Meaning |
| --- | --- |
| Canonical | Preferred copyable reference pattern for docs and new examples. |
| Working | Installed/local page with useful behavior, but not the first reference source. |
| Built-in | Copied as-is from VirtualDJ's application bundle; treat as semi-official executable examples, not curated copy/paste patterns. |
| Legacy | Kept for comparison or migration; do not copy into new examples without retesting. |

## Reference And Working Pages

For local pad XML files, VirtualDJ's pad-page selector generally shows the filename stem. The XML `<page name="">` remains useful for `pad_page` targets, internal metadata, and source documentation.

| File | XML `<page name="">` | Status | Notes |
| --- | --- | --- | --- |
| [Reference - Slot FX.xml](Reference%20-%20Slot%20FX.xml) | `REF: SLOT FX` | Canonical | Slot-based audio FX selection, sliders, and state. |
| [Reference - ColorFX.xml](Reference%20-%20ColorFX.xml) | `REF: COLOR FX` | Canonical | Main filter ColorFX plus extra custom ColorFX slots. Queries use `filter_label 'name'` for selected-state checks. |
| [SAMPLER READ ONLY.xml](SAMPLER%20READ%20ONLY.xml) | `SAMPLER READ ONLY` | Canonical | Confirmed read-only multi-page sampler with absolute empty-slot guards. |
| [Reference - Page Aware Sampler.xml](Reference%20-%20Page%20Aware%20Sampler.xml) | `REF: SAMPLER` | Legacy | Older page-aware sampler example; retained for comparison with the current read-only pattern. |
| [COLOR FX.xml](COLOR%20FX.xml) | `COLOR FX` | Working | ColorFX selector with stems context and read-only selected-state queries. |
| [PUSH FX.xml](PUSH%20FX.xml) | `PUSH FX` | Working | Momentary `padfx` performance page with stem-targeted variants. |
| [SAMPLER.xml](SAMPLER.xml) | `SAMPLER` | Working | Sixteen-pad page-aware sampler with explicit drop-slot mapping; still uses `sampler_loaded <n> 'auto'` for labels/actions, so retest before promoting. |
| [SAMPLER SIMPLE.xml](SAMPLER%20SIMPLE.xml) | `SAMPLER SIMPLE` | Working | Fixed-slot sampler page demonstrating `drop="sampler_assign <slot>"`. |
| [32 Samples.xml](32%20Samples.xml) | `Sampler 32` | Legacy | Internal `sam_page` variable pager predating the confirmed sampler-page findings. |
| [AUTO CUES.xml](AUTO%20CUES.xml) | `AUTO CUES` | Working | Remix cue page with cue-name-driven labels and colors. |
| [CUE.xml](CUE.xml) | `CUE` | Working | Hotcue page using `cue_display`, `has_cue`, and cue-color feedback. |
| [CUE 16.xml](CUE%2016.xml) | `CUE 16` | Working | Sixteen-pad hotcue page using `cue_display` and `cue_color`. |
| [CUE SCAN.xml](CUE%20SCAN.xml) | `CUE SCAN` | Working | Cue-name scanner for sections such as intro, build, cut, and drop. |
| [CUE-EDIT.xml](CUE-EDIT.xml) | `CUE-EDIT` | Working | Compact cue edit helpers. |
| [Phrase Jump.xml](Phrase%20Jump.xml) | `PHRASE JUMP` | Working | Phrase-sized beat jump controls. |
| [PLAY 16.xml](PLAY%2016.xml) | `PLAY 16` | Working | Sixteen-pad performance transport and stems page. |
| [TRANSPORT.xml](TRANSPORT.xml) | `TRANSPORT` | Working | Beat/bar navigation and transport utility page. |

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
