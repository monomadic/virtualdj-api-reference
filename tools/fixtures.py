#!/usr/bin/env python3
"""Named, self-verifying VirtualDJ states for argument probing.

Unknown arguments are silently ignored (`loaded bogusword` -> `yes`), so an
argument form can only be confirmed by comparing values across forms **in a
state where those forms would disagree**. `loaded opposite` says nothing with
both decks empty. This module is that missing half: named states, each
established over the HTTP channel and each **asserting its own preconditions
before any probe runs**.

The contract every fixture keeps:

1. `setup` runs, then `assertions` are polled until they all hold or the
   deadline passes. A fixture that cannot verify itself raises `FixtureError`
   — a probe against an unestablished state is worse than no probe at all.
2. `teardown` returns the app to the deck contents and transport state
   observed at `establish()` time, not to some assumed-clean baseline.
3. Fixture audio is generated locally (ffmpeg, a 120 BPM pulse train), never
   the user's library, so results do not depend on what is in the collection.

    python3 tools/fixtures.py --list
    python3 tools/fixtures.py --establish one_deck_loaded
    python3 tools/fixtures.py --establish loop_active --hold 5 --teardown
    python3 tools/fixtures.py --check         # offline: validate definitions

`--establish` changes live app state and some fixtures start playback, which
makes sound. See docs/HTTP Control Interface.md for the channel's semantics and
its error-code taxonomy.
"""

from __future__ import annotations

import argparse
import http.client
import json
import shutil
import subprocess
import sys
import time
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

HOST, PORT = "localhost", 80
TIMEOUT = 10
POLL_SECONDS = 0.25
DEFAULT_DEADLINE = 8.0

AUDIO_DIR = Path.home() / "Library/Caches/virtualdj-api-reference/fixtures"
AUDIO_NAME = "fixture-120bpm.wav"
AUDIO_SECONDS = 90
AUDIO_BPM = 120
# 0.2 amplitude, one decaying 440 Hz burst every 0.5 s -> a 120 BPM pulse train
# VirtualDJ can beatgrid, quiet enough not to dominate a room.
AUDIO_EXPR = r"0.2*sin(2*PI*440*t)*exp(-8*mod(t\,0.5))"  # comma escaped for lavfi


class FixtureError(RuntimeError):
    """A fixture could not be established, or could not verify itself."""


class Channel:
    """GET /query and /execute against the local Network Control plugin."""

    def __init__(self, host: str = HOST, port: int = PORT, timeout: int = TIMEOUT):
        self.host, self.port, self.timeout = host, port, timeout
        self._conn: http.client.HTTPConnection | None = None

    def _request(self, endpoint: str, script: str) -> str:
        path = f"/{endpoint}?" + urllib.parse.urlencode({"script": script})
        for attempt in (1, 2):
            try:
                if self._conn is None:
                    self._conn = http.client.HTTPConnection(self.host, self.port,
                                                            timeout=self.timeout)
                self._conn.request("GET", path)
                return self._conn.getresponse().read().decode(errors="replace").strip()
            except Exception:
                self.close()
                if attempt == 2:
                    raise
        raise AssertionError("unreachable")

    def close(self) -> None:
        if self._conn is not None:
            try:
                self._conn.close()
            finally:
                self._conn = None

    def query(self, script: str) -> str:
        return self._request("query", script)

    def execute(self, script: str) -> str:
        return self._request("execute", script)

    def reachable(self) -> bool:
        try:
            return self.query("get_version") != ""
        except Exception:
            return False


def is_error(value: str) -> bool:
    return value.startswith("error:")


def yes(value: str) -> bool:
    return value == "yes"


def no(value: str) -> bool:
    return value == "no"


def nonzero_number(value: str) -> bool:
    try:
        return float(value) != 0.0
    except ValueError:
        return False


@dataclass(frozen=True)
class Assertion:
    """One readback that must hold for the fixture to count as established."""

    script: str
    predicate: Callable[[str], bool]
    describes: str

    def check(self, channel: Channel) -> tuple[bool, str]:
        value = channel.query(self.script)
        return self.predicate(value), value


@dataclass(frozen=True)
class Fixture:
    name: str
    describes: str
    setup: list[str]
    assertions: list[Assertion]
    teardown: list[str] = field(default_factory=list)
    decks: tuple[int, ...] = (1, 2)
    plays_audio: bool = False
    needs_audio_file: bool = True
    deadline: float = DEFAULT_DEADLINE


def audio_path() -> Path:
    return AUDIO_DIR / AUDIO_NAME


