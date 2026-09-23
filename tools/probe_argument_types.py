#!/usr/bin/env python3
"""Fixed debug/consumer argument comparison; default prints plan, --phase executes it."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time
import urllib.parse
import urllib.request

TARGET = '$argtype_target_9644'
SOURCE = '$argtype_source_9644'
CASES = [('integer', '1'), ('decimal', '0.5'), ('percent', '50%'),
         ('quoted-number', "'0.5'"), ('source-variable', f"'{SOURCE}'"),
         ('junk-alpha', "'zzargalpha'"), ('junk-beta', "'zzargbeta'"),
         ('missing', ''), ('signed', '+0.5'), ('milliseconds', '500ms')]
MULTIPLY_EXTRA = [('zero', '0'), ('quoted-action', "'constant 0.5'"),
                  ('computed-action', '`constant 0.5`')]


def run(phase, output, consumer='set'):
    if output.exists() or output.with_suffix('.jsonl').exists():
        raise ValueError('Use a fresh capture path')
    data = {'build': None, 'phase': phase, 'consumer': consumer, 'complete': False, 'cases': []}
    cases = CASES + MULTIPLY_EXTRA if consumer=='multiply' else CASES
    data['matrix'] = 'extended' if consumer=='multiply' else 'base'
    stream = output.with_suffix('.jsonl').open('x')
    def log(**row):
        stream.write(json.dumps({'utc': datetime.now(timezone.utc).isoformat(), **row})+'\n')
        stream.flush()
        os.fsync(stream.fileno())
    def request(script, kind='query'):
        log(intent={'kind':kind, 'script':script})
        with urllib.request.urlopen('http://localhost/'+kind+'?'+urllib.parse.urlencode({'script':script}), timeout=20) as r:
            result=r.read().decode().strip()
        log(response=result)
        time.sleep(.1)
        return result
    def context():
        return {f'deck {n} {v}':request(f'deck {n} {v}') for n in range(1,5) for v in ('loaded','play')}
    def read(var):
        return request(f"get_var '{var}'")
    def write(var, tail):
        return request(f"set '{var}' {tail}".rstrip(), 'execute')
    dirty=False
    try:
        data['build']=request('get_build')
        if data['build']!='9644': raise ValueError('Requires build 9644')
        data['context_before']=context()
        if any(v not in ('no','off','false','0') for v in data['context_before'].values()):
            raise ValueError('Requires empty stopped decks')
        if phase=='values':
            data['variables_before']={v:read(v) for v in (TARGET,SOURCE)}
            for v in data['variables_before'].values():
                if v not in ('', '0'):
                    raise ValueError('Dedicated variables must be unset or zero; avoids lossy restoration through formatted readback')
            log(baseline=data)
            dirty=True
            write(SOURCE,'0.37')
            if read(SOURCE)!='0.37': raise ValueError('Source calibration failed')
            if consumer=='multiply':
                request(f"param_multiply 0.8 0.5 & set '{TARGET}'", 'execute')
                if read(TARGET)!='0.4': raise ValueError('Multiply pipeline calibration failed')
            for round_number in (1,2):
                for name,tail in (cases if round_number==1 else list(reversed(cases))):
                    write(TARGET,'0.12')
                    if read(TARGET)!='0.12': raise ValueError('Reset failed')
                    script=(f"set '{TARGET}' {tail}".rstrip() if consumer=='set' else
                            f"param_multiply 0.8 {tail}".rstrip()+f" & set '{TARGET}'")
                    returned=request(script,'execute')
                    row={'round':round_number,'case':name,'argument':tail,'execute_return':returned,'value':read(TARGET)}
                    row['execute_script']=script
                    if consumer=='multiply':
                        row['query_script']=f"param_multiply 0.8 {tail}".rstrip()
                        row['query_result']=request(row['query_script'])
                    data['cases'].append(row)
                    log(observation=row)
        else:
            group=int(phase[-1])
            for name,tail in cases[(group-1)*5:group*5]:
                request(f"debug '{consumer}_TYPE_{name}'", 'execute')
                script=(('debug '+tail).rstrip() if consumer=='set' else
                        f"param_multiply 0.8 {tail}".rstrip()+' & debug')
                returned=request(script,'execute')
                data['cases'].append({'case':name,'script':script,'execute_return':returned,'type':'requires retained UI readback'})
            request(f"debug 'TYPE_GROUP_{group}_END'", 'execute')
        data['complete']=True
    except Exception as e:
        data['error']=str(e)
        raise
    finally:
        try:
            if dirty:
                restored={}
                for var,old in data['variables_before'].items():
                    write(var,old or '0')
                    restored[var]=read(var)
                    if float(restored[var])!=float(old or '0'): raise ValueError('Restore failed')
                data['restoration']={'values':restored,'verified':True,'limitation':'Initially unset variables restored to zero, not deleted'}
            data['context_after']=context()
            if data['context_after']!=data.get('context_before'): raise ValueError('Deck state changed')
        finally:
            output.write_text(json.dumps(data,indent=2)+'\n')
            stream.close()
    print(json.dumps(data,indent=2))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase',choices=['values','debug1','debug2','debug3'])
    p.add_argument('--output',type=Path)
    p.add_argument('--consumer',choices=['set','multiply'],default='set')
    p.add_argument('--check',type=Path,help='check a completed values capture offline')
    a=p.parse_args()
    if a.check:
        d=json.loads(a.check.read_text())
        assert d['complete'] and d['build']=='9644' and d['phase']=='values'
        assert d['restoration']['verified'] and d['context_before']==d['context_after']
        cases=CASES + MULTIPLY_EXTRA if d.get('matrix')=='extended' else CASES
        expected={(r,n) for r in (1,2) for n,_ in cases}
        seen=set()
        outcomes={}
        for row in d['cases']:
            key=(row['round'],row['case'])
            assert key in expected and key not in seen
            assert row['argument']==dict(cases)[row['case']]
            seen.add(key)
            outcomes.setdefault(row['case'],set()).add(row['value'])
        assert seen==expected and all(len(v)==1 for v in outcomes.values())
        if d.get('consumer','set')=='set':
            assert outcomes['integer']=={'1'} and outcomes['source-variable']=={'0.37'}
        else:
            assert outcomes['integer']=={'0.8'} and outcomes['decimal']=={'0.4'}
            queries={}
            for row in d['cases']:
                queries.setdefault(row['case'],set()).add(row['query_result'])
            assert all(len(v)==1 for v in queries.values())
        print('Argument capture: complete, rounds agree, controls and restoration verified')
    elif a.phase=='debug3' and a.consumer!='multiply': p.error('debug3 requires multiply')
    elif not a.phase: print(json.dumps(CASES + MULTIPLY_EXTRA if a.consumer=='multiply' else CASES,indent=2))
    elif not a.output: p.error('--phase requires a fresh --output')
    else: run(a.phase,a.output,a.consumer)

if __name__=='__main__': main()
