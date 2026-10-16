"""Original integer pixel art. Run from any cwd; writes only under design/. Requires Pillow."""
import json, math
from pathlib import Path
from PIL import Image, ImageDraw, PngImagePlugin

ROOT = Path(__file__).resolve().parents[1]
T = json.loads((ROOT / 'tokens.json').read_text(encoding='utf-8'))
P = T['palette']
OUT = ROOT / 'sprites'
OUT.mkdir(exist_ok=True)
SHEETS = {}

def canvas(n=32): return Image.new('RGBA', (n,n))
def rgb(k): return P[k]
def rect(im, xy, c): ImageDraw.Draw(im).rectangle(xy, fill=rgb(c))
def poly(im, xy, c): ImageDraw.Draw(im).polygon(xy, fill=rgb(c))
def line(im, xy, c, w=1): ImageDraw.Draw(im).line(xy, fill=rgb(c), width=w)
def ellipse(im, xy, c): ImageDraw.Draw(im).ellipse(xy, fill=rgb(c))
def outline(im):
    # Explicit one-pixel 8-neighbor silhouette, without partial alpha.
    src=im.copy(); px=src.load(); dst=im.load(); w,h=im.size
    for y in range(h):
        for x in range(w):
            if not px[x,y][3] and any(0<=x+dx<w and 0<=y+dy<h and px[x+dx,y+dy][3] for dx,dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)]):
                dst[x,y]=tuple(bytes.fromhex(P['outline'][1:]))+(255,)
    return im

# Hand-authored head grid. Each character is a palette lookup; no resampling.
HEAD = [
 '...ssssss...', '..slllllls..', '.sllllmmmms.', '.sllmmmmmmms', '.sllmkkkkmms', '..smkSSSkms.', '..kSSSLSkk..', '..kSSSkSSk..', '...kSSSSk...', '....kkkk....']
HEAD_COLORS={'s':'slate_dark','l':'silver','m':'slate_mid','k':'outline','S':'skin_mid','L':'skin_light'}
def stamp(im, rows, colors, x,y):
    for j,row in enumerate(rows):
        for i,v in enumerate(row):
            if v!='.': rect(im,(x+i,y+j,x+i,y+j),colors[v])

