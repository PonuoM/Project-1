# แจ้ง Claude ก่อนปรับเกม: ฉากเดินทางและแอ็กชันเร็ว หนักแน่น

## คำสั่งเพิ่มเติม: ทดลอง PixelLab กับนักดาบ

เจ้าของแจ้งว่าภาพ prototype ยังไม่สวย และขอให้เชื่อม PixelLab แล้วเริ่มทดลองนักดาบ Codex จึงสร้างงานแยกใน `design/pixellab/swordsman/` โดยใช้ AI image-generation API ภาพนักดาบที่วาดด้วยโค้ดก่อนหน้านี้ยังไม่ถือว่าเจ้าของยอมรับ ห้ามนำเป็นต้นแบบภาพสุดท้ายโดยอัตโนมัติ ดู README/prompt/preview ในโฟลเดอร์ใหม่ และอ่าน provenance ใน `CREDITS.md` การทดลองนี้ไม่เปลี่ยน timing เป้าหมาย “ออกไว กระแทกหนัก” และยังไม่เปลี่ยน manifest/client/server

สถานะ: ทำ prototype แยกใน `design/prototypes/action/` เพื่อให้เจ้าของลองก่อนนำไปใช้จริง การเลือก layout และค่าตัวเลขยังเป็นการทดลอง ไม่ใช่การอนุมัติให้เปลี่ยน production ทั้งชุด

## คำสั่งล่าสุดของเจ้าของ (มีลำดับเหนือ brief เดิม)

เจ้าของชอบ UI และท่าใช้สกิลจาก `20261013-1555-21.4804181.mp4` และ `20261013-1553-31.4581978.mp4`: พื้นที่เกมขนาดเล็กได้ มีฉากหลังและพื้นที่เลื่อนไปมา เห็นตัวละครเดินจริง พร้อม UI กรอบแฟนตาซีและแอนิเมชันสกิลชัดเจน เจ้าของย้ำว่า **แอ็กชันต้องออกไว ดูหนักแน่น แรง ๆ** และให้เขียนแจ้งสิ่งที่ Claude ต้องรู้ก่อนแก้ส่วนที่มีผลต่อเกม

Codex ทำความเข้าใจ ref จากภาพในคลิป ไม่คัดลอก artwork ของเกมต้นฉบับ ภาพฉากเต็มจอบางช็อตเป็นภาพโปรโมต/วอลเปเปอร์ ไม่ใช่ข้อกำหนดว่าต้องทำเกมเต็มจอ

## ทำไมงานเดิมยังไม่ตรง

- `GAME_BRIEF.md` §7.1 วางเกมเป็นแถบสูงประมาณ 60px, §9 วาง pixel art 32px
- `design/CODEX_PROMPTS.md` Prompt 3 จำกัด band 64px และกำหนดฮีโร่เดิน/สู้กับที่; Prompt 6 ให้พื้นเพียง 64×8 ไม่มีฉากหลังหลายชั้น
- `client/src/main/index.ts` ยึด strip เต็มความกว้างจอ ย้าย/ปรับขนาดไม่ได้ และหน้าต่างหลัก 960×600
- `client/src/renderer/src/game/StripScene.ts` เล่นท่าเดินที่ตำแหน่งฮีโร่คงที่ โดย tween มอนเข้ามาหา ยังไม่มี camera/world scrolling
- `client/src/renderer/src/window/panels.ts` ยังแสดงช่องสกิลเป็น placeholder
- Sprites เดิมผ่านสัญญาขนาด/สี/ไฟล์ แต่รายละเอียดและ key poses ยังต่ำกว่า ref การผ่าน QA ไฟล์ไม่ใช่การยืนยัน visual fidelity

## Prototype ที่ Codex กำลังทำ

เปิด `design/prototypes/action/index.html` โดยตรง หรือผ่าน local web server มี 3 layout (`?variant=A/B/C`) ใช้ฉาก/แอ็กชันเดียวกันเพื่อเลือกการจัดพื้นที่: widget กะทัดรัด, แถบเดินทางกว้าง, ฉากพร้อมแผงอุปกรณ์ด้านข้าง

เดินผ่านฉากป่าหลายชั้น → พบมอน → ฟันเร็ว → ใช้สกิล → เก็บของ → เดินต่อ มีปุ่มใช้สกิล, พัก, เปิด/ปิดเล่นเอง, เปลี่ยน layout และลากเลื่อนกล้องบน canvas ตัวเลขและ combat outcome เป็นข้อมูลจำลองในหน่วยความจำ

ใช้ sprites ทดลองแยกใน `design/prototypes/action/assets/` ไม่เพิ่มลง manifest หลัก ไม่เปลี่ยน PNG เดิม ไม่ให้ `sync-design.mjs` ดึงไปใช้โดยอัตโนมัติ

## จังหวะแอ็กชันเป้าหมาย (ค่าทดลอง)

| ช่วง | ฟันธรรมดา | สกิลกระแทก |
|---|---:|---:|
| เตรียมท่า | 35ms | 70ms |
| พุ่ง/เหวี่ยงก่อนโดน | 55ms | 65ms |
| Hit stop เฉพาะโลกเกม | 45ms | 60ms |
| คืนท่า | 105ms | 145ms |

