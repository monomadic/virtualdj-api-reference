"""LLDB callbacks for the fixed offline XML spike; never attaches to a live app."""
import json
import lldb

pending = {}
return_breakpoints = {}
sequence = 0

def read(process, address, size):
    if not 0 <= size <= 16384: raise ValueError('read exceeds bound')
    if not size: return b''
    error=lldb.SBError();data=process.ReadMemory(address,size,error)
    if not error.Success(): raise ValueError(str(error))
    return data

def string(process, address):
    data=read(process,address,24);size=data[23]
    if size&128:address=int.from_bytes(data[:8],'little');size=int.from_bytes(data[8:16],'little')
    elif size>22:raise ValueError('invalid short string')
    return read(process,address,size).decode(errors='replace')

def emit(row):
    print('XMLTRACE '+json.dumps(row),flush=True)

def returned(frame, bp, internal):
    process=frame.GetThread().GetProcess();key=(frame.GetThread().GetThreadID(),frame.GetPC())
    if not pending.get(key):return False
    entry=pending[key].pop();name=entry['symbol'];value=frame.FindRegister('x0').GetValueAsUnsigned()
    row=dict(event='native_return',call_id=entry['call_id'],symbol=name)
    try:
        if name.startswith('CXMLNode::getParam') and 'allocator' not in name:
            row['text']=string(process,value)
        elif name.startswith('CXMLNode::getChild'):
            row['node']=string(process,value) if value else None
        elif name.startswith(('CXMLNode::getIntParam',)):
            value &= 0xffffffff;row['value']=value if value<0x80000000 else value-0x100000000
        elif name.startswith('CXMLNode::getFloatParam'):
            row['value']=float(frame.FindRegister('d0').GetValue())
        elif name.startswith(('ISkinObject::createSkinObject','IAction::create')):
            row['object_present']=bool(value)
            if value:
                vtable=int.from_bytes(read(process,value,8),'little')
                symbol=process.GetTarget().ResolveLoadAddress(vtable).GetSymbol()
                row['vtable_symbol']=symbol.GetName() if symbol.IsValid() else None
        else:row['value']=value & 0xffffffff
    except Exception as e:row['read_error']=str(e)
    emit(row);return False

def hit(frame,bp,internal):
    global sequence
    process=frame.GetThread().GetProcess();target=process.GetTarget()
    name=frame.GetFunctionName() or '';sequence+=1
    row=dict(event='native_call',call_id=sequence,symbol=name,pc=hex(frame.GetPCAddress().GetFileAddress()))
    def reg(n):return frame.FindRegister(n).GetValueAsUnsigned()
    try:
        if name.startswith('CXMLNode::') and ('get' in name or 'hasParam' in name):
            row['node']=string(process,reg('x0')) if reg('x0') else None
            row['key']=read(process,reg('x1'),reg('x2')).decode(errors='replace')
            if name.startswith('CXMLNode::getIntParam') and ', int)' in name:
                raw=reg('x3')&0xffffffff;row['default']=raw if raw<0x80000000 else raw-0x100000000
            if name.startswith('CXMLNode::getBoolParam'):row['default']=bool(reg('x3')&1)
        elif name.startswith('ISkinObject::createSkinObject'):row['node']=string(process,reg('x0'))
        elif name.startswith('IAction::create'):
            error=lldb.SBError();row['script']=process.ReadCStringFromMemory(reg('x0'),512,error)
            if not error.Success():raise ValueError(str(error))
        caller=frame.GetThread().GetFrameAtIndex(1)
        row['caller']=caller.GetFunctionName()
        row['caller_pc']=hex(caller.GetPCAddress().GetFileAddress())
    except Exception as e:row['read_error']=str(e)
    emit(row)
    # Constructors have tail aliases; avoid presenting duplicate return pairs for them.
    if not name.startswith(('CSkin','ISkinObject::ISkinObject')) and 'setErrorMessage' not in name:
        address=reg('x30');key=(frame.GetThread().GetThreadID(),address)
        pending.setdefault(key,[]).append(row)
        if address not in return_breakpoints:
            ret=target.BreakpointCreateByAddress(address)
            ret.SetScriptCallbackFunction(__name__+'.returned');return_breakpoints[address]=ret.GetID()
    return False

def ready(frame,bp,internal):
    target=frame.GetThread().GetProcess().GetTarget()
    for pattern in [r'^CXMLFile::(loadFromBuffer|loadFromString|setErrorMessage)',
                    r'^CXMLNode::(load\(|getParam\(|getParamNonConst\(|getChild\(|getIntParam\(|getBoolParam\(|getFloatParam\(|hasParam\()',
                    r'^ISkinObject::(createSkinObject|ISkinObject)',r'^CSkin(Button|Panel|Text)::CSkin',r'^IAction::create\(char const\*']:
        probe=target.BreakpointCreateByRegex(pattern,'libvdj-parser.dylib');probe.SetScriptCallbackFunction(__name__+'.hit')
    emit(dict(event='trace_ready'));return False

def setup(debugger,command,result,internal):
    probe=debugger.GetSelectedTarget().BreakpointCreateByName('XMLTraceReady')
    probe.SetScriptCallbackFunction(__name__+'.ready')
    result.PutCString('Tracing deferred until after integrity checks')

def __lldb_init_module(debugger,internal):
    debugger.HandleCommand('command script add -f '+__name__+'.setup xml-setup')
