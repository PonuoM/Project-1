"""Uniform source-to-native scaling preserves circles, shards and flame aspect ratios."""
from pathlib import Path
from PIL import Image
import numpy as np,json
D=Path(__file__).parent;spec=json.loads((D/'prompts-v1.json').read_text())
def save(name,im):
 p=D/name;assert not p.exists();im.save(p)
allrows=[];records=[]
for s in spec:
 src=Image.open(D/(s['id']+'-raw-v1.png')).convert('RGB');crops=[];bounds=[]
 for i in range(4):
  crop=src.crop((round(i*src.width/4),0,round((i+1)*src.width/4),src.height));crops.append(crop)
  a=np.array(crop);yy,xx=np.where(a.max(axis=2)>45);bounds.append((xx.min(),yy.min(),xx.max()+1,yy.max()+1))
 anchorx=(bounds[0][0]+bounds[0][2])/2;anchory=bounds[0][3]-1
 up=anchory-min(b[1] for b in bounds);down=max(b[3] for b in bounds)-anchory
 left=anchorx-min(b[0] for b in bounds);right=max(b[2] for b in bounds)-anchorx
 scale=min(48/max(1,up),7/max(1,down),27/max(1,left),27/max(1,right))
 pal=np.array([(0,0,0)]+[tuple(bytes.fromhex(h[1:])) for h in s['palette']],dtype=np.int32)
 cells=[];fr=[]
 for i,crop in enumerate(crops):
  srca=np.array(crop);out=np.zeros((64,64,3),dtype=np.uint8)
  for y in range(3,61):
   for x in range(3,61):
    sx=round(anchorx+(x-32)/scale);sy=round(anchory+(y-52)/scale)
    if 0<=sx<crop.width and 0<=sy<crop.height:
     c=srca[sy,sx].astype(np.int32);out[y,x]=pal[np.sum((pal-c)**2,axis=1).argmin()]
  yy,xx=np.where(out.max(axis=2)>0)
  fr.append(dict(frame=i+1,phase=['start','peak','breakup','remains'][i],boundsArtPx=[int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1],occupiedArtPixels=len(xx)))
  cells.append(out)
 native=Image.fromarray(np.concatenate(cells,axis=1));im=native.resize((1024,256),Image.Resampling.NEAREST);save(s['id']+'-v2.png',im);allrows.append(im)
 records.append(dict(effect=s['id'],sourceSize=list(src.size),size=list(im.size),anchorArtPx=[32,52],sourceAnchor=[float(anchorx),int(anchory)],uniformScale=float(scale),palette=['#000000']+s['palette'],frames=fr))
line=Image.new('RGB',(1024,1280))
for i,im in enumerate(allrows):line.paste(im,(0,i*256))
save('lineup-v2.png',line);save('lineup-1x-v2.png',line.resize((256,320),Image.Resampling.NEAREST))
p=D/'verification-v2.json';assert not p.exists();p.write_text(json.dumps(dict(exact4x4Grid=True,blackBackground=True,uniformAspectScale=True,effects=records),indent=2))
print([(r['effect'],r['frames'][1]['boundsArtPx']) for r in records])
