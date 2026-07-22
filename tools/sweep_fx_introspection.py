#!/usr/bin/env python3
"""Sweep VirtualDJ's installed effect catalog over the HTTP control interface.

Key discovery driving this version: every `get_effect_*` introspection helper
accepts an effect NAME where the docs show a slot number --
`get_effect_slider_count 'Echo'`, `get_effect_slider_default 'Echo' 3`, etc.
Structure, labels, and defaults therefore come out of a purely READ-ONLY pass
with no `effect_select` at all. Selection is needed only to answer "which
targets accept this effect", which is a separate question from "what controls
does it have".

`get_effect_title '<name>'` returns `'<Canonical> - Deck N'` for an installed
effect and `''` for an unknown one, so it mostly doubles as an existence probe
and a name resolver (it accepts at least one alias that `effect_select` rejects:
`Shader` -> `Visuals`). Matching is case-insensitive but NOT space-insensitive
(`BeatGrid` misses `Beat Grid`). It has a blind spot: `Stems` and `Vocals` select
fine and introspect fine through a SLOT, but the name form reports nothing for
them -- so a title miss is confirmed by actually selecting the name before it is
called unknown, and those effects are read through the slot instead.

Category comes from cycle membership, NOT from what a target accepts: all three
selectors accept any installed effect name (`video_fx_select 'Echo'` really does
set the video slot to Echo), so loadability discriminates nothing. The three
`+1` cycles are disjoint and are the app's own category assignment.

Passes:
  A. Cycle each of the three targets (`effect_select 1 +1`, `video_fx_select +1`,
     `video_transition_select +1`) -- these enumerate the ENABLED/favorites list
     per target, not the full installed set.
  B. Resolve every asked name (docs catalog + all three cycles) to its canonical
     installed name via `get_effect_title`, falling back to a select probe.
  C. Introspection per canonical effect: counts, short/full labels, normalized
     DEFAULTS, live value text, length/beats flags, button names. Read-only via
     the name form; via the slot for the title-blind-spot names.

Restores the video-FX and transition selections it changed; leaves the deck slot
parked on the sentinel. Emits JSON to stdout.
"""
import json
import sys
import time
import urllib.parse
import urllib.request

BASE = "http://localhost"
SLOT = "1"
SAFETY_CAP = 300
SETTLE = 0.06  # seconds to let a select settle before reading back

# Park states used to detect "asked for X, nothing loaded". Each target needs a
# park value that is itself installed; the sweep skips the probe when the asked
# name IS the park value (selecting X onto X reads back as X and would look like
# a non-load).
DECK_PARK = "Dump"          # installed, 0 sliders/buttons, harmless
VIDEO_PARK = "Cover"
TRANS_PARK = "None"


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
    return call("execute", script)


def to_int(s, default=0):
    try:
        return int(s)
    except (ValueError, TypeError):
        return default


def esc(name):
    """VDJScript single-quoted argument. No installed effect name contains a quote."""
    return name.replace("'", "")


# Documented catalog union (docs/Native Effects.md), audio + video mixed. Names
# that do not resolve are reported in `unresolved_names` rather than dropped --
# a name in the docs that the app does not know is itself a finding.
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

def cycle(select, readback, label):
    """Walk a target's `+1` list until it wraps. Returns the order seen."""
    order, seen = [], set()
    current = q(readback)
    for _ in range(SAFETY_CAP):
        if current in seen:
            break
        seen.add(current)
        order.append(current)
        x(f"{select} +1")
        time.sleep(SETTLE)
        current = q(readback)
    print(f"  {label}: {len(order)}", file=sys.stderr)
    return order


def deck_select(name):
    """Park, then select `name` into the deck slot. Returns the readback name."""
    x(f"effect_select {SLOT} '{esc(DECK_PARK)}'")
    time.sleep(SETTLE)
    x(f"effect_select {SLOT} '{esc(name)}'")
    time.sleep(SETTLE)
    return q(f"get_effect_name {SLOT}")


