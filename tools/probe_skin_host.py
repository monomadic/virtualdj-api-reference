#!/usr/bin/env python3
"""Isolated native skin window/full-engine host experiment on 9246 arm64."""
import argparse,json,datetime,struct,zlib,subprocess,zipfile,shutil,plistlib
from pathlib import Path
import offline_xml,offline_parser as base

def prepare(app,work):
 offline_xml.prepare(app,work)
 from capstone import Cs,CS_ARCH_ARM64,CS_MODE_LITTLE_ENDIAN
 from extract_verb_table import sections,slice_offset
 from extract_skin_classes import function_starts
 from extract_action_vtables import demangled,symbol_maps
 from types import SimpleNamespace
 data=(work/'original.universal').read_bytes();offset=slice_offset(data);sec=next(s for s in sections(data,offset) if s[1]=='__text')
 starts=function_starts(SimpleNamespace(data=data,base=offset));ends=dict(zip(starts,starts[1:]));symbols,_=symbol_maps(demangled(work/'original.universal','arm64'));md=Cs(CS_ARCH_ARM64,CS_MODE_LITTLE_ENDIAN)
 prefixes=('CSkinEngine::load(', 'CSkinEngine::CSkinEngine(', 'CSkinWindow::CSkinWindow(', 'CSkinWindow::load(', 'CSkinWindow::drawWindow(', 'CImage::CImage(', 'CImage::loadFromFile(', 'CImage::saveToPNG(', 'IOSWindow::IOSWindow(', 'IRenderTarget::getNew(', 'CRenderTargetMetal::create(', 'CRenderTargetMetal::resize(', 'CRenderTargetMetal::createRenderTarget(', 'CRenderTargetMetal::beginDraw(', 'CRenderTargetMetal::copyRenderTargetData(', 'CImage::construct(', 'CSkinPanel::draw(', '-[CNSRenderTargetMetal beginDraw:', '-[CNSRenderTargetMetal setRenderTargetBeginDraw:', '-[CNSRenderTargetMetal setCmdBuffer:')
 routines=[]
 for address,name in symbols.items():
  if not name.startswith(prefixes) or address not in ends:continue
  off=offset+sec[4]+address-sec[2];body=data[off:off+ends[address]-address]
  routines.append(dict(address=address,size=len(body),symbol=name,sha256=base.digest(body),instructions=[dict(pc=hex(i.address),instruction=i.mnemonic+' '+i.op_str) for i in md.disasm(body,address)]))
 (work/'skin-layout.json').write_text(json.dumps({'build':'18.0.9246','source_sha256':base.digest(data),'routines':routines},indent=2)+'\n')
 header='constexpr XMLGuard skinGuards[]={\n'+''.join('{%s,%d,"%s"},\n'%(hex(r['address']),r['size'],r['sha256']) for r in routines)+'};\n'
 (work/'offline_skin_guard.h').write_text(header)
 base.call(['clang++','-std=c++17','-arch','arm64','-I',work,base.ROOT/'tools/plugin/offline_skin_host.cpp','-lobjc','-o',work/'bin/host'])
 xml='<skin name="Offline probe" version="8" width="320" height="200"><button><pos x="20" y="20"/><size width="100" height="40"/><up x="0" y="0"/></button></skin>'
 (work/'minimal.xml').write_text(xml)
 def chunk(tag,payload):return struct.pack('>I',len(payload))+tag+payload+struct.pack('>I',zlib.crc32(tag+payload)&0xffffffff)
 raw=b''.join(b'\0'+b''.join(bytes([230,120,40,255] if x<100 and y<40 else [40,90,160,255]) for x in range(320)) for y in range(200))
 png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',320,200,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b'')
 (work/'minimal.png').write_bytes(png)
 with zipfile.ZipFile(work/'minimal.zip','w') as archive:
  archive.writestr('minimal.xml',xml);archive.writestr('minimal.png',png)
 (work/'Skins').mkdir()
 for f in ('minimal.xml','minimal.png','minimal.zip'):shutil.copyfile(work/f,work/'Skins'/f)
 prep=json.loads((work/'preparation.json').read_text());prep.update(host_sha256=base.digest((work/'bin/host').read_bytes()),skin_host_source_sha256=base.digest((base.ROOT/'tools/plugin/offline_skin_host.cpp').read_bytes()),skin_layout_sha256=base.digest((work/'skin-layout.json').read_bytes()),fixtures={f:base.digest((work/f).read_bytes()) for f in ('minimal.xml','minimal.png','minimal.zip','Skins/minimal.xml','Skins/minimal.png','Skins/minimal.zip')})
 bundle=work/'Host.app/Contents';(bundle/'MacOS').mkdir(parents=True);(bundle/'Resources').mkdir()
 shutil.copyfile(work/'bin/host',bundle/'MacOS/host');(bundle/'MacOS/host').chmod(0o755)
 (bundle/'Frameworks').symlink_to('../../Frameworks')
 shutil.copyfile(app/'Contents/Resources/default.metallib',bundle/'Resources/default.metallib')
 (bundle/'Info.plist').write_bytes(plistlib.dumps(dict(CFBundleExecutable='host',CFBundleIdentifier='org.local.vdj-skin-probe',CFBundleName='Offline skin probe',CFBundlePackageType='APPL')))
 prep['launch_host']='Host.app/Contents/MacOS/host'
 prep['bundle_files']={str(p.relative_to(work)):base.digest(p.read_bytes()) for p in bundle.rglob('*') if p.is_file() and not p.is_symlink()}
 prep['bundle_symlinks']={'Host.app/Contents/Frameworks':'../../Frameworks'}
 (work/'preparation.json').write_text(json.dumps(prep,indent=2)+'\n');print('Prepared',work)

