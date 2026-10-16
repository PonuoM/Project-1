from pathlib import Path
from PIL import Image
import json,numpy as np
D=Path(__file__).parent;records=json.loads((D/'effects-v2.json').read_text());report=[]
for r in records:
 name=r['effect'];sheet=Image.open(D/r['sheet']).convert('RGB');a=np.array(sheet);n=a[::4,::4]
 assert np.array_equal(a,np.repeat(np.repeat(n,4,0),4,1))
 assert len(np.unique(n.reshape(-1,3),axis=0))<=5
 assert len(r['frames'])==r['frameCount']
 areas=[f['pixelArea'] for f in r['frames']];assert max(areas)>areas[0] and areas[-1]<=3
 for i in range(r['frameCount']):
  c=n[(i//4)*64:(i//4+1)*64,(i%4)*64:(i%4+1)*64]
  assert not np.any(c[:3]) and not np.any(c[-3:]) and not np.any(c[:,:3]) and not np.any(c[:,-3:])
 apng=Image.open(D/(name+'-preview-v2.png'));duration=0
 for i in range(apng.n_frames):apng.seek(i);duration+=apng.info['duration']
 assert abs(duration-r['totalEffectMs']-500)<1
 target=Image.open(D/(name+'-on-target-v2.png'));p=D/(name+'-on-target-still-v2.png');assert not p.exists();target.convert('RGB').save(p)
 # Contact strip: start, initial impact, peak, breakup, late, final.
 picks=[0,2,r['peakFrame'],r['frameCount']//2,r['frameCount']-3,r['frameCount']-1]
 strip=Image.new('RGB',(1152,96))
 for j,i in enumerate(picks):target.seek(i);strip.paste(target.convert('RGB').resize((192,96),Image.Resampling.NEAREST),(j*192,0))
 p=D/(name+'-contact-v2.png');assert not p.exists();strip.save(p)
 report.append(dict(effect=name,sheetSize=list(sheet.size),frameCount=r['frameCount'],effectMs=r['totalEffectMs'],previewMs=duration,storedApngFrames=apng.n_frames,distinctFrameAreas=areas,exactGrid=True,blackGutters=True))
files=[]
for p in sorted(D.glob('*.png')):
 with Image.open(p) as im:files.append(dict(file=p.name,size=list(im.size),frames=getattr(im,'n_frames',1)))
for name,data in [('verification-v2.json',report),('files-v2.json',files)]:
 p=D/name;assert not p.exists();p.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(report,indent=2))
