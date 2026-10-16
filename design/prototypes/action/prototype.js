/* Isolated visual simulation: no game APIs, saves, production sheets or reward mutations.
   Hero art is switchable: PixelLab swordsman (cleaned copy or untouched originals from design/pixellab/swordsman)
   or the earlier code-drawn knight. PixelLab frame size, count, fps, impact frame and hit stop are read from that
   folder's animation.json; nothing about the sheet is assumed here. */
const canvas = document.getElementById('scene'), ctx = canvas.getContext('2d');
ctx.imageSmoothingEnabled = false;
const $ = id => document.getElementById(id);
const colors = {ink:'#171C2C',outline:'#252C40',slate:'#343E52',metal:'#55647A',silver:'#B8C4CF',cream:'#F4EAD5',white:'#FFF9ED',wood:'#593A31',bark:'#8B5739',gold:'#FFD875',brass:'#D69B37',glint:'#FFF0AC',red:'#D75B60',green:'#365945',leaf:'#6DB586',light:'#B6E2B1',blue:'#314F79'};
const specs = {knight_idle:[64,64,4,8],knight_walk:[64,64,6,14],knight_slash:[64,64,6,24],knight_skill:[64,64,8,24],foe_idle:[48,48,4,8],foe_walk:[48,48,6,12],foe_death:[48,48,4,12]};
const PIXELLAB = '../../pixellab/swordsman/';
const ARTS = {
  clean:{label:'PixelLab · ปรับแล้ว',dir:PIXELLAB+'cleaned/'},
  raw:{label:'PixelLab · ต้นฉบับ',dir:PIXELLAB},
  code:{label:'ภาพโค้ดเดิม'}
};
const ENGAGE = {code:66,pixellab:50}; // the PixelLab sword reaches ~27px in front of the hero's center
const art = {}, rigs = {}, variants = ['A','B','C'], sizes = {A:[560,180],B:[800,160],C:[560,240]};
// Where the camera keeps the hero. B's in-scene action bar covers the bottom-left, so the hero stands right of it.
const heroView = {A:.29,B:.4,C:.29};
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
if(reduced) $('shake').checked = false;
let variant = 'A', artKey = 'clean', stillFile = 'candidate-11.png', state, previousTime = 0, simTime = 0, paused = false, cameraPan = 0, follow = true, dragging = false;
let particles = [], numbers = [], bursts = [], waves = [], audio;
function rig(){return artKey==='code'?null:rigs[artKey]||null;}
function engageGap(){return rig()?ENGAGE.pixellab:ENGAGE.code;}
function reset(){state={hero:180,enemy:400,hp:120,mode:'walk',action:null,hold:0,shake:0,flash:0,flinch:0,wait:0,cooldown:0,kills:0,gold:12345,boxes:3,stage:12,combo:0,death:0};simTime=0;particles=[];numbers=[];bursts=[];waves=[];cameraPan=0;follow=true;}
reset();
// Scanline polygons: integer rasterization keeps scene art crisp without antialiasing.
function rect(x,y,w,h,c){ctx.fillStyle=c;ctx.fillRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h));}
function poly(points,c){ctx.fillStyle=c;const lo=Math.ceil(Math.min(...points.map(p=>p[1]))),hi=Math.floor(Math.max(...points.map(p=>p[1])));for(let y=lo;y<=hi;y++){const xs=[];for(let i=0;i<points.length;i++){const a=points[i],b=points[(i+1)%points.length];if((a[1]<=y&&b[1]>y)||(b[1]<=y&&a[1]>y))xs.push(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]));}xs.sort((a,b)=>a-b);for(let i=0;i+1<xs.length;i+=2)ctx.fillRect(Math.ceil(xs[i]),y,Math.max(1,Math.floor(xs[i+1])-Math.ceil(xs[i])+1),1);}}
function random(n){return Math.abs(Math.sin(n*127.1+311.7)*43758.5453)%1;}
/* Draw one frame with its feet (bottom-center) at x,y. sx/sy squash around the feet; tint = hit flash. */
function drawFrame(img,frame,w,h,x,y,{sx=1,sy=1,tint=false}={}){const dw=Math.round(w*sx),dh=Math.round(h*sy),dx=Math.round(x-dw/2),dy=Math.round(y-dh);ctx.drawImage(img,frame*w,0,w,h,dx,dy,dw,dh);if(tint){const source=document.createElement('canvas');source.width=w;source.height=h;const c=source.getContext('2d');c.drawImage(img,frame*w,0,w,h,0,0,w,h);c.globalCompositeOperation='source-in';c.fillStyle=colors.cream;c.fillRect(0,0,w,h);ctx.drawImage(source,dx,dy,dw,dh);}}
function sprite(key,frame,x,y,opts){const [w,h,n]=specs[key];drawFrame(art[key],Math.max(0,Math.min(n-1,Math.floor(frame))),w,h,x,y,opts);}
function pixelText(text,x,y,color,size=13){ctx.font=`bold ${size}px Tahoma`;ctx.textAlign='center';ctx.lineWidth=3;ctx.strokeStyle=colors.ink;ctx.strokeText(text,Math.round(x),Math.round(y));ctx.fillStyle=color;ctx.fillText(text,Math.round(x),Math.round(y));}
function tree(x,base,height,seed,near){
  const top=base-height,trunk=near?colors.wood:colors.slate,leaf=near?colors.green:colors.blue;
  // Bent trunks, forks and irregular stepped broadleaf crowns rather than cone icons.
  poly([[x-9,base],[x-4,base-25],[x-7,top+37],[x-3,top+22],[x+4,top+23],[x+2,base-47],[x+6,base-16],[x+13,base]],trunk);
  poly([[x-4,top+54],[x-25,top+29],[x-22,top+20],[x+1,top+43],[x+23,top+22],[x+27,top+27],[x+4,top+61]],trunk);
  if(near){rect(x-4,top+44,2,height-51,colors.bark);rect(x+3,base-21,2,17,colors.bark);rect(x-12,base-2,26,2,colors.green);}
  for(let k=0;k<4;k++){const cx=x+[-27,0,24,-8][k],cy=top+[18,2,21,32][k],w=[27,32,29,25][k],h=[17,22,19,16][k];
    poly([[cx-w+5,cy],[cx-w+12,cy-5],[cx-9,cy-7],[cx-2,cy-11],[cx+12,cy-8],[cx+w-9,cy-4],[cx+w-3,cy+2],[cx+w,cy+9],[cx+w-5,cy+h-3],[cx+12,cy+h],[cx+3,cy+h+4],[cx-8,cy+h],[cx-w+3,cy+h-3],[cx-w,cy+8]],leaf);
    if(near){for(let j=0;j<6;j++){const px=cx-w+8+j*7,py=cy-2+Math.round(random(seed*13+k*7+j)*5);rect(px,py,5,2,colors.leaf);}rect(cx-w+8,cy+7,7,2,colors.leaf);}
  }
}
function background(cam,ground){const w=canvas.width,h=canvas.height;rect(0,0,w,h,colors.ink);rect(0,0,w,Math.round(h*.53),colors.outline);
  // A small moon and broken clouds provide a light anchor without filling the desktop.
  const mx=Math.round(w*.74-cam*.045)% (w+100);rect(mx,24,18,18,colors.silver);rect(mx-3,29,24,8,colors.silver);rect(mx+8,22,12,12,colors.outline);rect(mx-14,43,64,4,colors.slate);
  for(let layer=0;layer<2;layer++){const p=.11+layer*.17;const offset=-cam*p;const step=130-layer*20;for(let i=Math.floor(cam*p/step)-1;i<Math.ceil((cam*p+w)/step)+1;i++){const x=i*step+offset;poly([[x-30,ground],[x+50,ground-60-layer*22-random(i+layer)*25],[x+140,ground]],layer?colors.blue:colors.slate);}}
  for(let i=Math.floor(cam*.5/80)-1;i<Math.ceil((cam*.5+w)/80)+1;i++)tree(i*80-cam*.5,ground-2,90+random(i)*50,i,false);
  for(let i=Math.floor(cam*.82/155)-1;i<Math.ceil((cam*.82+w)/155)+1;i++)tree(i*155+20-cam*.82,ground+4,115+random(i)*45,i,true);
  // Half-buried stone arches along the route.
  for(let i=Math.floor(cam/380)-1;i<Math.ceil((cam+w)/380)+1;i++){const x=i*380+265-cam;rect(x,ground-49,11,49,colors.slate);rect(x+37,ground-38,12,38,colors.slate);rect(x-2,ground-52,17,5,colors.metal);rect(x-2,ground-54,52,5,colors.slate);rect(x+4,ground-40,2,17,colors.metal);rect(x+1,ground-4,15,4,colors.green);}
  rect(0,ground,w,h-ground,colors.wood);rect(0,ground,w,4,colors.green);rect(0,ground+4,w,2,colors.ink);
  for(let i=Math.floor(cam/32)-1;i<Math.ceil((cam+w)/32)+1;i++){const x=i*32-cam;rect(x,ground+7,30,9,colors.slate);rect(x+1,ground+7,26,1,colors.metal);rect(x+4,ground+19,29,8,colors.outline);if(i%3===0){rect(x+3,ground-2,8,2,colors.leaf);rect(x+13,ground+3,2,3,colors.ink);}}
  // Pixel fireflies, never blinking at high contrast.
  for(let i=0;i<7;i++){const x=(i*91+Math.sin(simTime*.0007+i)*7-cam*.3)%w;rect((x+w)%w,45+random(i)*55,1,1,colors.light);}
}
function sound(skill){if(!$('sound').checked)return;audio??=new (window.AudioContext||window.webkitAudioContext)();void audio.resume();const now=audio.currentTime;const osc=audio.createOscillator(),gain=audio.createGain();osc.type='triangle';osc.frequency.setValueAtTime(skill?145:240,now);osc.frequency.exponentialRampToValueAtTime(45,now+.085);gain.gain.setValueAtTime(.16,now);gain.gain.exponentialRampToValueAtTime(.001,now+.12);osc.connect(gain).connect(audio.destination);osc.start(now);osc.stop(now+.13);const length=Math.round(audio.sampleRate*.05),buffer=audio.createBuffer(1,length,audio.sampleRate),data=buffer.getChannelData(0);for(let i=0;i<length;i++)data[i]=(Math.random()*2-1)*(1-i/length)*.16;const noise=audio.createBufferSource();noise.buffer=buffer;noise.connect(audio.destination);noise.start(now);}
/* Ground dust: low, slow, muted pixels kicked away from a foot. dir -1 = backwards (left). */
function dust(x,dir,count,seed){for(let i=0;i<count;i++){const r=random(seed+i*3.7);particles.push({x:x+dir*r*6,y:-1-random(seed+i)*3,vx:dir*(18+r*48),vy:-(12+random(seed+i*1.3)*34),g:70,life:200+r*140,color:i%3===0?colors.cream:i%2?colors.silver:colors.metal,size:i%4===0?3:2});}}
function impact(action){const skill=action.kind==='skill',damage=skill?82:36,r=rig();state.hp=Math.max(0,state.hp-damage);
  // Hit stop freezes only the world simulation; HUD, cooldown and timers keep running.
  state.hold=skill?60:(r?r.spec.hitStopMs:45);state.shake=skill?180:110;state.flash=reduced?0:75;state.flinch=140;state.enemy+=skill?16:9;state.combo++;sound(skill);
  numbers.push({x:state.enemy,y:-63,text:skill?'312!':'128',life:600,max:600,skill});
  // The PixelLab frames already carry their own sword arc, so only the code knight gets the big drawn crescent.
  if(!r)bursts.push({x:state.enemy-10,life:skill?235:150,max:skill?235:150,skill});
  waves.push({x:state.enemy-18,life:skill?210:150,max:skill?210:150,skill});
  const count=skill?30:16;for(let i=0;i<count;i++){const angle=random(i+simTime)*Math.PI*2,speed=35+random(i+7)*95;particles.push({x:state.enemy-14,y:-25,vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed-45,life:170+random(i)*180,color:i%4===0?colors.white:i%3===0?colors.brass:colors.gold,size:i%5===0?3:2});}
  dust(state.hero-6,-1,skill?10:6,simTime);dust(state.enemy+8,1,skill?12:7,simTime+50);
  if(!state.hp){state.mode='death';state.death=0;state.gold+=82;state.kills++;if(state.kills%2===0)state.boxes++;if(state.kills%4===0)state.stage++;}
}
function attack(kind,manual=false){if(paused||state.mode==='death'||state.mode==='loot')return;if(kind==='skill'&&state.cooldown>0)return;if(state.action){if(manual)state.queued=kind;return;}const gap=engageGap();if(manual&&state.enemy-state.hero>gap+10){state.enemy=state.hero+gap;state.mode='fight';}if(state.mode!=='fight')return;
  const r=rig();
  if(r){const frameMs=1000/r.spec.fps;state.action={kind,t:0,hit:false,frameMs,impact:r.spec.impact*frameMs,duration:r.spec.frames*frameMs};}
  else state.action={kind,t:0,hit:false,impact:kind==='skill'?135:90,duration:kind==='skill'?280:195};
  if(kind==='skill')state.cooldown=1600;}
