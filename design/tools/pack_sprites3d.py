"""Prompt 8.1: native 3D layers + original pixel head. No image rotation or AI calls."""
from pathlib import Path
import json, math
import numpy as np
import OpenEXR
from PIL import Image, ImageDraw, PngImagePlugin
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'design/sprites3d/adventurer'; RAW=OUT/'raw'; W=H=96
meta=json.loads((RAW/'render.json').read_text())
base=Image.open(ROOT/'design/pixellab/chibi-modular/base/candidate-01.png').convert('RGBA')
ref=Image.open(ROOT/'design/pixellab/chibi-modular/reference-native.png').convert('RGBA')
# Claude (Prompt 8.1 takeover): Blender now renders DATA. R = material id, G = light band (0/.5/1).
# Each id is painted with a dark/mid/light ramp sampled from reference-native.png and base/candidate-01.png,
# so the 3D body uses exactly the colours of the original character instead of nearest-colour guesses.
RAMPS={ # id: (dark, mid, light)
 1:('#B47356','#E09673','#F7C79E'),  # skin (base)
 2:('#CAAD92','#E2D3B6','#F4EDD3'),  # underwear (base)
 3:('#5D613E','#7F7D48','#A19952'),  # olive tunic (reference)
 4:('#A79075','#DDC7A7','#FBEED7'),  # cream scarf (reference)
 5:('#944634','#D16A48','#E98A5E'),  # red sash / plume (reference)
 6:('#825935','#BF8E4F','#F1C874'),  # brass (reference)
 7:('#423430','#584840','#7C6A5E'),  # dark shorts (reference)
 8:('#4A3226','#6E4B33','#A07243'),  # brown leather boots (reference)
 9:('#9B9590','#D8D4D2','#FFFDF8'),  # blade (reference)
 10:('#55647A','#8794A7','#C9D3DC'), # steel plate / greaves (tokens)
 11:('#593F7A','#8A6BB0','#B19AD8'), # plum (tokens)
 12:('#3A2620','#5A3A2C','#7A5240'), # grip leather
 13:('#4E5658','#7C8585','#AEB4B2'), # iron
}
hexrgb=lambda h:[int(h[i:i+2],16) for i in (1,3,5)]
RAMP=np.zeros((256,3,3),np.uint8)
for mid,ramp in RAMPS.items():RAMP[mid]=[hexrgb(h) for h in ramp]
palette=np.array(sorted({tuple(hexrgb(h)) for ramp in RAMPS.values() for h in ramp}),dtype=np.int32)
outline=np.array([23,6,4],dtype=np.uint8)  # the head's own outline colour (base/candidate-01.png)
INNER_STEP=.10   # world units: a nearer surface this much in front draws a line on the farther one
RING_EPS=.02     # outline ring sits just behind the surface it outlines
HEAD_FRONT=.35   # a weapon/arm pixel this much nearer than the head bone is drawn over the 2D head
FRONT_KEYS=('body','wrist_','weapon_')
HEAD=ROOT/'design/3d/pixel-head'; HEAD.mkdir(parents=True,exist_ok=True)
cut=base.crop((13,1,51,31))
variants={}
for name in ['neutral','forward','back','hurt']:
    head=Image.new('RGBA',(44,36)); src=np.array(cut); dst=np.array(head)
    # Authored integer row edits: keep each original pixel, redraw silhouette with stepped tilt.
    # This is an OFFLINE pixel variant, never affine rotation or runtime stretching.
    for y in range(30):
        shift=0 if name=='neutral' else (2 if y<8 else 1 if y<17 else 0 if y<24 else -1)
        if name=='back': shift=-shift
        if name=='hurt': shift=1 if y<16 else 0
        dst[y+1,3+shift:41+shift]=src[y]
    variants[name]=dst
    Image.fromarray(dst).save(HEAD/f'head_{name}.png')
