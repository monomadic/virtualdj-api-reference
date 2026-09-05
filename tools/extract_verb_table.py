#!/usr/bin/env python3
r"""Extract VirtualDJ's authoritative verb table from the binary.

This is a **serialised structure**, not a heuristic: a sorted array of 16-byte
records in `__DATA,__data`, each

    { const char *name; uint32 id; uint32 flags; }

1,028 records on VirtualDJ 2026, `action_deck` .. `zoom_vertical`. It is the
complete verb set — it covers 1,007/1,007 of the names the HTTP sweep proved real
— which makes membership both proof of existence AND, by absence, disproof.

It also settles aliases outright: **records sharing an `id` are the same verb**,
and `flags == 1` marks the alias/secondary spelling while the canonical carries
`flags == 0` (`auto_sync`=1 / `smart_play`=0, `config`=1 / `settings`=0). No
name-resemblance guessing required.

`flags` also carries the Button-Editor-hidden bit: 0 normal, 1 alias spelling,
256 hidden from the editor's browsable list (37 names, the "flag1-hidden" set).

Two further structures give each verb its **Button Editor category**: a
`const char *[38]` name array sitting after the verb table, and a non-decreasing
`uint8[distinct_ids + 1]` in `__TEXT,__const` indexed by `id + 1`. Both are located
structurally.

These are the same tables `extract_vdjscript_taxonomy.py` reads by hard-coded address on an
older build, so its identical per-category counts are a reproduction, not an independent
check — see rule 1c2 in docs/Evidence Standards.md. That older tool is where the provenance
comes from: it located them via `DLGActionWizard`, which is why they are the Button Editor's
categories and why `defines` is compiled but not displayed.

Located by anchoring rather than hard-coded addresses, so it survives builds: find
a known verb string in `__cstring`, find the record that points at it, then walk
outward while records stay valid. Note `nothing` legitimately has `id == 0`.

    python3 tools/extract_verb_table.py > tests/verb-table.json
    python3 tools/extract_verb_table.py --get hotcue
    python3 tools/extract_verb_table.py --check
    python3 tools/extract_verb_table.py --stamp   # the phrase to quote in prose
"""
import datetime
import json
import plistlib
import re
import struct
import sys
from pathlib import Path

BINARY = "/Applications/VirtualDJ.app/Contents/MacOS/VirtualDJ"
ARTIFACT = "tests/verb-table.json"
ANCHOR = "hot_cue"          # any verb certain to be in the table
CAT_ANCHOR = "audio_scratch"  # a distinctive Button Editor category name
# Bundle 18.0.9583 dropped the `const char *[38]` category-name array — none of the
# names survives anywhere in the executable, though the uint8 id -> category array
# still does. The order below is the array as it stands in two independent builds,
# 18.0.9246 (unstripped, read directly) and 18.0.9482 (the previous artifact); it is
# used ONLY as a fallback, and the summary records which source was used.
CATEGORY_NAMES = [
    "defines", "flow", "param", "repeat", "skin", "system", "variables", "window",
    "audio", "audio_controls", "audio_inputs", "audio_scratch", "audio_volumes",
    "automix", "browser", "config", "controllers", "cues", "deck_select",
    "equalizer", "get", "karaoke", "key", "loop", "macro", "pads", "pitch",
    "plugins", "poi", "prelisten", "rane", "record", "sampler", "sandbox", "sync",
    "text", "timecode", "video",
]
ARM64 = 0x0100000C
RECORD = 16
ARCH_NAMES = {0x0100000C: "arm64", 0x01000007: "x86_64"}


def build_identity(binary: str, cputype: int = ARM64) -> dict:
    """Which binary these counts describe.

    Every count in this artifact is a measurement of one build, so the build
    belongs *in* the artifact: a stamped figure in prose ("1,032 records on
    18.0.9598") is only trustworthy if the writer can copy the stamp instead
    of recalling it. `CFBundleVersion` is the build number VirtualDJ uses
    (`CFBundleShortVersionString` is the legacy 8.x display version).
    """
    path = Path(binary)
    ident = {"binary": binary, "arch": ARCH_NAMES.get(cputype, hex(cputype))}
    plist = path.parent.parent / "Info.plist"
    try:
        info = plistlib.loads(plist.read_bytes())
        ident["build"] = str(info.get("CFBundleVersion", "unknown"))
        if info.get("CFBundleShortVersionString"):
            ident["display_version"] = str(info["CFBundleShortVersionString"])
    except (OSError, plistlib.InvalidFileException):
        ident["build"] = "unknown"
    try:
        st = path.stat()
        ident["binary_bytes"] = st.st_size
        ident["binary_mtime"] = datetime.date.fromtimestamp(st.st_mtime).isoformat()
    except OSError:
        pass
    ident["extracted"] = datetime.date.today().isoformat()
    return ident


