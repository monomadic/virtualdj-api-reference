"""Attribute consumption experiment: native call traces plus hardware read watches."""
import offline_xml_trace as trace
import lldb

original_hit=trace.hit
original_returned=trace.returned
active=[]
hits={}
root=0

def number(process,address):return int.from_bytes(trace.read(process,address,8),'little')

def attributes(process,node):
    begin=number(process,node+24);end=number(process,node+32)
    if end<begin or end-begin>512:raise ValueError('attribute vector bounds')
    return [(trace.string(process,p),p) for p in (number(process,q) for q in range(begin,end,8))]

def children(process,node):
    begin=number(process,node+48);end=number(process,node+56)
    if end<begin or end-begin>512:raise ValueError('child vector bounds')
    return [number(process,q) for q in range(begin,end,8)]

def nodes(process,node,depth=0):
    if depth>8:raise ValueError('tree depth limit')
    yield node
    for child in children(process,node):yield from nodes(process,child,depth+1)

def snapshot(process,node,depth=0):
    if depth>8:raise ValueError('tree depth limit')
    return dict(name=trace.string(process,node),attributes=[dict(name=n,value=trace.string(process,p+24)) for n,p in attributes(process,node)],children=[snapshot(process,c,depth+1) for c in children(process,node)])

def watched(frame,wp,internal):
    label=next(label for ident,label in active if ident==wp.GetID());hits[label]=hits.get(label,0)+1
    trace.emit(dict(event='value_read',label=label,symbol=frame.GetFunctionName(),pc=hex(frame.GetPCAddress().GetFileAddress()),callers=[frame.GetThread().GetFrameAtIndex(i).GetFunctionName() for i in range(min(4,frame.GetThread().GetNumFrames()))]))
    return False

def hit(frame,bp,internal):
    global root
    name=frame.GetFunctionName() or ''
    if name.startswith('ISkinObject::createSkinObject') and not active:
        process=frame.GetThread().GetProcess();target=process.GetTarget();root=frame.FindRegister('x0').GetValueAsUnsigned()
        trace.emit(dict(event='tree_before_factory',tree=snapshot(process,root)))
        candidates=[]
        for node in nodes(process,root):
            for key,p in attributes(process,node):
                if key in ('zzunknown','width','widht') and len(candidates)<2:candidates.append((trace.string(process,node)+'.'+key,p+24))
        for label,p in candidates:
            # Fixed fixtures use SSO: watch all text bytes (including terminator) and length/tag.
            if trace.read(process,p,24)[23]>7:raise ValueError('watch fixture must be short')
            for suffix,address,size in [('.text',p,8),('.length',p+23,1)]:
                error=lldb.SBError();watch=target.WatchAddress(address,size,True,False,error)
                if not error.Success() or not watch.IsValid():raise ValueError('read watch failed: '+str(error))
                command=lldb.SBCommandReturnObject()
                target.GetDebugger().GetCommandInterpreter().HandleCommand('watchpoint command add -F '+__name__+'.watched '+str(watch.GetID()),command)
                if not command.Succeeded():raise ValueError(command.GetError())
                active.append((watch.GetID(),label+suffix));hits[label+suffix]=0
                trace.emit(dict(event='watch_installed',label=label+suffix,size=size,read=True,write=False))
    return original_hit(frame,bp,internal)

def returned(frame,bp,internal):
    process=frame.GetThread().GetProcess();key=(frame.GetThread().GetThreadID(),frame.GetPC())
    entry=trace.pending.get(key,[])
    factory=bool(entry and entry[-1]['symbol'].startswith('ISkinObject::createSkinObject'))
    result=original_returned(frame,bp,internal)
    if factory:
        for ident,label in active:process.GetTarget().DeleteWatchpoint(ident)
        trace.emit(dict(event='watch_summary',hits=hits.copy(),tree_after_factory=snapshot(process,root)))
        active.clear()
    return result

trace.hit=hit
trace.returned=returned

def __lldb_init_module(debugger,internal):
    debugger.HandleCommand('command script import '+trace.__file__)
    trace.hit=hit
    trace.returned=returned
