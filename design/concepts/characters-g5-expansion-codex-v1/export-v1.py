from PIL import Image
from pathlib import Path
import json
p=Path(r'C:/AppServ/www/Projects-1/design/concepts/characters-g5-expansion-codex-v1')
report=[]
for src in sorted(p.glob('*-raw-v1.png')):
 dst=p/src.name.replace('-raw','')
 if dst.exists(): raise RuntimeError('Never overwrite '+str(dst))
 im=Image.open(src).convert('RGB'); rawsize=im.size
 native=im.resize((64,64),Image.Resampling.NEAREST); bg=(0,177,64)
 for y in range(64):
  for x in range(64):
   r,g,b=native.getpixel((x,y))
   if g>95 and g>r+40 and g>b+40: native.putpixel((x,y),bg)
 pts=[(x,y) for y in range(64) for x in range(64) if native.getpixel((x,y))!=bg]
 dy=62-max(y for x,y in pts)
 out=Image.new('RGB',(64,64),bg);out.paste(native,(0,dy))
 out.resize((512,512),Image.Resampling.NEAREST).save(dst)
 report.append({'file':dst.name,'rawSize':list(rawsize),'size':[512,512],'bottomRow':62,'verticalShift':dy,'bounds':[min(x for x,y in pts),min(y for x,y in pts)+dy,max(x for x,y in pts),62]})
exp=['melee-brawler-v1.png','melee-assassin-v1.png','mage-summoner-v1.png','ranged-gunner-dual-v1.png','ranged-gunner-laser-v1.png']
line=Image.new('RGB',(1536,1024),bg)
for i,n in enumerate(exp):line.paste(Image.open(p/n),((i%3)*512,(i//3)*512))
line.save(p/'changes-lineup-v1.png')
old=p.parent/'characters-g5'/'codex-export-v1'
full=[old/'melee-1-v2.png',p/'melee-brawler-v1.png',old/'melee-3-v1.png',p/'melee-assassin-v1.png',old/'mage-1-v1.png',old/'mage-2-v1.png',p/'mage-summoner-v1.png',None,old/'archer-1-v1.png',old/'archer-2-v1.png',p/'ranged-gunner-dual-v1.png',p/'ranged-gunner-laser-v1.png']
line=Image.new('RGB',(2048,1536),bg)
for i,f in enumerate(full):
 if f:line.paste(Image.open(f),((i%4)*512,(i//4)*512))
line.save(p/'roster-lineup-v1.png')
(p/'verification-v1.json').write_text(json.dumps(report,indent=2))
for f in sorted(p.glob('*.png')):print(f.name,Image.open(f).size)
print(json.dumps(report,indent=2))
