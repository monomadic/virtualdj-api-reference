# Skin Runtime Findings

Local-test notes for VirtualDJ skin behavior that is terse, ambiguous, or easy
to misread in the official Skin SDK documentation.

These notes were promoted from GraveRaver and StackRaver skin development
experiments. Keep
project-specific XML scraps in the skin project, but record broadly reusable
runtime behavior here and fold stable guidance into [Skin SDK](Skin%20SDK.md).

## Define Placeholders And `*`

Source: `Local test` from a temporary GraveRaver skin canary; build not
recorded. See also the maintained canary fixture in
[tests/Skins/PlaceholderConditionTest](../tests/Skins/PlaceholderConditionTest/).

The official docs describe `*placeholder` as enabling simple math. Local
testing showed a broader practical rule for expression-like contexts:

- Use unstarred placeholders for simple pass-through values that match official
  and built-in skin examples.
- Prefer `*name` where the placeholder participates in arithmetic,
  coordinate/size formulas, boolean conditions, `param_equal` comparisons, or
  other VDJScript expression-like contexts.
- Treat text and text-action substitution as pattern-specific until more build
  results are recorded; the canary below kept an unstarred string literal.

Observed as fragile/non-working in the temporary canary:

```xml
<define class="STRING_CONDITION_CANARY" placeholders="side=false">
  <text text="[SIDE]"/>
  <group condition="param_equal '[SIDE]' 'true'"/>
</define>
```

`[SIDE]` stayed literal and did not drive conditions.

The starred form substituted correctly:

```xml
<define class="STRING_CONDITION_CANARY" placeholders="*side=false">
  <text text="[SIDE]"/>
  <group condition="param_equal '[SIDE]' 'true'"/>
</define>
```

For production skin code, this is the safer pattern for boolean-like
placeholders used in conditions:

```xml
<define class="TRACK_MODIFIERS_PANEL" placeholders="*mirror=false">
  <group condition="not [MIRROR]"/>
  <group condition="[MIRROR]"/>
</define>
```

Called as:

```xml
<panel class="track_modifiers_panel" mirror="false"/>
<panel class="track_modifiers_panel" mirror="true"/>
```

Numeric starred placeholders also worked:

```xml
<define class="EXAMPLE" placeholders="*flip=0">
  <group condition="param_equal [FLIP] 0"/>
  <group condition="param_equal [FLIP] 1"/>
</define>
```

## String Comparisons

Source: `Local test` from the same temporary GraveRaver skin canary.

When comparing placeholder values as strings, quote the placeholder expansion
and the target value:

```xml
condition="param_equal '[MIRROR]' 'true'"
```

For boolean-like placeholders declared with `*`, direct boolean conditions also
worked:

```xml
condition="[MIRROR]"
condition="not [MIRROR]"
```

Use direct boolean conditions only when the placeholder value is exactly `true`
or `false`.

## Deck-Scoped Dynamic Text Color

Source: `Official` for dynamic color syntax, `Official forum` for the
single-`<text>` dynamic-color recommendation, and `Local test` from the
GraveRaver `SYNC_INFO_EXTENDED` class in June 2026.

When a reusable class needs a dynamic text color based on deck state, explicitly
scope the predicate to the class deck placeholder:

```xml
<define class="SYNC_INFO_EXTENDED" placeholders="*deck,*width=920,*height=75">
  <textzone>
    <pos x="+0" y="+17"/>
    <size width="90" height="30"/>
    <text color="`deck [DECK] masterdeck ? color 'orange' : color 'white'`"
          align="left"
          size="36"
          weight="bold"
          action="var_equal '@$bpm_hide_options' 1 ? get_text '--.--' : var_equal '@$jog_bpm_digits' 0 ? get_text '%Pbpm' : get_text '%Pbpmex'"/>
  </textzone>
</define>
```

This pattern was confirmed working after an unscoped dynamic-color example was
not sufficient in the GraveRaver context. Treat it as the safest form when a
class can be instantiated for different decks, mirrored, or nested inside other
deck-aware containers.

Do not replace `orange` with a skin-defined color name inside the backticked
script:

```xml
<!-- Not supported by staff guidance. -->
<text color="`masterdeck ? color 'color_masterdeck' : color 'white'`"/>
```

Skin-defined color names such as `color_masterdeck` still work in direct XML
color fields:

```xml
<text color="color_masterdeck" action="get_bpm"/>
```

If a dynamic branch must preserve a defined skin color, split the element into
wrapper-level `visibility=""` branches instead of putting the defined color name
inside a script.

Related sources:

