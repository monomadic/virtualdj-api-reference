#!/usr/bin/env python3
"""Prepare and inspect the runtime skin the VDJIntrospectSkin plugin serves.

The plugin's OnGetUserInterface re-reads `skin.xml` and `skin.png` from its work
dir on every call, so this script is the whole authoring side of the loop: write
a skin, ask VirtualDJ to re-open the panel, look at what rendered. No rebuild and
no restart, provided VirtualDJ asks more than once — which is the first thing the
experiment establishes.

    python3 tools/plugin_skin.py prepare            # write skin.png + the probe skin.xml
    python3 tools/plugin_skin.py prepare --xml F    # serve an arbitrary skin instead
    python3 tools/plugin_skin.py log                # skin-related plugin.log lines
    python3 tools/plugin_skin.py --check            # offline self-check (just check)

Read-only with respect to VirtualDJ: this writes files the plugin reads, and
never sends a command.
"""
import argparse
import os
import pathlib
import struct
import sys
import zlib

WORK = pathlib.Path.home() / "Library/Application Support/VirtualDJ/VDJIntrospect"
REPO = pathlib.Path(__file__).resolve().parent.parent
FIXTURES = REPO / "tests" / "Skins" / "runtime-probe"

PANEL_W, PANEL_H = 220, 200
SHEET_W, SHEET_H = 256, 512


def png_bytes(width, height, pixel):
    """Encode an RGBA PNG. stdlib only — no Pillow dependency for `just check`."""
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter type 0 (None)
        for x in range(width):
            raw.extend(pixel(x, y))

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )


def sheet():
    """A sprite sheet laid out the way the SDK example's FX_GUI.png is.

    Band 0 (y < PANEL_H) is the panel background; the band below it is the
    "over/selected" copy the example addresses with `y="+200"` offsets. Colours
    are deliberately flat and distinct so a screenshot says unambiguously whether
    the image was used at all.
    """
    def pixel(x, y):
        if y < PANEL_H:
            return (0x20, 0x20, 0x28, 0xFF)      # panel background: near-black
        if y < 2 * PANEL_H:
            return (0x00, 0x88, 0xCC, 0xFF)      # "+200" band: strong blue
        return (0xCC, 0x22, 0x66, 0xFF)          # anything below: magenta
    return png_bytes(SHEET_W, SHEET_H, pixel)


# The first probe skin. Structure is copied from the SDK's own FX_GUI.xml, which
# is the only known-good example of a plugin skin, so that a failure to render
# points at the delivery path rather than at invented XML. Two readouts:
#   * a literal, which renders even if no VDJScript works at all
#   * a backtick-interpolated `get_deck`, which renders only if the panel
#     evaluates VDJScript the way a real skin does
PROBE_XML = """<Skin name="VDJIntrospectSkin" version="8" width="220" height="200">
    <Copyright>virtualdj-api-reference runtime skin probe</Copyright>

    <textzone>
        <size width="200" height="18"/>
        <pos x="10" y="8"/>
        <text font="arial" size="14" weight="bold" color="#FFFFFF" align="left"
              format="PROBE REV 1"/>
    </textzone>

    <textzone>
        <size width="200" height="18"/>
        <pos x="10" y="32"/>
        <text font="arial" size="13" weight="bold" color="#00CCFF" align="left"
              format="deck=`get_deck`"/>
    </textzone>

    <textzone>
        <size width="200" height="18"/>
        <pos x="10" y="56"/>
        <text font="arial" size="13" weight="bold" color="#00CCFF" align="left"
              action="get_effect_slider_text 1"/>
    </textzone>

    <button action="effect active">
        <tooltip>Activate Effect</tooltip>
        <size width="15" height="15"/>
        <pos x="11" y="90"/>
        <up x="+0" y="+0"/>
        <over x="+0" y="+200"/>
        <selected x="+0" y="+200"/>
        <down x="+0" y="+200"/>
    </button>
</Skin>
"""


def do_prepare(args):
    WORK.mkdir(parents=True, exist_ok=True)
    xml = pathlib.Path(args.xml).read_text() if args.xml else PROBE_XML
    (WORK / "skin.xml").write_text(xml)
    (WORK / "skin.png").write_bytes(sheet())
    print(f"wrote {WORK/'skin.xml'} ({len(xml)} bytes)")
    print(f"wrote {WORK/'skin.png'} ({(WORK/'skin.png').stat().st_size} bytes, "
          f"{SHEET_W}x{SHEET_H})")
    print("The plugin re-reads both on every OnGetUserInterface call — re-open the")
    print("panel (close and show the effect GUI) to pick this up. No restart needed")
    print("IF VirtualDJ asks more than once; `plugin_skin.py log` says whether it did.")


def do_log(args):
    path = WORK / "plugin.log"
    if not path.exists():
        print(f"no log at {path}", file=sys.stderr)
        return 1
    lines = [l.rstrip("\n") for l in path.read_text(errors="replace").splitlines()
             if "[SKIN]" in l or "OnGetUserInterface" in l]
    if not lines:
        print("no OnGetUserInterface activity in the log — VirtualDJ has not asked.")
        return 0
    for l in lines[-args.tail:]:
        print(l)
    calls = sum(1 for l in lines if "OnGetUserInterface CALL" in l)
    print(f"\n{calls} OnGetUserInterface call(s) recorded.")
    return 0


def do_check(args):
    """Offline invariants, so `just check` covers this tool without VirtualDJ."""
    data = sheet()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "PNG signature"
    # Walk the chunk stream and verify every CRC — a malformed sprite sheet would
    # otherwise only show up as a panel that silently fails to render.
    pos, tags = 8, []
    while pos < len(data):
        (n,) = struct.unpack(">I", data[pos:pos + 4])
        tag = data[pos + 4:pos + 8]
        body = data[pos + 4:pos + 8 + n]
        (crc,) = struct.unpack(">I", data[pos + 8 + n:pos + 12 + n])
        assert crc == zlib.crc32(body), f"CRC mismatch in {tag!r}"
        tags.append(tag.decode())
        pos += 12 + n
    assert tags == ["IHDR", "IDAT", "IEND"], tags
    w, h, depth, ctype = struct.unpack(">IIBB", data[16:26])
    assert (w, h, depth, ctype) == (SHEET_W, SHEET_H, 8, 6), (w, h, depth, ctype)

    # The probe skin must be well-formed enough for the repo's own skin linter to
    # be able to read it; built-in skin XML often is not, but ours should be.
    import xml.etree.ElementTree as ET
    root = ET.fromstring(PROBE_XML)
    assert root.tag == "Skin", root.tag
    assert root.get("width") == str(PANEL_W) and root.get("height") == str(PANEL_H)

    print(f"plugin skin check passed: {len(data)} byte PNG {w}x{h} RGBA, "
          f"probe skin {len(PROBE_XML)} bytes, {len(list(root))} top-level elements")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="offline self-check")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("prepare", help="write skin.xml and skin.png")
    p.add_argument("--xml", help="serve this file instead of the built-in probe skin")
    p = sub.add_parser("log", help="show OnGetUserInterface activity")
    p.add_argument("--tail", type=int, default=40)
    sub.add_parser("check", help="offline self-check")
    args = ap.parse_args()

    if args.check or args.cmd == "check":
        return do_check(args)
    if args.cmd == "prepare":
        return do_prepare(args)
    if args.cmd == "log":
        return do_log(args)
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
