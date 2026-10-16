"""View original PixelLab candidates/animation locally, without APIs or credentials."""
import json,math
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]/'pixellab/swordsman'
files=sorted(ROOT.glob('candidate-[0-9][0-9].png'))
assert files,'Download candidates before building preview.'
selected=json.loads((ROOT/'selection.json').read_text()).get('file') if (ROOT/'selection.json').exists() else files[0].name
frames=sorted((ROOT/'attack-frames').glob('frame-[0-9][0-9].png'))
if frames:
    first=Image.open(frames[0]).convert('RGBA');w,h=first.size
    sheet=Image.new('RGBA',(w*len(frames),h))
    board=Image.new('RGB',(280*3,308*math.ceil(len(frames)/3)),'#202020');bd=ImageDraw.Draw(board)
    for i,file in enumerate(frames):
        frame=Image.open(file).convert('RGBA');assert frame.size==(w,h)
        sheet.paste(frame,(i*w,0)) # Exact RGBA copy: no alpha compositing or recoloring.
        tile=frame.resize((w*4,h*4),Image.Resampling.NEAREST);x=i%3*280+12;y=i//3*308+8
        board.paste(tile,(x,y),tile);bd.text((x,y+270),str(i)+' / '+file.name,fill='#FFF9ED')
    sheet.save(ROOT/'attack.png');board.save(ROOT/'attack-atlas.png')
    (ROOT/'animation.json').write_text(json.dumps({'file':'attack.png','width':w,'height':h,'frames':len(frames),'fps':32,'impact':3,'hitStopMs':45,'loopPauseMs':650,'source':'PixelLab animate-with-text-v3; original downloaded frames retained','requestedFrames':8,'returnedImages':len(frames)},indent=2)+'\n')
