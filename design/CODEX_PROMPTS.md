# Prompt สำหรับ Codex (งานดีไซน์)

> **ทิศทางทดลองล่าสุด:** เจ้าของต้องการฉากที่เห็นตัวละครเดินจริง พร้อมแอ็กชันออกไวและกระแทกหนัก ก่อนปรับ UI / scene / FPS ในเกม โปรดอ่าน [CLAUDE_HANDOFF_ACTION_PROTOTYPE.md](CLAUDE_HANDOFF_ACTION_PROTOTYPE.md) และลอง [prototype](prototypes/action/index.html) ข้อกำหนดด้าน layout ของ Prompt 1–6 ด้านล่างเป็นฐานงานเดิม; prototype ยังรอการเลือก layout และไม่ควรซิงค์ assets ทดลองเข้าเกมโดยอัตโนมัติ
>
> **ทดลองภาพใหม่ด้วย PixelLab:** เจ้าของยังไม่ยอมรับภาพที่วาดด้วยโค้ด จึงขอให้ลองนักดาบจาก PixelLab ดู [ภาพ 16 ตัวเลือกและท่าฟัน](pixellab/swordsman/preview.html) พร้อม prompt / provenance ในโฟลเดอร์นั้น ยังไม่เปลี่ยน manifest หรือ assets ในเกม

วิธีใช้: คัดลอกทีละ prompt ไปให้ Codex **เรียงตามลำดับ 1 → 6**
- Prompt 1 ต้องเสร็จก่อน เพราะ prompt อื่นใช้สีและขนาดจาก Prompt 1
- Prompt 2, 3, 4 สั่งพร้อมกันได้หลัง Prompt 1 เสร็จ
- Prompt 5, 6 ทำต่อหลังชุดภาพพื้นฐานเสร็จ และสั่งพร้อมกันได้
- Codex เขียนไฟล์ได้เฉพาะในโฟลเดอร์ `design/` เท่านั้น ฝั่ง Claude จะเป็นคนเอาไปใส่ในเกม

| # | ทำอะไร | ไฟล์ที่ได้ |
|---|---|---|
| 1 | แนวภาพ ชุดสี สีระดับความหายาก | `design/tokens.json`, `design/STYLE_GUIDE.md`, `design/palette.png` |
| 2 | Sprite ตัวละคร มอนสเตอร์ กล่อง ไอคอน | `design/sprites/*.png`, `design/sprites/manifest.json`, `design/sprites/preview.html` |
| 3 | หน้าตาแถบบน taskbar | `design/mockups/strip.html`, `design/mockups/NOTES.md` |
| 4 | หน้าตาหน้าต่างใหญ่ (เมนูทั้งหมด) | `design/mockups/window.html` |
| 5 | ไอคอนแอป (ถาดระบบ, taskbar, ตัวติดตั้ง) | `design/icons/*` |
| 6 | ชุดภูมิภาค: มอนใหม่ บอส และพื้นของแต่ละภูมิภาค | `design/sprites/*` (เพิ่มใน manifest เดิม) |

> สถานะ 13 ต.ค. 2026 (ค่ำ): Prompt 1–4 เสร็จและใส่ในเกมแล้ว · เจ้าของเลือก widget แบบ A จาก prototype `design/prototypes/action/` และให้ Codex ใช้ PixelLab
> - ส่ง **Prompt 7** ได้เลย (แทน Prompt 3 และ Prompt 6 เรื่องขนาด: ตัวละครไม่ต้องอยู่ใน band 64px แล้ว)
> - Prompt 5 (ไอคอน) ยังใช้ได้ ส่งพร้อมกันได้
> - Prompt 6 ถ้ายังไม่ได้ส่ง **ไม่ต้องส่ง** เนื้อหาเรื่องภูมิภาครวมไว้ใน Prompt 7 ส่วน B แล้ว
>
> สถานะ 14 ต.ค. 2026: เจ้าของยังไม่พอใจห้องลองชุด PixelLab และโควตาหมด → ส่ง **Prompt 8** (ทำ sprite เองด้วย 3D → pixel ใน Blender) ได้เลย · ตามด้วย **Prompt 8.1** (ต้องเป็นตัวละครผมเขียวเดิม ไม่ใช่ KayKit Rogue)
> - อัปเดต 14 ต.ค. (บ่าย): Codex โควตาหมดกลางงาน **Claude ทำ Prompt 8 + 8.1 ต่อจนใช้งานได้แล้ว** (ดู `design/prototypes/wardrobe/NOTES.md` หัวข้อ 3D render source) ถ้าส่งงานต่อให้ Codex ให้เริ่มจากหัวข้อ Known gaps ในไฟล์นั้น ไม่ต้องทำใหม่
>
> อัปเดต: Prompt 5–6 สร้าง assets และตรวจผ่านแล้ว — ดู `design/icons/preview.html`, `design/sprites/preview.html` และ `design/regions.json` พร้อมให้ฝั่งเกมนำไปเชื่อม

---

## Prompt 1: แนวภาพ ชุดสี และ design tokens

