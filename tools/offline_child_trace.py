"""Source-path traces for fixed native child-relationship cases in our own host."""
import json
import lldb
from offline_xml_trace import read, string

paths = {}
pending = {}
returns = {}
sequence = 0


def emit(row):
    print('CHILDTRACE ' + json.dumps(row), flush=True)


def index_nodes(process, node, path='/skin', depth=0):
    if depth > 10 or len(paths) > 128:raise ValueError('XML path bound')
    paths[node] = path
    raw=read(process,node+48,16)
    begin=int.from_bytes(raw[:8],'little');end=int.from_bytes(raw[8:],'little')
    if end < begin or (end-begin)%8 or end-begin > 1024:raise ValueError('XML child bound')
    counts={}
    for offset in range(begin,end,8):
        child=int.from_bytes(read(process,offset,8),'little')
        tag=string(process,child);counts[tag]=counts.get(tag,0)+1
        index_nodes(process,child,path+'/'+tag+'['+str(counts[tag])+']',depth+1)


def returned(frame,bp,internal):
    key=(frame.GetThread().GetThreadID(),frame.GetPC())
    if not pending.get(key):return False
    entry=pending[key].pop();value=frame.FindRegister('x0').GetValueAsUnsigned()
    row=dict(event='return',call_id=entry['call_id'],symbol=entry['symbol'],present=bool(value))
    process=frame.GetThread().GetProcess()
    try:
        if entry['symbol'].startswith('CXMLNode::getChild'):
            row['source_path']=paths.get(value)
            row['node']=string(process,value) if value else None
        elif value:
            vtable=int.from_bytes(read(process,value,8),'little')
            symbol=process.GetTarget().ResolveLoadAddress(vtable).GetSymbol()
            row['class_symbol']=symbol.GetName() if symbol.IsValid() else None
    except Exception as e:row['read_error']=str(e)
    emit(row);return False


def hit(frame,bp,internal):
    global sequence
    sequence+=1
    name=frame.GetFunctionName() or ''
    process=frame.GetThread().GetProcess();target=process.GetTarget()
    reg=lambda n:frame.FindRegister(n).GetValueAsUnsigned()
    row=dict(event='call',call_id=sequence,symbol=name,pc=hex(frame.GetPCAddress().GetFileAddress()))
    try:
        node=reg('x0') if name.startswith(('ISkinObject::createSkinObject','CXMLNode::getChild')) else reg('x1')
        if name.startswith('CSkinButton::addTextObject'):
            node=reg('x2');error=lldb.SBError();row['key']=process.ReadCStringFromMemory(reg('x1'),128,error)
            if not error.Success():raise ValueError(str(error))
        if name.startswith('CSkinRack::addUnitChildren'):node=reg('x2')
        row['source_path']=paths.get(node);row['node']=string(process,node) if node else None
        if name.startswith('CXMLNode::getChild'):row['key']=read(process,reg('x1'),reg('x2')).decode()
        caller=frame.GetThread().GetFrameAtIndex(1)
        row['caller']=caller.GetFunctionName();row['caller_pc']=hex(caller.GetPCAddress().GetFileAddress())
        if name.startswith(('ISkinObject::createSkinObject','CXMLNode::getChild')):
            address=reg('x30');key=(frame.GetThread().GetThreadID(),address)
            pending.setdefault(key,[]).append(row)
            if address not in returns:
                ret=target.BreakpointCreateByAddress(address);ret.SetScriptCallbackFunction(__name__+'.returned');returns[address]=ret.GetID()
    except Exception as e:row['read_error']=str(e)
    emit(row);return False


def ready(frame,bp,internal):
    target=frame.GetThread().GetProcess().GetTarget()
    try:
        index_nodes(frame.GetThread().GetProcess(),frame.FindRegister('x1').GetValueAsUnsigned())
        for pattern in [r'^ISkinObject::createSkinObject\(',r'^CSkinPanel::loadChildren\(',r'^CSkinRack::(loadChildren|addUnitChildren)\(',r'^CSkinButton::addTextObject\(',r'^CXMLNode::getChild\(']:
            probe=target.BreakpointCreateByRegex(pattern,'libvdj-parser.dylib');probe.SetScriptCallbackFunction(__name__+'.hit')
        emit(dict(event='ready',source_paths=list(paths.values())))
    except Exception as e:emit(dict(event='ready',read_error=str(e)))
    bp.GetBreakpoint().SetEnabled(False)
    return False


def arm(frame,bp,internal):
    probe=frame.GetThread().GetProcess().GetTarget().BreakpointCreateByRegex(r'^CSkinWindow::load\(', 'libvdj-parser.dylib')
    probe.SetScriptCallbackFunction(__name__+'.ready')

    return False


def __lldb_init_module(debugger,internal):
    probe=debugger.GetSelectedTarget().BreakpointCreateByName("RelationshipTraceReady")
    probe.SetScriptCallbackFunction(__name__+".arm")
