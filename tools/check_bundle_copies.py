#!/usr/bin/env python3
"""Verify the vendor XML copied into `examples/` still matches the installed app.

`examples/*/Built-In/` holds byte copies of pad pages, skins, sampler banks and
video skins read out of `/Applications/VirtualDJ.app`. They are the corpus's
`builtin` source and the evidence behind every `Built-in pad page` /
`Built-in skin` label, so a copy that has silently fallen behind a VirtualDJ
update is a reference doc citing a file the vendor no longer ships.

Nothing detected that before: `pads_stems+fx.xml` sat one build stale with
`padfx "Reverb" 80%` after Atomix changed it to `50%`, and the corpus attested
the old value.

Bundle-dependent by construction, so it SKIPS (exit 0) when VirtualDJ is not
installed — `just check` stays hermetic on a machine without the app.

    python3 tools/check_bundle_copies.py
    python3 tools/check_bundle_copies.py --refresh   # overwrite drifted copies
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

DEFAULT_APP = Path("/Applications/VirtualDJ.app")
# Copied trees, and the bundle zips whose members they came out of. Loose
# Resources/*.xml covers the pad pages and sampler banks.
COPY_ROOTS = (Path("examples/Pads/Built-In"), Path("examples/Skins/Built-In"),
              Path("examples/Samplerbanks/Built-In"), Path("examples/VideoSkins/Built-In"))
ZIPS = ("skin.zip", "remoteskin.zip", "videoskinbroadcast.zip",
        "videoskinkaraoke.zip", "videoskinlive.zip")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bundle_index(app: Path) -> dict[str, dict[str, bytes]]:
    """basename -> {sha256: content} for every XML the bundle ships."""
    index: dict[str, dict[str, bytes]] = defaultdict(dict)
    resources = app / "Contents/Resources"
    for path in sorted(resources.glob("*.xml")):
        data = path.read_bytes()
        index[path.name][digest(data)] = data
    for name in ZIPS:
        archive = resources / name
        if not archive.exists():
            continue
        with ZipFile(archive) as zf:
            for member in zf.namelist():
                if not member.lower().endswith(".xml"):
                    continue
                data = zf.read(member)
                index[Path(member).name][digest(data)] = data
    return index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=Path, default=DEFAULT_APP)
    parser.add_argument("--refresh", action="store_true",
                        help="overwrite drifted copies with the bundle's current bytes")
    args = parser.parse_args()

    if not (args.app / "Contents/Resources").is_dir():
        print(f"bundle copy check skipped: {args.app} not installed")
        return 0

    index = bundle_index(args.app)
    checked = 0
    drift: list[tuple[Path, str]] = []
    orphan: list[Path] = []

    for root in COPY_ROOTS:
        for path in sorted(root.rglob("*.xml")):
            checked += 1
            versions = index.get(path.name)
            if not versions:
                # The vendor renamed or dropped it. Not drift — the copy may be
                # a deliberate record of a file a past build shipped — so it is
                # reported separately and does not fail the check.
                orphan.append(path)
                continue
            current = path.read_bytes()
            if digest(current) in versions:
                continue
            drift.append((path, sorted(versions)[0]))
            if args.refresh:
                path.write_bytes(next(iter(versions.values())))

    for path in orphan:
        print(f"  no bundle counterpart: {path}")
    for path, _ in drift:
        print(f"  {'refreshed' if args.refresh else 'STALE'}: {path}")

    if drift and not args.refresh:
        sys.exit(f"bundle copy check FAILED: {len(drift)} of {checked} copies differ from "
                 f"{args.app.name} — re-copy them, or run with --refresh, then re-extract "
                 f"the corpus (tools/extract_script_corpus.py)")
    print(f"bundle copy check passed: {checked} copies match the bundle"
          + (f", {len(drift)} refreshed" if drift else "")
          + (f", {len(orphan)} without a bundle counterpart" if orphan else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