```text
You are the art director for a small indie PC game. Produce the visual foundation that every other asset will follow.

## The game
An idle loot-hunting RPG that lives on the Windows desktop. A thin transparent strip sits directly above the Windows taskbar; inside it a tiny 32x32 pixel-art hero auto-fights monsters while the player works. Monsters drop wooden boxes (open instantly) and gold boxes (must unlock on a timer). Setting: classic medieval fantasy. Mood: cozy, cheerful, satisfying "loot pop" moments. Players are Thai and English speakers; all in-game copy is Thai first.

Hard constraint: the strip is drawn over ANY background the user has — a white spreadsheet, a dark code editor, a bright wallpaper. Every sprite and text must stay readable on all of them.

## Deliverables (write ONLY inside the `design/` folder; do not touch any other folder)
1. `design/tokens.json` — exactly this shape (fill in values; hex colors as "#RRGGBB", alpha colors as "rgba(r,g,b,a)"):
{
  "version": 1,
  "palette": { "<name>": "#RRGGBB", ... },          // 24–32 colors max, named (e.g. "ink", "outline", "skin_mid", "wood_dark", "gold_light")
  "rarity": {
    "common": "#RRGGBB", "uncommon": "#RRGGBB", "rare": "#RRGGBB", "epic": "#RRGGBB", "legendary": "#RRGGBB"
  },
  "ui": {
    "bandBg": "rgba(...)",        // translucent plate behind the strip (may be fully transparent if you choose the no-plate style)
    "bandBorder": "rgba(...)",
    "text": "#RRGGBB",
    "textMuted": "#RRGGBB",
    "textOutline": "#RRGGBB",     // 1px outline/shadow color behind all text
    "accent": "#RRGGBB",
    "danger": "#RRGGBB",
    "panelBg": "#RRGGBB",         // big window background
    "panelBgAlt": "#RRGGBB",
    "panelBorder": "#RRGGBB"
  },
  "spacing": { "xs": 2, "sm": 4, "md": 8, "lg": 12, "xl": 16 },   // px
  "radius": { "sm": 0, "md": 2 },                                  // px; pixel style prefers 0–2
  "font": {
    "family": "GameFont",
    "fallback": ["Leelawadee UI", "Tahoma", "sans-serif"],
    "sizes": { "xs": 10, "sm": 12, "md": 16, "lg": 24 }            // px; pick sizes that stay crisp for a pixel font
  }
}
2. `design/STYLE_GUIDE.md` (Thai or English) covering: pixel rules (32x32 characters, 16x16 icons, no anti-aliasing, 1px dark outline on every sprite for readability on light AND dark backgrounds, light source from top-left, max colors per sprite), palette usage, rarity color meaning, how text is drawn (outline/shadow), do/don't examples.
3. `design/palette.png` — every palette color as a 16x16 swatch in one row, same order as tokens.json, with nothing else in the image.

## Rules
- Rarity colors must be distinguishable for color-blind players (also differ in brightness, not only hue) and readable on both white and near-black.
- No external URLs, fonts, or CDNs. Original work only; if you use anything third-party it must be CC0 and listed in `design/CREDITS.md`. If you used AI image generation for anything, say so in `design/CREDITS.md` (Steam requires disclosure).
- When done, reply with a short summary of the chosen style and the rarity colors.
```

---

## Prompt 2: Sprite (ตัวละคร มอนสเตอร์ กล่อง ไอคอน)

