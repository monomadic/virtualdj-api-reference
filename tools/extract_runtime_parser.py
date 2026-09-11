#!/usr/bin/env python3
"""Capture bounded x86_64 binary evidence for VirtualDJ's action parser.

This is a structural extractor.  It records symbol identity, exact
LC_FUNCTION_STARTS bounds, bounded disassembly, direct calls, indirect call
sites, and disassembly references.  It does not infer parser behavior or
claim exhaustive transitive coverage.
"""
from __future__ import annotations

import argparse
import bisect
import datetime
import hashlib
import json
import plistlib
import re
import struct
import subprocess
from pathlib import Path

TARGETS = {
    "IAction::create": "IAction::create",
    "IAction::stringGetParam": "IAction::stringGetParam",
    "IAction::stringMatch": "IAction::stringMatch",
    "IAction::deckMatch": "IAction::deckMatch",
    "IAction::getParamEval": "IAction::getParamEval",
    "IAction::getFloatParamEval": "IAction::getFloatParamEval",
    "IAction::getParam": "IAction::getParam",
    "IAction::getFloatParam": "IAction::getFloatParam",
    "IAction::getBoolParam": "IAction::getBoolParam",
    "IAction::getListParam": "IAction::getListParam",
    "IAction::paramToString": "IAction::paramToString",
    "numberMatch": "numberMatch",
    "IAction::getDeckFromString": "IAction::getDeckFromString",
    "IAction::setSource": "IAction::setSource",
    "SActionParam::toFloat": "SActionParam::toFloat",
    "SActionParam::toInt": "SActionParam::toInt",
    "ACTION_constant::onQuery": "ACTION_constant::onQuery",
    "ACTION_get_text::onQuery": "ACTION_get_text::onQuery",
    "ACTION_param_add::onQuery": "ACTION_param_add::onQuery",
    "IParamValuesAction::getValues(SActionParam*, SActionParam*)": "IParamValuesAction::getValues(SActionParam*, SActionParam*)",
    "IParamValuesAction::getValues(float*, float*)": "IParamValuesAction::getValues(float*, float*)",
    "actionGetText": "actionGetText",
    "IAction::query": "IAction::query",
    "IAction::queryText": "IAction::queryText",
    "IAction::execute": "IAction::execute",
    "DLGActionWizard::updateList": "DLGActionWizard::updateList",
    "DLGActionWizard::getCurrentWord": "DLGActionWizard::getCurrentWord",
    "DLGActionWizard::onChanged": "DLGActionWizard::onChanged",
    "DLGActionWizard::updateHint": "DLGActionWizard::updateHint",
    "ACTION_zoom::onExecute": "ACTION_zoom::onExecute",
    "IActionSwitch::onExecute": "IActionSwitch::onExecute",
    "ACTION_beatlock::setValue": "ACTION_beatlock::setValue",
    "getDeckSafe": "getDeckSafe",
    "getDeck": "getDeck",
    "ACTION_select::onExecute": "ACTION_select::onExecute",
    "CDeck::select": "CDeck::select",
    "ACTION_all_decks::onExecute": "ACTION_all_decks::onExecute",
    "createAction_all_decks": "createAction_all_decks",
    "ACTION_all_decks::init": "ACTION_all_decks::init",
    "IAction::queryValue": "IAction::queryValue",
    "IAction::queryBool": "IAction::queryBool",
    "createAction_combine_query": "createAction_combine_query(IAction*)",
    "isLeftCI": "isLeftCI(char const*, char const*)",
    "strIsEqualCI": "strIsEqualCI(char const*, char const*)",
    "matchStringWithFlag": "matchStringWithFlag",
    "isLeftCI(string_view, char const*)": "isLeftCI(std::__1::basic_string_view<char, std::__1::char_traits<char>>, char const*)",
    "strIsEqualCI(string_view, string_view)": "strIsEqualCI(std::__1::basic_string_view<char, std::__1::char_traits<char>>, std::__1::basic_string_view<char, std::__1::char_traits<char>>)",
    "CDeck::getActiveDeck": "CDeck::getActiveDeck",
}
STREE_PREFIX = "DLGActionWizard::STree::"
NM_RE = re.compile(r"^([0-9a-fA-F]+)\s+([tTuUwW])\s+(\S+)$")
ADDR_RE = re.compile(r"^([0-9a-f]{16})\s+(.*)$")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def x86_slice(data: bytes) -> int:
    magic = struct.unpack_from(">I", data)[0]
    if magic not in (0xCAFEBABE, 0xCAFEBABF):
        return 0
    n = struct.unpack_from(">I", data, 4)[0]
    for i in range(n):
        off = 8 + i * (32 if magic == 0xCAFEBABF else 20)
        cpu = struct.unpack_from(">I", data, off)[0]
        if cpu == 0x01000007:
            return struct.unpack_from(">Q" if magic == 0xCAFEBABF else ">I", data, off + 8)[0]
    raise ValueError("x86_64 slice not present")


