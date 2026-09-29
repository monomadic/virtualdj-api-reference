#!/usr/bin/env python3
"""Screenshot the VirtualDJ window (macOS).

Finds the largest on-screen layer-0 window owned by VirtualDJ through
CoreGraphics (via osascript/JXA, so no pyobjc) and captures just that window
with `screencapture -l`. Needs Screen Recording permission for the calling
terminal/app; without it macOS captures a blank desktop, which this reports.

    python3 tools/vdj_screenshot.py [--out PATH] [--owner NAME] [--list]

Default output is tests/screenshots/virtualdj-<timestamp>.png — a UI
observation must persist what it saw (CLAUDE.md), so cite that path as evidence.
Prints the written path on stdout.
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

JXA = """
ObjC.import("CoreGraphics");
var l = ObjC.deepUnwrap(ObjC.castRefToObject($.CGWindowListCopyWindowInfo(1, 0)));
JSON.stringify(l.map(w => ({owner: w.kCGWindowOwnerName, id: w.kCGWindowNumber,
  layer: w.kCGWindowLayer, name: w.kCGWindowName || "",
  w: w.kCGWindowBounds.Width, h: w.kCGWindowBounds.Height})))
"""


def windows(owner):
    r = subprocess.run(["osascript", "-l", "JavaScript", "-e", JXA],
                       capture_output=True, text=True, timeout=15)
    if r.returncode != 0:
        sys.exit(f"window enumeration failed: {r.stderr.strip()}")
    return [w for w in json.loads(r.stdout)
            if w["owner"] and owner.lower() in w["owner"].lower() and w["layer"] == 0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--owner", default="VirtualDJ")
    ap.add_argument("--list", action="store_true", help="list candidate windows and exit")
    a = ap.parse_args()

    if sys.platform != "darwin":
        sys.exit("macOS only")
    ws = windows(a.owner)
    if a.list:
        for w in ws:
            print(f"{w['id']}\t{int(w['w'])}x{int(w['h'])}\t{w['name']!r}")
        return
    if not ws:
        sys.exit(f"no on-screen {a.owner} window (is it running, and not minimized?)")
    win = max(ws, key=lambda w: w["w"] * w["h"])

    out = Path(a.out) if a.out else REPO / "tests" / "screenshots" / time.strftime("virtualdj-%Y%m%d-%H%M%S.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["screencapture", "-x", "-o", "-l", str(win["id"]), str(out)],
                       capture_output=True, text=True, timeout=20)
    if r.returncode != 0 or not out.exists():
        sys.exit(f"screencapture failed: {r.stderr.strip() or r.returncode} "
                 "(grant Screen Recording to the calling app)")
    print(out)


if __name__ == "__main__":
    main()