def resolve(name):
    """Canonical installed name for `name`, plus how it was resolved.

    Returns (canonical, method) or (None, None). `get_effect_title` answers most
    names without touching app state; a title miss is re-checked by selecting the
    name, because Stems/Vocals are installed but title-invisible.
    """
    title = q(f"get_effect_title '{esc(name)}'")
    if title:
        head, sep, _ = title.rpartition(" - Deck ")
        return (head if sep else title), "title"
    got = deck_select(name)
    if got and got != DECK_PARK:
        return got, "select"
    return None, None


def introspect(name, via):
    """Control map for an installed effect.

    `via` is the introspection subject: the quoted effect name (no state change)
    or the slot number, for effects the name form cannot see. Slot-form callers
    must have the effect loaded already.
    """
    slider_count = to_int(q(f"get_effect_slider_count {via}"))
    button_count = to_int(q(f"get_effect_button_count {via}"))
    sliders = []
    for i in range(1, slider_count + 1):
        sliders.append({
            "index": i,
            "has": q(f"effect_has_slider {via} {i}"),
            "short": q(f"get_effect_slider_label {via} {i}"),
            "full": q(f"get_effect_slider_label_full {via} {i}"),
            "default": q(f"get_effect_slider_default {via} {i}"),
            "text": q(f"get_effect_slider_text {via} {i}"),
            # the i-th slider of the list with the length slider REMOVED --
            # a re-index, not a blank; the last entry falls off the end
            "skip_length_label": q(f"get_effect_slider_label_skip_length {via} {i}"),
        })
    buttons = []
    for i in range(1, button_count + 1):
        buttons.append({
            "index": i,
            "has": q(f"effect_has_button {via} {i}"),
            "short": q(f"get_effect_button_shortname {via} {i}"),
            "full": q(f"get_effect_button_name {via} {i}"),
        })
    # The length slider is wherever the plain and skip-length labels diverge.
    # It is not always slider 2 (Loop Out, Slideshow put it first) and is not
    # always labelled LEN (Phaser and Wahwah label it SPD).
    length_index = next(
        (s["index"] for s in sliders if s["short"] != s["skip_length_label"]), None)
    return {
        "effect": name,
        "slider_count": slider_count,
        "button_count": button_count,
        "has_length": q(f"effect_has_length {via}"),
        "has_beats": q(f"effect_has_beats {via}"),
        "length_slider_index": length_index,
        "sliders": sliders,
        "buttons": buttons,
    }