def rendered_png(raw):
 if len(raw)!=320*200*4:raise ValueError('unexpected readback size')
 rgba=bytearray(raw)
 for i in range(0,len(raw),4):rgba[i],rgba[i+2]=raw[i+2],raw[i]
 def chunk(tag,payload):return struct.pack('>I',len(payload))+tag+payload+struct.pack('>I',zlib.crc32(tag+payload)&0xffffffff)
 rows=b''.join(b'\0'+rgba[y*1280:(y+1)*1280] for y in range(200))
 return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',320,200,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(rows))+chunk(b'IEND',b'')

def verify_pixels(raw):
 if len(raw)!=320*200*4:raise ValueError('wrong pixel length')
 for y in range(200):
  for x in range(320):
   orange=(x<100 and y<40) or (20<=x<120 and 20<=y<60)
   expected=bytes((40,120,230,255) if orange else (160,90,40,255))
   if raw[(y*320+x)*4:(y*320+x+1)*4]!=expected:raise ValueError(f'pixel mismatch at {x},{y}')
 return True

def run(work,output):
 if output.exists() or output.with_suffix('.png').exists():raise ValueError('capture exists')
 (work/'render.bgra').unlink(missing_ok=True)
 prep=offline_xml.verify_preparation(work)
 for f,sha in {**prep['fixtures'],**prep.get('bundle_files',{})}.items():
  if base.digest((work/f).read_bytes())!=sha:raise ValueError('fixture changed')
 for f,target in prep.get('bundle_symlinks',{}).items():
  if str((work/f).readlink())!=target:raise ValueError('bundle link changed')
 if base.digest((work/'skin-layout.json').read_bytes())!=prep['skin_layout_sha256']:raise ValueError('skin layout changed')
 commands='\n'.join(['settings set target.disable-aslr false','settings set target.env-vars HOME='+str(work)+' TMPDIR='+str(work),'command script import '+str(base.ROOT/'tools/offline_skin_trace.py'),'skin-setup','run','process status','script p=lldb.debugger.GetSelectedTarget().GetProcess(); lldb.debugger.HandleCommand("thread backtrace all") if p.GetState()==lldb.eStateStopped else None','quit',''])
 (work/'skin-trace.lldb').write_text(commands)
 capture={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'preparation':prep,'fixture_xml':(work/'minimal.xml').read_text(),'trace_source_sha256':base.digest((base.ROOT/'tools/offline_skin_trace.py').read_bytes()),'driver_source_sha256':base.digest(Path(__file__).read_bytes()),'commands':commands,'runs':[],'suite_finished':False}
 for mode in ('window','offscreen','engine'):
  args=['xcrun','lldb','--batch','-s',str(work/'skin-trace.lldb'),'--',str(work/prep.get('launch_host','bin/host')),str(work/'libvdj-parser.dylib'),mode,str(work/'sandbox.sb')]
  try:
   p=subprocess.run(args,cwd=work,capture_output=True,text=True,timeout=55);row=dict(mode=mode,argv=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
  except subprocess.TimeoutExpired as e:row=dict(mode=mode,argv=args,timeout=True,stdout=(e.stdout or b'').decode(errors='replace'),stderr=(e.stderr or b'').decode(errors='replace'))
  row['events']=[json.loads(l) for l in row['stdout'].splitlines() if l.startswith('{"event":')];row['trace']=[json.loads(l[10:]) for l in row['stdout'].splitlines() if l.startswith('SKINTRACE ')]
  row['completed']=row['events'][-1:]==[{'event':'complete'}];capture['runs'].append(row);output.write_text(json.dumps(capture,indent=2)+'\n');print(mode,row['completed'],flush=True)
 if any(r['mode']=='offscreen' and r['completed'] for r in capture['runs']):
  raw=(work/'render.bgra').read_bytes();png=rendered_png(raw);frame=output.with_suffix('.png');frame.write_bytes(png)
  capture['render']={'png_file':frame.name,'png_sha256':base.digest(png),'raw_bgra_sha256':base.digest(raw),'width':320,'height':200,'stride':1280,'expected_pixels_match':verify_pixels(raw),'oracle':'blue background with orange source rectangle [0,100)x[0,40) and native button copy at [20,120)x[20,60)'}
 capture['suite_finished']=True;output.write_text(json.dumps(capture,indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','run']);p.add_argument('--work',type=Path,required=True);p.add_argument('--app',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();prepare(a.app,a.work) if a.mode=='prepare' else run(a.work,a.output)
