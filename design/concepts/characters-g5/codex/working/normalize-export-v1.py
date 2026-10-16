from PIL import Image
from pathlib import Path
import json
p=Path(r'C:/AppServ/www/Projects-1/design/concepts/characters-g5')
ids=['melee-1','melee-2','melee-3','mage-1','mage-2','mage-3','archer-1','archer-2','archer-3']
report=[]; images=[]
for name in ids:
 src=p/(name+'-raw-'+('v2' if name=='melee-1' else 'v1')+'.png')
 native=Image.open(src).convert('RGB').resize((64,64),Image.Resampling.NEAREST)
 bg=(0,177,64)
 for y in range(64):
  for x in range(64):
   r,g,b=native.getpixel((x,y))
   if g>95 and g>r+40 and g>b+40: native.putpixel((x,y),bg)
 points=[(x,y) for y in range(64) for x in range(64) if native.getpixel((x,y))!=bg]
 bottom=max(y for x,y in points); dy=62-bottom
 out=Image.new('RGB',(64,64),bg); out.paste(native,(0,dy))
 final=out.resize((512,512),Image.Resampling.NEAREST)
 dst=p/(name+'-'+('v3' if name=='melee-1' else 'v2')+'.png')
 if dst.exists(): raise RuntimeError('Never overwrite')
 final.save(dst); images.append(final)
 report.append({'file':dst.name,'size':[512,512],'groundRow':62,'exportShiftY':dy,'foregroundBounds':[min(x for x,y in points),min(y for x,y in points)+dy,max(x for x,y in points),62],'background':'#00B140','artPixelScale':8})
line=Image.new('RGB',(1536,1536),bg)
for i,im in enumerate(images): line.paste(im,((i%3)*512,(i//3)*512))
if (p/'lineup-v2.png').exists(): raise RuntimeError('Never overwrite')
line.save(p/'lineup-v2.png')
(p/'verification-v1.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