def stamp(summary: dict) -> str:
    """The exact phrase to quote in prose. Never write a bare count."""
    return (f"{summary['records']} records / {summary['distinct_ids']} distinct verbs / "
            f"{summary['alias_groups']} alias groups / {summary['hidden']} editor-hidden "
            f"on build {summary.get('build', 'unknown')} "
            f"({summary.get('arch', '?')}, extracted {summary.get('extracted', '?')})")


def slice_offset(data: bytes, cputype: int = ARM64) -> int:
    if struct.unpack_from(">I", data, 0)[0] not in (0xCAFEBABE, 0xCAFEBABF):
        return 0
    for i in range(struct.unpack_from(">I", data, 4)[0]):
        cpu, _sub, off, _size, _al = struct.unpack_from(">5I", data, 8 + i * 20)
        if cpu == cputype:
            return off
    raise SystemExit("no matching architecture slice")


def sections(data: bytes, base: int):
    ncmds = struct.unpack_from("<I", data, base + 16)[0]
    off, out = base + 32, []
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from("<II", data, off)
        if cmd == 0x19:  # LC_SEGMENT_64
            seg = data[off + 8:off + 24].rstrip(b"\0").decode()
            soff = off + 72
            for _s in range(struct.unpack_from("<I", data, off + 64)[0]):
                name = data[soff:soff + 16].rstrip(b"\0").decode()
                addr, size = struct.unpack_from("<QQ", data, soff + 32)
                fileoff = struct.unpack_from("<I", data, soff + 48)[0]
                out.append((seg, name, addr, size, fileoff))
                soff += 80
        off += cmdsize
    return out


def build(binary: str = BINARY) -> dict:
    data = open(binary, "rb").read()
    base = slice_offset(data)
    secs = sections(data, base)
    cseg = next(s for s in secs if s[1] == "__cstring")
    dseg = next(s for s in secs if s[0] == "__DATA" and s[1] == "__data")
    cblob = data[base + cseg[4]: base + cseg[4] + cseg[3]]
    dblob = data[base + dseg[4]: base + dseg[4] + dseg[3]]

    def string_at(addr: int):
        k = addr - cseg[2]
        if 0 <= k < len(cblob):
            end = cblob.find(b"\0", k)
            if end > k:
                try:
                    return cblob[k:end].decode("ascii")
                except UnicodeDecodeError:
                    return None
        return None

    def record(i: int):
        if i < 0 or i + RECORD > len(dblob):
            return None
        name = string_at(struct.unpack_from("<Q", dblob, i)[0])
        if not name or not name[0].islower():
            return None
        if not all(c.islower() or c.isdigit() or c == "_" for c in name):
            return None
        vid, flags = struct.unpack_from("<II", dblob, i + 8)
        # `nothing` carries id 0 — do not reject it.
        if vid > 0x10000 or flags > 0x10000:
            return None
        return {"name": name, "id": vid, "flags": flags}

    def find_string(text):
        k = cblob.find(b"\0" + text.encode() + b"\0")
        return cseg[2] + k + 1 if k >= 0 else None

    def category_names():
        """const char *[38] in __DATA,__data — located by anchoring on a member."""
        addr = find_string(CAT_ANCHOR)
        if addr is None:
            return []
        for i in range(0, len(dblob) - 8, 8):
            if struct.unpack_from("<Q", dblob, i)[0] == addr:
                lo = hi = i
                while lo - 8 >= 0:
                    s = string_at(struct.unpack_from("<Q", dblob, lo - 8)[0])
                    if s and s.replace("_", "").isalpha() and s.islower():
                        lo -= 8
                    else:
                        break
                while hi + 8 < len(dblob):
                    s = string_at(struct.unpack_from("<Q", dblob, hi + 8)[0])
                    if s and s.replace("_", "").isalpha() and s.islower():
                        hi += 8
                    else:
                        break
                return [string_at(struct.unpack_from("<Q", dblob, j)[0])
                        for j in range(lo, hi + 8, 8)]
        return []

    def category_of_id(n_ids, n_cats):
        """uint8[n_ids+1] in __TEXT,__const: non-decreasing, one entry per id.

        Found structurally, not by address: ids are allocated in category order, so
        the array is non-decreasing, exactly n_ids+1 long, and uses every category.
        Index with id+1.
        """
        tconst = next((s for s in secs if s[0] == "__TEXT" and s[1] == "__const"), None)
        if not tconst:
            return None
        blob = data[base + tconst[4]: base + tconst[4] + tconst[3]]
        want, limit = n_ids + 1, n_cats - 1
        i = 0
        while i < len(blob):
            run, prev = 0, -1
            j = i
            while j < len(blob) and blob[j] <= limit and blob[j] >= prev:
                prev = blob[j]
                run += 1
                j += 1
            if run == want and len(set(blob[i:j])) == n_cats:
                return list(blob[i:j])
            i = j + 1 if j > i else i + 1
        return None

    anchor_addr = None
    needle = b"\0" + ANCHOR.encode() + b"\0"
    k = cblob.find(needle)
    if k >= 0:
        anchor_addr = cseg[2] + k + 1
    if anchor_addr is None:
        raise SystemExit(f"anchor string {ANCHOR!r} not found in __cstring")
    anchor = None
    for i in range(0, len(dblob) - RECORD, 8):
        if struct.unpack_from("<Q", dblob, i)[0] == anchor_addr and record(i):
            anchor = i
            break
    if anchor is None:
        raise SystemExit(f"no record referencing {ANCHOR!r}")

    start = end = anchor
    while record(start - RECORD):
        start -= RECORD
    while record(end + RECORD):
        end += RECORD
    recs = [record(i) for i in range(start, end + RECORD, RECORD)]

    by_id = {}
    for r in recs:
        by_id.setdefault(r["id"], []).append(r["name"])
    groups = {str(k): sorted(v) for k, v in by_id.items() if len(v) > 1}

    cats, cats_source = category_names(), "binary"
    if not cats:  # 9583 and later: names gone, index array still present
        cats, cats_source = CATEGORY_NAMES, "pinned"
    cat_by_id = category_of_id(len(by_id), len(cats)) if cats else None
    if cat_by_id is None and cats_source == "pinned":
        cats, cats_source = [], "unresolved"
    verbs = {}
    for r in recs:
        rec = {"id": r["id"], "flags": r["flags"]}
        if cat_by_id and r["id"] + 1 < len(cat_by_id):
            rec["category"] = cats[cat_by_id[r["id"] + 1]]
        verbs[r["name"]] = rec
    counts = {}
    for rec in verbs.values():
        if "category" in rec:
            counts[rec["category"]] = counts.get(rec["category"], 0) + 1
    return {
        "summary": {
            **build_identity(binary),
            "address": hex(dseg[2] + start),
            "records": len(recs),
            "distinct_ids": len(by_id),
            "alias_groups": len(groups),
            "alias_forms": sum(1 for r in recs if r["flags"] == 1),
            "hidden": sum(1 for r in recs if r["flags"] == 256),
            "categories": len(cats),
            "categories_source": cats_source,
            "categorised": sum(1 for r in verbs.values() if "category" in r),
            "sorted": [r["name"] for r in recs] == sorted(r["name"] for r in recs),
        },
        "categories": cats,
        "category_counts": counts,
        "alias_groups": groups,
        "verbs": verbs,
    }


