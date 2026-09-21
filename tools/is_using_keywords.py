#!/usr/bin/env python3
"""Small validated view of consumer candidates and native recognition captures."""
import hashlib,json
from pathlib import Path


def check():
    suite=json.loads(Path('tests/is-using-keyword-cases.json').read_text())['scripts']
    header='// Frozen from tests/is-using-keyword-cases.json. Public queries only.\nstatic const char* kKeywordCases[] = {\n'+''.join('    '+json.dumps(s)+',\n' for s in suite)+'};\n'
    if Path('tools/plugin/is_using_cases.h').read_text()!=header:raise ValueError('compiled case list differs')
    files=sorted(Path('tests').glob('is-using-keywords-9644-run*.jsonl'))
    if not files:raise ValueError('no native captures')
    baseline=None
    for path in files:
        rows=[json.loads(line) for line in path.read_text().splitlines()]
        if rows[0]['event']!='start' or rows[0]['build']!=9644 or rows[0]['build_hresult']!=0 or rows[-1]!={'event':'complete'}:raise ValueError('incomplete capture or wrong build')
        cases=rows[1:-1]
        if len(cases)!=2*len(suite):raise ValueError('missing/extra cases')
        for round in (1,2):
            group=cases[(round-1)*len(suite):round*len(suite)]
            if [r['script'] for r in group]!=suite or any(r['round']!=round or r['event']!='case' for r in group):raise ValueError('case order differs')
            result={r['script']:{k:r[k] for k in ['numeric_hresult','numeric_value','text_hresult','text']} for r in group}
            if baseline is None:baseline=result
            if result!=baseline:raise ValueError('capture rounds differ')
    controls=[baseline['is_using zzunknowna'],baseline['is_using zzunknownb']]
    if controls[0]!=controls[1] or controls[0]['numeric_hresult']!=-2147467263:raise ValueError('nonsense controls do not agree')
    candidates=json.loads(Path('tests/is-using-consumer-9644.json').read_text())['literals']
    recognised=[];matches=[]
    for word in candidates:
        row=baseline['is_using '+word]
        if row['numeric_hresult']==0 and row['text_hresult']==0:recognised.append(word)
        elif row==controls[0]:matches.append(word)
        else:raise ValueError('unclassified candidate')
    if baseline['is_using']['numeric_hresult']!=-2147024809:raise ValueError('bare control drift')
    if baseline["is_using 'cue'"]!=baseline['is_using cue'] or baseline['is_using CUE']!=baseline['is_using cue']:raise ValueError('cue spelling control drift')
    pairs=[('is_using cue inaudible','is_using cue zzunknowna'),('is_using cue 1000ms inaudible','is_using cue 1000ms zzunknowna')]
    if not all(baseline[a]==baseline[b] for a,b in pairs):raise ValueError('modifier fixture now discriminates; reassess')
    journal=json.loads(Path('tests/is-using-keyword-run-9644.json').read_text())
    if not journal['state_checks_match'] or journal['before']!=journal['after']:raise ValueError('state restore not verified')
    if {str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}!=journal['captures']:raise ValueError('capture provenance mismatch')
    source=json.loads(Path(journal['consumer_source']).read_text())['source']
    if source['binary_sha256']!=journal['binary_sha256']:raise ValueError('consumer provenance mismatch')
    return {'build':'18.0.9644','recognised_as_first_argument':recognised,'first_argument_matches_nonsense':matches,'modifier_pairs_match_controls':pairs,'repeat_captures':len(files),'all_rounds_match':True,'state_checks_match':True,'claim_scope':'Recognition only in stopped/unloaded fixture; modifier behaviour and exhaustive grammar remain unresolved.'}

if __name__=='__main__':print(json.dumps(check(),indent=2))