ความแรงมาจาก key pose ที่ต่างกันชัด, ระยะพุ่งสั้น, slash ที่ขยายเกินกรอบตัวละคร, มอนสะดุ้ง/ถอย, ฝุ่น/เศษพิกเซล, ตัวเลขเด้งเร็ว และ camera shake สั้น 2–4px ในพื้นที่เกม ไม่ใช่ชะลอท่าทั้งชุด ตัวละครเป้าหมายสูงราว 48px บนจอและมีพื้นที่เผื่อเอฟเฟกต์ ไม่จำเป็นต้องขยายทั้ง UI

ท่าโจมตีควรอัปเดต animation/render ที่ 60 FPS ในโหมดดูฉาก; background idle mode อาจใช้ FPS ต่ำเพื่อประหยัดเครื่อง ปัจจุบัน settings รองรับ 10/15/30 FPS (ค่าเริ่มต้น 15) โดย 10/15 FPS หนึ่งเฟรมกิน 100/67ms และไม่สามารถแสดงช่วงเตรียม 35ms ได้ครบ เรื่องนี้ต้องแก้ทั้ง setting และ renderer เมื่อเลือกนำไปใช้จริง

Hit stop ต้องแช่เฉพาะภาพโลก/ตัวละคร ไม่หยุด UI timer, server sync, input หรือเวลาปลดล็อกกล่อง Reduced motion ปิด shake/flash; เอฟเฟกต์แสงจำกัดบริเวณตัวละครและไม่ใช้ full-screen flash

## จุดที่ต้องประสานก่อนเชื่อม production

1. **World/camera:** แยกตำแหน่ง world ของฮีโร่/มอนจาก screen HUD; camera follow ขณะเดิน, พัก camera ขณะโจมตี, drag pan แล้วกลับมาตามฮีโร่ ต้องไม่ใช้ full-window pointer-events ที่ทำให้ desktop click-through หาย
2. **Native window:** หากเลือก widget ย้ายได้/ปรับขนาดได้ แก้ `client/src/main/index.ts`, drag handle, hit regions, workArea/taskbar/DPI/multi-monitor constraints ไม่เปลี่ยนการคลิกทะลุโดยใช้ HTML เพียงอย่างเดียว
3. **Animation contract:** sprite source อาจไม่ใช่ 32×32; frameWidth/frameHeight ต้องอ่านต่อ sheet, combat FX แยก sheet มี hit event ตรงจังหวะโดน ไม่ยัด slash ใหญ่ให้ติดขอบ frame ตัวละคร
4. **Combat authority:** คง gold, kills, drops และ rate จาก server ไม่เพิ่มจำนวน hit/kill จริงเพียงเพราะภาพโจมตีเร็วขึ้น สามารถเล่นหลาย visual strikes ภายใน kill cycle เดิมได้ `rates.killMs` และ offline rewards ยังคงอำนาจที่ server
5. **Skills:** prototype แสดง visual skill อย่างเดียว ไม่ได้ตัดสินจำนวนช่อง, หินสกิล, damage multiplier, cooldown จริง, ราคา หรือ reward balance ถ้าจะทำ skill mechanics ต้องกำหนดกับเจ้าของแยก
6. **UI:** รักษาเมนูรวมหน้าต่างเดียว เปลี่ยน visual hierarchy เป็นกรอบแฟนตาซีกะทัดรัด; ข้อมูล inventory เลื่อนภายในได้ ต้องรักษาข้อความไทยและเปรียบเทียบอุปกรณ์
7. **Assets/build:** `sync-design.mjs`, `sheets.ts`, asset loader, preload และ animation timings ต้องตรวจหลังยอมรับ direction ใหม่ ห้ามแทนที่ manifest/sprites เดิมด้วยไฟล์ prototype โดยอัตโนมัติ

## สิ่งที่ยังไม่เปลี่ยนในรอบ prototype

ไม่มีการแก้ `client/`, `server/`, `GAME_BRIEF.md`, tokens หลัก หรือ manifest หลัก ไม่ส่งข้อความ/อัปโหลดให้ Claude ผ่านระบบภายนอก ไฟล์นี้เป็นบันทึกให้ agent อ่านใน workspace

หลังเจ้าของเลือก prototype: อัปเดต brief และ prompts ให้ระบุ camera movement, scene viewport, skill timing, sprite detail, FPS และ layout ที่เลือกก่อนทำ production implementation ไม่ใช้ข้อกำหนดเก่า “เดินกับที่บน band 64px” เป็นอำนาจเหนือความต้องการล่าสุด

---

## อัปเดตจาก Claude (13 ต.ค. 2026 ดึก): ทดลองนักดาบ PixelLab ใน prototype

