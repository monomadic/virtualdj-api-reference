#!/usr/bin/env python3
"""Build-pinned exploratory XML reader/factory experiment, one sandbox per input."""
import argparse
import datetime
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace
import offline_parser as base

ROOT = base.ROOT
CASES = [
    ('empty', ''), ('whitespace', ' \n '), ('minimal', '<skin/>'),
    ('nested', '<skin><button width="100"/></skin>'),
    ('unknown_element', '<skin><zzunknown/></skin>'),
    ('unknown_attribute', '<skin zzunknown="yes"/>'),
    ('mismatched_end', '<skin><button></skin>'), ('unclosed', '<skin><button>'),
    ('unquoted', '<skin width=100/>'), ('duplicate_attribute', '<skin width="1" width="2"/>'),
    ('case_mismatch', '<Skin></skin>'), ('bare_ampersand', '<skin text="a & b"/>'),
    ('entities', '<skin text="a &amp; b &lt; c &#65;"/>'),
    ('invalid_number', '<skin width="nonsense"/>'),
    ('trailing_junk', '<skin/>garbage'), ('second_root', '<skin/><button/>'),
    ('comment', '<!-- before --><skin/>'), ('bad_declaration', '<?xml broken><skin/>'),
    ('text', '<skin>hello</skin>'),
    ('factory_unknown', '<zzunknown/>'), ('factory_button', '<button/>'),
    ('factory_panel', '<panel/>'), ('factory_text', '<text/>'),
    ('factory_button_geometry', '<button><pos x="1" y="2"/><size width="10" height="20"/></button>'),
    ('factory_button_bad_geometry', '<button><pos x="bad" y="2"/><size width="nonsense" height="20"/></button>'),
    ('factory_button_unknown_fields', '<button zzunknown="yes"><zzchild/><pos x="1" y="2"/><size width="10" height="20"/></button>'),
    ('factory_button_action', '<button action="is_using cue"><pos x="1" y="2"/><size width="10" height="20"/></button>'),
    ('factory_button_duplicate_width', '<button><size width="10" width="99" height="20"/></button>'),
    ('factory_button_case', '<BUTTON><SIZE WIDTH="10" HEIGHT="20"/></BUTTON>'),
]

def prepare(app, work):
    info = base.plistlib.loads((app/'Contents/Info.plist').read_bytes())
    if info['CFBundleVersion'] != '18.0.9246':
        raise ValueError('XML spike is pinned to 9246')
    report = base.prepare(app, work)
    from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
    from extract_verb_table import sections, slice_offset
    from extract_skin_classes import function_starts
    from extract_action_vtables import demangled, symbol_maps
    p = work/'original.universal'; data=p.read_bytes(); offset=slice_offset(data)
    section=next(s for s in sections(data,offset) if s[1]=='__text')
    starts=function_starts(SimpleNamespace(data=data,base=offset)); ends=dict(zip(starts,starts[1:]))
    symbols,_=symbol_maps(demangled(p,'arm64')); md=Cs(CS_ARCH_ARM64,CS_MODE_LITTLE_ENDIAN)
    prefixes=('CXMLFile::loadFromBuffer(', 'CXMLFile::loadFromString(', 'CXMLFile::close(',
              'CXMLFile::setErrorMessage(', 'CXMLNode::load(', 'CXMLNode::~', 'CXMLNode::getParam(',
              'CXMLNode::getChild(', 'ISkinObject::createSkinObject(', 'CSkinButton::CSkinButton(')
    routines=[]
    for address,name in symbols.items():
        if not name.startswith(prefixes) or address not in ends: continue
        off=offset+section[4]+address-section[2]; body=data[off:off+ends[address]-address]
        routines.append(dict(address=address,size=len(body),symbol=name,sha256=base.digest(body),
                             instructions=[dict(pc=hex(i.address),instruction=i.mnemonic+' '+i.op_str) for i in md.disasm(body,address)]))
    layout=dict(build=report['build'],binary_sha256=report['source_sha256'],routines=routines,
                file_layout=dict(size=56,root=0,error=8,position=16,message=24,flags=48),
                node_layout=dict(size=96,name=0,attributes=24,children=48,text=72),
                provenance='Named arm64 routines and bounded disassembly; layout is a reviewed ABI hypothesis exercised by the capture.')
    (work/'xml-layout.json').write_text(json.dumps(layout,indent=2)+'\n')
    header='struct XMLGuard {uint64_t address; size_t size; const char* sha256;};\nconstexpr XMLGuard xmlGuards[]={\n'
    header+=''.join('{%s,%d,"%s"},\n'%(hex(r['address']),r['size'],r['sha256']) for r in routines)+'};\n'
    header+='struct XMLCase {const char* xml; bool factory;};\nconstexpr XMLCase xmlCases[]={\n'
    header+=''.join('{%s,%s},\n'%(json.dumps(xml),'true' if name.startswith('factory_') else 'false') for name,xml in CASES)+'};\n'
    (work/'offline_xml_guard.h').write_text(header)
    base.call(['clang++','-std=c++17','-arch','arm64','-I',work,ROOT/'tools/plugin/offline_xml_host.cpp','-o',work/'bin/host'])
    report.update(host_sha256=base.digest((work/'bin/host').read_bytes()),
                  xml_host_source_sha256=base.digest((ROOT/'tools/plugin/offline_xml_host.cpp').read_bytes()),
                  xml_guard_sha256=base.digest((work/'offline_xml_guard.h').read_bytes()),
                  xml_layout_sha256=base.digest((work/'xml-layout.json').read_bytes()),
                  experiment_source_sha256=base.digest(Path(__file__).read_bytes()))
    (work/'preparation.json').write_text(json.dumps(report,indent=2)+'\n')
    return {'prepared':str(work),'build':report['build']}

