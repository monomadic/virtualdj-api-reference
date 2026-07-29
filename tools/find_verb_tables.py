#!/usr/bin/env python3
r"""Find SERIALISED verb-name tables in the VirtualDJ binary.

`strings` plus adjacency only shows that literals were pooled near each other by
the compiler; it does not prove they form a table. This tool looks for the actual
structure: a contiguous run of pointer-sized words in a data section, each of
which resolves to a C string in `__cstring` that looks like a verb name. A run
like that IS a serialised array of `const char *`, which is provable grouping.

    python3 tools/find_verb_tables.py                # report runs
    python3 tools/find_verb_tables.py --dump N       # print members of run N
    python3 tools/find_verb_tables.py --names        # emit every name found, one per line

Handles the universal binary (one report per slice) and dyld chained fixups,
where a stored word is not a plain address: candidate interpretations are tried
per slice and the one that resolves the most strings wins.
"""
import struct
import sys
from collections import namedtuple

BINARY = "/Applications/VirtualDJ.app/Contents/MacOS/VirtualDJ"
MIN_RUN = 8

Section = namedtuple("Section", "seg name addr size offset")


def slices(data: bytes):
    magic = struct.unpack_from(">I", data, 0)[0]
    if magic in (0xCAFEBABE, 0xCAFEBABF):
        count = struct.unpack_from(">I", data, 4)[0]
        out = []
        for i in range(count):
            cpu, _sub, off, size, _al = struct.unpack_from(">5I", data, 8 + i * 20)
            out.append((cpu, off, size))
        return out
    return [(0, 0, len(data))]


def sections(data: bytes, base: int):
    """Parse LC_SEGMENT_64 load commands into a section list."""
    ncmds = struct.unpack_from("<I", data, base + 16)[0]
    off = base + 32
    out = []
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from("<II", data, off)
        if cmd == 0x19:  # LC_SEGMENT_64
            segname = data[off + 8:off + 24].rstrip(b"\0").decode()
            nsects = struct.unpack_from("<I", data, off + 64)[0]
            soff = off + 72
            for _s in range(nsects):
                name = data[soff:soff + 16].rstrip(b"\0").decode()
                addr, size = struct.unpack_from("<QQ", data, soff + 32)
                fileoff = struct.unpack_from("<I", data, soff + 48)[0]
                out.append(Section(segname, name, addr, size, fileoff))
                soff += 80
        off += cmdsize
    return out


def cstrings(data: bytes, base: int, sect: Section):
    """Map virtual address -> string for every C string in the section."""
    blob = data[base + sect.offset: base + sect.offset + sect.size]
    table, start = {}, 0
    while True:
        end = blob.find(b"\0", start)
        if end < 0:
            break
        if end > start:
            try:
                table[sect.addr + start] = blob[start:end].decode("ascii")
            except UnicodeDecodeError:
                pass
        start = end + 1
    return table


def is_verby(text: str) -> bool:
    return (2 <= len(text) <= 42 and text[0].islower()
            and all(c.islower() or c.isdigit() or c == "_" for c in text))


def scan(data: bytes, base: int, name: str):
    secs = sections(data, base)
    cs = {}
    for s in secs:
        if s.name == "__cstring":
            cs.update(cstrings(data, base, s))
    if not cs:
        return []
    lo, hi = min(cs), max(cs)
    # Chained fixups store a target offset rather than a live address; try the raw
    # value and a few plausible rebases, then keep whichever resolves most strings.
    slide_candidates = [0, lo & ~0xFFFFFFFF, secs[0].addr]
    best, best_hits = 0, -1
    for slide in slide_candidates:
        hits = 0
        for s in secs:
            if s.seg.startswith("__DATA") or s.name in ("__const", "__cfstring"):
                blob = data[base + s.offset: base + s.offset + min(s.size, 4_000_000)]
                for i in range(0, len(blob) - 8, 8):
                    word = struct.unpack_from("<Q", blob, i)[0] + slide
                    if lo <= word <= hi and word in cs:
                        hits += 1
        if hits > best_hits:
            best, best_hits = slide, hits
    runs = []
    for s in secs:
        if not (s.seg.startswith("__DATA") or s.name in ("__const",)):
            continue
        blob = data[base + s.offset: base + s.offset + s.size]
        cur, cur_addr = [], None
        for i in range(0, len(blob) - 8, 8):
            word = struct.unpack_from("<Q", blob, i)[0] + best
            text = cs.get(word) if lo <= word <= hi else None
            if text is not None and is_verby(text):
                if not cur:
                    cur_addr = s.addr + i
                cur.append(text)
            else:
                if len(cur) >= MIN_RUN:
                    runs.append((f"{name}:{s.seg},{s.name}", cur_addr, cur))
                cur, cur_addr = [], None
        if len(cur) >= MIN_RUN:
            runs.append((f"{name}:{s.seg},{s.name}", cur_addr, cur))
    return runs


def packed_blobs(data: bytes, base: int, label: str, secs):
    """Find contiguous, strictly-sorted, NUL-separated identifier blobs in __cstring.

    Byte-exact: every member must abut the next (delta == len+1) with no interleaved
    strings, and the sequence must ascend. That contiguity is the provable structure —
    unlike `strings` adjacency, nothing unrelated can be sitting between members.
    """
    out = []
    for s in secs:
        if s.name != "__cstring":
            continue
        blob = data[base + s.offset: base + s.offset + s.size]
        pos, cur, start = 0, [], None
        while pos < len(blob):
            end = blob.find(b"\0", pos)
            if end < 0:
                break
            try:
                text = blob[pos:end].decode("ascii")
            except UnicodeDecodeError:
                text = None
            ok = text is not None and is_verby(text) and (not cur or text > cur[-1])
            if ok:
                if not cur:
                    start = pos
                cur.append(text)
            else:
                if len(cur) >= 40:
                    out.append((f"{label}:__cstring(packed)", s.addr + start, cur))
                cur, start = [], None
            pos = end + 1
        if len(cur) >= 40:
            out.append((f"{label}:__cstring(packed)", s.addr + start, cur))
    return out


def main() -> None:
    data = open(BINARY, "rb").read()
    all_runs = []
    for cpu, off, _size in slices(data):
        label = {0x0100000C: "arm64", 0x01000007: "x86_64"}.get(cpu, f"cpu{cpu}")
        secs = sections(data, off)
        all_runs += scan(data, off, label)
        all_runs += packed_blobs(data, off, label, secs)
    all_runs.sort(key=lambda r: -len(r[2]))
    if "--names" in sys.argv:
        seen = set()
        for _, _, names in all_runs:
            seen.update(names)
        for n in sorted(seen):
            print(n)
        return
    if "--dump" in sys.argv:
        idx = int(sys.argv[sys.argv.index("--dump") + 1])
        where, addr, names = all_runs[idx]
        print(f"run {idx}: {where} @ 0x{addr:x}, {len(names)} entries")
        for n in names:
            print(" ", n)
        return
    print(f"pointer runs of >={MIN_RUN} verb-like C strings: {len(all_runs)}")
    for i, (where, addr, names) in enumerate(all_runs[:12]):
        print(f"  [{i}] {where:34} @ 0x{addr:010x}  {len(names):>5} entries  "
              f"{names[0]} .. {names[-1]}")
    total = set()
    for _, _, names in all_runs:
        total.update(names)
    print(f"distinct names across all runs: {len(total)}")


if __name__ == "__main__":
    main()
