#!/usr/bin/env python3
"""Fixed native composition cases on symbol-rich 9246; no rendering required."""
import argparse,json,subprocess,datetime
from pathlib import Path
import offline_parser as base
import offline_xml
import probe_skin_host
CASES=[
 ('flat','<button><pos x="10" y="15"/><size width="30" height="20"/></button><button><pos x="100" y="50"/><size width="60" height="25"/></button>'),
 ('nested','<panel name="outer" visible="yes"><pos x="40" y="30"/><size width="200" height="100"/><button><pos x="7" y="9"/><size width="30" height="20"/></button></panel>'),
 ('nested_relative','<panel name="outer" visible="yes"><pos x="40" y="30"/><size width="200" height="100"/><button><pos x="+7" y="+9"/><size width="30" height="20"/></button></panel>'),
 ('expressions','<button><pos x="100-20" y="80/2"/><size width="10*3" height="5+15"/></button>'),
 ('deck','<deck deck="1"><button><pos x="10" y="15"/><size width="30" height="20"/></button></deck>'),
 ('class','<define class="tile"><size width="80" height="24"/></define><button class="tile"><pos x="12" y="18"/></button>'),
 ('class_override','<define class="tile"><size width="80" height="24"/></define><button class="tile"><pos x="12" y="18"/><size width="45" height="16"/></button>'),
 ('class_partial_override','<define class="tile"><size width="80" height="24"/></define><button class="tile"><pos x="12" y="18"/><size width="45"/></button>'),
 ('class_forward','<button class="tile"><pos x="12" y="18"/></button><define class="tile"><size width="80" height="24"/></define>'),
 ('unknown_wrapper','<zzwrapper><button><pos x="10" y="15"/><size width="30" height="20"/></button></zzwrapper>'),
 ('unknown_class','<button class="zzmissing"><pos x="12" y="18"/><size width="45" height="16"/></button>'),
]
def fixtures():return [(name,'<skin name="Composition probe" version="8" width="320" height="200">'+xml+'</skin>') for name,xml in CASES]

def prepare(app,work):
 probe_skin_host.prepare(app,work)
 finish_prepare(work)

def finish_prepare(work, cases=None, extra_classes=(), extra_prefixes=(), host_source=None):
 host_source=host_source or base.ROOT/'tools/plugin/offline_composition_host.cpp'
 cases=fixtures() if cases is None else cases
 from extract_action_vtables import demangled,symbol_maps
 from extract_verb_table import sections,slice_offset
 from extract_skin_classes import function_starts
 from types import SimpleNamespace
 from capstone import Cs,CS_ARCH_ARM64,CS_MODE_LITTLE_ENDIAN
 data=(work/'original.universal').read_bytes();offset=slice_offset(data);sec=next(s for s in sections(data,offset) if s[1]=='__text');starts=function_starts(SimpleNamespace(data=data,base=offset));ends=dict(zip(starts,starts[1:]));symbols,vtables=symbol_maps(demangled(work/'original.universal','arm64'));md=Cs(CS_ARCH_ARM64,CS_MODE_LITTLE_ENDIAN)
 prefixes=('CImage::CImage(', 'CSkinPanel::CSkinPanel(', 'ISkinObject::createSkinObject(', 'CSkinGrabZone::CSkinGrabZone(', 'CSkinButton::CSkinButton(', 'ISkinContainer::ISkinContainer(', 'ISkinContainer::draw(', 'ISkinContainer::move(', 'CSkinPanel::loadChildren(', 'CSkinPanel::move(', 'ISkinObject::load(', 'CSkinClass::apply(', 'CSkinClass::applyXml(', 'CSkinClass::add(', 'CSkinWindow::load(', 'CSkinWindow::CSkinWindow(', 'CXMLFile::loadFromBuffer(')
 prefixes+=tuple(extra_prefixes)
 routines=[]
 for address,name in symbols.items():
  if not name.startswith(prefixes) or address not in ends:continue
  off=offset+sec[4]+address-sec[2];body=data[off:off+ends[address]-address]
  routines.append(dict(address=address,size=len(body),symbol=name,sha256=base.digest(body),instructions=[dict(pc=hex(i.address),instruction=i.mnemonic+' '+i.op_str) for i in md.disasm(body,address)]))
 vtables={name[len('vtable for '):]:address for address,name in symbols.items() if name.startswith('vtable for ')}
 classes=[dict(name=name,address=vtables[name]+16,container=name!='CSkinGrabZone') for name in ('CSkinWindow','CSkinPanel','CSkinButton','CSkinGrabZone')]
 classes.extend(extra_classes)
 manifest=dict(build='18.0.9246',binary_sha256=base.digest(data),routines=routines,classes=classes,layout={'current_rect':8,'definition_rect':24,'deck_field':64,'children_begin':192,'children_end':200,'children_capacity':208},scope='Reviewed container ABI and fixed native composition cases, not a complete skin schema.')
 (work/'composition-layout.json').write_text(json.dumps(manifest,indent=2)+'\n')
 header='constexpr XMLGuard compositionGuards[]={\n'+''.join('{%s,%d,"%s"},\n'%(hex(r['address']),r['size'],r['sha256']) for r in routines)+'};\n'
 header+='struct CompositionClass {const char* name; uint64_t address; bool container;};\nconstexpr CompositionClass compositionClasses[]={'+','.join('{"%s",%s,%s}'%(c['name'],hex(c['address']),str(c['container']).lower()) for c in classes)+'};\n'
 header+='constexpr const char* compositionCases[]={'+','.join(json.dumps(x) for n,x in cases)+'};\n'
 (work/'composition_guard.h').write_text(header)
 base.call(['clang++','-std=c++17','-arch','arm64','-I',work,host_source,'-o',work/'bin/host'])
 prep=json.loads((work/'preparation.json').read_text());prep.update(host_sha256=base.digest((work/'bin/host').read_bytes()),composition_host_source_sha256=base.digest(host_source.read_bytes()),composition_layout_sha256=base.digest((work/'composition-layout.json').read_bytes()),composition_guard_sha256=base.digest((work/'composition_guard.h').read_bytes()),composition_cases=cases)
 (work/'preparation.json').write_text(json.dumps(prep,indent=2)+'\n')

