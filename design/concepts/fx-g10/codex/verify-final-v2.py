from pathlib import Path
from PIL import Image
import numpy as np,json
D=Path(__file__).parent;records=[]
for name in ['fire','ice','poison','lightning','explosion']:
 im=Image.open(D/(name+'-v2.png'));assert im.size==(1024,256) and im.format=='PNG'
 a=np.array(im.convert('RGB'));n=a[::4,::4]
 assert np.array_equal(a,np.repeat(np.repeat(n,4,0),4,1))
 colors=np.unique(n.reshape(-1,3),axis=0);assert len(colors)<=5
 assert (0,0,0) in map(tuple,colors) and (122,60,255) not in map(tuple,colors)
 for i in range(4):
  c=n[:,i*64:(i+1)*64];assert not np.any(c[:3]) and not np.any(c[-3:]) and not np.any(c[:,:3]) and not np.any(c[:,-3:])
 areas=[int(np.any(n[:,i*64:(i+1)*64]>0,axis=2).sum()) for i in range(4)]
 assert areas[3]<areas[1] and areas[0]>0
 records.append(dict(effect=name,size=list(im.size),gridPassed=True,blackCellGuttersPassed=True,colors=len(colors),phasePixelAreas=areas))
line=Image.open(D/'lineup-v2.png');assert line.size==(1024,1280)
files=[]
for p in sorted(D.glob('*.png')):
 with Image.open(p) as im:files.append(dict(file=p.name,size=list(im.size),format=im.format))
for name,data in [('verification-final-v2.json',records),('files-v2.json',files)]:
 p=D/name;assert not p.exists();p.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(dict(checks=records,files=files),indent=2))
