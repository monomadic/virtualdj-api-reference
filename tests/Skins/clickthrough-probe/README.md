# `clickthrough` probe — seven minimal deck skins

The first candidate from the binary skin-reader extraction
(`just skin-candidates`) taken to a live deck-skin test. `clickthrough` is
compared by the shared skin-object reader on build 18.0.9598 — so every skin
object reads it — and it appears in **no** shipped skin and **no** SDK doc.

## The fixture

`generate.py` renders all seven skins from one template so they are identical
apart from one attribute on one element; do not hand-edit the `.xml` files.

Two buttons occupy the same rectangle, the lower one declared first. Each
writes its own global, so the result is read over HTTP rather than judged from
a screenshot:

```
<button action="set '$ct_bottom' 1">   <- declared first, underneath
<button action="set '$ct_top' 1" ...>  <- declared second, on top, carries the variant
```

| Variant | Attribute on the top button | Role |
| --- | --- | --- |
| `baseline` | *(none)* | floor: the top button should swallow the click |
| `visible-off` | `visibility="param_equal 'no' 'yes'"` | **calibration** with a known working attribute |
| `pass` | `clickthrough="pass"` | the candidate, at the value the reader compares |
| `value-control` | `clickthrough="qzqzqz"` | nonsense **value** on the real attribute |
| `attr-control` | `zzclickthrough="pass"` | nonsense **attribute** carrying the real value |
| `yes` | `clickthrough="yes"` | the **boolean path**: stored TRUE, the one state never observed |
| `true` | `clickthrough="TRUE"` | same state in the other accepted spelling, upper-cased for the case rule |

The two boolean variants (added 2026-09-07) come from the historical-installer
finding that `ISkinObject::load` stores `-2` for `pass` and otherwise the result
of `CXMLNode::getBoolParam` with a false default. That parser, read by name on
builds 9.0.5308, 9.0.7607 and 18.0.9246, accepts exactly `yes`/`true` → true
and `no`/`false` → false, case-insensitively and by exact length, and returns
the default for every other value. So `no`, `false`, `1`, `0`, `on`, `off`
and nonsense all store the same `0` that `value-control` already tested;
the only stored state with no live observation is `1`. Evidence:
`tests/build-history-2026-09-06/*-bool-param.asm`. The two variants ran on
2026-09-07; see the result below.

`visible-off` is the control that makes a negative interpretable: it proves in
the same fixture that the click coordinate really is over the bottom button and
that attributes on the top button are honored, so "the click did not reach the
bottom" cannot be blamed on a missed coordinate.

## Running it

```sh
python3 tests/Skins/clickthrough-probe/generate.py --install
# load_skin 'ZZ Clickthrough <variant>/:skin', reset both globals, click the
# overlap, then read get_var "$ct_top" / "$ct_bottom"
python3 tests/Skins/clickthrough-probe/generate.py --uninstall
```

Two things the setup itself established, both needed to run this at all:

- **A skin folder with no image beside the XML is refused.** VirtualDJ puts up a
  modal *"Impossible to open skin `<name>`"* and keeps the current skin;
  `load_skin` still returns `true`. Adding `skin.png` and `preview.png` (flat
  colour, generated) made the identical XML load. So the generator installs both.
- **The skin list is not cached.** A folder created while VirtualDJ is running
  loads immediately — verified by copying a known-good skin to a new name.

Restore the operator's skin afterwards: read it with `load_skin` in *query*
position before starting, and pass that exact string back to `load_skin`.

## Result (2026-09-05, build 18.0.9598, deck-skin surface)

| Variant | `$ct_top` | `$ct_bottom` |
| --- | --- | --- |
| `baseline` | 1 | 0 |
| `visible-off` | 0 | 1 |
| **`pass`** | **1** | **1** |
| `value-control` | 1 | 0 |
| `attr-control` | 1 | 0 |

Reproduced in two independent runs with the variant order reversed in the
second. `clickthrough="pass"` fires the top element's own action **and** lets
the click continue to the element underneath; both controls separate from it,
so the attribute name and the value each matter.

## Result, all seven (2026-09-07, build 18.0.9598, deck-skin surface)

| Variant | `$ct_top` | `$ct_bottom` |
| --- | --- | --- |
| `baseline` | 1 | 0 |
| `visible-off` | 0 | 1 |
| **`pass`** | **1** | **1** |
| `value-control` | 1 | 0 |
| `attr-control` | 1 | 0 |
| **`yes`** | **0** | **1** |
| **`true`** (written `TRUE`) | **0** | **1** |

Two runs, forward then reversed, every row identical both times. Each variant
was loaded, confirmed with `load_skin` in query position, both globals reset to
`0` over HTTP, clicked once at the overlap's centre by a CGEvent helper, then
both globals read back. A screenshot of the `yes` skin shows the TOP button
still drawn, so the boolean form is transparency to clicks and not hidden
geometry — `visible-off` reaches the same counters by not rendering.

So the attribute has **three states**, exactly the three the loader can store:

| Value | Top element's action | Element underneath |
| --- | --- | --- |
| absent, `no`, `false`, nonsense | fires | not reached |
| `pass` | fires | reached |
| `yes`, `true` (any case) | **does not fire** | reached |

`TRUE` agreeing with `yes` is the live confirmation of the parser's
case-insensitive compare. `no`/`false` were not run: the parser stores the same
`0` for them as for `value-control`, which was.
