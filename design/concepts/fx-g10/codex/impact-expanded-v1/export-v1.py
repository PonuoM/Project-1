"""Mechanical sprite-sheet export, metadata and animated previews from generated frames."""
from pathlib import Path
from PIL import Image,ImageChops
import numpy as np,json
D=Path(__file__).parent
spec=json.loads((D/'prompts-v1.json').read_text())
def save(name,im,**kw):
 p=D/name;assert not p.exists();im.save(p,**kw)
def keygreen(im):
 a=np.array(im.convert('RGBA'));m=(a[:,:,1]>a[:,:,0]*1.5)&(a[:,:,1]>a[:,:,2]*1.5);a[m,3]=0
 return Image.fromarray(a)
reference=Image.open(D.parents[1]/'ref/scale-hero-and-monster.png').convert('RGB').resize((128,64),Image.Resampling.NEAREST)
hero=keygreen(reference.crop((7,3,48,64)));foe=keygreen(reference.crop((77,22,117,62)))
records=[];peaks=[]
for s in spec:
 src=Image.open(D/(s['id']+'-raw-v1.png')).convert('RGB');rows=s['rows'];frames=[];fr=[]
 pal=np.array([(0,0,0)]+[tuple(bytes.fromhex(h[1:])) for h in s['palette']],dtype=np.int32)
 native=Image.new('RGB',(256,64*rows))
 for i in range(s['count']):
  col=i%4;row=i//4
  box=(round(col*src.width/4),round(row*src.height/rows),round((col+1)*src.width/4),round((row+1)*src.height/rows))
  im=src.crop(box).resize((64,64),Image.Resampling.NEAREST)
  a=np.array(im).astype(np.int32);idx=np.sum((a[:,:,None,:]-pal[None,None,:,:])**2,axis=3).argmin(axis=2);a=pal[idx].astype(np.uint8)
  a[:3]=0;a[-3:]=0;a[:,:3]=0;a[:,-3:]=0
  im=Image.fromarray(a);frames.append(im);native.paste(im,(col*64,row*64))
  yy,xx=np.where(np.any(a>0,axis=2))
  fr.append(dict(frame=i,sourceCell=i+1,durationMs=s['times'][i],boundsArtPx=[int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1] if len(xx) else None,pixelArea=int(len(xx))))
 sheet=native.resize((1024,rows*256),Image.Resampling.NEAREST);save(s['id']+'-v1.png',sheet)
 save(s['id']+'-native-v1.png',native)
 # Explicit black endpoint is a playback hold, not an invented in-between image.
 preview=[im.resize((256,256),Image.Resampling.NEAREST) for im in frames]+[Image.new('RGB',(256,256))]
 durations=s['times']+[500]
 save(s['id']+'-preview-v1.png',preview[0],save_all=True,append_images=preview[1:],duration=durations,loop=0,disposal=0,blend=0)
 scenes=[]
 for i,fx in enumerate(frames+[Image.new('RGB',(64,64))]):
  scene=Image.new('RGB',(192,96),'#181b28');scene.paste('#303448',(0,76,192,96));scene.paste('#4c5362',(0,76,192,77))
  scene.paste(hero,(25,76-hero.height),hero);scene.paste(foe,(96-foe.width//2,76-foe.height),foe)
  # Fixed torso hit target, FX native pivot32,32. Ground54 lands atscene y76.
  layer=Image.new('RGB',scene.size);layer.paste(fx,(96-32,54-32));scene=ImageChops.add(scene,layer)
  scenes.append(scene.resize((576,288),Image.Resampling.NEAREST))
 save(s['id']+'-on-target-v1.png',scenes[0],save_all=True,append_images=scenes[1:],duration=durations,loop=0,disposal=0,blend=0)
 peakidx=max(range(len(fr)),key=lambda i:fr[i]['pixelArea']);peaks.append(frames[peakidx])
 arr=np.array(sheet);assert np.array_equal(arr,np.repeat(np.repeat(arr[::4,::4],4,0),4,1))
 assert set(map(tuple,np.unique(arr.reshape(-1,3),axis=0)))<=set(map(tuple,pal))
 records.append(dict(effect=s['id'],sourceSize=list(src.size),sheet=s['id']+'-v1.png',size=list(sheet.size),frameCount=s['count'],cols=4,rows=rows,frameWidth=256,frameHeight=256,nativeFrameSize=[64,64],anchorArtPx=[32,32],anchorImagePx=[128,128],groundArtY=54,palette=['#000000']+s['palette'],totalEffectMs=sum(s['times']),previewBlackHoldMs=500,peakFrame=peakidx,frames=fr))
line=Image.new('RGB',(256,64))
for i,im in enumerate(peaks):line.paste(im,(i*64,0))
save('impact-peaks-v1.png',line.resize((1024,256),Image.Resampling.NEAREST));save('impact-peaks-1x-v1.png',line)
p=D/'effects-v1.json';assert not p.exists();p.write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps([dict(effect=r['effect'],size=r['size'],frameCount=r['frameCount'],totalEffectMs=r['totalEffectMs'],areas=[f['pixelArea'] for f in r['frames']]) for r in records],indent=2))
