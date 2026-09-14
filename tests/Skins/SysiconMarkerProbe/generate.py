"""Frozen b9598 diagnostic atlas: opaque numbered cells, file and main-PNG routes."""
import hashlib,json,plistlib
from pathlib import Path
from xml.sax.saxutils import quoteattr
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
APP=Path('/Applications/VirtualDJ.app')
build=plistlib.loads((APP/'Contents/Info.plist').read_bytes())['CFBundleVersion']
if build!='18.0.9598':raise SystemExit('Create a new build-specific fixture instead of overwriting this one.')
ROWS=[('folder',32),('plus',64),('search',68),('headphones',69),('load_next',124),('sampler_drop',128),('close',139),('stems_vocal',144),('stems_instru',145),('stems_bass',146),('stems_kick',147),('stems_hihat',148),('zz_sysicon_control',None),('font_size 0',None)]
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',25)
for mode,letter in [('file','F'),('main','M')]:
 p=ROOT/mode;p.mkdir(exist_ok=True)
 atlas=Image.new('RGBA',(1024,640),'white');d=ImageDraw.Draw(atlas)
 for i in range(160):
  x=i%16*64;y=i//16*64
  d.rectangle((x+2,y+2,x+61,y+61),outline='black',width=3)
  d.text((x+32,y+30),str(i),font=font,fill='black',anchor='mm')
  d.text((x+32,y+52),letter,font=font.font_variant(size=14),fill='black',anchor='mm')
 assert atlas.getchannel('A').getextrema()==(255,255)
 atlas.save(p/'markers.png')
 sheet=Image.new('RGBA',(1200,1500),(20,24,30,255));sheet.paste(atlas,(0,800));sheet.save(p/'skin.png')
 xml=['<skin name="ZZ Sysicon Marker Probe" version="8" width="1200" height="740">','<nbdecks value="2"/>']
 xml.append('<customicons file="markers.png" x="0" y="0" iconsize="64" nb="160" nbx="16"/>' if mode=='file' else '<customicons x="0" y="800" iconsize="64" nb="160" nbx="16"/>')
 xml.append('<square color="#14181e"><pos x="0" y="0"/><size width="1200" height="740"/></square>')
 def text(x,y,w,s,size=16):
  xml.append(f'<textzone><pos x="{x}" y="{y}"/><size width="{w}" height="24"/><text font="Arial" size="{size}" color="#eeeeee" align="left" format={quoteattr(s)}/></textzone>')
 text(20,12,1160,f'OPAQUE ATLAS / {mode.upper()} route / {letter} markers / b9598',22)
 text(20,42,1160,'Every atlas pixel has alpha 255. Known keys must show numbers before blank candidates are interpreted.',15)
 for x,s in [(20,'Explicit sysicon'),(440,'Normal'),(580,'Selected'),(740,'Direct marker'),(960,'Expected index')]:text(x,80,240,s)
 for n,(key,index) in enumerate(ROWS):
  y=114+n*41
  text(20,y+8,400,key)
  for x,query in [(440,'off'),(580,'on')]:
   xml.append(f'<button action="nothing" query="{query}"><pos x="{x}" y="{y}"/><size width="56" height="40"/><off shape="square" color="#242b35"/><on shape="square" color="#242b35"/><icon sysicon={quoteattr(key)} width="36" height="36" color="#ffffff" colorselected="#ffbf40" colorover="#40dfff" coloroverselected="#40dfff"/></button>')
  if index is not None:
   # Raw reference at source size, outside the button grid; shrink bitmap beforehand.
   crop=atlas.crop((index%16*64,index//16*64,index%16*64+64,index//16*64+64)).resize((36,36),Image.Resampling.LANCZOS)
   sheet.paste(crop,(1100,n*40+800))
   xml.append(f'<visual><pos x="740" y="{y+2}"/><size width="36" height="36"/><off x="1100" y="{800+n*40}"/></visual>')
  text(960,y+8,200,'control' if index is None else str(index))
 text(20,706,1160,'Only nothing is executed by buttons. No persistent variables or transport actions.',14)
 xml.append('</skin>');(p/'skin.xml').write_text('\n'.join(xml)+'\n');sheet.save(p/'skin.png')
meta={'build':build,'rows':[{'key':k,'predicted_index':i} for k,i in ROWS],'atlas_cells':160,'cell_size':64,'columns':16,'alpha_extrema':[255,255],'modes':['file','main'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.glob('*/*')) if p.suffix in ('.png','.xml')}}
(ROOT/'fixture.json').write_text(json.dumps(meta,indent=2)+'\n')
