# ทดสอบ MiniMax Design (เครดิตฟรี 3,000) — ฟันปกติ + แทง

เป้าหมาย: ดูว่า H3 ในแอปให้ผลเท่า H3 ผ่าน API ไหม ใส่ "เฟรมแรก = เฟรมสุดท้าย" ได้ไหม และ H3 Max 480P (ถูกกว่า) ใช้ได้ไหม
ประมาณการ: คลิป 768P 5 วิ ≈ 350 เครดิต, 480P ≈ 200 เครดิต → 4 คลิป ≈ 1,100 จาก 3,000

## ภาพตั้งต้น
`design/motion/swordsman/input/base-sword-1280x720.png` (ตัวเปล่าชุดเทา ดาบม่วง พื้นเขียว)

## ทางลัด: สั่ง agent ของ MiniMax Design ทีเดียว 4 คลิป
แนบภาพตั้งต้น 1 ภาพ (ปุ่ม +) แล้ววางข้อความนี้ในช่องแชตของแอป (โหมด Auto):

```text
Make 4 separate image-to-video clips from the attached image. For EVERY clip use the attached image unchanged as BOTH the first frame and the last frame, 16:9, 5 seconds, 1 output each. Do not redesign, restyle, upscale or crop the character, do not add a script, music, voice or editing. Just the 4 raw video generations:
1) model MiniMax H3, 768P, prompt A
2) model MiniMax H3, 768P, prompt B
3) model MiniMax H3 Max, 480P, prompt A
4) model MiniMax H3 Max, 480P, prompt B
Prompt A: (วาง Prompt ฟัน ด้านล่าง)
Prompt B: (วาง Prompt แทง ด้านล่าง)
Before generating, tell me the credit cost of each clip.
```
ถ้า agent จะทำเกินที่สั่ง (เขียนสคริปต์ ใส่เพลง ตัดต่อ) ให้หยุดแล้วทำทีละคลิปตามขั้นตอนด้านล่างแทน

## ขั้นตอน (ทำในแอป ทีละคลิป)
1. Start Creating → กด **+** แนบภาพตั้งต้น
2. **Models** → เลือก MiniMax H3 (คลิป 1–2) หรือ H3 Max (คลิป 3–4)
3. ตั้ง 16:9, 5 วิ, ความละเอียดตามตาราง, 1 คลิป
4. ถ้ามีช่อง First frame / Last frame ให้ใส่ภาพเดียวกันทั้งสองช่อง
   ถ้าไม่มี ให้พิมพ์บรรทัดนี้นำหน้า prompt: `Use the attached image as BOTH the first frame and the last frame of the video. Do not redesign the character.`
5. วาง prompt แล้วสร้าง
6. ดาวน์โหลด mp4 แล้วบันทึกไว้ที่โฟลเดอร์ในตาราง ตั้งชื่อ `video.mp4` (หรือทิ้งไว้ใน Downloads แล้วบอก Claude)

| คลิป | โมเดล | ความละเอียด | prompt | บันทึกที่ |
|---|---|---|---|---|
| 1 | H3 | 768P | ฟัน | `design/motion/swordsman/S01-slash-mmd768/` |
| 2 | H3 | 768P | แทง | `design/motion/swordsman/S02-thrust-mmd768/` |
| 3 | H3 Max | 480P | ฟัน | `design/motion/swordsman/S01-slash-mmd480/` |
| 4 | H3 Max | 480P | แทง | `design/motion/swordsman/S02-thrust-mmd480/` |

## Prompt ฟัน
```text
Static locked-off camera, side view, flat solid green background that never changes. A chibi pixel-art character in a plain grey bodysuit holding a short violet sword in the right hand. He takes a small step forward and slashes the sword in one fast diagonal arc from high behind his shoulder down to low in front of him, only once. Fast, snappy and weighty animation: quick anticipation, very fast strike, short hold on impact, quick return to the exact starting pose. The sword keeps exactly the same short length and violet colour the whole time. Same character, same size, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no new objects, no text.
```

## Prompt แทง
```text
Static locked-off camera, side view, flat solid green background that never changes. A chibi pixel-art character in a plain grey bodysuit holding a short violet sword in the right hand. He pulls the sword back at hip height, then lunges forward with a long step and stabs straight ahead at chest height with the arm fully extended, only once, then steps back. Fast, snappy and weighty animation: quick anticipation, very fast strike, short hold on impact, quick return to the exact starting pose. The sword keeps exactly the same short length and violet colour the whole time. Same character, same size, chunky pixel art, no camera movement, no zoom, no motion blur, no effects, no new objects, no text.
```

จดไว้ด้วย: แต่ละคลิปใช้กี่เครดิต และแอปมีช่องเฟรมแรก/เฟรมสุดท้ายไหม

## ผล (14 ต.ค.)
- คลิป 1 (H3 768P ฟัน) สำเร็จ · แอปใช้ `mode: first-last-frame` จริง (ภาพเดียวกันเป็นเฟรมแรก+สุดท้าย) · ได้ 1344×768, 5.17 วิ = เหมือน H3 ผ่าน API
- agent ของแอปโหลดสกิล `h3-prompt-expert` แล้วเขียน prompt ใหม่ให้ละเอียดขึ้นเอง (ยังตรงท่าที่สั่ง)
- ไฟล์ที่แอปเจนอยู่ที่ `C:\Users\user\Movies\Hub\Projects\<ชื่อโปรเจกต์>\` → Claude ดึงเองได้ ไม่ต้องดาวน์โหลด
- แอปไม่ส่งจำนวนเครดิตที่ใช้กลับมา ต้องดูยอดคงเหลือในแอปเอง
- แปลงแล้ว: `S01-slash-mmd768/` (12 เฟรม 0.71 วิ)
