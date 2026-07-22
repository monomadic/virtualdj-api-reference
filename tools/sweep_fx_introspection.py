#!/usr/bin/env python3
"""Sweep VirtualDJ's native deck-FX catalog over the HTTP control interface.

Two passes into deck-FX slot 1:
  A. Cycle `effect_select 1 +1` until the name wraps -> the ENABLED/favorites list.
  B. By-name `effect_select 1 '<name>'` over the documented catalog union -> the full
     installed set reachable by name. A 'Dump' sentinel before each attempt detects
     names that fail to load into an audio slot (e.g. video-only effects).

Non-destructive: reads structure/labels/current values only; no slider resets. Leaves
slot 1 on the last selected effect. Emits a merged JSON dump to stdout; per-effect
`reached` records whether it was in the cycle, reachable by name, and which asked
spellings resolved to it. Bootstrap input for the verb store.
"""
import json
import sys
import time
import urllib.parse
import urllib.request

BASE = "http://localhost"
SLOT = "1"
SAFETY_CAP = 300
SENTINEL = "Dump"  # installed, 0 sliders/buttons, harmless park state


SETTLE = 0.06  # seconds to let a select settle before reading back


def call(endpoint, script, retries=4):
    url = f"{BASE}/{endpoint}?" + urllib.parse.urlencode({"script": script})
    last = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=8) as r:
                return r.read().decode("utf-8", "replace").strip()
        except Exception as e:  # noqa: BLE001 - transient interface stalls
            last = e
            time.sleep(0.25 * (attempt + 1))
    raise RuntimeError(f"call failed after {retries} tries: {script!r}: {last}")


def q(script):
    return call("query", script)


def x(script):
    out = call("execute", script)
    if script.startswith("effect_select"):
        time.sleep(SETTLE)
    return out


def to_int(s, default=0):
    try:
        return int(s)
    except (ValueError, TypeError):
        return default


def introspect_current():
    name = q(f"get_effect_name {SLOT}")
    slider_count = to_int(q(f"get_effect_slider_count {SLOT}"))
    button_count = to_int(q(f"get_effect_button_count {SLOT}"))
    sliders = []
    for i in range(1, slider_count + 1):
        sliders.append({
            "index": i,
            "has": q(f"effect_has_slider {SLOT} {i}"),
            "short": q(f"get_effect_slider_label {SLOT} {i}"),
            "full": q(f"get_effect_slider_label_full {SLOT} {i}"),
            "name": q(f"get_effect_slider_name {SLOT} {i}"),
            "text": q(f"get_effect_slider_text {SLOT} {i}"),
        })
    buttons = []
    for i in range(1, button_count + 1):
        buttons.append({
            "index": i,
            "has": q(f"effect_has_button {SLOT} {i}"),
            "short": q(f"get_effect_button_shortname {SLOT} {i}"),
        })
    return {
        "effect": name,
        "slider_count": slider_count,
        "button_count": button_count,
        "sliders": sliders,
        "buttons": buttons,
    }


# Documented catalog union (from docs/Native Effects.md), audio + video mixed.
CATALOG = [
    "Additive", "BackSpin", "Beat Brake", "BeatGrid", "Blinds", "Blur",
    "Blur Black Bars", "Boom", "Boom Auto", "Brake", "BrakeStart", "Camera",
    "Cloud Dissolve", "Color Swap", "Colorize", "Cover", "Cube", "Cut", "Cyclone",
    "Distortion", "Doors", "Down Echo", "Drain", "Drain Light", "Droplets",
    "Ducking Echo", "Echo", "Extreme Cut", "Fade", "Filter", "Fixed Grid",
    "Flanger", "Flippin Double", "Helix", "Hold Echo", "Karaoke", "LFO Filter",
    "Loop Out", "Loop Roll", "Lottery", "Low Cut Echo", "Lyrics", "Matrix",
    "MergeFX", "Mobius", "Mobius Saw", "Mobius Tri", "MT Delay", "Mute",
    "Negative", "Noise", "Pan", "Phaser", "Ping Pong", "Pitch", "Pitch Down",
    "Pitch Echo", "Pumper", "Recycler", "Rev Delay", "Reverb", "Rider", "Riser",
    "Scale Down", "Scratch DNA", "Screen Grab", "Shader", "Shake", "Slicer",
    "Slideshow", "Slip Roll", "Spectral", "Spiral", "Stems", "Stretch", "Strobe",
    "Stutter Out", "Sweep", "Text", "Title", "Up Echo", "VinylBrake", "Vocals",
    "Wahwah",
]