### สถานะเกมจริงที่ต้องรู้ก่อน
เจ้าของเลือก **layout A + ให้ Codex ใช้ PixelLab** ไปแล้วในรอบก่อน และ Claude ทำ widget A ลง `client/` แล้ว (ลากย้ายได้, parallax, กล้องตาม, จังหวะฟัน/hit stop/shake ตามตารางด้านบน, ภาพยังเป็นชุด 32px เดิม) รายละเอียดใน `GAME_BRIEF.md` §7.1, §9 และ `design/CODEX_PROMPTS.md` Prompt 7 ข้อห้ามในส่วน "สิ่งที่ยังไม่เปลี่ยนในรอบ prototype" ด้านบนจึงไม่ตรงกับ `client/` ปัจจุบันแล้ว

### รอบนี้แก้เฉพาะ `design/` (ไม่กระทบเกมจริง)
| ไฟล์ | การเปลี่ยน |
|---|---|
| `design/pixellab/swordsman/cleaned/` (ใหม่) | สำเนาที่ลบพิกเซลหลุด/จัดแนวแล้ว พร้อม `animation.json` และ `inspection.json` ของสำเนา ไฟล์ต้นฉบับ PixelLab ไม่ถูกแก้ |
| `design/tools/clean_pixellab_frames.py` (ใหม่) | สคริปต์ตรวจและทำสำเนาที่ปรับแล้ว (ไม่เรียก PixelLab) |
| `design/prototypes/action/index.html`, `prototype.js`, `prototype.css`, `NOTES.md` | เพิ่มตัวเลือกภาพ PixelLab (ปรับแล้ว / ต้นฉบับ) สลับกับภาพโค้ดเดิม, อ่านขนาด/เฟรม/FPS/impact/hit stop จาก `animation.json`, คลื่นฟัน ฝุ่น มอนสะดุ้ง |

ไม่แตะ `client/`, `server/`, `design/sprites/manifest.json`, `sync-design.mjs` และไม่เรียก PixelLab

### ถ้าเจ้าของเลือกนักดาบ PixelLab: ไฟล์ที่ต้องแก้ตอนเชื่อมเกมจริง (ยังไม่ทำ)
| ไฟล์ | ผลกระทบ |
|---|---|
| `design/sprites/manifest.json` + PNG (Codex) | เพิ่ม/แทน `hero_melee_attack` เป็น 64×64 9 เฟรม `fps 32`, `events.impact 3`, และฟิลด์ใหม่ `hitStopMs` · เพิ่ม `hero_melee_idle`/`walk` เมื่อมีจาก PixelLab |
| `client/src/renderer/src/sheets.ts` | รับฟิลด์ `hitStopMs` (ไม่บังคับ) |
| `client/src/renderer/src/game/WorldScene.ts` | ท่าฟันเล่นตามเฟรม/FPS ของ sheet แทนตาราง 35/55/45/105ms เมื่อ sheet ระบุ `fps`; ระยะปะทะตามความกว้างดาบ; คลื่นฟัน/ฝุ่นแบบ prototype นี้ |
| `client/src/renderer/src/game/assets.ts` | ไม่ต้องแก้ (อ่านขนาดเฟรมต่อ sheet อยู่แล้ว) |
| `server/` | ไม่ต้องแก้ ภาพเร็วหรือช้าไม่เปลี่ยนอัตราฆ่า/รางวัล (`rates.killMs` จาก server) |
| `design/CREDITS.md` | ระบุไฟล์ที่มาจาก PixelLab (Steam AI disclosure) |

### ผลรอบนี้
- Prototype: `http://localhost/Projects-1/design/prototypes/action/index.html?variant=A&art=clean` (`art=clean|raw|code`, `variant=A|B|C`) ต้องเปิดผ่าน web server เพราะอ่าน `animation.json` ด้วย fetch ถ้าเปิดไฟล์ตรง ๆ ปุ่ม PixelLab จะปิดและแสดงคำอธิบาย
- จังหวะที่วัดได้ในเบราว์เซอร์: impact ที่ a.t = 94ms (เฟรม 3) ค้าง 45ms แล้วคืนท่าจนจบราว 326ms
- Layout B ย้ายตำแหน่งฮีโร่ในกล้องเป็น 40% ของความกว้าง เพราะแถบปุ่มในฉากบังตัวละครที่สูงขึ้น
- ยังรอเจ้าของเลือก: ตัวละคร (candidate 1–16), layout A/B/C และว่าจะสั่ง PixelLab ทำท่าเดิน/ท่าสกิลต่อหรือไม่

### อัปเดต 14 ต.ค. 2026 (บ่าย): ภาพ 3D → pixel
Codex โควตาหมดระหว่างทำ Prompt 8/8.1 Claude ทำต่อใน `design/3d/build_and_render.py`, `design/tools/pack_sprites3d.py`, `design/prototypes/wardrobe/render3d-character.js` (+ แก้ข้อความไทยที่เสียเป็น ? ใน `index.html`, `wardrobe.js`) รายละเอียดและข้อจำกัดอยู่ใน `design/prototypes/wardrobe/NOTES.md` เกมจริง (`client/`) ยังไม่ได้เชื่อมกับ `design/sprites3d/` รอเจ้าของตัดสินภาพก่อน
