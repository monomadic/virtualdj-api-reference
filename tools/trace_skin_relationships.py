#!/usr/bin/env python3
"""Trace source-node paths through a sandboxed 9246 child-composition host."""
import argparse,datetime,json,subprocess
from pathlib import Path
import offline_parser as base
import offline_xml
from probe_skin_relationships import fixtures

NAMES=['panel_panel','button_button','button_text_repeat','button_text_states','slider_fader','stack_item','rack_unit_panel','split_left_content','group_visibility_button','group_button']

def run(work,output):
    if output.exists():raise ValueError('capture exists')
    prep=offline_xml.verify_preparation(work)
    if prep['composition_cases'] != [list(c) for c in fixtures()]:raise ValueError('fixture mismatch')
    for file,key in [('composition-layout.json','composition_layout_sha256'),('composition_guard.h','composition_guard_sha256')]:
        if base.digest((work/file).read_bytes())!=prep[key]:raise ValueError('prepared artifact changed')
    module=base.ROOT/'tools/offline_child_trace.py'
    commands='\n'.join(['settings set target.disable-aslr false','settings set target.env-vars HOME='+str(work)+' TMPDIR='+str(work),'command script import '+str(module),'run','process status','quit',''])
    script=work/'child-trace.lldb';script.write_text(commands)
    capture=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),preparation=prep,trace_source_sha256=base.digest(module.read_bytes()),commands=commands,runs=[],suite_finished=False)
    for name in NAMES:
        i=next(i for i,c in enumerate(fixtures()) if c[0]==name)
        args=['xcrun','lldb','--batch','-s',str(script),'--',str(work/'bin/host'),str(work/'libvdj-parser.dylib'),str(i),str(work/'sandbox.sb')]
        try:
            p=subprocess.run(args,cwd=work,capture_output=True,text=True,timeout=55)
            row=dict(name=name,xml=fixtures()[i][1],argv=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
        except subprocess.TimeoutExpired as e:
            row=dict(name=name,xml=fixtures()[i][1],argv=args,timeout=True,stdout=(e.stdout or b'').decode(errors='replace'),stderr=(e.stderr or b'').decode(errors='replace'))
        row['trace']=[json.loads(l[11:]) for l in row['stdout'].splitlines() if l.startswith('CHILDTRACE ')]
        row['events']=[json.loads(l) for l in row['stdout'].splitlines() if l.startswith('{"event":')]
        row['completed']=row.get('returncode')==0 and row['events'][-1:]==[{'event':'complete'}] and bool(row['trace']) and not any('read_error' in e for e in row['trace'])
        capture['runs'].append(row);output.write_text(json.dumps(capture,indent=2)+'\n');print(name,row['completed'],flush=True)
    capture['suite_finished']=True;output.write_text(json.dumps(capture,indent=2)+'\n')
    if not all(r['completed'] for r in capture['runs']):raise RuntimeError('trace failures recorded')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.work.resolve(),a.output.resolve())