def hero(cls, anim, f):
    im=canvas(); walk=[0,1,2,0,-1,-2][f%6] if anim=='walk' else 0
    bob=(f%2) if anim in ('idle','walk') else 0
    if anim=='death':
        if f<2:
            base=hero(cls,'hurt',f); im.alpha_composite(base,(0,f*2)); return im
        rect(im,(7,27,22,30),'slate_mid'); rect(im,(8,27,15,28),'silver')
        rect(im,(20,25,25,29),'skin_mid'); rect(im,(21,25,24,26),'skin_light')
        rect(im,(4,29,8,30),'wood_dark'); rect(im,(24,30,29,30),'wood_dark'); return outline(im)
    cloth={'melee':'blue_dark','mage':'purple_dark','ranged':'green_dark'}[cls]
    light={'melee':'blue_mid','mage':'purple_mid','ranged':'green_mid'}[cls]
    y=5+bob; stamp(im,HEAD,HEAD_COLORS,10,y)
    # Eye faces right, visor and top-left steel rim.
    rect(im,(19,y+6,20,y+6),'ink')
    if cls=='mage':
        poly(im,[(9,y+3),(14,y-4),(19,y+3)],'purple_dark'); line(im,[(10,y+2),(18,y+2)],'purple_mid')
    elif cls=='ranged':
        poly(im,[(10,y+1),(13,y-2),(19,y),(21,y+3),(10,y+3)],'green_dark'); line(im,[(11,y),(17,y-1)],'green_mid')
    rect(im,(11,15+bob,20,25),'slate_dark'); rect(im,(12,16+bob,19,24),cloth)
    rect(im,(12,16+bob,14,23),light); rect(im,(11,15+bob,20,16+bob),'red_mid')
    rect(im,(8,16+bob,12,18+bob),'red_dark')
    rect(im,(11,24,20,25),'wood_dark'); rect(im,(15,24,16,25),'gold_mid')
    rect(im,(12+walk,26,15+walk,29),'slate_mid'); rect(im,(17-walk,26,20-walk,29),'slate_dark')
    rect(im,(11+walk,30,16+walk,30),'wood_dark'); rect(im,(16-walk,30,21-walk,30),'wood_dark')
    strike=anim=='attack'; reach=[0,-1,2,6,3,0][f%6] if strike else 0
    rect(im,(20,18+bob,23,20+bob),'skin_mid'); rect(im,(21,18+bob,23,18+bob),'skin_light')
    if cls=='melee':
        if strike and f in (2,3,4):
            line(im,[(22,19),(29,13)],'silver',2); line(im,[(23,18),(29,12)],'white'); line(im,[(22,17),(25,20)],'gold_mid')
            if f==3: line(im,[(27,7),(30,10),(30,17),(27,21)],'cream')
        else:
            rect(im,(24,11+bob,25,22+bob),'silver'); rect(im,(24,11+bob,24,18+bob),'white')
            rect(im,(22,22+bob,27,23+bob),'gold_mid'); rect(im,(24,24,25,26),'wood_mid')
        poly(im,[(8,18),(13,18),(14,24),(11,28),(8,25)],'wood_mid')
        line(im,[(8,18),(12,18),(13,23),(11,26)],'silver'); rect(im,(10,20,11,24),'gold_mid')
    elif cls=='mage':
        rect(im,(24,13-reach//2,25,29),'wood_mid'); rect(im,(23,12-reach//2,26,15-reach//2),'blue_light')
        rect(im,(24,12-reach//2,25,13-reach//2),'white')
        if strike and f==3: poly(im,[(28,10),(30,12),(28,14),(26,12)],'gold_light')
    else:
        line(im,[(24,13),(27,16),(28,22),(25,27)],'wood_light',2)
        draw=3 if strike and f in (1,2) else 0
        line(im,[(24,13),(24-draw,20),(25,27)],'cream')
        if strike and f<4:
            tip=[27,25,26,30][f]
            line(im,[(19-draw,20),(tip,20)],'silver'); rect(im,(tip-1,19,tip,21),'cream')
    if anim=='hurt':
        rect(im,(11,17+f,19,18+f),'red_light')
        if f==0: line(im,[(5,10),(3,8)],'red_light'); line(im,[(7,6),(6,3)],'red_light')
    return outline(im)

def monster(kind, anim, f):
    im=canvas(); bob=f%2 if anim in ('idle','walk') else 0
    if anim=='death':
        if f<2: return monster(kind,'idle',f)
        if kind=='slime':
            ellipse(im,(7,27+min(f-2,2),26,30),'green_dark'); line(im,[(9,29),(20,29)],'green_light')
        else:
            rect(im,(8,28,24,30),'cream' if kind=='skeleton' else 'green_mid'); rect(im,(9,28,13,28),'white' if kind=='skeleton' else 'green_light')
            rect(im,(4,29,6,30),'slate_light'); rect(im,(27,30,29,30),'wood_mid')
        return outline(im)
    if kind=='slime':
        top=18+bob-(2 if anim=='attack' and f==2 else 0)
        poly(im,[(6,29),(6,24),(9,top+2),(13,top),(21,top),(25,top+4),(27,28),(25,30),(8,30)],'green_mid')
        poly(im,[(7,27),(8,23),(11,top+2),(18,top+1),(15,top+4),(9,27)],'green_light')
        line(im,[(9,30),(25,30),(26,28)],'green_dark',2)
        rect(im,(10,24,11,25),'ink'); rect(im,(16,24,17,25),'ink'); rect(im,(12,28,15,28),'green_dark')
        if anim=='attack' and f==2: rect(im,(3,26,8,28),'green_mid')
    else:
        bone=kind=='skeleton'; c='cream' if bone else 'green_mid'; hi='white' if bone else 'green_light'
        if bone:
            rect(im,(11,7+bob,22,15+bob),c); rect(im,(12,7+bob,18,8+bob),hi)
            rect(im,(12,11+bob,14,13+bob),'ink'); rect(im,(18,11+bob,20,13+bob),'ink')
            rect(im,(14,16+bob,20,17+bob),'cream'); rect(im,(16,16+bob,16,17+bob),'ink')
            line(im,[(16,18),(16,25)],c,2)
            for yy in (19,21,23): line(im,[(12,yy),(21,yy)],c)
        else:
            poly(im,[(7,12+bob),(11,9+bob),(13,6+bob),(20,6+bob),(22,10+bob),(27,9+bob),(25,15+bob),(21,17+bob),(12,17+bob)],c)
            line(im,[(12,9+bob),(15,7+bob),(20,7+bob)],hi,2)
            rect(im,(12,12+bob,14,13+bob),'ink'); rect(im,(18,12+bob,20,13+bob),'ink')
            rect(im,(12,18,22,25),'wood_mid'); rect(im,(12,18,15,23),'wood_light'); rect(im,(11,25,23,26),'wood_dark')
        shift=[0,1,2,0,-1,-2][f%6] if anim=='walk' else 0
        line(im,[(14,26),(12+shift,30)],c,2); line(im,[(20,26),(22-shift,30)],c,2)
        reach=4 if anim=='attack' and f==2 else 0
        line(im,[(12,19),(9-reach,23)],c,2)
        line(im,[(8-reach,17),(8-reach,27)],'wood_mid',2)
        rect(im,(6-reach,15,10-reach,19),'slate_light'); rect(im,(6-reach,15,9-reach,16),'silver')
    return outline(im)

def sparkle(im,x,y,c='gold_glint'):
    line(im,[(x-2,y),(x+2,y)],c); line(im,[(x,y-2),(x,y+2)],c)

def box(material,anim,f):
    im=canvas(); gold=material=='gold'; dark='gold_dark' if gold else 'wood_dark'; mid='gold_mid' if gold else 'wood_mid'; light='gold_light' if gold else 'wood_light'
    rect(im,(6,20,25,30),dark); rect(im,(7,21,24,28),mid); rect(im,(8,21,23,22),light)
    for x in (8,22): rect(im,(x,20,x+1,30),light)
    rect(im,(8,29,23,30),dark)
    opening=anim=='open'; lift=[0,2,5,8,9,9][f] if opening else 0
    poly(im,[(6,19-lift),(8,14-lift),(23,14-lift),(25,19-lift)],mid)
    line(im,[(8,14-lift),(23,14-lift),(24,16-lift)],light,2); line(im,[(6,19-lift),(25,19-lift)],dark)
    rect(im,(8,16-lift,9,19-lift),light); rect(im,(22,16-lift,23,19-lift),light)
    if anim=='locked':
        line(im,[(14,20),(14,18),(17,18),(17,20)],'silver'); rect(im,(13,21,18,25),'outline'); rect(im,(14,21,17,24),'silver'); rect(im,(15,22,16,23),'ink')
        sparkle(im,22,15+f%3)
    else:
        rect(im,(14,19,17,22),'gold_mid'); rect(im,(15,19,16,20),'gold_glint')
    if anim=='ready' or opening and f>1:
        for x,y in [(3,17-f%2),(28,13+f%3),(16,6+f%2)]: sparkle(im,x,y)
    if opening and f>=2:
        poly(im,[(11,20),(12,13),(16,10),(20,13),(21,20)],'gold_light' if gold else 'cream')
        line(im,[(15,18),(15,12),(17,12)],'white')
    return outline(im)

def icon(key,f=0):
    im=canvas(16)
    if key in ('box_wood','box_gold'):
        dark,mid,light=('gold_dark','gold_mid','gold_light') if key=='box_gold' else ('wood_dark','wood_mid','wood_light')
        rect(im,(2,6,13,13),dark); rect(im,(3,7,12,12),mid); poly(im,[(2,5),(4,3),(11,3),(13,5)],mid)
        line(im,[(4,3),(11,3)],light); rect(im,(4,6,5,12),light); rect(im,(10,6,11,12),light); rect(im,(7,5,8,8),'silver')
    elif key=='coin':
        widths=[5,4,2,1,2,4]; w=widths[f%6]; ellipse(im,(8-w,2,8+w,13),'gold_dark'); ellipse(im,(9-w,3,7+w,12),'gold_mid'); line(im,[(8-w,5),(8-w,9)],'gold_light'); line(im,[(8,5),(8,10)],'gold_light')
    elif key=='weapon':
        poly(im,[(4,10),(10,3),(12,2),(12,5),(6,12)],'silver'); line(im,[(5,10),(11,3)],'white'); line(im,[(3,9),(7,13)],'wood_light',2); line(im,[(4,12),(2,14)],'wood_mid',2)
    elif key=='armor':
        poly(im,[(3,3),(6,2),(7,5),(9,5),(10,2),(13,3),(12,7),(11,13),(4,13),(3,7)],'slate_mid'); line(im,[(4,3),(5,11),(10,11)],'silver'); rect(im,(6,7,9,9),'slate_light')
    elif key=='ring':
        ellipse(im,(3,5,12,14),'wood_light'); ellipse(im,(5,7,10,12),'outline'); poly(im,[(5,4),(8,2),(11,4),(8,7)],'silver'); rect(im,(7,3,8,4),'white')
    elif key=='power': poly(im,[(8,1),(3,8),(7,8),(5,14),(13,6),(9,6),(11,1)],'gold_light')
    elif key=='stage':
        rect(im,(2,11,13,13),'slate_light'); rect(im,(5,8,13,10),'silver'); rect(im,(8,5,13,7),'cream'); line(im,[(10,2),(13,2),(13,4)],'gold_light')
    elif key=='expand':
        for a in [(2,6,2,2,6,2),(9,2,13,2,13,6),(2,9,2,13,6,13),(9,13,13,13,13,9)]: line(im,list(zip(a[::2],a[1::2])),'silver',2)
    elif key=='close': line(im,[(4,4),(11,11)],'silver',2); line(im,[(11,4),(4,11)],'silver',2)
    elif key=='settings':
        poly(im,[(6,2),(9,2),(10,4),(12,4),(13,6),(12,9),(11,10),(11,12),(8,13),(5,12),(4,10),(2,9),(2,6),(4,5),(4,3)],'slate_light'); ellipse(im,(5,5,10,10),'outline'); rect(im,(7,7,8,8),'silver')
    elif key=='arrow':
        line(im,[(2,8),(12,8)],'wood_light'); poly(im,[(11,5),(14,8),(11,11)],'silver' if f==0 else 'cream'); line(im,[(2,5),(4,8),(2,11)],'cream')
    return outline(im)

def effect(kind,f):
    im=canvas()
    if kind=='hit':
        r=[3,7,10,12][f]
        for dx,dy in [(-1,-1),(1,-1),(-1,1),(1,1)]: line(im,[(16+dx*max(1,r-4),16+dy*max(1,r-4)),(16+dx*r,16+dy*r)],'cream' if f<2 else 'gold_mid',2)
        if f==0: rect(im,(14,14,18,18),'white')
    else:
        y=28-f*4; line(im,[(6,y),(6,y+3)],'gold_mid'); line(im,[(25,y-2),(25,y+1)],'gold_mid'); sparkle(im,16,y-5,'cream')
        poly(im,[(13,y),(16,y-3),(19,y),(17,y),(17,y+3),(15,y+3),(15,y)],'gold_light')
    return outline(im)

def save(key,frames,fps,loop,paint,size=32,impact=None):
    sheet=Image.new('RGBA',(frames*size,size))
    for f in range(frames): sheet.alpha_composite(paint(f),(f*size,0))
    meta=PngImagePlugin.PngInfo(); meta.add_text('Source','Original integer pixel maps: design/tools/build_sprites.py; OpenAI Codex assisted code; no image generation.')
    sheet.save(OUT/(key+'.png'),pnginfo=meta)
    spec=dict(file=key+'.png',frameWidth=size,frameHeight=size,frames=frames,fps=fps,loop=loop)
    if impact is not None: spec['events']={'impact':impact}
    SHEETS[key]=spec

for cls in ('melee','mage','ranged'):
    for anim,n,fps,loop,impact in [('idle',4,6,True,None),('walk',6,10,True,None),('attack',6,14,False,3),('hurt',2,10,False,None),('death',5,8,False,None)]:
        save(f'hero_{cls}_{anim}',n,fps,loop,lambda f,c=cls,a=anim:hero(c,a,f),impact=impact)
for m in ('slime','goblin','skeleton'):
    for anim,n,fps,loop,impact in [('idle',4,6,True,None),('walk',6,10,True,None),('attack',4,10,False,2),('death',5,10,False,None)]:
        save(f'{m}_{anim}',n,fps,loop,lambda f,m=m,a=anim:monster(m,a,f),impact=impact)
for mat,anim,n,fps,loop in [('wood','idle',1,0,False),('wood','open',5,12,False),('gold','locked',4,6,True),('gold','ready',4,8,True),('gold','open',6,12,False)]:
    save(f'box_{mat}_{anim}',n,fps,loop,lambda f,m=mat,a=anim:box(m,a,f))
for k in ('box_wood','box_gold','coin','power','stage','expand','close','settings','weapon','armor','ring'): save('icon_'+k,1,0,False,lambda f,k=k:icon(k),16)
save('coin_spin',6,12,True,lambda f:icon('coin',f),16)
save('fx_hit',4,16,False,lambda f:effect('hit',f))
save('fx_levelup',6,12,False,lambda f:effect('levelup',f))
save('fx_arrow',2,12,True,lambda f:icon('arrow',f),16)
existing=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))['sheets'] if (OUT/'manifest.json').exists() else {}
existing.update(SHEETS)
(OUT/'manifest.json').write_text(json.dumps({'version':1,'sheets':existing},indent=2)+'\n',encoding='utf-8')
palette=Image.new('RGB',(len(P)*16,16))
for i,c in enumerate(P.values()): ImageDraw.Draw(palette).rectangle((i*16,0,i*16+15,15),fill=c)
palette.save(ROOT/'palette.png')

preview='''<!doctype html><html lang="th"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Sprite atlas · Hearth & Hoard</title><style>
body{margin:24px;background:#171c2c;color:#fff9ed;font:14px/1.6 Tahoma,sans-serif}h1{font-size:24px}button{padding:8px 16px;background:#ffd875;border:0;color:#171c2c;cursor:pointer}button:focus-visible{outline:2px solid #fff9ed;outline-offset:3px}.atlas{display:grid;grid-template-columns:repeat(auto-fit,minmax(370px,1fr));gap:16px}.entry{border:1px solid #55647a;padding:12px;min-width:0}h2{font-size:14px;margin:0 0 8px;overflow-wrap:anywhere}.contexts{display:flex;gap:4px}.context{display:flex;align-items:end;justify-content:center;gap:12px;width:33.33%;height:112px;border:1px solid #55647a}.light{background:#fff9ed}.dark{background:#1e1e1e}.color{background:linear-gradient(120deg,#5389ca,#d75b60,#6db586)}.sprite{display:inline-block;image-rendering:pixelated;flex:none}small{color:#b8c4cf}@media(max-width:430px){body{margin:12px}.atlas{grid-template-columns:minmax(0,1fr)}.contexts{flex-direction:column}.context{width:100%}}
</style><h1>คลังภาพ · ทุกท่าที่ 1× และ 3×</h1><p>ภาพต้นฉบับบนพื้นสว่าง มืด และสี · ท่าไม่วนจะหยุดเฟรมสุดท้าย</p><button id="replay">เล่นทุกท่าใหม่</button><p id="count"></p><main class="atlas" id="atlas"></main><script>
const manifest=MANIFEST; let start=performance.now(); const views=[];const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
for(const [key,s] of Object.entries(manifest.sheets)){const a=document.createElement('article');a.className='entry';a.innerHTML=`<h2>${key}</h2><small>${s.frameWidth}×${s.frameHeight} · ${s.frames} frames · ${s.fps} fps · ${s.loop?'วน':'ครั้งเดียว'}${s.events?' · impact '+s.events.impact:''}</small><div class="contexts"></div>`;for(const bg of ['light','dark','color']){const c=document.createElement('div');c.className='context '+bg;for(const scale of [1,3]){const el=document.createElement('span');el.className='sprite';el.style.cssText=`width:${s.frameWidth*scale}px;height:${s.frameHeight*scale}px;background-image:url(${s.file});background-size:${s.frameWidth*s.frames*scale}px ${s.frameHeight*scale}px`;c.append(el);views.push({el,s,scale})}a.lastChild.append(c)}atlas.append(a)}
count.textContent=Object.keys(manifest.sheets).length+' sprite sheets';replay.onclick=()=>{start=performance.now();render(start)};
function render(t){for(const {el,s,scale} of views){const raw=reduced?0:Math.floor((t-start)/1000*s.fps);const f=s.loop?raw%s.frames:Math.min(s.frames-1,raw);el.style.backgroundPosition=`${-f*s.frameWidth*scale}px 0`}if(!reduced)requestAnimationFrame(render)}requestAnimationFrame(render);
</script></html>'''.replace('MANIFEST',json.dumps({'version':1,'sheets':SHEETS}))
(OUT/'preview.html').write_text(preview,encoding='utf-8')
print(f'Built {len(SHEETS)} sprite sheets + palette + preview.')
from refresh_previews import refresh
refresh()