function update(dt,realDt){state.cooldown=Math.max(0,state.cooldown-realDt);state.shake=Math.max(0,state.shake-realDt);state.flash=Math.max(0,state.flash-realDt);state.flinch=Math.max(0,state.flinch-realDt);if(paused)return;if(state.hold>0){state.hold=Math.max(0,state.hold-realDt);return;}simTime+=dt;
  if(state.action){const a=state.action;a.t+=dt;if(!a.hit&&a.t>=a.impact){a.t=a.impact;a.hit=true;impact(a);}else if(a.t>=a.duration){state.action=null;state.wait=90;const queued=state.queued;state.queued=null;if(queued&&state.mode==='fight')attack(queued);}}
  else if(state.mode==='walk'){state.hero+=dt*.105;state.enemy-=dt*.014;if(state.enemy-state.hero<engageGap()){state.mode='fight';state.wait=80;}}
  else if(state.mode==='fight'){state.wait-=dt;if($('auto').checked&&state.wait<=0)attack(state.combo%3===2&&state.cooldown<=0?'skill':'slash');}
  if(state.mode==='death'){state.death+=dt;if(state.death>350&&!state.action){state.mode='loot';state.wait=350;numbers.push({x:state.enemy,y:-30,text:'+82 ทอง',life:800,max:800,skill:false});}}
  else if(state.mode==='loot'){state.wait-=dt;if(state.wait<=0){state.enemy=state.hero+220;state.hp=120;state.mode='walk';state.death=0;}}
  for(const p of particles){p.life-=dt;p.x+=p.vx*dt/1000;p.y=Math.min(0,p.y+p.vy*dt/1000);p.vy+=(p.g??220)*dt/1000;}particles=particles.filter(p=>p.life>0);for(const n of numbers)n.life-=dt;numbers=numbers.filter(n=>n.life>0);for(const b of bursts)b.life-=dt;bursts=bursts.filter(b=>b.life>0);for(const w of waves)w.life-=dt;waves=waves.filter(w=>w.life>0);
  if(follow&&!dragging)cameraPan*=Math.pow(.0008,dt/1000);
}
/* Code knight: hand-timed key poses. */
function codePose(){const a=state.action;if(!a)return [state.mode==='walk'?'knight_walk':'knight_idle',Math.floor(simTime/1000*(state.mode==='walk'?14:8))%(state.mode==='walk'?6:4),0];if(a.kind==='slash'){const f=a.t<35?0:a.t<60?1:a.t<90?2:a.t<130?3:a.t<165?4:5;return ['knight_slash',f,a.t<a.impact?-3:Math.max(0,14*(1-(a.t-a.impact)/(a.duration-a.impact)))];}const f=a.t<35?0:a.t<70?1:a.t<110?2:a.t<135?3:a.t<170?4:a.t<205?5:a.t<245?6:7;return ['knight_skill',f,a.t<a.impact?-2:Math.max(0,19*(1-(a.t-a.impact)/(a.duration-a.impact)))];}
/* PixelLab hero: frames at the sheet's fps, the impact frame held through hit stop. No walk sheet exists yet, so
   walking and idling show the still candidate sliding through the scene. The skill reuses the attack sheet. */
