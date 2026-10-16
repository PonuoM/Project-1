// Engine-independent visual attack driver. Authoritative gameplay stays in the host.
export const PROFILES = Object.freeze({
 plain: {windup:105,burst:105,stop:0,recover:160,lunge:24,knock:3,shake:0},
 heavy: {windup:95,burst:28,stop:65,recover:165,lunge:24,knock:12,shake:2},
 finisher: {windup:150,burst:25,stop:90,recover:240,lunge:30,knock:24,shake:3}
});
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
export class AttackDriver {
 constructor({contact=()=>null,onContact=()=>{},onFinish=()=>{}}={}) {this.contact=contact;this.onContact=onContact;this.onFinish=onFinish;this.active=false;this.hold=0;this.t=0;this.wall=0;this.index=0;this.serial=0;}
 start({kind='heavy',combo=false,x=80,direction=1}={}) {
  if(this.active)return false;
  if(!PROFILES[kind])throw new Error('Unknown attack profile');
  this.chain=combo?['heavy','heavy','finisher']:[kind];this.index=0;this.t=0;this.wall=0;this.hold=0;this.fired=false;this.active=true;this.x=x;this.direction=direction<0?-1:1;this.serial++;return true;
 }
 cancel(){this.active=false;this.hold=0;}
 get profile(){return PROFILES[this.chain?.[this.index]??'heavy'];}
 get impactAt(){return this.profile.windup+this.profile.burst;}
 get offset(){const p=this.profile,t=this.t;if(t<p.windup)return -4*Math.sin(t/p.windup*Math.PI/2);if(t<this.impactAt)return -4+(p.lunge+4)*Math.pow((t-p.windup)/p.burst,3);return p.lunge*Math.pow(1-clamp((t-this.impactAt)/p.recover,0,1),2);}
 pose(){if(!this.active)return {key:'slash',frame:0,x:this.x,phase:'ready',stop:false};const p=this.profile,t=this.t;let phase,frame;
 if(t<p.windup){phase='windup';frame=1+Math.min(3,Math.floor(t/p.windup*4));}
 else if(t<this.impactAt){phase='burst';frame=5+Math.min(1,Math.floor((t-p.windup)/p.burst*2));}
 else{phase=this.hold>0?'contact':'recover';frame=7+Math.min(7,Math.floor((t-this.impactAt)/p.recover*8));}
 return {key:this.chain[this.index]==='finisher'?'chop':'slash',frame,x:this.x+this.offset*this.direction,phase,stop:this.hold>0};}
 update(delta){if(!Number.isFinite(delta)||delta<0)throw new Error('delta must be finite and non-negative');this.wall+=delta;let remaining=delta;
 while(this.active&&remaining>1e-7){
  if(this.hold>0){let used=Math.min(remaining,this.hold);this.hold-=used;remaining-=used;continue;}
  let boundary=this.fired?this.impactAt+this.profile.recover:this.impactAt;
  let used=Math.min(remaining,Math.max(0,boundary-this.t));this.t+=used;remaining-=used;
  if(this.t<boundary-1e-7)break;
  if(!this.fired){this.fired=true;const p=this.profile;const event={id:this.serial+':'+this.index,index:this.index,kind:this.chain[this.index],x:this.x+p.lunge*this.direction,y:98,direction:this.direction,reach:49,knock:p.knock,shake:p.shake,stopMs:p.stop};
   const target=this.contact(event);if(target!=null){this.hold=p.stop;this.onContact({...event,target});} // no hit-stop / damage / sparks on a miss
  }else{this.index++;if(this.index>=this.chain.length){this.active=false;this.hold=0;this.onFinish();}else{this.t=0;this.fired=false;}}
 }
 }
}
