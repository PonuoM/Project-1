# characters-g5 — 9 Playable Character Roster Concepts (14 Oct 2026)

## Agents & Models Used
- **Started by:** Codex (GPT-6 / built-in image generation) — wrote `prompts-v1.json`, `prompts-v2.json`, `export-v1.py`, and generated the first 4 characters (`melee-1-v1.png`, `melee-1-v2.png`, `melee-2-v1.png`, `melee-3-v1.png`, `mage-1-v1.png` + their `*-raw-v*.png` files).
- **Resumed & completed by:** Gemini (Google Antigravity — **Gemini 4 Argon (Medium)**) — generated the remaining 5 characters (`mage-2`, `mage-3`, `archer-1`, `archer-2`, `archer-3`) using the exact prompts in `prompts-v2.json` and the same `64x64 -> 512x512` `Image.Resampling.NEAREST` export pipeline (`export-v1.py`), assembled `lineup-v1.png` (`1536×1536`), and wrote `characters.md` and `notes.md`.

## Exact Prompts Used
All 9 prompts are stored verbatim in `design/concepts/characters-g5/prompts-v2.json`. Each prompt edited the 512×512 grey-bodysuit chibi template (`design/concepts/base-claude-v1/base-body-64-x8-green.png`) with `design/pixellab/chibi-motion/hero-ref-64.png` as the style and low-weapon-pose reference:
1. **`melee-1` (Mara Bellwake — Human Sky-Port Swordswoman):** Auburn bob, navy fitted brigandine + cream sleeves + swept-back navy shoulder cape, ~14 art px cool steel broadsword held low-forward.
2. **`melee-2` (Orrik Kilnstep — Living Sandstone Folk Mason):** Rounded brick-like sandstone head, ochre arch shoulder yoke, amber tunic + rust apron, ~18 art px square iron masonry hammer held low-forward.
3. **`melee-3` (Sella Reedcrest — Hare Beast-Folk Courier):** Long backward-folded cream rabbit ears, copper bob, wine-red split coat, ~26 art px leaf-bladed spear held low-forward.
4. **`mage-1` (Pipra Tideglass — Reef-Coral Sprite-Folk):** Salmon-pink hair with branching coral crown, petrol-teal scalloped poncho, ~12 art px circular brass astrolabe ring-wand with solid cyan glass centre.
5. **`mage-2` (Vessa Foldlight — Human Stage-Troupe Dramaturge):** Warm brown skin, white asymmetrical fan-shaped bob, mulberry-purple theatre coat with marigold trim, ~12 art px open burgundy spellbook with 3 paper tabs held low-forward.
6. **`mage-3` (Noll Brackenbell — Plant-and-Stone Folk Bell-Keeper):** Pale weathered-grey stone face with clear visible eye, rounded ochre wooden mushroom-like canopy with two hanging seed pods, russet bark tunic, moss-olive root boots, ~26 art px birch staff with closed gold seed lantern.
7. **`archer-1` (Tavi Saffronwind — Desert Fox Beast-Folk Scout):** Sandy furry head with triangular ears, curled fluffy fox tail behind body, saffron-yellow hood-down jacket, ~20 art px dark wood recurve bow held low-forward.
8. **`archer-2` (Ilen Rivetwing — Human Airship Arbalestier):** Black angular bob hair, cool cyan quilted coat, turquoise scarf with two backward ribbons, ~14 art px brass-and-steel hand crossbow held low-forward at waist.
9. **`archer-3` (Bramble Kettlehop — Dormouse Beast-Folk Warden):** Tan furry head with round ears and cream cheeks, apple-red padded vest over cream shirt, round brown leather satchel behind body, ~10 art px braided cord sling with river stone in pouch held low-forward.

## Recommended Versions (Used in `lineup-v1.png`)
- **Row 1 (Melee):** `melee-1-v2.png` · `melee-2-v1.png` · `melee-3-v1.png`
- **Row 2 (Mage):** `mage-1-v1.png` · `mage-2-v2.png` · `mage-3-v2.png`
- **Row 3 (Archer):** `archer-1-v3.png` · `archer-2-v1.png` · `archer-3-v3.png`

