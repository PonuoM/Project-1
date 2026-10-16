from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
D=Path(__file__).parent;I=D.parent/'input';BG=(0,177,64)
layout=json.loads((I/'layout.json').read_text());results=[]
for name,lay in layout.items():
 orig=np.asarray(Image.open(I/(name+'.png')).convert('RGB'))
 final=np.asarray(Image.open(D/(name+'-v2.png')).convert('RGB'))
 assert orig.shape==final.shape
 allowed=np.ones(orig.shape[:2],bool)
 for c in lay['cells']:
  x,y,w,h,pad=[c[k]*2 for k in ['x','y','w','h','pad']]
  allowed[y+pad:y+pad+h,x:x+w]=False
 changed=np.any(orig!=final,axis=2)
 assert not np.any(changed&~allowed)
 assert np.array_equal(final,np.repeat(np.repeat(final[::2,::2],2,axis=0),2,axis=1))
 palette=set(map(tuple,np.unique(orig.reshape(-1,3),axis=0)))
 assert set(map(tuple,np.unique(final.reshape(-1,3),axis=0)))<=palette
 additions=np.zeros_like(final);additions[:]=BG;additions[allowed]=final[allowed]
 p=D/(name+'-additions-v2.png');assert not p.exists();Image.fromarray(additions).save(p)
 results.append(dict(sheet=name,size=[final.shape[1],final.shape[0]],changedImagePixels=int(changed.sum()),protectedChangedPixels=int(np.sum(changed&~allowed)),originalRectangleSha256=hashlib.sha256(orig[~allowed].tobytes()).hexdigest(),finalRectangleSha256=hashlib.sha256(final[~allowed].tobytes()).hexdigest(),exact2x2Grid=True,originalPaletteOnly=True))
files=[]
for p in sorted(D.glob('*.png')):
 with Image.open(p) as im:files.append(dict(file=p.name,size=list(im.size),format=im.format))
p=D/'files-v2.json';assert not p.exists();p.write_text(json.dumps(files,indent=2)+'\n')
p=D/'verification-final-v2.json';assert not p.exists();p.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'verification':results,'files':files},indent=2))