def function_starts(binary: Path) -> list[int]:
    data, base = binary.read_bytes(), x86_slice(binary.read_bytes())
    magic = struct.unpack_from("<I", data, base)[0]
    if magic != 0xFEEDFACF:
        raise ValueError(f"expected 64-bit Mach-O slice, got {magic:#x}")
    ncmds = struct.unpack_from("<I", data, base + 16)[0]
    p = base + 32
    text_vm = None
    cmd_data = None
    for _ in range(ncmds):
        cmd, size = struct.unpack_from("<II", data, p)
        if cmd == 0x19 and data[p + 8:p + 24].rstrip(b"\0") == b"__TEXT":
            text_vm = struct.unpack_from("<Q", data, p + 24)[0]
        if cmd == 0x26:
            off, length = struct.unpack_from("<II", data, p + 8)
            cmd_data = data[base + off:base + off + length]
        p += size
    if text_vm is None or cmd_data is None:
        raise ValueError("missing __TEXT or LC_FUNCTION_STARTS")
    out, address, value, shift = [], text_vm, 0, 0
    for byte in cmd_data:
        value |= (byte & 0x7f) << shift
        if byte & 0x80:
            shift += 7
            continue
        if value == 0:
            break
        address += value
        out.append(address)
        value, shift = 0, 0
    return out


def symbols(binary: Path) -> tuple[dict[str, int], dict[int, list[str]]]:
    raw = subprocess.check_output(["nm", "-arch", "x86_64", str(binary)], text=True)
    by_name, by_addr = {}, {}
    for line in raw.splitlines():
        m = NM_RE.match(line)
        if not m:
            continue
        address, kind, name = int(m[1], 16), m[2], m[3]
        if kind.lower() == "t":
            by_name[name] = address
            by_addr.setdefault(address, []).append(name)
    demangled = subprocess.check_output(["c++filt"], input="\n".join(by_name), text=True).splitlines()
    demap = {}
    for mangled, pretty in zip(by_name, demangled):
        demap.setdefault(pretty, []).append((mangled, by_name[mangled]))
    return {pretty: vals[0][1] for pretty, vals in demap.items()}, by_addr


def bounded_disassembly(binary: Path, mangled: str, start: int, end: int) -> str:
    proc = subprocess.Popen(["otool", "-arch", "x86_64", "-tV", "-p", mangled, str(binary)],
                            stdout=subprocess.PIPE, text=True)
    lines = []
    reached = False
    assert proc.stdout is not None
    for line in proc.stdout:
        m = ADDR_RE.match(line)
        if m:
            address = int(m[1], 16)
            if address >= end:
                reached = True
                break
            if address < start:
                continue
            lines.append(line)
    if reached:
        proc.terminate()
    proc.stdout.close()
    code = proc.wait()
    if not reached and code != 0:
        raise RuntimeError(f"otool failed for {mangled}: exit {code}")
    if not lines:
        raise RuntimeError(f"empty disassembly for {mangled}")
    return f"{mangled} [{start:#x}, {end:#x}):\n" + "".join(lines)