### Favourite per Class
- **Melee:** `melee-3-v1.png` (Sella Reedcrest) — strongest silhouette hook (swept-back rabbit ears + forward leaf spear) and crisp colour contrast.
- **Mage:** `mage-1-v1.png` (Pipra Tideglass) — unmistakable coral-branch crown and circular astrolabe wand silhouette.
- **Archer:** `archer-1-v3.png` (Tavi Saffronwind) — balanced fox-tail + recurve-bow profile on the exact template stance.

## Points of the Brief Not Followed Exactly / Caveats for Claude
1. **JPEG-to-PNG conversion on `mage-2..3` and `archer-1..3`:** Antigravity's `image-generator` outputs 1024×1024 `.jpg` files in the artifact folder; each attempt was snapped to `64×64` and scaled `8×` to `512×512` lossless `.png` using `Image.Resampling.NEAREST` (matching `export-v1.py`). Mild green JPEG fringe exists on a few border blocks around outlines, which Claude's chroma-key / palette-lock cleanup script removes cleanly.
2. **Slight head-top crop on `archer-3-v1` / `v2` fixed in `v3`:** Earlier attempts of `archer-3` (`Bramble Kettlehop`) had a slightly wider head; `archer-3-v3.png` keeps the round dormouse ears inside the 64×64 frame with feet on row 62, though the top of the left ear is 1 art px from the top edge instead of 2 art px.

## Saved Files in `design/concepts/characters-g5/`
- `lineup-v1.png` — `1536×1536 px` (`101,462 bytes`) — 3×3 comparison grid of all 9 recommended sprites
- `melee-1-v1.png` — `512×512 px` (`13,086 bytes`)
- `melee-1-v2.png` — `512×512 px` (`12,106 bytes`) **(Recommended `melee-1`)**
- `melee-2-v1.png` — `512×512 px` (`12,794 bytes`) **(Recommended `melee-2`)**
- `melee-3-v1.png` — `512×512 px` (`13,754 bytes`) **(Recommended `melee-3`)**
- `mage-1-v1.png` — `512×512 px` (`13,376 bytes`) **(Recommended `mage-1`)**
- `mage-2-v1.png` — `512×512 px` (`11,266 bytes`)
- `mage-2-v2.png` — `512×512 px` (`10,510 bytes`) **(Recommended `mage-2`)**
- `mage-3-v1.png` — `512×512 px` (`11,391 bytes`)
- `mage-3-v2.png` — `512×512 px` (`11,007 bytes`) **(Recommended `mage-3`)**
- `mage-3-v3.png` — `512×512 px` (`11,813 bytes`)
- `archer-1-v1.png` — `512×512 px` (`12,546 bytes`)
- `archer-1-v2.png` — `512×512 px` (`11,534 bytes`)
- `archer-1-v3.png` — `512×512 px` (`12,069 bytes`) **(Recommended `archer-1`)**
- `archer-2-v1.png` — `512×512 px` (`11,796 bytes`) **(Recommended `archer-2`)**
- `archer-3-v1.png` — `512×512 px` (`11,558 bytes`)
- `archer-3-v2.png` — `512×512 px` (`12,311 bytes`)
- `archer-3-v3.png` — `512×512 px` (`12,156 bytes`) **(Recommended `archer-3`)**
- `characters.md` — `11,261 bytes`
- `notes.md` — this file
- Plus Codex's initial raw files (`melee-1-raw-v1.png`, `melee-1-raw-v2.png`, `melee-2-raw-v1.png`, `melee-3-raw-v1.png`, `mage-1-raw-v1.png`), `prompts-v1.json`, `prompts-v2.json`, `export-v1.py`.



## Codex concurrent run clarification — 2026-10-14

Codex also generated all nine revised PNG concepts with built-in image_gen in this live turn. Their PNG source files are *-raw-v1.png and melee-1-raw-v2.png. The isolated Codex comparison is codex-export-v1/lineup-v1.png; see codex-export-v1/notes.md for exact authorship, versions, prompts and outstanding fidelity limitations. Existing Gemini text and versions are preserved.
