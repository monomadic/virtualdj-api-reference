#!/usr/bin/env python3
"""Structural skin discovery. Generation requires numpy; queries use only stdlib.
All names are Tier-2 leads, never functional confirmation.
"""
import functools
import argparse
import bisect
import hashlib
import json
import plistlib
import re
import struct
from pathlib import Path

ARTIFACT = Path('tests/skin-classes.json')
DEBUG = Path('tests/skin-classes-debug.json')


def function_starts(img):
    """LC_FUNCTION_STARTS gives real boundaries, including code after early RETs."""
    p = img.base + 32
    for _ in range(struct.unpack_from('<I', img.data, img.base + 16)[0]):
        cmd, size = struct.unpack_from('<II', img.data, p)
        if cmd == 0x26:
            off, length = struct.unpack_from('<II', img.data, p + 8)
            raw = img.data[img.base + off:img.base + off + length]
            address, value, shift, out = 0x100000000, 0, 0, []
            for b in raw:
                value |= (b & 127) << shift
                if b & 128:
                    shift += 7
                else:
                    if not value:
                        break
                    address += value
                    out.append(address)
                    value, shift = 0, 0
            return out
        p += size
    raise ValueError('LC_FUNCTION_STARTS missing')


class Analysis:
    def __init__(self, app):
        from extract_binary_vocabularies import Image
        self.img = Image(app)
        self.starts = function_starts(self.img)
        self.ends = self.starts[1:] + [self.img.text[2] + self.img.text[3]]
        self.refs = {}
        for vm, pcs in self.img.xrefs.items():
            for pc in pcs:
                fn = self.owner(pc)
                self.refs.setdefault(fn, []).append((pc, self.img.strings[vm]))
        self.symbols = {}

    def owner(self, pc):
        i = bisect.bisect_right(self.starts, pc) - 1
        return self.starts[i] if i >= 0 else None

    @functools.lru_cache(maxsize=None)
    def words(self, fn):
        i = bisect.bisect_left(self.starts, fn)
        if i == len(self.starts) or self.starts[i] != fn:
            return []
        off = self.img.base + self.img.text[4] + fn - self.img.text[2]
        return [(fn + k, struct.unpack_from('<I', self.img.data, off + k)[0])
                for k in range(0, self.ends[i] - fn, 4)]

    @functools.lru_cache(maxsize=None)
    def calls(self, fn):
        out = []
        for pc, w in self.words(fn):
            if w & 0xfc000000 == 0x94000000:
                v = w & 0x3ffffff
                if v & 0x2000000:
                    v -= 0x4000000
                out.append((pc, pc + v * 4))
        return out

    def fingerprint(self, fn):
        out = []
        for _, w in self.words(fn):
            if w & 0x7c000000 == 0x14000000: w &= 0xfc000000
            elif w & 0x9f000000 == 0x90000000: w &= 0x9f00001f
            elif w & 0xff800000 == 0x91000000: w &= ~0x3ffc00
            out.append(w)
        return tuple(out)


