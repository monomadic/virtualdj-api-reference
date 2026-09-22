#!/usr/bin/env python3
"""Breadth-first skin structure inventory with shared reader definitions (Tier 2)."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'tests/skin-structure-9246.json'
RELATIONS = ROOT / 'tests/skin-xml-relations.json'


def extract(app):
    from extract_skin_classes import Analysis, decoded, generate
    from extract_action_vtables import demangled, symbol_maps
    from skin_schema import analyze, node_paths, UNKNOWN
    from skin_node_helpers import models
    from skin_reader_audit import reader_models
    from plugin_memory import verify
    memory = ROOT / 'tests/plugin-memory-9246.json'
    verified = verify(json.loads(memory.read_text()), app / 'Contents/MacOS/VirtualDJ')
    audit_path = ROOT / 'tests/skin-reader-audit-9246.json'
    audit = json.loads(audit_path.read_text())
    source = generate(app)
    a = Analysis(app)
    binary_hash = hashlib.sha256(a.img.data).hexdigest()
    if binary_hash != verified['binary_sha256'] or source['source']['binary_sha256'] != binary_hash:
        raise ValueError('binary identity changed')
    symbols, _ = symbol_maps(demangled(app / 'Contents/MacOS/VirtualDJ', 'arm64'))
    getters = {int(k,16): v for k,v in source['xml_reader_anchors'].items()}
    named = reader_models(audit, binary_hash, lambda fn: b''.join(w.to_bytes(4,'little') for _,w in a.words(fn)))
    for fn, row in named.items(): getters.setdefault(fn,row)
    node_path = ROOT / 'tests/skin-node-helpers-9246.json'
    node_models, _ = models(a, node_path)
    getters.update(node_models)
    # The independently reviewed getParam2 call convention has two string_view
    # keys, in x1/x2 and x3/x4. Keep both, without claiming runtime precedence.
    for fn, row in getters.items():
        if symbols.get(fn,'').startswith('CXMLNode::getParam2('): row['extra_name_registers']=['x3']
    base = {a.owner(int(g['call_pc'],16)) for g in getters.values() if g.get('anchor')=='clickthrough'}
    if len(base)!=1: raise ValueError('shared base ambiguous')
    base = base.pop()
    text_helpers = [fn for fn,name in symbols.items() if name == 'CSkinButton::addTextObject(char const*, CXMLNode*, CImage*)']
    if len(text_helpers)!=1: raise ValueError('text-child helper ambiguous')
    text_helper=text_helpers[0]
    units = {}
    def unit(fn, register='x1', name_register=None):
        key = f'{hex(fn)}:{register}' + (f':name={name_register}' if name_register else '')
        if key in units: return key
        code = decoded(a,fn)
        raw = b''.join(w.to_bytes(4,'little') for _,w in a.words(fn))
        if sum(i.size for i in code)!=len(raw): raise ValueError('incomplete decoding')
        reads, calls = [], []
        initial={register:frozenset({('node','$node')})}
        if name_register:initial[name_register]=frozenset({('parameter',name_register)})
        for ins,target,state in analyze(code,initial,getters,a.img.strings,conditional_select=True):
            model=getters.get(target)
            if model:
                if model['role']=='matching_sibling_node': continue
                receiver=state.get(model.get('node_register','x0'),UNKNOWN)
                name_registers=[model.get('name_register','x1')]+model.get('extra_name_registers',[])
                for nr in name_registers:
                    values=state.get(nr,UNKNOWN)
                    reads.append({'pc':hex(ins.address),'getter':hex(target),'role':model['role'],
                                  'key_register':nr,'node_paths':node_paths(receiver),
                                  'name_parameters':sorted({v for k,v in values if k=='parameter'}),
                                  'names':sorted({a.img.strings[v] for k,v in values if k=='constant' and v in a.img.strings}),
                                  'receiver_unresolved':any(k!='node' for k,v in receiver),
                                  'name_unresolved':any(k not in ('constant','parameter') or (k=='constant' and v not in a.img.strings) for k,v in values)})
                continue
            arguments={r:{'paths':node_paths(v),'unresolved':any(k!='node' for k,_ in v)} for r,v in state.items()
                       if r in {'x'+str(n) for n in range(8)} and node_paths(v)}
            if arguments:
                calls.append({'pc':hex(ins.address),'target':hex(target) if target else None,
                              'symbol':symbols.get(target),'node_arguments':arguments,
                              'shared_reader_ref':f'{hex(base)}:x1' if target==base else (f'{hex(text_helper)}:x2:name=x1' if target==text_helper else None),
                              'shared_node_register':'x2' if target==text_helper else 'x1',
                              'name_bindings':{'x1':sorted({a.img.strings[v] for k,v in state.get('x1',UNKNOWN) if k=='constant' and v in a.img.strings})} if target==text_helper else {},
                              'binding_name_unresolved':any(k!='constant' or v not in a.img.strings for k,v in state.get('x1',UNKNOWN)) if target==text_helper else False})
        units[key]={'function':hex(fn),'symbol':symbols.get(fn),'node_register':register,
                    'sha256':hashlib.sha256(raw).hexdigest(),'reads':reads,'calls':calls}
        return key
    unit(base)
    unit(text_helper,'x2','x1')
    factory=int(source['factory']['function'],16)
    states={i.address:(target,state) for i,target,state in analyze(decoded(a,factory),{'x0':frozenset({('node','$node')})},getters,a.img.strings,conditional_select=True)}
    elements={}
    for d in source['factory']['dispatch']:
        tag=d['element']
        entry=elements.setdefault(tag,{'kind':'factory_element','variants':[],'status':'partial_structure'})
        for c in d['constructors']:
            fn=int(c['constructor'],16);pc=int(c['call_pc'],16)
            target,state=states.get(pc,(None,{}))
            xml_register='x2' if symbols.get(fn)=='CSkinEdit::CSkinEdit(CSkinWindow*, CXMLNode*, bool)' else 'x1'
            receiver=state.get(xml_register,UNKNOWN)
            bound=receiver==frozenset({('node','$node')})
            if target!=fn:
                thunk=decoded(a,target) if target in a.starts else []
                bound=bound and len(thunk)==1 and thunk[0].mnemonic=='b' and thunk[0].operands[0].imm==fn
            entry['variants'].append({'class':c['class'],'factory_callsite':hex(pc),
                                      'factory_binding_verified':bound,'dispatch_exhausted':d['traversal_exhausted'],
                                      'xml_register':xml_register,
                                      'binding_gap':None if bound else 'Constructor XML argument not established; initialization helpers remain untraced.',
                                      'reader_ref':unit(fn,xml_register) if bound else None})
    # Nested identities get their own entry; this does not imply factory creation.
    for definition in units.values():
        for read in definition['reads']:
            if read['role'] in ('child_node','conditional_child_node'):
                for tag in read['names']: elements.setdefault(tag,{'kind':'reader_child_identity','variants':[],'status':'identity_only'})
        for call in definition['calls']:
            if call['target']==hex(text_helper) and not call['binding_name_unresolved']:
                for tag in call['name_bindings'].get('x1',[]):
                    elements.setdefault(tag,{'kind':'reader_child_identity','variants':[],'status':'identity_only'})
    relations=json.loads(RELATIONS.read_text())
    for edge in relations['relationships']:
        if edge['family'] not in ('skins','video_skins'):continue
        for tag in (edge['parent'],edge['child']):
            elements.setdefault(tag,{'kind':'observed_xml_identity','variants':[],'status':'observed_only'})
    return {'schema_version':1,'source':source['source'],'elements':dict(sorted(elements.items())),
            'readers':units,'getters':{hex(k):v for k,v in getters.items()},
            'factory':{'function':hex(factory),'dispatch':source['factory']['dispatch']},
            'anchors':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [memory,audit_path,node_path,RELATIONS]},
            'limitations':['Structural reads only; no runtime behavior or completeness promotion.',
                           'Factory constructors, the shared base reader and the parameterized button text-child helper are analyzed; other calls are retained without recursive expansion.',
                           'A reused reader definition does not imply identical caller defaults, state, precedence or execution timing.',
                           'Own attributes and direct children are query projections on $node; descendant reads stay in reader definitions.',
                           'Observed parents come from literal vendor nesting, not accepted-parent closure.',
                           'Unresolved factory branches, names, receivers, helpers, templates and lifecycle routes remain open.',
                           'Conditional selections retain alternatives; branch feasibility, heap/stack aliases and inline XML accesses are not solved.']}


def describe(data, tag):
    entry=data['elements'][tag]
    attrs,partial,children=set(),set(),set()
    refs=set(); visited=set(); pending=[]
    for v in entry['variants']:
        if v['reader_ref']:pending.append((v['reader_ref'],{}))
    while pending:
        ref,binding=pending.pop()
        context=(ref,json.dumps(binding,sort_keys=True))
        if context in visited:continue
        visited.add(context);refs.add(ref);reader=data['readers'][ref]
        for r in reader['reads']:
            if '$node' not in r['node_paths']:continue
            names=set(r['names'])
            for param in r['name_parameters']:names.update(binding.get(param,[]))
            if r['role'] in ('child_node','conditional_child_node'):
                children.update(names)
            else:
                (partial if r['receiver_unresolved'] or r['name_unresolved'] else attrs).update(names)
        for c in reader['calls']:
            arg=c['node_arguments'].get(c['shared_node_register'],{})
            if c['shared_reader_ref'] and arg.get('paths')==['$node'] and not arg.get('unresolved') and not c['binding_name_unresolved']:
                pending.append((c['shared_reader_ref'],c['name_bindings']))
    relations=json.loads(RELATIONS.read_text())
    parents=sorted({e['parent'] for e in relations['relationships'] if e['child']==tag and e['family'] in ('skins','video_skins')})
    observed_children=sorted({e['child'] for e in relations['relationships'] if e['parent']==tag and e['family'] in ('skins','video_skins')})
    return {'element':tag,**entry,'own_attribute_candidates':sorted(attrs),'partial_attribute_candidates':sorted(partial),
            'direct_child_candidates':sorted(children),'reader_refs':sorted(refs),'observed_vendor_parents':parents,
            'observed_vendor_children':observed_children,
            'parent_source_matches_capture':hashlib.sha256(RELATIONS.read_bytes()).hexdigest()==data['anchors']['tests/skin-xml-relations.json'],
            'parent_evidence':'Observed vendor nesting only; does not establish accepted parent set.',
            'build':data['source']['build'],'limitations':data['limitations']}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('element',nargs='?')
    p.add_argument('--capture',type=Path,default=DEFAULT)
    p.add_argument('--app',type=Path)
    p.add_argument('--output',type=Path)
    p.add_argument('--check',action='store_true')
    args=p.parse_args()
    if (args.output or args.check) and not args.app:p.error('extraction/check requires --app')
    if args.output and args.output.exists():p.error('output already exists')
    data=extract(args.app) if args.app else json.loads(args.capture.read_text())
    if args.check and data!=json.loads(args.capture.read_text()):raise ValueError('structure inventory drift')
    if args.output:
        with args.output.open('x') as f:json.dump(data,f,indent=2);f.write('\n')
    if args.element:
        if args.element not in data['elements']:p.error('unknown element')
        print(json.dumps(describe(data,args.element),indent=2))
    else:
        print(json.dumps({'source':data['source'],'elements':{k:{'kind':v['kind'],'status':v['status'],'reader_refs':sorted({r['reader_ref'] for r in v['variants'] if r['reader_ref']})} for k,v in data['elements'].items()},'limitations':data['limitations']},indent=2))
