#!/usr/bin/env python3
"""Resolve every ACTION_ class vtable slot to a named method.

Requires an *unstripped* VirtualDJ binary. Bundle 18.0.9246 (app 8.5.8769) is
the last known build shipping a full symbol table: 321,571 nm entries including
952 `vtable for ACTION_*` symbols and 5,325 `ACTION_*::` method symbols.
Bundle 18.0.9482 and later are stripped to ~1,210 exports/imports, where only
`tools/extract_action_contracts.py` (RTTI + vtable walk, unnamed slots) works.

Slot indices match `tests/action-contracts.json`: 0/1 are the destructor pair,
2 is the first virtual method. Output: {class: [slot symbol, ...]}.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import subprocess
import sys
from collections import Counter
from pathlib import Path

DEFAULT_APP = Path("/Applications/VirtualDJ.app")
CPU_TYPE_ARM64 = 0x0100000C
FAT_MAGICS = (0xCAFEBABE, 0xCAFEBABF)
MAX_SLOTS = 40

SYMBOL_LINE = re.compile(
    r"^([0-9a-f]{16}) \(([^)]*)\) "
    r"(?:non-external \(was a private external\) |non-external |private external |"
    r"weak private external |weak external |external )?(.*)$"
)
SECTION = re.compile(
    r"sectname (\S+)\n\s+segname (\S+)\n\s+addr 0x([0-9a-f]+)\n"
    r"\s+size 0x([0-9a-f]+)\n\s+offset (\d+)"
)


def demangled(binary: Path, arch: str) -> list[str]:
    raw = subprocess.check_output(["nm", "-arch", arch, "-m", str(binary)], text=True)
    return subprocess.check_output(["c++filt"], input=raw, text=True).splitlines()


def symbol_maps(lines: list[str]) -> tuple[dict[int, str], dict[str, int]]:
    """address -> shortest symbol name, and ACTION_ class -> vtable address."""
    by_address: dict[int, str] = {}
    vtables: dict[str, int] = {}
    for line in lines:
        match = SYMBOL_LINE.match(line)
        if not match:
            continue
        address, name = int(match.group(1), 16), match.group(3)
        if address not in by_address or len(name) < len(by_address[address]):
            by_address[address] = name
        if name.startswith("vtable for ACTION_"):
            vtables[name[len("vtable for "):]] = address
    return by_address, vtables


def sections(binary: Path, arch: str) -> list[tuple[int, int, int]]:
    load = subprocess.check_output(["otool", "-arch", arch, "-l", str(binary)], text=True)
    return [
        (int(addr, 16), int(size, 16), int(offset))
        for _, _, addr, size, offset in SECTION.findall(load)
    ]


def slice_offset(data: bytes, cpu_type: int) -> int:
    if struct.unpack(">I", data[:4])[0] not in FAT_MAGICS:
        return 0
    for i in range(struct.unpack(">I", data[4:8])[0]):
        head = 8 + i * 20
        cpu, _sub, offset, _size, _align = struct.unpack(">5I", data[head:head + 20])
        if cpu == cpu_type:
            return offset
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=Path, default=DEFAULT_APP)
    parser.add_argument("--arch", default="arm64")
    parser.add_argument("--json", type=Path, help="write {class: [slot symbol]} here")
    args = parser.parse_args()

    binary = args.app / "Contents/MacOS/VirtualDJ"
    by_address, vtables = symbol_maps(demangled(binary, args.arch))
    if not vtables:
        print(f"No `vtable for ACTION_*` symbols in {binary} — this build is stripped.",
              file=sys.stderr)
        return 1

    secs = sections(binary, args.arch)
    data = binary.read_bytes()
    base = slice_offset(data, CPU_TYPE_ARM64)
    code = [(addr, size) for addr, size, _ in secs if 0x100000000 <= addr < 0x104000000]

    def qword(address: int) -> int | None:
        for addr, size, offset in secs:
            if addr <= address < addr + size:
                start = base + offset + (address - addr)
                return struct.unpack("<Q", data[start:start + 8])[0]
        return None

    def is_code(pointer: int) -> bool:
        return any(addr <= pointer < addr + size for addr, size in code)

    table: dict[str, list[str]] = {}
    for cls, vtable in sorted(vtables.items()):
        slots = []
        for index in range(2, MAX_SLOTS):  # 0 offset-to-top, 1 typeinfo
            pointer = qword(vtable + index * 8)
            if pointer is None:
                break
            pointer &= 0x7FFFFFFFFFFF
            if not is_code(pointer):
                break
            slots.append(by_address.get(pointer, hex(pointer)))
        table[cls] = slots

    print(f"ACTION_ classes with a resolved vtable: {len(table)}")
    print(f"vtable length histogram: {Counter(len(v) for v in table.values()).most_common()}")
    if args.json:
        args.json.write_text(json.dumps(table, indent=1) + "\n")
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