```text
Create the pixel-art sprite sheets for an idle loot RPG that runs in a thin strip above the Windows taskbar.

First read `design/tokens.json` and `design/STYLE_GUIDE.md` and follow them exactly (palette colors only, 1px dark outline, no anti-aliasing).

## Technical format (the game loads these automatically — follow precisely)
- PNG, transparent background, no anti-aliasing, palette colors only.
- One PNG per animation. Frames laid out left-to-right in a single row, no padding, no spacing.
- Characters/monsters/boxes/FX: 32x32 per frame. Icons: 16x16 per frame.
- Characters face RIGHT. Feet touch the bottom pixel row (y = 31). Body centered on x = 16.
- File name = key + ".png", key format `<entity>_<anim>` (lowercase, underscores).
- Write `design/sprites/manifest.json` with exactly this shape:
{
  "version": 1,
  "sheets": {
    "hero_melee_walk": { "file": "hero_melee_walk.png", "frameWidth": 32, "frameHeight": 32, "frames": 6, "fps": 10, "loop": true },
    "hero_melee_attack": { "file": "hero_melee_attack.png", "frameWidth": 32, "frameHeight": 32, "frames": 6, "fps": 14, "loop": false, "events": { "impact": 3 } }
    // ...one entry per PNG. "events.impact" = 0-based frame index where the hit lands.
  }
}

## Asset list (priority A first; do B only after A is complete)
A1. Hero, melee class (sword + small shield) — keys: hero_melee_idle (4f, 6fps, loop), hero_melee_walk (6f, 10fps, loop), hero_melee_attack (6f, 14fps, impact 3), hero_melee_hurt (2f, 10fps), hero_melee_death (5f, 8fps)
A2. Monsters — slime, goblin, skeleton. For each: <m>_idle (4f, 6fps, loop), <m>_walk (6f, 10fps, loop), <m>_attack (4f, 10fps, impact 2), <m>_death (5f, 10fps). Monsters face LEFT (they walk toward the hero).
A3. Boxes (32x32): box_wood_idle (1f), box_wood_open (5f, 12fps — lid pops, light burst), box_gold_locked (4f, 6fps, loop — subtle glint, small padlock), box_gold_ready (4f, 8fps, loop — strong glow, no padlock), box_gold_open (6f, 12fps — bigger burst).
A4. Icons (16x16, 1 frame each, fps 0, loop false): icon_box_wood, icon_box_gold, icon_coin, icon_power, icon_stage, icon_expand, icon_close, icon_settings, icon_weapon, icon_armor, icon_ring. Item icons must be neutral (no rarity color) — the game draws a rarity-colored border around them.
A5. Effects: coin_spin (16x16, 6f, 12fps, loop), fx_hit (32x32, 4f, 16fps), fx_levelup (32x32, 6f, 12fps).
B1. Hero, mage class — same 5 animations, keys hero_mage_*.
B2. Hero, ranged class (bow) — same 5 animations, keys hero_ranged_*, plus fx_arrow (16x16, 2f, 12fps, loop).

## Method
If you cannot paint images directly, write a generator script `design/tools/build_sprites.mjs` (Node, no dependencies beyond `pngjs` if needed) or `design/tools/build_sprites.py` (Pillow) that draws every frame from hand-authored pixel maps using the palette from tokens.json, then run it. Commit the script so the sprites can be regenerated.

## Also deliver
- `design/sprites/preview.html` — plays every animation from manifest.json at 1x and 3x scale (CSS `image-rendering: pixelated`), each shown on a white, a dark (#1e1e1e) and a colorful gradient background. Plain HTML/JS, no external URLs.
- Add any third-party/AI usage to `design/CREDITS.md`.
- Write ONLY inside `design/`. Do not touch other folders.
- Reply with the list of keys you produced and anything you skipped.
```

---

## Prompt 3: หน้าตาแถบบน taskbar (mockup)

```text
Design the always-on "taskbar strip" UI of a desktop idle loot RPG as a static HTML/CSS mockup.

First read `design/tokens.json` and `design/STYLE_GUIDE.md`. Use sprites from `design/sprites/` (via manifest.json) if they exist; otherwise use simple colored placeholder boxes of the right size.

## What the strip is
- A frameless, fully transparent window, full screen width x 220px, sitting directly ABOVE the Windows taskbar.
- The bottom 64px is the "band": the playfield + HUD. The 156px above it is transparent overlay space used only for popups/toasts; it must stay empty (fully transparent, click-through) most of the time.
- Everything is click-through except small interactive targets (min 24x24px). Design so the user never accidentally clicks the game while working.
- Sprites are 32x32 drawn at 1:1. The hero stays roughly in the left third and walks/fights in place while monsters approach from the right.

## Band contents (left → right; you decide exact layout and justify it)
- HUD: stage ("ด่าน 12"), power ("พลัง 1,540"), gold ("12,345" + coin icon).
- Playfield: hero + 1–3 monsters, damage numbers, coins popping.
- Box tray: wooden box count ("×12"), gold boxes (each shows a countdown "12:34" or a READY state), an "เปิดทั้งหมด" (open all) button visible when wooden boxes ≥ 5.
- Expand button (opens the big window).

## Show these states, each as its own row in the page
1. Normal farming.
2. 12 wooden boxes + 1 gold box unlocking (12:34) + 1 gold box ready + open-all button.
3. Just opened a box: item popup in the overlay area — item icon with rarity border, name "ดาบเพลิง", rarity "ตำนาน", "พลัง +312", tag "สวมใส่แล้ว" (auto-equipped, shows ▲ +120 power).
4. Offline summary toast after launching the game: "ระหว่างที่คุณไม่อยู่ 2 ชม. 13 นาที" → "+48,210 ทอง", "กล่องไม้ ×34", "กล่องทอง ×1", button "เก็บทั้งหมด".
5. Hover state on a box and on the expand button.

## Readability test (required)
Render each state on three backdrops: a white spreadsheet-like area, a dark code-editor-like area, a colorful wallpaper — with a fake Windows 11 taskbar (48px) under the strip for context. Backdrops and taskbar are context only, NOT part of the game UI. Make two style variants and show both:
- Variant A: translucent plate behind the band (ui.bandBg).
- Variant B: no plate; readability from sprite outlines + text outline only.

## Format
- `design/mockups/strip.html` + `design/mockups/strip.css`. Plain HTML/CSS (tiny inline JS allowed only to animate sprites). No frameworks, no external URLs.
- Class names prefixed `tb-` (BEM-like), all colors/sizes from CSS variables that mirror tokens.json (name them `--tb-<token-path>`, e.g. `--tb-rarity-legendary`).
- Font: `font-family: GameFont, "Leelawadee UI", Tahoma, sans-serif;` (the real font file is added later by the developer).
- `design/mockups/NOTES.md`: which variant you recommend and why, exact pixel layout of the band (x positions/widths at 1920px and 1366px wide), and the z-order of overlay elements.
- Write ONLY inside `design/`.
```

