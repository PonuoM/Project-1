from PIL import Image,ImageDraw
from pathlib import Path
import numpy as np,json
r=Path(__file__).parent
plans=json.loads((r/'timing-plan-v2.json').read_text())
sources={e['move']:e for e in json.loads((r/'motion-analysis-v1.json').read_text())}
contact=Image.new('RGB',(1024,len(plans)*192),(25,24,36));draw=ImageDraw.Draw(contact)
report=[]
def key_at(p,source,fi,acc):
    if p.get('cycle'):return (fi-p['start'])%4 if p['start']<=fi<p['end'] else None
    elapsed=sum(f['ms'] for f in source[:fi])+acc
    for start in reversed(p.get('starts',[p['start']])):
        age=elapsed-sum(f['ms'] for f in source[:start])
        if age<0:continue
        for k,d in enumerate(p['keys']):
            if age<d:return 1 if k==0 and fi in p['impact'] else k
            age-=d
        return None
    return None
for row,p in enumerate(plans):
    name=p['id'];old=Image.open(r/f'{name}-native-v1.png').convert('RGB')
    keys=[old.crop((k%2*128,k//2*80,k%2*128+128,k//2*80+80)) for k in range(4)]
    boxes=[im.getbbox() for im in keys];box=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
    x0,y0,x1,y1=p['region'];native=Image.new('RGB',(256,160),'black');registered=[];stats=[]
    # Apply ONE shared coordinate transform to all four keys, preserving animation registration.
    for k,im in enumerate(keys):
        target=Image.new('RGB',(128,80),'black');target.paste(im.crop(box).resize((x1-x0,y1-y0),Image.Resampling.NEAREST),(x0,y0));registered.append(target)
        native.paste(target,(k%2*128,k//2*80));a=np.asarray(target)[:,:,0];yy,xx=np.where(a>0)
        stats.append({'key':k,'bounds':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],'area':int(len(xx))})
    big=native.resize((1024,640),Image.Resampling.NEAREST)
    assert np.array_equal(np.asarray(big),np.asarray(native).repeat(4,0).repeat(4,1))
    assert set(native.getdata()) <= {(0,0,0),(60,60,60),(154,154,154),(255,255,255)}
    for path,im in [(r/f'{name}-native-v2.png',native),(r/f'{name}-v2.png',big)]:
        assert not path.exists();im.save(path)
    src=sources[name];frames=src['frames'];strip=Image.open(Path(src['strip']).with_name('strip-fast-blade-7.png')).convert('RGBA')
    layers=[]
    for im in registered:
        a=np.asarray(im);layers.append(Image.fromarray(np.dstack((a,np.where(a[:,:,0]>0,255,0).astype('uint8')))))
    def scene(fi,acc):
        stage=Image.new('RGBA',(160,104),(25,24,36,255));ImageDraw.Draw(stage).line((0,96,160,96),fill=(75,63,85))
        hero=strip.crop((fi*128,0,(fi+1)*128,80));key=key_at(p,frames,fi,acc);layer=layers[key].copy() if key is not None else None
        dx,dy=0,0
        if p.get('cycle'):
            body=frames[fi]['anchor']['body'];dx=round(body[0]-p['referenceBody'][0]);dy=round(body[1]-p['referenceBody'][1])
            if layer is not None:
                back=layer.copy();back.paste((0,0,0,0),(0,58,128,80));stage.alpha_composite(back,(16+dx,16+dy))
        stage.alpha_composite(hero,(16,16))
        if layer is not None:
            if p.get('cycle'):layer.paste((0,0,0,0),(0,0,128,58))
            stage.alpha_composite(layer,(16+dx,16+dy))
        return stage.convert('RGB').resize((480,312),Image.Resampling.NEAREST)
    # Split source-frame holds at effect-key boundaries rather than dropping8-15ms keys.
    cuts=set();time=0
    for f in frames:cuts.add(time);time+=f['ms']
    cuts.add(time)
    for start in p.get('starts',[p['start']]):
        t=sum(f['ms'] for f in frames[:start]);cuts.add(t)
        for ms in p['keys']:t+=ms;cuts.add(min(t,time))
    cuts=sorted(c for c in cuts if 0<=c<=time);animation=[];durations=[];starts=np.cumsum([0]+[f['ms'] for f in frames])
    for begin,end in zip(cuts,cuts[1:]):
        fi=min(len(frames)-1,int(np.searchsorted(starts,begin,side='right')-1));animation.append(scene(fi,begin-starts[fi]));durations.append(end-begin)
    preview=r/f'{name}-matched-preview-v2.png';assert not preview.exists()
    animation[0].save(preview,save_all=True,append_images=animation[1:],duration=durations,loop=0,disposal=0,blend=0)
    for col,fi in enumerate(range(p['start'],p['start']+4)):
        fi=min(fi,len(frames)-1);im=scene(fi,frames[fi]['ms']/2).resize((256,166),Image.Resampling.NEAREST)
        contact.paste(im,(col*256,row*192+23));draw.text((col*256+4,row*192+4),f'{name} hero frame{fi}',fill='white')
    report.append({'id':name,'sheetSize':[1024,640],'nativeSize':[256,160],'sourceUnion':box,'targetUnion':p['region'],'keys':stats,'heroFrames':len(frames),'attackMs':time,'apngChunks':len(animation),'exact4x':True})
contact.save(r/'matched-contact-v2.png')
(r/'verification-v2.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
