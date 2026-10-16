# combo-rush-g1 — High-Speed Stickman/Sakuga Sword Combo Demo (14 Oct 2026)

## Agent & Model
- Agent: Gemini (Google Antigravity)
- Model: Gemini 4 Argon (Medium)
- Paid generation services used: **0 gen** (assembled 100% programmatically from existing `design/pixellab/chibi-motion/body-slash/`, `body-chop/` and `design/concepts/weapons-g1b/native/long-sword.png`).

## Reference & Brief
- User reference video: `Screen_Recording_20261014_180756_Facebook.mp4` (Stickman high-speed combo with instant dash snap, teleport cross-up behind enemy, high-speed Ora-Ora flurry rush, and heavy silence-to-impact finisher that launches the target across the screen).
- Goal: Prove that the existing Chibi character (`hero-ref-64.png` frames) + modular weapon layer (`long-sword.png`) can achieve the same blistering speed, impact weight, and visual satisfaction without generating new AI frames.

## Combo Structure (31 Frames Total)
1. **Phase 0 — Coil & Silence (`frame-00` to `frame-02`, 255ms):**
   - Hero sinks back and holds the coiled stance (`110ms`) before the strike.
2. **Phase 1 — 1-Frame Blitz Rising Slash (`frame-03` to `frame-05`, 25ms snap + 90ms hit-stop):**
   - Zero in-between frames: hero snaps 41 art pixels forward in `25ms` leaving cyan/white silhouettes, with a wide crescent slash smear (`-45°` to `160°`), impact frame background flash (inverted Sakuga frame), screen shake, and enemy squash/flash.
3. **Phase 2 — Vanish Cross-Up Behind Target (`frame-06` to `frame-08`, 30ms vanish + 25ms slash):**
   - Hero teleports behind the enemy (`x=136`, flipped horizontally) leaving trailing afterimages and cleaves backward across the enemy.
4. **Phase 3 — High-Speed 12-Hit Sword Barrage (`frame-10` to `frame-21`, 12 × 30ms = 360ms):**
   - Re-enters in front and alternates `body-slash` frames 7 & 8 every `30ms` while `rotsprite` renders the main blade + 2 semi-transparent ghost blades simultaneously across 12 angles (`-45°` to `+42°`) with horizontal speed lines and continuous target hit-sparks.
5. **Phase 4 — Silence Coil + God-Speed Overhead Finisher (`frame-22` to `frame-30`):**
   - Sudden `125ms` silence hold in overhead coil (`body-chop` frame 4) → `25ms` 1-frame downward cleave (`frame-24`) with impact inversion flash, `95ms` heavy hit-stop (`frame-25`), launching the enemy spinning off-screen (`frame-26` to `frame-29`).

## Saved Files in `design/concepts/combo-rush-g1/`
- `combo-rush-preview.gif` — 640×384 px animated GIF (31 frames, 266,831 bytes)
- `combo-rush-preview.webp` — 640×384 px lossless animated WebP (31 frames)
- `combo-keyframes-sheet.png` — 1280×384 px 8-panel key-moment breakdown
- `viewer.html` — standalone pixel-art preview page
- `frame-00.png` .. `frame-30.png` — 640×384 px individual frames

