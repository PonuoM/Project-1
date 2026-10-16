from PIL import Image,ImageDraw
from pathlib import Path
import json,numpy as np
r=Path(__file__).parent
plans=json.loads((r/'timing-plan-v1.json').read_text())
sources={e['move']:e for e in json.loads((r/'motion-analysis-v1.json').read_text())} if False else {e['move']:e for e in []}
sources={e['move']:e for e in json.loads((r/'motion-analysis-v1.json').read_text())}
pal=np.array([0,60,154,255],dtype=np.int16)
results=[]
contact=Image.new('RGB',(1024,len(plans)*192),(25,24,36));d=ImageDraw.Draw(contact)
def key_at(plan,frames,fi,acc=0):
    elapsed=sum(f['ms'] for f in frames[:fi])+acc
    starts=plan.get('starts',[plan['start']])
    if plan.get('cycle'):
        if not plan['start']<=fi<plan['end']:return None
        return (fi-plan['start'])%4
    for start in reversed(starts):
        age=elapsed-sum(f['ms'] for f in frames[:start])
        if age<0:continue
        for key,duration in enumerate(plan['keys']):
            if age<duration:return key
            age-=duration
        return None
    return None
for row,p in enumerate(plans):
    name=p['id'];raw=Image.open(r/f'{name}-raw-v1.png').convert('RGB');cw,ch=raw.width/2,raw.height/2
    native=Image.new('RGB',(256,160),'black');keys=[];bounds=[]
    for k in range(4):
        x,y=k%2,k//2
        im=raw.crop((round(x*cw),round(y*ch),round((x+1)*cw),round((y+1)*ch))).resize((128,80),Image.Resampling.NEAREST)
        a=np.asarray(im,dtype=np.int16).mean(axis=2);a=pal[np.abs(a[:,:,None]-pal).argmin(axis=2)].astype('uint8')
        a[:2]=0;a[:,:2]=0;a[:,-2:]=0;a[-1:]=0
        im=Image.fromarray(a).convert('RGB');native.paste(im,(x*128,y*80));keys.append(im)
        yy,xx=np.where(a>0);bounds.append({'key':k,'bounds':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],'area':int(len(xx))})
    for path,im in [(r/f'{name}-native-v1.png',native),(r/f'{name}-v1.png',native.resize((1024,640),Image.Resampling.NEAREST))]:
        assert not path.exists();im.save(path)
    source=sources[name];frames=source['frames'];strip=Image.open(Path(source['strip']).with_name('strip-fast-blade-7.png')).convert('RGBA')
    animation=[]
    for fi,f in enumerate(frames):
        stage=Image.new('RGBA',(160,104),(25,24,36,255));dr=ImageDraw.Draw(stage);dr.line((0,96,160,96),fill=(75,63,85))
        hero=strip.crop((fi*128,0,(fi+1)*128,80));key=key_at(p,frames,fi)
        layer=None
        if key is not None:
            a=np.asarray(keys[key]).copy();alpha=np.where(a[:,:,0]>0,255,0).astype('uint8');layer=Image.fromarray(np.dstack((a,alpha)))
            if p.get('cycle'):
                back=layer.copy();back.paste((0,0,0,0),(0,58,128,80));stage.alpha_composite(back,(16,16))
        stage.alpha_composite(hero,(16,16))
        if layer is not None:
            if p.get('cycle'):layer.paste((0,0,0,0),(0,0,128,58))
            stage.alpha_composite(layer,(16,16))
        animation.append(stage.convert('RGB').resize((480,312),Image.Resampling.NEAREST))
    animation[0].save(r/f'{name}-matched-preview-v1.png',save_all=True,append_images=animation[1:],duration=[f['ms'] for f in frames],loop=0,disposal=0,blend=0)
    samples=[p['start'],min(p['start']+1,len(frames)-1),min(p['start']+2,len(frames)-1),min(p['start']+3,len(frames)-1)]
    for col,fi in enumerate(samples):
        im=animation[fi].resize((256,166),Image.Resampling.NEAREST);contact.paste(im,(col*256,row*192+23));d.text((col*256+4,row*192+4),f'{name} hero frame{fi}',fill='white')
    results.append({'id':name,'rawSize':list(raw.size),'sheetSize':[1024,640],'nativeSize':[256,160],'keys':bounds,'frames':len(frames),'attackMs':sum(f['ms'] for f in frames)})
contact.save(r/'matched-contact-v1.png')
(r/'verification-v1.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results))