---

## Prompt 4: หน้าตาหน้าต่างใหญ่ (mockup)

```text
Design the main window of a desktop idle loot RPG as a static HTML/CSS mockup. The player opens it from the taskbar strip; it holds every menu in ONE window (players of a similar game complained about many separate windows — avoid that).

First read `design/tokens.json`, `design/STYLE_GUIDE.md` and, if present, `design/mockups/NOTES.md` so this window matches the strip. Use icons/sprites from `design/sprites/` if present.

## Window
- 960x600px, frameless with a custom pixel-style title bar (title "ชื่อเกมชั่วคราว", buttons: ย่อกลับไปที่แถบ, ปิด). Mark the drag region with the class `tb-drag`.
- Left or top tab bar with these tabs (Thai labels): ฮีโร่, กระเป๋า, กล่อง, สำรวจ, ตั้งค่า.

## Tab contents (use realistic placeholder numbers, Thai copy)
1. ฮีโร่ — hero sprite large (3x), class "นักรบ", power, stage; 3 equipment slots (อาวุธ, เกราะ, เครื่องประดับ) with rarity borders; 4 skill slots ("ช่องสกิล", skills come from dropped gems — show 2 filled, 2 empty with hint "ได้หินสกิลจากกล่อง").
2. กระเป๋า — grid of item cells with rarity borders; sort (พลัง/ความหายาก/ใหม่สุด); filter by slot; "ขายอัตโนมัติ" toggles per rarity (ธรรมดา, ดี, หายาก); compare tooltip on hover showing ▲/▼ power vs equipped.
3. กล่อง — wooden box count + "เปิดทั้งหมด"; list of gold boxes with countdown or "เปิดได้แล้ว"; drop-rate disclosure link "อัตราการดรอป".
4. สำรวจ — minion expedition slots: 1 active (minion, destination "เหมืองแร่", 1:24:10 left, reward preview), 1 empty (choose 1/2/4/8 ชม.), 1 locked with label "แพ็กรายเดือน".
5. ตั้งค่า — when another app is fullscreen: (•) ซ่อนอัตโนมัติ ( ) อยู่บนสุดเสมอ; strip FPS 10/15; sprite scale 1x/2x; language ไทย/English; notifications toggles (กล่องทองพร้อม, ได้ของตำนาน, ทีมสำรวจกลับมา).

## Rarity names (use exactly): ธรรมดา, ดี, หายาก, มหากาพย์, ตำนาน

## Format
- `design/mockups/window.html` + `design/mockups/window.css`. Plain HTML/CSS; a tiny inline script to switch tabs is allowed. No frameworks, no external URLs.
- Class prefix `tb-`, colors/sizes via `--tb-*` CSS variables mirroring tokens.json, font `GameFont, "Leelawadee UI", Tahoma, sans-serif`.
- Every tab must fit 960x600 without page scrolling (inner lists may scroll).
- Write ONLY inside `design/`. Reply with a short summary and any open design questions.
```

---

## Prompt 5: ไอคอนแอป

```text
Create the application icon set for the desktop idle loot RPG whose art you already defined.

First read `design/tokens.json`, `design/STYLE_GUIDE.md` and look at `design/sprites/` so the icon matches the game.

## Concept
One instantly recognizable symbol that still reads at 16x16 in the Windows system tray: a small treasure box (gold box from the game) — optionally with the hero's sword or a tiny glow. No text, no letters. Must read on both light and dark taskbars (keep the 1px dark outline).

## Deliverables (write ONLY inside `design/icons/`)
- Pixel-perfect PNGs drawn per size (do NOT just downscale one image): `icon-16.png`, `icon-24.png`, `icon-32.png`, `icon-48.png`, `icon-64.png`, `icon-128.png`, `icon-256.png`. 16/24/32 must be hand-tuned pixel art; 128/256 may be a larger, more detailed pixel version.
- `app.ico` containing 16, 24, 32, 48, 64, 256.
- `tray-16.png` and `tray-32.png` (same symbol, tuned for the tray; transparent background).
- `preview.html` showing every size at 1x and 4x on a light (#f3f3f3) and a dark (#202020) taskbar strip. No external URLs.
- Extend your generator (`design/tools/`) so the icons can be regenerated, and note it in `design/CREDITS.md`.
- Reply with which sizes are hand-tuned.
```

---

## Prompt 6: ชุดภูมิภาค (มอนใหม่ บอส และพื้น)

