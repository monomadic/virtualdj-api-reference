#!/usr/bin/env python3
"""What changed in controllers.dat between two builds, from the committed manifests alone.

    python3 tools/controllers_diff.py 18.0.9583-r2237 18.0.9598-r2241
    python3 tools/controllers_diff.py 18.0.9583 18.0.9598          # bundle versions resolve too
    python3 tools/controllers_diff.py A B --format=json
    python3 tools/controllers_diff.py A B --root mapper            # one XML root only

Needs no decoded tree: every manifest carries a SHA-256, byte count and root
attributes per member, so added, removed and changed members are visible on a
machine that has never held either archive. What changed INSIDE a changed
member needs both trees decoded (`vendor/controllers/<key>/block-*/<name>`),
and `--show-paths` prints the pair to hand to `diff` when both are present.

Tier 2: this is vendor packaging evidence, not hardware behavior.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from controller_archives import load_manifest, vendor_dir  # noqa: E402


def members(manifest: dict) -> dict[str, dict]:
    out = {}
    for index, block in enumerate(manifest["blocks"]):
        for m in block["members"]:
            out[m["name"]] = {**m, "block": index, "revision": block["revision"]}
    return out


def diff(a: dict, b: dict, root: str | None) -> dict:
    ma, mb = members(a), members(b)
    if root:
        ma = {k: v for k, v in ma.items() if v["root"] == root}
        mb = {k: v for k, v in mb.items() if v["root"] == root}
    added = sorted(set(mb) - set(ma))
    removed = sorted(set(ma) - set(mb))
    changed, attr_only = [], []
    for name in sorted(set(ma) & set(mb)):
        x, y = ma[name], mb[name]
        if x["sha256"] != y["sha256"]:
            changed.append({"name": name, "root": y["root"], "bytes": [x["bytes"], y["bytes"]],
                            "attributes_changed": x["attributes"] != y["attributes"]})
        elif x["attributes"] != y["attributes"]:
            attr_only.append(name)
    return {
        "from": {"key": a["_key"], "source_sha256": a["source_sha256"], "members": len(ma)},
        "to": {"key": b["_key"], "source_sha256": b["source_sha256"], "members": len(mb)},
        "root_filter": root,
        "identical_archive": a["source_sha256"] == b["source_sha256"],
        "added": [{"name": n, "root": mb[n]["root"], "bytes": mb[n]["bytes"]} for n in added],
        "removed": [{"name": n, "root": ma[n]["root"], "bytes": ma[n]["bytes"]} for n in removed],
        "changed": changed,
        "unchanged": len(set(ma) & set(mb)) - len(changed),
        "attributes_only": attr_only,
        "by_root": {r: {"added": sum(1 for n in added if mb[n]["root"] == r),
                        "removed": sum(1 for n in removed if ma[n]["root"] == r),
                        "changed": sum(1 for c in changed if c["root"] == r)}
                    for r in sorted({*(m["root"] for m in ma.values()),
                                     *(m["root"] for m in mb.values())})},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("older", help="archive key, bundle version, or manifest path")
    parser.add_argument("newer", help="archive key, bundle version, or manifest path")
    parser.add_argument("--root", choices=["device", "mapper", "audio"])
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--show-paths", action="store_true",
                        help="for each changed member, the two decoded paths (when both trees exist)")
    args = parser.parse_args()
    a, b = load_manifest(args.older), load_manifest(args.newer)
    result = diff(a, b, args.root)
    if args.format == "json":
        print(json.dumps(result, indent=1, ensure_ascii=False))
        return 0
    print(f"{result['from']['key']} -> {result['to']['key']}"
          + (f" ({args.root} only)" if args.root else ""))
    if result["identical_archive"]:
        print("identical controllers.dat (same source sha256)")
        return 0
    print(f"members {result['from']['members']} -> {result['to']['members']}: "
          f"{len(result['added'])} added, {len(result['removed'])} removed, "
          f"{len(result['changed'])} changed, {result['unchanged']} unchanged")
    for r, c in result["by_root"].items():
        print(f"  {r:<7} +{c['added']} -{c['removed']} ~{c['changed']}")
    for label, rows in (("added", result["added"]), ("removed", result["removed"])):
        for m in rows:
            print(f"{'+' if label == 'added' else '-'} [{m['root']}] {m['name']} ({m['bytes']} B)")
    for c in result["changed"]:
        x, y = c["bytes"]
        print(f"~ [{c['root']}] {c['name']} ({x} -> {y} B"
              + (", attributes changed" if c["attributes_changed"] else "") + ")")
        if args.show_paths:
            for m, key in ((a, "old"), (b, "new")):
                p = vendor_dir(m["_key"]) / f"block-{members(m)[c['name']]['block']:03d}" / c["name"]
                print(f"    {key}: {p}" + ("" if p.exists() else "  (not decoded here)"))
    for n in result["attributes_only"]:
        print(f"? attributes differ, bytes identical: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
