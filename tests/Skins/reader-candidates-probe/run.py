#!/usr/bin/env python3
"""Run the reader-candidate probe against a live VirtualDJ.

Each variant is loaded, its globals reset over HTTP, clicked once at a named
point by a CGEvent helper, and both globals read back — so what a variant did
is a value, not a judgement about a screenshot.

The helper is compiled here rather than committed: macOS has no click CLI and
this machine has no PyObjC, and a 30-line Swift source next to the probe that
uses it keeps the fixture reproducible from the repo alone.

    python3 tests/Skins/reader-candidates-probe/generate.py --install
    python3 tests/Skins/reader-candidates-probe/run.py --calibrate
    python3 tests/Skins/reader-candidates-probe/run.py --series elements
    python3 tests/Skins/reader-candidates-probe/run.py --series all --reverse

Coordinates: the probe skins declare 900x560 and VirtualDJ scales the skin to
the window, so a skin coordinate reaches the screen as `origin + skin * scale`.
`--calibrate` clicks the known-element variant and reports whether the mapping
in force actually lands on it; do not run a series whose calibration failed.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from generate import (BROWSER, CENTRE, CONTAINERS, CORNER,  # noqa: E402
                      ELEMENTS, EVENTS,
                      FORCESHOW, GROUPED, MOUSE, POINTS, PREFIX, ROOTS)

BASE = "http://localhost"
HELPER_SRC = """import CoreGraphics
import Foundation
let a = CommandLine.arguments
guard a.count >= 3, let x = Double(a[1]), let y = Double(a[2]) else { exit(2) }
let p = CGPoint(x: x, y: y)
let src = CGEventSource(stateID: .hidSystemState)
CGEvent(mouseEventSource: src, mouseType: .mouseMoved, mouseCursorPosition: p,
        mouseButton: .left)?.post(tap: .cghidEventTap)
usleep(120_000)
let down = CGEvent(mouseEventSource: src, mouseType: .leftMouseDown,
                   mouseCursorPosition: p, mouseButton: .left)
let up = CGEvent(mouseEventSource: src, mouseType: .leftMouseUp,
                 mouseCursorPosition: p, mouseButton: .left)