```text
Extend the sprite set for an idle loot RPG with three regions. Follow `design/tokens.json`, `design/STYLE_GUIDE.md` and the exact sprite contract already used in `design/sprites/manifest.json` (horizontal strips, no padding, transparent, palette colors only, 1px dark outline, monsters face LEFT, feet on the bottom pixel row, `events.impact` = 0-based hit frame). ADD new entries to the existing manifest.json; do not rename or change existing keys or files.

## Regions (Thai name / key)
1. ทุ่งหญ้า / grassland — existing slime and goblin.
2. ป่ามืด / darkforest — new: wolf, spider.
3. สุสาน / crypt — existing skeleton, new: ghost.

## New monsters (32x32, same 4 animations as existing monsters)
wolf, spider, ghost — keys <m>_idle (4f, 6fps, loop), <m>_walk (6f, 10fps, loop), <m>_attack (4f, 10fps, impact 2), <m>_death (5f, 10fps). The ghost floats (feet row can be empty; keep its lowest pixel within the bottom 4 rows so it sits on the same baseline).

## Bosses (48x48 frames — they must fit a 64px-tall band: feet on the bottom row, nothing taller than 48px)
- boss_kingslime (grassland), boss_treant (darkforest), boss_lich (crypt)
- For each: <b>_idle (4f, 6fps, loop), <b>_walk (6f, 8fps, loop), <b>_attack (6f, 10fps, impact 3), <b>_death (8f, 10fps)
- Bosses should look clearly more important than normal monsters (silhouette, a crown/horns/aura) but stay inside the palette.

## Ground strips (one per region)
- ground_grassland, ground_darkforest, ground_crypt: 64x8 tiles (1 frame, fps 0) that repeat seamlessly left-right. They are drawn along the bottom of a dark (ink #171C2C, 94% opacity) band right under the sprites' feet, so keep them low-contrast and subtle — they must not compete with sprites or text.

## Also
- Region display names for the HUD: write `design/regions.json` = { "grassland": { "th": "ทุ่งหญ้า", "en": "Grassland", "monsters": ["slime","goblin"], "boss": "boss_kingslime", "ground": "ground_grassland" }, ... } for all three regions.
- Update `design/sprites/preview.html` and the atlas in `design/qa/` to include the new sheets.
- Regenerate via your generator script; note anything new in `design/CREDITS.md`.
- Write ONLY inside `design/`. Reply with the new keys.
```

---

## Prompt 7: ภาพจริงสำหรับ widget (ตัวละคร 48px, เอฟเฟกต์, ฉากหลังหลายชั้น, กรอบ UI) — ใช้ PixelLab

