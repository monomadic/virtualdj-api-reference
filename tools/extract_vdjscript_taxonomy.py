#!/usr/bin/env python3
"""Extract the compiled Button Editor VDJScript taxonomy from VirtualDJ.

This reads the arm64 Mach-O tables used by DLGActionWizard. It is intentionally
build-specific: the default table addresses are from VirtualDJ 8.5.9307 /
bundle build 18.0.9336.
"""

from __future__ import annotations

import argparse
import csv
import json
import struct
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from zipfile import ZipFile


CPU_TYPES = {
    "x86_64": 0x01000007,
    "arm64": 0x0100000C,
}
DEFAULT_APP = Path("/Applications/VirtualDJ.app")
DEFAULT_CATEGORY_NAMES_VA = 0x10457A880
DEFAULT_ACTION_ITEMS_VA = 0x104576830
DEFAULT_CATEGORY_IDS_VA = 0x103D43974
ACTION_SENTINEL = 0x3BB
FAT_MAGIC = 0xCAFEBABE
FAT_MAGIC_64 = 0xCAFEBABF
MH_MAGIC_64 = 0xFEEDFACF
MH_CIGAM_64 = 0xCFFAEDFE
LC_SEGMENT_64 = 0x19


@dataclass(frozen=True)
class Segment:
    name: str
    vmaddr: int
    vmsize: int
    fileoff: int
    filesize: int


@dataclass(frozen=True)
class TaxonomyEntry:
    name: str
    category: str
    category_id: int
    action_id: int
    visible: bool
    flag0_hidden: bool
    flag1_hidden: bool
    flags: str
    in_language_catalog: bool


class MachOReader:
    def __init__(self, binary: Path, arch: str) -> None:
        self.binary = binary
        self.data = binary.read_bytes()
        cputype = CPU_TYPES[arch]
        self.slice_offset = self._slice_offset(cputype)
        self.segments: list[Segment] = []
        self._load_segments()

    def _slice_offset(self, cputype: int) -> int:
        magic = struct.unpack_from(">I", self.data, 0)[0]
        if magic not in (FAT_MAGIC, FAT_MAGIC_64):
            return 0

        nfat = struct.unpack_from(">I", self.data, 4)[0]
        offset = 8
        for _index in range(nfat):
            if magic == FAT_MAGIC_64:
                arch_cputype, _cpusubtype, arch_offset, _size, _align, _reserved = struct.unpack_from(
                    ">IIQQII", self.data, offset
                )
                offset += 32
            else:
                arch_cputype, _cpusubtype, arch_offset, _size, _align = struct.unpack_from(
                    ">IIIII", self.data, offset
                )
                offset += 20
            if arch_cputype == cputype:
                return arch_offset
        raise SystemExit(f"{self.binary} does not contain requested architecture cputype {cputype:#x}")

    def _load_segments(self) -> None:
        magic_le = struct.unpack_from("<I", self.data, self.slice_offset)[0]
        magic_be = struct.unpack_from(">I", self.data, self.slice_offset)[0]
        if magic_le == MH_MAGIC_64:
            endian = "<"
        elif magic_be == MH_MAGIC_64 or magic_le == MH_CIGAM_64:
            endian = ">"
        else:
            raise ValueError(f"unsupported Mach-O magic at slice offset {self.slice_offset:#x}")

        _magic, _cputype, _cpusubtype, _filetype, ncmds, _sizeofcmds, _flags, _reserved = struct.unpack_from(
            f"{endian}IiiIIIII", self.data, self.slice_offset
        )
        command_offset = self.slice_offset + 32
        for _index in range(ncmds):
            command, command_size = struct.unpack_from(f"{endian}II", self.data, command_offset)
            if command == LC_SEGMENT_64:
                name = self.data[command_offset + 8 : command_offset + 24].rstrip(b"\0").decode(
                    "ascii", errors="ignore"
                )
                vmaddr, vmsize, fileoff, filesize = struct.unpack_from(
                    f"{endian}QQQQ", self.data, command_offset + 24
                )
                self.segments.append(Segment(name, vmaddr, vmsize, fileoff, filesize))
            command_offset += command_size

    def offset(self, va: int) -> int:
        for segment in self.segments:
            if segment.vmaddr <= va < segment.vmaddr + segment.vmsize:
                return self.slice_offset + segment.fileoff + (va - segment.vmaddr)
        raise ValueError(f"virtual address {va:#x} is not inside a mapped segment")

    def u64(self, va: int) -> int:
        return struct.unpack_from("<Q", self.data, self.offset(va))[0]

    def u32(self, va: int) -> int:
        return struct.unpack_from("<I", self.data, self.offset(va))[0]

    def i8(self, va: int) -> int:
        return struct.unpack_from("b", self.data, self.offset(va))[0]

    def bytes_at(self, va: int, size: int) -> bytes:
        offset = self.offset(va)
        return self.data[offset : offset + size]

    def cstr(self, va: int) -> str:
        offset = self.offset(va)
        end = self.data.index(b"\0", offset)
        return self.data[offset:end].decode("utf-8", errors="replace")


