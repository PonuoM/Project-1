# Idle Loot (ชื่อชั่วคราว) — ต้นแบบ

เกม idle ล่าของใน widget เล็กที่ลอยบนสุดของจอ Windows
โจทย์เกมทั้งหมดอยู่ที่ [GAME_BRIEF.md](GAME_BRIEF.md)

## โครงสร้าง

| โฟลเดอร์ | คืออะไร |
|---|---|
| `client/` | ตัวเกม: Electron 44 + TypeScript + Phaser 3.90 |
| `server/` | หลังบ้าน PHP + MySQL เป็นผู้คำนวณรางวัลทั้งหมด (ตัวเกมแค่แสดงภาพ) |
| `design/` | งานดีไซน์จาก Codex: tokens, sprite, mockup **เป็นต้นฉบับที่เดียว** |

## รันครั้งแรก

1. **ฐานข้อมูล** (AppServ):
   ```
   C:\AppServ\MySQL\bin\mysql.exe -uroot -p < server\schema.sql
   ```
2. **รหัสฐานข้อมูล**: สร้าง `server/config.local.php`
   ```php
   <?php return ['db' => ['pass' => 'รหัส MySQL ของคุณ']];
   ```
   ทดสอบ: เปิด `http://localhost/Projects-1/server/public/api.php?a=state` ต้องได้ `{"error":"unauthorized"}`
3. **ตัวเกม**:
   ```
   cd client
   npm install
   npm run dev
   ```
   ถ้าขึ้นว่าไม่พบ `electron.exe` ให้รัน `node node_modules/electron/install.js`

## ใช้งาน

- **Widget** ลอยบนสุดเสมอ เริ่มที่มุมขวาล่างเหนือ taskbar
  - **ลากแถบชื่อ** (แถบบนสุดของกรอบ) เพื่อย้ายไปไว้ตรงไหนก็ได้ เกมจำตำแหน่งไว้ ถ้าหายไปไหน ใช้เมนูถาดระบบ "ย้าย widget กลับมุมขวาล่าง"
  - ลากฉากเพื่อเลื่อนกล้องดูรอบ ๆ ปล่อยแล้วกล้องกลับมาตามฮีโร่เอง
  - ปุ่มด้านล่าง: กล่องไม้ (คลิก = เปิด 1 ใบ), เปิดทั้งหมด (มีตั้งแต่ 5 ใบ), กล่องทอง, สกิล (กด Space ได้ตอน widget ถูกเลือก), ⛶ เปิดหน้าต่างเกม
  - พื้นที่โปร่งใสเหนือกรอบ (ที่ป๊อปอัปขึ้น) คลิกทะลุไปโดนโปรแกรมข้างหลังได้
- **หน้าต่างเกม** (ฮีโร่ / กระเป๋า / กล่อง / สำรวจ / ตั้งค่า): กดปุ่ม ⛶ ขวาสุดของ widget หรือคลิกไอคอนเกมในถาดระบบ กด Esc เพื่อปิด
  - กระเป๋า: คลิกไอเทมเพื่อสวมใส่หรือขาย ดับเบิลคลิก = สวมทันที ชี้ค้างเพื่อเทียบกับของที่สวม
  - ขายอัตโนมัติ (ตั้งที่กระเป๋า บันทึกที่บัญชี) และกระเป๋าเต็ม 80 ช่องจะขายของใหม่ที่ไม่ได้สวมให้เอง
  - ตั้งค่า (FPS ของ widget 60/30, แจ้งเตือนกล่องทอง) และตำแหน่ง widget บันทึกในเครื่องที่ `%APPDATA%\idle-loot-client\settings.json`
- **คลิกขวาไอคอนเกมในถาดระบบ** (มุมขวาล่าง สี่เหลี่ยมสีทอง): เปิดหน้าต่างเกม / ย้าย widget กลับมุมขวาล่าง / ทดสอบฟอนต์ภาษาไทย / โหลดเกมใหม่ / เปิด DevTools / ออกจากเกม
- ฟอนต์: วางไฟล์ที่ `client/src/renderer/public/fonts/GameFont.ttf` (ดู README ในโฟลเดอร์นั้น)

## งานดีไซน์ (Codex)

- Prompt อยู่ที่ [design/CODEX_PROMPTS.md](design/CODEX_PROMPTS.md) Codex เขียนได้เฉพาะใน `design/`
- `npm run dev` / `npm run build` จะรัน `scripts/sync-design.mjs` ให้อัตโนมัติ คัดลอก sprite, tokens และ CSS ของหน้าต่างเกม (`design/mockups/tokens.css`, `window.css`) เข้าเกม
- หน้าต่างเกมใช้ class `tb-*` ของ mockup ตรง ๆ ถ้า Codex แก้ `window.css` เกมจะเปลี่ยนตามเอง
- widget ใช้ class `tw-*` ถ้ามี `design/mockups/widget.css` (Prompt 7) จะโหลดทับหน้าตาพื้นฐานเอง
- ฉากหลัง: ถ้ามี `design/backgrounds/backgrounds.json` เกมใช้ภาพหลายชั้นของ Codex ถ้ายังไม่มีจะวาดป่ามืดด้วยโค้ด (ย้ายมาจาก prototype ของ Codex)
- ตัวละครอ่านขนาดเฟรมจาก manifest ทีละไฟล์ ถ้า Codex ส่ง `hero_melee_*` ขนาด 64×64 มา เกมใช้ได้ทันทีโดยไม่ต้องแก้โค้ด
- sprite ใหม่ใส่ใน `design/sprites/manifest.json` ตามรูปแบบเดิม เกมจะโหลดและสร้างแอนิเมชันเอง

## ทดสอบ / แก้สมดุล

- ตัวเลขสมดุลทั้งหมดอยู่ที่ `server/src/Rules.php`
- ฐานข้อมูลที่สร้างก่อนวันที่ 13 ต.ค. 2026 ให้รัน `server/migrations/001_auto_sell.sql` เพิ่ม
- จำลองว่าปิดเกมไป 2 ชั่วโมง (แทน `<id>` ด้วยเลขบัญชี):
  ```sql
  UPDATE heroes SET last_sync_at = last_sync_at - INTERVAL 2 HOUR WHERE account_id = <id>;
  ```
- ให้กล่องทองพร้อมเปิดทันที:
  ```sql
  UPDATE boxes SET unlock_at = UTC_TIMESTAMP(3) WHERE account_id = <id> AND type = 'gold' AND opened_at IS NULL;
  ```
- เริ่มใหม่ทั้งหมด: `DROP DATABASE idle_loot;` แล้วรัน `schema.sql` ใหม่ (เกมจะสร้างบัญชีใหม่ให้เอง)
