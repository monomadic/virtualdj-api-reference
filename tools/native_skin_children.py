#!/usr/bin/env python3
"""Query or regenerate a partial, evidence-linked native skin relationship manifest."""
import argparse
import json
import xml.etree.ElementTree as ET
import offline_parser as base

ARTIFACT=base.ROOT/'tests/skin-container-manifest-9246.json'
INPUTS=['skin-child-readers-9246.json','skin-child-relations-9246.json','skin-child-trace-9246.json','skin-child-layout-9246.json']
RULES=[
 ('skin','CSkinWindow','general factory','Authored children enter the panel loader; generated grab zones also appear.', ['skin_button','ordered_repeat']),
 ('panel','CSkinPanel','general factory','Retains nested objects; unknown wrappers do not flatten their contents.', ['panel_button','panel_panel','panel_text','panel_unknown']),
 ('group','CSkinPanel','conditional wrapper','Plain group flattens into the owning container; the visibility fixture constructs a panel.', ['group_button','group_visibility_button','group_nested']),
 ('deck','CSkinPanel','context wrapper','Flattens children into the current container while passing deck context.', ['deck_button']),
 ('setdeck','CSkinPanel','context wrapper','Flattens children into the current container while passing deck context.', ['setdeck_button']),
 ('button','CSkinButton','named object slots','Text state slots construct CSkinText; repeated text selects the first. Nested buttons/panels and text hidden inside an unknown wrapper do not become children.', ['button_button','button_panel','button_text','button_text_repeat','button_text_states','button_unknown_text']),
 ('slider','CSkinSlider','named object slot','Fader constructs CSkinSliderFader; arbitrary button/text children do not become objects in these controls.', ['slider_button','slider_text','slider_fader']),
 ('textzone','CSkinText','leaf control','The nested marker button does not become an object.', ['textzone_button']),
 ('stack','CSkinStack','item wrapper','Each tested item creates a CSkinPanel that dispatches its children; direct button/panel controls do not.', ['stack_button','stack_panel','stack_item','stack_item_repeat']),
 ('rack','CSkinRack','unit/panel wrapper','A unit/panel creates CSkinResizePanel, which dispatches its contents. Direct buttons/panels and a unit/button control do not.', ['rack_button','rack_panel','rack_unit_button','rack_unit_panel']),
 ('split','CSkinSplit','named side wrappers','Default split constructs left/right ISkinResizePanel objects. Side content is dispatched, directly or through content; root-level button/content/panel controls do not populate the sides.', ['split_button','split_content','split_panel','split_left_right','split_left_content']),
 ('resizepanel','CSkinResizePanel','content dispatcher','Dispatches direct children or children inside content in the tested inputs.', ['resizepanel_button','resizepanel_content']),
 ('zzunknown',None,'unknown wrapper control','The unknown wrapper and its marker button are absent from the native tree.', ['unknown_button']),
]


def xml_paths(root, path='/skin'):
    result=[path];counts={}
    for child in root:
        counts[child.tag]=counts.get(child.tag,0)+1
        result+=xml_paths(child,path+'/'+child.tag+'['+str(counts[child.tag])+']')
    return result


def object_paths(node, path=''):
    path=path+'/'+node['class'];result=[path]
    for i,child in enumerate(node['children']):result+=object_paths(child,path+'['+str(i)+']')
    return result


def generate():
    evidence={name:json.loads((base.ROOT/'tests'/name).read_text()) for name in INPUTS}
    static=evidence[INPUTS[0]];runs={r['name']:r for r in evidence[INPUTS[1]]['runs']};traces={r['name']:r for r in evidence[INPUTS[2]]['runs']}
    if not evidence[INPUTS[1]]['all_cases_completed'] or not evidence[INPUTS[2]]['suite_finished'] or not all(r['completed'] for r in traces.values()):raise ValueError('incomplete evidence')
    records=[]
    for parent,cls,mechanism,finding,cases in RULES:
        rec=dict(parent=parent,native_reader_class=cls,mechanism=mechanism,finding=finding,closed_world=False,cases=[])
        for name in cases:
            row=runs[name]
            tree=next(e['tree'] for e in row['events'] if e.get('stage')=='loaded')
            rec['cases'].append(dict(name=name,xml=row['xml'],xml_paths=xml_paths(ET.fromstring(row['xml'])),native_class_paths=object_paths(tree),capture=INPUTS[1],trace_capture=INPUTS[2] if name in traces else None))
        rec['static_named_child_leads']=[r for r in static['named_child_reads']+static['named_child_helper_calls'] if cls and r['caller'].startswith(cls+'::')]
        rec['static_dispatch_sites']=[r for r in static['dispatch_calls'] if cls and (r['caller'] or '').startswith(cls+'::')]
        records.append(rec)
    return dict(schema_version=1,source=static['source'],scope='Partial contextual relationships observed in an isolated native host; not a complete allowed-child schema or live-app parity.',evidence_sha256={name:base.digest((base.ROOT/'tests'/name).read_bytes()) for name in INPUTS},relationships=records,limitations=['Do not reject unlisted child names: coverage is open.', 'RTTI container inheritance is not XML child acceptance.', 'Configuration nodes such as pos and size may be consumed by a reader and also return null from factory dispatch.', 'The manifest records loaded trees; subsequent direct panel-move snapshots are experimental layout operations.', 'The unsized rack panel failed with nonfinite geometry; the confirmed case supplies explicit dimensions.', 'Rendering, script evaluation and conditions were not exercised; same-build live fixtures are required for Tier 1.'])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--generate',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--parent');a=p.parse_args()
    if a.generate:
        if ARTIFACT.exists():raise SystemExit('manifest exists; preserve the previous capture first')
        ARTIFACT.write_text(json.dumps(generate(),indent=2)+'\n')
    data=json.loads(ARTIFACT.read_text())
    if a.check:
        if data!=generate():raise SystemExit('native child manifest differs from evidence')
        print('native child manifest matches its source captures')
    elif a.parent:
        found=[r for r in data['relationships'] if r['parent']==a.parent]
        if not found:raise SystemExit('parent not covered; absence is not a rejection rule')
        print(json.dumps(dict(source=data['source'],scope=data['scope'],relationships=found),indent=2))
    else:
        print(json.dumps(dict(source=data['source'],scope=data['scope'],parents=[dict(parent=r['parent'],mechanism=r['mechanism'],finding=r['finding']) for r in data['relationships']]),indent=2))
