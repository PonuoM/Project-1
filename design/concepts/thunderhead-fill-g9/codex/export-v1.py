"""Register imagegen fill to input cells, palette/grid-lock ONLY padding, preserve originals.
No source frame, input, game asset or merge_fill.py is modified.
"""
from pathlib import Path
from PIL import Image
import numpy as np
from collections import deque
import json, hashlib

D=Path(__file__).parent;I=D.parent/'input';BG=np.array([0,177,64],dtype=np.uint8)
layout=json.loads((I/'layout.json').read_text())
def shifted(a,dx,dy):
 h,w=a.shape[:2];out=np.zeros_like(a);out[:]=BG
 x0=max(0,dx);y0=max(0,dy);x1=min(w,w+dx);y1=min(h,h+dy)
 out[y0:y1,x0:x1]=a[y0-dy:y1-dy,x0-dx:x1-dx];return out
def overlap(a,b,mask):
 u=np.sum((a|b)&mask)
 return np.sum(a&b&mask)/u if u else 1
records=[]
for name,lay in layout.items():
 original=Image.open(I/(name+'.png')).convert('RGB')
 source=Image.open(D/(name+'-raw-v1.png')).convert('RGB')
 orig=np.array(original)[::2,::2];output=np.array(original).copy()
 palette=np.unique(orig.reshape(-1,3),axis=0)
 cols=lay['cols'];rows=2;cells=[]
 for j,c in enumerate(lay['cells']):
  x,y,w,h,pad=[c[k] for k in ['x','y','w','h','pad']];cw=w+pad;ch=h+pad
  # Rescale each generated cell independently; no interpolation of original pixels.
  col=j%cols;row=j//cols
  crop=source.crop((round(col*source.width/cols),round(row*source.height/rows),round((col+1)*source.width/cols),round((row+1)*source.height/rows)))
  a=np.asarray(crop.resize((cw,ch),Image.Resampling.NEAREST)).astype('float32')
  nearest=np.argmin(np.sum((a[:,:,None,:]-palette[None,None,:,:].astype('float32'))**2,axis=3),axis=2)
  a=palette[nearest]
  oc=orig[y:y+ch,x:x+cw];ofg=np.any(oc!=BG,axis=2)
  protected=np.zeros((ch,cw),bool);protected[pad:,:w]=True
  seam=np.zeros_like(protected);seam[pad:pad+10,:w]=True;seam[pad:,max(0,w-10):w]=True
  best=(-1,0,0,a);base=None
  for dy in range(-6,7):
   for dx in range(-6,7):
    candidate=shifted(a,dx,dy);fg=np.any(candidate!=BG,axis=2)
    score=.45*overlap(ofg,fg,protected)+.55*overlap(ofg,fg,seam)
    if dx==0 and dy==0:base=score
    if score>best[0]:best=(score,dx,dy,candidate)
  score,dx,dy,a=best
  if score<base+.005:dx=dy=0;a=palette[nearest];score=base
  af=np.any(a!=BG,axis=2)&~protected
  # Retain generated additions only if attached to an existing cut-edge pixel.
  connected=np.zeros_like(af);q=deque()
  for yy,xx in zip(*np.where(ofg&protected)):
   for ny,nx in [(yy-1,xx),(yy,xx+1)]:
    if 0<=ny<ch and 0<=nx<cw and af[ny,nx] and not connected[ny,nx]:connected[ny,nx]=True;q.append((ny,nx))
  while q:
   yy,xx=q.popleft()
   for oy in [-1,0,1]:
    for ox in [-1,0,1]:
     ny,nx=yy+oy,xx+ox
     if 0<=ny<ch and 0<=nx<cw and af[ny,nx] and not connected[ny,nx]:connected[ny,nx]=True;q.append((ny,nx))
  # All added samples are the generated art, without hand drawing or changing source pixels.
  out=oc.copy();out[~protected]=BG;out[connected]=a[connected]
  tile=np.repeat(np.repeat(out,2,axis=0),2,axis=1)
  # Full original rectangle restored at image resolution, including its background pixels.
  tile[pad*2:,:w*2]=np.asarray(original)[(y+pad)*2:(y+ch)*2,x*2:(x+w)*2]
  output[y*2:(y+ch)*2,x*2:(x+cw)*2]=tile
  top_orig=ofg[pad,:w];top_added=connected[pad-1,:w]
  right_orig=ofg[pad:,w-1];right_added=connected[pad:,w]
  assert np.array_equal(tile[pad*2:,:w*2],np.asarray(original)[(y+pad)*2:(y+ch)*2,x*2:(x+w)*2])
  assert not np.any(connected&protected)
  cells.append(dict(cell=j+1,move=c['move'],frame=c['frame'],registrationShiftNative=[dx,dy],matchScore=round(float(score),4),addedNativePixels=int(connected.sum()),topCutOriginalPixels=int(top_orig.sum()),topCutJoinedPixels=int((top_orig&top_added).sum()),rightCutOriginalPixels=int(right_orig.sum()),rightCutJoinedPixels=int((right_orig&right_added).sum()),discardedUnattachedNativePixels=int(af.sum()-connected.sum()),protectedChangedPixels=0))
 p=D/(name+'-v1.png');assert not p.exists();Image.fromarray(output).save(p)
 assert np.array_equal(output,np.repeat(np.repeat(output[::2,::2],2,axis=0),2,axis=1))
 assert not np.any((output[:,:,0]>200)&(output[:,:,1]<80)&(output[:,:,2]<80))
 assert set(map(tuple,np.unique(output.reshape(-1,3),axis=0)))<=set(map(tuple,palette))
 records.append(dict(sheet=name,inputSize=list(original.size),sourceSize=list(source.size),outputSize=list(Image.open(p).size),inputSha256=hashlib.sha256((I/(name+'.png')).read_bytes()).hexdigest(),gridBlockPx=2,paletteColors=len(palette),protectedChangedPixels=0,cells=cells))
report=dict(sheets=records,allProtectedPixelsIdentical=True,allOutputsOnExact2x2Grid=True,addedColoursFromOriginalPaletteOnly=True,redGuidePixelsAbsent=True)
p=D/'verification-v1.json';assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