def ensure_audio(verbose: bool = True) -> Path:
    """Generate the fixture track once; reuse it afterwards."""
    path = audio_path()
    if path.exists():
        return path
    if shutil.which("ffmpeg") is None:
        raise FixtureError("ffmpeg not found — needed once to generate the fixture track")
    path.parent.mkdir(parents=True, exist_ok=True)
    if verbose:
        print(f"generating fixture audio ({AUDIO_SECONDS}s, {AUDIO_BPM} BPM) -> {path}")
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y",
         "-f", "lavfi", "-i", f"aevalsrc=exprs={AUDIO_EXPR}:d={AUDIO_SECONDS}:s=44100",
         "-ac", "2", str(path)],
        check=True)
    return path


def load_script(deck: int, path: Path) -> str:
    return f'deck {deck} load "{path}"'


def deck_state(channel: Channel, deck: int) -> dict[str, str]:
    """Enough to put a deck back the way it was found."""
    return {
        "loaded": channel.query(f"deck {deck} loaded"),
        "path": channel.query(f'deck {deck} get_loaded_song "fullpath"'),
        "playing": channel.query(f"deck {deck} play"),
    }


def restore_deck(channel: Channel, deck: int, before: dict[str, str]) -> None:
    if before["playing"] == "yes" and channel.query(f"deck {deck} play") == "no":
        channel.execute(f"deck {deck} play")
    elif before["playing"] == "no" and channel.query(f"deck {deck} play") == "yes":
        channel.execute(f"deck {deck} pause")
    if before["loaded"] == "no":
        channel.execute(f"deck {deck} unload")
    elif before["path"] and not is_error(before["path"]):
        current = channel.query(f'deck {deck} get_loaded_song "fullpath"')
        if current != before["path"]:
            channel.execute(f'deck {deck} load "{before["path"]}"')


def build_fixtures(track: Path | None) -> dict[str, Fixture]:
    """Fixture definitions. `track` is None only for offline validation."""
    t = track if track is not None else Path("<fixture track>")
    load1, load2 = load_script(1, t), load_script(2, t)
    return {f.name: f for f in [
        Fixture(
            name="one_deck_loaded",
            describes="deck 1 holds the fixture track, deck 2 empty",
            setup=[load1, "deck 2 unload"],
            assertions=[
                Assertion("deck 1 loaded", yes, "deck 1 reports a track"),
                Assertion("deck 2 loaded", no, "deck 2 reports empty"),
            ],
            teardown=["deck 1 unload"],
        ),
        Fixture(
            name="both_decks_loaded",
            describes="both decks hold the fixture track, neither playing",
            setup=[load1, load2],
            assertions=[
                Assertion("deck 1 loaded", yes, "deck 1 reports a track"),
                Assertion("deck 2 loaded", yes, "deck 2 reports a track"),
            ],
            teardown=["deck 1 unload", "deck 2 unload"],
        ),
        Fixture(
            name="deck2_playing",
            describes="deck 2 playing, deck 1 loaded and stopped — the asymmetry "
                      "`opposite`/`other`/`active` style arguments need",
            setup=[load1, load2, "deck 1 pause", "deck 2 play"],
            assertions=[
                Assertion("deck 1 loaded", yes, "deck 1 reports a track"),
                Assertion("deck 2 play", yes, "deck 2 reports playing"),
                Assertion("deck 1 play", no, "deck 1 reports stopped"),
            ],
            teardown=["deck 2 pause", "deck 1 unload", "deck 2 unload"],
            plays_audio=True,
        ),
        Fixture(
            name="loop_active",
            describes="deck 1 playing inside a 4-beat loop",
            setup=[load1, "deck 1 play", "deck 1 loop 4"],
            assertions=[
                Assertion("deck 1 loop", yes, "deck 1 reports looping"),
                Assertion("deck 1 get_loop", nonzero_number, "loop length is nonzero"),
            ],
            teardown=["deck 1 loop_exit", "deck 1 pause", "deck 1 unload"],
            plays_audio=True,
        ),
        Fixture(
            name="fx_slot_1_on",
            describes="deck 1 loaded with effect slot 1 active",
            setup=[load1, "deck 1 effect_active 1 on"],
            assertions=[
                Assertion("deck 1 effect_active 1", yes, "slot 1 reports active"),
            ],
            teardown=["deck 1 effect_active 1 off", "deck 1 unload"],
        ),
        Fixture(
            name="sampler_slot_loaded",
            describes="sampler slot 1 holds a sample (shipped bank, not loaded by us)",
            setup=[],
            assertions=[
                Assertion("sampler_loaded 1", yes, "sampler slot 1 reports loaded"),
            ],
            needs_audio_file=False,
        ),
    ]}


