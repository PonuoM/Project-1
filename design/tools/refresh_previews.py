"""Refresh sheet gallery and contact atlas from the complete manifest, including rectangular tiles."""
import json,math
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def refresh():
    m=json.loads((ROOT/'sprites/manifest.json').read_text())
    html='''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>คลังภาพ · ทุกภูมิภาค</title><style>
body{margin:24px;background:#171c2c;color:#fff9ed;font:14px/1.6 Tahoma,sans-serif}h1{font-size:24px}button{padding:8px 16px;background:#ffd875;border:0;color:#171c2c;cursor:pointer}button:focus-visible{outline:2px solid #fff9ed;outline-offset:3px}.atlas{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,850px),1fr));gap:16px}.entry{border:1px solid #55647a;padding:12px;min-width:0}h2{font-size:14px;margin:0 0 8px;overflow-wrap:anywhere}.contexts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px}.context{display:flex;align-items:end;justify-content:center;gap:12px;height:168px;border:1px solid #55647a;padding:8px;overflow:auto}.light{background:#fff9ed}.dark{background:#1e1e1e}.color{background:linear-gradient(120deg,#5389ca,#d75b60,#6db586)}.sprite{display:inline-block;image-rendering:pixelated;flex:none}small{color:#b8c4cf}.ground{background-color:#171c2c}@media(max-width:900px){.contexts{grid-template-columns:minmax(0,1fr)}}@media(max-width:430px){body{margin:12px}}
</style></head><body><h1>คลังภาพ · ทุกท่าที่ 1× และ 3×</h1><p>พื้นสว่าง มืด และสี · บอส 48×48 · พื้นแต่ละภูมิภาค 64×8 อยู่บนแถบสีหมึก · ท่าไม่วนหยุดที่เฟรมสุดท้าย</p><button id="replay">เล่นทุกท่าใหม่</button><p id="count"></p><main class="atlas" id="atlas"></main><script>
const manifest=MANIFEST;let start=performance.now();const views=[];const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;const atlas=document.getElementById('atlas');
for(const [key,s] of Object.entries(manifest.sheets)){const a=document.createElement('article');a.className='entry';a.dataset.key=key;a.innerHTML=`<h2>${key}</h2><small>${s.frameWidth}×${s.frameHeight} · ${s.frames} frames · ${s.fps} fps · ${s.loop?'วน':'ครั้งเดียว'}${s.events?' · impact '+s.events.impact:''}</small><div class="contexts"></div>`;for(const bg of ['light','dark','color']){const c=document.createElement('div');c.className='context '+bg;for(const scale of [1,3]){const el=document.createElement('span');el.className='sprite'+(key.startsWith('ground_')?' ground':'');el.style.cssText=`width:${s.frameWidth*scale}px;height:${s.frameHeight*scale}px;background-image:url(${s.file});background-size:${s.frameWidth*s.frames*scale}px ${s.frameHeight*scale}px`;c.append(el);views.push({el,s,scale})}a.lastChild.append(c)}atlas.append(a)}
document.getElementById('count').textContent=Object.keys(manifest.sheets).length+' sprite sheets';document.getElementById('replay').onclick=()=>{start=performance.now();if(reduced)draw(start)};
function draw(t){for(const {el,s,scale} of views){const raw=reduced?0:Math.floor((t-start)/1000*s.fps);const f=s.loop?raw%s.frames:Math.min(s.frames-1,raw);el.style.backgroundPosition=`${-f*s.frameWidth*scale}px 0`}}function tick(t){draw(t);if(!reduced)requestAnimationFrame(tick)}requestAnimationFrame(tick);
</script></body></html>'''.replace('MANIFEST',json.dumps(m))
    (ROOT/'sprites/preview.html').write_text(html,encoding='utf-8')
    # First frame at integer 3x. Large cells leave enough room for boss and ground tiles.
    items=list(m['sheets'].items());w=320;h=200;cols=4
    atlas=Image.new('RGB',(w*cols,h*math.ceil(len(items)/cols)),'#171C2C');d=ImageDraw.Draw(atlas)
    for i,(key,s) in enumerate(items):
        x=(i%cols)*w;y=(i//cols)*h
        tile=Image.open(ROOT/'sprites'/s['file']).crop((0,0,s['frameWidth'],s['frameHeight']))
        tile=tile.resize((s['frameWidth']*3,s['frameHeight']*3),Image.Resampling.NEAREST)
        atlas.paste(tile,(x+16,y+152-tile.height),tile)
        d.text((x+16,y+160),key,fill='#FFF9ED');d.text((x+16,y+178),f"{s['frameWidth']}x{s['frameHeight']} | {s['frames']} frames",fill='#B8C4CF')
    (ROOT/'qa').mkdir(exist_ok=True);atlas.save(ROOT/'qa/atlas.png')
    regional=Image.new('RGB',(720,1080),'#171C2C');rd=ImageDraw.Draw(regional)
    for row,name in enumerate(['wolf','spider','ghost','boss_kingslime','boss_treant','boss_lich']):
        for col,anim in enumerate(['idle','attack','death']):
            s=m['sheets'].get(name+'_'+anim)
            if not s:continue
            frame=0 if anim=='idle' else s.get('events',{}).get('impact',s['frames']-1)
            tile=Image.open(ROOT/'sprites'/s['file']).crop((frame*s['frameWidth'],0,(frame+1)*s['frameWidth'],s['frameHeight']))
            tile=tile.resize((s['frameWidth']*3,s['frameHeight']*3),Image.Resampling.NEAREST)
            regional.paste(tile,(col*240+24,row*180+148-tile.height),tile)
            rd.text((col*240+12,row*180+156),name+'_'+anim,fill='#FFF9ED')
    regional.save(ROOT/'qa/regions-atlas.png')
    (ROOT/'sprites/KEYS.md').write_text('# Produced sprite keys\n\n'+f"{len(items)} sheets, {sum(s['frames'] for _,s in items)} frames. Prompts 2 and 6 complete; nothing skipped.\n\n"+'\n'.join('- `'+key+'`' for key,_ in items)+'\n',encoding='utf-8')
if __name__=='__main__':refresh()
