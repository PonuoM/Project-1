"""Prompt 6. Adds only the named regional assets; preserves existing sprite bytes/entries."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,PngImagePlugin
from refresh_previews import refresh
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'sprites'
P=json.loads((ROOT/'tokens.json').read_text())['palette']
REGIONS={
 'grassland':{'th':'ทุ่งหญ้า','en':'Grassland','monsters':['slime','goblin'],'boss':'boss_kingslime','ground':'ground_grassland'},
 'darkforest':{'th':'ป่ามืด','en':'Dark Forest','monsters':['wolf','spider'],'boss':'boss_treant','ground':'ground_darkforest'},
 'crypt':{'th':'สุสาน','en':'Crypt','monsters':['skeleton','ghost'],'boss':'boss_lich','ground':'ground_crypt'}}
NEW={}
def canvas(n=32):return Image.new('RGBA',(n,n))
def r(im,xy,c):ImageDraw.Draw(im).rectangle(xy,fill=P[c])
def line(im,xy,c,w=1):ImageDraw.Draw(im).line(xy,fill=P[c],width=w)
def poly(im,xy,c):ImageDraw.Draw(im).polygon(xy,fill=P[c])
def ellipse(im,xy,c):ImageDraw.Draw(im).ellipse(xy,fill=P[c])
def outline(im):
    src=im.copy();w,h=im.size;p=src.load();q=im.load();col=tuple(bytes.fromhex(P['outline'][1:]))+(255,)
    for y in range(h):
        for x in range(w):
            if not p[x,y][3] and any(0<=x+a<w and 0<=y+b<h and p[x+a,y+b][3] for a,b in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(1,-1),(-1,1),(1,1)]):q[x,y]=col
    return im
def sparkle(im,x,y,c):
    line(im,[(x-2,y),(x+2,y)],c);line(im,[(x,y-2),(x,y+2)],c)

def small_death(kind,f):
    im=canvas()
    if f<2:
        im=monster(kind,'idle',f)
        # First hit and fall pose, still anchored to the shared floor.
        if f==1:r(im,(9,21,15,22),'cream')
        return im
    spread=f-2
    if kind=='wolf':
        poly(im,[(5,28),(9,25+spread),(24,27),(27,30),(4,30)],'slate_mid')
        line(im,[(6,28),(14,27+spread),(22,28+min(spread,1))],'silver')
        r(im,(4,28,7,30),'slate_dark');r(im,(6,28,6,28),'ink')
    elif kind=='spider':
        ellipse(im,(11,26+spread,23,30),'purple_dark')
        for x in (5,9,25,28):line(im,[(x,30),(x+(-2 if x<16 else 2),27+spread)],'slate_mid')
        r(im,(12,28,14,28),'red_dark')
    else:
        for x,y in [(8,28),(15,25),(23,28),(19,30)]:
            r(im,(x,y+min(spread,30-y),x+max(0,2-spread),min(30,y+min(spread,30-y)+1)),'purple_mid' if spread>0 else 'cream')
    return outline(im)

def monster(kind,anim,f):
    if anim=='death':return small_death(kind,f)
    im=canvas();bob=[0,1,0,-1][f%4] if anim=='idle' else 0
    stride=[-1,0,1,2,1,0][f%6] if anim=='walk' else 0
    attack=anim=='attack';lunge=[0,-1,-3,0][f%4] if attack else 0
    if kind=='wolf':lunge=max(-1,lunge) # Keep the complete muzzle outline inside the frame.
    if kind=='wolf':
        # Long muzzle left, pointed ears, high tail right; steel-gray coat.
        poly(im,[(10,18+bob),(17,16+bob),(24,17+bob),(26,23),(23,25),(12,25)],'slate_mid')
        line(im,[(11,18+bob),(17,17+bob),(23,18+bob)],'silver',2)
        poly(im,[(23,18),(27,14+stride),(29,13+stride),(28,20),(25,24)],'slate_dark')
        line(im,[(26,16+stride),(28,14+stride)],'slate_light')
        poly(im,[(4+lunge,16+bob),(7+lunge,11+bob),(10+lunge,15+bob),(13+lunge,13+bob),(15+lunge,20+bob),(11+lunge,23+bob),(3+lunge,22+bob),(2+lunge,19+bob)],'slate_mid')
        line(im,[(5+lunge,16+bob),(7+lunge,13+bob),(10+lunge,17+bob)],'silver')
        r(im,(3+lunge,20+bob,7+lunge,21+bob),'cream');r(im,(2+lunge,19+bob,3+lunge,20+bob),'ink')
        r(im,(8+lunge,17+bob,9+lunge,17+bob),'gold_light')
        if attack and f==2:r(im,(3,22,7,23),'ink');r(im,(4,22,4,22),'cream')
        for x,s in [(12,stride),(16,-stride),(22,-stride),(24,stride)]:
            line(im,[(x,24),(x+s,28),(x+s-1,30)],'slate_dark',2)
            line(im,[(x+s-2,30),(x+s+1,30)],'silver')
    elif kind=='spider':
        # Four leg pairs, hind abdomen on the right, eyes on left-facing head.
        for i in range(4):
            x=10+i*4;delta=(stride if i%2 else -stride)
            line(im,[(x,22),(x-5,17+i%2),(max(2,x-8),28+delta//2)],'slate_mid')
            line(im,[(x,23),(x+4,25-i%2),(min(29,x+6),30)],'slate_mid')
        ellipse(im,(14,14+bob,26,25+bob),'purple_dark');line(im,[(17,16+bob),(22,15+bob),(25,18+bob)],'purple_mid',2)
        ellipse(im,(7+lunge,20+bob,15+lunge,27+bob),'slate_dark')
        r(im,(8+lunge,22+bob,9+lunge,23+bob),'red_light');r(im,(12+lunge,22+bob,13+lunge,23+bob),'red_mid')
        line(im,[(8+lunge,27+bob),(6+lunge,29+bob)],'silver');line(im,[(11+lunge,27+bob),(10+lunge,29+bob)],'silver')
        if attack and f==2:line(im,[(3,21),(1,19)],'cream');line(im,[(3,26),(1,28)],'cream')
    else:
        float_y=[0,1,2,1][f%4] if anim!='attack' else [1,0,0,1][f%4]
        xoff=-2 if attack and f==2 else 0;y=float_y
        poly(im,[(8+xoff,13+y),(11+xoff,8+y),(20+xoff,8+y),(24+xoff,13+y),(23,23+y),(26,28+y),(20,27+y),(17,29+y),(13,27+y),(7,28+y),(9,22+y)],'purple_mid')
        poly(im,[(10+xoff,13+y),(13+xoff,9+y),(19+xoff,9+y),(21+xoff,14+y),(18,23+y),(14,27+y),(11,23+y)],'cream')
        line(im,[(11+xoff,12+y),(14+xoff,10+y),(18+xoff,10+y)],'white')
        r(im,(10+xoff,15+y,12+xoff,17+y),'ink');r(im,(16+xoff,15+y,18+xoff,17+y),'ink')
        r(im,(12+xoff,21+y,15+xoff,22+y),'purple_dark')
        if attack and f==2:sparkle(im,3,20,'purple_light')
    return outline(im)

def boss_death(kind,f):
    if f<2:
        im=boss(kind,'idle',f);line(im,[(14,26),(24,26)],'cream',2);return im
    im=canvas(48);spread=f-2
    if kind=='kingslime':
        top=min(44,33+spread*2)
        ellipse(im,(7-spread,top,39+spread,46),'green_dark');line(im,[(8,top+2),(21,top+1),(34,top+2)],'green_mid')
        poly(im,[(18,top-4),(18,top-8),(21,top-5),(24,top-9),(27,top-5),(30,top-8),(30,top-4)],'gold_mid')
    elif kind=='treant':
        for x in (8,18,30,40):
            line(im,[(x,46),(x-3+spread,41+min(spread,3)),(x+3,44)],'wood_mid',3)
            r(im,(x,44,x+1,45),'wood_light')
        poly(im,[(14,40+min(spread,4)),(32,41+min(spread,3)),(35,46),(13,46)],'wood_dark')
        for x in (13,24,36):r(im,(x,36+min(spread*2,9),x+2,38+min(spread*2,7)),'green_dark')
    else:
        poly(im,[(8-spread,46),(16,38+min(spread,6)),(32,40+min(spread,4)),(39+spread,46)],'purple_dark')
        line(im,[(12,45),(20,43),(32,45)],'purple_mid',2)
        r(im,(20,36+min(spread,6),28,41+min(spread,4)),'cream');r(im,(21,38+min(spread,6),23,39+min(spread,5)),'ink')
        line(im,[(5,46),(12+spread,41+min(spread,4))],'gold_dark',2)
    return outline(im)

def boss(kind,anim,f):
    if anim=='death':return boss_death(kind,f)
    im=canvas(48);bob=f%2 if anim in ('idle','walk') else 0
    step=[0,1,2,0,-1,-2][f%6] if anim=='walk' else 0
    strike=anim=='attack';phase=[0,-1,-2,-4,-1,0][f%6] if strike else 0
    if kind=='kingslime':
        top=21+bob+phase
        poly(im,[(5,43),(6,top+10),(12,top+3),(20,top),(30,top),(37,top+4),(42,top+12),(43,43),(38,46),(10,46)],'green_mid')
        poly(im,[(7,40),(9,top+9),(14,top+4),(23,top+1),(29,top+2),(20,top+5),(13,top+12)],'green_light')
        line(im,[(12,45),(37,45),(41,42)],'green_dark',2)
        r(im,(13,top+10,16,top+12),'ink');r(im,(23,top+10,26,top+12),'ink')
        line(im,[(16,top+17),(20,top+19),(25,top+17)],'green_dark',2)
        # A broad crown, safely inside the 48px grid even in attack anticipation.
        y=top-3
        poly(im,[(15,y),(13,y-8),(19,y-5),(23,y-11),(27,y-5),(33,y-8),(31,y)],'gold_mid')
        line(im,[(15,y-1),(31,y-1)],'gold_light',2);r(im,(22,y-5,24,y-3),'red_mid')
        if strike and f==3:
            line(im,[(3,43),(1,40)],'green_light');line(im,[(43,43),(46,40)],'green_light')
        if step:line(im,[(13+step,46),(28+step,46)],'green_light')
    elif kind=='treant':
        # Rooted trunk, asymmetric branch arms and broad canopy crown.
        for x,delta in [(15,step),(22,-step),(31,step)]:
            poly(im,[(x,36),(x+3,39),(x+3+delta,45),(x+7+delta,46),(x-3+delta,46),(x-1,40)],'wood_mid')
            line(im,[(x,39),(x+1+delta,45)],'wood_light')
        poly(im,[(14,19+bob),(31,17+bob),(34,35),(28,41),(17,40),(12,31)],'wood_mid')
        line(im,[(15,20+bob),(15,31),(19,36)],'wood_light',2)
        line(im,[(27,22),(25,29),(28,35)],'wood_dark',2)
        poly(im,[(13,22),(9+phase,25),(7+phase,34),(4,34),(7,22),(12,18)],'wood_dark')
        line(im,[(8,25),(6,32)],'wood_light')
        poly(im,[(31,21),(38,24),(43,32+step),(41,34),(36,27),(31,26)],'wood_mid')
        # Branches beyond the canopy read as horns, not a decorative aura.
        line(im,[(14,17),(10,8),(6,6)],'wood_mid',3);line(im,[(31,17),(35,7),(40,5)],'wood_mid',3)
        poly(im,[(8,18+bob),(6,12+bob),(13,8+bob),(20,9+bob),(27,6+bob),(35,9+bob),(39,15+bob),(35,20+bob),(24,20+bob),(19,17+bob)],'green_dark')
        line(im,[(10,12+bob),(15,10+bob),(20,11+bob)],'green_mid',2)
        line(im,[(27,8+bob),(33,10+bob),(36,13+bob)],'green_mid')
        r(im,(15,22,17,24),'gold_light');r(im,(24,21,26,23),'gold_light');r(im,(17,29,23,30),'wood_dark')
        if strike and f==3:line(im,[(2,34),(1,38)],'cream');line(im,[(5,38),(2,40)],'cream')
    else:
        # Lich: purple robe, pale left-facing skull, gold crown and crooked staff.
        poly(im,[(17,22+bob),(32,22+bob),(34,34),(39,45),(36,46),(11,46),(13,35)],'purple_dark')
        poly(im,[(18,25),(21,24),(22,39),(18+step,44),(14,45)],'purple_mid')
        line(im,[(14,45),(35,45)],'gold_mid')
        r(im,(18+step,46,22+step,46),'silver');r(im,(30-step,46,34-step,46),'silver')
        poly(im,[(15,13+bob),(19,8+bob),(29,8+bob),(33,13+bob),(31,23),(17,24)],'purple_dark')
        r(im,(18,13+bob,28,20+bob),'cream');r(im,(19,13+bob,26,14+bob),'white')
        r(im,(18,16+bob,21,18+bob),'ink');r(im,(25,16+bob,27,18+bob),'ink');r(im,(21,21+bob,26,22+bob),'cream')
        r(im,(22,21+bob,22,22+bob),'ink');r(im,(25,21+bob,25,22+bob),'ink')
        poly(im,[(16,10+bob),(16,5+bob),(20,8+bob),(24,3+bob),(28,8+bob),(31,5+bob),(31,10+bob)],'gold_mid');line(im,[(17,10+bob),(30,10+bob)],'gold_light')
        line(im,[(15,26),(9,29),(7,26)],'cream',2)
        line(im,[(7,44),(7,15),(9,12)],'gold_dark',2);line(im,[(8,43),(8,18)],'gold_mid')
        poly(im,[(5,13),(8,9),(11,13),(8,17)],'purple_mid');r(im,(7,11,8,12),'white')
        if strike:
            r(im,(5,23+phase,7,25+phase),'purple_mid')
            if f==3:sparkle(im,3,20,'cream');sparkle(im,11,19,'gold_light')
    return outline(im)

def ground(region):
    im=Image.new('RGBA',(64,8))
    # Repeating edge samples agree; no vertical seam outline on repeatable tiles.
    r(im,(0,4,63,7),'ink');line(im,[(0,3),(63,3)],'outline')
    if region=='grassland':
        r(im,(0,4,63,4),'green_dark')
        for x in (6,17,32,45,56):line(im,[(x,4),(x+1,2),(x+2,4)],'outline')
        for x in (10,26,41,60):r(im,(x,6,x+2,6),'slate_dark')
    elif region=='darkforest':
        r(im,(0,4,63,4),'wood_dark')
        for x in (8,23,40,54):line(im,[(x,4),(x+5,5),(x+8,6)],'outline')
        for x in (13,34,49):r(im,(x,3,x+3,4),'green_dark')
    else:
        r(im,(0,4,63,5),'slate_dark')
        for x in (9,26,42,57):line(im,[(x,4),(x,6),(x-3,7)],'outline')
        r(im,(18,6,22,6),'outline');r(im,(46,7,50,7),'outline')
    return im

def save(key,n,fps,loop,size,paint,impact=None,height=None):
    height=height or size;sheet=Image.new('RGBA',(size*n,height))
    for f in range(n):sheet.alpha_composite(paint(f),(f*size,0))
    meta=PngImagePlugin.PngInfo();meta.add_text('Source','Original pixel geometry: design/tools/build_regions.py; Codex assisted code; no AI image generation.')
    sheet.save(OUT/(key+'.png'),pnginfo=meta)
    s={'file':key+'.png','frameWidth':size,'frameHeight':height,'frames':n,'fps':fps,'loop':loop}
    if impact is not None:s['events']={'impact':impact}
    NEW[key]=s

manifest=json.loads((OUT/'manifest.json').read_text())
reserved={f'{m}_{a}' for m in ('wolf','spider','ghost','boss_kingslime','boss_treant','boss_lich') for a in ('idle','walk','attack','death')}|{f'ground_{r}' for r in REGIONS}
before={k:(s.copy(),hashlib.sha256((OUT/s['file']).read_bytes()).hexdigest()) for k,s in manifest['sheets'].items() if k not in reserved}
for m in ('wolf','spider','ghost'):
    for a,n,fps,loop,impact in [('idle',4,6,True,None),('walk',6,10,True,None),('attack',4,10,False,2),('death',5,10,False,None)]:
        save(f'{m}_{a}',n,fps,loop,32,lambda f,m=m,a=a:monster(m,a,f),impact)
for b in ('kingslime','treant','lich'):
    for a,n,fps,loop,impact in [('idle',4,6,True,None),('walk',6,8,True,None),('attack',6,10,False,3),('death',8,10,False,None)]:
        save(f'boss_{b}_{a}',n,fps,loop,48,lambda f,b=b,a=a:boss(b,a,f),impact)
for region in REGIONS:save('ground_'+region,1,0,False,64,lambda f,r=region:ground(r),height=8)
manifest['sheets'].update(NEW)
for k,(s,digest) in before.items():
    assert manifest['sheets'][k]==s and hashlib.sha256((OUT/s['file']).read_bytes()).hexdigest()==digest,k
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(ROOT/'regions.json').write_text(json.dumps(REGIONS,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
refresh()
print(f'Added {len(NEW)} regional sheets; preserved {len(before)} existing sheets. Refreshed preview and atlas.')
