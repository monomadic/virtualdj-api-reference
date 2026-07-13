# VirtualDJ Example Pad XML Pages

Sampler-focused pad page examples for files stored in `Documents/VirtualDJ/Pads`.

These examples were checked against the current VirtualDJ manual, recent forum guidance, and local sampler-page tests.

## Read-Only Multi-Page Sampler

Use [SAMPLER READ ONLY.xml](../xml/Pads/SAMPLER%20READ%20ONLY.xml) when a pad page should only play existing samples and must never record into empty slots. This is the current safest pattern for banks with more than eight samples.

The important discovery is that `sampler_pad_page` evaluates as text ranges such as `"1 to 8"` and `"9 to 16"` in the tested pad/skin contexts. `sampler_loaded` should still be treated as an absolute-slot query, so each page branch checks the real slot behind the visible pad.

```xml
<!-- Pad 8: page "1 to 8" checks slot 8; page "9 to 16" checks slot 16. -->
<pad8 name="`sampler_pad_page &amp; param_equal &quot;1 to 8&quot; ? sampler_loaded 8 ? sampler_pad 8 : get_text ' ' : sampler_pad_page &amp; param_equal &quot;9 to 16&quot; ? sampler_loaded 16 ? sampler_pad 8 : get_text ' ' : get_text ' '`"
      color="sampler_pad_page &amp; param_equal &quot;1 to 8&quot; ? sampler_loaded 8 ? sampler_color 8 : dim : sampler_pad_page &amp; param_equal &quot;9 to 16&quot; ? sampler_loaded 16 ? sampler_color 8 : dim : dim"
      query="sampler_pad_page &amp; param_equal &quot;1 to 8&quot; ? sampler_loaded 8 ? sampler_play 8 'auto' ? blink 1bt : on : off : sampler_pad_page &amp; param_equal &quot;9 to 16&quot; ? sampler_loaded 16 ? sampler_play 8 'auto' ? blink 1bt : on : off : off">
  sampler_pad_page &amp; param_equal &quot;1 to 8&quot; ? sampler_loaded 8 ? sampler_pad 8 : nothing : sampler_pad_page &amp; param_equal &quot;9 to 16&quot; ? sampler_loaded 16 ? sampler_pad 8 : nothing : nothing
</pad8>
```

For 16-pad layouts, pads `9-16` address the next eight visible sampler positions. On sampler page `"9 to 16"`, `pad16` is therefore backed by absolute slot `24`, not slot `16`.

### What This Example Does

- Loaded pads trigger through `sampler_pad`, so the sample's own trigger mode still applies.
- Empty pads resolve to `nothing`, with no `sampler_rec`, `sampler_assign`, `drop=`, or shift edit action.
- Empty labels return `get_text ' '` instead of an empty string. In local testing, an empty string could make VirtualDJ fall back to displaying slot numbers on later pages.
- Empty-slot checks use absolute slot numbers for the visible page. Do not rely on `sampler_loaded <n> 'auto'` for this guard.
- `param1` cycles banks and `param2` cycles sampler sub-pages.

### Drag-and-Drop Assignment

The stock sampler workflow also supports dropping a file onto a sampler pad to assign it to a slot. The working custom pad-page pattern is:

```xml
<pad1 drop="sampler_assign 1">...</pad1>
```

Keep these limits in mind:

- Treat `sampler_assign` slot numbers as absolute-slot targets.
- The current official docs show `sampler_assign` with explicit slot numbers and do not document a page-aware `"auto"` form.
- `sampler_pad_page` is the official pager for the visible `1-8`, `9-16`, `17-24`, and later windows, but you should not assume `drop="sampler_assign 1"` follows that pager automatically.
- If you want page-aware drag targets, map each visible pad to the correct absolute slot yourself, or verify build-specific behavior before relying on it.
- The current stock/local sampler page in this repo uses this exact pattern in [SAMPLER SIMPLE.xml](../xml/Pads/SAMPLER%20SIMPLE.xml).
- The target bank must be unlocked for samples to be added by drag-and-drop.

## Sampler Utility Page

This is a compact companion page for common sampler tasks: lock/unlock the bank, switch StemSwap on/off, change routing, change trigger mode, and trim sampler master/PFL levels.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<page name="SAMPLER UTILITY">
  <pad1 name="Lock / Unlock">sampler_options "locked"</pad1>
  <pad2 name="StemSwap">sampler_options "stemswap"</pad2>
  <pad3 name="Output">sampler_output "popup"</pad3>
  <pad4 name="Trigger Mode">sampler_mode +1</pad4>
  <pad5 name="Main +5%">sampler_volume_master +5%</pad5>
  <pad6 name="Main -5%">sampler_volume_master -5%</pad6>
  <pad7 name="HP +5%">sampler_pfl +5%</pad7>
  <pad8 name="HP -5%">sampler_pfl -5%</pad8>
