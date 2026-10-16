"""Prototype-only native pixel poses. No production manifest or sprite is modified."""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw,PngImagePlugin
ROOT=Path(__file__).resolve().parents[2]
P=json.loads((ROOT/'tokens.json').read_text())['palette']
OUT=Path(__file__).resolve().parent/'assets';OUT.mkdir(exist_ok=True)
def r(im,xy,c):ImageDraw.Draw(im).rectangle(xy,fill=P[c])
def poly(im,points,c):ImageDraw.Draw(im).polygon(points,fill=P[c])
def line(im,points,c,w=1):ImageDraw.Draw(im).line(points,fill=P[c],width=w)
def outline(im):
    src=im.copy();px=src.load();q=im.load();w,h=im.size;col=tuple(bytes.fromhex(P['ink'][1:]))+(255,)
    for y in range(h):
        for x in range(w):
            if not px[x,y][3] and any(0<=x+a<w and 0<=y+b<h and px[x+a,y+b][3] for a,b in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]):q[x,y]=col
    return im
def sword(im,grip,tip):
    gx,gy=grip;tx,ty=tip;dx=tx-gx;dy=ty-gy;l=math.hypot(dx,dy);nx=-dy/l;ny=dx/l
    point=lambda x,y:(round(x),round(y))
    poly(im,[point(gx+nx*2,gy+ny*2),point(tx+nx,ty+ny),point(tx,ty),point(tx-nx,ty-ny),point(gx-nx*2,gy-ny*2)],'silver')
    line(im,[point(gx+nx,gy+ny),point(tx,ty)],'white')
    line(im,[point(gx+nx*5,gy+ny*5),point(gx-nx*5,gy-ny*5)],'gold_mid',2)
    line(im,[point(gx-dx/l*5,gy-dy/l*5),point(gx,gy)],'wood_dark',2)
def knight(anim,f):
    im=Image.new('RGBA',(64,64));walk=[-2,-1,1,2,1,-1][f%6] if anim=='walk' else 0
    pose=anim in ('slash','skill');lean=[-2,-3,1,4,2,0][f%6] if anim=='slash' else [0,-2,-3,-2,4,4,2,0][f%8] if anim=='skill' else 0
    bob=f%2 if anim in ('idle','walk') else 2 if pose and f<2 else 0
    x=lean;y=bob
    # Red cape behind the body, with faceted flutter rather than a translated rectangle.
    poly(im,[(24+x,31+y),(34+x,32+y),(28,46),(21-walk,57),(15-walk,56),(21,41)],'red_dark')
    line(im,[(24+x,33+y),(22,43),(18-walk,53)],'red_mid',2)
    # Articulated thigh, kneecap, shin and wide planted boots.
    for lx,offset,dark in [(27,walk,'slate_mid'),(36,-walk,'slate_dark')]:
        poly(im,[(lx+x,47),(lx+5+x,48),(lx+4+offset,54),(lx+2+offset,59),(lx-2+offset,59)],dark)
        r(im,(lx+offset-2,54,lx+offset+2,56),'silver')
        r(im,(lx+offset-2,57,lx+offset+1,60),dark)
        poly(im,[(lx+offset-3,60),(lx+offset+2,60),(lx+offset+5,62),(lx+offset-3,62)],'slate_dark')
        line(im,[(lx+offset-2,61),(lx+offset+2,61)],'slate_light')
    # Breastplate split into lit plates, waist rivets and a gorget.
    poly(im,[(24+x,32+y),(36+x,31+y),(41+x,37+y),(38+x,47),(27+x,49),(23+x,41)],'slate_mid')
    poly(im,[(26+x,33+y),(33+x,33+y),(35+x,41),(29+x,44),(26+x,42)],'silver')
    line(im,[(27+x,34+y),(32+x,34+y),(33+x,39)],'white')
    poly(im,[(36+x,34+y),(39+x,37+y),(36+x,44),(34+x,41)],'slate_dark')
    line(im,[(26+x,47),(36+x,46)],'gold_dark',2)
    r(im,(31+x,46,33+x,47),'gold_mid')
    # Faceted steel helmet with a clear right-facing visor and red horsehair crest.
    poly(im,[(24+x,22+y),(27+x,17+y),(35+x,17+y),(40+x,22+y),(40+x,29+y),(34+x,33+y),(25+x,30+y)],'slate_mid')
    poly(im,[(26+x,22+y),(28+x,18+y),(34+x,18+y),(36+x,21+y),(31+x,23+y)],'silver')
    line(im,[(28+x,18+y),(33+x,18+y)],'white')
    r(im,(32+x,24+y,41+x,25+y),'ink');r(im,(37+x,24+y,40+x,24+y),'gold_glint')
    line(im,[(39+x,27+y),(35+x,30+y)],'silver')
    line(im,[(32+x,26+y),(32+x,30+y)],'slate_dark')
    poly(im,[(28+x,17+y),(29+x,14+y),(34+x,13+y),(37+x,16+y),(32+x,16+y),(28,11+y),(20,12+y),(15,17+y),(13-walk,20+y),(14-walk,14+y),(21,9+y),(29,10+y)],'red_dark')
    line(im,[(17-walk,14+y),(23,11+y),(29,12+y)],'red_mid')
    # Shoulder and elbow overlap to make the arm read as a moving limb.
    poly(im,[(36+x,32+y),(40+x,31+y),(45+x,35+y),(43+x,38+y),(37+x,37+y)],'silver')
    line(im,[(39+x,32+y),(43+x,35+y)],'white')
    grip=(44+x,40+y)
    tip=(48,17+y)
    if anim=='slash':tip=[(13,19),(9,26),(60,27),(60,47),(51,55),(48,18)][f]
    if anim=='skill':tip=[(43,14),(37,6),(37,4),(47,7),(60,60),(60,58),(53,40),(48,18)][f]
    if anim=='skill' and f in (1,2,3):grip=(38+x,29+y)
    line(im,[(41+x,36+y),grip],'slate_mid',4);r(im,(grip[0]-1,grip[1]-1,grip[0]+1,grip[1]+1),'silver')
    sword(im,grip,tip)
    # Kite shield with brass rim, inner edge and a restrained heraldic cross.
    sx=22+x;sy=37+y
    poly(im,[(sx-6,sy),(sx+2,sy-2),(sx+5,sy+2),(sx+3,sy+14),(sx-1,sy+18),(sx-6,sy+13)],'gold_mid')
    poly(im,[(sx-5,sy+1),(sx+1,sy),(sx+3,sy+3),(sx+1,sy+13),(sx-1,sy+15),(sx-4,sy+11)],'blue_dark')
    line(im,[(sx-5,sy+1),(sx-5,sy+10),(sx-1,sy+15)],'silver')
    line(im,[(sx-1,sy+3),(sx-1,sy+12)],'gold_light');line(im,[(sx-3,sy+6),(sx+1,sy+6)],'gold_light')
    return outline(im)
