"""Validate the engine-facing sprite contract and write a concise QA report."""
import json,hashlib
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
t=json.loads((ROOT/'tokens.json').read_text(encoding='utf-8'))
m=json.loads((ROOT/'sprites/manifest.json').read_text(encoding='utf-8'))
assert m['version']==t['version']==1
expected={}
def spec(key,n,fps,loop,size=32,impact=None,height=None):expected[key]=(n,fps,loop,size,impact,height or size)
for cls in ('melee','mage','ranged'):
    for a,n,fps,loop,hit in [('idle',4,6,True,None),('walk',6,10,True,None),('attack',6,14,False,3),('hurt',2,10,False,None),('death',5,8,False,None)]:spec(f'hero_{cls}_{a}',n,fps,loop,impact=hit)
for entity in ('slime','goblin','skeleton'):
    for a,n,fps,loop,hit in [('idle',4,6,True,None),('walk',6,10,True,None),('attack',4,10,False,2),('death',5,10,False,None)]:spec(f'{entity}_{a}',n,fps,loop,impact=hit)
for mat,a,n,fps,loop in [('wood','idle',1,0,False),('wood','open',5,12,False),('gold','locked',4,6,True),('gold','ready',4,8,True),('gold','open',6,12,False)]:spec(f'box_{mat}_{a}',n,fps,loop)
for k in ('box_wood','box_gold','coin','power','stage','expand','close','settings','weapon','armor','ring'):spec('icon_'+k,1,0,False,16)
spec('coin_spin',6,12,True,16);spec('fx_hit',4,16,False);spec('fx_levelup',6,12,False);spec('fx_arrow',2,12,True,16)
for entity in ('wolf','spider','ghost'):
    for a,n,fps,loop,hit in [('idle',4,6,True,None),('walk',6,10,True,None),('attack',4,10,False,2),('death',5,10,False,None)]:spec(f'{entity}_{a}',n,fps,loop,impact=hit)
for entity in ('boss_kingslime','boss_treant','boss_lich'):
    for a,n,fps,loop,hit in [('idle',4,6,True,None),('walk',6,8,True,None),('attack',6,10,False,3),('death',8,10,False,None)]:spec(f'{entity}_{a}',n,fps,loop,48,hit)
for region in ('grassland','darkforest','crypt'):spec('ground_'+region,1,0,False,64,height=8)
assert set(m['sheets'])==set(expected),'Missing/unexpected sprite keys'
assert {p.stem for p in (ROOT/'sprites').glob('*.png')}==set(expected)
palette={tuple(bytes.fromhex(v[1:])) for v in t['palette'].values()}
assert 24<=len(palette)<=32
results=[]
for key,s in m['sheets'].items():
    n,fps,loop,size,hit,height=expected[key]
    assert (s['frames'],s['fps'],s['loop'],s['frameWidth'],s['frameHeight'])==(n,fps,loop,size,height),key
    assert s.get('events',{}).get('impact')==hit,key
    im=Image.open(ROOT/'sprites'/s['file']);assert im.mode=='RGBA' and im.size==(size*n,height),key
    pixels=list(im.get_flattened_data());opaque={c[:3] for c in pixels if c[3]}
    assert opaque<=palette and {c[3] for c in pixels}<={0,255},key
    maxcolors=18 if key.startswith('hero_') else 10 if key.startswith(('slime_','goblin_','skeleton_')) else 8 if key.startswith('icon_') else 6 if key.startswith('fx_') else 10
    assert len(opaque)<=maxcolors,(key,len(opaque))
    distinct=len({im.crop((i*size,0,(i+1)*size,height)).tobytes() for i in range(n)})
    assert n==1 or distinct>1,('Static animation',key)
    if key.startswith('hero_') and not key.endswith('death'):
        assert all(any(im.getpixel((i*size+x,size-1))[3] for x in range(size)) for i in range(n)),('Baseline',key)
    if key.startswith(('wolf_','spider_','boss_')) and not key.endswith('death'):
        assert all(any(im.getpixel((i*size+x,height-1))[3] for x in range(size)) for i in range(n)),('Region baseline',key)
    if key.startswith('ghost_'):
        assert all(any(im.getpixel((i*size+x,y))[3] for y in range(height-4,height) for x in range(size)) for i in range(n)),('Ghost floating baseline',key)
    if key.startswith('ground_'):
        assert all(im.getpixel((0,y))==im.getpixel((size-1,y)) for y in range(height)),('Ground seam',key)
    results.append({'key':key,'frames':n,'uniqueFrames':distinct,'colors':len(opaque)})
im=Image.open(ROOT/'palette.png');assert im.size==(len(palette)*16,16)
for i,c in enumerate(t['palette'].values()):assert set(im.crop((i*16,0,i*16+16,16)).get_flattened_data())=={tuple(bytes.fromhex(c[1:]))}
baseline=json.loads((ROOT/'qa/prompt56_before.json').read_text())
for key,s in baseline['manifest']['sheets'].items():
    assert m['sheets'][key]==s,('Existing entry changed',key)
    assert hashlib.sha256((ROOT/'sprites'/s['file']).read_bytes()).hexdigest()==baseline['hashes'][s['file']],('Existing PNG changed',key)
regions=json.loads((ROOT/'regions.json').read_text(encoding='utf-8'))
for key,region in regions.items():
    assert region['ground']=='ground_'+key and region['ground'] in expected
    assert all(entity+'_idle' in expected for entity in region['monsters']+[region['boss']])
report={'result':'pass','sheets':len(results),'totalFrames':sum(x['frames'] for x in results),'paletteColors':len(palette),'preservedOriginalSheets':len(baseline['hashes']),'checks':['required keys','frame size/count','fps/loop/impact','RGBA binary alpha','palette membership','color budget','animated frame variation','floor/floating baseline','ground seams','region references','original PNG hashes and entries','palette swatch order'],'details':results}
(ROOT/'qa').mkdir(exist_ok=True)
(ROOT/'qa/assets.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f"PASS: {report['sheets']} sheets, {report['totalFrames']} frames, {report['paletteColors']} palette colors.")
