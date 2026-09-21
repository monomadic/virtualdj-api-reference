#!/usr/bin/env python3
"""Recover direct literal-comparison sites in the current is_using consumer.

Strict local instruction patterns only; not a transitive keyword-completeness claim.
"""
import argparse,hashlib,json
from pathlib import Path
from types import SimpleNamespace
from extract_verb_table import BINARY,sections,slice_offset,build_identity
from extract_action_contracts import rtti_graph
from extract_skin_classes import function_starts


def extract():
    from capstone import Cs,CS_ARCH_ARM64,CS_MODE_ARM
    raw=Path(BINARY).read_bytes();base=slice_offset(raw);secs=sections(raw,base)
    text=next(s for s in secs if s[1]=='__text');strings=next(s for s in secs if s[1]=='__cstring')
    starts=function_starts(SimpleNamespace(data=raw,base=base));ends=dict(zip(starts,starts[1:]))
    graph=rtti_graph(raw,prefixes=('ACTION_is_using',))['ACTION_is_using'];fn=graph['slots'][3]
    decoder=Cs(CS_ARCH_ARM64,CS_MODE_ARM)
    def body(a):
        off=base+text[4]+a-text[2];return raw[off:off+ends[a]-a]
    def decode(a):
        code=body(a);ops=list(decoder.disasm(code,a))
        if sum(i.size for i in ops)!=len(code):raise ValueError('incomplete routine decode')
        return ops
    def string(a):
        if not strings[2]<=a<strings[2]+strings[3]:return None
        off=base+strings[4]+a-strings[2];end=raw.find(b'\0',off,off+80)
        return raw[off:end].decode('ascii') if end>=off else None
    instructions=decode(fn);sites=[];helpers={}
    # Require contiguous ADRP x1 / ADD x1 / MOV x0 / BL. No guessed dataflow.
    for a,b,c,d in zip(instructions,instructions[1:],instructions[2:],instructions[3:]):
        if not(a.mnemonic=='adrp' and a.op_str.startswith('x1, #') and b.mnemonic=='add' and b.op_str.startswith('x1, x1, #') and c.mnemonic=='mov' and c.op_str.startswith('x0, x') and d.mnemonic=='bl'):continue
        address=int(a.op_str.split('#')[1],0)+int(b.op_str.split('#')[1],0);literal=string(address)
        target=int(d.op_str.removeprefix('#'),0)
        if literal is None or target not in ends:continue
        ops=decode(target)
        # The observed comparison family checks txt tag, exact length, then calls
        # a shared comparison routine. Keep that routine's identity unresolved.
        pattern=[(i.mnemonic,i.op_str) for i in ops]
        if not(pattern[:3]==[('ldr','w9, [x0]'),('sub','w9, w9, #0x747, lsl #12'),('cmp','w9, #0x874')]):continue
        lengths=[int(i.op_str.split('#')[1],0) for i in ops if i.mnemonic=='mov' and i.op_str.startswith('w2, #')]
        if lengths!=[len(literal)]:raise ValueError('comparison length disagrees with literal')
        sites.append({'literal':literal,'literal_address':hex(address),'callsite':hex(d.address),'helper':hex(target),'argument_register':c.op_str.split(', ')[1]})
        helpers[hex(target)]={'end':hex(ends[target]),'sha256':hashlib.sha256(body(target)).hexdigest(),'instructions':[{'address':hex(i.address),'mnemonic':i.mnemonic,'operands':i.op_str} for i in ops]}
    return {'source':{**build_identity(BINARY),'binary_sha256':hashlib.sha256(raw).hexdigest()},'evidence_tier':2,'class':'ACTION_is_using','vtable':hex(graph['vtable']),'consumer':{'start':hex(fn),'end':hex(ends[fn]),'sha256':hashlib.sha256(body(fn)).hexdigest(),'parameter_setup':[{'address':hex(i.address),'mnemonic':i.mnemonic,'operands':i.op_str} for i in instructions[:32]]},'sites':sites,'helpers':helpers,'literals':sorted({s['literal'] for s in sites}),'limitations':['Direct contiguous literal-setup patterns only. No absence or global completeness claim.','Register identity is local code provenance, not by itself an argument-position proof.','Keywords and modifiers require separate runtime discrimination; static comparisons do not establish behaviour.']}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);p.add_argument('--check',type=Path);args=p.parse_args();result=extract()
    if args.check:
        previous=json.loads(args.check.read_text()); previous['source']['extracted']=result['source']['extracted']
        if previous!=result:raise ValueError('consumer extraction drift')
    if args.output:
        with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result['sites'],indent=2))