def verify_preparation(work):
    prep=json.loads((work/'preparation.json').read_text())
    expected=json.loads(base.manifest_for('18.0.9246').read_text())
    if prep['build']!='18.0.9246' or prep['source_sha256']!=expected['binary_sha256']:
        raise ValueError('unexpected source binary')
    for path,key in [('bin/host','host_sha256'),('libvdj-parser.dylib','converted_sha256'),('sandbox.sb','sandbox_sha256'),('xml-layout.json','xml_layout_sha256'),('offline_xml_guard.h','xml_guard_sha256')]:
        if base.digest((work/path).read_bytes()) != prep[key]: raise ValueError('changed '+path)
    for path,sha in prep['dependency_files'].items():
        if base.digest((work/path).read_bytes())!=sha:raise ValueError('changed dependency')
    for path,target in prep['dependency_symlinks'].items():
        if str((work/path).readlink())!=target:raise ValueError('changed dependency link')
    cases=''.join('{%s,%s},\n'%(json.dumps(xml),'true' if name.startswith('factory_') else 'false') for name,xml in CASES)+'};\n'
    if (work/'offline_xml_guard.h').read_text().split('constexpr XMLCase xmlCases[]={\n')[-1]!=cases:
        raise ValueError('prepared fixed inputs differ from current suite')
    return prep


def run(work, output):
    if output.exists(): raise ValueError('capture already exists')
    prep=verify_preparation(work)
    result=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),preparation=prep,
                scope='Offline native XML observations; no live renderer or schema conformance claim. Factory gets null image/window.',runs=[],suite_finished=False)
    env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(work),'TMPDIR':str(work)}
    for mode in ['--sandbox-check','--load-only']+[str(i) for i in range(len(CASES))]:
        args=['/usr/bin/sandbox-exec','-f',str(work/'sandbox.sb'),str(work/'bin/host'),str(work/'libvdj-parser.dylib'),mode]
        row=dict(mode=mode,argv=args,cwd=str(work),environment=env)
        if mode.isdigit():row.update(name=CASES[int(mode)][0],xml=CASES[int(mode)][1])
        try:
            p=subprocess.run(args,cwd=work,env=env,capture_output=True,text=True,timeout=20)
            row.update(returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
            row['events']=[json.loads(line) for line in p.stdout.splitlines()]
            row['completed']=p.returncode==0 and row['events'][-1:]==[{'event':'complete'}]
        except subprocess.TimeoutExpired as e:
            row.update(timeout=True,completed=False,stdout=(e.stdout or b'').decode(errors='replace'),stderr=(e.stderr or b'').decode(errors='replace'))
        result['runs'].append(row);output.write_text(json.dumps(result,indent=2)+'\n')
        if mode=='--sandbox-check':base.validate_run(row,[])
        if mode=='--load-only' and not row['completed']:raise ValueError('load control failed')
    result['suite_finished']=True;output.write_text(json.dumps(result,indent=2)+'\n')
    return [{'name':r.get('name',r['mode']),'completed':r['completed'],'result':next((e for e in r.get('events',[]) if e['event']=='xml_result'),None),'factory':next((e for e in r.get('events',[]) if e['event']=='factory_result'),None)} for r in result['runs']]

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['prepare','run']);p.add_argument('--work',type=Path,required=True);p.add_argument('--app',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    print(json.dumps(prepare(a.app,a.work) if a.mode=='prepare' else run(a.work,a.output),indent=2))
