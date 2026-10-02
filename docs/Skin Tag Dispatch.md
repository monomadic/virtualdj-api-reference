# Skin tag dispatch

Which tag names the skin engine recognizes, where it recognizes them, and what each
one becomes, recovered from the named arm64 code of **build 18.0.9246**. Everything
here is **Tier 2** under [Evidence Standards](Evidence%20Standards.md): it describes
recognition and construction paths in the binary, not runtime behaviour. Nothing in
it is a live-app result.

```sh
just skin-dispatch                 # summary: factory branches, loaders, site counts
just skin-dispatch group           # every rule and site for one name
just skin-dispatch --unresolved    # computed names and open rules
```

The capture is [tests/skin-dispatch-9246.json](../tests/skin-dispatch-9246.json).
`just skin-structure <tag>` remains the place for an element's attributes and direct
children; this capture is the layer underneath it, saying which names reach which code.

## A tag's meaning depends on who reads it

The same spelling is handled by different code depending on its parent, and the
object factory is only one of those readers.

| Context | What the code does |
| --- | --- |
| Object factory (`ISkinObject::createSkinObject`) | Matches the name and constructs a class, or performs a directive and returns no object |
| Panel, window and root children (`CSkinPanel::loadChildren`) | Intercepts `deck`, `setdeck`, `window`, `group` and `grabzone` before the factory |
| Rack (`CSkinRack::loadChildren`, `addUnitChildren`) | Matches only `deck` and `unit`, then `deck` and `panel` inside a unit |
| Stack | Matches only `slot` (geometry) and `item` (a panel) |
| Split | `type="vertical"` selects `up`/`down`, otherwise `left`/`right` |
| Resize panel | A `content` child, when present, supplies the children |
| Menu, multibutton | `item`/`submenu`/`separator` entries; `choice` entries |
| Per-class child slots (`CXMLNode::getChild`, `ISkinObject::getCondition`) | Named children read for images, geometry, colours or nested data |

Examples of the consequences:

- `group` without `visibility` or `novisibility` is a wrapper: its condition is
  checked, its `x`/`y` are added to the owner's offset, and its children join the
  owner. With either attribute it reaches the factory and becomes a `CSkinPanel`.
- `deck`/`setdeck` set the current deck from their `deck` attribute for their
  children only, and check no condition. One with no children is skipped.
- `panel` under a rack `unit` becomes a `CSkinResizePanel`; `item` under a `stack`
  becomes a `CSkinPanel` whose `visibility` is compiled and then removed.
- `window` anywhere a panel's children are read creates a separate top-level window.

## The factory

- **Gates first.** An `os` attribute, when present, must be exactly `mac` (a
  case-sensitive comparison, on this macOS build), and `ISkinObject::checkCondition`
  must pass. Failing either returns no object.
- **Names match case-insensitively but exactly**, with the length tested first.
  Branches are tried in order and the first match wins.
- **An unmatched name returns no object, with no diagnostic.** This is why a
  misspelled tag silently disappears.
- **Some branches create no object.** `window`, `tooltip`, `dialogs`, `onload`,
  `oninit`, `onexit`, `font`, `customicons` and `define` are directives: they
  configure the engine, compile actions, or register a class definition.
- **Some branches choose a class from an attribute.** For example, `text` with a
  `group` attribute builds a `CSkinTextGroup`, and `songpos` with
  `orientation="circle"` or `"vertical"` builds a slider bound to `song_pos`.

The root element of a skin file is not compared by name: the engine loads it as the
main window. A root child named `nbdecks` whose condition passes sets the deck count.

## How it was recovered

`tools/skin_dispatch.py` streams `objdump` over the pinned binary and keeps two
layers apart:

- **Sites (mechanical).** Every literal `strIsEqualCI` and every named child lookup
  in the `CSkin*`/`ISkin*`/`SSkin*` functions, with its address. A child node is
  followed until something consumes it, which assigns its role: `object`,
  `container`, `slot`, `data`, or `unknown`.
- **Reviewed rules.** The factory's gates, comparison rule, selectors and
  directives, and the container loaders above, were read from the disassembly.
  Each rule cites the instruction it rests on, and extraction fails if that address
  no longer holds the cited call or literal.

The scan is linear, which bounds what the mechanical layer can say:

- A role lists every consumer seen on any path.
- A compare is `tag_compare` only when the compared string is a known node, and
  `value_compare` when it is an attribute value or string object. Anything else
  stays `compare`.
- A branch reached from elsewhere can still be misread, which is why only the
  reviewed rules make claims about meaning.

## Window initialization

The window was the one factory element with no established XML binding. The factory
default-constructs `CSkinWindow` and then passes the node to
`CSkinWindow::load(node, image, nullptr)`. The panel loader and the engine's root
load do the same. `just skin-structure window` now projects its attributes and
children through that call.

## Open

`just skin-dispatch --unresolved` lists what is still open:

- Lookups whose name is computed, not a literal.
- Compares the scan could not classify.
- The engine field that gates `oninit` and the global flag that suppresses
  `browser`.

Child lookups whose node the linear scan loses keep role `unknown`. Template,
class and condition expansion (`define`, `class=`, `condition=`) is in
[Skin Expansion](Skin%20Expansion.md).