```text
The owner approved variant A of your action prototype (`design/prototypes/action/index.html?variant=A`) and the reference clips `20261013-1553-31.4581978.mp4` (character + skill look) and `20261013-1555-21.4804181.mp4` (small always-on-top widget UI) in the project root. Claude is now building the production widget in `client/`. Your job: the production art for it. You own all art. Use the PixelLab MCP server for base characters and animations (the owner will give you the PixelLab token), then clean up, add effects, and package everything to the contract below so the game loads it with no code changes.

Read first: `design/CLAUDE_HANDOFF_ACTION_PROTOTYPE.md` (your own notes), `design/tokens.json`, `design/STYLE_GUIDE.md`, `design/sprites/manifest.json`, `GAME_BRIEF.md` §7.1 and §9.

## Scene the art is drawn for
- Scene canvas 560x180 game pixels, shown at 2x on high-DPI screens (pixelated, no smoothing). Ground line (feet) at y=152; the bottom 28px is the ground strip.
- Camera follows the hero, who stands at ~29% from the left while walking right. Monsters come from the right, face LEFT. Heroes face RIGHT.
- Combat timing is fixed in code: slash = windup 35ms → lunge 55ms → hit stop 45ms → recover 105ms; skill = 70 / 65 / 60 / 145ms. The game picks frames by these times, so what matters is DISTINCT KEY POSES, not fps.

## Manifest contract (additive — add/replace entries in `design/sprites/manifest.json`, keep `"version": 1` fields)
Every sheet: horizontal strip, no padding, transparent, `frameWidth`/`frameHeight` per sheet, feet on the bottom pixel row, horizontally centered in the frame. Optional new fields the game reads:
- `"events": { "impact": <0-based frame where the blade/spell connects> }` — required for attack/skill sheets.
- `"anchor": { "x": <px from left>, "y": <px from top> }` — only if the feet are NOT bottom-center (e.g. FX). Default = bottom-center.
- `"offset": { "x": <px>, "y": <px> }` — FX only: where the anchor sits relative to the hero's feet (x positive = in front of the hero).

## A. Priority (deliver first, the widget is waiting on these)
1. Hero melee (นักรบ) — frames 64x64, character about 48px tall, same keys as today so the game swaps automatically:
   `hero_melee_idle` (4f loop), `hero_melee_walk` (6f loop), `hero_melee_attack` (6f: ready, wind-up, lunge, IMPACT, follow-through, recover; impact=3), `hero_melee_skill` (8f, the prototype's "สะบั้นแผ่นดิน" ground cleave; impact=3), `hero_melee_hurt` (2f), `hero_melee_death` (5f).
2. Monsters slime, goblin, skeleton re-drawn at frames 48x48 (32–40px tall), keys unchanged: `<m>_idle`, `<m>_walk`, `<m>_attack` (impact), `<m>_hurt` (2f, NEW — flinch/knock-back pose), `<m>_death`.
3. FX as SEPARATE sheets (never baked into character frames, never clipped by a 64px frame):
   `fx_slash` (crescent, ~96x64, 5–6f, impact frame), `fx_skill_melee` (shockwave + debris, ~160x96, 7–8f), `fx_hit` (spark burst 32x32, 4f), `fx_dust` (feet dust 32x16, 4f), `coin_spin` (keep). Give each `anchor` + `offset`.
4. Background for ป่ามืด / darkforest as parallax layers: `design/backgrounds/darkforest/` PNGs, each seamlessly tileable left-right (width a multiple of 32, ≥ 640px; height ≤ 180, transparent above its content), plus `design/backgrounds/backgrounds.json`:
   `{ "darkforest": { "th": "ป่ามืด", "sky": "#171C2C", "layers": [ { "file": "darkforest/far.png", "parallax": 0.11, "y": 0 }, ... nearest last, ground strip with "parallax": 1.0 ] } }`
   Match the prototype's mood (moon, two mountain layers, far trees, near trees + stone arches, ground) but at production detail. Keep contrast low behind the characters' height band so sprites always read.
5. Widget frame UI: `design/mockups/widget.html` + `design/mockups/widget.css` styling Claude's DOM (class names below; do not rename). Fantasy frame like the prototype (dark wood/brass, corner studs), title bar 32px, scene 560x180, action bar 46px, total width 568px incl. 4px borders. Thai text 12px. Popups (`.tw-popup`, rarity border via `--tw-tier`) float above the widget.
   Classes: `.tw-widget` (root), `.tw-titlebar` (drag handle) > `.tw-sigil`, `.tw-title`, `.tw-stage`; `.tw-scene` (canvas holder) > `.tw-scene-top`, `.tw-phase`; `.tw-actionbar` > `.tw-gold`, `.tw-box.tw-box-wood`, `.tw-box.tw-box-gold` (`.is-ready`), `.tw-openall`, `.tw-skill` (with `.tw-cooldown` bar), `.tw-expand`; `.tw-popups` > `.tw-popup`.

## B. After A is accepted
- Hero mage (นักเวท) and ranged (นักธนู): same key list, `hero_mage_skill` / `hero_ranged_skill` + `fx_skill_mage`, `fx_skill_ranged`, `fx_arrow` (projectile).
- Regions (this replaces the old Prompt 6 sizes): ทุ่งหญ้า/grassland (slime, goblin), ป่ามืด/darkforest (wolf, spider), สุสาน/crypt (skeleton, ghost) — new monsters at 48x48; bosses `boss_kingslime`, `boss_treant`, `boss_lich` at 96x96 frames (≤ 88px tall); background layers for grassland and crypt; `design/regions.json` = { key: { th, en, monsters[], boss, background } }.

## Rules
- PixelLab output is raw material: fix palette to tokens.json, keep a consistent 1px dark outline, remove AI artifacts (stray pixels, melted hands, inconsistent armor between frames), and make the key poses read at 1x.
- Record in `design/CREDITS.md` which files started from PixelLab (needed for Steam's AI disclosure) and which are hand/procedural.
- Do not edit `design/prototypes/` deliverables in place for production; production files live in `design/sprites/`, `design/backgrounds/`, `design/mockups/`.
- Update `design/sprites/preview.html` and `design/qa/` previews; extend `design/tools/verify_assets.py` for the new fields.
- Write ONLY inside `design/`. Reply with the new/changed keys and anything Claude must change in code.
```

---

## Prompt 8: ทำ sprite เองด้วย 3D → pixel (Blender) แก้ชุดไม่เป็นธรรมชาติ ท่าตีไม่แรง และมือถือดาบสลับ

> เขียนโดย Claude 14 ต.ค. 2026 หลังเจ้าของดู `design/prototypes/wardrobe/` แล้วยังไม่พอใจ และโควตา PixelLab หมด รอบนี้ **ห้ามเรียก PixelLab**

