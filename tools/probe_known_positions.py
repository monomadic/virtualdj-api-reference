#!/usr/bin/env python3
"""Discriminate `get_time`'s position arguments against known distinct positions.

None of the ten states in `fixtures.py` establishes a cue and loop endpoints at
positions that are *known* and *mutually distinct*, so the stored arg-form probe
could not tell `get_time 'cue1'` from `get_time 'anything-it-does-not-know'`:
both answered, and in a state where every position coincided both answered the
same number. Separation from a nonsense token was impossible by construction.

This builds that missing state and reads it with an oracle that is not
`get_time`:

    cue 1        <- cue_pos 1 mseconly
    loop in/out  <- get_loop_in_time on / get_loop_out_time on
    playhead     <- get_position x get_time 'total'

Every position is read back and asserted distinct before a single form is
probed; the run aborts rather than probe an unverified state. Then one position
moves while the others are held, which is what separates "tracks this position"
from "happens to equal it once".

    python3 tools/probe_known_positions.py --run > tests/get-time-positions.json
    python3 tools/probe_known_positions.py --check

The run loads a generated fixture track on deck 1, leaves the deck stopped
(no audio), and restores the deck contents, the cue and `display_time`
afterwards. It writes a cue point to the fixture track's database entry and
deletes it again.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixtures import (  # noqa: E402
    Channel, FixtureError, deck_state, ensure_audio, is_error, restore_deck,
)

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "tests" / "get-time-positions.json"
DECK = 1

# Every `get_time` tail worth asking here. The floors are first-class: an
# unknown tail does NOT fall back to the bare form, it falls back to elapsed,
# so "bare differs from my argument" is not evidence the argument was read.
FORMS = [
    ("", "floor: whatever display_time selects"),
    ("elapsed", "floor: documented, position of the playhead"),
    ("remain", "documented"),
    ("total", "documented"),
    ("absolute", "documented: ignore pitch"),
    ("cue1", "TARGET: cue point 1"),
    ("cue", "vocabulary-group member, never probed"),
    ("loopin", "TARGET: loop start"),
    ("loopout", "TARGET: loop end"),
    ("to_lyrics", "documented, no lyrics in the fixture"),
    ("short", "documented as a text format, not a position"),
    ("qzqzqz", "CONTROL: nonsense"),
    ("wvwvwv", "CONTROL: a second, different nonsense token"),
]
TARGETS = {"cue1": "cue_1", "loopin": "loop_in", "loopout": "loop_out"}


def q(ch: Channel, script: str) -> str:
    return ch.query(f"deck {DECK} {script}")


def number(value: str) -> int | None:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def oracles(ch: Channel) -> dict[str, int | None]:
    """The positions, read by something that is not `get_time`."""
    total = number(q(ch, "get_time 'total'"))
    position = q(ch, "get_position")
    playhead = None
    if total is not None and number(position) is not None:
        playhead = int(round(float(position) * total))
    return {
        "cue_1": number(q(ch, "cue_pos 1 mseconly")),
        "loop_in": number(q(ch, "get_loop_in_time on")),
        "loop_out": number(q(ch, "get_loop_out_time on")),
        "playhead_from_position": playhead,
        "total": total,
    }


def establish(ch: Channel, track: Path, seek_beats: int, cue_ms: int) -> dict:
    """Cue, loop and playhead at three distinct positions, deck stopped.

    Quantisation moves what it is given — `set_cue 1 15000ms` landed on 14496 —
    so nothing here assumes the requested number. The positions are whatever
    the app chose; the run reads them back and only requires them distinct.
    """
    ch.execute(f'deck {DECK} load "{track}"')
    time.sleep(2.5)
    if q(ch, "loaded") != "yes":
        raise FixtureError("deck 1 did not report the fixture track loaded")
    if q(ch, "play") == "yes":
        ch.execute(f"deck {DECK} pause")

    ch.execute(f"deck {DECK} goto_start")
    ch.execute(f"deck {DECK} set_cue 1 {cue_ms}ms")
    # `loop N` lays an N-beat loop ENDING at the playhead, so seek first.
    ch.execute(f"deck {DECK} goto_start")
    ch.execute(f"deck {DECK} goto +{seek_beats}")
    time.sleep(0.4)
    ch.execute(f"deck {DECK} loop 32")
    time.sleep(0.4)
    # Move off the loop-out point so the playhead is distinct from every target.
    ch.execute(f"deck {DECK} goto -16")
    time.sleep(0.6)
    return oracles(ch)


def verify(state: dict, loop_expected: str) -> list[str]:
    """A state that cannot prove its own positions is not a fixture."""
    problems = []
    for key in ("cue_1", "loop_in", "loop_out", "playhead_from_position", "total"):
        if state.get(key) is None:
            problems.append(f"{key} did not read back as a number")
    named = {k: state[k] for k in ("cue_1", "loop_in", "loop_out", "playhead_from_position")
             if state.get(k) is not None}
    for a in named:
        for b in named:
            if a < b and named[a] == named[b]:
                problems.append(f"{a} and {b} are both {named[a]} — the state cannot "
                                "discriminate the forms that read them")
    if state.get("loop_active") != loop_expected:
        problems.append(f"loop reports {state.get('loop_active')!r}, expected {loop_expected!r}")
    return problems


def probe(ch: Channel, order: list[str]) -> dict[str, str]:
    return {form: q(ch, f"get_time {repr(form) if form else ''}".strip()) for form in order}


def classify(values: dict[str, str], state: dict) -> dict:
    """Which forms match which independently known position."""
    floor = number(values.get("qzqzqz", ""))
    out = {}
    for form, _why in FORMS:
        v = number(values.get(form, ""))
        matches = sorted(k for k, p in state.items()
                         if isinstance(p, int) and p is not None and v == p)
        out[form] = {
            "value": values.get(form),
            "matches_oracle": matches,
            "equals_nonsense_floor": v is not None and v == floor,
        }
    return out


def one_run(ch: Channel, track: Path, label: str, order: list[str],
            seek_beats: int, cue_ms: int, move_to_beats: int) -> dict:
    state = establish(ch, track, seek_beats, cue_ms)
    state["loop_active"] = q(ch, "loop")
    state["display_time_mode"] = next(
        (m for m in ("elapsed", "remain", "total") if q(ch, f"display_time '{m}'") == "yes"),
        "unknown")
    problems = verify(state, "yes")
    if problems:
        raise FixtureError(f"{label}: " + "; ".join(problems))

    values = probe(ch, order)

    # Perturbation: move ONE position, hold the rest, re-read everything. A form
    # that tracks the move is reading that position; one that does not is not.
    ch.execute(f"deck {DECK} goto_start")
    ch.execute(f"deck {DECK} goto +{move_to_beats}")
    time.sleep(0.5)
    ch.execute(f"deck {DECK} set_cue 1")
    time.sleep(0.5)
    moved = oracles(ch)
    moved["loop_active"] = q(ch, "loop")
    moved["display_time_mode"] = state["display_time_mode"]
    moved_problems = verify(moved, moved["loop_active"])
    moved_values = probe(ch, list(reversed(order)))

    return {
        "label": label,
        "query_order": order,
        "before": {
            "oracles": state,
            "forms": classify(values, state),
        },
        "after_moving_cue_1": {
            "oracles": moved,
            "note": "seeking outside an active loop deactivates it; the stored "
                    "endpoints survive and `get_loop_*_time on` still reads them",
            "verification": moved_problems or "distinct",
            "forms": classify(moved_values, moved),
        },
    }


PHASES = ("before", "after_moving_cue_1")


def summarise(runs: list[dict]) -> dict:
    """A target is confirmed only where BOTH runs agree, phase by phase.

    A form that reads its position in one loop state and something else in the
    other is not unstable — it is conditional, and the verdict says which
    condition, because "partial" would hide a reproducible rule.
    """
    verdicts = {}
    for tail, oracle in TARGETS.items():
        by_loop: dict[str, list[bool]] = {"yes": [], "no": []}
        elsewhere: set[str] = set()
        for run in runs:
            for phase in PHASES:
                rec = run[phase]["forms"][tail]
                active = run[phase]["oracles"].get("loop_active", "?")
                hit = oracle in rec["matches_oracle"] and not rec["equals_nonsense_floor"]
                by_loop.setdefault(active, []).append(hit)
                if not hit:
                    elsewhere |= {m for m in rec["matches_oracle"]}
        every = [h for hits in by_loop.values() for h in hits]
        if all(every):
            verdict = "reads_its_position"
        elif by_loop["yes"] and all(by_loop["yes"]) and by_loop["no"] and not any(by_loop["no"]):
            verdict = "reads_its_position_only_while_a_loop_is_active"
        elif any(every):
            verdict = "partial"
        else:
            verdict = "no_relationship"
        verdicts[tail] = {
            "verdict": verdict,
            "matched_by_loop_state": {k: v for k, v in by_loop.items() if v},
            "otherwise_matched": sorted(elsewhere),
        }
    floors, absolutes = [], []
    for run in runs:
        for phase in PHASES:
            forms = run[phase]["forms"]
            floors.append(forms["qzqzqz"]["value"] == forms["wvwvwv"]["value"]
                          == forms["elapsed"]["value"] != forms[""]["value"])
            absolutes.append(forms["absolute"]["value"] == forms[""]["value"])
    return {
        "targets": verdicts,
        "nonsense_falls_back_to_elapsed_not_to_the_bare_form": all(floors),
        "absolute_keeps_the_display_time_mode": all(absolutes),
        "runs": len(runs),
        "phases_per_run": list(PHASES),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", action="store_true", help="establish, probe, restore")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        if not ARTIFACT.exists():
            print("known-position check skipped: artifact not captured yet")
            return 0
        art = json.load(open(ARTIFACT))
        s = art["summary"]
        if s["runs"] < 2:
            sys.exit("known-position check FAILED: fewer than two independent runs")
        unresolved = [k for k, v in s["targets"].items()
                      if v["verdict"] in ("partial", "no_relationship")]
        reads = sum(1 for v in s["targets"].values()
                    if v["verdict"].startswith("reads_its_position"))
        print(f"known-position check passed: {s['runs']} runs x "
              f"{len(s['phases_per_run'])} phases, {reads}/{len(s['targets'])} targets read "
              "their own position"
              + (f"; unresolved: {', '.join(unresolved)}" if unresolved else ""))
        return 0

    if not args.run:
        ap.error("pass --run (writes to a live VirtualDJ) or --check")

    ch = Channel()
    track = ensure_audio()
    before = deck_state(ch, DECK)
    runs = []
    try:
        order = [f for f, _ in FORMS]
        runs.append(one_run(ch, track, "run-1", order, 70, 15000, 140))
        # Independent: the fixture is torn down and rebuilt with different
        # numbers, and the forms are asked in a different order.
        ch.execute(f"deck {DECK} loop_exit")
        ch.execute(f"deck {DECK} delete_cue 1")
        ch.execute(f"deck {DECK} unload")
        time.sleep(1.0)
        runs.append(one_run(ch, track, "run-2", list(reversed(order)), 90, 25000, 120))
    finally:
        ch.execute(f"deck {DECK} loop_exit")
        ch.execute(f"deck {DECK} delete_cue 1")
        cue_left = ch.query(f"deck {DECK} has_cue 1")
        restore_deck(ch, DECK, before)

    payload = {
        "summary": summarise(runs) | {
            "has_cue_1_after_restore": cue_left,
            "deck_restored_to": before,
        },
        "method": {
            "oracles": {"cue_1": "cue_pos 1 mseconly",
                        "loop_in": "get_loop_in_time on",
                        "loop_out": "get_loop_out_time on",
                        "playhead_from_position": "get_position x get_time 'total'"},
            "forms": {f: why for f, why in FORMS},
        },
        "runs": runs,
    }
    json.dump(payload, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
