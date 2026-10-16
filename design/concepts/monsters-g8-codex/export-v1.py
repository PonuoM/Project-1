"""Mechanical sprite export: chroma key, native grid, palette lock, scale and lineup.
Does not generate replacement artwork. Original imagegen PNGs are retained.
Run once per version; refuses to overwrite outputs.
"""
from pathlib import Path
from PIL import Image
from collections import Counter
import json

D=Path(__file__).parent
BG=(0,177,64); OUT=(46,24,22)
RAMPS={
 'olive':['#50502b','#858344','#b6ad63'],
 'moss':['#35432b','#657445','#96a363'],
 'hide':['#49362c','#79503a','#aa7652'],
 'leather':['#4b3029','#80503b','#b27c51'],
 'cloth':['#542b27','#914437','#c16c4c'],
 'steel':['#42434a','#777a7b','#b0b5ad'],
 'bone':['#8e7a57','#c2b38e','#f0dfb6'],
 'fur':['#30303b','#515460','#81848a'],
 'red':['#641f2a','#a5323a','#df5050'],
 'straw':['#755b32','#ae8b48','#dfbc6b'],
 'sack':['#6c513a','#a08058','#d1b080'],
 'crow':['#25252e','#41434d','#626676'],
 'orange':['#ad3b18','#ec781c','#ffd05a'],
 'skin':['#66513f','#a17d57','#c9a875'],
 'bark':['#44332a','#70503b','#a17a4b'],
 'leaf':['#30492c','#567b3c','#91a44f'],
 'amber':['#a35c16','#e4a32a','#ffe067']}
MATERIALS={
 'kiki':['olive','hide','cloth','steel','bone','red'],
 'thornboar':['hide','moss','bone','amber'],
 'hex-scarecrow':['sack','cloth','straw','crow','orange'],
 'bridge-troll':['moss','steel','leather','bark','bone','amber'],
 'grimfang':['fur','red','bone'],
 'thunderhead':['skin','leather','steel','bark','leaf','bone','amber']}

def save_new(im,name):
 p=D/name
 assert not p.exists(),str(p)
 im.save(p)

records=[]; natives=[]
for s in json.loads((D/'prompts-v1.json').read_text(encoding='utf-8')):
 name=s['id']; src=Image.open(D/(name+'-raw-v1.png')).convert('RGB')
 # Key generated saturated greens; olive/moss body ramps are substantially less saturated.
 def green(c):
  r,g,b=c
  return g>110 and g>r*1.65 and g>b*1.5
 mask=Image.new('L',src.size)
 mask.putdata([0 if green(c) else 255 for c in src.getdata()])
 box=mask.getbbox(); assert box
 cut=src.crop(box); m=mask.crop(box)
 n=s['canvas']//8; h=s['height']; w=round(cut.width*h/cut.height)
 if name=='thornboar': w=40
 assert w<=n-4,(name,w,n)
 cut=cut.resize((w,h),Image.Resampling.NEAREST)
 m=m.resize((w,h),Image.Resampling.NEAREST)
 palette=[OUT]+[tuple(bytes.fromhex(v[1:])) for material in MATERIALS[name] for v in RAMPS[material]]
 native=Image.new('RGB',(n,n),BG); ox=(n-w)//2; oy=n-2-h
 for y in range(h):
  for x in range(w):
   if not m.getpixel((x,y)): continue
   c=cut.getpixel((x,y))
   edge=any(a<0 or b<0 or a>=w or b>=h or not m.getpixel((a,b)) for a,b in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
   v=OUT if edge else min(palette,key=lambda p:sum((p[k]-c[k])**2 for k in range(3)))
   native.putpixel((ox+x,oy+y),v)
 out=native.resize((s['canvas'],s['canvas']),Image.Resampling.NEAREST)
 save_new(out,name+'-v1.png')
 fm=Image.new('L',native.size); fm.putdata([0 if c==BG else 255 for c in native.getdata()]); bounds=fm.getbbox()
 assert bounds[1]>=2 and bounds[0]>=2 and bounds[2]<=n-2 and bounds[3]==n-2,(name,bounds)
 assert bounds[3]-bounds[1]==h
 assert (122,60,255) not in set(out.getdata())
 assert all(len(set(out.crop((x,y,x+8,y+8)).getdata()))==1 for y in range(0,out.height,8) for x in range(0,out.width,8))
 records.append(dict(id=name,file=name+'-v1.png',sourceSize=list(src.size),size=list(out.size),heightArtPx=h,widthArtPx=bounds[2]-bounds[0],boundsArtPx=bounds,groundRow=n-3,materials={k:RAMPS[k] for k in MATERIALS[name]},colorsUsed=dict(Counter('#%02x%02x%02x'%c for c in native.getdata()))))
 natives.append(native.crop(bounds))

# Hero retains all original RGB/RGBA art; alpha is composited onto the requested green.
hero=Image.open(D.parents[1]/'pixellab/chibi-motion/hero-ref-64.png').convert('RGBA')
hm=hero.getchannel('A'); hb=hm.getbbox(); hero=hero.crop(hb)
hc=Image.new('RGBA',hero.size,BG+(255,)); hc.alpha_composite(hero); hero=hc.convert('RGB')
figs=[hero]+natives; gap=8; margin=4; height=max(im.height for im in figs)+margin+2
width=sum(im.width for im in figs)+gap*(len(figs)-1)+2*margin
line=Image.new('RGB',(width,height),BG); x=margin
for im in figs:
 line.paste(im,(x,height-2-im.height)); x+=im.width+gap
save_new(line.resize((width*8,height*8),Image.Resampling.NEAREST),'lineup-v1.png')
report=dict(allChecksPassed=True,gridBlockPx=8,background='#00B140',outline='#2e1816',lineupSize=[width*8,height*8],lineupOrder=['hero']+[r['id'] for r in records],heroHeightArtPx=hero.height,monsters=records)
p=D/'verification-v1.json'; assert not p.exists(); p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='monsters'}))
for r in records: print(r['id'],r['size'],r['heightArtPx'],r['widthArtPx'])
