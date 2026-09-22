#!/usr/bin/env python3
"""Query shared skin attribute contracts; tables are projections, not editable copies."""
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STORE=ROOT/'docs/skin-attribute-contracts.json'


def load():
    data=json.loads(STORE.read_text())
    if data['schema_version']!=1:raise ValueError('unsupported attribute contract schema')
    for key,row in data['definitions'].items():
        if row['value_ref'] not in data['value_types']:raise ValueError('unknown value reference: '+key)
        if not row['sources'] or any(not (ROOT/p).is_file() for p in row['sources']):
            raise ValueError('missing evidence source: '+key)
    for tag,mapping in data['elements'].items():
        if any(ref not in data['definitions'] for ref in mapping.values()):raise ValueError('unknown contract reference: '+tag)
    return data


def attribute_rows(element, observed=None, data=None):
    data=data if data is not None else load()
    if observed is None:
        from xmldb import load as inventory,rows
        observed={}
        for family,name,entry in rows(inventory()):
            if name==element and family in ('skins','video_skins'):
                for attr,count in entry['attributes'].items():observed[attr]=observed.get(attr,0)+count
    mapping=data['elements'].get(element,{})
    result=[]
    for attr in sorted(set(observed)|set(mapping)):
        ref=mapping.get(attr);contract=data['definitions'].get(ref,{})
        value=data['value_types'].get(contract.get('value_ref'),{})
        result.append({'name':attr,'uses':observed.get(attr,0),'contract_ref':ref,
                       'value':(' | '.join(value['accepted_values']) if value.get('kind') == 'enum' else value.get('display','Unknown')),
                       'description':contract.get('description','Observed in XML; meaning and accepted values are not recorded.'),
                       'value_spec':value or None,'default':contract.get('default'),'constraints':contract.get('constraints'),
                       'context':contract.get('context','Observed tag context only; may include template parameters.'),
                       'status':contract.get('status','unknown'),'build':contract.get('build'),'sources':contract.get('sources',[])})
    return result


def markdown(rows):
    def cell(s):return str(s).replace('|','\\|').replace('\n',' ')
    lines=['| Attribute | Value | Description |','| --- | --- | --- |']
    for r in rows:
        note = {'reader_candidate': ' Reader candidate; behavior unverified.',
                'documented': ' Documentation summary; not live verification.'}.get(r['status'], '')
        lines.append('| '+ ' | '.join(cell(v) for v in [r['name'],r['value'],r['description']+note])+' |')
    return '\n'.join(lines)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('element');p.add_argument('--format',choices=['json','markdown'],default='markdown')
    a=p.parse_args();result=attribute_rows(a.element)
    print(json.dumps(result,indent=2) if a.format=='json' else markdown(result))
