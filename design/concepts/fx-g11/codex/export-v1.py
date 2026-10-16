from PIL import Image
from pathlib import Path
import json
import numpy as np

root=Path(__file__).parent
ids=['arc-down','arc-sweep-rl','arc-sweep-lr','arc-up','arc-thrust','arc-spin']
palette=np.array([0,60,154,255],dtype=np.int16)
line=Image.new('RGB',(1024,1536),'black')
native_line=Image.new('RGB',(256,384),'black')
report=[]
for row,name in enumerate(ids):
    raw=Image.open(root/f'{name}-raw-v1.png').convert('RGB')
    sheet=Image.new('RGB',(256,64),'black'); frames=[]; stats=[]
    cw=raw.width/4
    # One scale per entire sheet, preserving source aspect and relative keyframe size.
    factor=min(58/cw,58/raw.height)
    sw,sh=round(cw*factor),round(raw.height*factor)
    for i in range(4):
        cell=raw.crop((round(i*cw),0,round((i+1)*cw),raw.height))
        cell=cell.resize((sw,sh),Image.Resampling.NEAREST)
        v=np.asarray(cell,dtype=np.int16).mean(axis=2)
        v=palette[np.abs(v[:,:,None]-palette).argmin(axis=2)].astype('uint8')
        cell=Image.fromarray(v).convert('RGB')
        frame=Image.new('RGB',(64,64),'black');frame.paste(cell,((64-sw)//2,(64-sh)//2))
        sheet.paste(frame,(i*64,0));frames.append(frame.resize((256,256),Image.Resampling.NEAREST))
        a=np.asarray(frame)[:,:,0];ys,xs=np.where(a>0)
        bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)] if len(xs) else None
        stats.append({'frame':i,'area':int((a>0).sum()),'bounds':bounds,'colourCounts':{str(c):int((a==c).sum()) for c in palette}})
    out=sheet.resize((1024,256),Image.Resampling.NEAREST)
    assert set(out.getdata())<=set((int(v),)*3 for v in palette)
    a=np.asarray(out);assert np.array_equal(a,np.asarray(sheet).repeat(4,0).repeat(4,1))
    for i in range(4):
        c=np.asarray(sheet)[:,i*64:(i+1)*64]
        assert not c[:3].any() and not c[-3:].any() and not c[:,:3].any() and not c[:,-3:].any()
    assert stats[0]['area']<stats[1]['area'] and stats[3]['area']<stats[1]['area']*.25
    for path,im in [(root/f'{name}-v1.png',out),(root/f'{name}-native-v1.png',sheet)]:
        assert not path.exists(),path
        im.save(path)
    preview=root/f'{name}-preview-v1.png';assert not preview.exists()
    frames.append(Image.new('RGB',(256,256),'black'))
    frames[0].save(preview,save_all=True,append_images=frames[1:],duration=[25,40,35,30,600],loop=0,disposal=0,blend=0)
    line.paste(out,(0,row*256));native_line.paste(sheet,(0,row*64))
    peak=stats[1]['bounds'];span=max(peak[2]-peak[0],peak[3]-peak[1])
    report.append({'id':name,'rawSize':list(raw.size),'sheet':f'{name}-v1.png','sheetSize':[1024,256],
        'cellSize':[256,256],'nativeCellSize':[64,64],'cols':4,'frameCount':4,
        'anchorArtPx':[32,32] if name=='arc-spin' else [8,32],
        'suggestedFrameMs':[25,40,35,30],'previewBlackHoldMs':600,'peakSpanArtPx':span,
        'suggestedWorldScaleFor80pxPeak':round(80/span,3),'frames':stats,'exact4xGrid':True,'blackGutters':True})
for path,im in [(root/'lineup-v1.png',line),(root/'lineup-1x-v1.png',native_line)]:
    assert not path.exists();im.save(path)
(root/'verification-v1.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
inventory=[]
for p in sorted(root.glob('*.png')):
    im=Image.open(p);inventory.append({'file':p.name,'size':list(im.size),'animationFrames':getattr(im,'n_frames',1)})
(root/'files-v1.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
print(json.dumps([{'id':r['id'],'rawSize':r['rawSize'],'areas':[f['area'] for f in r['frames']],'peakSpan':r['peakSpanArtPx']} for r in report]))
