#!/usr/bin/env python3
"""Quit and relaunch VirtualDJ (macOS), then wait for the HTTP interface to answer.

A full quit and relaunch is the only fix for three states this repo has met: the
HTTP socket that accepts but no longer answers after a crash-recover
(tools/fixtures.py), `timecode_cd_mode` set from script, and session globals a
probe needs cleared. Task H5 also needs a launch with `-remote`.

Safety, in order:
  1. If the HTTP interface answers and any deck is playing, refuse: a restart
     would cut a live set. --allow-playing overrides.
  2. If the app is running but the interface does not answer, playback cannot be
     checked, so refuse unless --force.
  3. Quit gracefully (AppleEvent), so VirtualDJ saves its settings. If it has not
     exited within --quit-timeout (it may be showing a dialog), stop and say so;
     only --force then terminates it (SIGTERM, then SIGKILL).
  4. Relaunch with `open -a`, passing --arg values through, and poll get_version.
     The Network Control listener occasionally does not come up on a launch
     (2026-09-29, build 18.0.9644: a clean relaunch answered nothing for 120s,
     with no listener on port 80), so a launch that stays silent is quit and
     retried, --retries times. That instance cannot be playing, so a stalled quit
     of it is terminated without --force.

    python3 tools/vdj_restart.py [--force] [--allow-playing] [--arg -remote ...]
    python3 tools/vdj_restart.py --status     # running? answering? playing?

Prints a short report; exits non-zero when it refused or the app did not come back.
"""

import argparse
import os
import signal
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

APP = Path(os.environ.get("VDJ_APP", "/Applications/VirtualDJ.app"))
PROCESS = "VirtualDJ"
HTTP_BASE = os.environ.get("VDJ_MCP_HTTP_BASE", "http://localhost")
DECKS = (1, 2, 3, 4)
def query(script, timeout=3):
    """The body of /query, or None when the interface does not answer."""
    url = f"{HTTP_BASE}/query?" + urllib.parse.urlencode({"script": script})
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace").strip()
    except OSError:
        return None


def pids():
    r = subprocess.run(["pgrep", "-x", PROCESS], capture_output=True, text=True)
    return [int(p) for p in r.stdout.split()]


def status():
    running = pids()
    version = query("get_version")
    # Fail closed: only an explicit "no" counts as stopped (seen on build 9644;
    # "yes" while playing is the bool contract, not observed by this tool).
    playing = [d for d in DECKS if query(f"deck {d} play") != "no"] if version is not None else None
    return running, version, playing


def wait_for(predicate, timeout, step=0.5):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(step)
    return predicate()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--status", action="store_true", help="report state and change nothing")
    p.add_argument("--force", action="store_true",
                   help="restart even when playback cannot be checked, and terminate if a graceful quit stalls")
    p.add_argument("--allow-playing", action="store_true", help="restart even while a deck is playing")
    p.add_argument("--arg", action="append", default=[], help="launch argument, e.g. --arg -remote (repeatable)")
    p.add_argument("--quit-timeout", type=float, default=20)
    p.add_argument("--up-timeout", type=float, default=60)
    p.add_argument("--retries", type=int, default=2,
                   help="relaunch again when HTTP does not come up (it occasionally does not)")
    args = p.parse_args()

    running, version, playing = status()
    state = (f"running: {'pid ' + ', '.join(map(str, running)) if running else 'no'}; "
             f"HTTP: {'get_version -> ' + repr(version) if version is not None else 'not answering'}; "
             f"playing decks: {playing if playing is not None else 'unknown'}")
    if args.status:
        print(state)
        return 0
    if sys.platform != "darwin":
        print("refused: restart is implemented for macOS only")
        return 2
    if not APP.exists():
        print(f"refused: {APP} not found (set VDJ_APP)")
        return 2

    if running:
        if playing and not args.allow_playing:
            print(f"refused: deck {', '.join(map(str, playing))} is playing; a restart would cut it off. "
                  f"Pass allow-playing to restart anyway.\n{state}")
            return 3
        if version is None and not args.force:
            print("refused: VirtualDJ is running but its HTTP interface does not answer, so playback "
                  "cannot be checked. Pass force if nothing is playing (this is the hung-socket case "
                  f"a restart fixes).\n{state}")
            return 3

        quit_how = quit_app(args.quit_timeout, terminate=args.force)
        if quit_how is None:
            print(f"stopped: VirtualDJ did not quit within {args.quit_timeout:.0f}s — it may be showing "
                  "a dialog. Nothing was killed. Pass force to terminate it.")
            return 4
    else:
        quit_how = "was not running"

    with_args = f" with {' '.join(args.arg)}" if args.arg else ""
    log = [f"VirtualDJ {quit_how}"]
    for attempt in range(1, args.retries + 2):
        waited = launch_and_wait(args.arg, args.up_timeout)
        if isinstance(waited, str):  # launch itself failed
            print(f"failed: {waited}")
            return 5
        if waited is not None:
            log.append(f"relaunched{with_args}; HTTP answering after {waited:.1f}s "
                       f"(get_version -> {query('get_version')!r}, pid {', '.join(map(str, pids()))})")
            print("; ".join(log))
            return 0
        log.append(f"relaunch {attempt}: HTTP did not answer within {args.up_timeout:.0f}s")
        if attempt <= args.retries:
            # The instance was launched seconds ago by this tool, so it is not playing:
            # terminating a stalled quit is safe here without force.
            how = quit_app(args.quit_timeout, terminate=True)
            if how is None:
                break
            log.append(f"{how}, retrying")
    log.append(f"giving up (pid {pids() or 'none'}). The Network Control plugin did not start its "
               "listener; check it is enabled in the Master Effect drop-down")
    print("; ".join(log))
    return 6


def quit_app(timeout, terminate):
    """Quit gracefully; with terminate, SIGTERM then SIGKILL a stalled quit.

    Returns how it quit, or None if the app is still running.
    """
    started = time.monotonic()
    subprocess.run(["osascript", "-e", f'tell application "{PROCESS}" to quit'],
                   capture_output=True, text=True, timeout=timeout + 5)
    if wait_for(lambda: not pids(), timeout):
        return f"quit gracefully in {time.monotonic() - started:.1f}s"
    if not terminate:
        return None
    for sig in (signal.SIGTERM, signal.SIGKILL):
        for pid in pids():
            try:
                os.kill(pid, sig)
            except ProcessLookupError:
                pass
        if wait_for(lambda: not pids(), 10):
            return f"terminated after a {timeout:.0f}s graceful attempt"
    return None


def launch_and_wait(launch_args, timeout):
    """Seconds until get_version answered, None on timeout, or an error string."""
    launch = ["open", "-a", str(APP)] + (["--args", *launch_args] if launch_args else [])
    r = subprocess.run(launch, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        return f"{' '.join(launch)} -> {r.stderr.strip()}"
    started = time.monotonic()
    if wait_for(lambda: query("get_version", timeout=2) is not None, timeout, step=1):
        return time.monotonic() - started
    return None


if __name__ == "__main__":
    raise SystemExit(main())