# Hat variants are pixel-authored around exactly the same 44x36 head coordinate system.
hats={}
for variant,head in variants.items():
    for kind in ['hood','helm']:
        im=Image.new('RGBA',(44,36));d=ImageDraw.Draw(im)
        if kind=='hood':
            d.line([(4,20),(2,13),(6,7),(12,3),(23,0),(32,3),(40,10),(42,20)],fill='#241812',width=3)
            d.line([(4,19),(3,13),(7,7),(13,4),(23,1),(32,4),(39,10)],fill='#D6C6A3',width=2)
            d.line([(7,6),(13,3),(23,0),(31,3)],fill='#F2E5C8',width=1)
            d.polygon([(4,22),(7,28),(15,33),(29,34),(36,30),(40,24),(38,30),(31,35),(13,35),(6,31)],fill='#D6C6A3')
        else:
            d.polygon([(3,13),(6,6),(14,1),(29,1),(37,6),(41,14),(39,18),(34,16),(30,11),(13,11),(7,16)],fill='#241812')
            d.polygon([(4,12),(7,7),(14,2),(28,2),(36,7),(39,13),(34,14),(30,10),(13,10),(7,14)],fill='#7C8585')
            d.line([(9,6),(15,3),(27,3),(34,7)],fill='#C8C7AA',width=2)
            d.line([(15,9),(29,9),(35,13)],fill='#515B61',width=2)
            d.polygon([(21,1),(20,0),(21,-2),(26,-2),(28,0),(27,1)],fill='#934D39')
        # Variant-specific pixel offsets redraw the brim with the head's authored angle bucket.
        if variant!='neutral':
            a=np.array(im);out=np.zeros_like(a)
            for y in range(36):
                shift=(1 if y<18 else 0)*(-1 if variant=='back' else 1)
                if shift>0:out[y,1:]=a[y,:-1]
                elif shift<0:out[y,:-1]=a[y,1:]
                else:out[y]=a[y]
            im=Image.fromarray(out)
        hats[(kind,variant)]=np.array(im);im.save(HEAD/f'hat_{kind}_{variant}.png')
def quantize(im):
    """Paint a data render: material id (R) + light band (G) -> reference ramp colour."""
    a=np.array(im.convert('RGBA'));solid=a[:,:,3]>=128;ids=a[:,:,0];band=np.where(a[:,:,1]<64,0,np.where(a[:,:,1]<192,1,2))
    out=np.zeros_like(a);out[:,:,:3]=RAMP[ids,band];out[:,:,3]=np.where(solid,255,0);out[~solid]=0
    unknown=solid&(ids==0)|solid&(ids>13)
    if unknown.any():raise SystemExit(f'unknown material id in render: {sorted(set(ids[unknown].tolist()))}')
    return out

def shifted(a,dy,dx,fill):
    out=np.full_like(a,fill);h,w=a.shape[:2]
    out[max(0,dy):h+min(0,dy),max(0,dx):w+min(0,dx)]=a[max(0,-dy):h+min(0,-dy),max(0,-dx):w+min(0,-dx)]
    return out

def lined(a,z):
    """Outlines baked per layer so any outfit combination still gets them through the depth test:
    a 1 px ring just outside the layer (depth = the surface it touches, slightly behind) plus inner lines
    where a nearer part of the same layer overlaps a farther one (arm in front of the torso)."""
    a=a.copy();solid=a[:,:,3]>0;zz=np.where(solid,z,np.inf);inner=np.zeros_like(solid);ring=np.zeros_like(solid);ringz=np.full(z.shape,np.inf,dtype=np.float64)
    for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
        nz=shifted(zz,dy,dx,np.inf);ns=shifted(solid,dy,dx,False)
        inner|=solid&(nz<zz-INNER_STEP)
        edge=(~solid)&ns;ring|=edge;ringz=np.where(edge,np.minimum(ringz,nz+RING_EPS),ringz)
    a[inner,:3]=outline;a[ring,:3]=outline;a[ring,3]=255
    return a,np.where(ring,ringz,z)

def outlined(a):
    mask=a[:,:,3]>0;expanded=mask.copy()
    for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:expanded|=np.roll(mask,(dy,dx),(0,1))
    out=a.copy();border=expanded&~mask;out[border,:3]=outline;out[border,3]=255;return out

def save(path,a,provenance):
    info=PngImagePlugin.PngInfo();info.add_text('provenance',provenance);Image.fromarray(a).save(path,pnginfo=info)
