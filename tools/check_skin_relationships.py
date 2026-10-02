#!/usr/bin/env python3
"""Check paired native relationships, source-path traces and the partial manifest."""
import json
import offline_parser as base
from check_offline_xml import require
from probe_skin_relationships import fixtures
from trace_skin_relationships import NAMES
from native_skin_children import generate,ARTIFACT


def shape(node):
    return [node['class'], [shape(c) for c in node['children']]]


def check():
    folder=base.ROOT/'tests'
    data=json.loads((folder/'skin-child-relations-9246.json').read_text())
    trace=json.loads((folder/'skin-child-trace-9246.json').read_text())
    static=json.loads((folder/'skin-child-readers-9246.json').read_text())
    expected=json.loads(base.manifest_for('18.0.9246').read_text())
    require(data['suite_finished'] and data['all_cases_completed'],'unfinished native suite')
    require(trace['suite_finished'],'unfinished trace suite')
    require(static['source']['build']=='18.0.9246' and static['source']['binary_sha256']==expected['binary_sha256'],'wrong static source')
    for capture in [data,trace]:
        prep=capture['preparation']
        require(prep['source_sha256']==expected['binary_sha256'] and prep['build']=='18.0.9246','wrong host source')
        require(prep['relationship_source_sha256']==base.digest((folder/'skin-child-readers-9246.json').read_bytes()),'static evidence changed')
        require(prep['composition_layout_sha256']==base.digest((folder/'skin-child-layout-9246.json').read_bytes()),'ABI evidence changed')
        require(prep['composition_host_source_sha256']==base.digest((base.ROOT/'tools/plugin/offline_relationship_host.cpp').read_bytes()),'host wrapper changed')
        require(prep['composition_base_source_sha256']==base.digest((base.ROOT/'tools/plugin/offline_composition_host.cpp').read_bytes()),'base host changed')
        require(prep['composition_cases']==[list(c) for c in fixtures()],'prepared cases changed')
        for row in capture['runs']:
            require(row['completed'] and row['returncode']==0 and not row.get('timeout') and not row['stderr'],'worker failed')
            events=[json.loads(l) for l in row['stdout'].splitlines() if l.startswith('{"event":')]
            require(events==row['events'],'raw host output mismatch')
            require(events[:4]==[{'event':'sandbox_controls_passed','home_read_denied':True,'outside_write_denied':True,'network_denied':True},{'event':'guards_passed'},{'event':'composition_guards_passed'},{'event':'window_load_result','accepted':True}],'missing guards/load')
            require(events[-1:]==[{'event':'complete'}],'worker incomplete')
    require([(r['name'],r['xml']) for r in data['runs']]==fixtures(),'cases differ')
    rows={r['name']:r for r in data['runs']}
    trees={name:next(e['tree'] for e in r['events'] if e.get('stage')=='loaded') for name,r in rows.items()}
    def obj(name,children=()):return [name,list(children)]
    B=obj('CSkinButton');T=obj('CSkinText');P=lambda *c:obj('CSkinPanel',c)
    S=lambda *c:obj('CSkinSlider',c);I=lambda *c:obj('ISkinResizePanel',c)
    R=lambda *c:obj('CSkinResizePanel',c);K=lambda *c:obj('CSkinStack',c);A=lambda *c:obj('CSkinRack',c)
    X=lambda *c:obj('CSkinSplit',c)
    expected_shapes={
        'skin_button':[B],'panel_button':[P(B)],'button_button':[B],'slider_button':[S()],
        'textzone_button':[T],'group_button':[B],'group_visibility_button':[P(B)],'deck_button':[B],'setdeck_button':[B],
        'split_button':[X(I(),I())],'rack_button':[A()],'stack_button':[K()],'resizepanel_button':[R(B)],'unknown_button':[],
        'panel_panel':[P(P(B))],'button_text':[obj('CSkinButton',[T])],'panel_text':[P(T)],'button_panel':[B],
        'button_unknown_text':[B],'button_text_repeat':[obj('CSkinButton',[T])],'slider_text':[S()],
        'slider_fader':[S(obj('CSkinSliderFader'))],'split_content':[X(I(),I())],'split_panel':[X(I(),I())],
        'stack_panel':[K()],'rack_panel':[A()],'panel_unknown':[P()],'group_nested':[P(B)],'ordered_repeat':[B,B],
        'stack_item':[K(P(B))],'stack_item_repeat':[K(P(B),P(B))],'rack_unit_panel':[A(R(B))],'rack_unit_button':[A()],
        'split_left_right':[X(I(B),I(B))],'split_left_content':[X(I(B),I())],'resizepanel_content':[R(B)],
        'button_text_states':[obj('CSkinButton',[T,T,T,T])],
    }
    require(set(expected_shapes)==set(trees),'missing shape expectation')
    for name,tree in trees.items():
        require(tree['class']=='CSkinWindow','root class')
        children=tree['children'];require(children[0]['class']==children[-1]['class']=='CSkinGrabZone','generated root objects changed')
        require([shape(c) for c in children[1:-1]]==expected_shapes[name],name+': native relationship changed')
    for name in ['deck_button','setdeck_button']:
        require(trees[name]['children'][1]['deck_field']==2,'deck context lost')
    require([r['name'] for r in trace['runs']]==NAMES,'trace cases changed')
    traces={r['name']:r for r in trace['runs']}
    for name,row in traces.items():
        require(row['events']==rows[name]['events'],'debugger/native tree mismatch')
        require(row['trace']==[json.loads(l[11:]) for l in row['stdout'].splitlines() if l.startswith('CHILDTRACE ')],'raw trace mismatch')
        require(row['trace'][0]['event']=='ready' and not any('read_error' in t for t in row['trace']),'trace read error')
    def calls(name):return [t for t in traces[name]['trace'] if t['event']=='call']
    def factory(name):return [t for t in calls(name) if t['symbol'].startswith('ISkinObject::createSkinObject')]
    require([t['source_path'] for t in factory('button_button')]==['/skin/button[1]'],'button unexpectedly dispatched nested XML')
    require(any(t['source_path']=='/skin/panel[1]/panel[1]/button[1]' for t in factory('panel_panel')),'recursive panel factory route missing')
    require(any(t['source_path']=='/skin/stack[1]/item[1]/button[1]' for t in factory('stack_item')),'stack item route missing')
    require(any(t['source_path']=='/skin/rack[1]/unit[1]/panel[1]/button[1]' and t['caller'].startswith('ISkinResizePanel::') for t in factory('rack_unit_panel')),'rack route missing')
    require(any(t['source_path']=='/skin/split[1]/left[1]/content[1]/button[1]' and t['caller'].startswith('ISkinResizePanel::') for t in factory('split_left_content')),'split content route missing')
    selection=next(t for t in calls('button_text_repeat') if t['symbol'].startswith('CXMLNode::getChild') and t.get('key')=='text' and t['source_path']=='/skin/button[1]')
    result=next(t for t in traces['button_text_repeat']['trace'] if t['event']=='return' and t['call_id']==selection['call_id'])
    require(result['source_path']=='/skin/button[1]/text[1]','duplicate text selection changed')
    # A configuration node is consumed by a reader even though generic dispatch returns null.
    panel_calls=calls('panel_panel')
    require(trees['panel_panel']['children'][1]['current_rect']==[10,20,280,160],'panel configuration geometry changed')
    size_call=next(t for t in factory('panel_panel') if t['source_path']=='/skin/panel[1]/size[1]')
    require(any(t['event']=='return' and t['call_id']==size_call['call_id'] and not t['present'] for t in traces['panel_panel']['trace']),'size factory control changed')
    require(json.loads(ARTIFACT.read_text())==generate(),'partial manifest stale')
    return {'build':'18.0.9246','parent_child_matrix':'verified','source_path_traces':'verified','manifest':'partial, open coverage; not an exhaustive allowed-child schema'}


if __name__=='__main__':print(json.dumps(check(),indent=2))
