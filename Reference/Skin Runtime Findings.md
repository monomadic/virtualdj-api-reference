# Skin Runtime Findings

Local-test notes for VirtualDJ skin behavior that is terse, ambiguous, or easy
to misread in the official Skin SDK documentation.

These notes were promoted from GraveRaver skin development experiments. Keep
project-specific XML scraps in the skin project, but record broadly reusable
runtime behavior here and fold stable guidance into [Skin SDK](Skin%20SDK.md).

## Define Placeholders And `*`

Source: `Local test` from a temporary GraveRaver skin canary; build not
recorded. See also the maintained canary fixture in
[Test/Skins/PlaceholderConditionTest](../Test/Skins/PlaceholderConditionTest/).

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

## Official Docs

- [VirtualDJ Skin Define](https://www.virtualdj.com/wiki/Skin%20Define.html)
- [VirtualDJ Skin Element Positioning](https://www.virtualdj.com/wiki/Skin%20Element%20Positioning.html)
- [VirtualDJ Skin Element Properties](https://www.virtualdj.com/wiki/Skin%20Element%20Properties.html)
