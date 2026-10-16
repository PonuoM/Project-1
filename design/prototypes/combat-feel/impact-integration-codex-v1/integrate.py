from pathlib import Path
p=Path('design/prototypes/combat-feel/index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('<div class="row"><b>ดาบ</b>', '<div class="row"><b>เอฟเฟกต์</b><span id="fxsets"></span></div>\n  <div class="row"><b>ดาบ</b>')
s=s.replace('ตัวละครเล่นตามเฟรมของท่า ส่วนเอฟเฟกต์ ประกายไฟ ตัวเลขดาเมจ จอสั่น และศัตรูกระเด็น เป็นโค้ดของเกม ปรับได้โดยไม่ต้องเจนใหม่','เอฟเฟกต์ใหม่: ระเบิด 16 เฟรม · ไฟ / น้ำแข็งแตก / พิษสาด อย่างละ 12 เฟรม · ปะทะตรงตัวมอน เลือกชุดเดิมเพื่อเทียบได้')
s=s.replace("boom:false };", "boom:false, fxset:'expanded' };\nconst reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;\nif (reducedMotion) st.auto = false;")
s=s.replace("const img = src => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = src; });", "const img = src => new Promise((resolve, reject) => { const i = new Image(); i.onload = () => resolve(i); i.onerror = () => reject(new Error('โหลดภาพไม่สำเร็จ: ' + src)); i.src = src; });")
s=s.replace("  A.hits = await json", """  const expandedBase = '../../concepts/fx-g10/codex/impact-expanded-v1/';
  A.expanded = {};
  for (const spec of await json(expandedBase + 'effects-v2.json')) {
    const key = ({'ice-shatter':'ice', 'poison-slash':'poison'})[spec.effect] || spec.effect;
    A.expanded[key] = { img: await img(expandedBase + spec.sheet), w:spec.frameWidth, h:spec.frameHeight,
      cols:spec.cols, times:spec.frames.map(f=>f.durationMs), duration:spec.totalEffectMs, anchor:[32,32] };
  }
  A.expanded.lightning = { img:await img('../../concepts/fx-g10/codex/lightning-v2.png'),
    w:256, h:256, cols:4, times:[20,30,25,45], duration:120, anchor:[32,52] };
  A.hits = await json""")
s=s.replace("  foe.flash = S.flash;", "  foe.flash = reducedMotion ? 0 : st.fxset === 'expanded' ? 25 : S.flash;")
s=s.replace("{ flashT = 90; }", "{ flashT = reducedMotion ? 0 : st.fxset === 'expanded' ? 22 : 90; }")
s=s.replace("  bursts.push({ e: st.elem, v: Math.floor(Math.random()*3), life: 0, x: foe.x - 4, y: G - 14, s: S.size });\n  if (st.boom) bursts.push({ e: 'explosion', v: Math.floor(Math.random()*3), life: 0, x: foe.x - 4, y: G - 14, s: S.size * 1.2 });", """  const contact = { x:foe.x + foe.kb - 4, y:G - A.kiki[0].height * 0.52, kb:foe.kb, fxset:st.fxset };
  bursts.push({ ...contact, e:st.elem, v:Math.floor(Math.random()*3), life:0, s:S.size });
  if (st.boom) bursts.push({ ...contact, e:'explosion', v:Math.floor(Math.random()*3),
    life:st.fxset === 'expanded' && st.elem !== 'none' ? -45 : 0, s:S.size * 0.9 });""")
s=s.replace("  const frozen = t < stopUntil;", "  if (document.hidden) { requestAnimationFrame(tick); return; }\n  const frozen = t < stopUntil;")
s=s.replace("bursts = bursts.filter(b => b.life < (HIT_LEN[b.e] || 8) * BURST_MS);", "bursts = bursts.filter(b => b.life < (b.fxset === 'expanded' && A.expanded[b.e] ? A.expanded[b.e].duration : (HIT_LEN[b.e] || 8) * BURST_MS));")
s=s.replace("const sx = shakeT > 0 ?", "const sx = !reducedMotion && shakeT > 0 ?").replace("sy = shakeT > 0 ?", "sy = !reducedMotion && shakeT > 0 ?")
s=s.replace("  bursts.forEach(b => {\n    cx.globalCompositeOperation", """  bursts.forEach(b => {
    if (b.life < 0) return;
    const sheet = b.fxset === 'expanded' && A.expanded[b.e];
    if (sheet) {
      let n=0, end=sheet.times[0];
      while (n < sheet.times.length-1 && b.life >= end) end += sheet.times[++n];
      // Native64px artwork, torso pivot; the first beat follows recoil, debris then detaches.
      const scale = b.e === 'lightning' ? 1 : Math.min(1.25, 0.85 + (b.s-0.9)*0.45);
      const follow = Math.max(0, 1-b.life/140);
      const x = b.x + (foe.kb-b.kb)*follow;
      const y = b.e === 'lightning' ? G : b.y;
      cx.globalCompositeOperation='lighter';
      cx.drawImage(sheet.img, (n%sheet.cols)*sheet.w, Math.floor(n/sheet.cols)*sheet.h, sheet.w,sheet.h,
        Math.round(x-sheet.anchor[0]*scale),Math.round(y-sheet.anchor[1]*scale),Math.round(64*scale),Math.round(64*scale));
      cx.globalCompositeOperation='source-over';
      return;
    }
    cx.globalCompositeOperation""")
s=s.replace("  buttons('elems', ELEMS, 'elem');", "  buttons('fxsets', {expanded:'ใหม่ · Sprite', original:'เดิม'}, 'fxset');\n  document.getElementById('auto').classList.toggle('on', st.auto);\n  buttons('elems', ELEMS, 'elem');")
s=s.replace("  requestAnimationFrame(tick);\n});", "  requestAnimationFrame(tick);\n}).catch(error => { document.querySelector('.note').textContent = error.message; console.error(error); });")
p.write_text(s,encoding='utf-8')
