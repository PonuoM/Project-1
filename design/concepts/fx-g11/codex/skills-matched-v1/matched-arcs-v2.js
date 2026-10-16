// Source coordinates are the same128x80 canvas as each hero frame.
const MATCHED_BASE = '../../concepts/fx-g11/codex/skills-matched-v1/';
const MATCHED_ARCS = {};
async function loadMatchedArcs() {
  const plans = await json(MATCHED_BASE + 'timing-plan-v3.json');
  for (const p of plans) {
    const source = await img(MATCHED_BASE + p.sheet), tints = {};
    for (const [element, colours] of Object.entries(ARC_COL)) {
      const canvas = new OffscreenCanvas(source.width, source.height), context = canvas.getContext('2d');
      context.drawImage(source,0,0);
      const pixels = context.getImageData(0,0,source.width,source.height), data=pixels.data, ramp=colours.map(hex);
      for (let i=0;i<data.length;i+=4) {
        const v=data[i];
        if (!v) { data[i+3]=0;continue; }
        const colour=ramp[v>200?0:v>110?1:2];
        data[i]=colour[0];data[i+1]=colour[1];data[i+2]=colour[2];
      }
      context.putImageData(pixels,0,0);tints[element]=canvas;
    }
    MATCHED_ARCS[p.move]={...p,tints};
    // These are local playtest timings; the original source JSON is never edited.
    MOVES[p.move].originalHits=MOVES[p.move].hits;
    MOVES[p.move].hits=p.impact;
  }
}
function matchedArcKey(plan,attack) {
  const move=MOVES[attack.move];
  if (plan.cycle) return attack.f>=plan.start && attack.f<plan.end ? (attack.f-plan.start)%4 : -1;
  const elapsed=move.ms.slice(0,attack.f).reduce((a,b)=>a+b,0)+attack.acc;
  for (const start of [...(plan.starts || [plan.start])].reverse()) {
    let age=elapsed-move.ms.slice(0,start).reduce((a,b)=>a+b,0);
    if (age<0) continue;
    for (let key=0;key<plan.keys.length;key++) {
      if (age<plan.keys[key]) return key===0 && plan.impact.includes(attack.f)?1:key;
      age-=plan.keys[key];
    }
    return -1;
  }
  return -1;
}
function drawMatchedArcs(part) {
  if (!atk) return;
  const p=MATCHED_ARCS[atk.move];if (!p) return;
  const key=matchedArcKey(p,atk);if (key<0) return;
  const sheet=p.tints[st.elem];
  let y0=0,height=80,dx=p.offset[0],dy=p.offset[1];
  if (p.cycle) {
    const body=A.anchors[atk.move]?.[atk.f]?.body || p.referenceBody;
    dx+=Math.round(body[0]-p.referenceBody[0]);dy+=Math.round(body[1]-p.referenceBody[1]);
    y0=part==='back'?0:58;height=part==='back'?58:22;
  } else if (part==='back') return;
  cx.drawImage(sheet,(key%2)*128,Math.floor(key/2)*80+y0,128,height,
    20+dx,G-79+dy+y0,128,height);
}