def main():
    build = q("get_version")
    orig_video = q("get_videofx_name")
    orig_trans = q("get_videotrans_name")

    print("Pass A: cycling each target's enabled list...", file=sys.stderr)
    x(f"effect_select {SLOT} '{DECK_PARK}'")
    time.sleep(SETTLE)
    cycles = {
        "deck_fx": cycle(f"effect_select {SLOT}", f"get_effect_name {SLOT}", "deck_fx"),
        "video_fx": cycle("video_fx_select", "get_videofx_name", "video_fx"),
        "transition": cycle("video_transition_select", "get_videotrans_name",
                            "transition"),
    }
    x(f"video_fx_select '{esc(orig_video)}'")
    x(f"video_transition_select '{esc(orig_trans)}'")
    time.sleep(SETTLE)

    print("Pass B: resolving names...", file=sys.stderr)
    asked_names = list(dict.fromkeys(
        CATALOG + cycles["deck_fx"] + cycles["video_fx"] + cycles["transition"]))
    canonical = {}       # canonical name -> {"asked": set, "method": str}
    unresolved = []
    for asked in asked_names:
        got, method = resolve(asked)
        if got is None:
            unresolved.append(asked)
            print(f"  '{asked}' -> not installed", file=sys.stderr)
            continue
        rec = canonical.setdefault(got, {"asked": set(), "method": method})
        rec["asked"].add(asked)
        if method == "select":  # a title miss is the stronger fact; keep it
            rec["method"] = "select"
        if got != asked:
            print(f"  '{asked}' -> '{got}' (via {method})", file=sys.stderr)
    names = sorted(canonical, key=str.lower)
    print(f"  {len(names)} installed, {len(unresolved)} unresolved", file=sys.stderr)

    print("Pass C: introspection...", file=sys.stderr)
    data = {}
    for i, name in enumerate(names, 1):
        rec = canonical[name]
        if rec["method"] == "title":
            entry = introspect(name, f"'{esc(name)}'")
        else:
            # name form is blind to this effect; load it and read the slot
            if deck_select(name) != name:
                print(f"  [{i:3}/{len(names)}] {name}: SKIPPED (would not reload)",
                      file=sys.stderr)
                continue
            entry = introspect(name, SLOT)
        entry["introspected_via"] = rec["method"]
        entry["aliases"] = sorted(a for a in rec["asked"] if a != name)
        entry["cycles"] = [k for k, v in cycles.items() if name in v]
        entry["category"] = entry["cycles"][0] if entry["cycles"] else None
        entry["reached"] = {
            "in_cycle": name in cycles["deck_fx"],
            "by_name": True,
            "name_requests": entry["aliases"],
        }
        data[name] = entry
        print(f"  [{i:3}/{len(names)}] {name}: "
              f"{entry['slider_count']}s/{entry['button_count']}b "
              f"[{entry['category'] or 'uncategorised'}]", file=sys.stderr)

    x(f"effect_select {SLOT} '{esc(DECK_PARK)}'")
    x(f"video_fx_select '{esc(orig_video)}'")
    x(f"video_transition_select '{esc(orig_trans)}'")
    time.sleep(SETTLE)

    effects = [data[n] for n in names if n in data]
    dump = {
        "source": "HTTP control interface (localhost)",
        "channel": "read-only get_effect_* name-form introspection + per-target "
                   "select probes",
        "vdj_version": build,
        "slot": int(SLOT),
        "cycle_enabled_count": len(cycles["deck_fx"]),
        "cycle_order": cycles["deck_fx"],
        "cycles": cycles,
        "installed_reachable_count": len(effects),
        "unresolved_names": unresolved,
        "failed_by_name": [],
        "note": "Every get_effect_* helper accepts an effect NAME in place of the slot "
                "number, so counts, labels, defaults, and value text are read WITHOUT "
                "selecting anything; verified identical to the slot form for all "
                "title-resolvable effects. get_effect_title '<name>' returns the "
                "canonical installed name (case-insensitive, NOT space-insensitive: "
                "'BeatGrid' misses 'Beat Grid') and '' for unknown names -- but it is "
                "blind to Stems/Vocals, which select and introspect normally through a "
                "slot, so a title miss is re-checked by selecting and those effects are "
                "read via 'introspected_via':'select'. 'unresolved_names' did not "
                "resolve either way: names this build does not know. 'category' comes "
                "from cycle membership, not from loadability: all three selectors accept "
                "any installed effect name (video_fx_select 'Echo' really does set the "
                "video slot to Echo), so what a target accepts discriminates nothing. "
                "The three '+1' cycles are disjoint and are the app's own category "
                "assignment, but each is the ENABLED/favorites subset -- an installed "
                "effect in no cycle is category-unknown, not uncategorised by the app. "
                "Slider 'default' is the normalized reset value (0..1); 'text' is the "
                "current live value, not a default. The *_skip_length helpers RE-INDEX "
                "rather than blank: 'skip_length_label' at index i is the i-th slider of "
                "the list with the length slider removed, so the last entry is always ''. "
                "'length_slider_index' is where that divergence starts -- not always "
                "slider 2 (Loop Out and Slideshow put it first) and not always labelled "
                "LEN (Phaser and Wahwah label it SPD).",
        "effects": effects,
    }
    json.dump(dump, sys.stdout, indent=2, ensure_ascii=False)
    print(file=sys.stdout)
    print(f"\nDone: {len(effects)} installed, {len(unresolved)} unresolved names, "
          f"deck-cycle {len(cycles['deck_fx'])}, video-cycle {len(cycles['video_fx'])}, "
          f"transition-cycle {len(cycles['transition'])}.", file=sys.stderr)


if __name__ == "__main__":
    main()
