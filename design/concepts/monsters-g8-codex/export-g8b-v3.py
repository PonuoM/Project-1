"""Export generated low-resolution designs to exact native grids, preserving sources.
Colour-aware chroma classification protects bright green Thornboar vines.
Refuses to overwrite any export. Bosses are opened read-only.
"""
from pathlib import Path
from PIL import Image
import numpy as np
import json, hashlib

D=Path(__file__).parent
BG=(0,177,64); OUT=(46,24,22)
spec=json.loads((D/'prompts-g8b-v3.json').read_text(encoding='utf-8'))

def rgb(h): return tuple(bytes.fromhex(h[1:]))
def save(im,name):
 p=D/name
 assert not p.exists(),str(p)
 im.save(p)

def bbox(im):
 a=np.asarray(im)
 yy,xx=np.where(np.any(a!=BG,axis=2))
 return (int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1)

records=[]; figures=[]
for s in spec:
 name=s['id']; src=Image.open(D/(name+'-raw-v3.png')).convert('RGB')
 colors=[BG,OUT]+[rgb(h) for ramp in s['palette'].values() for h in ramp]
 assert len(colors)==12
 a=np.asarray(src).astype('float32')
 bgdist=np.sum((a-np.array(BG))**2,axis=2)
 other=np.full(a.shape[:2],np.inf)
 for c in colors[1:]: other=np.minimum(other,np.sum((a-np.array(c))**2,axis=2))
 # The exact nearest permitted class separates chroma from bright vine greens.
 m=Image.fromarray(np.where(bgdist<other,0,255).astype('uint8'))
 box=m.getbbox(); assert box
 cut=src.crop(box); m=m.crop(box)
 n=s['canvas']//8; h=s['height']; w=round(cut.width*h/cut.height)
 if name=='thornboar':w=40
 assert w<=n-4,(name,w,n)
 cut=cut.resize((w,h),Image.Resampling.NEAREST)
 m=m.resize((w,h),Image.Resampling.BOX).point(lambda v:255 if v else 0)
 small=np.asarray(cut).astype('float32')
 # Only content colours are allowed inside the foreground silhouette.
 pal=np.array(colors[1:])
 nearest=np.argmin(np.sum((small[:,:,None,:]-pal[None,None,:,:])**2,axis=3),axis=2)
 native=Image.new('RGB',(n,n),BG); ox=(n-w)//2; oy=n-2-h
 for y in range(h):
  for x in range(w):
   if not m.getpixel((x,y)):continue
   edge=any(i<0 or j<0 or i>=w or j>=h or not m.getpixel((i,j)) for i,j in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
   native.putpixel((ox+x,oy+y),OUT if edge else tuple(int(k) for k in pal[nearest[y,x]]))
 bounds=bbox(native)
 assert bounds[0]>=2 and bounds[1]>=2 and bounds[2]<=n-2 and bounds[3]==n-2,(name,bounds)
 assert bounds[3]-bounds[1]==h,(name,bounds,h)
 out=native.resize((n*8,n*8),Image.Resampling.NEAREST)
 save(out,name+'-v3.png')
 used=set(native.getdata()); assert len(used)<=12 and (122,60,255) not in used
 aa=np.asarray(out)
 assert np.all(aa==np.repeat(np.repeat(aa[::8,::8],8,axis=0),8,axis=1))
 eye=np.all(np.asarray(native)==rgb(s['palette']['eye'][0]),axis=2)
 eyesquares=int(np.sum(eye[:-1,:-1]&eye[1:,:-1]&eye[:-1,1:]&eye[1:,1:]))
 records.append(dict(id=name,file=name+'-v3.png',sourceSize=list(src.size),size=list(out.size),heightArtPx=h,widthArtPx=bounds[2]-bounds[0],boundsArtPx=list(bounds),groundRow=n-3,colorCount=len(used),eye2x2Squares=eyesquares,palette=s['palette']))
 figures.append(native.crop(bounds))

hero=Image.open(D.parents[1]/'pixellab/chibi-motion/hero-ref-64.png').convert('RGBA')
hero=hero.crop(hero.getchannel('A').getbbox())
hc=Image.new('RGBA',hero.size,BG+(255,));hc.alpha_composite(hero); hero=hc.convert('RGB')
bossfile=D/'grimfang-v2.png'; bossHash=hashlib.sha256(bossfile.read_bytes()).hexdigest()
boss=Image.open(bossfile).convert('RGB').resize((128,128),Image.Resampling.NEAREST); boss=boss.crop(bbox(boss))
allfig=[hero]+figures+[boss]
gap=8; margin=4; height=max(im.height for im in allfig)+4+2
width=sum(im.width for im in allfig)+gap*(len(allfig)-1)+2*margin
line=Image.new('RGB',(width,height),BG); x=margin
for im in allfig:
 line.paste(im,(x,height-2-im.height));x+=im.width+gap
save(line,'lineup-1x-v3.png');save(line.resize((width*8,height*8),Image.Resampling.NEAREST),'lineup-v3.png')
silwidth=sum(im.width for im in figures)+gap*3+margin*2
silheight=max(im.height for im in figures)+margin+2
sil=Image.new('RGB',(silwidth,silheight),BG);x=margin
for im in figures:
 a=np.asarray(im); black=Image.fromarray(np.where(np.any(a!=BG,axis=2)[:,:,None],np.array([0,0,0]),np.array(BG)).astype('uint8'))
 sil.paste(black,(x,silheight-2-im.height));x+=im.width+gap
save(sil,'silhouettes-1x-v3.png');save(sil.resize((silwidth*8,silheight*8),Image.Resampling.NEAREST),'silhouettes-v3.png')
report=dict(gridBlockPx=8,background='#00B140',outline='#2e1816',lineupNativeSize=list(line.size),lineupSize=[width*8,height*8],silhouetteNativeSize=list(sil.size),bossSha256=bossHash,monsters=records)
p=D/'verification-g8b-v3.json';assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
