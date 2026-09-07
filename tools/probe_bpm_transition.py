#!/usr/bin/env python3
"""Discriminate `auto_bpm_transition`'s three documented parameters.

The arg-form sweep and the execute-position pass both reported these tokens
behaving like nonsense, and the tracker first recorded that as a negative. It
was not one: the observable both probes had was a boolean saying whether a
transition is *running*, and what the parameters change is which BPM it lands
on. A verb whose argument is invisible to the observable is not a verb with no
argument — read `tail-ignored-in-execute` as "not visible in this observable".

The state this needs is three distinct landmarks, which no fixture builds:

    deck 1 (source)  100 BPM track, pitch 0    -> current 100 == its original
    deck 2 (target)  120 BPM track, `pitch 132 bpm` -> current 132, original 120

so `source_original` (100), `target_original` (120) and `target_current` (132)
are three different numbers, and where both decks settle says which one the
verb was told to use. Two nonsense controls run beside them: an ignored tail
lands where the bare form lands, and that is what a real token must differ from.

    python3 tools/probe_bpm_transition.py --run > tests/bpm-transition-forms.json
    python3 tools/probe_bpm_transition.py --check

The run loads generated fixture tracks on decks 1 and 2 and leaves both decks
STOPPED — the transition runs on a stopped deck, so this makes no sound — then
restores both decks' contents and pitch.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixtures import (  # noqa: E402
    AUDIO_DIR, AUDIO_EXPR, Channel, FixtureError, deck_state, ensure_audio,
    restore_deck,
)

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "tests" / "bpm-transition-forms.json"

SOURCE, TARGET = 1, 2
SOURCE_BPM, TARGET_BPM, TARGET_PITCHED = 100.0, 120.0, 132.0
SECOND_TRACK = "fixture-100bpm.wav"
SECOND_EXPR = AUDIO_EXPR.replace("0.5", "0.6")   # 0.6 s period == 100 BPM
SETTLE_TIMEOUT = 25.0
SETTLE_STABLE = 3          # consecutive equal reads that count as settled
SETTLE_MIN = 4.0           # watch at least this long: a form that lands where
                           # the deck already sits is stable from the first read

# (form, why). The junk tails are the floor: whatever they do is what "the tail
# was not read" looks like in this observable.
FORMS = [
    ("", "floor: the default landing point"),
    ("source_original", "documented: force the source deck's original BPM"),
    ("target_original", "documented: force the target deck's original BPM"),
    ("target_current", "documented: force the target deck's current BPM"),
    ("all", "the token the execute-position sweep found on this verb"),
    ("zzqqx", "nonsense control 1"),
    ("vfnrbq", "nonsense control 2"),
]

LANDMARKS = {
    "source_original": SOURCE_BPM,
    "target_original": TARGET_BPM,
    "target_current": TARGET_PITCHED,
}


def second_track() -> Path:
    """The 100 BPM counterpart of the shared fixture track.

    `fixtures.py` generates one tempo, and one tempo cannot separate a source
    original from a target original — both would be 120.
    """
    path = AUDIO_DIR / SECOND_TRACK
    if path.exists():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y",
         "-f", "lavfi", "-i", f"aevalsrc=exprs={SECOND_EXPR}:d=90:s=44100",
         "-ac", "2", str(path)],
        check=True)
    return path


def num(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def establish(ch: Channel, src_track: Path, tgt_track: Path) -> dict:
    """Build the three-landmark state and assert every one of them."""
    # The verb is a TOGGLE: a form that leaves a transition engaged makes the
    # next form stop it instead of starting one, and that form then measures
    # nothing while looking like a settled result. `target_current` does leave
    # it engaged, which is how this was found — run-2's `target_original` read
    # as "did not move" purely because it followed `target_current`.
    for _ in range(12):
        if ch.query(f"deck {SOURCE} auto_bpm_transition") != "yes":
            break
        ch.execute(f"deck {SOURCE} auto_bpm_transition")
        time.sleep(1.0)
    else:
        raise FixtureError("a transition is still running and will not stop; "
                           "the next form would toggle it off instead of "
                           "starting one")

    ch.execute(f'deck {SOURCE} load "{src_track}"')
    ch.execute(f'deck {TARGET} load "{tgt_track}"')
    time.sleep(3.0)
    ch.execute(f"deck {SOURCE} pitch 100%")
    ch.execute(f"deck {TARGET} pitch {TARGET_PITCHED:g} bpm")
    time.sleep(1.0)
    state = {
        "source_current": num(ch.query(f"deck {SOURCE} get_bpm")),
        "transition_running_before": ch.query(f"deck {SOURCE} auto_bpm_transition"),
        "source_original": num(ch.query(f"deck {SOURCE} get_bpm 'absolute'")),
        "target_current": num(ch.query(f"deck {TARGET} get_bpm")),
        "target_original": num(ch.query(f"deck {TARGET} get_bpm 'absolute'")),
    }
    # Only the three LANDMARKS are asserted. The source's *current* BPM is
    # recorded, not required: with the app's BPM matching on, setting either
    # deck's pitch drags the other, so the source cannot be held at its own
    # original while the target sits pitched. That does not matter — the
    # landmarks are what a landing is read against, and they are properties of
    # the two tracks plus the target's pitch.
    for key, expected in LANDMARKS.items():
        got = state[key]
        if got is None or abs(got - expected) > 0.6:
            raise FixtureError(
                f"state not established: {key} is {got}, expected {expected}. "
                "Probing an unverified state is worse than not probing.")
    if len({round(v) for v in LANDMARKS.values()}) < 3:
        raise FixtureError("the three landmarks are not distinct")
    return state


def settle(ch: Channel) -> dict:
    """Poll both decks until the pair stops moving, or give up saying so."""
    series, stable, last = [], 0, None
    start = time.monotonic()
    while time.monotonic() - start < SETTLE_TIMEOUT:
        pair = (num(ch.query(f"deck {SOURCE} get_bpm")),
                num(ch.query(f"deck {TARGET} get_bpm")))
        series.append({"t": round(time.monotonic() - start, 2),
                       "source": pair[0], "target": pair[1]})
        stable = stable + 1 if pair == last else 0
        last = pair
        if stable >= SETTLE_STABLE and time.monotonic() - start >= SETTLE_MIN:
            break
        time.sleep(0.5)
    return {
        "settled": stable >= SETTLE_STABLE,
        "source_bpm": last[0] if last else None,
        "target_bpm": last[1] if last else None,
        "source_pitch": num(ch.query(f"deck {SOURCE} get_pitch")),
        "target_pitch": num(ch.query(f"deck {TARGET} get_pitch")),
        "seconds": round(time.monotonic() - start, 2),
        "series": series,
    }


def probe_form(ch: Channel, form: str, src_track: Path, tgt_track: Path) -> dict:
    state = establish(ch, src_track, tgt_track)
    script = f"deck {SOURCE} auto_bpm_transition" + (f" {form}" if form else "")
    returned = ch.execute(script)
    result = settle(ch)
    result["transition_running_after"] = ch.query(f"deck {SOURCE} auto_bpm_transition")
    result["moved"] = (state["source_current"] is not None
                       and result["source_bpm"] is not None
                       and abs(result["source_bpm"] - state["source_current"]) > 0.6)
    return {"form": form, "script": script, "returned": returned,
            "established": state} | result


def one_run(ch: Channel, label: str, order: list[str],
            src_track: Path, tgt_track: Path) -> dict:
    rows = [probe_form(ch, form, src_track, tgt_track) for form in order]
    return {"run": label, "order": order, "forms": rows}


def landing(row: dict) -> str | None:
    """Which landmark this form settled on, if any."""
    value = row.get("source_bpm")
    if value is None or not row.get("settled"):
        return None
    for name, bpm in LANDMARKS.items():
        if abs(value - bpm) <= 0.6:
            return name
    return "other"


def summarise(runs: list[dict]) -> dict:
    by_form: dict[str, dict] = {}
    for run in runs:
        for row in run["forms"]:
            by_form.setdefault(row["form"], {"landings": [], "bpms": []})
            by_form[row["form"]]["landings"].append(landing(row))
            by_form[row["form"]]["bpms"].append(row.get("source_bpm"))

    floors = {tuple(by_form[c]["landings"]) for c in ("zzqqx", "vfnrbq")
              if c in by_form}
    bare = tuple(by_form.get("", {}).get("landings", []))

    forms = {}
    for form, rec in by_form.items():
        landings = tuple(rec["landings"])
        agree = len(set(landings)) == 1 and landings[0] is not None
        if not agree:
            verdict = "unstable-across-runs"
        elif form in ("zzqqx", "vfnrbq"):
            verdict = "control"
        elif form == "":
            verdict = f"bare-lands-on-{landings[0]}"
        elif landings == bare:
            # Not "ignored": a parameter that names the DEFAULT lands where an
            # ignored tail lands, and this observable cannot tell the two
            # apart. Say which it is, so nobody records it as refuted.
            verdict = "names-the-default-landing-so-cannot-separate"
        elif landings in floors:
            verdict = "indistinguishable-from-the-floor"
        else:
            verdict = f"recognized-lands-on-{landings[0]}"
        forms[form or "(bare)"] = {"verdict": verdict, "landing": landings[0],
                                   "bpms": rec["bpms"]}

    confirmed = sorted(f for f, r in forms.items()
                       if r["verdict"].startswith("recognized"))
    return {
        "runs": len(runs),
        "landmarks": LANDMARKS,
        "controls_agree": len(floors) == 1,
        "confirmed": confirmed,
        "forms": forms,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", action="store_true", help="establish, probe, restore")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        if not ARTIFACT.exists():
            print("bpm-transition check skipped: artifact not captured yet")
            return 0
        s = json.load(open(ARTIFACT))["summary"]
        if s["runs"] < 2:
            sys.exit("bpm-transition check FAILED: fewer than two independent runs")
        if not s["controls_agree"]:
            sys.exit("bpm-transition check FAILED: the nonsense controls disagree, "
                     "so nothing in the run has a floor to be read against")
        unstable = [f for f, r in s["forms"].items() if r["verdict"].endswith("runs")]
        print(f"bpm-transition check passed: {s['runs']} runs, "
              f"{len(s['confirmed'])} parameters confirmed "
              f"({', '.join(s['confirmed'])})"
              + (f"; unstable: {', '.join(unstable)}" if unstable else ""))
        return 0

    if not args.run:
        ap.error("pass --run (writes to a live VirtualDJ) or --check")

    ch = Channel()
    tgt_track, src_track = ensure_audio(), second_track()
    before = {deck: deck_state(ch, deck) for deck in (SOURCE, TARGET)}
    before_pitch = {deck: ch.query(f"deck {deck} get_pitch") for deck in (SOURCE, TARGET)}
    runs = []
    try:
        order = [f for f, _ in FORMS]
        runs.append(one_run(ch, "run-1", order, src_track, tgt_track))
        # Independent: same states, opposite order, so a result that depends on
        # what ran before it shows up as disagreement rather than as a finding.
        runs.append(one_run(ch, "run-2", list(reversed(order)), src_track, tgt_track))
    finally:
        for deck in (SOURCE, TARGET):
            ch.execute(f"deck {deck} pitch 100%")
            restore_deck(ch, deck, before[deck])
        time.sleep(1.0)
        for deck in (SOURCE, TARGET):
            # `get_pitch` reports a percent CHANGE (0 = none) but `pitch N%`
            # takes an absolute slider position where 100% is no change, so a
            # naive round-trip of the reading sets the slider to its floor.
            pct = num(before_pitch[deck]) or 0.0
            ch.execute(f"deck {deck} pitch {100 + pct:g}%")

    payload = {
        "summary": summarise(runs) | {
            "restored_to": {str(d): before[d] | {"pitch": before_pitch[d]}
                            for d in (SOURCE, TARGET)},
            "pitch_after_restore": {str(d): ch.query(f"deck {d} get_pitch")
                                    for d in (SOURCE, TARGET)},
        },
        "method": {
            "app_settings": {name: ch.query(f"setting '{name}'")
                             for name in ("smartPlay", "autoBPMMatch")},
            "state": {"source_deck": SOURCE, "target_deck": TARGET,
                      "source_track_bpm": SOURCE_BPM,
                      "target_track_bpm": TARGET_BPM,
                      "target_pitched_to": TARGET_PITCHED},
            "observable": "where deck 1 and deck 2 get_bpm settle after the "
                          "transition, not whether a transition is running",
            "decks_stopped": True,
            "forms": {f or "(bare)": why for f, why in FORMS},
        },
        "runs": runs,
    }
    json.dump(payload, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