</page>
```

## Useful Variations

- Always sync sampler pads to the active deck:

```text
deck active sampler_pad 1 "auto"
```

- Always sync sampler pads to the master deck:

```text
deck master sampler_pad 1 "auto"
```

- `deck master` means the current master deck, not a separate global sampler scope. If a custom skin or pad title/query path behaves differently from an explicit deck number, resolve the master deck explicitly:

```text
deck 1 masterdeck ? deck 1 sampler_pad 1 : deck 2 masterdeck ? deck 2 sampler_pad 1 : deck 3 masterdeck ? deck 3 sampler_pad 1 : deck 4 masterdeck ? deck 4 sampler_pad 1 : sampler_pad 1
```

- Page the sampler bank forward or backward from a controller or custom button:

```text
sampler_pad_page +1
sampler_pad_page -1
```

- Use the currently visible sampler pad volume instead of an absolute slot:

```text
sampler_pad_volume 1 75%
```

- Address a fixed absolute slot, regardless of the visible sampler page:

```text
sampler_volume 9 75%
get_sample_name 9
get_sample_color 9
```

- Use `sampler_pad <n>` to show the currently visible sample name in a page-aware label:

```text
sampler_pad 1
```

- Add stock stop/delete shift behavior to a sampler pad:

```xml
<shift_pad1>sampler_pad_shift 1</shift_pad1>
```

- If you need an explicit custom matrix instead of Automatic layout, staff guidance shows patterns such as:

```text
sampler_pad 1 "4x4x1"
```

## Practical Notes

- If you want deck 1 to expose `1-8` and deck 2 to expose `9-16` automatically, enable `samplerSpanAcrossDecks`.
- If you want both decks to start on `1-8`, leave `samplerSpanAcrossDecks` off and page manually with `sampler_pad_page`.
- In tested pad/skin contexts, compare `sampler_pad_page` to text ranges such as `"1 to 8"` and `"9 to 16"`, not numeric page indexes.
- `sampler_pad`, `sampler_color`, and `sampler_pad_volume` are the safest page-aware helpers.
- `sampler_loaded` should be treated as an absolute-slot query for empty-slot checks; page 2 pad 8 needs `sampler_loaded 16`.
- In 16-pad pad pages, pads `9-16` are the next eight visible sampler positions; on page `"9 to 16"`, pad 16 should be guarded by `sampler_loaded 24`.
- Use `get_text ' '` for intentionally blank sampler pad labels; an empty-string branch can fall back to visible slot numbers.
- Use pad `drop="sampler_assign <slot>"` when you want a custom sampler pad page to accept dragged files.
- Treat `drop="sampler_assign <slot>"` as an absolute-slot mapping unless you have verified a different build-specific behavior.
- In pad `name=` fields, `sampler_pad <n>` is the safest way to show the current visible sample name on the active page.
- In recent testing, `sampler_pad <n>` has been most reliable for paged names when the deck context is explicit. If `deck master` behaves oddly, prefer an explicit deck number or an explicit `masterdeck` resolver.
- `sampler_play`, `sampler_stop`, `sampler_volume`, `get_sample_name`, and `get_sample_color` are best treated as absolute-slot helpers.

## Source Notes

- Official pads behavior: [Pads manual](https://www.virtualdj.com/manuals/virtualdj/interface/decks/decksadvanced/pads.html)
- Official sampler drag-and-drop and unlocked-bank behavior: [Sampler manual](https://www.virtualdj.com/manuals/virtualdj/interface/browser/sideview/sampler.html)
- Official sampler verbs: [VDJScript verbs](https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html)
- Official sampler options: [Options list](https://www.virtualdj.com/manuals/virtualdj/appendix/optionslist.html)
- Trigger modes and loop sync details: [Sample Editor](https://www.virtualdj.com/manuals/virtualdj/editors/sampleeditor.html)
- Page-aware custom page examples: [Custom Sampler Pad Page](https://www.virtualdj.com/forums/253061/General_Discussion/Custom_Sampler_Pad_Page_%28Recording__Looping__Adjust_Beatgrid_and_more%29.html)
- Deck sync guidance: [problem with (pad pages) pads sampler sync](https://virtualdj.com/forums/224203/VirtualDJ_Technical_Support/problem_with_%28pad_pages%29_pads_sampler_sync%21_please_help___is_it_a_bug%3F%3F.html)
- Master-deck sampler quirks in newer builds: [Virtual Dj 2025 Sampler Sync](https://virtualdj.com/forums/265522/VirtualDJ_Technical_Support/Virtual_Dj_2025_Sampler_Sync.html)
- Paging and `9-16` workflow: [No longer possible to access 16 samples from controllers with 8 x 2 pads?](https://virtualdj.com/forums/261416/VirtualDJ_Technical_Support/No_longer_possible_to_access_16_samples_from_controllers_with_8_x_2_pads_.html)
- Matrix/layout hint: [Using Xone K2 to control the sampler](https://www.virtualdj.com/forums/261102/VirtualDJ_Technical_Support/Using_Xone_K2_to_control_the_sampler.html)
- Local read-only multi-page sampler test: [VDJScript Local Test Tracker](VDJScript%20Local%20Test%20Tracker.md#sampler)