def foe(anim,f):
    im=Image.new('RGBA',(48,48));bob=f%2 if anim=='idle' else 0
    if anim=='death':
        poly(im,[(8,43),(13,39+min(f,4)),(31,41+min(f,3)),(36,46),(8,46)],'green_dark')
        line(im,[(12,44),(21,43),(29,44)],'green_mid');return outline(im)
    step=[0,1,2,0,-1,-2][f%6] if anim=='walk' else 0
    for x,s in [(19,step),(30,-step)]:
        line(im,[(x,33),(x+s,41),(x+s-2,46)],'green_dark',4);line(im,[(x+s-4,46),(x+s+2,46)],'wood_dark',2)
    poly(im,[(12,22+bob),(21,20+bob),(32,21+bob),(37,31),(31,37),(16,37),(9,29)],'green_dark')
    poly(im,[(13,23+bob),(23,22+bob),(27,31),(17,34),(13,30)],'green_mid')
    r(im,(14,33,32,35),'wood_dark');r(im,(22,33,25,35),'gold_mid')
    poly(im,[(11,11+bob),(15,7+bob),(27,7+bob),(34,13+bob),(33,19+bob),(25,25+bob),(13,21+bob),(6,17+bob),(7,12+bob)],'green_mid')
    line(im,[(12,11+bob),(17,8+bob),(26,8+bob)],'green_light',2)
    poly(im,[(12,9+bob),(8,3+bob),(14,7+bob)],'cream');poly(im,[(28,9+bob),(31,3+bob),(33,10+bob)],'cream')
    r(im,(10,14+bob,13,15+bob),'ink');r(im,(20,14+bob,23,15+bob),'ink');r(im,(10,14+bob,11,14+bob),'red_light')
    line(im,[(9,19+bob),(23,21+bob)],'green_dark',2);r(im,(11,18+bob,12,21+bob),'cream');r(im,(21,20+bob,22,22+bob),'cream')
    line(im,[(12,26),(8,29),(5,27)],'green_mid',4)
    line(im,[(5,21),(4,38)],'wood_mid',3);poly(im,[(2,19),(2,14),(8,15),(9,21)],'slate_light');line(im,[(2,15),(6,16)],'silver')
    return outline(im)
manifest={}
for key,n,fps,paint in [('knight_idle',4,8,lambda f:knight('idle',f)),('knight_walk',6,14,lambda f:knight('walk',f)),('knight_slash',6,24,lambda f:knight('slash',f)),('knight_skill',8,24,lambda f:knight('skill',f)),('foe_idle',4,8,lambda f:foe('idle',f)),('foe_walk',6,12,lambda f:foe('walk',f)),('foe_death',4,12,lambda f:foe('death',f))]:
    first=paint(0);w,h=first.size;sheet=Image.new('RGBA',(w*n,h))
    for f in range(n):sheet.alpha_composite(paint(f),(f*w,0))
    meta=PngImagePlugin.PngInfo();meta.add_text('Source','Original prototype pixel poses: design/prototypes/action/build_art.py; Codex assisted code; no image-generation model.')
    sheet.save(OUT/(key+'.png'),pnginfo=meta);manifest[key]={'file':key+'.png','width':w,'height':h,'frames':n,'fps':fps}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Built 7 isolated prototype sheets; original game assets untouched.')
