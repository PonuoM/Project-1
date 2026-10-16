from PIL import Image
from pathlib import Path
import json
D=Path(__file__).parent
BG='#00B140'; O='#2e1816'
records=json.loads((D/'blades.json').read_text())
# Native-pixel reconstruction of the generated design motifs.
patterns=[
['oooooooooooo.','o12322123213o','oooooo.ooooo.'],
['ooooooooooooo.','o211111122223o','ooooooooooooo.'],
['...........oooo','oooooooooooa23o','o12222222233oo.','.oooooooooooo..'],
['.......ooooooo','ooooooo122223o','o12222333333o.','.ooooooooooo..'],
['...ooo...ooo...','ooo233ooo233oo.','o1232212332213o','.ooooooooooooo.'],
['...oo..oo..oo..','ooo23oo23oo233o','o12b22b22b223o.','.oo..oo..oooo..'],
['..ooo...ooo..ooo','oo112ooo1b2oo23o','o1b2b1bb2cb2b3o.','.ooo.oooo..ooo..'],
['............oooo','ooooooooooooa23o','o23333b33bca33o.','.ooooooooooooo..']
]
im=Image.new('RGB',(128,64),BG)
for i,(r,rows) in enumerate(zip(records,patterns)):
 w=max(map(len,rows)); ox=i%4*32+4; oy=i//4*32+15
 colors={'o':O,'.':BG}
 colors.update(dict(zip('123abc',r['palette'])))
 for y,line in enumerate(rows):
  for x,s in enumerate(line):
   im.putpixel((ox+x,oy+y),tuple(bytes.fromhex(colors[s][1:])))
 points=[(x,y) for y in range(32) for x in range(32) if im.getpixel((i%4*32+x,i//4*32+y))!=Image.new('RGB',(1,1),BG).getpixel((0,0))]
 box=[min(x for x,y in points),min(y for x,y in points),max(x for x,y in points)+1,max(y for x,y in points)+1]
 r.update(lengthPx=box[2]-box[0],widthPx=box[3]-box[1],boundsPx=box)
 assert r['lengthPx']<=16 and r['lengthPx']>=12 and r['widthPx']<=4
 assert im.getpixel((ox,i//4*32+16))==Image.new('RGB',(1,1),O).getpixel((0,0))
im.resize((1024,512),Image.Resampling.NEAREST).save(D/'blades-v2.png')
(D/'blades-v2.json').write_text(json.dumps(records,indent=2)+'\n')
out=Image.open(D/'blades-v2.png')
assert out.size==(1024,512)
for y in range(0,512,8):
 for x in range(0,1024,8):
  assert len(set(out.crop((x,y,x+8,y+8)).getdata()))==1
assert (122,60,255) not in set(out.getdata())
(D/'verification-v2.json').write_text(json.dumps({'allChecksPassed':True,'size':list(out.size),'blockPx':8,'basePx':[4,16],'blades':records},indent=2)+'\n')
print(json.dumps(records))
