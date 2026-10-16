"""Grid/palette export of imagegen VFX sheets. No replacement artwork drawn."""
from pathlib import Path
from PIL import Image
import numpy as np,json
D=Path(__file__).parent
spec=json.loads((D/'prompts-v1.json').read_text())
def save(name,im):
 p=D/name;assert not p.exists();im.save(p)
records=[];sheets=[]
for s in spec:
 src=Image.open(D/(s['id']+'-raw-v1.png')).convert('RGB')
 pal=np.array([(0,0,0)]+[tuple(bytes.fromhex(h[1:])) for h in s['palette']],dtype=np.int16)
 cells=[];frames=[]
 for i in range(4):
  crop=src.crop((round(i*src.width/4),0,round((i+1)*src.width/4),src.height))
  small=crop.resize((64,64),Image.Resampling.NEAREST)
  a=np.array(small).astype(np.int16)
  dist=np.sum((a[:,:,None,:].astype(np.int32)-pal[None,None,:,:])**2,axis=3)
  idx=dist.argmin(axis=2);out=pal[idx].astype(np.uint8)
  # Keep an empty gutter even if the generator put stray pixels near cell edges.
  out[:3]=0;out[-3:]=0;out[:,:3]=0;out[:,-3:]=0
  cells.append(out)
 # One shared alignment keeps all four temporal keys in a common space.
 yy,xx=np.where(np.any(cells[0]>0,axis=2));assert len(xx)
 dx=32-round((int(xx.min())+int(xx.max()))/2)
 dy=52-int(yy.max())
 # Lightning's tiny start charge is at the top; ground spark still anchors at52.
 for i,a in enumerate(cells):
  b=np.zeros_like(a)
  for y in range(64):
   for x in range(64):
    nx,ny=x+dx,y+dy
    if 3<=nx<61 and 3<=ny<61:b[ny,nx]=a[y,x]
  cells[i]=b
  yy,xx=np.where(np.any(b>0,axis=2))
  bounds=[int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1] if len(xx) else None
  frames.append(dict(frame=i+1,phase=['start','peak','breakup','remains'][i],boundsArtPx=bounds,occupiedArtPixels=int(len(xx))))
 native=Image.fromarray(np.concatenate(cells,axis=1))
 out=native.resize((1024,256),Image.Resampling.NEAREST)
 save(s['id']+'-v1.png',out);sheets.append(out)
 arr=np.asarray(out)
 assert np.array_equal(arr,np.repeat(np.repeat(arr[::4,::4],4,axis=0),4,axis=1))
 assert set(map(tuple,np.unique(arr.reshape(-1,3),axis=0)))<=set(map(tuple,pal))
 assert (122,60,255) not in set(map(tuple,pal))
 records.append(dict(effect=s['id'],sourceSize=list(src.size),size=list(out.size),nativeSize=list(native.size),hitAnchorArtPx=[32,52],sharedTranslationArtPx=[dx,dy],palette=['#000000']+s['palette'],frames=frames))
line=Image.new('RGB',(1024,1280));
for i,im in enumerate(sheets):line.paste(im,(0,i*256))
save('lineup-v1.png',line)
save('lineup-1x-v1.png',line.resize((256,320),Image.Resampling.NEAREST))
report=dict(exact4x4Grid=True,pureBlackBackground=True,contentColorsPerEffect=4,cellSizeArtPx=[64,64],frameOrder=['start','peak','breakup','remains'],effects=records)
p=D/'verification-v1.json';assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
