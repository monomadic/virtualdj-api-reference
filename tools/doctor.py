#!/usr/bin/env python3
"""Is this checkout able to do work? Environment health, in one screen.

`brew doctor` for the reference repo. Four things decide whether a session can
get anything done here, and three of them fail silently:

  1. The interpreter and its packages. The tools that read the VirtualDJ Mach-O
     binary need numpy, and not all of them fail loudly without it — `binary_blob()`
     in `extract_action_catalog.py` used to catch the ImportError alongside a
     genuinely absent app bundle and return None, at which point the catalog
     classified 30 of the vendor's own example placeholders (`loop_load myloop`,
     `var my_var`, `rack rack1`) as unconfirmed vocabulary and promoted them into
     the probe worklist. On 2026-09-09 that is exactly what happened, after
     Homebrew moved its default python to 3.14 and left numpy in the old
     site-packages; the only symptom was a cross-check drift in an
     unrelated-looking artifact.
  2. uv, which is how `just install` builds the venv.
  3. Which VirtualDJ is installed, against the builds the artifacts are anchored
     to. A build-anchored count is permanent evidence about ONE build, so a
     mismatch is not an error — it is the thing to know before quoting a figure
     or re-extracting.
  4. Whether the live probe channel is reachable, which decides half the queue.

Only (1) is a failure. The rest are notices: a checkout with no VirtualDJ
installed still answers every lookup question in the repo.

    python3 tools/doctor.py               # full report
    python3 tools/doctor.py --deps-only   # just (1), hermetic; this is what `just check` runs
"""
from __future__ import annotations

import argparse
import importlib
import json
import plistlib
import re
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIREMENTS = ROOT / "requirements.txt"
TESTS = ROOT / "tests"
APP = Path("/Applications/VirtualDJ.app")
CHANNEL = "http://localhost/query?script=get_version"

# Distribution name -> module name, for the cases where they differ. Nothing in
# this repo needs an entry yet; the map exists so adding `pyyaml` later does not
# turn into a mystery.
MODULE_NAMES: dict[str, str] = {}

OK, WARN, BAD = "ok  ", "note", "FAIL"


def say(state: str, line: str) -> None:
    print(f"  [{state}] {line}")


def required() -> list[str]:
    """Distribution names from requirements.txt, comments and pins stripped."""
    names = []
    for line in REQUIREMENTS.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            names.append(re.split(r"[<>=!~\[;]", line, maxsplit=1)[0].strip())
    return names


def check_python() -> bool:
    """The one section that can fail. True when the environment is usable."""
    version = ".".join(str(n) for n in sys.version_info[:3])
    where = "project .venv" if ".venv" in sys.executable else "system interpreter"
    print("python")
    say(OK, f"{sys.executable} ({version}, {where})")

    missing = []
    for dist in required():
        module = MODULE_NAMES.get(dist, dist.replace("-", "_"))
        try:
            mod = importlib.import_module(module)
        except ImportError:
            missing.append(dist)
            say(BAD, f"{dist} — not importable")
        else:
            say(OK, f"{dist} {getattr(mod, '__version__', '(no __version__)')}")

    if missing:
        say(BAD, "run `just install` to create .venv and install requirements.txt")
        say(BAD, "do not re-extract anything first: the binary-derived artifacts "
                 "degrade quietly without numpy rather than failing")
    return not missing


def check_uv() -> None:
    print("uv")
    path = shutil.which("uv")
    if path:
        say(OK, f"{path} — `just install` will work")
    else:
        say(WARN, "not installed; `just install` needs it (brew install uv)")


def installed_build() -> str | None:
    plist = APP / "Contents" / "Info.plist"
    if not plist.exists():
        return None
    with plist.open("rb") as fh:
        return plistlib.load(fh).get("CFBundleVersion")


def check_virtualdj() -> None:
    print("VirtualDJ")
    build = installed_build()
    if build is None:
        say(WARN, f"not installed at {APP} — extraction tools cannot run; "
                  "every lookup and lint still works")
        return
    say(OK, f"{APP} is build {build}")

    # Artifacts stamp the build they describe. A mismatch is information, not a
    # fault: the stamped figure stays true of the build it was taken on, and a
    # newer build earns a NEW stamped line rather than an edit to the old one.
    anchored: dict[str, list[str]] = {}
    for path in sorted(TESTS.glob("*.json")):
        try:
            summary = json.loads(path.read_text()).get("summary")
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(summary, dict) and isinstance(summary.get("build"), str):
            anchored.setdefault(summary["build"], []).append(path.name)

    for stamp, names in sorted(anchored.items()):
        # An artifact whose FILENAME carries the build is pinned on purpose —
        # `action-modules-9246.json` describes the last unstripped bundle, and
        # re-anchoring it to the installed build would destroy the only copy of
        # what that build held. Do not invite anyone to refresh those.
        short = stamp.split(".")[-1]
        pinned = [n for n in names if short in n]
        drifted = [n for n in names if short not in n]
        if pinned:
            say(OK, f"{stamp}: {', '.join(pinned)} (pinned by name — historical, keep)")
        if drifted:
            state = OK if stamp == build else WARN
            note = "" if stamp == build else "  (re-extract to re-anchor, or quote it as history)"
            say(state, f"{stamp}: {', '.join(drifted)}{note}")


def check_sdk() -> None:
    """The Atomix headers gate `just plugin-build`, and they are not vendored."""
    print("plugin SDK")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from download_sdk import present  # noqa: PLC0415
    where = present()
    if where:
        say(OK, f"{where.relative_to(ROOT)} — `just plugin-build` is unblocked")
    else:
        say(WARN, "headers absent; `just download-sdk` fetches them. Only the "
                  "plugin channel needs them")


def check_channel() -> None:
    print("live probe channel")
    try:
        with urllib.request.urlopen(CHANNEL, timeout=3) as response:
            body = response.read().decode("utf-8", "replace").strip()
        say(OK, f"http://localhost/ reachable — get_version → {body}")
    except (urllib.error.URLError, OSError, TimeoutError):
        say(WARN, "http://localhost/ not reachable. VirtualDJ running is not "
                  "enough: the Network Control extension has to be on")
        say(WARN, "Config → Extensions → Effects → Other → Network Control, then "
                  "Auto-Start it from the Master panel's Master Effect drop-down")
        say(WARN, "every Ready task that needs it says so; the desk-work ones do not")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--deps-only", action="store_true",
                    help="interpreter and packages only; touches nothing outside the repo")
    args = ap.parse_args()

    if args.deps_only:
        # Terse, because `just check` runs it before 30 other lines.
        missing = [d for d in required()
                   if not _importable(MODULE_NAMES.get(d, d.replace("-", "_")))]
        if missing:
            print(f"dependency check FAILED: {', '.join(missing)} not importable by "
                  f"{sys.executable} — run `just install`, and re-extract nothing "
                  "until it passes (the binary readers degrade quietly)",
                  file=sys.stderr)
            return 1
        version = ".".join(str(n) for n in sys.version_info[:3])
        where = "project .venv" if ".venv" in sys.executable else "system"
        print(f"dependency check passed: python {version} ({where}), "
              f"{len(required())} requirement(s) importable")
        return 0

    healthy = check_python()
    print()
    check_uv()
    print()
    check_virtualdj()
    print()
    check_sdk()
    print()
    check_channel()
    print()
    print("doctor: environment usable" if healthy else
          "doctor: NOT usable — fix the python section first")
    return 0 if healthy else 1


def _importable(module: str) -> bool:
    try:
        importlib.import_module(module)
    except ImportError:
        return False
    return True


if __name__ == "__main__":
    sys.exit(main())