def sites(body: str, address_names: dict[int, list[str]], mangled_addresses: dict[str, int]) -> tuple[list[dict], list[dict], list[dict]]:
    direct, indirect, literals = [], [], []
    for line in body.splitlines():
        m = ADDR_RE.match(line)
        if not m:
            continue
        pc, instruction = int(m[1], 16), m[2]
        call = re.search(r"\bcallq?\s+(.*)$", instruction)
        if call:
            operand = call[1].split("##", 1)[0].strip()
            target = re.fullmatch(r"0x([0-9a-fA-F]+)", operand)
            symbolic = operand in mangled_addresses
            if target or symbolic:
                addr = int(target[1], 16) if target else mangled_addresses[operand]
                direct.append({"site": hex(pc), "target": hex(addr), "symbols": address_names.get(addr, [])})
            else:
                indirect.append({"site": hex(pc), "operand": operand})
        if "##" in instruction:
            comment = instruction.split("##", 1)[1].strip()
            literals.append({"site": hex(pc), "reference": comment})
    return direct, indirect, literals


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--app", type=Path, required=True, help="expanded VirtualDJ.app")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--package", type=Path, help="optional source expanded package directory for provenance")
    args = p.parse_args()
    binary = args.app / "Contents/MacOS/VirtualDJ"
    if not binary.is_file():
        p.error(f"missing binary: {binary}")
    args.output.mkdir(parents=True, exist_ok=True)
    old_manifest = args.output / "manifest.json"
    previous_files = ({row["file"] for row in json.loads(old_manifest.read_text())["symbols"].values()}
                      if old_manifest.exists() else set())
    starts = function_starts(binary)
    pretty, address_names = symbols(binary)
    mangled_addresses = {mangled: address for address, names in address_names.items() for mangled in names}
    address_names = {a: sorted(set(v)) for a, v in address_names.items()}
    targets = dict(TARGETS)
    for name in sorted(pretty):
        if name.startswith(STREE_PREFIX):
            targets.setdefault(name, name)
    manifest = {
        "source": {"app": str(args.app), "binary": str(binary), "architecture": "x86_64",
                   "sha256": sha256(binary), "captured": datetime.date.today().isoformat(),
                   "evidence_tier": "Tier-2 binary structure; no runtime behavior claim"},
        "bounds": {"method": "LC_FUNCTION_STARTS exact starts; next start is end_exclusive", "count": len(starts)},
        "symbols": {}, "unresolved": {"requested": [], "indirect_call_sites": []},
        "scope": "Selected parser/editor symbols and their bounded bodies; transitive coverage is not exhaustive.",
        "call_graph_boundary": "Direct calls are captured only from selected bounded bodies. Indirect calls and direct targets outside this selection are listed as unresolved coverage edges; no exhaustive transitive graph is claimed.",
    }
    info = args.app / "Contents/Info.plist"
    if info.is_file():
        plist = plistlib.loads(info.read_bytes())
        manifest["source"]["bundle_version"] = plist.get("CFBundleVersion")
        manifest["source"]["bundle_short_version"] = plist.get("CFBundleShortVersionString")
    if args.package:
        manifest["source"]["package"] = str(args.package)
        if args.package.is_file():
            manifest["source"]["package_sha256"] = sha256(args.package)
    for label, wanted in targets.items():
        # Reconstruct the mangled name from nm's address map; demangled names can have overloads.
        pretty_matches = [(pretty_name, addr) for pretty_name, addr in pretty.items()
                          if pretty_name == wanted or pretty_name.startswith(wanted + "(")]
        if len(pretty_matches) > 1:
            raise ValueError(f"ambiguous overload for {label}: specify one exact demangled signature")
        candidates = [(n, a, pretty_name) for pretty_name, a in pretty_matches
                      for n in address_names.get(a, [])]
        if not candidates:
            manifest["unresolved"]["requested"].append({"name": label, "reason": "named symbol unavailable"})
            continue
        mangled, start, actual_name = candidates[0]
        index = bisect.bisect_left(starts, start)
        if index == len(starts) or starts[index] != start:
            manifest["unresolved"]["requested"].append({"name": label, "reason": "symbol not in LC_FUNCTION_STARTS"})
            continue
        end = starts[index + 1] if index + 1 < len(starts) else None
        if end is None:
            manifest["unresolved"]["requested"].append({"name": label, "reason": "no next function start"})
            continue
        body = bounded_disassembly(binary, mangled, start, end)
        filename = f"{len(manifest['symbols']):02d}-{re.sub(r'[^A-Za-z0-9]+', '-', label).strip('-')}.asm"
        (args.output / filename).write_text(body)
        direct, indirect, literals = sites(body, address_names, mangled_addresses)
        manifest["symbols"][label] = {"demangled": actual_name, "mangled": mangled, "start": hex(start),
                                       "end_exclusive": hex(end), "file": filename,
                                       "asm_sha256": sha256(args.output / filename),
                                       "direct_calls": direct, "indirect_calls": indirect,
                                       "literal_references": literals}
        manifest["unresolved"]["indirect_call_sites"].extend(
            [{"function": label, **entry} for entry in indirect])
    selected_addresses = {int(v["start"], 16) for v in manifest["symbols"].values()}
    expanded = {}
    for function in manifest["symbols"].values():
        for call in function["direct_calls"]:
            address = int(call["target"], 16)
            if address not in selected_addresses:
                expanded.setdefault((address, tuple(call["symbols"])), []).append(function["demangled"])
    manifest["coverage"] = {"direct_unexpanded_targets": [
        {"target": hex(address), "symbols": list(names), "callers": sorted(callers)}
        for (address, names), callers in sorted(expanded.items())],
        "selected_symbol_count": len(manifest["symbols"]),
    }
    known_masks = {0x100002600, 0xF400024300002401, 0x20100000001}
    mask_refs = []
    for label, function in manifest["symbols"].items():
        body = (args.output / function["file"]).read_text()
        for line in body.splitlines():
            m = ADDR_RE.match(line)
            imm = re.search(r"##\s+imm\s*=\s*0x([0-9a-fA-F]+)", line)
            if m and imm and int(imm[1], 16) in known_masks:
                value = int(imm[1], 16)
                mask_refs.append({"function": label, "instruction": hex(int(m[1], 16)),
                                  "value": hex(value), "set_bit_positions": [i for i in range(value.bit_length()) if value & (1 << i)],
                                  "evidence": "bounded disassembly immediate; structural bitset only"})
    manifest["derived_immediates"] = mask_refs
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    current_files = {row["file"] for row in manifest["symbols"].values()}
    for name in previous_files - current_files:
        # Remove only bodies owned by the prior manifest, never arbitrary evidence files.
        if Path(name).name == name:
            (args.output / name).unlink(missing_ok=True)
    print(f"captured {len(manifest['symbols'])} selected symbol bodies to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
