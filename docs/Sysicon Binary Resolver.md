# Sysicon binary resolver

- **Tier 2, binary analysis:** VirtualDJ **18.0.9598, arm64**, inspected
  2026-09-15. The inspected XML path calls a compiled comparison chain, not a
  serialized key-to-icon table. The chain assigns pointers into a shared icon
  object array.
- It contains additional mappings for `folder`, `playlist`, `plus`, `minus`,
  `browser_shortcut`, `load_next`, and `search_folder`.
- The initial binary pass did not test rendering. **Follow-up local test,
  2026-09-15, build 18.0.9598 arm64:** `folder`, `playlist`, `plus`, `minus`,
  `browser_shortcut`, `search_folder`, and `load_next` rendered matching atlas
  glyphs in normal, selected, hover and selected-hover states. See the
  [named fixture and screenshots](../tests/Skins/SysiconAtlasProbe/README.md).
  Other spellings and general matcher rules below remain Tier 2.

## Reproduce and query

Run `just doctor` first. Generation requires numpy and capstone; lookup requires
only Python's standard library:

```sh
python3 tools/extract_sysicon_resolver.py --extract --output tests/sysicon-resolver-9598
python3 tools/extract_sysicon_resolver.py --get folder
python3 tools/extract_sysicon_resolver.py --get 'font_size 0'
```

Use a different output directory for a new build; preserve this capture.
The [manifest](../tests/sysicon-resolver-9598/manifest.json) records the build,
whole universal-binary SHA-256, architecture, literal call sites and capture
hashes. The extractor locates the function using intersecting string-reference
owners and verifies an incoming call from the XML `sysicon` reader. It does not
rely on this build's hard-coded addresses. Offline lookup reports literals by
argument role; it does not pretend every literal is a usable key.

## What the binary actually contains

The [XML reader](../tests/sysicon-resolver-9598/xml-reader-0.asm) at
`0x1004ce7d0` reads the `sysicon` attribute and passes its string data and length
to `0x1004cf99c` at call site `0x1004ce980`.

The [resolver](../tests/sysicon-resolver-9598/resolver.asm) gates comparisons by
length and makes byte-comparison calls to `0x10370677c`. Equal results branch
to assignments using the array base loaded from object offset `+0x1d8`.
The primary icon pointer is written at `+0x2a8`; other writes configure state
graphics and flags. This is actual consuming code, stronger evidence than a
cluster of strings, but still Tier 2 under the project's evidence standards.

The offsets align with a **0xa0-byte object stride** and a sixteen-column atlas:
`search` uses `0x2a80` (index 68, E5), `headphones` uses `0x2b20` (69, E6),
`settings` uses `0x2f80` (76, E13), and `sampler_drop` uses `0x5000` (128, I1).
Grid labels below are the structural correspondence obtained by dividing the
offset by `0xa0` and matching these documented anchors. This pass did not trace
the array constructor or inspect rendered pixels, so it does not establish
the object's complete layout or a visual result.

## Additional mappings compared with the official page