function drawHero(x,ground){const r=rig();
  if(!r){const [key,frame,lunge]=codePose();sprite(key,frame,x+lunge,ground);return;}
  const a=state.action,s=r.spec;
  if(!a){ctx.drawImage(r.still,Math.round(x-r.still.width/2),Math.round(ground-r.still.height));return;}
  const frame=Math.min(s.frames-1,Math.floor(a.t/a.frameMs)),reach=a.kind==='skill'?12:8;
  const lunge=a.t<a.impact?-2:reach*(1-(a.t-a.impact)/(a.duration-a.impact));
  drawFrame(r.sheet,frame,s.width,s.height,x+lunge,ground);}
/* Monster flinch: squash on contact, stretch on the rebound, a 1px shiver, then settle. */
function flinchShape(){if(!state.flinch||reduced)return {sx:1,sy:1,dx:0};const t=140-state.flinch;if(t<50)return {sx:1.16,sy:.86,dx:2+(t%20<10?1:-1)};if(t<100)return {sx:.94,sy:1.06,dx:1};return {sx:1,sy:1,dx:0};}
/* Thin crescent: outer arc minus an arc shifted back by its thickness, so it tapers at both tips. */
function crescent(cx,cy,R,th,c){const pts=[];for(let i=0;i<=10;i++){const a=-1.2+2.4*i/10;pts.push([cx+Math.cos(a)*R,cy+Math.sin(a)*R*1.2]);}for(let i=10;i>=0;i--){const a=-1.2+2.4*i/10;pts.push([cx-th+Math.cos(a)*R,cy+Math.sin(a)*R*1.2]);}poly(pts,c);}
function effects(cam,ground){for(const b of bursts){const x=b.x-cam,t=1-b.life/b.max;ctx.globalAlpha=1-t;const reach=b.skill?95:67;
    // Broad faceted crescent with a pale leading edge; separate from character frame.
    poly([[x-35,ground-62],[x+22,ground-55],[x+reach,ground-18],[x+reach-12,ground-4],[x+19,ground-37],[x-27,ground-48]],colors.gold);
    poly([[x-30,ground-62],[x+22,ground-55],[x+reach,ground-18],[x+reach-4,ground-12],[x+19,ground-48]],colors.white);
    if(b.skill){const radius=12+t*83;for(let i=0;i<14;i++){const a=Math.PI*i/13,xx=x+Math.cos(a)*radius,yy=ground-Math.sin(a)*radius*.24;rect(xx,yy,4,2,colors.gold);}rect(x-22,ground-68,5,60*(1-t),colors.glint);poly([[x-20,ground-5],[x+26,ground-7],[x+60,ground],[x-45,ground]],colors.brass);}
    ctx.globalAlpha=1;
  }
  // Slash wave: the cut keeps travelling through and past the monster, thinning as it goes.
  for(const w of waves){const t=1-w.life/w.max,x=w.x-cam+t*(w.skill?78:50),R=w.skill?30:22,th=Math.max(1,(w.skill?8:6)*(1-t));ctx.globalAlpha=1-t*t;crescent(x,ground-30,R,th,colors.gold);crescent(x+1,ground-30,R-1,Math.max(1,th*.5),colors.white);if(w.skill){rect(x-R-30*t,ground-3,60*t+10,2,colors.brass);}ctx.globalAlpha=1;}
  for(const p of particles){ctx.globalAlpha=Math.min(1,p.life/120);rect(p.x-cam,ground+p.y,p.size,p.size,p.color);}ctx.globalAlpha=1;
  for(const n of numbers){const t=1-n.life/n.max;ctx.globalAlpha=Math.min(1,n.life/170);pixelText(n.text,n.x-cam,ground+n.y-t*20,n.skill?colors.gold:colors.cream,n.skill?17:13);}ctx.globalAlpha=1;
}
function phaseLabel(){if(paused)return 'พักภาพ';if(state.hold>0)return 'ปะทะ!';if(state.action)return state.action.t<state.action.impact?'เตรียม / พุ่ง':'คืนท่า';const base=({walk:'กำลังเดินทาง',fight:'พร้อมโจมตี',death:'เก็บชัยชนะ',loot:'เก็บของ'})[state.mode];return rig()&&state.mode!=='fight'?base+' · ภาพนิ่ง (ยังไม่มีท่าเดิน)':base;}
function draw(){const ground=canvas.height-28;const cam=state.hero-canvas.width*heroView[variant]+cameraPan;ctx.clearRect(0,0,canvas.width,canvas.height);ctx.save();
  // Camera shake moves only the canvas content; the HUD around it is DOM and stays still.
  const power=state.shake>0&&$('shake').checked&&!reduced?(state.shake/180)*4:0;ctx.translate(Math.round(Math.sin(performance.now()*.16)*power),Math.round(Math.cos(performance.now()*.13)*power*.55));background(cam,ground);
  rect(state.hero-cam-15,ground-1,31,2,colors.ink);drawHero(state.hero-cam,ground);
  if(state.mode!=='loot'){const f=flinchShape();rect(state.enemy-cam-15,ground-1,28,2,colors.ink);sprite(state.mode==='death'?'foe_death':state.mode==='walk'?'foe_walk':'foe_idle',state.mode==='death'?Math.min(3,Math.floor(state.death/85)):Math.floor(simTime/(state.mode==='walk'?85:125))%(state.mode==='walk'?6:4),state.enemy-cam+f.dx,ground,{sx:f.sx,sy:f.sy,tint:state.flash>35});if(state.hp>0&&state.mode==='fight'){rect(state.enemy-cam-15,ground-54,30,3,colors.ink);rect(state.enemy-cam-14,ground-53,28*state.hp/120,1,colors.red);}}
  if(state.mode==='loot'){const x=state.enemy-cam;rect(x-7,ground-12,14,11,colors.wood);rect(x-6,ground-11,12,9,colors.brass);rect(x-6,ground-12,12,3,colors.gold);rect(x-1,ground-10,2,3,colors.silver);}
  effects(cam,ground);ctx.restore();
  $('gold').textContent=state.gold.toLocaleString('en-US');$('boxes').textContent=state.boxes;$('stage').textContent=state.stage;
  const phase=phaseLabel();$('phase').textContent=phase;
  $('cooldown').style.width=(100-state.cooldown/16)+'%';$('skill').disabled=paused||state.cooldown>0||state.mode==='death'||state.mode==='loot';$('slash').disabled=paused||state.mode==='death'||state.mode==='loot';
  const r=rig(),a=state.action,frameInfo=r&&a?` · เฟรม ${Math.min(r.spec.frames-1,Math.floor(a.t/a.frameMs))}/${r.spec.frames-1}`:'';
  $('readout').textContent=`${variant} · ${canvas.width}×${canvas.height}px · ${ARTS[artKey].label} · ${phase}${frameInfo} · HP มอน ${state.hp}/120 · ${follow?'กล้องตาม':'กล้องเลื่อนเอง'}${$('slow').checked?' · ช้าลง 4 เท่า':''}`;
  window.prototypeState={variant,art:artKey,mode:state.mode,phase,heroWorldX:Math.round(state.hero),enemyWorldX:Math.round(state.enemy),hp:state.hp,kills:state.kills,holdMs:Math.round(state.hold),cooldownMs:Math.round(state.cooldown),cameraPan:Math.round(cameraPan),paused,action:a?{kind:a.kind,t:Math.round(a.t),impact:Math.round(a.impact),duration:Math.round(a.duration)}:null};
}
function tick(now){const elapsed=previousTime?Math.min(50,now-previousTime):16;previousTime=now;const k=$('slow').checked?.25:1;update(Math.min(32,elapsed)*k,elapsed*k);draw();requestAnimationFrame(tick);}
function timingNote(){const r=rig();if(!r)return 'ภาพโค้ดเดิม · ฟัน: เตรียม 35ms → พุ่ง 55ms → hit stop 45ms → คืนท่า 105ms · สกิล: 70 / 65 / 60 / 145ms';const s=r.spec,fm=1000/s.fps;return `${ARTS[artKey].label} (จาก animation.json) · ${s.width}×${s.height}px · ${s.frames} เฟรม · ${s.fps} FPS (${fm.toFixed(2)}ms/เฟรม) · impact เฟรม ${s.impact} ที่ ${Math.round(s.impact*fm)}ms → hit stop ${s.hitStopMs}ms → จบท่าที่ ${Math.round(s.frames*fm+s.hitStopMs)}ms · สกิลใช้เฟรมชุดเดียวกัน hit stop 60ms`;}
function chooseArt(key){artKey=ARTS[key]&&(key==='code'||rigs[key])?key:'code';document.querySelectorAll('.art').forEach(b=>b.classList.toggle('selected',b.dataset.art===artKey));const url=new URL(location.href);url.searchParams.set('art',artKey);history.replaceState(null,'',url);state.action=null;state.queued=null;$('timing').textContent=timingNote();$('inspector-name').textContent=rig()?'นักดาบ (ทดลอง PixelLab)':'นักรบ';$('hero-name').textContent=(rig()?'นักดาบ':'นักรบ')+' · Lv. 12';draw();}
function choose(key){variant=variants.includes(key)?key:'A';$('game-window').dataset.variant=variant;[canvas.width,canvas.height]=sizes[variant];ctx.imageSmoothingEnabled=false;document.querySelectorAll('.variant').forEach(b=>b.classList.toggle('selected',b.dataset.variant===variant));const url=new URL(location.href);url.searchParams.set('variant',variant);history.replaceState(null,'',url);$('game-window').style.transform='';offsetX=0;offsetY=0;draw();}
function cycle(delta){choose(variants[(variants.indexOf(variant)+delta+3)%3]);}
$('previous').onclick=()=>cycle(-1);$('next').onclick=()=>cycle(1);document.querySelectorAll('.variant').forEach(b=>b.onclick=()=>choose(b.dataset.variant));document.querySelectorAll('.art').forEach(b=>b.onclick=()=>chooseArt(b.dataset.art));
$('pause').onclick=()=>{paused=!paused;$('pause').textContent=paused?'เล่นต่อ':'พักภาพ';};$('skill').onclick=()=>attack('skill',true);$('slash').onclick=()=>attack('slash',true);$('follow').onclick=()=>{follow=true;};$('restart').onclick=()=>{reset();paused=false;$('pause').textContent='พักภาพ';};
document.addEventListener('keydown',e=>{if(e.target instanceof Element&&e.target.matches('input,textarea,select,[contenteditable=true],button'))return;if(e.code==='Space'){e.preventDefault();attack('skill',true);}if(e.code==='KeyF'){e.preventDefault();attack('slash',true);}if(e.code==='ArrowLeft'){e.preventDefault();cycle(-1);}if(e.code==='ArrowRight'){e.preventDefault();cycle(1);}});
let pointerX=0;canvas.addEventListener('pointerdown',e=>{dragging=true;follow=false;pointerX=e.clientX;canvas.setPointerCapture(e.pointerId);});canvas.addEventListener('pointermove',e=>{if(!dragging)return;cameraPan-=(e.clientX-pointerX)*canvas.width/canvas.getBoundingClientRect().width;pointerX=e.clientX;});canvas.addEventListener('pointerup',()=>dragging=false);canvas.addEventListener('pointercancel',()=>dragging=false);
let moving=false,dragX=0,dragY=0,offsetX=0,offsetY=0;
$('drag-handle').addEventListener('pointerdown',e=>{moving=true;dragX=e.clientX-offsetX;dragY=e.clientY-offsetY;e.currentTarget.setPointerCapture(e.pointerId);});$('drag-handle').addEventListener('pointermove',e=>{if(!moving)return;const limit=Math.max(0,($('desktop').clientWidth-$('game-window').offsetWidth)/2-12);offsetX=Math.max(-limit,Math.min(limit,e.clientX-dragX));offsetY=Math.max(-30,Math.min(35,e.clientY-dragY));$('game-window').style.transform=`translate(${offsetX}px,${offsetY}px)`;});$('drag-handle').addEventListener('pointerup',()=>moving=false);$('drag-handle').addEventListener('pointercancel',()=>moving=false);
function loadImage(src){return new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>resolve(image);image.onerror=()=>reject(new Error(src));image.src=src;});}
async function loadJson(src){const res=await fetch(src);if(!res.ok)throw new Error(src);return res.json();}
/* One PixelLab rig: animation.json says which sheet, its frame size, count, fps, impact frame and hit stop. */
async function loadRig(key){const dir=ARTS[key].dir,spec=await loadJson(dir+'animation.json');for(const field of ['file','width','height','frames','fps','impact','hitStopMs'])if(spec[field]===undefined)throw new Error(`animation.json: missing ${field}`);const [sheet,still]=await Promise.all([loadImage(dir+spec.file),loadImage(dir+stillFile)]);if(sheet.width!==spec.width*spec.frames||sheet.height!==spec.height)throw new Error(`${spec.file}: ${sheet.width}×${sheet.height} ≠ ${spec.frames}×${spec.width}×${spec.height}`);rigs[key]={spec,sheet,still};}
async function boot(){
  await Promise.all(Object.keys(specs).map(key=>loadImage('assets/'+key+'.png').then(image=>{art[key]=image;})));
  const problems=[];
  try{stillFile=(await loadJson(PIXELLAB+'selection.json')).file||stillFile;}catch(e){problems.push('selection.json');}
  for(const key of ['clean','raw']){try{await loadRig(key);}catch(e){problems.push(`${ARTS[key].label}: ${e.message}`);document.querySelector(`.art[data-art="${key}"]`).disabled=true;}}
  const params=new URLSearchParams(location.search);choose(params.get('variant'));chooseArt(params.get('art')||'clean');
  if(problems.length)$('load-note').textContent=`โหลดภาพ PixelLab ไม่ครบ (${problems.join(' · ')}) ถ้าเปิดไฟล์ตรง ๆ ให้เปิดผ่าน http://localhost/Projects-1/design/prototypes/action/ แทน เพราะเบราว์เซอร์ไม่ให้อ่าน JSON จากไฟล์ในเครื่อง`;
  requestAnimationFrame(tick);
}
boot().catch(()=>{$('readout').textContent='เปิดภาพไม่สำเร็จ กรุณาเปิด prototype จากโฟลเดอร์เดิมพร้อม assets/';});