def cmd_get(name: str) -> None:
    data = json.load(open(ARTIFACT))
    rec = data["verbs"].get(name)
    if rec is None:
        print(json.dumps({"name": name, "in_verb_table": False,
                          "meaning": "NOT a verb on this build — the table is the "
                                     "complete verb set"}, indent=1))
        return
    siblings = [n for n, r in data["verbs"].items()
                if r["id"] == rec["id"] and n != name]
    out = {"name": name, "in_verb_table": True, **rec,
           "canonical": rec["flags"] != 1}
    if siblings:
        out["same_id_as"] = siblings
    print(json.dumps(out, indent=1))


def cmd_check() -> None:
    data = json.load(open(ARTIFACT))
    s = data["summary"]
    if s["records"] < 900 or not s["sorted"]:
        sys.exit(f"verb table extraction looks wrong: {s}")
    if len(data["verbs"]) != s["records"]:
        sys.exit("verb table summary does not match record count")
    if s.get("categorised", 0) != s["records"]:
        sys.exit(f"category mapping incomplete: {s.get('categorised')}/{s['records']}")
    print(f"verb table check passed: {s['records']} records @ {s['address']}, "
          f"{s['alias_groups']} alias groups, {s['alias_forms']} alias forms, "
          f"{s['hidden']} hidden, {s['categories']} categories "
          f"on build {s.get('build', 'unstamped')} ({s.get('arch', '?')})")
    if s.get("build", "unknown") == "unknown":
        sys.exit("verb table artifact carries no build stamp: re-extract so prose "
                 "can quote `--stamp` instead of recalling a build number")


def main() -> None:
    argv = sys.argv[1:]
    binary = BINARY
    if "--binary" in argv:
        i = argv.index("--binary")
        binary = argv[i + 1]
        del argv[i:i + 2]
    if len(argv) > 1 and argv[0] == "--get":
        return cmd_get(argv[1])
    if argv and argv[0] == "--check":
        return cmd_check()
    if argv and argv[0] == "--stamp":
        return print(stamp(json.load(open(ARTIFACT))["summary"]))
    print(json.dumps(build(binary), indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