raw={k:quantize(Image.open(RAW/f'{k}.png')) for k in meta['groups']}
depth={k:next(iter(OpenEXR.File(str(RAW/f'{k}_depth_.exr')).channels().values())).pixels for k in meta['groups']}
refs={k:quantize(Image.open(RAW/f'ref_{k}.png')) for k in ['cloth','iron']}
keys=meta['groups'];stack=np.stack([np.where(raw[k][:,:,3]>0,depth[k],1e12) for k in keys]);rank=np.argsort(np.argsort(stack,axis=0),axis=0)+1
ranks={k:rank[i].astype(np.uint8) for i,k in enumerate(keys)}
plain_raw={k:v.copy() for k,v in raw.items()};plain_depth=dict(depth);plain_ranks=ranks
for k in keys:raw[k],depth[k]=lined(raw[k],depth[k])
headD=np.full(raw['body'].shape[1],np.inf)
for f in meta['frames']:headD[f['cell']*W:(f['cell']+1)*W]=meta['anchors'][f['animation']][f['index']]['headDepth']
headY=np.full(raw['body'].shape[1],-np.inf)
for f in meta['frames']:headY[f['cell']*W:(f['cell']+1)*W]=meta['anchors'][f['animation']][f['index']]['head'][1]
# Body pixels may cover the head only above the chin (a raised arm), never the chest/neck under the face.
aboveChin=np.arange(raw['body'].shape[0])[:,None]<headY[None,:]-6
front={k:(raw[k][:,:,3]>0)&(depth[k]<headD[None,:]-HEAD_FRONT)&(aboveChin if k=='body' else True) if k.startswith(FRONT_KEYS) else np.zeros(raw[k].shape[:2],bool) for k in keys}
stack=np.stack([np.where(raw[k][:,:,3]>0,depth[k],1e12) for k in keys]);rank=np.argsort(np.argsort(stack,axis=0),axis=0)+1
ranks={k:rank[i].astype(np.uint8) for i,k in enumerate(keys)}
items={'hat':['hood','helm'],'chest':['tunic','plate','plum'],'legs':['trousers','leather'],'boots':['boots','greaves'],'wrist':['bracer','cuff'],'weapon':['sword','sabre']}
outfits={'cloth':{'hat':'none','chest':'tunic','legs':'trousers','boots':'boots','wrist':'bracer','weapon':'sword'},'iron':{'hat':'helm','chest':'plate','legs':'leather','boots':'greaves','wrist':'cuff','weapon':'sabre'}}
manifest={'version':2,'frameWidth':W,'frameHeight':H,'footOrigin':[48,64],'footRow':63,'animations':{},'body':{},'head':{},'layers':{},'anchors':meta['anchors'],'outline':outline.tolist(),'palette':palette.tolist(),'drawOrder':{'default':['body','legs','boots','chest','wrist','weapon','head','hat'],'perFrame':{},'occlusion':'3D surfaces use per-pixel native depth. Original 2D head and fitted hat overlay at snapped bone anchor.'},'source':'Hybrid: original PixelLab head (existing AI asset) + NON-AI KayKit CC0 rig/body/animations + authored equipment','renderSeconds':meta['renderSeconds'],'camera':meta['camera']}
qa={'frames':[],'referenceDifferences':{},'renderSeconds':meta['renderSeconds'],'weaponGripFailures':0,'edgeFrames':[],'feetFailures':[],'colorsPerItem':{},'headSource':'base/candidate-01.png unchanged; 38x30 crop, offline integer pixel edits','noNewAICalls':True,'note':'3D-only composite compared to independently rendered full outfit. Hybrid reference adds the same original head and authored hat to that independent render.'}

def paste(dst,src,x,y):
    h,w=src.shape[:2];x0=max(0,x);y0=max(0,y);x1=min(W,x+w);y1=min(H,y+h)
    if x1<=x0 or y1<=y0:return dst
    s=src[y0-y:y1-y,x0-x:x1-x];d=dst[y0:y1,x0:x1];mask=s[:,:,3]>0;d[mask]=s[mask];return dst

def head_layer(name,index,hat=None):
    a=meta['anchors'][name][index];variant=a['headVariant'];cx,cy=a['head'];x=round(cx)-22;y=round(cy)-29
    dst=np.zeros((H,W,4),np.uint8);paste(dst,hats[(hat,variant)] if hat else variants[variant],x,y);return dst

