"""Build a no-action sysicon comparison fixture from the installed vendor atlas."""
import hashlib,json,plistlib
from pathlib import Path
from xml.sax.saxutils import quoteattr
from PIL import Image
ROOT=Path(__file__).resolve().parent
APP=Path('/Applications/VirtualDJ.app')
build=plistlib.loads((APP/'Contents/Info.plist').read_bytes())['CFBundleVersion']
if build != '18.0.9598':
 raise SystemExit('This is a frozen b9598 fixture. Create a new build-specific fixture instead.')
ROWS=[('folder',32),('playlist',37),('plus',64),('minus',65),('browser_shortcut',75),('search_folder',68),('load_next',124),('search',68),('headphones',69),('zz_sysicon_control',None),('font_size 0',None),('stems_vocal',144)]
W,H=1200,740
atlas=Image.open(APP/'Contents/Resources/icons.png').convert('RGBA')
sheet=Image.new('RGBA',(W,1120),(20,24,30,255))
small=atlas.resize((512,320),Image.Resampling.LANCZOS)
sheet.alpha_composite(small,(0,800))
gold=Image.new('RGBA',small.size,(255,191,64,0));gold.putalpha(small.getchannel('A'))
sheet.alpha_composite(gold,(600,800))
sheet.save(ROOT/'skin.png')
xml=[f'<skin name="ZZ Sysicon Atlas Probe" version="8" width="{W}" height="{H}">','<nbdecks value="2"/>','<square color="#14181e"><pos x="0" y="0"/><size width="1200" height="740"/></square>']
def text(x,y,w,s,size=16):
 xml.append(f'<textzone><pos x="{x}" y="{y}"/><size width="{w}" height="24"/><text font="Arial" size="{size}" color="#eeeeee" align="left" format={quoteattr(s)}/></textzone>')
text(24,15,1100,'SYSICON ATLAS PROBE / b9598 / revision 2',22)
text(24,46,1100,'White = normal. Amber = selected. Cyan = actual mouse hover. Buttons execute nothing.',14)
for x,s in [(24,'Key'),(420,'Normal'),(560,'Selected'),(700,'Atlas crop'),(840,'Crop selected'),(990,'Cell')]:text(x,82,190,s)
for n,(key,idx) in enumerate(ROWS):
 y=118+n*46
 text(24,y+6,380,key)
 for x,selected,crop in [(420,False,False),(560,True,False),(700,False,True),(840,True,True)]:
  if crop and idx is None:continue
  if crop:
   xml.append(f'<visual><pos x="{x+8}" y="{y+4}"/><size width="32" height="32"/><off x="{idx%16*32+(600 if selected else 0)}" y="{800+idx//16*32}"/></visual>')
   continue
  source=f'sysicon={quoteattr(key)}'
  xml.append(f'<button action="nothing" query="{"on" if selected else "off"}"><pos x="{x}" y="{y}"/><size width="48" height="40"/><off shape="square" color="#242b35"/><on shape="square" color="#242b35"/><icon {source} width="32" height="32" color="#ffffff" colorselected="#ffbf40" colorover="#40dfff" coloroverselected="#40dfff"/></button>')
 text(990,y+6,160,'control' if idx is None else f'{chr(65+idx//16)}{idx%16+1} / {idx}')
text(24,690,1150,'No browser, track labels, transport controls, or persistent variables. Original skin restored after capture.',14)
xml.append('</skin>')
(ROOT/'skin.xml').write_text('\n'.join(xml)+'\n')
meta={'build':plistlib.loads((APP/'Contents/Info.plist').read_bytes())['CFBundleVersion'],'atlas_sha256':hashlib.sha256((APP/'Contents/Resources/icons.png').read_bytes()).hexdigest(),'atlas_size':list(atlas.size),'rows':[{'key':k,'index':i} for k,i in ROWS],'fixture_sha256':hashlib.sha256((ROOT/'skin.xml').read_bytes()).hexdigest(),'scope':'Explicit icon sysicon attribute, action nothing, queries off and on. No customicons override. Direct bitmap crops use vendor atlas RGB/alpha; gold reference uses alpha silhouette.'}
(ROOT/'fixture.json').write_text(json.dumps(meta,indent=2)+'\n')
