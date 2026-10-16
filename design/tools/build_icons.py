"""Prompt 5: independently drawn pixel icons; no resampling, ICO packs native PNGs."""
import io,json,struct
from pathlib import Path
from PIL import Image,ImageDraw,PngImagePlugin
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'tokens.json').read_text())['palette']
OUT=ROOT/'icons';OUT.mkdir(exist_ok=True)
# Native-size composition: left, right, lid top, lid bottom, base bottom, band width.
# Each size has its own pixel geometry, not a resized master.
LAYOUT={16:(2,13,4,7,13,1),24:(3,20,6,11,20,2),32:(4,27,8,14,27,2),
        48:(6,41,12,22,41,3),64:(8,55,16,29,55,4),
        128:(17,110,33,59,110,7),256:(34,221,67,119,221,13)}
def outlined(im):
    source=im.copy();w,h=im.size;p=source.load();q=im.load()
    color=tuple(bytes.fromhex(P['outline'][1:]))+(255,)
    for y in range(h):
        for x in range(w):
            if not p[x,y][3] and any(0<=x+a<w and 0<=y+b<h and p[x+a,y+b][3] for a,b in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(1,-1),(-1,1)]):q[x,y]=color
    return im
def draw(n,tray=False):
    im=Image.new('RGBA',(n,n));d=ImageDraw.Draw(im)
    def r(xy,c):d.rectangle(xy,fill=P[c])
    def line(xy,c,width=1):d.line(xy,fill=P[c],width=width)
    def poly(xy,c):d.polygon(xy,fill=P[c])
    l,rr,top,seam,bot,b=LAYOUT[n];cx=n//2
    # Bottom front face and bevel. Always keep a bright inner rim on dark taskbars.
    r((l,seam+1,rr,bot),'gold_dark');r((l+1,seam+2,rr-1,bot-1),'gold_mid')
    r((l+2,seam+2,rr-2,seam+2),'gold_light')
    r((l+1,seam+2,l+1,bot-1),'gold_light');r((rr-1,seam+2,rr-1,bot-1),'gold_light')
    r((l+2,bot-1,rr-2,bot-1),'gold_mid')
    # Shallow barrel lid, with individual facet coordinates for the current grid.
    poly([(l,seam),(l,top+2*b),(l+2*b,top),(rr-2*b,top),(rr,top+2*b),(rr,seam)],'gold_mid')
    line([(l+1,seam-1),(l+1,top+2*b),(l+2*b,top+1),(rr-2*b,top+1)],'gold_light',max(1,b//2))
    line([(l,seam),(rr,seam)],'gold_dark')
    # Brass bands bridge lid/body; the central silver latch is the identifying detail.
    for x in (l+2*b,rr-3*b+1):
        r((x,top+1,x+b-1,bot-1),'gold_light')
        if n>=32:r((x,top+2,x,bot-2),'gold_glint')
    latch_w={16:2,24:4,32:4,48:6,64:8,128:15,256:29}[n]
    latch_h={16:3,24:5,32:6,48:8,64:11,128:20,256:39}[n]
    x=cx-latch_w//2;y=seam-1
    r((x,y,x+latch_w-1,y+latch_h-1),'outline')
    r((x,y,x+latch_w-1,y+max(0,latch_h//3)),'silver')
    if n>=24:r((x+1,y+1,x+latch_w-2,y+1),'white')
    if n>=32:r((cx,y+latch_h//2,cx,y+latch_h-2),'gold_glint')
    # Larger versions get hammered metal rivets and stepped embossed facets.
    if n>=48 and not tray:
        for x in (l+3*b,rr-3*b):
            for y in (seam+3*b,bot-2*b):
                r((x,y,x+max(1,b//3),y+max(1,b//3)),'gold_glint')
        line([(l+4*b,bot-3*b),(l+4*b,bot-4*b),(cx-b,bot-4*b)],'gold_dark',max(1,b//3))
        line([(cx+b,bot-4*b),(rr-4*b,bot-4*b),(rr-4*b,bot-3*b)],'gold_dark',max(1,b//3))
    if n>=128:
        for i in range(3):line([(l+4*b,top+3+b*i//2),(rr-4*b,top+3+b*i//2)],'gold_light')
    # Small detached glint; asymmetry is recognizable even at 16px.
    gx=rr-b;gy=max(2,top-b-1);arm=max(1,b//2)
    line([(gx-arm,gy),(gx+arm,gy)],'gold_glint');line([(gx,gy-arm),(gx,gy+arm)],'gold_glint')
    if tray:
        # Simplify the tray to a broad bright lid with fewer internal seams.
        line([(l+2,top+2),(rr-2,top+2)],'gold_glint')
    return outlined(im)

meta=PngImagePlugin.PngInfo();meta.add_text('Source','Original native-size pixel geometry: design/tools/build_icons.py; Codex assisted code, no AI image generation.')
for n in LAYOUT:draw(n).save(OUT/f'icon-{n}.png',pnginfo=meta)
for n in (16,32):draw(n,True).save(OUT/f'tray-{n}.png',pnginfo=meta)
# ICO header and directory. Each payload is exactly its independently drawn PNG.
sizes=(16,24,32,48,64,256);payloads=[(OUT/f'icon-{n}.png').read_bytes() for n in sizes]
offset=6+16*len(sizes);entries=[]
for n,data in zip(sizes,payloads):
    entries.append(struct.pack('<BBBBHHII',n if n<256 else 0,n if n<256 else 0,0,0,1,32,len(data),offset));offset+=len(data)
(OUT/'app.ico').write_bytes(struct.pack('<HHH',0,1,len(sizes))+b''.join(entries)+b''.join(payloads))

items=[(f'icon-{n}.png',n) for n in LAYOUT]+[(f'tray-{n}.png',n) for n in (16,32)]
html='''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ไอคอนแอป · กล่องสมบัติ</title><style>
body{margin:24px;background:#171c2c;color:#fff9ed;font:14px/1.6 Tahoma,sans-serif}h1{font-size:24px}h2{font-size:16px}.sizes{display:grid;gap:24px}.size{min-width:0;border-top:1px solid #55647a;padding-top:8px}.contexts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.taskbar{display:flex;align-items:center;gap:24px;padding:16px;overflow:auto;min-height:64px}.light{background:#f3f3f3;color:#171c2c}.dark{background:#202020;color:#fff9ed}.sample{display:grid;justify-items:center;gap:8px;flex:none}img{display:block;image-rendering:pixelated}p{max-width:75ch}a{color:#ffd875}a:focus-visible{outline:2px solid #ffd875;outline-offset:4px}@media(max-width:800px){.contexts{grid-template-columns:minmax(0,1fr)}body{margin:12px}}
</style></head><body><h1>ไอคอนแอป · กล่องสมบัติทอง</h1><p>ทุกขนาดวาดบนกริดของตัวเอง · 16 / 24 / 32 ปรับพิกเซลโดยตรง · Tray ใช้ลายเรียบและฝาที่สว่างขึ้น · พื้นโปร่งใส ไม่มีตัวหนังสือบนไอคอน</p><p><a href="app.ico">app.ico — 16, 24, 32, 48, 64, 256</a></p><main class="sizes">'''
for file,n in items:
    html+=f'<section class="size"><h2>{file} · {n}×{n}</h2><div class="contexts">'
    for bg,label in [('light','Taskbar สว่าง'),('dark','Taskbar มืด')]:
        html+=f'<div class="taskbar {bg}" aria-label="{label}"><span>{label}</span>'
        for scale in (1,4):html+=f'<figure class="sample"><img src="{file}" width="{n*scale}" height="{n*scale}" alt="ไอคอนกล่องสมบัติ {n}px ที่ {scale}x"><figcaption>{scale}×</figcaption></figure>'
        html+='</div>'
    html+='</div></section>'
html+='</main></body></html>'
(OUT/'preview.html').write_text(html,encoding='utf-8')
print('Built 7 native-size app PNGs, 2 tray PNGs, multi-size ICO and preview.')