def composite(keys,x0,x1,images=None,order=None,fronts=None):
    images=images or raw;order=order or ranks
    best=np.full((H,W),255,np.uint8);a=np.zeros((H,W,4),np.uint8);front=np.zeros((H,W),bool)
    for key in keys:
        image=images[key][:,x0:x1];z=order[key][:,x0:x1];use=(image[:,:,3]>0)&(z<best);a[use]=image[use];best[use]=z[use]
        if fronts is not None:front[use]=fronts[key][:,x0:x1][use]
    return (a,front) if fronts is not None else a

for name,spec in meta['animations'].items():
    indices=[f['cell'] for f in meta['frames'] if f['animation']==name];n=len(indices);columns=[(i*W,(i+1)*W) for i in indices]
    manifest['animations'][name]={'frames':n,'frameMs':spec['frameMs'],'impact':spec['impact'],'loop':spec['loop'],'sourceClip':spec['action']}
    for key in keys:
        sheet=np.concatenate([raw[key][:,x0:x1] for x0,x1 in columns],1);z=np.concatenate([ranks[key][:,x0:x1] for x0,x1 in columns],1)
        file=f'{key}_{name}.png';save(OUT/file,sheet,'NON-AI native Blender render');dimg=np.zeros((*z.shape,4),np.uint8);dimg[:,:,0]=z;dimg[:,:,1]=np.concatenate([front[key][:,x0:x1] for x0,x1 in columns],1)*255;dimg[:,:,3]=sheet[:,:,3];save(OUT/f'depth_{key}_{name}.png',dimg,'Native camera depth rank')
        qa['colorsPerItem'][key]=len(np.unique(sheet[sheet[:,:,3]>0,:3],axis=0))
        if key=='body':manifest['body'][name]={'file':file,'depth':f'depth_{key}_{name}.png'};continue
        slot,item=key.split('_',1);rec=manifest['layers'].setdefault(slot,{}).setdefault(item,{'files':{},'depth':{},'hidesBody':{}});rec['files'][name]=file;rec['depth'][name]=f'depth_{key}_{name}.png'
        masks=[]
        for x0,x1 in columns:
            mask=(plain_raw[key][:,x0:x1,3]>0)&(plain_raw['body'][:,x0:x1,3]>0)&(plain_depth[key][:,x0:x1]<=plain_depth['body'][:,x0:x1]);a=np.zeros((H,W,4),np.uint8);a[mask]=255;masks.append(a)
        mfile=f'mask_{key}_{name}.png';save(OUT/mfile,np.concatenate(masks,1),'Body coverage mask');rec['hidesBody'][name]=mfile
    hsheet=np.concatenate([head_layer(name,i) for i in range(n)],1);save(OUT/f'head_{name}.png',hsheet,'Existing AI-generated character head, offline pixel-edited variants');manifest['head'][name]=f'head_{name}.png'
    for item in items['hat']:
        sheet=np.concatenate([head_layer(name,i,item) for i in range(n)],1);file=f'hat_{item}_{name}.png';save(OUT/file,sheet,'Authored pixel hat fitted per head variant')
        ds=np.zeros_like(sheet);ds[:,:,0]=1;ds[:,:,3]=sheet[:,:,3];save(OUT/f'depth_hat_{item}_{name}.png',ds,'2D overlay')
        save(OUT/f'mask_hat_{item}_{name}.png',np.zeros_like(sheet),'Hat does not cover 3D body')
        rec=manifest['layers'].setdefault('hat',{}).setdefault(item,{'files':{},'depth':{},'hidesBody':{}});rec['files'][name]=file;rec['depth'][name]=f'depth_hat_{item}_{name}.png';rec['hidesBody'][name]=f'mask_hat_{item}_{name}.png'
    for outfit,selection in outfits.items():
        selected=['body']+[f'{s}_{i}' for s,i in selection.items() if s!='hat'];comps=[];references=[];diffs=[]
        for i,(x0,x1) in enumerate(columns):
            plain=composite(selected,x0,x1,plain_raw,plain_ranks);r=refs[outfit][:,x0:x1].copy();difference=int(np.any(plain!=r,2).sum());diffs.append(difference)
            c,cf=composite(selected,x0,x1,fronts=front)  # cf: winning pixel is a weapon/arm in front of the head
            head=head_layer(name,i);hm=(head[:,:,3]>0)&~cf;c[hm]=head[hm];r[head[:,:,3]>0]=head[head[:,:,3]>0]
            if selection['hat']!='none':
                hat=head_layer(name,i,selection['hat']);hm=(hat[:,:,3]>0)&~cf;c[hm]=hat[hm];r[hat[:,:,3]>0]=hat[hat[:,:,3]>0]
            r=outlined(r);comps.append(c);references.append(r)  # c already carries the baked per-layer outlines
            a=meta['anchors'][name][i];distance=math.dist(a['rightHand'],a['weaponGrip']);qa['weaponGripFailures']+=int(distance>1)
            bounds=Image.fromarray(c).getbbox();edge=bool(c[0,:,3].any() or c[-1,:,3].any() or c[:,0,3].any() or c[:,-1,3].any())
            if edge:qa['edgeFrames'].append([name,i,outfit])
            feet=Image.fromarray(composite(['body']+[k for k in selected if k.startswith('boots_')],x0,x1,plain_raw,plain_ranks)).getbbox();bottom=feet[3]-1 if feet else None  # feet only; a lowered sword is not a foot
            if name!='leap' and bottom!=62:qa['feetFailures'].append([name,i,outfit,bottom])  # feet on 62, their baked outline on 63
            qa['frames'].append({'animation':name,'frame':i,'outfit':outfit,'compositeDifferingPixels3D':difference,'bounds':bounds,'bottomRow':bottom,'gripDistancePx':distance,'rightHandBone':a['rightHandBone'],'headVariant':a['headVariant']})
        save(OUT/f'ref_{outfit}_{name}.png',np.concatenate(references,1),'Independent 3D outfit render plus original 2D head');save(OUT/f'composite_{outfit}_{name}.png',np.concatenate(comps,1),'Composited exported hybrid layers');qa['referenceDifferences'][f'{outfit}_{name}']=diffs
    fx=Image.new('RGBA',(W*n,H));d=ImageDraw.Draw(fx)
    if spec['impact'] is not None:
        i=max(0,spec['impact']-1);x,y=meta['anchors'][name][spec['impact']]['rightHand'];cx=i*W+round(x);cy=round(y)
        d.arc((cx-18,cy-28,cx+36,cy+25),270,440,fill='#EBD8AB',width=3)
    save(OUT/f'fx_{name}.png',np.array(fx),'Authored separate pixel FX');manifest['animations'][name]['fx']={'file':f'fx_{name}.png','anchor':'rightHand','impact':spec['impact']}