- [Skin Default Colors](https://virtualdj.com/wiki/Skin%20Default%20Colors.html) - official `source=` versus backticked `color=` distinction.
- [Skin text action; visibility or visual?](https://www.virtualdj.com/forums/267953/VirtualDJ_Skins/Skin_text_action%3B_visibility_or_visual%3F.html) - staff recommendation for one dynamic text color expression.
- [On the use of colour defines](https://virtualdj.com/forums/265321/VirtualDJ_Skins/On_the_use_of_colour_defines.html) - staff note that defined skin colors are not available inside scripts.

## Conditional Group Positioning

Source: `Local test` from the same temporary GraveRaver skin canary.

For `<group>`, put `x` and `y` directly on the group node. Do not rely on
conditional child `<pos>` elements for group placement.

Verified working:

```xml
<group x="+0" y="+5" condition="not [MIRROR]">
  ...
</group>
<group x="+265" y="+5" condition="[MIRROR]">
  ...
</group>
```

Observed as fragile/non-working:

```xml
<group>
  <pos x="+0" y="+5" condition="not [MIRROR]"/>
  <pos x="+265" y="+5" condition="[MIRROR]"/>
  ...
</group>
```

In the canary, the child-`<pos>` group rendered but did not move horizontally,
while equivalent `condition` branches on groups with direct `x` / `y` behaved
correctly.

## Runtime Variables In Position/Size Values

Source: `Local test` from the GraveRaver desktop skin, June 2026.

VirtualDJ evaluates `@$vars` and VDJScript in element **`condition=""`** attributes,
but **not** inside the `x` / `y` / `width` / `height` **value** expressions. Position
and size values are static arithmetic over numeric literals and `[PLACEHOLDER]`
substitutions only. An embedded backtick script or `get_var` term in a value is
dropped — VirtualDJ keeps the static remainder, so the element renders at a fixed
spot instead of tracking the variable.

This is distinct from `[PLACEHOLDER]` substitution (see "Define Placeholders And
`*`"), which *does* work in position/size values because it is resolved at class
instantiation, before the value is evaluated. The limitation is specifically about
reading a **runtime** variable inside a value.

Observed as non-working (a browser surface meant to track `@$infntywavesize`):

```xml
<!-- Browser stayed at the @$infntywavesize=0 position; the backtick term was ignored. -->
<pos x="0" width="1920"
     y="1080-[HEIGHT]+7+`get_var '@$infntywavesize' &amp; param_multiply 20`-207"
     height="[HEIGHT]-7-`get_var '@$infntywavesize' &amp; param_multiply 20`+207-50"/>
```

The working form enumerates one rung per value and selects it with a `condition`:

```xml
<pos x="0" width="1920" y="1080-[HEIGHT]+7-207"  height="+[HEIGHT]-7+207-50"  condition="var_equal '@$infntywavesize' 0"/>
<pos x="0" width="1920" y="1080-[HEIGHT]+27-207" height="+[HEIGHT]-27+207-50" condition="var_equal '@$infntywavesize' 1"/>
<!-- ...one rung per @$infntywavesize value... -->
```

Implication: a size/position that depends on a runtime variable must be a ladder of
`condition`-gated `<pos>` rungs, not a single computed expression. To keep large
ladders DRY, generate the rungs with a build script rather than computing inline
(GraveRaver does this in `tools`/`scripts` for its browser position tables). This is
the same condition-vs-value split seen in "Conditional Group Positioning" above.

## Conditional Breaklines

Source: `Official forum` for the top-level `<breaklines>` element syntax,
`Community` for the conditional build-7438 example in the VirtualDJ 2020
skin-engine additions thread, and `Local test` from the GraveRaver desktop skin
in June 2026.

VirtualDJ supports top-level `<breaklines>` child elements with `breakline1`,
`breakline2`, and optional `condition` attributes:

```xml
<breaklines breakline1="675" breakline2="1000" condition="var_equal '@$skin_mode' 0"/>
<breaklines breakline1="980" breakline2="1070" condition="var_equal '@$skin_mode' 1"/>
```

This is distinct from the older static root attributes:

```xml
<skin ... breakline="1000" breakline2="1000">
```

In GraveRaver, replacing static root breaklines with conditional top-level
`<breaklines>` entries worked in a desktop skin, allowing different structural
layouts to use different vertical stretch regions. The controlling layout
variable still belongs to the structural skin state bucket: when a button or
menu changes it, pair the state change with `load_skin` so the skin reparses and
selects the matching breakline entry.

Do not conflate this desktop/root mechanism with bundled Remote skins that place
`breakline1` / `breakline2` attributes on browser/settings panels. The Remote
panel-local pattern is shipped XML evidence, while desktop conditional
`<breaklines>` currently has community plus local-test evidence.

Related forum sources:

- [VirtualDJ 2020 - Additions in Skin Engine](https://virtualdj.com/forums/230926/VirtualDJ_Skins/VirtualDJ_2020_-_Additions_in_Skin_Engine.html?page=2) - community conditional `<breaklines>` example.
- [The basic question about skin](https://virtualdj.com/forums/265030/VirtualDJ_Skins/The_basic_question_about_skin.html) - staff use of top-level `<breaklines breakline1="" breakline2=""/>` syntax.

## Stack Slot Assignment Is Not A Queue

Source: `Local test` from the StackRaver desktop skin, tested in VirtualDJ on
2026-07-14.

The official `Skin Stack.html` docs imply that a `<stack>` shows "the last N
visible items" for N slots, suggesting a queue where the newest visible items
win the slots. Local testing did not reproduce that behavior: when more items
are visible than there are slots, the surplus items are not dropped — items
render **overlapping** within the slots instead of the newest N replacing the
oldest.

Observed as non-working (multiple items visible at once for one slot; they
drew on top of each other rather than queueing):

```xml
<stack fadein="150ms" fadeout="300ms">
  <size width="1920" height="164"/>
  <slot x="0" y="46"/>
  <item visibility="is_using 'loop' 8000ms"><panel class="row_loop"/></item>
  <item visibility="is_using 'effect' 8000ms"><panel class="row_fx"/></item>
  <!-- Both conditions true at the same time -> both items rendered
       overlapping in the single slot. -->
</stack>
```

The reliable pattern is to keep item visibility **mutually exclusive** per
stack — one stack per screen slot, driven by a selector variable, with each
item gated by `var_equal` so exactly one item can be visible at a time:

```xml
<stack fadein="150ms" fadeout="300ms">
  <size width="1920" height="164"/>
  <slot x="0" y="46"/>
  <item visibility="var_equal '$sr_slot1' 0"><panel class="row_deck" deck="1"/></item>
  <item visibility="var_equal '$sr_slot1' 1"><panel class="row_deck" deck="2"/></item>
  <item visibility="var_equal '$sr_slot1' 4"><panel class="row_mixer"/></item>
  <item visibility="var_equal '$sr_slot1' 5"><panel class="row_pads"/></item>
</stack>
```

With mutually exclusive items, cross-fading between items in a slot works well
via the stack's `fadein` / `fadeout` attributes: switching the selector
variable fades the old item out and the new item in. Treat `<stack>` as a
cross-fade container per slot, not as a notification queue.

## Defined Color Names In Custom-Browser `<colors>` Blocks

Source: `Local test` from the StackRaver desktop skin, tested in VirtualDJ on
2026-07-14. Contrast case from the GraveRaver production skin.

Skin-defined color names (declared with `<define color=.../>`) do **not**
resolve inside the `<colors>` blocks of the standalone custom-browser
components `<folderlist>`, `<filelist>`, and `<browsertoolbar>`. VirtualDJ
falls back to its magenta error color in the list backgrounds instead of
resolving the name.

Observed as non-working:

```xml
<define color="panel_bg" value="#0a0a0c"/>
...
<filelist attachX="both" attachY="both">
  <pos x="0" y="38"/>
  <size width="1904" height="364-38"/>
  <colors>
    <!-- Rendered with VirtualDJ's magenta fallback, not #0a0a0c. -->
    <lists background="panel_bg" text="#9aa4b2"/>
  </colors>
</filelist>
```

Literal hex values work:

```xml
<filelist attachX="both" attachY="both">
  <pos x="0" y="38"/>
  <size width="1904" height="364-38"/>
  <colors>
    <lists background="#0a0a0c" stripes="#0e0f12" text="#9aa4b2"
           over="#1d2330" selected="#232b3a" selectedtext="#ffffff"/>
    <scrollbars background="#111111" button="#444444"/>
  </colors>
</filelist>
```

Note this differs from full `<browser>` elements: the GraveRaver production
skin successfully uses defined color names inside `<browser>` `<colors>`
blocks. The limitation appears specific to the standalone custom-browser
components. When building `folderlist` / `filelist` / `browsertoolbar` color
schemes, use literal hex values (or generate the `<colors>` block from a
palette at build time if DRY-ness matters).

This is a separate restriction from defined color names inside backticked
scripts (see "Deck-Scoped Dynamic Text Color" above) — there the names are
unavailable in script contexts; here they fail in a plain XML `<colors>` block
of specific components.

## Official Docs

- [VirtualDJ Skin Define](https://www.virtualdj.com/wiki/Skin%20Define.html)
- [VirtualDJ Skin Element Positioning](https://www.virtualdj.com/wiki/Skin%20Element%20Positioning.html)
- [VirtualDJ Skin Element Properties](https://www.virtualdj.com/wiki/Skin%20Element%20Properties.html)
