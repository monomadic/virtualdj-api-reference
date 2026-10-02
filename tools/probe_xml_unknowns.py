#!/usr/bin/env python3
"""Fixed comparisons for recognition versus consumption; no broad schema claim."""
import argparse
import json
from pathlib import Path
import offline_xml
import trace_offline_xml

CASES=[
 ('factory_known','<button><size width="10" height="20"/></button>'),
 ('factory_unknown_tag','<zzunknown/>'),
 ('factory_known_child_as_root','<size width="10" height="20"/>'),
 ('factory_unknown_attribute','<button zzunknown="yes"><size width="10" height="20"/></button>'),
 ('factory_unknown_child','<button><zzchild width="99"/><size width="10" height="20"/></button>'),
 ('factory_unknown_wrapper','<button><zzchild><size width="99" height="20"/></zzchild></button>'),
 ('factory_misspelled_width','<button><size widht="99" height="20"/></button>'),
]

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['prepare','run','trace']);p.add_argument('--work',type=Path,required=True);p.add_argument('--app',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
 offline_xml.CASES=CASES
 if a.mode=='prepare':print(json.dumps(offline_xml.prepare(a.app,a.work)))
 elif a.mode=='run':print(json.dumps(offline_xml.run(a.work,a.output)))
 else:
  trace_offline_xml.CASES=CASES;trace_offline_xml.TRACE_NAMES=[n for n,x in CASES]
  trace_offline_xml.run(a.work,a.output,module=Path(__file__).with_name('offline_xml_unknown_trace.py').resolve())
if __name__=='__main__':main()
