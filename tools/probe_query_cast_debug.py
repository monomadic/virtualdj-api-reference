#!/usr/bin/env python3
"""Fixed query/cast probes with debug UI output. Default prints the selected plan."""
import argparse
import hashlib
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
CASTS=[('bare',''),('float','float'),('integer','integer'),('percentage','percentage'),
       ('ms','ms'),('beats','beats'),('boolean','boolean'),('text','text'),
       ('int-trunc','int_trunc'),('frac','frac'),('relative','relative'),('absolute','absolute'),
       ('format',"'000'"),('text-limit',"'text' 3"),('junk-alpha','zzcastalpha'),('junk-beta','zzcastbeta')]
CAST_CASES=[(f'{source_name}-{name}',f'{source} & param_cast {tail}'.rstrip()+' & debug')
            for source_name,source in [('number','constant 1.75'),('text',"get_text '1.75'")]
            for name,tail in CASTS]

def check_cast_capture(folder):
 observations=json.loads((folder/'observations.json').read_text())
 seen=set();results={}
 for row in observations['observations']:
  key=(row['batch'],row['name'])
  if key in seen:raise ValueError('Duplicate observation')
  seen.add(key)
  batch=json.loads((folder/f"batch{row['batch']}.json").read_text())
  if not batch['complete'] or batch['build']!='9644' or batch['before']!=batch['after']:raise ValueError('Incomplete batch or changed state')
  raw=next(r for r in batch['cases'] if r['name']==row['name'])
  if raw['script']!=dict(CAST_CASES)[row['name']]:raise ValueError('Script mismatch')
  results.setdefault(row['name'],[]).append((raw['query_result'],row['debug']))
 groups=[CAST_CASES[i:i+8] for i in range(0,len(CAST_CASES),8)]
 groups += [list(reversed(g)) for g in reversed(groups)]
 expected={(i+1,name) for i,g in enumerate(groups) for name,_ in g}
 if seen!=expected or any(len(v)!=2 or v[0]!=v[1] for v in results.values()):raise ValueError('Missing cases or disagreement across rounds')
 if {row['screenshot'] for row in observations['observations']}!=set(observations['sha256']):raise ValueError('Screenshot coverage mismatch')
 for name,digest in observations['sha256'].items():
  if hashlib.sha256((folder/name).read_bytes()).hexdigest()!=digest:raise ValueError('Screenshot hash mismatch')
 print('Cast capture: joins, round agreement, unchanged state and screenshot hashes verified')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--batch',type=int,choices=range(1,9));p.add_argument('--output',type=Path);p.add_argument('--suite',choices=['genre','casts'],default='genre');p.add_argument('--check',type=Path,help='Check saved cast capture directory offline');a=p.parse_args()
 if a.check:check_cast_capture(a.check);return
 cases=CASES if a.suite=='genre' else CAST_CASES
 size=4 if a.suite=='genre' else 8
 groups=[cases[i:i+size] for i in range(0,len(cases),size)]
 groups+= [list(reversed(g)) for g in reversed(groups)]
 if not a.batch: print(json.dumps(cases,indent=2));return
 if a.batch>len(groups):p.error('Batch outside selected suite')
 if not a.output:p.error('--output required')
 journal=a.output.with_suffix('.jsonl')
 if a.output.exists() or journal.exists():p.error('Fresh paths required')
 d={'build':None,'batch':a.batch,'suite':a.suite,'cases':[],'complete':False}
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
   if d['build']!='9644':raise ValueError('Requires build 9644')
   if a.suite=='genre' and (d['before']['deck 1 loaded']!='yes' or d['before']['deck 2 loaded']!='no'):raise ValueError('Requires loaded deck 1, empty deck 2')
   for name,script in groups[a.batch-1]:
    request(f"debug '{a.suite}{a.batch}_{name}'",'execute')
    returned=request(script,'execute')
    row={'name':name,'script':script,'execute_return':returned,'observation':'Requires saved debug screenshot'}
    if a.suite=='casts':
     row['query_script']=script.removesuffix(' & debug')
     row['query_result']=request(row['query_script'])
    d['cases'].append(row)
   request(f"debug '{a.suite}{a.batch}_END'",'execute')
   d['after']=context()
   if d['before']!=d['after']:raise ValueError('Deck loaded/play state changed')
   d['complete']=True
  except Exception as e:d['error']=str(e);raise
  finally:a.output.write_text(json.dumps(d,indent=2)+'\n')
 print('Completed batch',a.batch)
if __name__=='__main__':main()