```text
The owner reviewed design/prototypes/wardrobe/ and is not satisfied. Do NOT call PixelLab this round (quota is spent). Build the sprites yourself with a 3D-to-pixel pipeline in Blender, the way Dead Cells did (3D models + skeleton rendered to pixel art so one change never means redrawing every frame). The game stays in Phaser/TypeScript; Blender is only an offline art tool. Do not use Unity.

Read first: GAME_BRIEF.md §5.3 and §9 (every equipment piece is a separate visible layer, transmog keeps stats), design/CLAUDE_HANDOFF_ACTION_PROTOTYPE.md, design/prototypes/wardrobe/NOTES.md, design/tokens.json, design/STYLE_GUIDE.md.

## Why the current wardrobe fails (owner feedback + Claude's diagnosis)
1. "Clothes don't look natural": pixellab-character.js pastes ONE static image per garment onto per-frame anchors and stretches/rotates it along limbs (segment()). No shipped game does this; rotated/stretched pixel textures always look wrong.
2. "Attack doesn't feel strong / holds the sword in the right hand but punches with the left": the PixelLab attack clips are unarmed punches; the sword is attached afterwards to the other hand. In attack frames 4–5 the front arm punches forward while the sword trails behind; in slam 3–5 the re-posed arm is a pasted skin segment and the blade crosses the face.
Root cause for both: weapon and garments were added after the motion instead of being part of it.

## How games actually do layered equipment (use these as the rules)
- Every garment is its own per-frame sheet with the SAME frame layout as the body, drawn/rendered as if worn on the bare body; layers stack in a fixed draw order (Universal LPC spritesheet, Terraria armor). Draw order can differ per frame for items that pass in front of and behind limbs (capes, far-side arm).
- The weapon belongs to the animation: the swing is authored around the weapon arc, gripped by the same hand in every frame.
- A 3D pipeline gives all of that for free: equipment meshes are parented to bones, so every new item reuses every animation.

## Pipeline to build (scripted, reproducible, no GUI steps)
1. Blender 5.2.2 LTS is installed at `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe` (installed by Claude 14 Oct 2026; headless scripting verified). Run it headless: `"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b <file.blend> -P <script.py>` (or `--factory-startup --python <script.py>` with no .blend). Use the Blender 5.x Python API; render engine BLENDER_EEVEE or BLENDER_WORKBENCH.
2. Source models: KayKit Character Pack: Adventurers + KayKit Character Animations (CC0, rigged, chibi proportions, weapon and accessory meshes). Alternatively Quaternius Modular Character Outfits (check the licence file in the download; QAL allows commercial games, forbids redistributing the raw assets). Mixamo only if the owner downloads it (needs the owner's Adobe login). Record exact source URL + licence of every asset in design/CREDITS.md. These are not AI-generated, so state that (it matters for Steam's AI disclosure).
3. Camera: orthographic, true side view, character facing RIGHT, fixed ortho scale so the character is ~48–54 px tall inside a 64×64 frame (big weapons may need a 96×64 or 96×96 frame — choose and document). Feet on row 63 in every frame. Same camera for every pass.
4. Pixel look: render at the TARGET resolution with anti-aliasing off (filter size 0, no motion blur), toon shading (Shader to RGB → Color Ramp, Constant, 3–4 bands, one fixed key light from upper-left/front), then in Python: quantize each material to a ramp from design/tokens.json, add a 1 px dark outline on the outer silhouette, remove isolated pixels. Do not downscale a high-res render (that makes mush).
5. Layers: render per frame (a) base body (bare/underwear), (b) each equipment piece separately with the body set as holdout so parts behind the body are cut correctly, (c) a "hides body" mask per piece (body pixels covered by that piece, e.g. feet under boots), (d) the full outfit as a reference composite. Prove that compositing (a)+(b) in the documented draw order equals (d) pixel-for-pixel or report the differing pixels.
6. Anchors: export per-frame 2D pixel positions of bones (right hand, left hand, head, chest, hip, both feet, weapon tip) projected through the camera. The game uses them for FX and hit sparks.
7. Weapon: one-handed sword parented to the RIGHT hand bone in every clip. Facing right, make the weapon arm the readable near-side arm (mirror the rig if needed); never switch hands inside a clip.

## Slots and items (first pass, prove the method — not volume)
hat, chest (shirt/armour), legs, boots, wrist, weapon (sword) + base body. 2 looks per slot minimum (e.g. cloth hood / iron helm; tunic / plate) so the owner can see a real swap. Palette-swapped variants count as extra items for free — show one recolor.

## Animations (frame times in ms are a starting point; tune by eye)
- idle 4 frames loop
- walk 8 frames loop (Pixelblog 25 / 60: legs first, then arms, head bob)
- attack (fast one-hand slash, use a KayKit 1H melee clip): ~6–7 frames: ready 60 · anticipation 90 (hold) · smear/swing 30 · IMPACT 40 (+ game hit stop) · follow-through 80 · recover 100
- heavy slash (overhead chop): ~8–9 frames with a longer anticipation hold (~150–200 ms total), 1-frame smear, impact, long follow-through. Exaggerate key poses beyond the raw clip (rotate spine/shoulder/hips further, lower the stance on impact, lean forward) — Pixelblog 9: realistic poses look stiff in pixels.
- hurt 2 frames, death 5–6 frames (can wait for a second pass)
Choose frames by key pose, not by uniform sampling. Put the slash arc / smear in a SEPARATE fx sheet (never baked into body frames) with its own anchor + impact frame, so it can overreach the 64 px frame.
Also write design/ANIMATION_GUIDE.md: our rules (frame counts, key poses, timing, draw order per slot, anchor list, hand rule) from Pixelblog 9, 25, 58, 60 (principles only, no copied art).

