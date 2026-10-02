#!/usr/bin/env python3
"""Validate saved XML spike evidence without loading vendor code or a debugger."""
import json
from pathlib import Path
import offline_parser as base
from offline_xml import CASES
from trace_offline_xml import TRACE_NAMES

def require(value,message):
    if not value:raise ValueError(message)

def check():
    root=base.ROOT/'tests';native=json.loads((root/'offline-xml-9246.json').read_text());trace=json.loads((root/'offline-xml-trace-9246.json').read_text())
    layout=root/'xml-reader-layout-9246.json'
    expected=json.loads(base.manifest_for('18.0.9246').read_text())
    for capture in (native,trace):
        prep=capture['preparation']
        require(capture['suite_finished'],'incomplete suite')
        require(prep['build']=='18.0.9246' and prep['source_sha256']==expected['binary_sha256'],'wrong source')
        require(prep['xml_layout_sha256']==base.digest(layout.read_bytes()),'layout mismatch')
        for row in capture['runs']:
            require(row['returncode']==0 and row['completed'] and not row.get('timeout'),'failed worker')
    require(native['preparation']['host_sha256']==trace['preparation']['host_sha256'],'different hosts')
    require([r['mode'] for r in native['runs']]==['--sandbox-check','--load-only']+[str(i) for i in range(len(CASES))],'missing native cases')
    base.validate_run(native['runs'][0],[])
    results={}
    for row,(name,xml) in zip(native['runs'][2:],CASES):
        require((row['name'],row['xml'])==(name,xml),'input identity mismatch')
        events=[json.loads(line) for line in row['stdout'].splitlines()]
        require(events==row['events'],'native events differ from raw output')
        sequence=['before_dlopen','loaded','guards_passed','xml_guards_passed','before_xml','xml_result']
        if name.startswith('factory_'):sequence+=['before_factory','factory_result']
        sequence+=['xml_closed','complete']
        require([e['event'] for e in events]==sequence,'missing native stage')
        results[name]=next(e for e in events if e['event']=='xml_result')
    for name in ('mismatched_end','unclosed','unquoted','empty'):
        r=results[name];require(not r['accepted'] and r['error'] and r['message']=='XMLError','failure observation changed')
    r=results['bad_declaration'];require(not r['accepted'] and not r['error'] and not r['message'],'declaration observation changed')
    for name in ('unknown_element','unknown_attribute','duplicate_attribute','case_mismatch','bare_ampersand','invalid_number','trailing_junk','second_root'):
        require(results[name]['accepted'],'permissive observation changed')
    for name in ('trailing_junk','second_root'):require(results[name]['position']==len('<skin/>'),'root boundary changed')
    require([r['name'] for r in trace['runs']]==TRACE_NAMES,'missing trace cases')
    pairs={}
    for row in trace['runs']:
        events=[json.loads(line[len('XMLTRACE '):]) for line in row['stdout'].splitlines() if line.startswith('XMLTRACE ')]
        host=[json.loads(line) for line in row['stdout'].splitlines() if line.startswith('{"event":')]
        require(events==row['trace'] and host==row['host_events'],'trace differs from raw output')
        require(host[-1:]==[{'event':'complete'}] and host[0]['event']=='sandbox_controls_passed','missing trace controls/completion')
        require(all(host[0].get(k) is True for k in ('home_read_denied','outside_write_denied','network_denied')),'sandbox control failed')
        require(any(e['event']=='xml_guards_passed' for e in host),'missing code guards')
        require(events[0]=={'event':'trace_ready'} and not row['read_errors'],'trace not readable')
        require(row['xml']==dict(CASES)[row['name']],'trace input mismatch')
        calls={};returns={}
        for e in events:
            require('read_error' not in e,'trace read error')
            if e['event']=='native_call':
                require(e['call_id'] not in calls,'duplicate call id');calls[e['call_id']]=e
            elif e['event']=='native_return':
                require(e['call_id'] in calls and e['call_id'] not in returns,'orphan/duplicate return')
                require(e['symbol']==calls[e['call_id']]['symbol'],'return symbol mismatch');returns[e['call_id']]=e
        for i,c in calls.items():
            if not c['symbol'].startswith(('CSkin','ISkinObject::ISkinObject')) and 'setErrorMessage' not in c['symbol']:
                require(i in returns,'missing return')
        pairs[row['name']]=[(calls[i],r) for i,r in returns.items()]
    for name,width in [('factory_button_geometry',10),('factory_button_bad_geometry',0),('factory_button_duplicate_width',10),('factory_button_case',10)]:
        require(any(c.get('key')=='width' and c['symbol'].startswith('CXMLNode::getIntParam') and r.get('value')==width for c,r in pairs[name]),'width observation changed')
    require(any(c['symbol'].startswith('IAction::create') and c.get('script')=='is_using cue' and r.get('vtable_symbol')=='vtable for ACTION_is_using' for c,r in pairs['factory_button_action']),'script bridge missing')
    for name,cls in [('factory_button','CSkinButton'),('factory_panel','CSkinPanel'),('factory_text','CSkinText')]:
        require(any(c['symbol'].startswith('ISkinObject::createSkinObject') and r.get('vtable_symbol')=='vtable for '+cls for c,r in pairs[name]),'factory class missing')
    require(any(c['symbol'].startswith('ISkinObject::createSkinObject') and r.get('object_present') is False for c,r in pairs['factory_unknown']),'unknown factory result changed')
    return dict(build='18.0.9246',saved_native_suite='verified',saved_trace_suite='verified',scope='offline observations only; no renderer parity claim')

if __name__=='__main__':print(json.dumps(check(),indent=2))