def language_action_union(app: Path) -> set[str]:
    zip_path = app / "Contents/Resources/languages.zip"
    names: set[str] = set()
    with ZipFile(zip_path) as archive:
        for member in archive.namelist():
            if not member.endswith(".xml"):
                continue
            root = ET.fromstring(archive.read(member))
            actions = root.find("Actions")
            if actions is not None:
                names.update(child.tag for child in actions)
    return names


def category_names(reader: MachOReader, category_names_va: int) -> list[str]:
    names: list[str] = []
    for index in range(256):
        pointer = reader.u64(category_names_va + index * 8)
        if pointer == 0:
            return names
        names.append(reader.cstr(pointer))
    raise ValueError("category pointer list did not terminate within 256 entries")


def taxonomy_entries(
    reader: MachOReader,
    categories: list[str],
    language_names: set[str],
    action_items_va: int,
    category_ids_va: int,
) -> list[TaxonomyEntry]:
    entries: list[TaxonomyEntry] = []
    for table_index in range(4096):
        entry_va = action_items_va + table_index * 16
        name_pointer = reader.u64(entry_va)
        action_id = reader.u32(entry_va + 8)
        flags = reader.bytes_at(entry_va + 12, 4)
        if action_id == ACTION_SENTINEL:
            return entries
        category_id = reader.i8(category_ids_va + action_id)
        category = categories[category_id] if 0 <= category_id < len(categories) else f"unknown_{category_id}"
        name = reader.cstr(name_pointer)
        flag0_hidden = bool(flags[0] & 1)
        flag1_hidden = bool(flags[1] & 1)
        entries.append(
            TaxonomyEntry(
                name=name,
                category=category,
                category_id=category_id,
                action_id=action_id,
                visible=not flag0_hidden and not flag1_hidden,
                flag0_hidden=flag0_hidden,
                flag1_hidden=flag1_hidden,
                flags=flags.hex(),
                in_language_catalog=name in language_names,
            )
        )
    raise ValueError("action item table did not reach sentinel within 4096 entries")


def filtered_entries(entries: list[TaxonomyEntry], category: str | None, include_hidden: bool) -> list[TaxonomyEntry]:
    filtered = entries
    if category:
        filtered = [entry for entry in filtered if entry.category == category]
    if not include_hidden:
        filtered = [entry for entry in filtered if entry.visible]
    return filtered


def category_summary(entries: list[TaxonomyEntry], categories: list[str]) -> list[dict[str, object]]:
    by_category: dict[str, list[TaxonomyEntry]] = defaultdict(list)
    for entry in entries:
        by_category[entry.category].append(entry)

    rows: list[dict[str, object]] = []
    for category_id, category in enumerate(categories):
        if category == "defines":
            displayed = False
        else:
            displayed = True
        members = by_category.get(category, [])
        if not members and category == "defines":
            rows.append(
                {
                    "id": category_id,
                    "category": category,
                    "displayed": displayed,
                    "total": 0,
                    "visible": 0,
                    "flag0_hidden": 0,
                    "flag1_hidden": 0,
                    "examples": "",
                }
            )
            continue
        if not members:
            continue
        visible_examples = [entry.name for entry in members if entry.visible][:8]
        rows.append(
            {
                "id": category_id,
                "category": category,
                "displayed": displayed,
                "total": len(members),
                "visible": sum(entry.visible for entry in members),
                "flag0_hidden": sum(entry.flag0_hidden for entry in members),
                "flag1_hidden": sum(entry.flag1_hidden for entry in members),
                "examples": ", ".join(visible_examples),
            }
        )
    return rows


