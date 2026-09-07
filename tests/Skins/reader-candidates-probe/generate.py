#!/usr/bin/env python3
"""Generate the reader-candidate probe skins from one template.

R7: the skin-reader extraction (`just skin-candidates`, `just skin-reader
<name>`) recovered names the binary compares that no shipped skin and no doc
uses. `clickthrough` was carried to a live test in
`tests/Skins/clickthrough-probe/`; this fixture carries the rest.

Same method, same discriminator: two elements share one rectangle, the lower
one declared first, each writing its own global, so the answer is read over
HTTP rather than judged from a screenshot. What varies is what sits on top.

    python3 tests/Skins/reader-candidates-probe/generate.py --install
    python3 tests/Skins/reader-candidates-probe/run.py --origin X,Y
    python3 tests/Skins/reader-candidates-probe/generate.py --uninstall
"""

from __future__ import annotations

import argparse
import shutil
import struct
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTALL = Path.home() / "Library/Application Support/VirtualDJ/Skins"
PREFIX = "ZZ Reader"

# The shared rectangle. `spot` is the click point every one-click variant uses
# (the rectangle's centre); `corner` is inside the rectangle but outside the
# circle the `r` series draws, and is only used by that series.
GEOM = dict(bx=300, by=180, bw=300, bh=160, ry=380, dy=420)
CENTRE = (GEOM["bx"] + GEOM["bw"] // 2, GEOM["by"] + GEOM["bh"] // 2)
CORNER = (GEOM["bx"] + 30, GEOM["by"] + 20)
# 55 px right of the centre: inside a default circular hit area, outside a
# small explicit radius. CORNER is 134 px from the centre, outside both.
MID = (CENTRE[0] + 55, CENTRE[1])
POINTS = {"centre": CENTRE, "mid": MID, "corner": CORNER}

# --- series 1: does the tag build an object that takes the click? ------------
# A tag the switch does not know is dropped, so the click lands on BOTTOM. A
# tag that builds a hit-taking object keeps it. The two calibration rows are a
# known element and a nonsense one, so a row in between is interpretable.
ELEMENT_BLOCK = """<{tag}>
      <pos x="{bx}" y="{by}"/>
      <size width="{bw}" height="{bh}"/>
    </{tag}>"""

ELEMENTS = [
    ("el-button", "button", "calibration: a known element that takes clicks"),
    ("el-nonsense", "zzznotanelement", "control: a tag the switch cannot know"),
    ("el-pannel", "pannel", "calibration: the misspelling the switch is known to accept"),
    ("el-songpos", "songpos", "calibration: the shipped element `song_pos` sits beside"),
    ("el-song_pos", "song_pos", "candidate (also a verb name — the switch may only "
                                "reference it as the songpos default action)"),
    ("el-foldersearch", "foldersearch", "candidate, browser family"),
    ("el-multibutton", "multibutton", "known to the switch, in no skin and no doc"),
    ("el-resizepanel", "resizepanel", "known to the switch, in no skin and no doc"),
    ("el-rack", "rack", "known to the switch, in no skin and no doc"),
    ("el-keyboardmap", "keyboardmap", "known to the switch, in no skin and no doc"),
    ("el-os", "os", "known to the switch, in no skin and no doc"),
    ("el-darkmode", "darkmode", "known to the switch, in no skin and no doc"),
]

# --- series 1b: does the tag build a CONTAINER that loads its children? -----
# Series 1 cannot tell an unknown tag from a known container: `<pannel>` is a
# tag the switch is known to accept, and an empty one lets the click through
# exactly as a dropped tag does. So the candidate wraps a button instead of
# standing empty. If the tag builds a container, the button inside it is built
# and takes the click; if the tag is dropped, the question is whether its
# subtree goes with it — which is what the nonsense control measures.
CONTAINER_BLOCK = """<{tag}>
      {button}
    </{tag}>"""

CONTAINERS = [
    ("box-group", "group", "calibration: a known container"),
    ("box-pannel", "pannel", "calibration: the accepted misspelling of panel"),
    ("box-nonsense", "zzznotanelement",
     "control: does a dropped tag take its children with it?"),
    ("box-song_pos", "song_pos", "candidate"),
    ("box-foldersearch", "foldersearch", "candidate, browser family"),
    ("box-multibutton", "multibutton", "known to the switch, in no skin and no doc"),
    ("box-resizepanel", "resizepanel", "known to the switch, in no skin and no doc"),
    ("box-rack", "rack", "known to the switch, in no skin and no doc"),
    ("box-keyboardmap", "keyboardmap", "known to the switch, in no skin and no doc"),
    ("box-os", "os", "known to the switch, in no skin and no doc"),
    ("box-darkmode", "darkmode", "known to the switch, in no skin and no doc"),
]

# --- series 1d: the browser family, with a browser-family calibration -------
# `foldersearch` sits between `folderlist` and `fileview` in the switch, and a
# deck-skin button is the wrong yardstick for it. The SDK Example browser skin
# places `<folderlist>` and `<fileview>` as standalone elements with their own
# pos/size, so the same placement gives the candidate a calibration drawn from
# its own family.
BROWSER = [
    ("br-folderlist", "folderlist", "calibration: a shipped browser element"),
    ("br-foldersearch", "foldersearch", "the candidate"),
    ("br-nonsense", "zzznotabrowserelement", "control"),
]

# --- series 1c: the same tags as a direct child of <skin> --------------------
# Series 1b puts the candidate inside `<panel>`, where a `<rack>` or a
# `<keyboardmap>` plausibly does not belong. These variants hang the candidate
# off the root instead, with the same button inside it, so a tag that only
# constructs at the top level is not recorded as dropped. The two calibration
# rows say what the root does with a container and with a bare button.
ROOTS = [
    ("root-group", "group", "calibration: a known container at the root"),
    ("root-nonsense", "zzznotanelement", "control: unknown tag at the root"),
    ("root-rack", "rack", "candidate at the root"),
    ("root-keyboardmap", "keyboardmap", "candidate at the root"),
    ("root-os", "os", "candidate at the root"),
    ("root-darkmode", "darkmode", "candidate at the root"),
    ("root-resizepanel", "resizepanel", "candidate at the root"),
    ("root-multibutton", "multibutton", "candidate at the root"),
]

# --- series 2: `r` on <mousecircle> ------------------------------------------
# The SDK doc gives `<mousecircle x="" y="" r=""/>` as official and unused by
# any built-in skin; the shipped skins write `width`/`height` instead. A circle
# at the rectangle's centre with r=40 excludes CORNER and includes CENTRE, so
# two clicks per variant separate a honored radius from an ignored one.
MOUSE = [
    ("r-none", '<mousecircle/>', "mousecircle with no attributes at all",
     ("centre", "corner")),
    ("r-xyr", '<mousecircle x="150" y="80" r="40"/>',
     "the documented form, with the centre written as element-local coordinates",
     ("centre", "corner")),
    ("r-zzr", '<mousecircle x="150" y="80" zzr="40"/>',
     "control: nonsense ATTRIBUTE in place of the candidate",
     ("centre", "corner")),
    ("r-wh", '<mousecircle width="80" height="80"/>',
     "the form every shipped skin writes", ("centre", "corner")),
    # Second pass. The first four cannot separate `r` from `x`/`y`: every
    # variant that wrote x/y lost the hit area at both points, so the placement
    # was what moved, not the radius. These vary the radius alone.
    ("r-small", '<mousecircle r="20"/>',
     "radius only, smaller than the default: MID must fall outside it",
     ("centre", "mid", "corner")),
    ("r-big", '<mousecircle r="150"/>',
     "radius only, large enough to include CORNER (134 px from the centre)",
     ("centre", "mid", "corner")),
    ("r-zz-big", '<mousecircle zzr="150"/>',
     "control: the same value on a nonsense attribute — must behave like `r-none`",
     ("centre", "mid", "corner")),
    ("r-abs", '<mousecircle x="450" y="260" r="40"/>',
     "the same centre written as absolute skin coordinates: separates local "
     "from absolute placement", ("centre", "mid")),
]

# --- series 3: the `forceshow` vocabulary ------------------------------------
# `8pads` is the value the panel builder knows and no shipped skin writes; the
# five used values and a nonsense value are the frame that makes it readable.
FORCESHOW = [
    ("fs-none", "", "no forceshow: the panel is shown"),
    ("fs-8pads", 'forceshow="8pads"', "the candidate value"),
    ("fs-16pads", 'forceshow="16pads"', "a value shipped skins write"),
    ("fs-1fx", 'forceshow="1fx"', "a value shipped skins write"),
    ("fs-timecode", 'forceshow="timecode"', "the documented-only value"),
    ("fs-nonsense", 'forceshow="qzqzqz"', "control: nonsense value"),
]

# --- series 3b: forceshow inside a real panel GROUP --------------------------
# Series 3 could not discriminate: a lone panel is shown whatever it says, so
# every value looked alike. Shipped skins only ever write `forceshow` on a
# named `@panel` inside a `group=`, where exactly one member shows at a time —
# and the app carries two settings, `skin3FxLayout` and `skin6FxLayout` (named
# in the `effect_beats_all` catalog entry, and the only `skin*Layout` strings
# in the binary), which are what an fx value can be keyed to. Two panels on one
# rectangle, each with its own button, so one click says which is showing.
GROUP_PANELS = """<panel name="@fs_a" group="fsg" visible="yes" available="yes" displayname="A" {a}>
      {button_a}
    </panel>
    <panel name="@fs_b" group="fsg" visible="no" available="yes" displayname="B" {b}>
      {button_b}
    </panel>"""

GROUPED = [
    ("fsg-none", "", "", "control: neither panel forces; A is the visible one"),
    ("fsg-fx", 'forceshow="3fx"', 'forceshow="6fx"',
     "A on the 3fx layout, B on the 6fx layout: flipping `skin6FxLayout` "
     "should move the click from A to B"),
    ("fsg-pads", 'forceshow="8pads"', 'forceshow="16pads"',
     "the candidate against the shipped pads value, with no controller attached"),
]

# --- series 4: <onexit>, which needs no click --------------------------------
# `onload` and `oninit` are shipped elements that run script when the skin
# loads; `onexit` is known to the switch and appears nowhere. If it is the
# unload counterpart, its global is still 0 after this skin loads and 1 after
# the NEXT skin replaces it.
EVENTS = [
    ("ev-onexit", '<onexit action="set \'$rc_onexit\' 1"/>', "the candidate"),
    ("ev-control", '<zzonexit action="set \'$rc_zzonexit\' 1"/>',
     "control: nonsense event tag, same shape"),
]

TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!-- reader-candidate probe: {why}
     Generated by tests/Skins/reader-candidates-probe/generate.py — do not hand-edit. -->
<skin name="{name}" version="8" width="900" height="560" author="virtualdj-api-reference">

  <font name="Helvetica Neue"/>
  <nbdecks value="2"/>

  <onload action="set '$rc_onload' 1"/>
  <oninit action="set '$rc_oninit' 1"/>
{events}{root}
  <panel name="main" visible="yes">
    <square color="#11151A">
      <pos x="0" y="0"/>
      <size width="900" height="560"/>
    </square>
    <grabzone x="0" y="0" width="900" height="40"/>

    <textzone>
      <pos x="24" y="12"/>
      <size width="852" height="20"/>
      <text font="arial" size="14" weight="bold" color="#E7EEF7" align="left" format="{name}"/>
    </textzone>

    <!-- BOTTOM button, declared first: it receives the click that the element
         on top of it does not take. -->
    <button action="set '$rc_bottom' 1">
      <pos x="{bx}" y="{by}"/>
      <size width="{bw}" height="{bh}"/>
      <off shape="square" color="#1D4F2A" border="#3FBF63" border_size="3"/>
      <on shape="square" color="#3FBF63" border="#3FBF63" border_size="3"/>
      <text font="arial" size="16" weight="bold" color="#E7EEF7" align="center" format="BOTTOM"/>
    </button>

    <!-- TOP slot, declared last, exactly over BOTTOM. -->
    {open_wrap}{top}
    {close_wrap}

    <textzone>
      <pos x="24" y="{ry}"/>
      <size width="852" height="18"/>
      <text font="arial" size="12" color="#63D2FF" align="left" format="top=`get_var '$rc_top'` bottom=`get_var '$rc_bottom'`"/>
    </textzone>
  </panel>

  <deck deck="1">
    <textzone>
      <pos x="24" y="{dy}"/>
      <size width="400" height="18"/>
      <text font="arial" size="12" color="#93A1B1" align="left" format="deck 1 bpm `get_bpm`"/>
    </textzone>
  </deck>

</skin>
"""

# The TOP button, used by every series except the element one (which puts the
# candidate tag there instead).
TOP_BUTTON = """<button action="set '$rc_top' 1">
      <pos x="{bx}" y="{by}"/>
      <size width="{bw}" height="{bh}"/>
      <off shape="square" color="#4A2350" border="#C46BD8" border_size="3"/>
      <on shape="square" color="#C46BD8" border="#C46BD8" border_size="3"/>
      <text font="arial" size="16" weight="bold" color="#E7EEF7" align="center" format="TOP"/>
      {child}
    </button>"""


MID_BUTTON = """<button action="set '$rc_mid' 1">
      <pos x="{bx}" y="{by}"/>
      <size width="{bw}" height="{bh}"/>
      <off shape="square" color="#4F3D1D" border="#D8A83F" border_size="3"/>
      <on shape="square" color="#D8A83F" border="#D8A83F" border_size="3"/>
      <text font="arial" size="16" weight="bold" color="#E7EEF7" align="center" format="PANEL B"/>
    </button>"""


def png(width: int, height: int, rgb: tuple[int, int, int]) -> bytes:
    """A flat-colour PNG. VirtualDJ refuses a skin folder with no image beside
    the XML ("Impossible to open skin <name>"), so every probe ships two."""
    row = bytes(rgb) * width
    raw = b"".join(b"\x00" + row for _ in range(height))

    def chunk(tag: bytes, body: bytes) -> bytes:
        return (struct.pack(">I", len(body)) + tag + body
                + struct.pack(">I", zlib.crc32(tag + body) & 0xFFFFFFFF))

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def render(variant: str, why: str, *, top: str, wrap: str = "", events: str = "",
           root: str = "") -> tuple[str, str]:
    name = f"{PREFIX} {variant}"
    open_wrap = close_wrap = ""
    if wrap:
        open_wrap, close_wrap = f"<panel {wrap}>".replace(" >", ">") + "\n    ", "\n    </panel>"
    xml = TEMPLATE.format(name=name, why=why, top=top, open_wrap=open_wrap,
                          close_wrap=close_wrap, events=events, root=root, **GEOM)
    return name, "\n".join(line.rstrip() for line in xml.splitlines()) + "\n"


def all_variants():
    """(variant, render kwargs) for every series, in run order."""
    for variant, tag, why in ELEMENTS:
        # The known-element calibration is the only one that can write a global;
        # a candidate tag gets no action, because the point is whether it takes
        # the click at all.
        if tag == "button":
            top = TOP_BUTTON.format(child="", **GEOM)
        else:
            top = ELEMENT_BLOCK.format(tag=tag, **GEOM)
        yield variant, dict(why=why, top=top)
    for variant, tag, why in CONTAINERS:
        yield variant, dict(why=why, top=CONTAINER_BLOCK.format(
            tag=tag, button=TOP_BUTTON.format(child="", **GEOM)))
    for variant, tag, why in BROWSER:
        yield variant, dict(why=why, top=ELEMENT_BLOCK.format(tag=tag, **GEOM))
    for variant, tag, why in ROOTS:
        # nothing in the panel's TOP slot: the candidate is at the root, and the
        # BOTTOM button inside the panel is what the click falls through to.
        yield variant, dict(why=why, top="", root="  " + CONTAINER_BLOCK.format(
            tag=tag, button=TOP_BUTTON.format(child="", **GEOM)) + "\n")
    for variant, child, why, _points in MOUSE:
        yield variant, dict(why=why, top=TOP_BUTTON.format(child=child, **GEOM))
    for variant, attr, why in FORCESHOW:
        yield variant, dict(why=why, top=TOP_BUTTON.format(child="", **GEOM), wrap=attr)
    for variant, a, b, why in GROUPED:
        yield variant, dict(why=why, top=GROUP_PANELS.format(
            a=a, b=b, button_a=TOP_BUTTON.format(child="", **GEOM),
            button_b=MID_BUTTON.format(**GEOM)).replace(" >", ">"))
    for variant, tag, why in EVENTS:
        yield variant, dict(why=why, top=TOP_BUTTON.format(child="", **GEOM),
                            events=f"  {tag}\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--install", action="store_true",
                    help=f"also copy each skin into {INSTALL}")
    ap.add_argument("--uninstall", action="store_true",
                    help="remove the installed copies and stop")
    args = ap.parse_args()

    if args.uninstall:
        for path in sorted(INSTALL.glob(f"{PREFIX} *")):
            shutil.rmtree(path)
            print(f"removed {path}")
        return 0

    for variant, kwargs in all_variants():
        name, xml = render(variant, **kwargs)
        (HERE / f"{variant}.xml").write_text(xml, encoding="utf-8")
        print(f"wrote {variant}.xml")
        if args.install:
            folder = INSTALL / name
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "skin.xml").write_text(xml, encoding="utf-8")
            (folder / "skin.png").write_bytes(png(64, 64, (0x11, 0x15, 0x1A)))
            (folder / "preview.png").write_bytes(png(64, 40, (0x11, 0x15, 0x1A)))
            print(f"  installed {folder.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