def cycle_pass():
    x(f"effect_select {SLOT} 'Backspin'")
    start = q(f"get_effect_name {SLOT}")
    order = []
    seen = set()
    current = start
    steps = 0
    while steps < SAFETY_CAP:
        if current in seen:
            break
        seen.add(current)
        order.append(current)
        print(f"  cycle[{len(order):3}] {current}", file=sys.stderr)
        x(f"effect_select {SLOT} +1")
        current = q(f"get_effect_name {SLOT}")
        steps += 1
        time.sleep(0.02)
    return order


def main():
    build = q("get_version")

    print("Pass A: cycling enabled list...", file=sys.stderr)
    cycle_order = cycle_pass()
    cycle_set = set(cycle_order)

    print("Pass B: by-name over catalog union...", file=sys.stderr)
    # data keyed by resolved effect name -> merged entry
    data = {}

    def record(entry, *, in_cycle, asked=None):
        name = entry["effect"]
        if name not in data:
            data[name] = entry
            data[name]["reached"] = {
                "in_cycle": False, "by_name": False, "name_requests": [],
            }
        d = data[name]["reached"]
        if in_cycle:
            d["in_cycle"] = True
        if asked is not None:
            d["by_name"] = True
            if asked not in d["name_requests"]:
                d["name_requests"].append(asked)

    # seed cycle results with a fresh introspection pass (deterministic order)
    for nm in cycle_order:
        x(f"effect_select {SLOT} '{nm}'")
        if q(f"get_effect_name {SLOT}") != nm:
            # selection by exact cycle name failed; skip re-introspect, still mark
            record({"effect": nm, "slider_count": None, "button_count": None,
                    "sliders": [], "buttons": [], "reintrospect_failed": True},
                   in_cycle=True)
            continue
        record(introspect_current(), in_cycle=True)

    # Exclude the sentinel itself: selecting Dump-onto-Dump reads back as Dump and
    # would be a false "did not load". Dump is already captured via the cycle pass.
    candidates = [n for n in dict.fromkeys(CATALOG + cycle_order) if n != SENTINEL]
    failed_by_name = []
    for asked in candidates:
        x(f"effect_select {SLOT} '{SENTINEL}'")
        if q(f"get_effect_name {SLOT}") != SENTINEL:
            print(f"  ! sentinel park failed before '{asked}'", file=sys.stderr)
        x(f"effect_select {SLOT} '{asked}'")
        got = q(f"get_effect_name {SLOT}")
        if got == SENTINEL:
            failed_by_name.append(asked)
            print(f"  name '{asked}' -> did not load (video-only or absent)",
                  file=sys.stderr)
            continue
        record(introspect_current(), in_cycle=got in cycle_set, asked=asked)
        note = "" if got.lower().replace(" ", "") == asked.lower().replace(" ", "") \
            else f"  (resolved to '{got}')"
        print(f"  name '{asked}' -> {got}{note}", file=sys.stderr)
        time.sleep(0.02)

    effects = sorted(data.values(), key=lambda e: e["effect"].lower())
    dump = {
        "source": "HTTP control interface (localhost)",
        "channel": "execute effect_select (cycle +1 and by-name) + query introspection",
        "vdj_version": build,
        "slot": int(SLOT),
        "cycle_enabled_count": len(cycle_order),
        "cycle_order": cycle_order,
        "installed_reachable_count": len(effects),
        "failed_by_name": failed_by_name,
        "note": "Pass A cycled the enabled/favorites list (effect_select +1). Pass B added "
                "by-name catalog entries. 'failed_by_name' did not load into an audio deck-FX "
                "slot (video-only or not installed). Slider text is live value, not reset/default; "
                "labels and counts are state-independent. Names are installed selector names.",
        "effects": effects,
    }
    json.dump(dump, sys.stdout, indent=2, ensure_ascii=False)
    print(file=sys.stdout)
    print(f"\nDone: {len(effects)} reachable, {len(failed_by_name)} failed by-name, "
          f"{len(cycle_order)} in cycle.", file=sys.stderr)


if __name__ == "__main__":
    main()
