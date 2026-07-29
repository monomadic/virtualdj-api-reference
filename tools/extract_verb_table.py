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

Located by anchoring rather than hard-coded addresses, so it survives builds: find
a known verb string in `__cstring`, find the record that points at it, then walk
outward while records stay valid. Note `nothing` legitimately has `id == 0`.

    python3 tools/extract_verb_table.py > tests/verb-table.json
    python3 tools/extract_verb_table.py --get hotcue
    python3 tools/extract_verb_table.py --check
"""
import json
import struct
import sys

BINARY = "/Applications/VirtualDJ.app/Contents/MacOS/VirtualDJ"
ARTIFACT = "tests/verb-table.json"
ANCHOR = "hot_cue"          # any verb certain to be in the table
ARM64 = 0x0100000C
RECORD = 16


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


def build() -> dict:
    data = open(BINARY, "rb").read()
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
    return {
        "summary": {
            "address": hex(dseg[2] + start),
            "records": len(recs),
            "distinct_ids": len(by_id),
            "alias_groups": len(groups),
            "alias_forms": sum(1 for r in recs if r["flags"] == 1),
            "sorted": [r["name"] for r in recs] == sorted(r["name"] for r in recs),
        },
        "alias_groups": groups,
        "verbs": {r["name"]: {"id": r["id"], "flags": r["flags"]} for r in recs},
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
    print(f"verb table check passed: {s['records']} records @ {s['address']}, "
          f"{s['alias_groups']} alias groups, {s['alias_forms']} alias forms")


def main() -> None:
    if len(sys.argv) > 2 and sys.argv[1] == "--get":
        return cmd_get(sys.argv[2])
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        return cmd_check()
    print(json.dumps(build(), indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
