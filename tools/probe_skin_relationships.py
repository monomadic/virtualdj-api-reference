#!/usr/bin/env python3
"""Paired XML parent/child probes in the isolated symbol-rich 9246 host."""
import argparse
import json
from pathlib import Path
import offline_parser as base
import probe_skin_composition as composition
import probe_skin_host

MARKER = '<button><pos x="101" y="103"/><size width="17" height="19"/></button>'
GEOMETRY = '<pos x="10" y="20"/><size width="280" height="160"/>'
PARENTS = [('skin', '', ''), ('panel', '<panel name="p">'+GEOMETRY, '</panel>'), ('button', '<button>'+GEOMETRY, '</button>'), ('slider', '<slider>'+GEOMETRY, '</slider>'), ('textzone', '<textzone>'+GEOMETRY, '</textzone>'), ('group', '<group x="10" y="20">', '</group>'), ('group_visibility', '<group visibility="true" x="10" y="20">', '</group>'), ('deck', '<deck deck="2">', '</deck>'), ('setdeck', '<setdeck deck="2">', '</setdeck>'), ('split', '<split>'+GEOMETRY, '</split>'), ('rack', '<rack>'+GEOMETRY, '</rack>'), ('stack', '<stack>'+GEOMETRY, '</stack>'), ('resizepanel', '<resizepanel>'+GEOMETRY, '</resizepanel>'), ('unknown', '<zzunknown>', '</zzunknown>')]


def fixtures():
    cases = [(name+'_button', start+MARKER+end) for name,start,end in PARENTS]
    cases += [
        ('panel_panel', '<panel name="outer">'+GEOMETRY+'<panel name="inner"><pos x="30" y="40"/><size width="100" height="80"/>'+MARKER+'</panel></panel>'),
        ('button_text', '<button>'+GEOMETRY+'<text text="literal child"/></button>'),
        ('panel_text', '<panel name="p">'+GEOMETRY+'<text text="literal child"/></panel>'),
        ('button_panel', '<button>'+GEOMETRY+'<panel name="p">'+MARKER+'</panel></button>'),
        ('button_unknown_text', '<button>'+GEOMETRY+'<zzunknown><text text="literal child"/></zzunknown></button>'),
        ('button_text_repeat', '<button>'+GEOMETRY+'<text text="first"/><text text="second"/></button>'),
        ('slider_text', '<slider>'+GEOMETRY+'<text text="literal child"/></slider>'),
        ('slider_fader', '<slider>'+GEOMETRY+'<fader><size width="12" height="14"/><up x="0" y="0"/></fader></slider>'),
        ('split_content', '<split>'+GEOMETRY+'<content>'+MARKER+'</content></split>'),
        ('split_panel', '<split>'+GEOMETRY+'<panel>'+MARKER+'</panel></split>'),
        ('stack_panel', '<stack>'+GEOMETRY+'<panel name="stacked">'+MARKER+'</panel></stack>'),
        ('rack_panel', '<rack>'+GEOMETRY+'<panel name="racked">'+MARKER+'</panel></rack>'),
        ('panel_unknown', '<panel name="p">'+GEOMETRY+'<zzunknown>'+MARKER+'</zzunknown></panel>'),
        ('group_nested', '<panel name="p">'+GEOMETRY+'<group x="+5" y="+6">'+MARKER+'</group></panel>'),
        ('ordered_repeat', MARKER+MARKER),
        ('stack_item', '<stack>'+GEOMETRY+'<item>'+MARKER+'</item></stack>'),
        ('stack_item_repeat', '<stack>'+GEOMETRY+'<item>'+MARKER+'</item><item>'+MARKER+'</item></stack>'),
        ('rack_unit_panel', '<rack>'+GEOMETRY+'<unit><panel>'+GEOMETRY+MARKER+'</panel></unit></rack>'),
        ('rack_unit_button', '<rack>'+GEOMETRY+'<unit>'+MARKER+'</unit></rack>'),
        ('split_left_right', '<split>'+GEOMETRY+'<left>'+MARKER+'</left><right>'+MARKER+'</right></split>'),
        ('split_left_content', '<split>'+GEOMETRY+'<left><content>'+MARKER+'</content></left></split>'),
        ('resizepanel_content', '<resizepanel>'+GEOMETRY+'<content>'+MARKER+'</content></resizepanel>'),
        ('button_text_states', '<button>'+GEOMETRY+'<text text="normal"/><textdown text="down"/><textover text="over"/><textselected text="selected"/></button>'),
    ]
    return [(name,'<skin name="Child relationships" version="8" width="320" height="200">'+xml+'</skin>') for name,xml in cases]


def prepare(app, work):
    probe_skin_host.prepare(app, work)
    evidence = json.loads((base.ROOT/'tests/skin-child-readers-9246.json').read_text())
    extra = []
    known = {'CSkinWindow','CSkinPanel','CSkinButton','CSkinGrabZone'}
    # Only primary ISkinObject chains have the reviewed base fields at offset zero.
    def primary(name, target):
        if name == target:return True
        parents=evidence['classes'].get(name,{}).get('bases',[])
        return bool(parents) and primary(parents[0],target)
    for name,record in evidence['classes'].items():
        if name not in known and record['vtable'] and primary(name,'ISkinObject'):
            extra.append(dict(name=name,address=record['vtable'],container=primary(name,'ISkinContainer')))
    prefixes=tuple(name+'::'+name+'(' for name in evidence['classes'])
    composition.finish_prepare(work, fixtures(), extra, prefixes, base.ROOT/'tools/plugin/offline_relationship_host.cpp')
    prep=json.loads((work/'preparation.json').read_text())
    prep['composition_base_source_sha256']=base.digest((base.ROOT/'tools/plugin/offline_composition_host.cpp').read_bytes())
    prep['relationship_source_sha256']=base.digest((base.ROOT/'tests/skin-child-readers-9246.json').read_bytes())
    (work/'preparation.json').write_text(json.dumps(prep,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['prepare','run','show'])
    p.add_argument('--app',type=Path)
    p.add_argument('--work',type=Path)
    p.add_argument('--output',type=Path)
    p.add_argument('--case',default='panel_panel',choices=[n for n,_ in fixtures()])
    p.add_argument('--capture',type=Path,default=base.ROOT/'tests/skin-child-relations-9246.json')
    a=p.parse_args()
    if a.mode=='show':composition.show(a.case,'loaded',a.capture)
    elif a.mode=='prepare':prepare(a.app.resolve(),a.work.resolve())
    else:composition.run(a.work.resolve(),a.output.resolve(),fixtures())
