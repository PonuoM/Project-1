# weapons-g1b — 16 weapon sprites redo (Gemini in Google Antigravity, 14 Oct 2026)

## Model Used
- Calling agent: Gemini 4 Argon (Medium)
- Image generation subagent: `image-generator` (inheriting parent model configuration; outputs 1024×1024 raw `.jpg` files in the Antigravity artifact folder, converted to lossless `.png` in `design/concepts/weapons-g1b/`).

## Prompts Given to the Image Tool

### Attempt 1 (`sheet-v1.png`)
```text
Generate a 1024x1024 pixel art weapon sprite sheet in a strict 4x4 grid (16 invisible cells, each 256x256 image pixels = 32x32 art pixels, where 1 art pixel = 8x8 image pixels).

CRITICAL STYLE & BACKGROUND RULES:
- Plain flat solid chroma-key green background (#00B140) EVERYWHERE. No grid lines, no cell borders, no shadows, no gradients, no text, no numbers, no labels.
- Chunky pixel art where 1 art pixel = an 8x8 block of image pixels.
- Crisp 1-art-pixel dark warm brown/black outline (#2e1816) around every weapon.
- Flat 3-shade colour ramps (cool steel greys, warm bronze/gold trim, rich dark oak/walnut wood browns, icy cyan crystal for the wand). No anti-aliasing, no glow, no blur.
- Do NOT use ivory, moss-green, terracotta, or violet (#7a3cff).
- Every weapon is posed on the 45-degree diagonal with its handle/pommel at the LOWER-LEFT and its tip/head pointing toward the UPPER-RIGHT.

CRITICAL SCALE & LENGTH RULES (DO NOT OVERSIZE! Leave plenty of empty #00B140 green margin inside each 256x256 cell!):
Each cell is 32x32 art pixels (diagonal ~45 art pixels). Measure the total diagonal length from handle end to tip in art pixels:
Row 1 (top, left to right):
Cell 1: dagger — tiny, only 9 art pixels long (~20% of cell diagonal, very large green margin around it)
Cell 2: short sword — small, 14 art pixels long (~31% of cell diagonal, less than half the cell width)
Cell 3: long sword — medium, 20 art pixels long (~44% of cell diagonal)
Cell 4: greatsword — large broadsword, 26 art pixels long (~58% of cell diagonal)
Row 2: Cell 5: curved sabre (16), Cell 6: katana (20), Cell 7: hand axe (13), Cell 8: battle axe (20)
Row 3: Cell 9: mace (14), Cell 10: war hammer (20), Cell 11: spear (30), Cell 12: halberd (30)
Row 4: Cell 13: wooden staff (26), Cell 14: crystal wand (11), Cell 15: scythe (26), Cell 16: club (15)
```

### Attempt 2 (`sheet-v2.png`)
Follow-up prompt to `image-generator` referencing `sheet-v1` and specifying exact bounding-box dimensions in image pixels (`0.707 × lengthPx × 8`) so the weapons stay well inside their 256×256 cells:
- Cell 1 (`dagger`, 9 art px): ~50×50 image px
- Cell 2 (`short sword`, 14 art px): ~80×80 image px
- Cell 3 (`long sword`, 20 art px): ~112×112 image px
- Cell 4 (`greatsword`, 26 art px): ~148×148 image px
- Cell 5 (`curved sabre`, 16 art px): ~90×90 image px
- Cell 6 (`katana`, 20 art px): ~112×112 image px
- Cell 7 (`hand axe`, 13 art px): ~74×74 image px
- Cell 8 (`battle axe`, 20 art px): ~112×112 image px
- Cell 9 (`mace`, 14 art px): ~80×80 image px
- Cell 10 (`war hammer`, 20 art px): ~112×112 image px
- Cell 11 (`spear`, 30 art px): ~168×168 image px
- Cell 12 (`halberd`, 30 art px): ~168×168 image px
- Cell 13 (`wooden staff`, 26 art px): ~148×148 image px
- Cell 14 (`crystal wand`, 11 art px): ~62×62 image px
- Cell 15 (`scythe`, 26 art px): ~148×148 image px
- Cell 16 (`club`, 15 art px): ~85×85 image px

