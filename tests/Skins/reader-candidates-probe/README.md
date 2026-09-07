# Reader-candidate probe — the rest of the skin-reader vocabulary

`tests/Skins/clickthrough-probe/` took the first name out of the binary
skin-reader extraction to a live test. This fixture takes the rest: the
candidates `just skin-candidates` prints, and the element names
`just skin-reader element_dispatch` shows the switch accepting that appear in
no shipped skin and no doc.

Same discriminator throughout. Two things share one rectangle, the lower one
declared first; each writes its own global, so what happened is read over HTTP
instead of judged from a screenshot:

```
<button action="set '$rc_bottom' 1">   <- declared first, underneath
   …the candidate…                     <- declared second, on top
```

`generate.py` renders every variant from one template — do not hand-edit the
`.xml` files. `run.py` loads each variant, resets the globals, clicks a named
point with a CGEvent helper it compiles itself, and reads both globals back.

```sh
python3 tests/Skins/reader-candidates-probe/generate.py --install
python3 tests/Skins/reader-candidates-probe/run.py --calibrate   # must pass first
python3 tests/Skins/reader-candidates-probe/run.py --series all
python3 tests/Skins/reader-candidates-probe/run.py --series all --reverse
python3 tests/Skins/reader-candidates-probe/generate.py --uninstall
```

`--calibrate` clicks the one variant whose answer is known (a plain `<button>`)
and refuses to go on if the mapping from skin coordinates to screen points is
wrong. On the machine this ran on, VirtualDJ scaled the 900×560 skin to the
full 1440×900-point display, so `--scale 1.6 --origin 0,0` (the defaults) put
the rectangle's centre at (720, 415). Restore the operator's skin afterwards:
read it with `load_skin` in *query* position first, and pass that exact string
back.

## Results (2026-09-07, build 18.0.9598, deck-skin surface)

Every table below ran twice, forward and with the variant order reversed, and
every row was identical in both runs.

### The tag alone, with its own `pos`/`size`

`bottom=1` means the click fell through to the button underneath.

| Variant | Top element | `$rc_top` | `$rc_bottom` | Reading |
| --- | --- | --- | --- | --- |
| `el-button` | `<button>` | **1** | 0 | calibration: a known element takes the click |
| `el-nonsense` | `<zzznotanelement>` | 0 | **1** | control: an unknown tag is dropped |
| `el-pannel` | `<pannel>` | 0 | **1** | an empty container has nothing to hit |
| `el-songpos` | `<songpos>` | 0 | 0 | calibration: **takes the click** |
| `el-song_pos` | `<song_pos>` | 0 | **1** | like the control |
| `el-foldersearch` | `<foldersearch>` | 0 | **1** | like the control |
| `el-multibutton` | `<multibutton>` | 0 | 0 | **takes the click** |
| `el-resizepanel` | `<resizepanel>` | 0 | **1** | like the control |
| `el-rack` | `<rack>` | 0 | **1** | like the control |
| `el-keyboardmap` | `<keyboardmap>` | 0 | **1** | like the control |
| `el-os` | `<os>` | 0 | **1** | like the control |
| `el-darkmode` | `<darkmode>` | 0 | **1** | like the control |

`<multibutton>` draws nothing — a screenshot of that variant shows the BOTTOM
button unobscured and unpressed — and still absorbs the click, so it builds a
real object with a hit area and no default rendering.

### The tag wrapping a button

The row above cannot separate an unknown tag from a known container: an empty
`<pannel>` lets the click through exactly as a dropped tag does. So the
candidate wraps the TOP button instead.

| Variant | Wrapper | `$rc_top` | `$rc_bottom` |
| --- | --- | --- | --- |
| `box-group` | `<group>` | **1** | 0 |
| `box-pannel` | `<pannel>` | **1** | 0 |
| `box-nonsense` | `<zzznotanelement>` | 0 | **1** |
| `box-song_pos`, `box-foldersearch`, `box-multibutton`, `box-resizepanel`, `box-rack`, `box-keyboardmap`, `box-os`, `box-darkmode` | the candidate | 0 | **1** |

The control settles the question the series depends on: **a dropped tag takes
its subtree with it.** A button inside `<zzznotanelement>` is not built, so
"the child was not built" is what a dropped tag looks like, and every candidate
looks like that.

### The browser family, calibrated against itself

A deck-skin button is the wrong yardstick for `foldersearch`, which sits
between `folderlist` and `fileview` in the switch. The SDK Example browser skin
places `<folderlist>` as a standalone element with its own `pos`/`size`, so the
candidate gets the same placement and a calibration from its own family.

