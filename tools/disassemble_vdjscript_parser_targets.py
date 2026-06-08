#!/usr/bin/env python3
"""Summarize targeted VDJScript parser/editor disassembly.

This is a read-only helper. It uses otool's Mach-O routine disassembly mode
for known parser/editor symbols, then extracts a compact call/literal/immediate
summary so the reference docs do not need to quote long instruction listings.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


DEFAULT_APP = Path("/Applications/VirtualDJ.app")
TARGETS = {
    "getCurrentWord": "__ZN15DLGActionWizard14getCurrentWordERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEmRmS9_",
    "onChanged": "__ZN15DLGActionWizard9onChangedEv",
    "updateList": "__ZN15DLGActionWizard10updateListEv",
    "updateHint": "__ZN15DLGActionWizard10updateHintEv",
    "setColor": "__ZN15DLGActionWizard5STree8setColorEj",
    "toString": "__ZN15DLGActionWizard5STree8toStringEv",
    "xyToPos": "__ZN15DLGActionWizard7xyToPosEii",
    "customDraw": "__ZN15DLGActionWizard10customDrawEiiiiii",
}

INSTRUCTION_RE = re.compile(r"^\s*(?P<address>[0-9a-f]{16})\s+(?P<instruction>.+)$")
LABEL_RE = re.compile(r"^__[A-Za-z0-9_]+:")
CALL_RE = re.compile(r"\bbl\t(?P<target>.+)$")
LITERAL_RE = re.compile(r"literal pool(?: symbol address)?(?: for)?: (?P<literal>.+)$")
IMM_RE = re.compile(r"#0x(?P<value>[0-9a-fA-F]+)")
MOV_RE = re.compile(r"\bmov\s+(?P<reg>x\d+), #0x(?P<value>[0-9a-fA-F]+)")
MOVK_RE = re.compile(r"\bmovk\s+(?P<reg>x\d+), #0x(?P<value>[0-9a-fA-F]+), lsl #(?P<shift>32|48)")
SUB_IMM_RE = re.compile(r"\bsub\s+w\d+, w\d+, #0x(?P<value>[0-9a-fA-F]+)")


@dataclass(frozen=True)
class CallSite:
    address: str
    target: str


@dataclass(frozen=True)
class CharImmediate:
    value: str
    char: str
    count: int


@dataclass(frozen=True)
class BitmaskLiteral:
    value: str
    offset: str
    chars: str


@dataclass(frozen=True)
class TargetSummary:
    target: str
    symbol: str
    instruction_count: int
    calls: list[CallSite]
    literals: list[str]
    char_immediates: list[CharImmediate]
    bitmasks: list[BitmaskLiteral]


def disassembly_lines(app: Path, arch: str, symbol: str) -> list[str]:
    binary = app / "Contents/MacOS/VirtualDJ"
    return subprocess.check_output(
        ["otool", "-arch", arch, "-tV", "-p", symbol, str(binary)],
        text=True,
        errors="replace",
    ).splitlines()


def routine_instructions(lines: list[str], symbol: str) -> list[tuple[str, str]]:
    in_target = False
    instructions: list[tuple[str, str]] = []
    for line in lines:
        if line == f"{symbol}:":
            in_target = True
            continue
        if in_target and LABEL_RE.match(line):
            break
        if not in_target:
            continue
        match = INSTRUCTION_RE.match(line)
        if match:
            instructions.append((match.group("address"), match.group("instruction")))
    return instructions


def printable_char(value: int) -> str:
    if value == 0:
        return "\\0"
    if value == 10:
        return "\\n"
    if value == 9:
        return "\\t"
    if 32 <= value <= 126:
        return chr(value)
    return f"0x{value:x}"


def decode_bitmask(value: int, offset: int = 0) -> str:
    chars = [printable_char(bit + offset) for bit in range(128) if value & (1 << bit)]
    return " ".join(chars)


def code_span(text: str) -> str:
    longest_run = max((len(match.group(0)) for match in re.finditer(r"`+", text)), default=0)
    fence = "`" * (longest_run + 1)
    return f"{fence}{text}{fence}"


def summarize_target(app: Path, arch: str, target: str, symbol: str) -> TargetSummary:
    instructions = routine_instructions(disassembly_lines(app, arch, symbol), symbol)
    calls: list[CallSite] = []
    literals: list[str] = []
    char_counts: dict[int, int] = {}
    bitmasks: list[BitmaskLiteral] = []
    pending_mov: dict[str, tuple[int, int]] = {}
    recent_sub_offset = 0
    recent_sub_age = 999

    for address, instruction in instructions:
        recent_sub_age += 1
        if sub_match := SUB_IMM_RE.search(instruction):
            recent_sub_offset = int(sub_match.group("value"), 16)
            recent_sub_age = 0
        if call_match := CALL_RE.search(instruction):
            calls.append(CallSite(address, call_match.group("target")))
        if literal_match := LITERAL_RE.search(instruction):
            literal = literal_match.group("literal")
            if literal not in literals:
                literals.append(literal)
        for imm_match in IMM_RE.finditer(instruction):
            value = int(imm_match.group("value"), 16)
            if value <= 0x7f:
                char_counts[value] = char_counts.get(value, 0) + 1
        if mov_match := MOV_RE.search(instruction):
            offset = recent_sub_offset if recent_sub_age <= 8 else 0
            pending_mov[mov_match.group("reg")] = (int(mov_match.group("value"), 16), offset)
        if movk_match := MOVK_RE.search(instruction):
            reg = movk_match.group("reg")
            if reg in pending_mov:
                base_value, offset = pending_mov[reg]
                value = base_value | (int(movk_match.group("value"), 16) << int(movk_match.group("shift")))
                decoded = decode_bitmask(value, offset)
                if decoded:
                    bitmask = BitmaskLiteral(f"0x{value:x}", f"+0x{offset:x}" if offset else "", decoded)
                    if bitmask not in bitmasks:
                        bitmasks.append(bitmask)

    char_immediates = [
        CharImmediate(f"0x{value:x}", printable_char(value), count)
        for value, count in sorted(char_counts.items())
    ]
    return TargetSummary(
        target=target,
        symbol=symbol,
        instruction_count=len(instructions),
        calls=calls,
        literals=literals,
        char_immediates=char_immediates,
        bitmasks=bitmasks,
    )


def print_markdown(summaries: list[TargetSummary], max_calls: int) -> None:
    for summary in summaries:
        print(f"## {summary.target}")
        print()
        print(f"- symbol: {code_span(summary.symbol)}")
        print(f"- instructions: {summary.instruction_count}")
        print(f"- calls: {len(summary.calls)}")
        if summary.literals:
            print("- literals: " + ", ".join(code_span(literal) for literal in summary.literals))
        if summary.bitmasks:
            print("- decoded bitmasks:")
            for bitmask in summary.bitmasks:
                offset = f" offset {code_span(bitmask.offset)}" if bitmask.offset else ""
                print(f"  - {code_span(bitmask.value)}{offset} -> {code_span(bitmask.chars)}")
        if summary.char_immediates:
            chars = ", ".join(f"{code_span(item.value)} {code_span(item.char)} x{item.count}" for item in summary.char_immediates)
            print(f"- ASCII immediates: {chars}")
        if summary.calls:
            print("- call targets:")
            for call in summary.calls[:max_calls]:
                print(f"  - {code_span(call.address)} {call.target}")
            if len(summary.calls) > max_calls:
                print(f"  - ... {len(summary.calls) - max_calls} more")
        print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=Path, default=DEFAULT_APP)
    parser.add_argument("--arch", default="arm64")
    parser.add_argument(
        "--target",
        action="append",
        choices=sorted(TARGETS),
        help="Target to summarize; repeat for multiple targets. Defaults to all targets.",
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--max-calls", type=int, default=24)
    args = parser.parse_args()

    target_names = args.target if args.target else sorted(TARGETS)
    summaries = [summarize_target(args.app, args.arch, name, TARGETS[name]) for name in target_names]
    if args.format == "json":
        print(json.dumps([asdict(summary) for summary in summaries], indent=2, sort_keys=True))
    else:
        print_markdown(summaries, args.max_calls)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
