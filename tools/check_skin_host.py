#!/usr/bin/env python3
"""Validate saved native render evidence and the full-loader limitation offline."""
import json,struct,zlib
from pathlib import Path
import offline_parser as base
from probe_skin_host import verify_pixels
from check_offline_xml import require

def check():
 path=base.ROOT/'tests/offline-skin-host-9246.json';data=json.loads(path.read_text());prep=data['preparation']
 require(data['suite_finished'],'unfinished suite')
 expected=json.loads(base.manifest_for('18.0.9246').read_text())
 require(prep['build']=='18.0.9246' and prep['source_sha256']==expected['binary_sha256'],'wrong binary')
 require(base.digest((base.ROOT/'tests/skin-host-layout-9246.json').read_bytes())==prep['skin_layout_sha256'],'layout changed')
 require([r['mode'] for r in data['runs']]==['window','offscreen','engine'],'missing modes')
 for row in data['runs']:
  events=[json.loads(l) for l in row['stdout'].splitlines() if l.startswith('{"event":')]
  traces=[json.loads(l[10:]) for l in row['stdout'].splitlines() if l.startswith('SKINTRACE ')]
  require(events==row['events'] and traces==row['trace'],'raw output mismatch')
  require(not row.get('timeout') and row['returncode']==0,'debugger failed')
  require('Traceback' not in row['stdout'] and not row['stderr'],'debugger error')
  require(events[:3]==[{'event':'sandbox_controls_passed','home_read_denied':True,'outside_write_denied':True,'network_denied':True},{'event':'guards_passed'},{'event':'skin_guards_passed'}],'missing isolation/guards')
  if row['mode']!='engine':
   require(row['completed'] and events[-1:]==[{'event':'complete'}],'worker did not complete')
   require({'event':'window_load_result','accepted':True,'width':320,'height':200} in events,'window load changed')
  else:
   require(not row['completed'],'full loader outcome changed: review evidence')
   require({'event':'blocked_message_box','message':'Graphics failed to initialize.'} in traces,'missing full-loader limitation')
   require(any('CSkinEngine::loadEnd()'==t.get('symbol') for t in traces),'full loader never reached loadEnd')
 row=data['runs'][1]
 require({'event':'host_offscreen_encoder_supplied'} in row['events'],'adapter missing')
 require({'event':'readback_result','accepted':True,'stride':1280,'width':320,'height':200} in row['events'],'readback missing')
 require(any(t.get('symbol','').startswith('CSkinButton::draw(') for t in row['trace']),'no native button drawing')
 render=data['render'];png=(path.parent/render['png_file']).read_bytes()
 require(base.digest(png)==render['png_sha256'],'frame changed')
 require(png[:8]==b'\x89PNG\r\n\x1a\n','bad PNG signature');offset=8;compressed=b'';header=None
 while offset<len(png):
  n=struct.unpack_from('>I',png,offset)[0];tag=png[offset+4:offset+8];payload=png[offset+8:offset+8+n]
  require(zlib.crc32(tag+payload)&0xffffffff==struct.unpack_from('>I',png,offset+8+n)[0],'PNG CRC mismatch')
  if tag==b'IHDR':header=struct.unpack('>IIBBBBB',payload)
  if tag==b'IDAT':compressed+=payload
  offset+=n+12
 require(header==(320,200,8,6,0,0,0),'unexpected PNG format')
 rows=zlib.decompress(compressed);require(len(rows)==200*1281,'pixel data length')
 raw=bytearray()
 for y in range(200):
  require(rows[y*1281]==0,'unsupported filter');row=bytearray(rows[y*1281+1:(y+1)*1281])
  for x in range(0,1280,4):row[x],row[x+2]=row[x+2],row[x]
  raw.extend(row)
 require(base.digest(raw)==render['raw_bgra_sha256'],'PNG does not match native readback')
 require(verify_pixels(raw) and render['expected_pixels_match'],'pixel oracle failed')
 return {'build':'18.0.9246','headless_native_render':'verified against every fixture pixel','full_application_loader':'reaches loadEnd; graphics initialization unresolved','scope':'offline native host, not live-app parity'}

if __name__=='__main__':print(json.dumps(check(),indent=2))