def inspect(app, historical):
    from extract_action_contracts import rtti_graph
    from extract_action_vtables import demangled, symbol_maps
    cur, old = Analysis(app), Analysis(historical)
    old.symbols, _ = symbol_maps(demangled(historical / 'Contents/MacOS/VirtualDJ', 'arm64'))
    graph = rtti_graph(cur.img.data, ('CSkin', 'ISkinObject'))
    # Byte-shape matches are cross-build leads, retained only when unique.
    wanted = {fn: name for fn, name in old.symbols.items()
              if name.startswith(('CSkin', 'ISkinObject::', 'CXMLNode::')) and fn in old.starts}
    fingerprints = {}
    for fn, name in wanted.items():
        fp = old.fingerprint(fn)
        if len(fp) >= 8:
            fingerprints.setdefault(fp, []).append((fn, name))
    matches = {}
    for fn in cur.starts:
        fp = cur.fingerprint(fn)
        if fp in fingerprints:
            matches.setdefault(fp, []).append(fn)
    linked = {}
    for fp, targets in matches.items():
        if len(targets) == 1 and len(fingerprints[fp]) == 1:
            ofn, name = fingerprints[fp][0]
            linked[targets[0]] = {'name': name, 'historical_address': hex(ofn), 'method': 'unique normalized instruction fingerprint; cross-build lead'}
    debug = {'matches': {hex(k):v for k,v in linked.items()}, 'anchors': {}, 'graph': graph}
    for anchor in ['multibutton','resizepanel','keyboardmap','pannel','action2','action%d','action%i','action','clickthrough']:
        debug['anchors'][anchor] = [{'function':hex(fn),'references':[(hex(pc),s) for pc,s in cur.refs.get(fn,[])], 'calls':[(hex(pc),hex(t),linked.get(t,{}).get('name')) for pc,t in cur.calls(fn)]} for fn in sorted({cur.owner(pc) for vm in cur.img.by_text.get(anchor,[]) for pc in cur.img.xrefs.get(vm,[])})]
    DEBUG.write_text(json.dumps(debug,indent=2))
    return cur, old, graph, linked


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--app', type=Path, default=Path('/Applications/VirtualDJ.app'))
    p.add_argument('--historical-app', type=Path)
    p.add_argument('--get')
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    if args.historical_app:
        print(json.dumps(generate(args.app, args.historical_app), indent=2))
    else:
        data = json.loads(ARTIFACT.read_text())
        print(json.dumps(data['classes'][args.get] if args.get else data['summary'], indent=2))


# Decoder used only to regenerate; offline queries do not import capstone/numpy.
@functools.lru_cache(maxsize=None)
def decoded(a, fn):
    from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.detail = True
    words = a.words(fn)
    return list(md.disasm(b''.join(struct.pack('<I', w) for _, w in words), fn))


@functools.lru_cache(maxsize=None)
def literal_calls(a, fn):
    """Conservative straight-line register tracking; no values survive control joins.
    Only actual x1 string pointers at BL are returned, never nearby literals.
    """
    regs, out = {}, []
    insns = decoded(a, fn)
    targets = {int(i.op_str.split('#')[-1], 16) for i in insns
               if (i.mnemonic in ('b','cbz','cbnz','tbz','tbnz') or i.mnemonic.startswith('b.')) and '#' in i.op_str}
    for i in insns:
        if i.address in targets:
            regs.clear()
        op = i.operands
        def reg(o): return i.reg_name(o.reg).replace('w','x',1)
        value = None
        if i.mnemonic in ('adrp','adr'):
            value = op[1].imm
        elif i.mnemonic == 'add' and len(op) == 3 and op[1].type == 1 and op[2].type == 2:
            if reg(op[1]) in regs: value = regs[reg(op[1])] + op[2].imm
        elif i.mnemonic == 'mov' and len(op) == 2:
            if op[1].type == 1: value = regs.get(reg(op[1]))
            elif op[1].type == 2: value = op[1].imm
        if i.mnemonic == 'bl':
            vm = regs.get('x1')
            if vm in a.img.strings:
                out.append({'pc': i.address, 'target': op[0].imm, 'name':a.img.strings[vm], 'string_address':vm})
            for n in range(19): regs.pop('x'+str(n),None)
        else:
            try:
                _, writes = i.regs_access()
                for r in writes: regs.pop(i.reg_name(r).replace('w','x',1), None)
            except Exception:
                regs.clear()
            if value is not None and op and op[0].type == 1:
                regs[reg(op[0])] = value
            if i.mnemonic in ('b','br','blr','ret','cbz','cbnz','tbz','tbnz') or i.mnemonic.startswith('b.'):
                regs.clear()
    return out


