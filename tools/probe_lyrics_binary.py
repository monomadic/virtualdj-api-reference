#!/usr/bin/env python3
"""Tier-2 synthetic execution of original lyric hash and payload-parser code.

Requires Unicorn and the SHA-guarded unstripped build. Standard string/vector
operations are hooked. This never launches VirtualDJ or accesses private media.
"""
import argparse
import hashlib
import json
import random
import struct
from pathlib import Path
from extract_verb_table import slice_offset, sections
from extract_linked_sid import EXPECTED_SHA
from lyrics_cache import lid_from_words, describe_lid

PAYLOADS = [
    '#LANG=eng\n[0.10-0.30] alpha\n[0.40-0.80] beta\\n\n',
    '#CUSTOM\n[2.00-3.00] alpha\n[1.00-1.50] beta\n',
    '[1.00-1.00] zero\n[2.00-1.00] reverse\n',
    '[0.10-0.50] <marker>\n[0.20-0.40] word\n',
    '#NOLYRICS', '#LANG=eng',
    '[-1.00--1.00] pending\n',
    '[0.00-1.00] \n[0.20-0.30] word\n',
]


def probe(app):
    from unicorn import Uc, UC_ARCH_ARM64, UC_MODE_ARM, UC_HOOK_CODE
    from unicorn.arm64_const import (UC_ARM64_REG_X0, UC_ARM64_REG_X1,
        UC_ARM64_REG_X2, UC_ARM64_REG_X3, UC_ARM64_REG_X8,
        UC_ARM64_REG_SP, UC_ARM64_REG_LR, UC_ARM64_REG_PC)
    data = (app / 'Contents/MacOS/VirtualDJ').read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA:
        raise ValueError('Unexpected binary hash')
    base = slice_offset(data)
    secs = sections(data, base)
    u = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
    mapped = set()
    def mapping(start, length):
        for page in range(start & ~4095, (start+length+4095) & ~4095, 4096):
            if page not in mapped:
                u.mem_map(page, 4096)
                mapped.add(page)
    def copy(start, length):
        sec = next(s for s in secs if s[2] <= start and start+length <= s[2]+s[3])
        offset = base+sec[4]+start-sec[2]
        mapping(start, length)
        u.mem_write(start, data[offset:offset+length])
    for address, length in [(0x100596700,0xfc),(0x103cb3240,16),
                            (0x100570430,0x450),(0x100588e70,0x274),
                            (0x10408c0c4,3),(0x103c81ca4,4),
                            (0x104075d67,3),(0x1040b0af0,7),(0x104075609,2)]:
        copy(address,length)
    stack, input_address, output, halt = 0x200000000,0x210000000,0x220000000,0x230000000
    for address in (stack,input_address,output,halt):
        mapping(address,0x20000)
    mapping(0x10429c460,8)
    u.mem_write(0x10429c460,struct.pack('<Q',output+0x1000))
    def run(start, stop):
        u.reg_write(UC_ARM64_REG_SP,stack+0x1f000)
        u.reg_write(UC_ARM64_REG_LR,halt)
        try:
            u.emu_start(start,stop,count=2000000)
        except Exception as exc:
            raise RuntimeError(f'Emulation failed at {u.reg_read(UC_ARM64_REG_PC):#x}') from exc
        if u.reg_read(UC_ARM64_REG_PC) != stop:
            raise ValueError('Instruction budget exhausted')
    hash_vectors=[]
    rng=random.Random(9246)
    word_cases=[[0,0],[0xffffffff]*3,[1,2,4,8,0x80000000],
                [rng.getrandbits(32) for _ in range(257)]]
    for words in word_cases:
        u.mem_write(input_address,struct.pack('<'+'I'*len(words),*words))
        u.reg_write(UC_ARM64_REG_X0,input_address)
        u.reg_write(UC_ARM64_REG_X1,len(words))
        u.reg_write(UC_ARM64_REG_X8,output)
        run(0x100596700,halt)
        raw=bytes(u.mem_read(output,18))
        assert raw==lid_from_words(words)
        hash_vectors.append({'words':words,**describe_lid(raw)})
    # Execute setLyrics up to the point it installs parsed data into CSong.
    # Hook storage primitives, leaving timestamp parsing/repair in native code.
    callbacks={0x10006160c:'get_song',0x103aded38:'memchr',0x1000755f8:'find',
               0x100587ef0:'left_ci',0x100588270:'right_ci',0x10001b054:'assign',
               0x103aded5c:'memcpy',0x103adddb4:'append',0x100573a38:'segment_view',0x100573770:'segment_string'}
    for address in callbacks:
        mapping(address,4)
    segments=[]
    language=[]
    def cstr(address):
        value=bytearray()
        while True:
            ch=u.mem_read(address+len(value),1)[0]
            if not ch:return bytes(value)
            value.append(ch)
    def smallstring(address):
        raw=bytes(u.mem_read(address,24))
        if raw[23]&128:
            ptr,n=struct.unpack('<QQ',raw[:16]);return bytes(u.mem_read(ptr,n))
        return raw[:raw[23]]
    def hook(uc,address,size,_):
        kind=callbacks.get(address)
        if not kind:return
        x0,x1,x2,x3=(uc.reg_read(r) for r in (UC_ARM64_REG_X0,UC_ARM64_REG_X1,UC_ARM64_REG_X2,UC_ARM64_REG_X3))
        answer=0
        if kind=='get_song':answer=output+0x10000
        elif kind=='memcpy':
            uc.mem_write(x0,bytes(uc.mem_read(x1,x2)));answer=x0
        elif kind=='memchr':
            pos=bytes(uc.mem_read(x0,x2)).find(bytes([x1&255]));answer=0 if pos<0 else x0+pos
        elif kind=='find':
            ptr,n=struct.unpack('<QQ',uc.mem_read(x0,16));pos=bytes(uc.mem_read(ptr,n)).find(cstr(x1),x2)
            answer=pos if pos>=0 else (1<<64)-1
        elif kind in ('left_ci','right_ci'):
            value=bytes(uc.mem_read(x0,x1)).lower();term=cstr(x2).lower()
            answer=int(value.startswith(term) if kind=='left_ci' else value.endswith(term))
        elif kind in ('assign','append'):
            value=(b'' if kind=='assign' else smallstring(x0))+bytes(uc.mem_read(x1,x2))
            if len(value)>=23:raise ValueError('Synthetic hook supports short strings only')
            uc.mem_write(x0,value+b'\0'*(23-len(value))+bytes([len(value)]));answer=x0
            if kind=='assign':language.append(value.decode())
        else:
            start=struct.unpack('<f',uc.mem_read(x1,4))[0];end=struct.unpack('<f',uc.mem_read(x2,4))[0]
            if kind=='segment_view':
                ptr,n=struct.unpack('<QQ',uc.mem_read(x3,16));word=bytes(uc.mem_read(ptr,n))
            else:word=smallstring(x3)
            segments.append({'start':start,'end':end,'text':word.decode()})
            answer=output+0x2000+len(segments)*32
        uc.reg_write(UC_ARM64_REG_X0,answer)
        uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
    u.hook_add(UC_HOOK_CODE,hook)
    payload_vectors=[]
    for text in PAYLOADS:
        segments.clear();language.clear()
        u.mem_write(input_address,text.encode()+b'\0')
        u.reg_write(UC_ARM64_REG_X0,output+0x8000)
        u.reg_write(UC_ARM64_REG_X1,input_address)
        u.reg_write(UC_ARM64_REG_X2,len(text.encode()))
        run(0x100570430,0x1005707a8)
        payload_vectors.append({'payload':text,'language':language[-1] if language else '',
                                'native_segments':list(segments)})
    return {'evidence_tier':2,'binary_sha256':EXPECTED_SHA,'build':'18.0.9246','arch':'arm64',
            'method':'Original ARM64 hash128 and setLyrics/strToDbl instructions in Unicorn; string/vector storage primitives hooked.',
            'limitations':'Synthetic short strings; no live app, audio decoding, Chromaprint execution, database write, or server request.',
            'hash_vectors':hash_vectors,'payload_vectors':payload_vectors}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--app',type=Path,required=True)
    print(json.dumps(probe(p.parse_args().app),indent=2))