animation=json.loads((ROOT/'animation.json').read_text()) if (ROOT/'animation.json').exists() else None
cell=280;cols=4;rows=math.ceil(len(files)/cols)
atlas=Image.new('RGB',(cols*cell,rows*(cell+28)),'#202020');draw=ImageDraw.Draw(atlas)
for i,file in enumerate(files):
    im=Image.open(file).convert('RGBA');scale=max(1,min(4,(cell-20)//max(im.size)))
    tile=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
    x=i%cols*cell+(cell-tile.width)//2;y=i//cols*(cell+28)+10
    atlas.paste(tile,(x,y),tile);draw.text((i%cols*cell+12,(i//cols+1)*(cell+28)-24),file.stem+(' [selected]' if file.name==selected else ''),fill='#FFD875' if file.name==selected else '#FFF9ED')
atlas.save(ROOT/'candidate-atlas.png')
im=Image.open(ROOT/selected);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/'selected-4x.png')
records=[{'file':file.name,'width':Image.open(file).width,'height':Image.open(file).height} for file in files]
html='''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PixelLab · นักดาบทดลอง</title><style>
body{margin:24px;background:#171c2c;color:#fff9ed;font:14px/1.6 Tahoma,sans-serif}h1{font-size:24px}h2{font-size:18px}p{color:#b8c4cf;max-width:80ch}button{cursor:pointer;background:#252c40;border:1px solid #55647a;color:#fff9ed;padding:8px;min-height:32px}button:hover,button.selected{border-color:#ffd875}button:focus-visible{outline:2px solid #ffd875;outline-offset:3px}.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:16px;margin-top:24px}.candidate{text-align:left}.candidate img{display:block;margin:8px auto;image-rendering:pixelated}.contexts{display:flex;flex-wrap:wrap;gap:16px;margin:16px 0}.context{display:flex;align-items:end;gap:24px;padding:16px;min-height:300px;border:1px solid #55647a}.dark{background:#202020}.light{background:#f3f3f3}.image,.frame{image-rendering:pixelated}figure{margin:0;display:grid;justify-items:center;gap:8px}.light figcaption{color:#171c2c}a{color:#ffd875}.hint{color:#ffd875}.animation{border-top:1px solid #55647a;padding-top:16px;margin-top:24px}.frame{display:block;background-repeat:no-repeat}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}select{padding:6px;background:#252c40;color:#fff9ed;border:1px solid #55647a;font:inherit}@media(max-width:600px){body{margin:12px}.context{gap:12px;padding:8px}.gallery{grid-template-columns:minmax(0,1fr)}}
</style></head><body><h1>นักดาบ · ทดลอง PixelLab</h1><p>AI-generated artwork · ภาพต้นฉบับพื้นโปร่งใส · ยังไม่แทนที่ assets ในเกม · กดภาพด้านล่างเพื่อเทียบรายละเอียด</p><h2 id="selected-label"></h2><div class="contexts" id="contexts"></div><section class="animation" id="animation" hidden><h2>ท่าฟันเร็ว</h2><p>ภาพท่าจาก PixelLab · จังหวะ playback ทดลอง 32 FPS + hit stop 45ms · ตัวเลือก FPS ใช้ดูรายละเอียดท่า</p><div class="controls"><button id="replay">เล่นท่าอีกครั้ง</button><label>FPS <select id="fps"><option>16</option><option>24</option><option selected>32</option></select></label><label><input type="checkbox" id="loop" checked> เล่นซ้ำ</label></div><div class="contexts" id="animation-contexts"></div></section><p class="hint">ภาพที่กดเลือกเปลี่ยนเฉพาะ preview ในหน้านี้ ไม่บันทึกหรือเรียก API</p><main class="gallery" id="gallery"></main><p><a href="candidate-atlas.png">ภาพรวมทุกตัวเลือก</a> · <a href="README.md">ที่มาและวิธีใช้ API</a></p><script>
const images=IMAGES,initial=INITIAL,anim=ANIMATION;const gallery=document.getElementById('gallery'),contexts=document.getElementById('contexts');
function select(file){const s=images.find(s=>s.file===file);document.getElementById('selected-label').textContent=file+' · '+s.width+'×'+s.height;contexts.replaceChildren();for(const bg of ['dark','light']){const c=document.createElement('div');c.className='context '+bg;for(const scale of [1,4]){const fig=document.createElement('figure');fig.innerHTML=`<img class="image" src="${file}" width="${s.width*scale}" height="${s.height*scale}" alt="นักดาบ ${file}"><figcaption>${scale}×</figcaption>`;c.append(fig)}contexts.append(c)}for(const b of gallery.children)b.classList.toggle('selected',b.dataset.file===file)}
for(const s of images){const b=document.createElement('button');b.className='candidate';b.dataset.file=s.file;b.innerHTML=`<strong>${s.file}</strong><img src="${s.file}" width="${s.width*4}" height="${s.height*4}" alt="นักดาบ ${s.file}">`;b.onclick=()=>select(s.file);gallery.append(b)}select(initial);
if(anim){document.getElementById('animation').hidden=false;const views=[];for(const bg of ['dark','light']){const c=document.createElement('div');c.className='context '+bg;for(const scale of [1,4]){const el=document.createElement('span');el.className='frame';el.style.cssText=`width:${anim.width*scale}px;height:${anim.height*scale}px;background-image:url(${anim.file});background-size:${anim.width*anim.frames*scale}px ${anim.height*scale}px`;c.append(el);views.push({el,scale})}document.getElementById('animation-contexts').append(c)}let start=performance.now();document.getElementById('replay').onclick=()=>start=performance.now();function tick(now){const step=1000/Number(document.getElementById('fps').value),total=step*anim.frames+45;let t=now-start;if(document.getElementById('loop').checked)t%=total+650;let f;if(t>=total)f=anim.frames-1;else if(t>=step*anim.impact&&t<step*(anim.impact+1)+45)f=anim.impact;else f=Math.min(anim.frames-1,Math.floor((t-(t>step*(anim.impact+1)+45?45:0))/step));for(const {el,scale} of views)el.style.backgroundPosition=`${-f*anim.width*scale}px 0`;requestAnimationFrame(tick)}requestAnimationFrame(tick)}
</script></body></html>'''.replace('IMAGES',json.dumps(records)).replace('INITIAL',json.dumps(selected)).replace('ANIMATION',json.dumps(animation))
html=html.replace('.context{display:flex;', '.context{max-width:100%;box-sizing:border-box;overflow-x:auto;display:flex;')
(ROOT/'preview.html').write_text(html,encoding='utf-8')
print(f'Built preview for {len(files)} original candidates'+(' + animation' if animation else '')+'.')
