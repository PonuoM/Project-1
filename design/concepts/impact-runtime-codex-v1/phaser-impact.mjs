import {AttackDriver} from './attack-driver.mjs';
// Phaser adapter. No timers, animations, rewards or global scene timeScale are changed.
export class ImpactPresentation {
 constructor(scene,{hero,target,graphics,resolveTarget,onVisualContact=()=>{},reduced=()=>false}){
  this.scene=scene;this.hero=hero;this.target=target;this.g=graphics;this.resolveTarget=resolveTarget;this.reduced=reduced;this.fx=[];this.trails=[];this.lastPose=null;this.age=0;this.reaction=null;this.onVisualContact=onVisualContact;
  this.driver=new AttackDriver({contact:e=>resolveTarget(e),onContact:e=>this.impact(e)});
 }
 start(options){return this.driver.start(options);}
 cancel(){this.driver.cancel();this.fx.length=0;this.trails.length=0;this.reaction=null;this.target.clearTint();this.scene.cameras.main.setScroll(0,0);}
 impact(e){this.reaction={age:0,knock:e.knock,dir:e.direction,finish:e.kind==='finisher',seed:e.index+1};this.fx.push({x:e.target.x-e.direction*14,y:91,age:0,kind:e.kind,seed:e.index+1});this.fx=this.fx.slice(-8);this.onVisualContact(e);}
 update(delta){this.age+=delta;for(const b of this.fx)b.age+=delta;this.fx=this.fx.filter(b=>b.age<300);for(const t of this.trails)t.age+=delta;this.trails=this.trails.filter(t=>t.age<75);
  if(this.reaction)this.reaction.age+=delta;
  this.driver.update(delta);const p=this.driver.pose();
  if(p.phase==='burst'&&this.lastPose){this.trails.push({...this.lastPose,age:0});this.trails=this.trails.slice(-3);}
  this.lastPose=p;this.hero.setTexture(p.key,p.frame).setPosition(Math.round(p.x),112).setFlipX(this.driver.direction<0);
  const logical=this.resolveTarget(null);const r=this.reaction;let kick=0,lift=0,shake=0;
  if(r&&r.age<350){const k=r.age/350;kick=r.dir*r.knock*Math.sin(Math.min(1,k*2)*Math.PI/2)*Math.pow(1-k,1.3);lift=r.finish?Math.sin(k*Math.PI)*9:0;shake=(r.finish?3:2)*Math.pow(1-k,3);}
  this.target.setPosition(Math.round((logical?.x??this.target.x)+kick),112-Math.round(lift)).setScale(2,2).setAngle(0);
  if(r&&r.age<45&&!this.reduced())this.target.setTintFill(0xffffff);else this.target.clearTint();
  if(r&&r.age<100){const s=Math.sin(r.age*.16);this.target.setScale(2*(1-.12*s),2*(1+.12*s));}
  const cam=this.scene.cameras.main;const motion=this.reduced()?0:shake;
  cam.setScroll(Math.round(Math.sin(this.age*.17)*motion),Math.round(Math.cos(this.age*.23)*motion*.6));
  this.drawFx(p);return p;
 }
 drawFx(p){const g=this.g;g.clear();for(const b of this.fx){const f=1-b.age/300;if(f<=0)continue;const big=b.kind==='finisher';const radius=(big?8:5)+b.age*.07;const points=[];for(let i=0;i<16;i++){let a=i*Math.PI/8,rr=i%2?radius*.22:radius;points.push({x:Math.round(b.x+Math.cos(a)*rr),y:Math.round(b.y+Math.sin(a)*rr)});}g.fillStyle(0xf1d788,f).fillPoints(points,true);g.fillStyle(0xfff5d7,f).fillRect(b.x-2,b.y-2,4,4);
  for(let i=0;i<8;i++){let a=i*.91+b.seed;let d=b.age*.09;g.fillStyle(i%2?0xe9b96c:0xeee7d5,f).fillRect(Math.round(b.x+Math.cos(a)*d),Math.round(b.y+Math.sin(a)*d+b.age*b.age*.0003),2,2);}
 }
 // Weapon smear is keyed to the swing, even on a miss. Hit sparks above require contact.
 if(this.driver.active&&this.driver.t>=this.driver.profile.windup&&this.driver.t<this.driver.impactAt+65){const dir=this.driver.direction,x=p.x+dir*23;const age=Math.max(0,this.driver.t-this.driver.impactAt);const a=1-age/65;const poly=[[-22,-38],[8,-38],[43,-15],[46,-8],[6,-25],[-18,-30]].map(([dx,dy])=>({x:Math.round(x+dx*dir),y:112+dy}));g.fillStyle(0xf1d788,a*.9).fillPoints(poly,true);g.lineStyle(2,0xfff5d7,a).lineBetween(x-16*dir,78,x+41*dir,98);}
 }
 destroy(){this.cancel();this.fx=[];this.trails=[];}
}
