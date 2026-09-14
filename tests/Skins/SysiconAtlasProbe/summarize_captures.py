"""Make a contact sheet from saved app screenshots; never synthesizes glyphs."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).resolve().parent
rows=json.loads((root/'fixture.json').read_text())['rows']
base=Image.open(root/'normal-selected.png')
out=Image.new('RGB',(860,700),(20,24,30))
draw=ImageDraw.Draw(out)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',17)
for x,label in [(15,'Key'),(310,'Normal'),(415,'Selected'),(525,'Hover'),(625,'Hover+sel'),(750,'Atlas')]:
    draw.text((x,10),label,font=font,fill='white')
for n,row in enumerate(rows):
    key=row['key']; slug=key.replace(' ','_')
    cy=round(150+n*47.4); top=48+n*53
    draw.text((15,top+12),key,font=font,fill='white')
    samples=[(320,base,454),(430,base,597),
             (535,Image.open(root/f'edge-hover-{slug}.png'),454),
             (650,Image.open(root/f'edge-hover-selected-{slug}.png'),597),
             (760,base,741)]
    for x,img,cx in samples:
        out.paste(img.crop((cx-24,cy-21,cx+25,cy+22)),(x,top))
out.save(root/'comparison.png')
