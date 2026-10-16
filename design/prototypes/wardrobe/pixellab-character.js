// All raster artwork comes from actual PixelLab output. Code attaches independent
// wearable textures to per-frame anchors; it does not draw substitute character art.
import {poseFor} from './character.js';
export const SLOTS={hat:{label:'หมวก',choices:[['none','ไม่ใส่'],['hood','ฮู้ดผ้าครีม']]},shirt:{label:'เสื้อ',choices:[['none','ไม่ใส่'],['moss','เสื้อคลุมป่า']]},pants:{label:'กางเกง',choices:[['none','ไม่ใส่'],['charcoal','กางเกงสีถ่าน']]},weapon:{label:'อาวุธ',choices:[['none','ไม่ใส่'],['sword','ดาบนักผจญภัย']]},wrist:{label:'ข้อมือ',choices:[['none','ไม่ใส่'],['bronze','ข้อมือทองแดง']]},boots:{label:'รองเท้า',choices:[['none','ไม่ใส่'],['leather','รองเท้าหนัง']]}};
export const DEFAULT_OUTFIT={hat:'none',shirt:'moss',pants:'charcoal',weapon:'sword',wrist:'bronze',boots:'leather'};
export const ACTIONS={idle:{label:'ยืน',frames:1,duration:1200},walk:{label:'เดิน',frames:9,duration:720},attack:{label:'ตีธรรมดา',frames:9,duration:360,impact:.62,damage:24},slam:{label:'ฟาด',frames:9,duration:620,impact:.50,damage:58,frameMs:[25,45,70,100,25,45,90,140,80]},leap:{label:'กระโดดพุ่งโจมตี',frames:13,duration:820,impact:.69,damage:76}};
export function frameIndex(mode,t){const a=ACTIONS[mode];if(!a.frameMs)return Math.min(a.frames-1,Math.round(t*(a.frames-1)));let elapsed=0;for(let i=0;i<a.frameMs.length;i++){elapsed+=a.frameMs[i];if(t*a.duration<elapsed)return i;}return a.frames-1;}
export function progressForFrame(mode,index){const a=ACTIONS[mode];return a.frameMs?a.frameMs.slice(0,index).reduce((n,v)=>n+v,0)/a.duration:index/Math.max(1,a.frames-1);}
const ROOT=new URL('../../pixellab/chibi-modular/',import.meta.url);
let data;const images=new Map();
export async function loadArt(){const response=await fetch(new URL('assets.json',ROOT));if(!response.ok)throw Error('ไม่พบไฟล์ภาพ PixelLab');data=await response.json();const paths=[...Object.values(data.parts).map(p=>p.file),...Object.values(data.animations).flat().map(p=>p.file)];await Promise.all([...new Set(paths)].map(path=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{images.set(path,im);resolve();};im.onerror=()=>reject(Error(`โหลดภาพไม่สำเร็จ: ${path}`));im.src=new URL(path,ROOT).href;})));for(const key of Object.keys(ACTIONS))ACTIONS[key].frames=data.animations[key].length;return data;}
const make=()=>{const c=document.createElement('canvas');c.width=c.height=128;c.getContext('2d').imageSmoothingEnabled=false;return c;};
function paint(c,image,x,y,w,h,angle=0,px=w/2,py=h/2,source){c.save();c.translate(Math.round(x+32),Math.round(y+32));c.rotate(angle);if(source)c.drawImage(image,...source,-px,-py,w,h);else c.drawImage(image,-px,-py,w,h);c.restore();}
function segment(c,image,a,b,width,source){const angle=Math.atan2(b[1]-a[1],b[0]-a[0]),length=Math.max(3,Math.hypot(b[0]-a[0],b[1]-a[1]));paint(c,image,a[0],a[1],length+2,width,angle,1,width/2,source);}
export class PaperDoll{
  constructor(){this.layers=Object.fromEntries(['body',...Object.keys(SLOTS)].map(k=>[k,make()]));this.frame=make();}
  draw(outfit,mode,t){if(!data)return{image:this.frame,pose:{rootX:0,rootY:0},layers:this.layers};const frames=data.animations[mode],index=frameIndex(mode,t),f=frames[index],motion=poseFor(mode,t),bodyImage=images.get(f.file),dy=f.dy;const at=p=>[p[0],p[1]+dy];for(const c of Object.values(this.layers))c.getContext('2d').clearRect(0,0,128,128);const part=name=>images.get(data.parts[name].file),layer=name=>this.layers[name].getContext('2d');
    if(mode==='slam'){motion.weapon=[.2,-.4,-1.7,-2.1,-.8,.9,1.1,.5,.2][index];motion.rootX=[0,-1,-3,-3,5,13,13,7,0][index];motion.rootY=0;motion.bodyLean=[0,-.025,-.05,-.07,.04,.14,.12,.05,0][index];}
    layer('body').drawImage(bodyImage,32,32+dy);
    // The generated v2 still lowered the near arm. Re-pose the ORIGINAL PixelLab
    // skin texture at reviewed joints for a legible right-handed overhead chop.
    if(mode==='slam'&&index>0&&index<8){const c=layer('body'),torso=at(f.torso),hip=at(f.hip),a=c.getImageData(0,0,128,128);for(let y=Math.floor(f.headBounds[3]+dy+32);y<hip[1]+34;y++)for(let x=32;x<torso[0]+29;x++){const i=(y*128+x)*4,r=a.data[i],g=a.data[i+1],b=a.data[i+2];if(r>135&&r-g>28&&g-b>14)a.data[i+3]=0;}c.putImageData(a,0,0);const shoulder=[torso[0]-5,torso[1]-4],hand=at(f.rightHand),bend=index<4?-5:2,elbow=[(shoulder[0]+hand[0])/2+bend,(shoulder[1]+hand[1])/2];const donor=images.get(data.animations.idle[0].file);segment(c,donor,shoulder,elbow,6,[23,33,6,10]);segment(c,donor,elbow,hand,5,[21,41,6,7]);}
    let hoodPose;
    if(outfit.hat!=='none'){const head=at(f.head),w=f.headBounds?f.headBounds[2]-f.headBounds[0]+8:42,h=f.headBounds?f.headBounds[3]-f.headBounds[1]+14:46;hoodPose=[head[0]-1,head[1]+3,w,h];paint(layer('hat'),part('hoodOpen'),...hoodPose,0,w/2,h/2);}
    if(outfit.pants!=='none'){const c=layer('pants'),im=part('pants'),hip=at(f.hip),a=at(f.frontHip),b=at(f.backHip);const sw=im.width,sh=im.height;paint(c,im,hip[0],hip[1]-1,14,5,0,7,2.5,[0,0,sw,Math.ceil(sh*.35)]);segment(c,im,b,at(f.backKnee),6,[0,Math.floor(sh*.25),Math.ceil(sw/2),Math.ceil(sh*.75)]);segment(c,im,a,at(f.frontKnee),6,[Math.floor(sw/2),Math.floor(sh*.25),Math.ceil(sw/2),Math.ceil(sh*.75)]);}
    if(outfit.boots!=='none'){const c=layer('boots');for(const box of [f.backFoot,f.frontFoot]){const [x0,y0,x1,y1]=box;const w=Math.max(7,x1-x0),h=Math.max(7,y1-y0);paint(c,part('boots'),(x0+x1)/2,y1+dy,w,h,0,w/2,h);}}
    if(outfit.shirt!=='none'){const torso=at(f.torso),hip=at(f.hip),angle=Math.atan2(hip[0]-torso[0],hip[1]-torso[1])*-1;paint(layer('shirt'),part('shirt'),torso[0],torso[1]+2,20,24,angle,10,11);}
    if(outfit.wrist!=='none'){const c=layer('wrist');for(const hand of [f.hand,f.rightHand||f.backHand]){const p=at(hand);paint(c,part('wrist'),p[0],p[1]-1,5,5);}}
    const grippingHand=at(f.rightHand||f.backHand);
    if(outfit.weapon!=='none'){paint(layer('weapon'),part('sword'),grippingHand[0],grippingHand[1],31,11,motion.weapon,7,5.5);}
    const c=this.frame.getContext('2d');c.clearRect(0,0,128,128);c.drawImage(this.layers.hat,0,0);c.drawImage(this.layers.body,0,0);
    // Replace bare feet in the composed result, leaving the base layer immutable.
    if(outfit.boots!=='none'){for(const box of [f.backFoot,f.frontFoot]){const [x0,y0,x1,y1]=box;c.clearRect(Math.floor(x0+32),Math.floor(y0+32+dy),Math.ceil(x1-x0),Math.ceil(y1-y0));}}
    for(const key of ['pants','boots','shirt'])c.drawImage(this.layers[key],0,0);
    if(hoodPose){const [x,y,w,h]=hoodPose;paint(c,part('hoodFront'),x,y,w,h,0,w/2,h/2);}
    // Return bare foreground hands over shirt edges before bracers/weapon.
    if(outfit.shirt!=='none'){for(const hand of [f.hand,f.rightHand||f.backHand]){c.save();const p=at(hand);c.beginPath();c.rect(p[0]+29,p[1]+29,7,6);c.clip();c.drawImage(this.layers.body,0,0);c.restore();}}
    c.drawImage(this.layers.wrist,0,0);c.drawImage(this.layers.weapon,0,0);
    if(outfit.weapon!=='none'){c.save();c.beginPath();c.rect(grippingHand[0]+30,grippingHand[1]+30,5,5);c.clip();c.drawImage(this.layers.body,0,0);c.restore();}
    return{image:this.frame,pose:{...motion,frame:index,anchors:f,weaponHand:'right',grip:grippingHand},layers:this.layers};
  }
}