### Attempt 3 (`sheet-v3.png`)
Follow-up prompt to `image-generator` referencing `sheet-v2` to widen the relative size contrast between the smallest items (`crystal wand`, `dagger`) and the longest weapons (`greatsword`, `spear`, `halberd`).

## Recommendation
- **Recommended sheet overall:** **`sheet-v2.png`** (with **`sheet-v3.png`** for `greatsword` if a slightly larger 29.7-art-px greatsword is desired).
- Why `sheet-v2.png` is recommended:
  - In `sheet-v2.png`, every single weapon sits cleanly inside a 18×18 art-pixel (~146×146 image-pixel) footprint inside its 32×32 art-pixel (256×256 image-pixel) cell with generous `#00B140` margin on all four sides.
  - Running `python -I design/tools/weapons_from_sheet.py design/concepts/weapons-g1b/sheet-v2.png ... --period 8.2` extracts all 16 weapons cleanly (no broken shafts, 26-colour shared palette) with measured diagonal lengths (`L` in `weapons_from_sheet.py`):
    - `dagger`: **11.3 art px** (target 9)
    - `short-sword`: **16.3 art px** (target 14)
    - `long-sword`: **21.2 art px** (target 20)
    - `greatsword`: **23.3 art px** (target 26; in `sheet-v3.png` it is **29.7 art px**)
    - `sabre`: **19.2 art px** (target 16)
    - `katana`: **21.9 art px** (target 20)
    - `hand-axe`: **16.9 art px** (target 13)
    - `battle-axe`: **17.7 art px** (target 20)
    - `mace`: **20.5 art px** (target 14)
    - `war-hammer`: **18.4 art px** (target 20)
    - `spear`: **21.2 art px** in `sheet-v2.png` / **38.2 art px** in `sheet-v3.png` (target 30)
    - `halberd`: **22.6 art px** in `sheet-v2.png` / **38.9 art px** in `sheet-v3.png` (target 30)
    - `staff`: **21.2 art px** (target 26)
    - `wand`: **21.9 art px** in `sheet-v2.png` (in `sheet-v3.png` the wand is **12.8 art px** total, though its wooden shaft is only 1 art px thick so `weapons_from_sheet.py` splits the crystal head if despeckled at `--period 8.2`)
    - `scythe`: **18.0 art px** (target 26)
    - `club`: **20.5 art px** (target 15)

## Points of the Brief Not Followed Exactly
1. **Underlying tool format (JPEG → PNG conversion):** The `image-generator` subagent outputs `.jpg` files in the Antigravity artifact folder (`weapon_spritesheet_*.jpg`). Per `GEMINI.md`, each attempt was immediately converted and saved as lossless `.png` (`sheet-v1.png`, `sheet-v2.png`, `sheet-v3.png`) in `design/concepts/weapons-g1b/`. Because the source was JPEG, mild chroma-key edge ringing exists around outlines (which `design/tools/weapons_from_sheet.py` automatically strips via its JPEG-safe median sampler and green-fringe filter).
2. **Exact per-weapon pixel lengths vs. AI image generation granularity:** While `sheet-v2.png` eliminated the 1.85× global oversize from `sheet-v1.png` (bringing the average scale from 1.86× down to ~1.0–1.2× and putting `long sword`, `katana`, `greatsword`, `battle axe`, and `war hammer` within 1–2.7 art px of their exact targets), the image model still compresses the dynamic range between the shortest one-handed blunt/magic weapons (`mace`, `club`, `wand` in `v2`) and the longest polearms (`spear`, `halberd`, `staff`, `scythe`). In `sheet-v3.png`, `wand` was shrunk to ~12.8 art px (target 11) and `greatsword` increased to ~29.7 art px (target 26), while `spear` and `halberd` jumped back to ~38 art px.

## Saved Files in `design/concepts/weapons-g1b/`
- `design/concepts/weapons-g1b/sheet-v1.png` — 1024×1024 px (943,110 bytes)
- `design/concepts/weapons-g1b/sheet-v2.png` — 1024×1024 px (766,942 bytes) **(Recommended)**
- `design/concepts/weapons-g1b/sheet-v3.png` — 1024×1024 px (707,342 bytes)
- `design/concepts/weapons-g1b/weapons.json` — 863 bytes
- `design/concepts/weapons-g1b/notes.md` — 7,096 bytes