| Variant | Top element | `$rc_top` | `$rc_bottom` |
| --- | --- | --- | --- |
| `br-folderlist` | `<folderlist>` | 0 | 0 (**takes the click**) |
| `br-foldersearch` | `<foldersearch>` | 0 | **1** |
| `br-nonsense` | `<zzznotabrowserelement>` | 0 | **1** |

### `r` on `<mousecircle>` — the one attribute candidate

`CENTRE` is the rectangle's centre, `MID` is 55 px to its right, `CORNER` is
134 px away inside the rectangle. A hit is `$rc_top=1`; a miss falls through to
`$rc_bottom`.

| Variant | `<mousecircle …>` | CENTRE | MID | CORNER |
| --- | --- | --- | --- | --- |
| `r-none` | *(no attributes)* | hit | — | miss |
| `r-small` | `r="20"` | hit | **miss** | miss |
| `r-big` | `r="150"` | hit | hit | **hit** |
| `r-zz-big` | `zzr="150"` | hit | hit | **miss** |
| `r-wh` | `width="80" height="80"` | hit | — | miss |
| `r-xyr` | `x="150" y="80" r="40"` | **miss** | — | miss |
| `r-abs` | `x="450" y="260" r="40"` | **hit** | **miss** | — |

Two results, both with a separating control:

- **`r` sets the radius of the hit circle, in skin units.** `r="20"` excludes a
  point 55 px out that the default includes; `r="150"` includes a point 134 px
  out that the default excludes; the same value on `zzr` behaves exactly like
  no attribute at all. Without `r`, the circle already excludes CORNER and
  includes MID, so the default radius is the element's half-height (80 here).
- **`x`/`y` are absolute, not element-local.** `x="150" y="80"` — the
  rectangle's centre expressed *locally* — loses the hit area at every point,
  because the circle is drawn at (150, 80) in the skin's own coordinates, off
  the element. Writing the same centre absolutely (`x="450" y="260"`) puts it
  back, and `r="40"` then excludes MID at 55 px, which is the radius confirming
  itself a second time.

### `<onexit>` — confirmed, and it needs no click

| Variant | `<onexit>` present | `$rc_onexit` while loaded | after the next skin replaces it |
| --- | --- | --- | --- |
| `ev-onexit` | `<onexit action="set '$rc_onexit' 1"/>` | 0 | **1** |
| `ev-control` | `<zzonexit action="…"/>` | 0 | 0 |

`<onexit>` is the unload counterpart of `<onload>` / `<oninit>`: its action runs
when the skin is replaced, not when it loads. The nonsense-tag control never
fired, so the tag name is what matters.

### `forceshow` — not reached, and why

| Series | What varied | Result |
| --- | --- | --- |
| `fs-*` | one lone panel carrying `forceshow` = *(absent)*, `8pads`, `16pads`, `1fx`, `timecode`, `qzqzqz` | the panel is shown in every case, including the nonsense value |
| `fsg-*` | two panels in one `group=`, as shipped skins write them: A `3fx` / B `6fx`, A `8pads` / B `16pads`, and neither | panel A shows in every case |

The `fsg-*` series was run in both states of the app's own layout settings —
`skin3FxLayout` yes / `skin6FxLayout` no, then the reverse, with the skin
reloaded after the change — and once more after `effect_3slots_layout`, the
verb that flips `skin3FxLayout` itself. The visible panel never moved.

Boundary, in the R2 shape: the reader is `panel_builder`
(`just skin-reader panel_builder`), the values tried are all six it compares
plus a nonsense control, and the branch never exercised is whatever *asks* for
a layout variant. `skin3FxLayout` and `skin6FxLayout` are the only `skin*Layout`
settings in the binary, so `8pads` / `16pads` / `timecode` cannot be keyed to a
setting of that shape at all; `pad_has_16pads` ("returns true when a controller
is connected with a 4x4 pad layout") is the nearest thing the catalog offers,
which would make the pads values controller-conditional and untestable here.

### The root series is void — its calibration failed

`root-*` hangs the candidate off `<skin>` instead of putting it inside the
`<panel>`, in case a `<rack>` or a `<keyboardmap>` only constructs there. The
calibration row (`root-group`, a known container holding the same button) did
not deliver the click either, so nothing in that series is interpretable. Kept
because the calibration itself is the finding: **a container at the root of the
skin did not build a clickable button in this fixture** — every element that
worked here lives inside a `<panel>`.

## What a negative here does and does not say

Every candidate that behaved like the nonsense control was *dropped or inert in
this surface*. That is not "the name is unreal": the switch demonstrably holds
it, and a tag can need a context this fixture never built — a browser skin
proper, a `<split>`, a video skin, a mapper-driven layout request. What the
fixture does establish is that none of them constructs a click-taking object,
or builds its children, in a deck-skin panel or at the skin root on this build.