def print_summary(app: Path, arch: str, categories: list[str], entries: list[TaxonomyEntry]) -> None:
    visible = [entry for entry in entries if entry.visible]
    flag_counts = Counter((entry.flag0_hidden, entry.flag1_hidden) for entry in entries)
    language_names = {entry.name for entry in entries if entry.in_language_catalog}
    visible_names = {entry.name for entry in visible}

    print(f"App: {app}")
    print(f"Architecture: {arch}")
    print(f"Categories: {len(categories)} ({len(categories) - 1} displayed; 'defines' is skipped by the UI)")
    print(f"Compiled action items: {len(entries)}")
    print(f"Visible Button Editor actions: {len(visible)}")
    print(f"Flag0-hidden items: {flag_counts[(True, False)]}")
    print(f"Flag1-hidden items: {flag_counts[(False, True)]}")
    print(f"Language-catalog names in compiled table: {len(language_names)}")
    print(f"Visible compiled names not in language catalog: {len(visible_names - language_names)}")
    print(f"Language-catalog compiled names not visible: {len(language_names - visible_names)}")
    print()
    print("| ID | Category | Displayed | Total | Visible | Flag0 Hidden | Flag1 Hidden | Examples |")
    print("| ---: | --- | --- | ---: | ---: | ---: | ---: | --- |")
    for row in category_summary(entries, categories):
        print(
            f"| {row['id']} | `{row['category']}` | {str(row['displayed']).lower()} | "
            f"{row['total']} | {row['visible']} | {row['flag0_hidden']} | {row['flag1_hidden']} | "
            f"{row['examples']} |"
        )


def write_entries_csv(entries: list[TaxonomyEntry]) -> None:
    writer = csv.DictWriter(sys.stdout, fieldnames=list(asdict(entries[0]).keys()) if entries else [])
    writer.writeheader()
    for entry in entries:
        writer.writerow(asdict(entry))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=Path, default=DEFAULT_APP)
    parser.add_argument("--arch", choices=sorted(CPU_TYPES), default="arm64")
    parser.add_argument("--category", help="Limit action rows to one category")
    parser.add_argument("--include-hidden", action="store_true", help="Include entries hidden from the Button Editor list")
    parser.add_argument("--format", choices=("summary", "csv", "json", "names"), default="summary")
    parser.add_argument("--category-names-va", type=lambda text: int(text, 0), default=DEFAULT_CATEGORY_NAMES_VA)
    parser.add_argument("--action-items-va", type=lambda text: int(text, 0), default=DEFAULT_ACTION_ITEMS_VA)
    parser.add_argument("--category-ids-va", type=lambda text: int(text, 0), default=DEFAULT_CATEGORY_IDS_VA)
    args = parser.parse_args()

    reader = MachOReader(args.app / "Contents/MacOS/VirtualDJ", args.arch)
    language_names = language_action_union(args.app)
    categories = category_names(reader, args.category_names_va)
    entries = taxonomy_entries(reader, categories, language_names, args.action_items_va, args.category_ids_va)
    selected = filtered_entries(entries, args.category, args.include_hidden)

    if args.format == "summary":
        print_summary(args.app, args.arch, categories, entries)
    elif args.format == "csv":
        write_entries_csv(selected)
    elif args.format == "json":
        print(json.dumps([asdict(entry) for entry in selected], indent=2, sort_keys=True))
    elif args.format == "names":
        for entry in selected:
            print(entry.name)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
