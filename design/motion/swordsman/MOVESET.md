# นักดาบ (สายประชิด) — ชุดท่า v1

แผน (เจ้าของ 14 ต.ค.): เจนวิดีโอท่าละ 1 คลิปด้วย **ตัวเปล่าชุดเทา + ดาบสีม่วง** (Google Flow ใช้ได้เฉพาะงานท่าแบบนี้)
→ Claude แยกเฟรม → Codex/Gemini ใส่ชุดทับทีหลัง → Claude เปลี่ยนดาบม่วงเป็นอาวุธจริง (เลเยอร์)

- ภาพตั้งต้น: `input/base-sword-1280x720.png` (สไปรต์ `design/concepts/base-claude-v1/base-body-sword-64.png` ×8 บนเขียว #00B140 ที่ (300,168))
- เฟรมเริ่ม = เฟรมจบ (ยกเว้นท่าตาย) เพื่อให้วนต่อท่ายืนได้
- **ให้ไว**: ท่าโจมตีรวม 0.4–0.6 วิ ตอนตัดเฟรมเร่งด้วย `sprite_autopick.py --speed` แล้วเกมเร่ง/ชะลอตามค่าความเร็วโจมตีได้อีกชั้น
- 1 ท่า ≠ 1 สกิล: สกิลคือ ท่า + เอฟเฟกต์ + ตัวเลข สกิลหลายตัวใช้ท่าเดียวกันได้ (เช่น ฟันไฟ/ฟันสายฟ้า = ฟันปกติ + เอฟเฟกต์)

## ท่าดาบ

| id | ท่า | ใช้กับสกิลแบบ (อ้างอิง POE) | ความยาวในเกม | จังหวะโดน |
|---|---|---|---|---|
| S01 | ฟันปกติ (เฉียงลง) | โจมตีปกติ, Molten/Lightning Strike, Frenzy | ~0.45 วิ | 1 |
| S02 | แทง (พุ่งแทงตรง) | Perforate, Lunge, Spectral Throw (ปล่อยคลื่นตอนแทง) | ~0.5 วิ | 1 |
| S03 | ฟัน 3 จังหวะ (ฟัน–ฟันกลับ–ฟาดลง) | Double/Combo Strike, คอมโบจบด้วยแรงกระแทก | ~1.0 วิ | 3 |
| S04 | หมุนลูกข่าง (วนได้) | Cyclone, Bladestorm | วน ~0.35 วิ/รอบ | ทุกรอบ |
| S05 | กระโดดฟาดพื้น | Leap Slam (เข้าหาศัตรู + วงกระแทก) | ~0.8 วิ | 1 (ตอนลง) |
| S06 | พุ่งผ่านฟัน | Whirling Blades, Flicker Strike, Dash | ~0.4 วิ | 1 |
| S07 | ปักดาบลงพื้น | Earthshatter, Ground Slam (คลื่น/หนามจากพื้น) | ~0.8 วิ | 1 |
| S08 | แทงรัว (วนได้) | Blade Flurry, Lacerate | วน ~0.3 วิ | ทุก 2 เฟรม |
| S09 | เสยขึ้น | Uppercut / ลอยศัตรู, Rising Slash | ~0.5 วิ | 1 |

## ท่าพื้นฐาน (ถือดาบ)

| id | ท่า | หมายเหตุ |
|---|---|---|
| A01 | ยืนหายใจ (วน) | ท่าพักระหว่างตี |
| A02 | วิ่งอยู่กับที่ (วน) | ฉากเลื่อนแทน ตัวไม่เคลื่อนข้ามจอ |
| A03 | โดนตี | สะดุ้งถอยแล้วกลับ ~0.25 วิ |
| A04 | ตาย | ล้มหงาย ไม่วน (ไม่ใช้เฟรมจบ) |
| A05 | หลบ (กระโดดถอย) | ตอนหลบได้ |
| A06 | ตะโกนบัฟ | Warcry / บัฟ (Enduring Cry, Berserk) และใช้เป็นท่าร่ายของนักดาบ |

ลำดับทำ: S01 S02 S03 S04 (ที่เจ้าของขอ) → A01 A02 A03 A04 → S05–S09, A05 A06
Flow Veo 3.1 Lite: 5 เครดิตต่อคลิป → ครบ 15 ท่า ≈ 75 เครดิต (เจนซ้ำเฉพาะท่าที่เสีย เพดาน 3 ครั้ง/ท่า)

## Prompt (Flow: Frames to video, เฟรมเริ่มและเฟรมจบ = ภาพตั้งต้น, 16:9, 720p)

ส่วนหัวที่ใส่ทุก prompt:

```text
Static locked-off camera, side view, flat solid green background that never changes. A chibi pixel-art character in a plain grey bodysuit holding a short violet sword in the right hand. ACTION. Fast, snappy and weighty animation: quick anticipation, very fast strike, short hold on impact, quick return to the exact starting pose. The sword keeps exactly the same short length and violet colour the whole time. Same character, same size, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no new objects, no text.
```

ACTION ของแต่ละท่า:
- S01: He takes a small step forward and slashes the sword in one fast diagonal arc from high behind his shoulder down to low in front of him.
- S02: He pulls the sword back at hip height, then lunges forward with a long step and stabs straight ahead at chest height with the arm fully extended, then steps back.
- S03: He performs a fast three-hit combo: first a horizontal slash to the front, then a backhand slash returning the other way, then a big jumping overhead chop that slams the blade down to the ground in front of him.
- S04: He spins on the spot like a spinning top, two full turns, with the sword held straight out at arm's length, feet staying in place, then stops.
- S05: He crouches, jumps high forward, raises the sword over his head in the air, lands and slams the sword into the ground, then stands back up and steps back.
- S06: He dashes forward very fast and low with the sword held back, slicing as he passes, slides to a stop, then hops back to the start.
- S07: He raises the sword above his head with both hands and plunges it point-first into the ground in front of him while dropping to one knee, holds, then pulls it out.
- S08: He stabs forward again and again very fast, many short thrusts in a row like a flurry, without stepping.
- S09: He crouches low with the sword down behind him, then slashes upward in a rising arc while hopping slightly, and lands.
- A01: He stands ready and breathes slowly, shoulders rising and falling slightly. No walking.
- A02: He runs on the spot like on a treadmill, facing right, sword held low; he does not move across the screen.
- A03: He is hit from the front, flinches backward with his head snapping back, then recovers.
- A04 (เฟรมจบไม่ต้องใส่): He is hit hard, staggers, drops the sword arm, falls backward onto the ground and lies still.
- A05: He quickly hops backward to dodge, lands, then steps forward back to the start.
- A06: He plants his feet, raises the sword up and shouts a battle cry with his whole body tensed, then relaxes.

## ผลรอบแรก (14 ต.ค., Flow Veo 3.1 Lite, 4 คลิป = 20 เครดิต)
ไฟล์ต่อท่า: `video.mp4` (ต้นฉบับ), `frames/` (แปลงเป็นพิกเซล 128×80), `strip-manual.png` + `pick-manual.json` (Claude เลือกเฟรม จังหวะไว), `strip-auto.png` (อัตโนมัติ ทั้งคลิป ช้า) · เลือกเฟรมใหม่: แก้ `make_pick.py` แล้วรันซ้ำ

| ท่า | เฟรม / เวลา | ผล |
|---|---|---|
| S01 ฟันปกติ | 9 / 0.55 วิ | ดี: ง้างเหนือหัวแล้วฟาดลงหน้า · วิดีโอฟันซ้ำหลายรอบ (เลือกรอบเดียว) · มีเส้นวงดาบสีเทาติดมา · ดาบยาวขึ้นช่วงกลางคลิป (ไม่ได้ใช้ช่วงนั้น) |
| S02 แทง | 10 / 0.65 วิ | ดีที่สุด: ง้าง-พุ่งแทง ดาบยาวคงที่ · กลับท่ายืนแบบตัดฉับ (ต้องเติมเฟรมกลับ 1–2 เฟรม) |
| S03 ฟัน 3 จังหวะ | 16 / 0.85 วิ | ใช้ได้: ฟันหน้า-ฟันกลับ-กระโดดฟาดลง · ดาบหายไปช่วงหนึ่งในวิดีโอ (ไม่ได้ใช้) · ท่าที่ 1–2 ออกแนวแทงมากกว่าฟัน |
| S04 หมุน | 12 / 0.59 วิ (วนเฟรม 3–8) | หมุนจริง เห็นด้านหลัง · เฟรมหมุนมีรอยเบลอสีเขียวอมเทา ต้องเก็บมือ หรือให้ Codex วาดทับตอนใส่ชุด |

## H3 (MiniMax, เครดิตโบนัส 2 คลิป = 800 เครดิต, 14 ต.ค.) เทียบ Flow
| ท่า | เฟรม / เวลา | ผล |
|---|---|---|
| S01 ฟันปกติ H3 | 12 / 0.70 วิ | ตัวนิ่งกว่า Flow, ดาบยาวคงที่, ฟันรอบเดียวตามสั่ง · จังหวะฟาดมีรอยเบลอสีม่วงเป็นแผ่น (ใช้เป็นเส้นวงดาบได้ หรือแทนด้วยดาบจริง) |
| S02 แทง H3 | 11 / 0.71 วิ | ง้าง-พุ่งแทง-ค้าง-กลับท่ายืนครบ (กลับนุ่มกว่า Flow) · ดาบหายหลังตัว 2 เฟรมตอนง้าง (เลเยอร์ดาบเติมให้ได้) |

## SpriteFlow (spriteflow.io, เครดิตฟรี, 14 ต.ค.)
- 1 ท่า = 10 เครดิต (ฟรีวันละ ~15) · ใช้เวลา ~4 นาที · ข้างในคือเจนวิดีโอแล้วตัดเฟรม ("Generating video…") · ได้ 32 เฟรม PNG 1024² ลบพื้นหลังให้แล้ว (ไฟล์อยู่ที่ asset.spriteflow.io ดึงตรงได้)
- แปลงลงกริดของเรา: สเกล 12.4 px/art px ที่ (116,116) บนผืน 1024 → `S01-slash-spriteflow/` (13 เฟรม 0.77 วิ)
- ผล: ตัวละครคงที่ดี ท่าง้างค้างชัด · แต่ดาบใหญ่/ยาวขึ้นตอนง้าง และสั่ง "ฟันเฉียงลง" ได้ท่าแทงตรง

## PixelLab animate-with-text-v3 (1 gen/ท่า, เฟรมแรก=สุดท้าย = ตัวเปล่า 64px, 14 ต.ค.)
- ได้พิกเซลจริง 64×64 ไม่ต้องแปลง · ตัวละคร/ชุด/สีคงที่ที่สุดในทุกตัวที่ลอง · ใช้ 2.5–4 นาที
- v1 (prompt แบบเดียวกับวิดีโอ, 16 เฟรม): ท่าอ่อน ดาบยกตรงขึ้นซ่อนหลังหัว แล้วโผล่ข้างล่าง ครึ่งหลังเป็นท่ายืน
- v2 (prompt บอกทีละช่วงเฟรม + "exaggerated", 12 เฟรม): ง้างดาบหลังหัวเห็นชัด ยกขาก้าว แล้วตัดฉับไปท่าโดนต่ำ (ไม่มีเฟรมกลางวงฟัน → ใส่เส้นวงดาบเป็นเอฟเฟกต์) · ดาบหนาขึ้นตอนท่าต่ำ
- สรุป: กับ PixelLab ต้องเขียน prompt แยกทีละช่วงเฟรม (เหมือนบทเรียน E-Sport) ไม่ใช่ประโยคเดียวแบบวิดีโอ
