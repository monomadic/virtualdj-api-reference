# Native skin container and child relationships

The symbol-rich **18.0.9246 arm64** custom host now recovers contextual XML-to-object
relationships, including children built without the general factory. The
2026-09-30 UTC captures pair positive fixtures with controls, retain native trees,
and trace original XML paths into the actual readers. These are **Tier 2 offline
native observations**, not same-build live-app proof or an exhaustive schema.

## Recovered relationships

| XML parent/path | Construction observed in the fixed 9246 host | Paired control or boundary |
| --- | --- | --- |
| `skin`, `panel` | `CSkinPanel::loadChildren` recursively invokes the object factory | Nested panels retain their children; an unknown wrapper drops its subtree |
| Plain `group` | Children flatten into the current owner | A group with `visibility="true"` instead creates `CSkinPanel`; visibility evaluation itself was not tested |
| `deck`, `setdeck` | Children flatten into the owner and receive deck context | The wrapper is absent from the runtime tree |
| `button/text`, `textdown`, `textover`, `textselected` | Named lookups construct `CSkinText` directly | Nested button/panel controls are not dispatched; repeated `text` selects the first node |
| `slider/fader` | Named lookup constructs `CSkinSliderFader` | Direct button and text controls produce no child object |
| `stack/item` | Each item constructs `CSkinPanel`, whose children enter the factory | Repeated items create separate panels; direct button/panel controls are ignored |
| `rack/unit/panel` | Constructs `CSkinResizePanel`, whose contents enter the factory | Direct rack/button, rack/panel, and unit/button controls produce no child object |
| `split/left`, `split/right` | Constructs `ISkinResizePanel` for each side; side children enter the factory | Direct split/button, split/content, and split/panel do not populate the sides |
| `split/left/content` | The resize panel selects `content` and dispatches its children | `content` itself is not an object |
| `resizepanel` or `resizepanel/content` | `ISkinResizePanel` dispatches direct children or the selected content's children | These cases have different geometry processing from an ordinary panel |
| `textzone/button` | `CSkinText` is constructed; the marker button is absent | This is a contextual negative, not a global rejection of `button` |

For example, a split containing a button under `left/content` produces:

```text
CSkinWindow
  CSkinGrabZone                       generated
  CSkinSplit
    ISkinResizePanel                  left
      CSkinButton                    left/content/button
    ISkinResizePanel                  right, empty
  CSkinGrabZone                       generated
```

An XML `<panel>` beneath a rack unit becomes a **resize panel**, while an XML
`<item>` beneath a stack becomes an **ordinary panel**. The tag spelling alone
does not determine the resulting native class. Conversely, button text and slider
faders are child objects even though they bypass the general factory.

## How the relationships were recovered

The static pass reads RTTI inheritance, symbol names, direct factory/loader calls,
named child lookups, helper arguments, and bounded routine disassembly from the
exact pinned binary. It keeps three kinds of evidence separate:

- A C++ base such as `ISkinContainer` establishes an object-layout relationship.
- A child lookup or constructor call identifies a reader or construction lead.
- A native fixture and source-path trace establish what the tested XML actually
  produced inside this host.

The host reads ordered native child vectors and recognizes primary `ISkinObject`
base layouts through RTTI. Unknown layouts, invalid bounds, cycles, and non-finite
rectangles stop the reader. The new wrapper reuses the original bounded
composition host. Debugger probes are armed **after** native-code hashes pass;
placing software breakpoints earlier changes the bytes being checked and caused
the retained initial trace failure.

Before loading, the debugger indexes the original XML nodes by paths such as
`/skin/rack[1]/unit[1]/panel[1]/button[1]`. Function-entry and return traces retain
these paths, reader names, call-site addresses, lookup keys, and returned classes.
New or unindexed nodes have no attributed source path. This supplies evidence
beyond merely observing a successful loader return.

The trace specifically records `CSkinButton::addTextObject` selecting
`/skin/button[1]/text[1]` from the repeated-text input. It also records a panel's
`size` node reaching the general factory and returning null, while the native
panel has the dimensions specified by that node. **Null factory return is not an
unknown-tag diagnostic**: configuration children and constructed object children
are different roles.

## Query and reproduce

```sh
# Partial contextual manifest, no native execution:
just native-skin-children --parent button
just native-skin-children --parent split

# Static reader leads, with call sites and named arguments:
just skin-child-readers --class CSkinButton

# Complete saved input and native tree:
just skin-child-probe show --case rack_unit_panel
just skin-child-probe show --case split_left_content
just skin-child-check
```

Regenerate from the user-provided symbol-rich app with fresh work/capture paths:

```sh
just doctor
uv run --with capstone --with numpy --python .venv/bin/python3 python \
  tools/probe_skin_relationships.py prepare \
  --app /Volumes/nom/src/virtualdj-api-reference-resources/unpacked/9246/vdj.pkg/Payload/VirtualDJ.app \
  --work /private/tmp/vdj-child-example
just skin-child-probe run --work /private/tmp/vdj-child-example \
  --output /private/tmp/vdj-child-example/native.json
just skin-child-trace --work /private/tmp/vdj-child-example \
  --output /private/tmp/vdj-child-example/trace.json
```

`tools/extract_skin_relationships.py --app ... --output NEW.json` regenerates the
static evidence and requires capstone/numpy. The manifest generator reads the
confirmed evidence files and refuses to overwrite its artifact. Preserve prior
captures before replacing evidence. Queries and checks require no vendor binary,
debugger, capstone, or numpy.

Evidence artifacts:

- [Contextual manifest](../tests/skin-container-manifest-9246.json): rules, exact
  fixtures, XML/native paths, evidence hashes, and `closed_world: false`.
- [Native relationship matrix](../tests/skin-child-relations-9246.json).
- [Source-path call/return traces](../tests/skin-child-trace-9246.json).
- [Static readers and calls](../tests/skin-child-readers-9246.json).
- [Host class ABI and routine fingerprints](../tests/skin-child-layout-9246.json).

Confirmed worker runs reproduced every loaded-tree result from the sized initial
matrix, and independent debugger runs reproduced the source-path traces. The
saved checker checks expected object shapes, positive/negative controls, source
identity, native/debugger agreement, key call/return paths, and manifest freshness.

## Remaining boundaries

This is a **partial manifest with open coverage**. Unlisted children are unknown,
not unsupported. Static named-child lists may refer to nested configuration nodes;
method ownership is not enough to assign an XML parent. Direct-call extraction
does not resolve every indirect call, dynamic lookup name, or value held across
control-flow joins. For example, the split's conditional side names are recovered
more clearly by the native source-path trace than by straight-line literal tracking.

The initial rack unit's panel had no dimensions and produced non-finite geometry.
The confirmed fixture supplies explicit position and size. That failure remains
in `skin-child-relations-9246-expanded-initial.json`; it is not classified as an
invalid XML grammar. Rendering, script evaluation, conditional visibility,
plugins, and arbitrary runtime state are outside this experiment.

The captures retain experimental resize/restore snapshots, but this manifest uses
the **loaded** tree. In particular, the initially unsized text under a panel does
not return to the identical rectangle after the direct move round trip. This does
not establish window-resize semantics; see [Offline Skin Host](Offline%20Skin%20Host.md).

The [vendor nesting graph](Skin%20Element%20Discovery.md) remains a separate source
observation. These native relationships can guide contextual lint diagnostics and
compiler structure, but promotion to supported behavior needs a discriminating
fixture in the same live build, with layout/object effects independently observed.