(OUT/'sprites3d.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');(ROOT/'design/qa/sprites3d.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
sheet=Image.new('RGBA',(W*4*3,H*4*4),(32,40,43,255));d=ImageDraw.Draw(sheet)
# Reference-native is 5x pixel art: restore native size by nearest-neighbor only for comparison.
reference=ref.resize((64,64),Image.Resampling.NEAREST)
for row,anim in enumerate(['idle','walk','attack','slam']):
    sheet.alpha_composite(reference.resize((256,256),Image.Resampling.NEAREST),(40,row*384+64));d.text((12,row*384+12),'ORIGINAL REFERENCE',fill='#F2E5C8')
    for col,outfit in enumerate(['cloth','iron'],1):
        im=Image.open(OUT/f'composite_{outfit}_{anim}.png');idx=manifest['animations'][anim]['impact'] or 0;frame=im.crop((idx*W,0,(idx+1)*W,H));sheet.alpha_composite(frame.resize((384,384),Image.Resampling.NEAREST),(col*384,row*384));d.text((col*384+12,row*384+12),f'{outfit} / {anim}',fill='#F2E5C8')
sheet.save(OUT/'contact-sheet.png')
print('Packed',len(meta['frames']),'poses;',sum(sum(x) for x in qa['referenceDifferences'].values()),'reference differences;',len(qa['edgeFrames']),'edge frames;',len(qa['feetFailures']),'feet failures')
