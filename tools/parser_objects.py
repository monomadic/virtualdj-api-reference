#!/usr/bin/env python3
"""Validate and summarize the bounded live parser experiment; never infer effect from parse success."""
import argparse
import json
import struct
from pathlib import Path

SCRIPTS=['is_using','is_using cue',"is_using 'cue'",'is_using zzunknowna','is_using zzunknownb',"is_using 'cue' 1000ms",'is_using cue 7','is_using cue 7.5','is_using cue 50%']
EXPECTED=[[], [('txt','cue')], [('txt','cue')], [('txt','zzunknowna')], [('txt','zzunknownb')], [('txt','cue'),('ms',1000.0)], [('txt','cue'),('int',7)], [('txt','cue'),('val',7.5)], [('txt','cue'),('%',0.5)]]


def decode(p):
    tag=p['tag'].to_bytes(4,'big').lstrip(b'\0').decode('ascii')
    if tag=='txt':value=p['text']
    elif tag=='int':value=struct.unpack('<i',struct.pack('<I',p['payload_u32']))[0]
    elif tag in ('val','ms','%'):value=struct.unpack('<f',struct.pack('<I',p['payload_u32']))[0]
    else:raise ValueError(f'unexpected tag {tag!r}')
    return tag,value


def check(path):
    rows=[json.loads(line) for line in path.read_text().splitlines()]
    if rows[0]['event']!='start' or rows[0]['build']!='18.0.9644' or rows[0]['arch']!='arm64':raise ValueError('wrong capture identity')
    if rows[0]['image_uuid']!='46743daaff0430269dab1cc69450155a':raise ValueError('wrong image UUID')
    if rows[1]!={'event':'guards_passed'} or rows[-1]!={'event':'complete'}:raise ValueError('incomplete or unguarded run')
    cases=rows[2:-1]
    if len(cases)!=2*len(SCRIPTS):raise ValueError('missing or extra cases')
    for i,row in enumerate(cases):
        case=i%len(SCRIPTS)
        if row['event']!='case' or row['round']!=i//len(SCRIPTS)+1 or row['script']!=SCRIPTS[case]:raise ValueError('wrong case order')
        if row['class']!='ACTION_is_using' or row['initial_refcount']!=1 or row['released'] is not True:raise ValueError('object ownership check failed')
        if [decode(p) for p in row['parameters']]!=EXPECTED[case]:raise ValueError('parameter representation changed')
        expected_hr=-2147024809 if case==0 else -2147467263 if case in (3,4) else 0
        if row['numeric_hresult']!=expected_hr:raise ValueError('keyword discrimination changed')
        if i>=len(SCRIPTS):
            earlier={k:v for k,v in cases[case].items() if k!='round'}
            if {k:v for k,v in row.items() if k!='round'}!=earlier:raise ValueError('rounds disagree')
    return [{'script':r['script'],'parameters':[decode(p) for p in r['parameters']],'numeric_hresult':r['numeric_hresult']} for r in cases[:len(SCRIPTS)]]


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('capture',nargs='?',type=Path,default=Path('tests/parser-objects-9644.jsonl'))
    args=p.parse_args()
    print(json.dumps({'build':'18.0.9644','two_rounds_match':True,'cases':check(args.capture)},indent=2))
