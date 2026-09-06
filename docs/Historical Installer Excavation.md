# Historical Installer Excavation

Extraction date: 2026-09-06. Sources: the user's four original macOS installers,
unpacked with `pkgutil --expand-full`, without installation or execution.
Evidence: **binary structures and named disassembly**. No runtime behavior was
established and no verb-store test status was changed.

## Most useful new lead: clickthrough has a boolean path

The previous Skin SDK statement that every non-`pass` value behaves like an absent
attribute exceeded its live evidence, which tested only a nonsense value.

In `ISkinObject::load(CXMLNode*, CImage*)`, the historical binaries:

1. Check whether `clickthrough` is present.
2. Compare it with `pass`; that branch stores signed integer `-2`.
3. Otherwise call a boolean XML accessor with a false default and store its result
   in the same field.

| Build (x86_64) | Branch range, inclusive instruction addresses | Boolean accessor |
| --- | --- | --- |
| 9.0.5308 | `0x1001c73eb`–`0x1001c743b` | `CXMLNode::getBoolParamNS` |
| 9.0.7607 | `0x1002e9211`–`0x1002e926c` | `CXMLNode::getBoolParam` |
| 18.0.9246 | `0x100381a58`–`0x100381ab3` | `CXMLNode::getBoolParam` |

The named accessor call is the additional evidence that the earlier literal-only
scan missed. It does **not** establish what the stored boolean does to event
delivery. The current build's demonstrated additive `pass` behavior remains
valid; the universal negative has been corrected in
[Skin SDK](Skin%20SDK.md#clickthrough).

### The accepted spellings are readable (2026-09-07)

The boolean accessor itself is short enough to read in full, and it is the same
in all three named builds (`*-bool-param.asm`; 5308 is the `getBoolParamNS`
variant that its `ISkinObject::load` calls). It looks the attribute up by
case-insensitive name and returns the caller's default when it is absent. Then
it compares the value, by exact length and case-insensitively, against four
literals and nothing else:

| Value | Result |
| --- | --- |
| `yes`, `true` | true |
| `no`, `false` | false |
| any other value | the caller's default |

| Build (x86_64) | Symbol | Range |
| --- | --- | --- |
| 9.0.5308 | `CXMLNode::getBoolParamNS(char const*, int, bool)` | `0x10022aaf6`–`0x10022ac54` |
| 9.0.7607 | `CXMLNode::getBoolParam(string_view, bool)` | `0x10037625a`–`0x1003763ec` |
| 18.0.9246 | `CXMLNode::getBoolParam(string_view, bool)` | `0x10044fbee`–`0x10044fd58` |

Since `ISkinObject::load` passes a false default, the field can hold only three
values: `-2` for `pass`, `1` for `yes`/`true`, and `0` for everything else,
including `no`, `false`, `1`, `0`, `on`, `off`, nonsense, and the attribute
being absent. The 2026-09-05 live run already observed `-2` (`pass`) and `0`
(`value-control`). The only stored state never observed is `1`.

**Settled live (2026-09-07, build 18.0.9598).** The fixture gained
`clickthrough="yes"` and `clickthrough="TRUE"` variants beside the existing
baseline, `pass`, and control skins; two runs, forward then reversed, both
counters read over HTTP after each click. Boolean true is a third behavior: the
element stays drawn but its own action does not fire and the click reaches the
element underneath (`top=0 bottom=1`), where `pass` fires both (`1`/`1`) and the
stored `0` swallows the click (`1`/`0`). `TRUE` agreed with `yes`, confirming
the case-insensitive compare on the current build. The historical parser was
the lead; the counters are the result. Recorded in
[Skin SDK](Skin%20SDK.md#clickthrough) and the tracker.

Evidence: `*-object-load.asm` and `*-bool-param.asm` in the
[capture directory](../tests/build-history-2026-09-06/).

## Plain groups have a separate construction path

`CSkinPanel::loadChildren` in all three named builds compares a child tag with
`group`, then tests the **presence**, not the evaluated value, of `visibility`
and `novisibility`. If either attribute exists, it takes the ordinary
`ISkinObject::createSkinObject` path. Otherwise it calls `checkCondition`, reads
coordinate offsets, recursively processes the children, and restores offsets.

On build 18.0.9246 (x86_64), the discrimination is at
`0x100810f4e`–`0x100810f9c`; the alternate branch begins at `0x10081104a` and
recurses at `0x100811103`. The older named routines contain the same branch
shape. This resolves the earlier investigation's missing group-constructor clue:
there is a path that processes a group without constructing that group through
the ordinary object factory.

**Boundary:** this is control-flow evidence for these binaries, not a demonstrated
current UI contract or a claim that every group avoids allocation. It motivates
checking whether generic object attributes are honored on a plain group.

**Settled live (2026-09-07, build 18.0.9598).** The clickthrough fixture wrapped
its top button in a `<panel>`, a plain `<group>`, and a `<group>` with a
constant-true `visibility`, each with no attribute, `clickthrough="pass"` and
`clickthrough="yes"`; two reversed-order runs agreed on every row. The panel and
the visibility-bearing group honored both values exactly as a button does. The
plain group honored neither: the wrapped button behaved as if unwrapped. All
three no-attribute wrappers rendered and delivered the click, so the difference
is attribute handling, not placement. That is the runtime counterpart of the
branch above — attributes from the shared skin-object reader are not read on
the plain-group path. A constant-false `novisibility` variant was not run.
Recorded in [Skin SDK](Skin%20SDK.md#group). The same run established that
`pass` moves a click exactly one layer down.

Evidence: `*-panel-children.asm` in the capture directory. This is separate from
the panel constructor; function boundaries come from the next distinct text-symbol
address, because `otool -p` can print subsequent functions without labels.

## A sampled compatibility history, not release-introduction dates

The same sorted name/id/flags structure is readable in every installer. Exact
stamps from each extraction's summary, printed with `stamp()`:

- 847 records / 785 distinct verbs / 50 alias groups / 17 editor-hidden on build 9.0.5308 (x86_64, extracted 2026-09-06).
- 955 records / 888 distinct verbs / 55 alias groups / 34 editor-hidden on build 9.0.7607 (x86_64, extracted 2026-09-06).
- 1025 records / 952 distinct verbs / 61 alias groups / 37 editor-hidden on build 18.0.9246 (x86_64, extracted 2026-09-06).
- 1032 records / 958 distinct verbs / 62 alias groups / 38 editor-hidden on build 18.0.9583 (x86_64, extracted 2026-09-06).

No name disappears between adjacent samples. That establishes name retention in
the extracted tables, not behavioral compatibility. Shared numeric ids identify
aliases **within** a build; ids move across builds and must not be used as stable
cross-version identities.

| Earlier primary spelling | Later alias peer / primary spelling | Observed transition interval |
| --- | --- | --- |
| `get_constant` | `constant` | 9.0.5308 → 9.0.7607 |
| `pad_page_favorite_select` | `pad_page_select` | 9.0.5308 → 9.0.7607 |
| `add_virtualfolder` | `add_list` | 9.0.7607 → 18.0.9246 |
| `virtualfolder_add` | `add_to_list` | 9.0.7607 → 18.0.9246 |
| `create_virtualfolder_from_playlist` | `create_list_from_playlist` | 9.0.7607 → 18.0.9246 |
| `goto_bar` | `goto_beat_in_bar` | 18.0.9246 → 18.0.9583 |

These are observed flag changes from primary to secondary spelling with shared
ids in the later table. They are not guesses based on similar names. Exact name
additions, hidden-flag changes, and alias peers are in `summary.json` →
`transitions`. For example, `beatjump` is absent from 9.0.5308 and present in
9.0.7607; this brackets table appearance, not the precise release that added it.

## What the old installers add as instruments

Build 9.0.5308 is x86_64-only. Builds 9.0.7607, 18.0.9246 and 18.0.9583 are
universal. For each universal sample, independently extracted arm64 and x86_64
name/id/flags maps agree exactly (`arm64_name_id_flags_equal` in the summary).
The named skin routines are available in the first three samples; they are not
available as named symbols in 18.0.9583.

The `forceshow` comparison chain in 9.0.5308 contains `1fx`, `3fx`, `8pads`,
`16pads`, and `timecode`; 9.0.7607 and 18.0.9246 additionally compare `6fx`.
Likewise, the `clickthrough` special/boolean split already exists in 9.0.5308.
These are historical implementation observations, not newly proven UI behavior.

An extraction bug surfaced: a thin x86_64 binary could be read while the summary
claimed arm64. `extract_verb_table.py` now accepts `--arch x86_64`, propagates that
identity, and rejects a thin binary whose architecture does not match the request.
The older x86_64 category-index mappings remain unresolved by this extractor;
category-name recovery alone is not a mapping. No categories were guessed or
copied from the current build into those records.

## Remaining research value

Assessment recorded 2026-09-06. These are proposed investigations, not findings
about runtime behavior or new test-status claims. The active operational queue
remains [TODO.md](../TODO.md); this assessment does not change its ordering.

The strongest remaining use of the older installers is to follow named calls and
recover decision rules that the stripped builds make harder to inspect. Prefer
build 18.0.9246 for a named implementation closer to the current app, and use
9.0.5308 and 9.0.7607 to distinguish longstanding structures from later changes.
Neither matching names nor similar code licenses transferring old behavior to a
new build without a current observation.

### Immediate follow-ups: event delivery and group construction

**Clickthrough event delivery.** Follow the field written by `ISkinObject::load`
into its consumers, including `ISkinObject::onMouseDown(int, int, int)` and the
container's event traversal. The `onMouseDown` method name is available on each named
sample; on build 18.0.9246 (x86_64), `ISkinObject::onMouseDown` starts at
`0x10015c2c4`. That is an entry point, not evidence that it alone implements
pass-through. Recover the decisions for the boolean values and the `-2` sentinel,
including whether they affect the object itself, traversal to siblings, or both.
Then run the overlapping-button controls described above on the current app.
A useful result would be an independently tested event-delivery matrix, with the
historical branch explanation kept separate from the current runtime contract.

**Group attribute handling.** Follow the alternate paths in `loadChildren` through
`ISkinObject::createSkinObject(CXMLNode*, CImage*, CSkinWindow*)`, whose named entry
on build 18.0.9246 (x86_64) is `0x100382ec0`. Identify which constructors and common
attribute readers each path actually reaches. Test plain groups, groups carrying
visibility attributes, and panels with identical children and independent action
counters, as described above. A useful result would explain which wrapper
attributes each construction path honors, without generalizing from one attribute
to all attributes. These two follow-ups have the highest expected value because
they extend specific captured branches and have bounded live validation fixtures.

### Larger opportunities

| Investigation | Available lead | Useful output and validation boundary |
| --- | --- | --- |
| Settings types, enums and conversion | Named `CSettingEnum` methods, including `unserialize`, `getActionParam` and `setActionParam`, survive in the named samples. On build 18.0.9246 (x86_64), `CSettingEnum::unserialize` starts at `0x10078a142`. | Recover typed candidate values and conversion rules by following registration and accessor code. Associate defaults with concrete keys only when the initializer establishes that association. Confirm accepted values and effects independently on a prepared instance; any persistent writes need round-trip restoration. A type name alone does not establish a key's schema. |
| Historical vendor descriptions and examples | **Done 2026-09-07** — see [What the older vendor text and skins still say](#what-the-older-vendor-text-and-skins-still-say). | `just vendor-history-diff` regenerates `vendor-text-diff.json`; `just verb <name>` shows a verb's share of it. |
| Runtime argument parsing | `IAction::create(char const*, char const**, int)` is named in the older samples; its entry on build 18.0.9246 (x86_64) is `0x100596f1c`. | Follow argument consumption, delimiter handling and fallback branches in the runtime path. Contrast with the separately documented editor parser. Each proposed rule needs a discriminating current runtime test; editor highlighting and parser acceptance cannot substitute for an observed result. |
| Configuration serialization | Named `CSettingCrossfaderCustom::serialize` and `unserialize` survive in the older samples; on build 18.0.9246 (x86_64) they start at `0x1002a6e56` and `0x1002a6b9e`, respectively. | Recover a narrowly scoped format description if configuration tooling needs it. Validate with app-produced samples and isolated round trips, preserving the original configuration. Serializer symbols alone do not establish delimiters, field meanings or compatibility. |

The entry addresses above were checked against the unpacked binaries' x86_64
symbol tables with `nm -arch x86_64 -m` followed by `c++filt`. Unlike the skin
routines already captured, these additional functions have not been disassembled
and interpreted in this pass. Resolve their names again before analysis rather
than reusing addresses on another build.

### Lower expected return

Another undirected verb-name inventory, symbol dump, or source-module census
would largely repeat the existing verb-table, action-vtable and action-module
work. Repeat those comparisons when they answer a concrete compatibility question
or expose a changed structure. Historical name retention is already captured;
precise feature-introduction dates cannot be recovered from these widely spaced
samples alone. The next useful excavation should end in a bounded mechanism,
a provenance-preserved vendor example, or a falsifiable runtime test.

## What the older vendor text and skins still say

Comparison date 2026-09-07, current app 18.0.9598 against the four samples,
produced by [tools/diff_vendor_history.py](../tools/diff_vendor_history.py)
(`just vendor-history-diff`) into
[vendor-text-diff.json](../tests/build-history-2026-09-06/vendor-text-diff.json).
Everything in it is vendor prose or vendor script, Tier 2: a lead about what a
verb or keyword means, never a claim that the current build accepts it. Sizes
are the artifact's own `summary` block; do not copy them into prose.

**Descriptions.** Every verb described in an older appendix but not the current
one is either a rename already stored as an alias (`goto_bar`,
`add_virtualfolder`, `get_constant`, …) or one of three unofficial verbs the
store carried without prose — `setting_if_unchanged`, `get_pad_page_name`,
`pad_page_favorite` — which now carry the 9.0.5308 appendix text through
`put-verb`, stamped with the build it came from. Of the descriptions that
changed, nearly all grew: the current text is the old text plus examples. The
exceptions worth knowing are parameter spellings that moved:
`get_saved_loop 'len'` → `'length'`, `browsed_file_analyze 'multi'` → `'fluid'`,
`show_splitpanel 'sidelist'` → `'sideview'`, `video_source 'shader'` →
`'visuals'`, `padfx 'smart_temporary'` → `'smart_pressed'`; one correction,
`get_totaltime_ms` now says 1/100th seconds where 9.0.5308 said milliseconds;
and one dropped equivalence, `get_totaltime_min` ≡ `get time_min "total"`.
Whether an old spelling is still accepted is a `probe_arg_forms.py` question
(task 10b), and `documented_parameters_lost` in the artifact is its worklist.

**Shipped skins.** `skin2018.zip` (2 Decks, 4 Decks, 6 Decks, Tablet, Welcome)
shipped in 9.0.5308 and 9.0.7607 and is gone from 18.0.9246 onward; the `skin.zip`
five persist with edits. `skin_usages_lost` lists every verb a historical
shipped skin used in a script attribute and no current shipped skin uses, with
archive, member and the exact attribute value: `clone_deck`, `loop_back`,
`loop_roll_mode`, `mixer_order 3124`, `pad_has_16pads`, `skin_pannel 'left_cues' on`,
`video_source_select`, `setting_if_unchanged skinWaveformType 1` and the rest.
These are the only vendor-written usages of those verbs the repo has. Read the
snippet, not only the name: a verb name inside a quoted argument
(`sampler_mode 'hold'`) matches too. The old archives themselves were not
copied into `examples/`; the artifact holds the attribute values, and the
installers hold the files.

**In the store view.** `just verb <name>` now ends with a History block: the
samples that carried the name, flag and same-id-peer changes by build, and the
verb's lines from this diff. The data is joined from `summary.json` →
`verb_history` and from `vendor-text-diff.json` at read time; nothing was
copied into store records except the three descriptions above.

## Reproduction and limits

After expanding each installer into `/tmp/vdj-history-20260906/BUILD`, run:

```sh
python3 tools/extract_build_history.py \
  --root /tmp/vdj-history-20260906 \
  --output tests/build-history-2026-09-06
just vendor-history-diff   # tools/diff_vendor_history.py, same root
```

The installers are `~/Downloads/install_virtualdj_2020_b5308_mac.pkg`,
`~/Downloads/VirtualDJ_2023_b7607_mac.pkg`,
`~/Downloads/install_virtualdj_2026_b9246_mac.pkg` and the 18.0.9583 package;
the expanded tree under `/tmp` is not kept. `summary.json` carries each
executable's SHA-256 so a re-expansion can be checked against this capture.

The capture includes bundle identities, executable SHA-256 digests, both-slice
comparison results, complete historical verb tables, and narrowly bounded named
skin-reader disassembly. Installer filenames are routing hints; `CFBundleVersion`
in each payload supplies the recorded identity. Payload dates and legacy display
versions are retained separately rather than treated as release dates.

The extraction does not recover source code or debug line information. `otool`'s
symbolic rendering can substitute unrelated absolute symbol names for numeric
immediates (for example `CONFIG_EMULATE_HARDWARE` for zero); those annotations are
not evidence that the routine accesses that setting. Only actual calls, branch
targets, literal references and checked operand flow support the observations above.
