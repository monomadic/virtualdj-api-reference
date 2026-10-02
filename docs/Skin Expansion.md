# Skin expansion: classes, placeholders and conditions

How the skin loader of **build 18.0.9246** (arm64) rewrites and filters XML before
objects read it. The rules below were read from the named code (`CSkinClass::add`,
`apply`, `applyXml`, `applyPlaceholders`, `ISkinObject::checkCondition`,
`getCondition`). Each rule that changes geometry was then tested with a paired
fixture in the offline composition host.

Both halves are **Tier 2** under [Evidence Standards](Evidence%20Standards.md):

- **Disassembly** says what the code does.
- **The fixtures** are native observations of the copied image, not live-app
  results.

```sh
just skin-expansion check     # saved fixtures against their predictions
just skin-dispatch define     # where `define` is recognized
```

Evidence: [tests/skin-expansion-9246.json](../tests/skin-expansion-9246.json), produced by
[tools/probe_skin_expansion.py](../tools/probe_skin_expansion.py). Each case states its
predicted button rectangles before the run, beside a control. The table names the
fixtures; the capture has the inputs and the native trees.

## There is no include mechanism

No skin function on this build loads another file into a skin. The only
`include` symbols in the binary belong to bundled third-party libraries. A skin is
one XML file, plus whatever its `define`s supply.

## `define`

`<define>` is a factory directive: it creates no object and registers data in the
order the loader meets it. A class is only available to elements loaded after its
definition (fixture `class_forward` in the composition capture).

| Form | Rule |
| --- | --- |
| `class="NAME"` | Stores the node as a class, keyed by name (case-insensitive) and `classdeck` (absent means any deck). Defining the same name and deck again replaces the earlier definition (`class_redefined`). |
| `color="NAME"` | Stores a named colour from `value`, keyed by `deck`. Redefining overwrites the value. |
| neither | Ignored. |

## `class="NAME"` on an element

- **Where it applies.** Only for objects (`ISkinObject::load`) and windows
  (`CSkinWindow::load`). These are its only callers in the binary. On anything else,
  such as a `size` child, it does nothing (`class_on_child_ignored`, control
  `class_on_object`).
- **Which variant.** The object's deck comes from `deck`, or else `chan`, and is
  read *before* the merge, so a class cannot choose its own variant. The first
  definition, in definition order, whose `classdeck` is absent or equal to that deck
  wins. A generic definition made first therefore shadows deck-specific ones made
  after it (`classdeck_specific_first`, control `classdeck_generic_first`). Four
  mixer-order pseudo-decks are resolved through `getMixerOrderDeck` and retried
  first; that path has no fixture.
- **Attributes merge.** Each class attribute except `placeholders` is added unless
  the element already has one with that name (compared case-insensitively). The
  element wins (`class_partial_override` in the composition capture).
- **Children merge.** The element's *n*-th child with a given name absorbs the
  class's *n*-th child of that name, recursively. Class children with no partner
  are copied after the element's own children (`class_children_by_occurrence`,
  control `class_children_copied`).

## Placeholders

A class declares `placeholders="NAME=default,…"`. For each entry, an element
attribute with that name supplies the value and is then removed from the element.
Otherwise the default after `=` is used, or an empty string when there is no `=`.
The class's attribute values are then searched for the token `[NAME]`:

- **The token is upper case and matched exactly.** `[w]` is not replaced by
  placeholder `W` (`placeholder_case`).
- **Whole-value by default.** Only a value that is exactly `[NAME]` is replaced
  (`placeholder_value`, `placeholder_default`). `1[W]` stays as written
  (`placeholder_substring_off`).
- **`*` turns on substring replacement for the whole class.** If any entry is
  written `*NAME`, every `[NAME]` occurrence inside any value is replaced, up to 50
  per attribute (`placeholder_substring_on`).
- **Attribute values only.** Attribute names and node text are never substituted.
  Substitution applies to the element and all its children.

## Conditions

`condition="…"` is compiled as VDJScript and evaluated **once, at load**
(`IAction::create`, then `queryBool` with deck 0). A missing or empty condition
passes. It is honoured only where the loader asks:

| Where | Effect |
| --- | --- |
| Factory objects | A failing object is not created (`condition_object`) |
| Plain `group` wrapper | A failing group drops its children (`group_condition`) |
| `size`, `pos` and image slots (`getRectangle`, `getImage`, `getImageWithMask`) | A failing slot yields to the next same-named sibling whose condition passes (`condition_size_fallback`, control `condition_size_first`) |
| Named conditional children: `size`, `pos` (every object), `overlay` (rhythm, scratchwave), `breaklines` (window) | The first same-named child whose condition passes is used |
| A root child named `nbdecks` | Sets the deck count from `value` when its condition passes |

Objects built without the factory have no condition check on their own node on
this build. That covers button text children, stack items, rack units, split sides,
menu entries and multibutton choices. `deck`/`setdeck` wrappers check none either.

## `os`

A factory object with an `os` attribute is created only when the value is exactly
`mac`: `win` and `MAC` both drop it (`os_gate`). This is the macOS build; which value
the Windows build accepts is not established here.

## Open

- `define color` and named colours: the rule is from the disassembly, with no
  fixture. This host does not read colours.
- Mixer-order pseudo-decks in class selection: no fixture.
- Removal of the element attribute that fed a placeholder: from the disassembly
  only. The host does not read attributes back.
- Whether conditions see the deck set by a surrounding `deck` wrapper:
  `queryBool` is called with deck 0, and what that resolves to under a wrapper was
  not tested.
