#!/usr/bin/env python3
"""Fetch the Atomix plugin SDK headers into vendor/vdj-sdk/.

This repo does NOT vendor these headers. They carry "(c)Atomix Productions
2011-2018" with no license text, and the download page states no terms of use or
redistribution conditions, so redistributing them is not something this repo
does — `vendor/` is gitignored. Fetching your own copy is a different act, and
this automates that.

    python3 tools/download_sdk.py            # fetch if absent
    python3 tools/download_sdk.py --force    # re-fetch over an existing copy
    python3 tools/download_sdk.py --check    # report presence, fetch nothing

`tools/plugin/build.sh` finds the headers by searching `vendor/` for
`vdjPlugin8.h`, so the exact subdirectory is a convention rather than a
requirement; `VDJ_SDK=<dir>` overrides it entirely.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import sys
import urllib.error
import urllib.request
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "vendor" / "vdj-sdk"
PAGE = "https://www.virtualdj.com/wiki/PluginSDK8.html"
URL = "https://www.virtualdj.com/developers/VirtualDJ8_SDK_20211003.zip"
# The header the build script anchors on. Its presence is what "installed" means.
ANCHOR = "vdjPlugin8.h"
STAMP = "SOURCE.txt"


def present() -> Path | None:
    """The directory under vendor/ holding the anchor header, if any."""
    hits = sorted((ROOT / "vendor").rglob(ANCHOR)) if (ROOT / "vendor").exists() else []
    return hits[0].parent if hits else None


def fetch() -> bytes:
    request = urllib.request.Request(URL, headers={"User-Agent": "curl/8"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true", help="re-fetch over an existing copy")
    ap.add_argument("--check", action="store_true", help="report presence; fetch nothing")
    args = ap.parse_args()

    where = present()
    if args.check:
        if where:
            print(f"SDK headers present: {where.relative_to(ROOT)}")
            return 0
        print(f"SDK headers absent — `just download-sdk` fetches them into "
              f"{DEST.relative_to(ROOT)}/")
        return 1

    if where and not args.force:
        print(f"already present: {where.relative_to(ROOT)} (--force to re-fetch)")
        return 0

    print(f"fetching {URL}")
    try:
        blob = fetch()
    except (urllib.error.URLError, OSError) as exc:
        sys.exit(f"download failed: {exc}\n  The SDK is linked from {PAGE}; fetch it "
                 f"by hand and unzip into {DEST.relative_to(ROOT)}/ if the URL has moved.")

    if not blob.startswith(b"PK"):
        sys.exit(f"not a zip ({len(blob)} bytes) — the URL may now serve a login or error "
                 f"page. Check {PAGE}.")

    DEST.mkdir(parents=True, exist_ok=True)
    written = []
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        for info in archive.infolist():
            # Flatten and refuse anything that tries to escape the destination.
            # The archive ships three headers at its root today; a future one
            # with a folder should still land under vendor/vdj-sdk/.
            name = Path(info.filename).name
            if info.is_dir() or not name or not name.endswith(".h"):
                continue
            (DEST / name).write_bytes(archive.read(info))
            written.append(name)

    if ANCHOR not in written:
        sys.exit(f"archive did not contain {ANCHOR} (got: {', '.join(written) or 'nothing'})")

    # Stamp what was fetched. These headers are unversioned inside the archive,
    # so the URL, the date and the digest are the only record of WHICH SDK a
    # plugin was built against.
    (DEST / STAMP).write_text(
        f"VirtualDJ plugin SDK headers — third party, NOT redistributed by this repo.\n"
        f"Fetched:  {date.today().isoformat()} by tools/download_sdk.py\n"
        f"From:     {URL}\n"
        f"Linked:   {PAGE}\n"
        f"sha256:   {hashlib.sha256(blob).hexdigest()}\n"
        f"Contents: {', '.join(sorted(written))}\n"
        f"\n"
        f"The headers carry \"(c)Atomix Productions 2011-2018\" with no license text,\n"
        f"and the download page states no terms. vendor/ is gitignored for that\n"
        f"reason; do not commit these files.\n")

    print(f"wrote {len(written)} headers to {DEST.relative_to(ROOT)}/: {', '.join(sorted(written))}")
    print(f"provenance recorded in {(DEST / STAMP).relative_to(ROOT)}")
    print("tools/plugin/build.sh will now find them; `just plugin-build` is unblocked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
