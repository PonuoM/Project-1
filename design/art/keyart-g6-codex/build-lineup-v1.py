from PIL import Image
from pathlib import Path
import json
p=Path(r'C:/AppServ/www/Projects-1/design/art/keyart-g6-codex')
best=json.loads((p/'recommended-v1.json').read_text())
line=Image.new('RGB',(1600,960))
for i,(name,f) in enumerate(best.items()):
 im=Image.open(p/f).convert('RGB')
 assert im.size==(1024,1536),(f,im.size)
 line.paste(im.resize((320,480),Image.Resampling.LANCZOS),((i%5)*320,(i//5)*480))
if (p/'lineup-v1.png').exists():raise RuntimeError('Never overwrite')
line.save(p/'lineup-v1.png')
rows=[]
for f in sorted(p.glob('*.png')):
 im=Image.open(f)
 rows.append({'file':f.name,'size':list(im.size),'bytes':f.stat().st_size,'format':im.format})
 print(f.name,im.size)
(p/'files-v1.json').write_text(json.dumps(rows,indent=2))
