#!/usr/bin/env python3
"""Breadth-first skin structure inventory with shared reader definitions (Tier 2)."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'tests/skin-structure-9246.json'
RELATIONS = ROOT / 'tests/skin-xml-relations.json'
MAX_UNITS = 3000
# Calls that consume a node without reading it as skin syntax. CXMLNode's own
# mutators are not readers; its copy constructor and assignment are, since a copy
# can be read later, and stay open routes.
NOT_A_READER = ('CXMLNode::~CXMLNode', 'operator delete', 'CXMLNode::deleteParam', 'CXMLNode::setParam',
                'CXMLNode::addParam', 'CXMLNode::addChild', 'CXMLNode::deleteChild', 'CXMLNode::setParamBool')


def node_parameter_registers(symbol):
    """Registers that can carry a CXMLNode argument: param i is x_i (static) or x_{i+1} (member)."""
    if not symbol or '(' not in symbol:
        return None  # unnamed or indirect: unknown, so every register stays a candidate
    inner = symbol[symbol.find('(') + 1:symbol.rfind(')')]
    depth, cur, params = 0, '', []
    for ch in inner:
        depth += 1 if ch in '<(' else -1 if ch in '>)' else 0
        if ch == ',' and depth == 0:
            params.append(cur.strip()); cur = ''
        else:
            cur += ch
    params.append(cur.strip())
    return {f'x{i + d}' for i, t in enumerate(params) if t.startswith(('CXMLNode', 'CXMLNodeT')) for d in (0, 1)}


def immediate_default(code, k, symbol):
    """The immediate a getter receives as its default (w3), if set just before the call."""
    if not re.search(r'getIntParam\(.*, int\)|getBoolParam|getIntParamFast|getSignedParamApply', symbol):
        return None
    for ins in reversed(code[max(0, k - 10):k]):
        if ins.mnemonic in ('bl', 'blr', 'b', 'ret') or ins.mnemonic.startswith('b.'):
            return None
        ops = ins.operands
        if ops and ops[0].type == 1 and ins.reg_name(ops[0].reg) in ('w3', 'x3'):
            if ins.mnemonic in ('mov', 'movz') and len(ops) == 2 and ops[1].type == 2:
                return ops[1].imm
            return None
    return None


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
    def unit(fn, register='x1', name_register=None, expand=False):
        key = f'{hex(fn)}:{register}' + (f':name={name_register}' if name_register else '') + (':follow' if expand else '')
        if key in units: return key
        code = decoded(a,fn)
        raw = b''.join(w.to_bytes(4,'little') for _,w in a.words(fn))
        if sum(i.size for i in code)!=len(raw): raise ValueError('incomplete decoding')
        reads, calls = [], []
        initial={register:frozenset({('node','$node')})}
        if name_register:initial[name_register]=frozenset({('parameter',name_register)})
        if expand:
            # Followed helpers may take the attribute name as an argument (getColorParam).
            for n in range(1,8):
                initial.setdefault(f'x{n}',frozenset({('parameter',f'x{n}')}))
        index={i.address:k for k,i in enumerate(code)}
        found,states=analyze(code,initial,getters,a.img.strings,conditional_select=True,return_states=True)
        # Loads of a known node's child vector (offset 0x30/0x38): children reached by
        # iteration, not by name, which no read below can attribute.
        iterations=[]
        for pc,(ins,state) in sorted(states.items()):
            if not ins.mnemonic.startswith('ld'):continue
            for op in ins.operands:
                if op.type==3 and op.mem.base and op.mem.disp in (0x30,0x38):
                    paths=node_paths(state.get(ins.reg_name(op.mem.base),UNKNOWN))
                    if paths:iterations.append({'pc':hex(pc),'node_paths':paths})
        for ins,target,state in found:
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
                    default=immediate_default(code,index[ins.address],symbols.get(target,''))
                    if default is not None:reads[-1]['default']=default
                continue
            arguments={r:{'paths':node_paths(v),'unresolved':any(k!='node' for k,_ in v)} for r,v in state.items()
                       if r in {'x'+str(n) for n in range(8)} and node_paths(v)}
            if arguments:
                names={r:sorted({a.img.strings[v] for k,v in state.get(r,UNKNOWN) if k=='constant' and v in a.img.strings})
                       for r in (f'x{n}' for n in range(8)) if r not in arguments}
                params={r:sorted({v for k,v in state.get(r,UNKNOWN) if k=='parameter'})
                        for r in (f'x{n}' for n in range(8)) if r not in arguments}
                calls.append({'pc':hex(ins.address),'target':hex(target) if target else None,
                              'string_arguments':{r:v for r,v in names.items() if v},
                              'parameter_arguments':{r:v for r,v in params.items() if v},
                              'symbol':symbols.get(target),'node_arguments':arguments,
                              'shared_reader_ref':f'{hex(base)}:x1' if target==base else (f'{hex(text_helper)}:x2:name=x1' if target==text_helper else None),
                              'shared_node_register':'x2' if target==text_helper else 'x1',
                              'name_bindings':{'x1':sorted({a.img.strings[v] for k,v in state.get('x1',UNKNOWN) if k=='constant' and v in a.img.strings})} if target==text_helper else {},
                              'binding_name_unresolved':any(k!='constant' or v not in a.img.strings for k,v in state.get('x1',UNKNOWN)) if target==text_helper else False})
        units[key]={'function':hex(fn),'symbol':symbols.get(fn),'node_register':register,
                    'sha256':hashlib.sha256(raw).hexdigest(),'reads':reads,'calls':calls,
                    'child_iterations':iterations}
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
            initializer=None
            if c['class']=='CSkinWindow' and not bound:
                # The window is default-constructed; the factory then passes the node to
                # CSkinWindow::load(window, node, image, nullptr). Bind that call instead.
                loads=[f for f,n in symbols.items() if n=='CSkinWindow::load(CXMLNode*, CImage*, char const*)']
                calls=[(p,st) for p,(t,st) in states.items() if loads and t==loads[0]]
                if len(loads)==1 and len(calls)==1 and calls[0][1].get('x1',UNKNOWN)==frozenset({('node','$node')}):
                    bound,fn,initializer=True,loads[0],{'symbol':symbols[loads[0]],'callsite':hex(calls[0][0])}
            entry['variants'].append({'class':c['class'],'factory_callsite':hex(pc),
                                      **({'initializer':initializer} if initializer else {}),
                                      'factory_binding_verified':bound,'dispatch_exhausted':d['traversal_exhausted'],
                                      'xml_register':xml_register,
                                      'binding_gap':None if bound else 'Constructor XML argument not established; initialization helpers remain untraced.',
                                      'reader_ref':unit(fn,xml_register) if bound else None})
    # Contexts a reviewed dispatch rule names but no factory branch reaches: the child is
    # found by iterating the parent's children, so the rule's cited call is the binding.
    dispatch_path=ROOT/'tests/skin-dispatch-9246.json'
    if dispatch_path.exists():
        dispatch=json.loads(dispatch_path.read_text())
        for loader,row in dispatch['dispatch']['loaders'].items():
            parent=re.split(r'[ ,(]',row['used_by'],1)[0]
            for rule in row['rules']:
                if not rule.get('call') or rule.get('literal'):continue
                pc=int(rule['pc'],16)
                insn=next((i for i in decoded(a,a.owner(pc)) if i.address==pc),None)
                target=insn.operands[0].imm if insn is not None and insn.mnemonic=='bl' else None
                name=symbols.get(target,'')
                if not name.startswith(rule['call']+'(') or not name.split('(',1)[1].startswith('CXMLNode*'):continue
                for child in rule['names']:
                    if child=='*':continue  # the factory fallback, not a context
                    tag=child if child.startswith('(') else f'{parent}/{child}'
                    elements.setdefault(tag,{'kind':'context_element','variants':[],'status':'partial_structure'})
                    elements[tag]['variants'].append({'class':None,'binding':{'symbol':name,'callsite':rule['pc'],'dispatch_loader':loader},
                                                      'factory_binding_verified':False,'xml_register':'x1',
                                                      'binding_gap':None,'reader_ref':unit(target,'x1')})
    # Follow every node-carrying call into a function that takes a CXMLNode, so a
    # helper's reads count for the caller's path. Getters, CXMLNode members and the
    # two shared readers already modelled are not re-entered.
    followed=set()
    while True:
        pending=[(key,c) for key,u in list(units.items()) for c in u['calls'] if (key,c['pc']) not in followed]
        if not pending:break
        for key,c in pending:
            followed.add((key,c['pc']))
            target=int(c['target'],16) if c['target'] else None
            name=symbols.get(target,'')
            refs={}
            allowed=node_parameter_registers(name)
            for r,arg in c['node_arguments'].items():
                if c['shared_reader_ref'] and r==c['shared_node_register']:refs[r]=c['shared_reader_ref'];continue
                if allowed is not None and r not in allowed:continue
                if (target is None or target in getters or name.startswith('CXMLNode::') or 'CXMLNode' not in name
                        or target not in a.starts or len(units)>=MAX_UNITS):continue
                try:refs[r]=unit(target,r,expand=True)
                except ValueError:continue
            if refs:c['callee_refs']=refs
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
            'anchors':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [memory,audit_path,node_path,RELATIONS,ROOT/'tests/skin-dispatch-9246.json']},
            'limitations':['Structural reads only; no runtime behavior or completeness promotion.',
                           'Factory constructors and every function they pass a node to (when its signature takes a CXMLNode) are analyzed; attribute names passed as arguments are bound from the call site. Indirect calls, and calls whose node argument is only partly resolved, are listed per element as open routes.',
                           'Child XML nodes are freed once the panel loader has processed them, so reads after construction can only reach a node that was copied; copies are open routes.',
                           'A reused reader definition does not imply identical caller defaults, state, precedence or execution timing.',
                           'Own attributes and direct children are query projections on $node; descendant reads stay in reader definitions.',
                           'Observed parents come from literal vendor nesting, not accepted-parent closure.',
                           'Unresolved factory branches, names, receivers, helpers, templates and lifecycle routes remain open.',
                           'Conditional selections retain alternatives; branch feasibility, heap/stack aliases and inline XML accesses are not solved.']}


# Class expansion walks children to merge them (docs/Skin Expansion.md, fixtures in
# tests/skin-expansion-9246.json); that walk is a reviewed rule, not unnamed syntax.
EXPANSION_FUNCTIONS = ('CSkinClass::apply', 'CSkinClass::applyXml', 'CSkinClass::applyPlaceholders')


def reviewed_loaders():
    """Functions whose child iteration a reviewed rule explains: dispatch loaders and class expansion."""
    path = ROOT / 'tests/skin-dispatch-9246.json'
    loaders = tuple(json.loads(path.read_text())['dispatch']['loaders']) if path.exists() else ()
    return loaders + EXPANSION_FUNCTIONS


def describe(data, tag):
    entry=data['elements'][tag]
    attrs,partial,children=set(),set(),set()
    slots={}            # direct child name -> attribute names read on it
    readings={}         # own attribute -> sorted getter roles and defaults
    open_routes=[]
    refs=set(); visited=set(); pending=[]
    for v in entry['variants']:
        if v['reader_ref']:pending.append((v['reader_ref'],{},'$node'))
    def rebase(path,prefix):
        return prefix+path[len('$node'):] if path.startswith('$node') else None
    while pending:
        ref,binding,prefix=pending.pop()
        context=(ref,json.dumps(binding,sort_keys=True),prefix)
        if context in visited or len(visited)>5000:continue
        visited.add(context);refs.add(ref);reader=data['readers'][ref]
        for r in reader['reads']:
            names=set(r['names'])
            for param in r['name_parameters']:names.update(binding.get(param,[]))
            for path in filter(None,(rebase(p,prefix) for p in r['node_paths'])):
                if r['role'] in ('child_node','conditional_child_node'):
                    if path=='$node':children.update(names)
                    continue
                if path=='$node':
                    (partial if r['receiver_unresolved'] or r['name_unresolved'] else attrs).update(names)
                    for n in names:
                        row=readings.setdefault(n,{'roles':set(),'defaults':set()})
                        row['roles'].add(r['role'])
                        if 'default' in r:row['defaults'].add(r['default'])
                elif path.count('/')==1:
                    slots.setdefault(path.split('/',1)[1],set()).update(names)
        for it in reader.get('child_iterations',[]):
            mapped=[m for m in (rebase(p,prefix) for p in it['node_paths']) if m]
            if not mapped:continue
            covered=next((k for k in reviewed_loaders() if (reader['symbol'] or '').startswith(k+'(')),None)
            if covered:continue
            open_routes.append({'pc':it['pc'],'symbol':reader['symbol'],'register':None,'paths':mapped,
                                'reason':'children iterated without names'})
        for c in reader['calls']:
            callee=c.get('callee_refs') or ({c['shared_node_register']:c['shared_reader_ref']} if c['shared_reader_ref'] else {})
            if c['shared_reader_ref'] and not c.get('callee_refs') and c['binding_name_unresolved']:callee={}
            allowed=node_parameter_registers(c['symbol'])
            for reg,arg in c['node_arguments'].items():
                mapped=[m for m in (rebase(p,prefix) for p in arg['paths']) if m]
                if not mapped or (allowed is not None and reg not in allowed and reg not in callee):continue
                if reg not in callee:
                    # A named target with no symbol is an imported library stub on this
                    # unstripped build (allocation, copies, stack checks), not a skin reader.
                    if c['target'] and not c['symbol']:continue
                    if not (c['symbol'] or '').startswith(NOT_A_READER):
                        open_routes.append({'pc':c['pc'],'symbol':c['symbol'],'register':reg,'paths':mapped,
                                            'reason':'call not followed' if c['symbol'] else 'indirect or unnamed call'})
                    continue
                inner={}
                for r_,vals in c.get('string_arguments',{}).items():inner[r_]=vals
                for r_,ps in c.get('parameter_arguments',{}).items():
                    inner[r_]=sorted({n for q in ps for n in binding.get(q,[])})
                if c['shared_reader_ref'] and not c.get('callee_refs'):inner=c['name_bindings']
                for m in mapped:pending.append((callee[reg],inner,m))
                if arg.get('unresolved'):
                    open_routes.append({'pc':c['pc'],'symbol':c['symbol'],'register':reg,'paths':mapped,
                                        'reason':'node argument only partly resolved'})
    merged={}
    for r in open_routes:
        row=merged.setdefault((r['pc'],r['register'],r['reason']),{**r,'paths':set()})
        row['paths'].update(r['paths'])
    routes=[{**r,'paths':sorted(r['paths'])} for _,r in sorted(merged.items())]
    closure={'structurally_closed':(not routes and not partial) if refs else None,'open_routes':routes}
    if not refs:
        closure['note']='No reader binds this name; it is a directive or a child identity (see just skin-dispatch).'
    relations=json.loads(RELATIONS.read_text())
    parents=sorted({e['parent'] for e in relations['relationships'] if e['child']==tag and e['family'] in ('skins','video_skins')})
    observed_children=sorted({e['child'] for e in relations['relationships'] if e['parent']==tag and e['family'] in ('skins','video_skins')})
    return {'element':tag,**entry,'own_attribute_candidates':sorted(attrs),'partial_attribute_candidates':sorted(partial),
            'attribute_readings':{n:{'roles':sorted(v['roles']),'defaults':sorted(v['defaults'])} for n,v in sorted(readings.items())},
            'direct_child_candidates':sorted(children),
            'child_slot_attributes':{k:sorted(v) for k,v in sorted(slots.items()) if v},
            'closure':closure,
            'reader_refs':sorted(refs),'observed_vendor_parents':parents,
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
        rows={}
        for k,v in data['elements'].items():
            row={'kind':v['kind'],'status':v['status'],'reader_refs':sorted({r['reader_ref'] for r in v['variants'] if r['reader_ref']})}
            if row['reader_refs']:
                c=describe(data,k)['closure'];row['structurally_closed']=c['structurally_closed'];row['open_routes']=len(c['open_routes'])
            rows[k]=row
        print(json.dumps({'source':data['source'],'elements':rows,'limitations':data['limitations']},indent=2))