def generate(app, historical):
    from extract_binary_vocabularies import SEEDS
    cur, old, graph, linked = inspect(app, historical)
    anchors = SEEDS['skin_elements'][0]
    owners = [{cur.owner(pc) for vm in cur.img.by_text.get(s,[]) for pc in cur.img.xrefs.get(vm,[])} for s in anchors]
    common = set.intersection(*owners)
    if len(common) != 1: raise ValueError('factory anchor function is ambiguous')
    factory = common.pop()
    vrefs = cur.img.address_xrefs([r['vtable'] for r in graph.values() if r['vtable']])
    writers = {}
    for name, r in graph.items():
        for pc in vrefs.get(r['vtable'], []):
            fn = cur.owner(pc)
            code = decoded(cur, fn)
            # Confirm a vtable pointer is stored at object offset zero.
            window = [i for i in code if pc <= i.address <= pc + 16]
            adds = [i for i in window if i.mnemonic == 'add' and len(i.operands)==3 and i.operands[2].type==2]
            for add in adds:
                rd = add.operands[0].reg
                for i in window:
                    if i.address > add.address and i.mnemonic == 'str' and i.operands[0].reg == rd and i.operands[1].mem.disp == 0:
                        writers.setdefault(fn, []).append({'class':name,'vtable':hex(r['vtable']),'store_pc':hex(i.address)})
    def resolve(fn):
        seen = set()
        while fn not in seen:
            seen.add(fn)
            code = cur.words(fn)
            if len(code)==1 and code[0][1]&0xfc000000==0x14000000:
                w=code[0][1]&0x3ffffff
                if w&0x2000000: w-=0x4000000
                fn += w*4
            else: break
        return fn
    calls = literal_calls(cur, factory)
    compare_targets = {c['target'] for c in calls if c['name'] in anchors}
    # Other fixed-length string comparators share the same node-name receiver.
    # Calibrate each from a known factory tag, not every literal in the function.
    for c in calls:
        if c['name'] in ('button','panel','text','textzone','browser','browsertoolbar','browsertoolbartree','equalizer'):
            compare_targets.add(c['target'])
    code = {i.address:i for i in decoded(cur,factory)}
    mappings, dispatch = {}, []
    for c in calls:
        if c['target'] not in compare_targets: continue
        branch = code.get(c['pc']+4)
        if not branch or branch.mnemonic not in ('cbz','cbnz','tbz','tbnz'): continue
        start = branch.address+4 if branch.mnemonic in ('cbz','tbz') else branch.operands[-1].imm
        todo, visited, found, unresolved = [start], set(), [], []
        while todo and len(visited)<512:
            pc=todo.pop()
            if pc in visited or pc not in code: continue
            visited.add(pc); i=code[pc]
            if i.mnemonic=='bl':
                t=i.operands[0].imm
                if t in compare_targets: continue
                target=resolve(t)
                if target in writers:
                    found += [dict(w,constructor=hex(target),call_pc=hex(pc)) for w in writers[target]]
                    continue
                unresolved.append(hex(t))
            if i.mnemonic in ('ret','br'): continue
            if i.mnemonic=='b': todo.append(i.operands[0].imm); continue
            if i.mnemonic in ('cbz','cbnz','tbz','tbnz') or i.mnemonic.startswith('b.'):
                todo.append(i.operands[-1].imm)
            todo.append(pc+4)
        record={'element':c['name'],'comparison_pc':hex(c['pc']),'success_pc':hex(start),'constructors':found,'visited_instructions':len(visited),'other_calls':sorted(set(unresolved))}
        dispatch.append(record)
        if found: mappings.setdefault(c['name'],[]).extend(found)
    # Anchor XML reader roles from the independently bounded common base reader.
    base_fns={cur.owner(pc) for vm in cur.img.by_text['clickthrough'] for pc in cur.img.xrefs.get(vm,[])}
    if len(base_fns)!=1: raise ValueError('base reader is ambiguous')
    basefn=base_fns.pop(); basecalls=literal_calls(cur,basefn)
    role_anchors={'clickthrough':['attribute_presence','attribute_value_comparison','attribute_boolean'], 'mouserect':['child_node'], 'minwidth':['attribute_integer']}
    getters={}
    for name,roles in role_anchors.items():
        matches=[c for c in basecalls if c['name']==name]
        if len(matches)!=len(roles): raise ValueError(f'XML role anchor changed: {name}')
        for c,role in zip(matches,roles): getters[c['target']]={'role':role,'anchor':name,'call_pc':hex(c['pc'])}
    # The presence and string getter pair is read directly in the literal action2 arm.
    action2owners={cur.owner(pc) for vm in cur.img.by_text['action2'] for pc in cur.img.xrefs.get(vm,[])}
    for fn in action2owners:
        pair=[c for c in literal_calls(cur,fn) if c['name']=='action2']
        if len(pair)==2:
            getters[pair[1]['target']]={'role':'attribute_string','anchor':'action2','call_pc':hex(pair[1]['pc'])}
    constructors={}
    for records in mappings.values():
        for r in records: constructors.setdefault(r['class'],set()).add(int(r['constructor'],16))
    classes={}
    all_children=set()
    for name,r in sorted(graph.items()):
        roots=set(r['slots']) | constructors.get(name,set())
        # Include all vptr-writing routines, labelled separately: constructors/destructors,
        # not a claim that all are readers. This covers classes not reached by factory.
        roots.update(fn for fn,ws in writers.items() if any(w['class']==name for w in ws))
        calls_by_fn={fn:cur.calls(fn) for fn in roots}
        reached=set(roots)
        reached.update(resolve(t) for cs in calls_by_fn.values() for _,t in cs if resolve(t) in cur.starts)
        attrs,children,unclassified,unresolved=[],[],[],[]
        for fn in sorted(reached):
            for c in literal_calls(cur,fn):
                entry={k:hex(v) if k in ('pc','target','string_address') else v for k,v in c.items()}
                entry['function']=hex(fn); entry['scope']='root' if fn in roots else 'direct_callee'
                role=getters.get(c['target'],{}).get('role')
                if role=='child_node': children.append(entry);all_children.add(c['name'])
                elif role: entry['reader_role']=role;attrs.append(entry)
                else: unclassified.append(entry)
            unresolved.extend(hex(t) for _,t in cur.calls(fn) if resolve(t) not in reached)
        classes[name]={'typeinfo':hex(r['typeinfo']),'vtable':hex(r['vtable']) if r['vtable'] else None,'bases':r['bases'],'vtable_slots':[hex(t) for t in r['slots']], 'elements':sorted(e for e,rs in mappings.items() if any(x['class']==name for x in rs)), 'roots':[hex(f) for f in sorted(roots)], 'visited_functions':[hex(f) for f in sorted(reached)], 'attribute_candidates':sorted({c['name'] for c in attrs}), 'attribute_reads':attrs,'child_node_reads':children,'other_literal_calls':unclassified,'unvisited_call_targets':sorted(set(unresolved))}
    inv=json.loads(Path('docs/skin-xml-inventory.json').read_text())
    metadata=plistlib.loads((app/'Contents/Info.plist').read_bytes())
    result={'schema_version':1,'source':{'build':metadata['CFBundleVersion'],'architecture':'arm64','binary_sha256':hashlib.sha256(cur.img.data).hexdigest(),'binary_date':'2026-08-24','evidence_tier':2},'summary':{},'factory':{'function':hex(factory),'end':hex(cur.ends[cur.starts.index(factory)]),'method':'LC_FUNCTION_STARTS boundary; element comparison success control flow to constructor vptr store to RTTI','pointer_tables':cur.img.tables([vm for s in anchors for vm in cur.img.by_text.get(s,[])]),'dispatch':dispatch,'element_classes':{e:sorted({r['class'] for r in rs}) for e,rs in mappings.items()}},'xml_reader_anchors':{hex(k):v for k,v in getters.items()},'classes':classes,'limitations':['Tier 2 leads only. Validate with a discriminating skin canary and independent readback.','Attributes include reads on child nodes and direct helper callees; not necessarily attributes on the outer element.','Only statically recovered x1 literals at direct calls to anchored XML readers are classified. Other calls are retained separately.','Traversal covers root routines and direct BL callees only; indirect calls and further callees remain unresolved.','Vptr writers include constructors and destructors; method names are not inferred from class spelling.','No absence from these candidate sets establishes a dead attribute. Template parameters are an open vocabulary.']}
    ARTIFACT.write_text(json.dumps(result,indent=2))
    return result

if __name__ == '__main__':
    main()
