#!/usr/bin/env python3
"""Which decoded controller archives this checkout knows about, and how to name one.

`controllers.dat` is keyed by BOTH the app build it shipped in and the archive's
own final block revision — `18.0.9598-r2241` — because the archive carries a
revision chain of its own (`blocks[].predecessor` → `revision`) and can move
independently of the bundle. The manifests under `tests/controllers-manifests/`
are committed (hashes and attributes only, no vendor XML), so two builds'
archives can be compared from the manifests alone; the decoded trees live under
the gitignored `vendor/controllers/<key>/`, one directory per key, so decoding
on a new machine ADDS a record instead of replacing the last one.

Stdlib only. Imported by the reader, the corpus extractor and the diff tool.
"""
from __future__ import annotations

import json
import plistlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "tests/controllers-manifests"
VENDOR_ROOT = ROOT / "vendor/controllers"
DEFAULT_APP = Path("/Applications/VirtualDJ.app")


def archive_key(manifest: dict) -> str:
    """`<bundle_version>-r<final revision>`, derived so old manifests need no new field."""
    return f"{manifest['bundle_version']}-r{manifest['blocks'][-1]['revision']}"


def manifest_path(key: str) -> Path:
    return MANIFEST_DIR / f"{key}.json"


def vendor_dir(key: str) -> Path:
    return VENDOR_ROOT / key


def load_manifest(key_or_path: str | Path) -> dict:
    """A key (`18.0.9598-r2241`), a bare bundle version (newest revision wins), or a path."""
    path = Path(key_or_path)
    if not path.exists():
        path = manifest_path(str(key_or_path))
    if not path.exists():
        found = find_manifest(bundle_version=str(key_or_path))
        if found is None:
            raise FileNotFoundError(f"no controller manifest for {key_or_path!r} under {MANIFEST_DIR}")
        path = found
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["_key"] = archive_key(manifest)
    manifest["_path"] = str(path)
    return manifest


def list_manifests() -> list[dict]:
    """Every committed manifest, newest build and revision last."""
    out = []
    for path in sorted(MANIFEST_DIR.glob("*.json")):
        m = json.loads(path.read_text(encoding="utf-8"))
        out.append({"key": archive_key(m), "path": path, "bundle_version": m["bundle_version"],
                    "revision": m["blocks"][-1]["revision"], "blocks": len(m["blocks"]),
                    "members": sum(b["member_count"] for b in m["blocks"]),
                    "roots": m.get("roots", {}), "source_sha256": m["source_sha256"],
                    "decoded_locally": vendor_dir(archive_key(m)).is_dir()})
    out.sort(key=lambda r: (_version_tuple(r["bundle_version"]), r["revision"]))
    return out


def installed_bundle_version(app: Path = DEFAULT_APP) -> str | None:
    plist = app / "Contents/Info.plist"
    if not plist.exists():
        return None
    return plistlib.loads(plist.read_bytes()).get("CFBundleVersion")


def find_manifest(bundle_version: str | None = None, app: Path | None = None) -> Path | None:
    """The manifest for a build (newest revision if several), or for the installed app."""
    if bundle_version is None and app is not None:
        bundle_version = installed_bundle_version(app)
    if bundle_version is None:
        return None
    rows = [r for r in list_manifests() if r["bundle_version"] == bundle_version]
    return rows[-1]["path"] if rows else None


def _version_tuple(v: str) -> tuple:
    return tuple(int(p) if p.isdigit() else p for p in v.split("."))


if __name__ == "__main__":
    import sys
    as_json = "--format=json" in sys.argv
    rows = list_manifests()
    installed = installed_bundle_version()
    if as_json:
        print(json.dumps({"installed_bundle_version": installed,
                          "archives": [{**r, "path": str(r["path"])} for r in rows]}, indent=1))
        sys.exit(0)
    if not rows:
        print(f"no controller manifests under {MANIFEST_DIR} — run `just controllers-vendor`")
        sys.exit(0)
    print(f"{'key':<22} {'members':>7} {'blocks':>6}  roots                          decoded here  ")
    for r in rows:
        roots = ", ".join(f"{k}={v}" for k, v in r["roots"].items())
        mark = "yes" if r["decoded_locally"] else "no"
        here = "  <- installed" if r["bundle_version"] == installed else ""
        print(f"{r['key']:<22} {r['members']:>7} {r['blocks']:>6}  {roots:<30} {mark:<12}{here}")
    if installed and not any(r["bundle_version"] == installed for r in rows):
        print(f"installed build {installed} has no manifest yet — run `just controllers-vendor` to add one")
