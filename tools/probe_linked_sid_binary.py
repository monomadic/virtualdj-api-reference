#!/usr/bin/env python3
"""Execute recovered ARM64 reduction/hash instructions in Unicorn, not VirtualDJ.

Synthetic inputs only. This is a Tier-2 reproduction of the historical binary,
not a live integration test. The libc/string calls are narrowly hooked; the
reducer, Unicode lookup and FNV loop execute the original machine instructions.
Requires unicorn. Use --app with the SHA-guarded unstripped 18.0.9246 bundle.
"""
import argparse
import hashlib
import json
from pathlib import Path

from extract_verb_table import slice_offset, sections
from extract_linked_sid import EXPECTED_SHA
from linked_sid import calculate, reduce_field, load_evidence

CASES = [
    ('Example Artist', 'Example Track', 'Club Mix'),
    ('Example Artist', 'Example Track', 'Dub Mix'),
    ('A1 & B2', 'Tune 123 (Live)', 'Club Mix'),
    ('A[guest]', 'Tune/other', 'Dub'),
    ('Straße', 'Été Ελληνικά Русский עברית', ''),
    ('A', '中文 ไทย', ''),
    ('A', 'Cafe\u0301 😀', ''),
    ('www.example', 'WWW.example', ''),
    ('A', 'Tune', 'promo.com Mix'),
    ('A', 'Tune', 'promo.COM Mix'),
    ('AB', 'C', ''), ('A', 'BC', ''),
]


def probe(app):
    from unicorn import Uc, UC_ARCH_ARM64, UC_MODE_ARM, UC_HOOK_CODE
    from unicorn.arm64_const import (UC_ARM64_REG_X0, UC_ARM64_REG_X1,
        UC_ARM64_REG_X2, UC_ARM64_REG_X9, UC_ARM64_REG_X19, UC_ARM64_REG_W8,
        UC_ARM64_REG_SP, UC_ARM64_REG_LR, UC_ARM64_REG_PC)
    data = (app / 'Contents/MacOS/VirtualDJ').read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA:
        raise ValueError('Unexpected binary hash')
    base = slice_offset(data)
    secs = sections(data, base)
    evidence = load_evidence()
    u = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
    mapped = set()
    def map_range(start, length):
        for page in range(start & ~4095, (start + length + 4095) & ~4095, 4096):
            if page not in mapped:
                u.mem_map(page, 4096)
                mapped.add(page)
    def copy(va, length):
        sec = next(s for s in secs if s[2] <= va and va+length <= s[2]+s[3])
        offset = base + sec[4] + va-sec[2]
        map_range(va, length)
        u.mem_write(va, data[offset:offset+length])
    for start, length in [(0x1005c14b4, 0x184), (0x1000f9754, 0xa4),
                          (0x1005c1808, 0x38), (0x104084965, 5),
                          (0x1044b5998, 6), (0x104080e79, 3),
                          (0x1044a5078, 0x1e3)]:
        copy(start, length)
    stubs = {0x103adf4e8: 'strncmp', 0x103adf470: 'strchr',
             0x103adde2c: 'push', 0x103adddb4: 'append'}
    for addr in stubs:
        map_range(addr, 4)
    stack, text, halt = 0x200000000, 0x210000000, 0x220000000
    map_range(stack, 0x10000)
    map_range(text, 0x10000)
    map_range(halt, 4096)
    result = bytearray()
    def cstr(ptr):
        out = bytearray()
        while True:
            byte = u.mem_read(ptr+len(out), 1)[0]
            if not byte:
                return bytes(out)
            out.append(byte)
    def hook(uc, address, size, _):
        kind = stubs.get(address)
        if kind is None:
            return
        x0, x1, x2 = (uc.reg_read(r) for r in (UC_ARM64_REG_X0, UC_ARM64_REG_X1, UC_ARM64_REG_X2))
        if kind == 'push':
            result.append(x1 & 255)
        elif kind == 'append':
            result.extend(uc.mem_read(x1, x2))
        elif kind == 'strncmp':
            a, b = cstr(x0)[:x2], cstr(x1)[:x2]
            uc.reg_write(UC_ARM64_REG_X0, 0 if a == b else 1)
        else:
            pos = cstr(x0).find(bytes([x1 & 255]))
            uc.reg_write(UC_ARM64_REG_X0, 0 if pos < 0 else x0+pos)
        uc.reg_write(UC_ARM64_REG_PC, uc.reg_read(UC_ARM64_REG_LR))
    u.hook_add(UC_HOOK_CODE, hook)
    def native_reduce(value):
        result.clear()
        u.mem_write(text, value.encode()+b'\0')
        u.reg_write(UC_ARM64_REG_X0, text+0x8000)  # abstract output string
        u.reg_write(UC_ARM64_REG_X1, text)
        u.reg_write(UC_ARM64_REG_SP, stack+0xf000)
        u.reg_write(UC_ARM64_REG_LR, halt)
        u.emu_start(0x1005c14b4, halt, count=100000)
        if u.reg_read(UC_ARM64_REG_PC) != halt:
            raise ValueError('Reducer did not return')
        return bytes(result)
    cases = []
    for artist, title, remix in CASES:
        fields = [native_reduce(s) for s in (artist, title, remix)]
        assert fields == [reduce_field(s, evidence) for s in (artist, title, remix)]
        # Remix inclusion is from getSID's separately captured find() branches.
        excluded = any(s in remix for s in evidence['algorithm']['remix_excluded_if_contains'])
        reduced = fields[0] + fields[1] + (b'' if excluded else fields[2])
        u.mem_write(text, reduced+b'\0')
        u.reg_write(UC_ARM64_REG_X9, text)
        u.reg_write(UC_ARM64_REG_W8, 0)
        u.emu_start(0x1005c1808, 0x1005c1840, count=100000)
        assert u.reg_read(UC_ARM64_REG_PC) == 0x1005c1840
        actual = u.reg_read(UC_ARM64_REG_X19)
        expected = calculate(artist, title, remix, evidence)
        assert actual == expected['sid_unsigned']
        cases.append({'artist': artist, 'title': title, 'remix': remix,
                      'reduced_utf8_hex': reduced.hex(), 'sid_hex': f'{actual:016x}',
                      'sid_signed': expected['sid_signed']})
    return {'evidence_tier': 2, 'source': evidence['source'],
            'method': 'Unicorn executes original reducer, utfcanonical and FNV-loop instructions; hooked libc/std::string calls.',
            'limitations': 'Not the running application. Cleanup, remix inclusion branches, sentinel rejection, and SQLite writes are not emulated.',
            'cases': cases}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--app', required=True, type=Path)
    print(json.dumps(probe(p.parse_args().app), indent=2, ensure_ascii=False))
