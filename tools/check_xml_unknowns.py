#!/usr/bin/env python3
"""Check saved known/unknown consumption comparisons; never runs vendor code."""
import json
from pathlib import Path
from offline_parser import ROOT, validate_run
from probe_xml_unknowns import CASES
from check_offline_xml import require

def check():
    native=json.loads((ROOT/'tests/offline-xml-unknowns-9246.json').read_text())
    capture=json.loads((ROOT/'tests/offline-xml-unknowns-trace-9246.json').read_text())
    require(native['suite_finished'] and capture['suite_finished'],'unfinished capture')
    require(native['preparation']==capture['preparation'],'native and traced host differ')
    require(capture['preparation']['build']=='18.0.9246','wrong build')
    validate_run(native['runs'][0],[])
    require([(r['name'],r['xml']) for r in native['runs'][2:]]==CASES,'native inputs changed')
    require([(r['name'],r['xml']) for r in capture['runs']]==CASES,'traced inputs changed')
    result={}
    for r in native['runs']:
        require(r['returncode']==0 and r['completed'],'native run failed')
        events=[json.loads(line) for line in r['stdout'].splitlines()]
        require(events==r['events'] and events[-1:]==[{'event':'complete'}],'native output mismatch')
    for r in capture['runs']:
        require(r['completed'] and r['returncode']==0 and not r['read_errors'],'trace failed')
        require(not r['stderr'] and 'Traceback' not in r['stdout'],'debugger errors')
        trace=[json.loads(line[len('XMLTRACE '):]) for line in r['stdout'].splitlines() if line.startswith('XMLTRACE ')]
        require(trace==r['trace'],'raw trace mismatch')
        host=[json.loads(line) for line in r['stdout'].splitlines() if line.startswith('{"event":')]
        require(host==r['host_events'] and host[-1:]==[{'event':'complete'}],'host output mismatch')
        require(host[0]=={'event':'sandbox_controls_passed','home_read_denied':True,'outside_write_denied':True,'network_denied':True},'sandbox missing')
        require(any(e['event']=='xml_guards_passed' for e in host),'guards missing')
        before=next(e['tree'] for e in trace if e['event']=='tree_before_factory')
        summary=next(e for e in trace if e['event']=='watch_summary')
        require(before==summary['tree_after_factory'],'XML was mutated during factory')
        labels=[e['label'] for e in trace if e['event']=='watch_installed']
        require(set(labels)==set(summary['hits']) and len(labels)==len(set(labels)),'watch setup mismatch')
        for label,value in summary['hits'].items():
            require(value==sum(e['event']=='value_read' and e['label']==label for e in trace if 'label' in e),'watch count mismatch')
        factory=[e for e in trace if e['event']=='native_return' and e['symbol'].startswith('ISkinObject::createSkinObject')]
        require(len(factory)==1,'factory return missing')
        calls={e['call_id']:e for e in trace if e['event']=='native_call'}
        widths=[e['value'] for e in trace if e['event']=='native_return' and e['symbol'].startswith('CXMLNode::getIntParam') and calls[e['call_id']].get('key')=='width']
        result[r['name']]={'hits':summary['hits'],'object_present':factory[0]['object_present'],'widths':widths}
    for name in ('factory_unknown_tag','factory_known_child_as_root'):
        require(not result[name]['object_present'],'nonobject control changed')
    for name in ('factory_known','factory_unknown_attribute','factory_unknown_child'):
        r=result[name];require(r['object_present'] and r['widths']==[10],'known width not consumed')
        require(r['hits']['size.width.text']>0 and r['hits']['size.width.length']>0,'positive watch control failed')
    for name,label in [('factory_unknown_attribute','button.zzunknown'),('factory_unknown_child','zzchild.width'),('factory_misspelled_width','size.widht'),('factory_unknown_wrapper','size.width')]:
        require(all(result[name]['hits'][label+part]==0 for part in ('.text','.length')),'unconsumed value was read')
    for name in ('factory_misspelled_width','factory_unknown_wrapper'):
        require(result[name]['object_present'] and result[name]['widths']==[0],'fallback changed')
    return {'build':'18.0.9246','comparison':'known width read; candidate values unread during construction','XML_tree':'preserved','classification':'context-specific non-consumption; not a universal unknown-name oracle'}

if __name__=='__main__':print(json.dumps(check(),indent=2))
