#!/usr/bin/env python3
"""Journal the HTTP legs; clicks and screenshots are performed through cua_repl.

begin -> load -> arm left/right -> CUA clicks -> read; repeat after reload;
restore always restores the original skin and every probe variable, then verifies.
No uncertain write is retried. The append-only journal records intent first.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import plistlib
import time
import urllib.parse
import urllib.request
from generate import HERE, NAME, files

JOURNAL = HERE / 'run-9644.jsonl'
STATE = Path('/tmp/vdj-schema-condition-state.json')
VARIABLES = [f'$schema_condition_{n}' for n in range(1, 10)]


def log(row):
    with JOURNAL.open('a') as f:
        f.write(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),**row})+'\n');f.flush();os.fsync(f.fileno())


def request(script, kind='query'):
    if kind=='execute':log({'intent':script})
    with urllib.request.urlopen('http://localhost/'+kind+'?'+urllib.parse.urlencode({'script':script}),timeout=20) as r:
        result=r.read().decode().strip()
    log({kind:script,'result':result})
    if result.startswith('error:'):raise ValueError(result)
    return result


def q(s):return request(s)
def ex(s):return request(s,'execute')
def values():return {name:q("get_var '"+name+"'") for name in VARIABLES}
def context():return {f'deck {n} {what}':q(f'deck {n} {what}') for n in range(1,5) for what in ('loaded','play')}


def wait_skin(expected):
    # Loading is asynchronous. Poll readback only; never replay a write.
    for _ in range(20):
        got=q('load_skin')
        if got==expected:return got
        time.sleep(0.25)
    raise ValueError('skin readback mismatch: '+got)


def main():
    global JOURNAL, STATE
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('step',choices=['begin','load','arm','read','restore']);p.add_argument('--side',choices=['left','right']);p.add_argument('--round',type=int)
    p.add_argument('--journal',type=Path,default=JOURNAL);p.add_argument('--state',type=Path,default=STATE);a=p.parse_args()
    JOURNAL,STATE=a.journal,a.state
    if a.step=='begin':
        if JOURNAL.exists() or STATE.exists():raise ValueError('run already exists')
        data={'build':plistlib.loads(Path('/Applications/VirtualDJ.app/Contents/Info.plist').read_bytes())['CFBundleVersion'],
              'fixture_hashes':{k:hashlib.sha256(v).hexdigest() for k,v in files().items()},'context_before':context(),
              'skin_before':q('load_skin'),'variables_before':values()}
        if data['build']!='18.0.9644':raise ValueError('fixture is anchored to build 9644')
        for value in data['variables_before'].values():
            if value:float(value) # Validate restoration before any mutation.
        if any(v not in ('0','off','no','false') for v in data['context_before'].values()):raise ValueError('requires empty stopped decks')
        if q('on') not in ('1','on','yes','true') or q('off') not in ('0','off','no','false'):raise ValueError('condition calibration failed')
        if not data['skin_before'] or "'" in data['skin_before']:raise ValueError('skin cannot be safely quoted')
        STATE.write_text(json.dumps(data,indent=2));log({'begin':data})
    else:
        data=json.loads(STATE.read_text())
        if a.step=='load':
            ex("load_skin '"+NAME+"/:skin'")
            got=wait_skin(NAME+'/:skin')
            log({'loaded_round':a.round,'skin':got})
        elif a.step=='arm':
            if not a.side or not a.round:raise ValueError('side and round required')
            if q('load_skin')!=NAME+'/:skin':raise ValueError('fixture not loaded')
            for name in VARIABLES:ex("set '"+name+"' 0")
            if any(v!='0' for v in values().values()):raise ValueError('reset failed')
            data['pending']={'round':a.round,'side':a.side};STATE.write_text(json.dumps(data,indent=2));log({'armed':data['pending']})
        elif a.step=='read':
            if 'pending' not in data:raise ValueError('not armed')
            log({'observation':{**data.pop('pending'),'values':values(),'click_channel':'cua_repl; coordinates recorded in README'}})
            STATE.write_text(json.dumps(data,indent=2))
        else:
            ex("load_skin '"+data['skin_before']+"'")
            wait_skin(data['skin_before'])
            for name,value in data['variables_before'].items():
                value = value or '0'  # Previously unset probe names are reset, not deleted.
                float(value) # numeric restoration only
                ex("set '"+name+"' "+value)
            restored={'skin':q('load_skin'),'variables':values(),'context':context()}
            expected={name:value or '0' for name,value in data['variables_before'].items()}
            ok=restored['skin']==data['skin_before'] and restored['variables']==expected and restored['context']==data['context_before']
            log({'restoration':restored,'verified':ok,
                 'exact_variable_restoration':restored['variables']==data['variables_before'],
                 'note':'Previously unset probe variables are left at zero; no deletion API is established.'})
            if not ok:raise ValueError('restoration mismatch')
    print(json.dumps({'step':a.step,'ok':True}))


if __name__=='__main__':main()
