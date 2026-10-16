/* Independent art preview. No game state, purchases, combat or server writes. */
(()=>{'use strict';
const D=window.MAP_DATA,c=document.querySelector('#map'),ctx=c.getContext('2d'),land=new Image();
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
let region=0,selected=null,paused=reduced.matches,ready=false,clock=0,last=performance.now();
const byId=id=>document.getElementById(id);
const state={clouds:true,pins:false,routes:false};
function camera(){if(!region)return{x:0,y:0,w:256,h:192};const b=D.regions.find(r=>r.id===region).view;return{x:b[0],y:b[1],w:b[2],h:b[3]};}
function visibleStages(){return D.stages.filter(s=>!region||s.city===region);}
function rect(x,y,w,h,color){ctx.fillStyle=color;ctx.fillRect(Math.round(x),Math.round(y),w,h);}
function cloud(x,y,size,alpha){ctx.globalAlpha=alpha;ctx.fillStyle='#a8c9d1';ctx.fillRect(x+2*size,y+4*size,16*size,3*size);ctx.fillStyle='#eaf4e9';ctx.fillRect(x,y+3*size,20*size,3*size);ctx.fillRect(x+3*size,y+size,13*size,5*size);ctx.fillRect(x+7*size,y,7*size,4*size);ctx.fillStyle='#fff9df';ctx.fillRect(x+4*size,y+size,9*size,size);ctx.globalAlpha=1;}
function render(t){if(!ready)return;const cam=camera();ctx.setTransform(1,0,0,1,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#145e78';ctx.fillRect(0,0,c.width,c.height);ctx.setTransform(c.width/cam.w,0,0,c.height/cam.h,-cam.x*c.width/cam.w,-cam.y*c.height/cam.h);
// WATER: world-space pixel wave tiles. Rendered behind the transparent continent.
for(let y=-8;y<208;y+=12)for(let x=-20;x<276;x+=21){let n=((x*17+y*23)%11+11)%11;let phase=Math.floor(t*2+n)%6;let wx=x+((Math.floor(y/12)%2)*9)+phase;rect(wx,y,5,1,'#278c9d');rect(wx+2,y+1,3,1,'#1b738c');if(n%3===0)rect(wx+9,y+6,2,1,'#4bb3b5');}
// LAND: single stable native pixel layer. No camera drift or terrain deformation.
ctx.drawImage(land,0,0,256,192);
// CLOUDS: separate far/near weather passes, under pins so destinations stay visible.
if(state.clouds){D.clouds.forEach((p,i)=>{const speed=p.near?1.15:.45;let x=Math.floor(((p.x+t*speed+30)%316)-30);cloud(x,p.y,p.near?1:.7,p.near?.58:.35);});}
const stages=visibleStages();
if(state.routes){for(const r of D.regions.filter(r=>!region||r.id===region)){const list=D.stages.filter(s=>s.city===r.id);ctx.beginPath();list.forEach((s,i)=>i?ctx.lineTo(s.x,s.y):ctx.moveTo(s.x,s.y));ctx.strokeStyle='#314737';ctx.lineWidth=1.6;ctx.stroke();ctx.strokeStyle='#efc969';ctx.lineWidth=.5;ctx.stroke();}}
if(state.pins){for(const s of stages){const active=selected?.id===s.id;const size=s.boss?1.25:.85;rect(s.x-size,s.y-size,size*2+1,size*2+1,'#293431');rect(s.x-size+.7,s.y-size+.7,size*2-.4,size*2-.4,active?'#fff4bf':s.boss?'#e48258':'#d6d9b0');if(active){ctx.strokeStyle='#fff6b8';ctx.lineWidth=.6;ctx.strokeRect(Math.round(s.x)-4,Math.round(s.y)-4,8,8);}}}
ctx.setTransform(1,0,0,1,0,0);}
function updatePause(){byId('pause').textContent=paused?'เปิดภาพเคลื่อนไหว':'หยุดภาพเคลื่อนไหว';byId('pause').setAttribute('aria-pressed',String(paused));}
function selectStage(s){selected=s;byId('stage-title').textContent=`ด่าน ${s.city}-${s.localStage}${s.boss?' · บอสประจำภูมิภาค':''}`;byId('stage-description').textContent=`${s.regionName} / ${s.zoneName} · ด่านที่ ${s.inZone} จาก 5`;byId('stage-count').textContent=`${s.id} / 100`;document.querySelectorAll('[data-stage]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.stage)===s.id)));render(clock);}
function fillStages(){const root=byId('stage-list');root.replaceChildren();if(!region){const p=document.createElement('p');p.textContent='เลือกภูมิภาคด้านบนเพื่อขยายแผนที่และดู 20 ด่านของพื้นที่นั้น';root.append(p);return;}for(const z of D.zones.filter(z=>z.city===region&&z.zone>0)){const row=document.createElement('div');row.className='zone-row';const title=document.createElement('h3');title.textContent=z.nameTh;row.append(title);const group=document.createElement('div');group.className='stage-buttons';for(const s of D.stages.filter(s=>s.city===region&&s.zone===z.zone)){const b=document.createElement('button');b.type='button';b.textContent=`${s.city}-${s.localStage}${s.boss?' บอส':''}`;b.dataset.stage=s.id;b.dataset.boss=s.boss;b.setAttribute('aria-pressed',String(selected?.id===s.id));b.setAttribute('aria-label',`ด่าน ${s.city}-${s.localStage} ${s.zoneName}${s.boss?' บอสประจำภูมิภาค':''}`);b.onclick=()=>selectStage(s);group.append(b);}row.append(group);root.append(row);}}
function focusRegion(id){region=id;state.pins=Boolean(id);state.routes=Boolean(id);byId('pins').checked=state.pins;byId('routes').checked=state.routes;document.querySelectorAll('[data-region]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.region)===id)));fillStages();if(id)selectStage(D.stages.find(s=>s.city===id));else{byId('stage-title').textContent='แผนที่โลกทั้งหมด';byId('stage-description').textContent='5 ภูมิภาค · 20 โซน · 100 ด่าน';byId('stage-count').textContent='';render(clock);}}
const nav=byId('regions');[{id:0,name:'ทั้งโลก',color:'#145e78'},...D.regions].forEach(r=>{const b=document.createElement('button');b.type='button';b.dataset.region=r.id;b.textContent=r.name;b.style.setProperty('--region',r.color);b.setAttribute('aria-pressed',String(r.id===0));b.onclick=()=>focusRegion(r.id);nav.append(b);});
byId('pause').onclick=()=>{paused=!paused;updatePause();render(clock);};byId('reset').onclick=()=>focusRegion(0);
for(const key of Object.keys(state))byId(key).onchange=e=>{state[key]=e.target.checked;render(clock);};
c.onclick=e=>{if(!state.pins||!ready)return;const b=c.getBoundingClientRect(),cam=camera();const x=cam.x+(e.clientX-b.left)/b.width*cam.w,y=cam.y+(e.clientY-b.top)/b.height*cam.h;let s=visibleStages().reduce((best,p)=>Math.hypot(p.x-x,p.y-y)<Math.hypot(best.x-x,best.y-y)?p:best);if(Math.hypot(s.x-x,s.y-y)<7){if(!region){focusRegion(s.city);}selectStage(s);}};
c.onkeydown=e=>{if(!['ArrowLeft','ArrowRight'].includes(e.key))return;e.preventDefault();const list=visibleStages(),i=selected?list.findIndex(s=>s.id===selected.id):0;selectStage(list[(i+(e.key==='ArrowRight'?1:-1)+list.length)%list.length]);};
land.onload=()=>{ready=true;byId('load-state').hidden=true;focusRegion(0);render(0);};land.onerror=()=>{byId('load-state').textContent='เปิดภาพแผนที่ไม่ได้ กรุณาวาง land-v1.png ไว้ข้าง viewer.html แล้วเปิดใหม่';};land.src='land-v1.png';
setInterval(()=>{const now=performance.now();const dt=Math.min((now-last)/1000,.25);last=now;if(!paused&&!document.hidden){clock+=dt;render(clock);}},100);
reduced.addEventListener('change',e=>{if(e.matches){paused=true;updatePause();render(clock);}});updatePause();fillStages();
window.mapPreview={renderAt:render,selectRegion:focusRegion,selectStage:id=>selectStage(D.stages.find(s=>s.id===id)),getState:()=>({region,selected:selected?.id,paused,ready,clock,stages:D.stages.length}),canvas:c};
})();