// Explicit empty flags: a modifier left over from an earlier event is
// inherited by these, and VirtualDJ then swallows the click.
down?.flags = []
up?.flags = []
down?.post(tap: .cghidEventTap)
usleep(60_000)
up?.post(tap: .cghidEventTap)
usleep(120_000)
"""


def http(path: str, script: str, tries: int = 3) -> str:
    """One HTTP leg, retried: loading a skin occasionally stalls the interface
    for a few seconds, and a timeout there is not a result."""
    url = f"{BASE}/{path}?" + urllib.parse.urlencode({"script": script})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=15) as fh:
                return fh.read().decode("utf-8", "replace").strip()
        except (TimeoutError, OSError):
            if attempt == tries - 1:
                raise
            time.sleep(2.0)
    raise AssertionError("unreachable")


def query(script: str) -> str:
    return http("query", script)


def execute(script: str) -> str:
    return http("execute", script)


def helper(cache: Path) -> Path:
    binary = cache / "vdjclick"
    source = cache / "vdjclick.swift"
    if not binary.exists():
        cache.mkdir(parents=True, exist_ok=True)
        source.write_text(HELPER_SRC, encoding="utf-8")
        subprocess.run(["swiftc", "-O", "-o", str(binary), str(source)], check=True)
    return binary


class Probe:
    def __init__(self, args):
        self.origin = tuple(float(v) for v in args.origin.split(","))
        self.scale = args.scale
        self.click_binary = helper(Path(args.cache))
        self.settle = args.settle

    def point(self, skin_xy: tuple[int, int]) -> tuple[float, float]:
        return (self.origin[0] + skin_xy[0] * self.scale,
                self.origin[1] + skin_xy[1] * self.scale)

    def click(self, skin_xy: tuple[int, int]) -> None:
        x, y = self.point(skin_xy)
        subprocess.run([str(self.click_binary), f"{x:.0f}", f"{y:.0f}"], check=True)

    def load(self, variant: str) -> bool:
        name = f"{PREFIX} {variant}"
        execute(f"load_skin '{name}/:skin'")
        time.sleep(self.settle)
        return query("load_skin") == f"{name}/:skin"

    def reset(self) -> None:
        for var in ("$rc_top", "$rc_bottom", "$rc_onload", "$rc_oninit",
                    "$rc_onexit", "$rc_zzonexit", "$rc_mid"):
            execute(f"set '{var}' 0")

    def globals(self) -> dict:
        return {name: query(f"get_var '${name}'")
                for name in ("rc_top", "rc_mid", "rc_bottom")}

    def run_click(self, variant: str, where: str, skin_xy: tuple[int, int]) -> dict:
        loaded = self.load(variant)
        self.reset()
        self.click(skin_xy)
        time.sleep(0.4)
        row = {"variant": variant, "click": where, "loaded": loaded}
        row.update(self.globals())
        return row


def series_rows(name: str):
    """(variant, click-name, skin point) for one series, in file order."""
    if name in ("elements", "all"):
        for variant, _tag, _why in ELEMENTS:
            yield variant, "centre", CENTRE
    if name in ("containers", "all"):
        for variant, _tag, _why in CONTAINERS:
            yield variant, "centre", CENTRE
    if name in ("browser", "all"):
        for variant, _tag, _why in BROWSER:
            yield variant, "centre", CENTRE
    if name in ("roots", "all"):
        for variant, _tag, _why in ROOTS:
            yield variant, "centre", CENTRE
    if name in ("grouped", "all"):
        for variant, _a, _b, _why in GROUPED:
            yield variant, "centre", CENTRE
    if name in ("mouse", "all"):
        for variant, _child, _why, points in MOUSE:
            for where in points:
                yield variant, where, POINTS[where]
    if name in ("forceshow", "all"):
        for variant, _attr, _why in FORCESHOW:
            yield variant, "centre", CENTRE


def run_events(probe: Probe) -> list[dict]:
    """`<onexit>` needs no click: load the probe, read (it must not have fired
    yet), load the next skin, read again (it fires on unload, or never)."""
    rows = []
    for variant, _tag, _why in EVENTS:
        probe.reset()
        loaded = probe.load(variant)
        during = {n: query(f"get_var '${n}'")
                  for n in ("rc_onload", "rc_oninit", "rc_onexit", "rc_zzonexit")}
        probe.load("el-button")           # replace it: this is the unload event
        after = {n: query(f"get_var '${n}'")
                 for n in ("rc_onload", "rc_oninit", "rc_onexit", "rc_zzonexit")}
        rows.append({"variant": variant, "loaded": loaded,
                     "while_loaded": during, "after_replaced": after})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--series", default="all",
                    choices=["all", "elements", "containers", "browser", "roots", "mouse",
                             "forceshow", "grouped", "events"])
    ap.add_argument("--reverse", action="store_true",
                    help="run the rows back to front; a result that only holds "
                         "in one order is an ordering artifact")
    ap.add_argument("--origin", default="0,0", help="screen point of skin (0,0)")
    ap.add_argument("--scale", type=float, default=1.6,
                    help="screen points per skin unit")
    ap.add_argument("--settle", type=float, default=0.8,
                    help="seconds to wait after a skin load")
    ap.add_argument("--cache", default="/tmp/vdj-probe-helper",
                    help="where the compiled click helper is kept")
    ap.add_argument("--calibrate", action="store_true",
                    help="click the known-element variant and report only that")
    ap.add_argument("--out", help="write the rows as JSON here as well")
    args = ap.parse_args()

    subprocess.run(["osascript", "-e",
                    'tell application "VirtualDJ" to activate'], check=False)
    time.sleep(1.0)
    probe = Probe(args)

    if args.calibrate:
        row = probe.run_click("el-button", "centre", CENTRE)
        ok = row["loaded"] and row["rc_top"] == "1" and row["rc_bottom"] == "0"
        print(json.dumps(row))
        print("calibration OK" if ok else
              "calibration FAILED: the click did not land on the known element "
              "— fix --origin/--scale before reading any other row")
        return 0 if ok else 1

    if args.series == "events":
        rows = run_events(probe)
        for row in rows:
            print(json.dumps(row))
    else:
        rows = list(series_rows(args.series))
        if args.reverse:
            rows.reverse()
        out = []
        for variant, where, xy in rows:
            row = probe.run_click(variant, where, xy)
            out.append(row)
            print(f"{row['variant']:<18} {row['click']:<7} "
                  f"loaded={str(row['loaded']):<5} "
                  f"top={row['rc_top']:<3} mid={row['rc_mid']:<3} "
                  f"bottom={row['rc_bottom']}")
        rows = out

    if args.out:
        Path(args.out).write_text(json.dumps(rows, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