def run(work,output,cases=None):
 cases=fixtures() if cases is None else cases
 if output.exists():raise ValueError('capture exists')
 prep=offline_xml.verify_preparation(work)
 for path,key in [('composition-layout.json','composition_layout_sha256'),('composition_guard.h','composition_guard_sha256')]:
  if base.digest((work/path).read_bytes())!=prep[key]:raise ValueError('prepared composition artifact changed')
 if prep['composition_cases']!=[list(c) for c in cases]:raise ValueError('cases changed')
 if base.digest((work/'minimal.png').read_bytes())!=prep['fixtures']['minimal.png']:raise ValueError('image changed')
 capture=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),preparation=prep,runs=[],suite_finished=False,scope='Native window composition and panel move; no rendering or evaluation.')
 env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(work),'TMPDIR':str(work)}
 for i,(name,xml) in enumerate(cases):
  args=[str(work/'bin/host'),str(work/'libvdj-parser.dylib'),str(i),str(work/'sandbox.sb')]
  try:
   p=subprocess.run(args,cwd=work,env=env,capture_output=True,text=True,timeout=25);row=dict(name=name,xml=xml,argv=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
  except subprocess.TimeoutExpired as e:row=dict(name=name,xml=xml,argv=args,timeout=True,stdout=(e.stdout or b'').decode(errors='replace'),stderr=(e.stderr or b'').decode(errors='replace'))
  row['events']=[json.loads(l) for l in row['stdout'].splitlines()];row['completed']=row.get('returncode')==0 and row['events'][-1:]==[{'event':'complete'}]
  capture['runs'].append(row);output.write_text(json.dumps(capture,indent=2)+'\n');print(name,row['completed'],flush=True)
 capture['suite_finished']=True
 capture['all_cases_completed']=all(row['completed'] for row in capture['runs'])
 output.write_text(json.dumps(capture,indent=2)+'\n')
 if not capture['all_cases_completed']:raise RuntimeError('composition workers failed; see saved capture')

def show(case,stage,capture):
 """Read saved native evidence; never load the vendor binary."""
 data=json.loads(capture.read_text())
 row=next(r for r in data['runs'] if r['name']==case)
 event=next(e for e in row['events'] if e['event']=='composition' and e['stage']==stage)
 print(json.dumps(dict(build=data['preparation']['build'],case=case,xml=row['xml'],stage=stage,tree=event['tree']),indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('mode',choices=['prepare','run','show'])
 p.add_argument('--app',type=Path)
 p.add_argument('--work',type=Path)
 p.add_argument('--output',type=Path)
 p.add_argument('--case',choices=[name for name,_ in CASES],default='nested_relative')
 p.add_argument('--stage',choices=['loaded','resized','restored'],default='loaded')
 p.add_argument('--capture',type=Path,default=base.ROOT/'tests/offline-skin-composition-9246.json')
 a=p.parse_args()
 if a.mode=='show':show(a.case,a.stage,a.capture)
 else:
  if a.work is None:p.error('--work is required for prepare/run')
  if a.mode=='prepare':
   if a.app is None:p.error('--app is required for prepare')
   prepare(a.app.resolve(),a.work.resolve())
  else:
   if a.output is None:p.error('--output is required for run')
   run(a.work.resolve(),a.output.resolve())