## Deliverables (write ONLY inside design/)
- design/3d/ : source .blend + scripts (design/tools/render_sprites3d.py does everything from a clean checkout in one command), downloaded asset packs with their licence files.
- design/sprites3d/adventurer/ : body_<anim>.png, <slot>_<item>_<anim>.png, mask_<slot>_<item>_<anim>.png, fx_<anim>.png, ref_<anim>.png, and sprites3d.json = { frameWidth, frameHeight, animations: { <anim>: { frames, frameMs[], impact, loop } }, layers: { <slot>: { <item>: { files, hidesBody } } }, drawOrder: { default: [...], perFrame: {...} }, anchors: { <anim>: [ { rightHand:[x,y], leftHand, head, chest, hip, frontFoot, backFoot, weaponTip } ] } }.
- Update design/prototypes/wardrobe/: add an art-source switch "PixelLab (เดิม) | 3D render (ใหม่)" so the owner can compare in the same page with the same buttons (J/K/L, walk, frame scrub, slot changes). The 3D source must composite only rendered layers — no stretching, rotating or re-posing of pixels in the browser.
- design/qa/sprites3d.json + contact sheets: per frame, composite == reference check, feet row, weapon always in right hand (anchor distance to grip ≤ 1 px), no layer touching frame edge, colors per item.
- Short NOTES.md section: what looks better/worse than PixelLab, render time, how to add a new item (target: one new mesh + one command).

## Rules
- Do not touch client/, server/, design/sprites/manifest.json or sync-design.mjs.
- No PixelLab calls, no API keys in files.
- If the 3D look clearly cannot reach the owner's bar, say so plainly with screenshots instead of hacking pixels in code.
- Reply with: screenshots of idle/walk/attack/heavy with 2 outfits, what you could not do, and the list of files.
```

---

## Prompt 8.1 (ต่อจาก Prompt 8): ต้องเป็นตัวละครเดิมของเจ้าของ ไม่ใช่ KayKit Rogue

> เขียนโดย Claude 14 ต.ค. 2026 หลังเจ้าของเห็นภาพเรนเดอร์แรกแล้วถามว่า "ไม่เปลี่ยนคาแรคเตอร์ไม่ได้หรอ"

```text
Addendum to Prompt 8. Everything in Prompt 8 still applies; this changes WHO the character is.

The owner's character is the teal-haired chibi in design/pixellab/chibi-modular/reference-native.png (dressed) and design/pixellab/chibi-modular/base/candidate-01.png (bare base, 64x64). The current render shows KayKit Rogue's head, hair and face texture, so it reads as a different person. KayKit is ONLY the skeleton, the animation clips and the base body/clothing-shell meshes. Never show KayKit's head, hair, face or texture.

Identity lives in the head (big teal hair mass, side-swept fringe over the face, ear, eye, blush), which is a rigid part in a side view. So:

## A. Recommended: 2D pixel head on the 3D body (hybrid, like MapleStory-style rigid head sprites)
- Cut the head (hair + face + ear, down to the neck seam) from a cleaned copy of base/candidate-01.png. Keep the original file untouched.
- Every frame, place the head at the projected head-bone anchor from your render. Snap to whole pixels.
- Head rotation: never rotate pixels at runtime. Pick from pre-made head variants by head-bone angle bucket: neutral, tilted forward ~10° (attack windup/impact), tilted back ~10° (heavy windup), hurt. Make the variants by hand-editing pixels from the same head, not by rotating it.
- Hats are 2D layers drawn per head variant (so a hood/helm fits the hair). Body, chest, legs, boots, wrist and weapon stay 3D-rendered layers.
- Hide KayKit's head mesh in every pass; render a neck stub that the 2D head overlaps.

## B. Fallback, only if A's seam looks wrong: model a simple low-poly head and hair in Blender (6–10 stylized hair clumps) matching candidate-01's silhouette and colors, then render it like the body. Show A and B side by side and let the owner choose.

## Make the 3D body read as the same character
- Proportions: scale KayKit bones so the body silhouette matches candidate-01 at 64x64: shoulder width, arm length, short legs, small hands, foot size, feet on row 63. Bare arms must be visible at the sides (like the base), not hidden.
- Palette: sample ramps from reference-native.png (teal hair, skin + blush, olive tunic, cream scarf, red sash, brass, steel blade, dark brown boots) and quantize every 3D layer to them. The outline is the reference's 1 px very dark brown, not pure black, on the outer silhouette, the same as the head.
- Shading: same light direction as the PixelLab art (lit from upper-left/front, 3 bands max), so the 3D body and the 2D head look painted together.

## First outfit = the reference outfit exactly (proof of identity)
cream scarf/collar, olive tunic, red sash, brass bracer on the front wrist, dark shorts, brown boots, sword with brass guard and cream/steel blade in the RIGHT hand. At idle the sword points down-forward at about 30° like the reference — never sticking straight out sideways from the hip.

## Acceptance
- A contact sheet: reference-native.png and your idle frame at the same scale side by side, then walk, attack and heavy-slash frames with the same outfit. The owner must recognize the same character before you build more items.
- Then a second outfit to prove swapping (e.g. iron helm as a 2D hat layer + plate chest + greaves).
- Keep all QA from Prompt 8 (layer composite == reference composite for the 3D layers, sword in right hand every frame, feet row, no edge touches).
- Write ONLY inside design/. No PixelLab calls.
```
