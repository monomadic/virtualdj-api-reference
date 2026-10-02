"""Trace milestones in the isolated skin host, then preserve any crash backtrace."""
import json

def hit(frame,bp,internal):
 if 'sysMessageBox' in (frame.GetFunctionName() or ''):
  # Stop at the application error dialog before it creates a GUI/modal loop.
  from offline_xml_trace import string
  process=frame.GetThread().GetProcess()
  try:message=string(process,frame.FindRegister('x0').GetValueAsUnsigned())
  except Exception as e:message=str(e)
  print('SKINTRACE '+json.dumps(dict(event='blocked_message_box',message=message)),flush=True)
  return True
 row=dict(event='native_call',symbol=frame.GetFunctionName(),pc=hex(frame.GetPCAddress().GetFileAddress()))
 if (frame.GetFunctionName() or '').startswith(('CZip::open(', 'CZip::openFile(', 'CXMLFile::loadFromFile(', 'CImage::loadFromFile(')):
  from offline_xml_trace import string
  try:row['path']=string(frame.GetThread().GetProcess(),frame.FindRegister('x1').GetValueAsUnsigned())
  except Exception as e:row['read_error']=str(e)
 print('SKINTRACE '+json.dumps(row),flush=True);return False

def ready(frame,bp,internal):
 target=frame.GetThread().GetProcess().GetTarget()
 for pattern in [r'^CSkinEngine::(load\(|loadEnd|openZip|loadImage)',r'^CSkinWindow::(CSkinWindow|load\(|drawWindow)',r'^CImage::(loadFrom|createBuffer)',r'^IOSWindow::',r'^ISkinObject::createSkinObject',r'^CBrowser::initImages',r'^CSkinPanel::load',r'^ISkinContainer::',r'^CRenderTargetMetal::(create|beginDraw|copyRenderTargetData)',r'^CSkinPanel::draw',r'^CSkinButton::draw',r'^CZip::open',r'^CXMLFile::loadFromFile']:
  b=target.BreakpointCreateByRegex(pattern,'libvdj-parser.dylib');b.SetScriptCallbackFunction(__name__+'.hit')
 return False

def setup(debugger,command,result,internal):
 b=debugger.GetSelectedTarget().BreakpointCreateByName('SkinTraceReady');b.SetScriptCallbackFunction(__name__+'.ready')

def __lldb_init_module(debugger,internal):debugger.HandleCommand('command script add -f '+__name__+'.setup skin-setup')
