from PIL import Image
from pathlib import Path
import json, math
D=Path(__file__).parent
src=Image.open(D/'blades-raw-v1.png').convert('RGB')
BG=(0,177,64); O=(46,24,22)
spec=[
('worn iron','common',13,3,['#534b49','#827a71','#b6afa0']),
('fullered steel','uncommon',14,3,['#465465','#8c98a8','#c4cfde']),
('sky-port sabre','rare',15,4,['#5d6775','#8c98a8','#c4cfde','#8c6224','#c49238','#e8be5a']),
('broad cleaver','rare',14,4,['#465465','#8c98a8','#c4cfde']),
('frost crystal','epic',15,4,['#398a9c','#80ccdc','#d5f6ff']),
('storm blade','epic',15,4,['#465465','#8c98a8','#c4cfde','#1859aa','#268ee8','#79d5ff']),
('ember blade','legendary',16,4,['#302e36','#4d4851','#6c6266','#b6431a','#ed7823','#ffc453']),
('captains gilded blade','legendary',16,4,['#8d9eaf','#cbd9e5','#f1f7ff','#8c6224','#c49238','#e8be5a'])]
native=Image.new('RGB',(128,64),BG); records=[]
def fg(c):
 r,g,b=c
 return not (g>r*1.4 and g>b*1.3)
for i,(name,tier,w,h,hexes) in enumerate(spec):
 col,row=i%4,i//4
 cell=src.crop((round(col*src.width/4),round(row*src.height/2),round((col+1)*src.width/4),round((row+1)*src.height/2)))
 mask=Image.new('L',cell.size); mask.putdata([255 if fg(c) else 0 for c in cell.getdata()])
 box=mask.getbbox(); blade=cell.crop(box); mask=mask.crop(box)
 small=blade.resize((w,h),Image.Resampling.NEAREST)
 sm=mask.resize((w,h),Image.Resampling.NEAREST)
 # Keep the generated profile and make every occupied silhouette boundary one native pixel.
 colors=[tuple(bytes.fromhex(s[1:])) for s in hexes]
 ox=col*32+4; oy=row*32+15
 for y in range(h):
  for x in range(w):
   if not sm.getpixel((x,y)): continue
   boundary=any(nx<0 or nx>=w or ny<0 or ny>=h or not sm.getpixel((nx,ny)) for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
   color=O if boundary else min(colors,key=lambda p:sum((p[k]-small.getpixel((x,y))[k])**2 for k in range(3)))
   native.putpixel((ox+x,oy+y),color)
 # Exact base attachment pixel.
 native.putpixel((ox,row*32+16),O)
 points=[(x,y) for y in range(32) for x in range(32) if native.getpixel((col*32+x,row*32+y))!=BG]
 bounds=[min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points)+1,max(p[1] for p in points)+1]
 records.append(dict(cell=i+1,name=name,tier=tier,lengthPx=bounds[2]-bounds[0],widthPx=bounds[3]-bounds[1],basePx=[4,16],boundsPx=bounds,palette=hexes))
native.resize((1024,512),Image.Resampling.NEAREST).save(D/'blades-v1.png')
(D/'blades.json').write_text(json.dumps(records,indent=2)+'\n')
# Independent file-level checks of saved output.
im=Image.open(D/'blades-v1.png').convert('RGB')
assert im.size==(1024,512)
for y in range(0,512,8):
 for x in range(0,1024,8):
  assert len(set(im.crop((x,y,x+8,y+8)).getdata()))==1
assert (122,60,255) not in set(im.getdata())
for r in records:
 assert 12<=r['lengthPx']<=16 and 2<=r['widthPx']<=4
 assert r['boundsPx'][0]==4 and r['boundsPx'][2]<32 and r['boundsPx'][3]<32
report={'sourceSize':list(src.size),'savedSize':list(im.size),'gridBlockPx':8,'background':'#00B140','outline':'#2e1816','allChecksPassed':True,'blades':records}
(D/'verification-v1.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
