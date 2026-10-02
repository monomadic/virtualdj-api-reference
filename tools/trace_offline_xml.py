#!/usr/bin/env python3
"""Trace fixed XML cases in our own sandboxed host; not a live-app debugger."""
import argparse
import datetime
import json
from pathlib import Path
import subprocess
import offline_parser as base
from offline_xml import CASES, verify_preparation

TRACE_NAMES = ['mismatched_end','factory_unknown','factory_button','factory_panel','factory_text',
               'factory_button_geometry','factory_button_bad_geometry','factory_button_unknown_fields',
               'factory_button_action','factory_button_duplicate_width','factory_button_case']

def run(work, output, module=None):
    if output.exists(): raise ValueError('capture already exists')
    prep=verify_preparation(work)
    module=module or base.ROOT/'tools/offline_xml_trace.py'
    commands='\n'.join(['settings set target.disable-aslr false',
        'settings set target.env-vars HOME='+str(work)+' TMPDIR='+str(work),
        'command script import '+str(module),'xml-setup','run','process status','quit',''])
    script=work/'trace.lldb';script.write_text(commands)
    result=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),preparation=prep,
                trace_source_sha256=base.digest(module.read_bytes()),driver_source_sha256=base.digest(Path(__file__).read_bytes()),
                commands=commands,scope='Offline native breakpoint trace, selected function entries and returns; not instruction coverage or rendering.',
                runs=[],suite_finished=False)
    for name in TRACE_NAMES:
        index=next(i for i,c in enumerate(CASES) if c[0]==name)
        args=['xcrun','lldb','--batch','-s',str(script),'--',str(work/'bin/host'),str(work/'libvdj-parser.dylib'),str(index),str(work/'sandbox.sb')]
        row=dict(name=name,xml=CASES[index][1],argv=args,cwd=str(work))
        try:
            p=subprocess.run(args,cwd=work,capture_output=True,text=True,timeout=75)
            row.update(returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
            row['trace']=[json.loads(line[len('XMLTRACE '):]) for line in p.stdout.splitlines() if line.startswith('XMLTRACE ')]
            row['host_events']=[json.loads(line) for line in p.stdout.splitlines() if line.startswith('{"event":')]
            row['completed']=p.returncode==0 and row['host_events'][-1:]==[{'event':'complete'}] and bool(row['trace'])
            row['read_errors']=[e for e in row['trace'] if 'read_error' in e]
            row['completed'] &= not row['read_errors']
        except subprocess.TimeoutExpired as e:
            row.update(timeout=True,completed=False,stdout=(e.stdout or b'').decode(errors='replace'),stderr=(e.stderr or b'').decode(errors='replace'))
        result['runs'].append(row);output.write_text(json.dumps(result,indent=2)+'\n')
        print(name+': '+('completed' if row['completed'] else 'incomplete'),flush=True)
    result['suite_finished']=True;output.write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.work,a.output)