def establish(channel: Channel, fixture: Fixture, verbose: bool = True) -> dict[int, dict]:
    """Run setup, then poll the assertions. Raise unless every one holds."""
    before = {d: deck_state(channel, d) for d in fixture.decks}
    for script in fixture.setup:
        result = channel.execute(script)
        if verbose:
            print(f"  setup   {script!r} -> {result}")
    deadline = time.monotonic() + fixture.deadline
    failures: list[str] = []
    while True:
        failures = []
        for a in fixture.assertions:
            ok, value = a.check(channel)
            if not ok:
                failures.append(f"{a.describes}: `{a.script}` -> {value!r}")
        if not failures:
            break
        if time.monotonic() >= deadline:
            raise FixtureError(
                f"fixture {fixture.name!r} did not establish within "
                f"{fixture.deadline:.0f}s:\n    - " + "\n    - ".join(failures))
        time.sleep(POLL_SECONDS)
    if verbose:
        for a in fixture.assertions:
            print(f"  verify  {a.describes}: ok")
    return before


def teardown(channel: Channel, fixture: Fixture, before: dict[int, dict] | None,
             verbose: bool = True) -> None:
    for script in fixture.teardown:
        result = channel.execute(script)
        if verbose:
            print(f"  teardown {script!r} -> {result}")
    if before:
        for deck, state in before.items():
            restore_deck(channel, deck, state)
            if verbose:
                print(f"  restored deck {deck} to {state['loaded']}"
                      f"{'/playing' if state['playing'] == 'yes' else ''}")


def cmd_list(fixtures: dict[str, Fixture]) -> int:
    for f in fixtures.values():
        audio = " [plays audio]" if f.plays_audio else ""
        print(f"{f.name:22s} {f.describes}{audio}")
        for a in f.assertions:
            print(f"{'':22s}   asserts: `{a.script}` — {a.describes}")
    return 0


def cmd_check(fixtures: dict[str, Fixture]) -> int:
    """Offline validation: definitions only, so `just check` stays hermetic."""
    errs = []
    for name, f in fixtures.items():
        if name != f.name:
            errs.append(f"{name}: key does not match fixture name {f.name!r}")
        if not f.assertions:
            errs.append(f"{name}: no assertions — it could not verify itself")
        if f.setup and not f.teardown and f.name != "sampler_slot_loaded":
            errs.append(f"{name}: sets up but never tears down")
        for a in f.assertions:
            if not a.script.strip() or not callable(a.predicate):
                errs.append(f"{name}: malformed assertion {a.script!r}")
    if errs:
        sys.exit("fixture check FAILED:\n  - " + "\n  - ".join(errs))
    channel = Channel()
    live = "reachable" if channel.reachable() else "not reachable (offline check only)"
    print(f"fixture check passed: {len(fixtures)} fixtures, "
          f"{sum(len(f.assertions) for f in fixtures.values())} assertions; "
          f"channel {live}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--list", action="store_true")
    p.add_argument("--check", action="store_true")
    p.add_argument("--establish", metavar="NAME")
    p.add_argument("--verify", metavar="NAME", help="check assertions without running setup")
    p.add_argument("--teardown", action="store_true", help="tear down after --establish")
    p.add_argument("--hold", type=float, default=0.0, metavar="SECONDS")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.list or args.check:
        fixtures = build_fixtures(None)
        return cmd_list(fixtures) if args.list else cmd_check(fixtures)

    if not (args.establish or args.verify):
        p.error("nothing to do: pass --list, --check, --establish or --verify")

    name = args.establish or args.verify
    channel = Channel()
    if not channel.reachable():
        raise FixtureError(
            "HTTP channel unreachable on localhost:80 — is VirtualDJ running with the "
            "Network Control plugin enabled? After a crash-recover the socket listens "
            "but stops accepting; a full quit and relaunch is the only fix.")
    fixtures = build_fixtures(None)
    if name not in fixtures:
        p.error(f"unknown fixture {name!r}; known: {', '.join(fixtures)}")
    track = ensure_audio() if fixtures[name].needs_audio_file else None
    fixture = build_fixtures(track)[name]

    if args.verify:
        results = [(a.describes, a.script, *a.check(channel)) for a in fixture.assertions]
        if args.json:
            print(json.dumps([{"describes": d, "script": s, "ok": ok, "value": v}
                              for d, s, ok, v in results], indent=1))
        else:
            for d, s, ok, v in results:
                print(f"  {'ok  ' if ok else 'FAIL'}  {d}: `{s}` -> {v!r}")
        return 0 if all(r[2] for r in results) else 1

    print(f"establishing {fixture.name}: {fixture.describes}")
    before = establish(channel, fixture)
    print(f"established {fixture.name}")
    if args.hold:
        time.sleep(args.hold)
    if args.teardown:
        teardown(channel, fixture, before)
        print(f"torn down {fixture.name}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FixtureError as exc:
        raise SystemExit(f"fixture error: {exc}")
