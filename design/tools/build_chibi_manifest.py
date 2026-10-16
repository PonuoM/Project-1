"""Record native PixelLab frames and per-frame wardrobe attachment coordinates."""
import json
from pathlib import Path
from PIL import Image

root=Path(__file__).resolve().parents[2]/'design/pixellab/chibi-modular'
def mean(points,default):return [round(sum(p[0] for p in points)/len(points),1),round(sum(p[1] for p in points)/len(points),1)] if points else default
def anatomy(path):
    im=Image.open(path).convert('RGBA');pixels=im.load();box=im.getbbox();dy=61-(box[3]-1)
    hair=[(x,y) for y in range(64) for x in range(64) if pixels[x,y][3] and pixels[x,y][1]>pixels[x,y][0]*1.18 and pixels[x,y][2]>pixels[x,y][0]*1.05]
    left=min(x for x,y in hair);right=max(x for x,y in hair);top=min(y for x,y in hair);bottom=max(y for x,y in hair)
    head=[(left+right)/2,(top+bottom)/2]
    pale=[(x,y) for y in range(bottom,64) for x in range(64) if pixels[x,y][3] and pixels[x,y][0]>155 and pixels[x,y][1]>145 and pixels[x,y][2]>100 and abs(pixels[x,y][0]-pixels[x,y][1])<34]
    if pale:
        neck=min(y for x,y in pale);torso=mean([(x,y) for x,y in pale if y<neck+12],[33,39]);hip=mean([(x,y) for x,y in pale if y>=neck+12],[torso[0],torso[1]+8])
    else:neck=bottom;torso=[head[0]+1,bottom+8];hip=[torso[0],torso[1]+8]
    skin=[(x,y) for y in range(64) for x in range(64) if pixels[x,y][3] and pixels[x,y][0]>135 and pixels[x,y][0]-pixels[x,y][1]>28 and pixels[x,y][1]-pixels[x,y][2]>14]
    legs=[(x,y) for x,y in skin if y>hip[1]+1]
    feetY=max([y for x,y in legs],default=60)
    a=mean([(x,y) for x,y in legs if y>feetY-3 and x<hip[0]],[hip[0]-4,feetY])
    b=mean([(x,y) for x,y in legs if y>feetY-3 and x>=hip[0]],[hip[0]+4,feetY])
    def foot_bounds(points,ankle):
        if not points:return [ankle[0]-4,ankle[1]-3,ankle[0]+5,ankle[1]+2]
        last=max(y for x,y in points);foot=[(x,y) for x,y in points if y>=last-3]
        return [min(x for x,y in foot)-1,min(y for x,y in foot)-2,max(x for x,y in foot)+2,max(y for x,y in foot)+2]
    backFoot=foot_bounds([(x,y) for x,y in legs if x<hip[0]],a)
    frontFoot=foot_bounds([(x,y) for x,y in legs if x>=hip[0]],b)
    ka=mean([(x,y) for x,y in legs if y<=feetY-3 and x<hip[0]],[(a[0]+hip[0]-3)/2,(a[1]+hip[1])/2])
    kb=mean([(x,y) for x,y in legs if y<=feetY-3 and x>=hip[0]],[(b[0]+hip[0]+3)/2,(b[1]+hip[1])/2])
    arms=[(x,y) for x,y in skin if y>=neck+2 and y<=hip[1]+1]
    far=[(x,y) for x,y in arms if x>torso[0]+6]
    near=[(x,y) for x,y in arms if x<torso[0]-5]
    def hand(points,default):
        if not points:return default
        lowest=max(y for x,y in points)
        return mean([(x,y) for x,y in points if y>=lowest-2],default)
    handFar=hand(far,[torso[0]+9,hip[1]-1]);handNear=hand(near,[torso[0]-9,hip[1]-1])
    return {'file':str(path.relative_to(root)).replace('\\','/'),'dy':dy,'head':head,'headBounds':[left,top,right+1,bottom+1],'torso':torso,'hip':hip,
        'frontHip':[hip[0]+3,hip[1]],'backHip':[hip[0]-3,hip[1]],'frontKnee':kb,'backKnee':ka,'frontAnkle':b,'backAnkle':a,
        'hand':handFar,'backHand':handNear,'frontFoot':frontFoot,'backFoot':backFoot,'elbow':[(torso[0]+5+handFar[0])/2,(neck+4+handFar[1])/2]}

manifest={'provenance':'PixelLab generate-image-v2 and animate-with-text-v3; original jobs/prompts/results retained',
    'nativeBodySize':[64,64],'layerSize':[128,128],'padding':32,'footOrigin':[64,94],
    'parts':json.loads((root/'parts/provenance.json').read_text()),'animations':{}}
manifest['animations']['idle']=[anatomy(root/'base/candidate-01.png')]
for name in ['walk','attack','slam','leap']:
    folder='slam-v2' if name=='slam' and (root/'slam-v2/frame-01.png').exists() else name
    paths=sorted((root/folder).glob('frame-*.png'))
    if not paths:raise SystemExit(f'Missing actual PixelLab {name} frames.')
    manifest['animations'][name]=[anatomy(p) for p in paths]
# Explicitly reviewed main-hand locations on the generated attack sheet.
attackHands=[[42,45],[45,44],[49,43],[47,38],[50,33],[51,37],[48,44],[45,45],[42,45]]
for frame,hand in zip(manifest['animations']['attack'],attackHands):frame['hand']=hand
slamHands=[[42,45],[46,45],[50,36],[48,25],[40,33],[41,33],[42,44],[48,38],[45,45],[44,45],[42,45]]
for frame,hand in zip(manifest['animations']['slam'],slamHands):frame['hand']=hand
for frames in manifest['animations'].values():
    for frame in frames:frame['rightHand']=frame['backHand'];frame['weaponHand']='right (near arm in right-facing side view)'
rightHands={'idle':[[24,45]],'walk':[[24,45],[25,45],[31,44],[35,44],[34,44],[34,45],[33,44],[25,44],[24,45]],
    'attack':[[24,45],[24,44],[19,43],[18,38],[12,33],[15,36],[19,43],[23,45],[24,45]]}
for action,hands in rightHands.items():
    for frame,hand in zip(manifest['animations'][action],hands):frame['rightHand']=hand
manifest['parts']['hoodOpen']={'file':'parts/hood-open.png','source':'parts/hood.png','processing':'transparent face opening'}
slamRight=[[24,45],[21,40],[20,25],[23,16],[44,27],[49,48],[48,50],[33,45],[24,45]]
for frame,hand in zip(manifest['animations']['slam'],slamRight):frame['rightHand']=hand
manifest['parts']['hoodFront']={'file':'parts/hood-front.png','source':'parts/hood.png','processing':'foreground cloth occlusion mask'}
(root/'assets.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print({k:len(v) for k,v in manifest['animations'].items()})
