#!/usr/bin/env python3
"""Read-only query/cast probes with debug UI output; --batch 1..4 sends a fixed batch."""
import argparse
import json
import os
from pathlib import Path
import time
from datetime import datetime, timezone
import urllib.parse
import urllib.request
CASES=[('loaded-direct','deck 1 get_genre & debug'),
       ('loaded-cast','deck 1 get_genre & param_cast & debug'),
       ('loaded-typo','deck 1 getgenre & param_cast & debug'),
       ('loaded-junk','deck 1 zzcastalpha & param_cast & debug'),
       ('empty-cast','deck 2 get_genre & param_cast & debug'),
       ('empty-typo','deck 2 getgenre & param_cast & debug'),
       ('empty-junk','deck 2 zzcastalpha & param_cast & debug'),
       ('bad-selector','deck spoon get_genre & param_cast & debug')]

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--batch',type=int,choices=range(1,5));p.add_argument('--output',type=Path);a=p.parse_args()
 if not a.batch: print(json.dumps(CASES,indent=2));return
 if not a.output:p.error('--output required')
 journal=a.output.with_suffix('.jsonl')
 if a.output.exists() or journal.exists():p.error('Fresh paths required')
 d={'build':None,'batch':a.batch,'cases':[],'complete':False}
 with journal.open('x') as f:
  def log(**row):
   f.write(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),**row})+'\n');f.flush();os.fsync(f.fileno())
  def request(script,kind='query'):
   log(intent={'kind':kind,'script':script})
   with urllib.request.urlopen('http://localhost/'+kind+'?'+urllib.parse.urlencode({'script':script}),timeout=20) as r:v=r.read().decode().strip()
   log(response=v);time.sleep(.15);return v
  def context():return {f'deck {n} {v}':request(f'deck {n} {v}') for n in range(1,5) for v in ('loaded','play')}
  try:
   d['build']=request('get_build');d['before']=context()
   if d['build']!='9644' or d['before']['deck 1 loaded']!='yes' or d['before']['deck 2 loaded']!='no':raise ValueError('Requires 9644, loaded deck 1, empty deck 2')
   groups=[CASES[:4],CASES[4:],list(reversed(CASES[4:])),list(reversed(CASES[:4]))]
   for name,script in groups[a.batch-1]:
    request(f"debug 'QC{a.batch}_{name}'",'execute')
    returned=request(script,'execute')
    d['cases'].append({'name':name,'script':script,'execute_return':returned,'observation':'Requires saved debug screenshot'})
   request(f"debug 'QC{a.batch}_END'",'execute')
   d['after']=context()
   if d['before']!=d['after']:raise ValueError('Deck loaded/play state changed')
   d['complete']=True
  except Exception as e:d['error']=str(e);raise
  finally:a.output.write_text(json.dumps(d,indent=2)+'\n')
 print('Completed batch',a.batch)
if __name__=='__main__':main()
