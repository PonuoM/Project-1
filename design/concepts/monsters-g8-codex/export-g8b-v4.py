"""Export only the two eye retries; compose mixed final lineup non-destructively."""
from pathlib import Path
import json
p=Path(__file__).parent
code=(p/'export-g8b-v3.py').read_text(encoding='utf-8').split('\nhero=')[0]
code=code.replace("for s in spec:","for s in [q for q in spec if q['id'] in ['thornboar','hex-scarecrow']]:")
code=code.replace("name+'-raw-v3.png'","name+'-raw-v4.png'")
code=code.replace("name+'-v3.png'","name+'-v4.png'")
exec(compile(code,str(p/'export-g8b-v3.py'),'exec'))

assert all(m['eye2x2Squares']>0 for m in records),records
old=json.loads((D/'verification-g8b-v3.json').read_text())
updated={m['id']:m for m in records}
mixed=[updated.get(m['id'],m) for m in old['monsters']]
figures=[]
for m in mixed:
 im=Image.open(D/m['file']).convert('RGB')
 im=im.resize((im.width//8,im.height//8),Image.Resampling.NEAREST)
 figures.append(im.crop(bbox(im)))

hero=Image.open(D.parents[1]/'pixellab/chibi-motion/hero-ref-64.png').convert('RGBA')
hero=hero.crop(hero.getchannel('A').getbbox());hc=Image.new('RGBA',hero.size,BG+(255,));hc.alpha_composite(hero);hero=hc.convert('RGB')
bossfile=D/'grimfang-v2.png';bossHash=hashlib.sha256(bossfile.read_bytes()).hexdigest()
assert bossHash==old['bossSha256']
boss=Image.open(bossfile).convert('RGB').resize((128,128),Image.Resampling.NEAREST);boss=boss.crop(bbox(boss))
allfig=[hero]+figures+[boss];gap=8;margin=4
height=max(im.height for im in allfig)+6;width=sum(im.width for im in allfig)+gap*5+margin*2
line=Image.new('RGB',(width,height),BG);x=margin
for im in allfig:line.paste(im,(x,height-2-im.height));x+=im.width+gap
save(line,'lineup-1x-v4.png');save(line.resize((width*8,height*8),Image.Resampling.NEAREST),'lineup-v4.png')
sw=sum(im.width for im in figures)+gap*3+margin*2;sh=max(im.height for im in figures)+6
sil=Image.new('RGB',(sw,sh),BG);x=margin
for im in figures:
 a=np.asarray(im);black=Image.fromarray(np.where(np.any(a!=BG,axis=2)[:,:,None],np.array([0,0,0]),np.array(BG)).astype('uint8'))
 sil.paste(black,(x,sh-2-im.height));x+=im.width+gap
save(sil,'silhouettes-1x-v4.png');save(sil.resize((sw*8,sh*8),Image.Resampling.NEAREST),'silhouettes-v4.png')
report=dict(gridBlockPx=8,background='#00B140',outline='#2e1816',lineupNativeSize=list(line.size),lineupSize=[width*8,height*8],silhouetteNativeSize=list(sil.size),bossSha256=bossHash,monsters=mixed)
path=D/'verification-g8b-v4.json';assert not path.exists();path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