The [official atlas page](https://virtualdj.com/wiki/skindefaulticons.html),
read 2026-09-15, leaves the corresponding folder, playlist, expand/collapse and
shortcut entries without names. The following branches exist in this build:

| Compared key | Icon array offset | Grid correspondence | Equal-result destination |
| --- | --- | --- | --- |
| `folder` | `0x1400` | C1, files folder | `0x1004d089c` |
| `playlist` | `0x1720` | C6, playlist folder | `0x1004d0808` |
| `plus` | `0x2800` | E1, expand | `0x1004d0810` |
| `minus` | `0x28a0` | E2, collapse | `0x1004d0800` |
| `browser_shortcut` | `0x2ee0` | E12, add shortcut | `0x1004d0034` |
| `search_folder` | `0x2a80` | E5, same object as `search` | `0x1004d0818` |
| `load_next` | `0x4d80` | H13, sampler on/off graphic | `0x1004d00f4` |

`load_next` is especially worth a visual check: its literal comparison really
does select that offset; an intuitive name-to-picture guess would miss it.
`browser_shortcut` additionally sets a state graphic at `+0x270`, so sharing an
atlas slot does not imply identical complete button behavior.

Additional spellings absent from that page's key column:

| Compared form | Static branch result |
| --- | --- |
| `deck master sampler_bank -1` | `0x3020`, same primary object as `arrowleft` |
| `deck master sampler_bank +1` | `0x30c0`, same primary object as `arrowright` |
| `font_size 'big'` | `0x4380`, same primary object as `font_size +` |
| `sideview 'automix' 'blink'` | `0x4600`, same primary object as the ordinary automix sideview form |
| `sideview 'karaoke' 'blink'` | `0x47e0`, same primary object as the ordinary karaoke sideview form |
| `sampler_options` prefix | Same state-graphic branch as `context_menu` |

This comparison concerns the linked page, not a claim that these strings have
never been documented anywhere else.

## Why the pasted string list is misleading

- `dx`, `dy`, `width`, `height`, `downx`, `downy`, `clipmask`, `mask`, the
  state names, and click/text attributes belong to the XML reader. Their
  proximity to the resolver's literals does not make them icon keys.
- `font_size 0` is passed in **x0 to an action-construction call** at
  `0x1004d03cc`, after a font-size icon has already been selected. It is not
  an input comparison. The code installs it at `+0x230` when that field is
  empty; this pass does not assign a user-facing click meaning to that field.
- `_options` and ` 'popup'` are **suffix predicates**, not two more exact
  icon names. The captured [helper](../tests/sysicon-resolver-9598/predicate-0-tail.asm)
  compares the end of the supplied string. A match selects the context-menu
  state graphics (`0x3480` and `0x3520`).
- `sampler_options`, `browser_shortcut`, `font_size -`, `font_size +`,
  `sideview "` and `sampler_bank '` have prefix comparisons on their paths.
  The unfinished quotes are deliberate matcher prefixes, not complete scripts
  to execute. Other listed forms have exact length gates; do not assume the
  resolver parses arbitrary equivalent VDJScript expressions.
- Bare `sampler_bank` and `deck master sampler_bank` take an early return in
  this resolver. Their presence alone does not establish an H11 assignment.
  The quoted-bank prefix does assign `0x4c40` (H11 correspondence).
- `sampler_mode`, `play_button`, `stop_button`, and `maximize` have special
  state-dependent branches. They cannot be described adequately as one fixed
  atlas coordinate each.

## Bounds and next test

The official page also names `stems_vocal`, `stems_instru`, `stems_bass`,
`stems_kick`, and `stems_hihat`. They are not comparison literals in this
captured resolver. That is a discrepancy to investigate, not a universal
claim that those names cannot work through another path or in another build.

There is no arbitrary numeric atlas-index fallback in the captured resolver:
an unmatched string eventually returns after the default state-graphic setup.
This does not rule out coordinate-based icon elements or a separate consumer.

The planned discriminating test was a named skin fixture comparing the additional
keys with crops from the same build's atlas, alongside a known key and a junk
key, at normal/hover/selected states. Record the installed build and screenshots
and restore the original skin afterward. That test is now recorded in
[SysiconAtlasProbe](../tests/Skins/SysiconAtlasProbe/README.md): the named keys
rendered, the original skin was restored, and `font_size 0`, a junk key and
`stems_vocal` were blank. This promotion applies only to the exact tested keys
and states, not to all binary-derived matcher rules or all stems spellings.

**Interpretation correction (2026-09-15):** the blank observations do not prove
key rejection. The fixture lacked an explicit `customicons` declaration, but
the effective runtime atlas and selected cell were not independently verified.
A transparent/replaced cell or another drawing issue remains unresolved. A
diagnostic atlas whose replacement is verified with known keys is needed before
using blank output to reason about recognition.

**Controlled atlas follow-up (2026-09-15, 18.0.9598 arm64):**
[SysiconMarkerProbe](../tests/Skins/SysiconMarkerProbe/README.md) supplied fully
opaque numbered grids through both `customicons file="markers.png"` and
`customicons x="0" y="800"` in the main skin image. Known keys displayed the
expected numbers and changed route letters, independently verifying override
use for those controls. The five tested `stems_*` keys stayed blank in normal
and selected states. Transparent supplied cells no longer explain that result;
the loader's handling of higher indices and the stems keys' runtime pointers
were not independently observed. No universal key-rejection claim is made.

For future agents, query the manifest before loading assembly. The original
adjacent-string list mixes attributes, suffixes, prefixes, action construction,
and actual comparisons; repeating that discovery is unnecessary context cost.
