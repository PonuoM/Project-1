# weapons-g1 — 16 weapon sprites (Gemini in Google Antigravity, 14 Oct 2026)

Prompt: design/GEMINI_PROMPTS.md "Prompt G1". Gemini (Antigravity, image-generator sub-agent) produced three
sheets (v1–v3) but did not save them into the repo; Claude copied them from Antigravity's artifact folder
`C:\Users\user\.gemini\antigravity\brain\8f155921-87b1-4f1d-b171-7415d5c96cec\` (sheet_raw*.jpg). AI-generated:
record provenance when shipping (Steam AI disclosure).

How it followed the brief:
- OK: 4x4 grid on chroma green, the 16 weapons in the requested order, steel greys + brown wood, no outfit colours.
- Not followed: 1024x1024 JPEG instead of a 2048 PNG; weapons drawn diagonally (up-right) instead of horizontal;
  grip not at a fixed cell position; sizes larger than asked (art pixel ~8.2 px; dagger 18, swords 26-37 art px).

Converted by `python -I design/tools/weapons_from_sheet.py sheet-raw-v3.jpg native --names ... --period 8.2`
→ `native/<name>.png|json` (grid rebuilt, shared 23-colour palette, green JPEG fringe removed, grip + blade
angle per weapon, same format as weapon_layer.py). `native/preview.png` marks each grip with a red circle.
Demo: the weapon-less PixelLab chop body with six of them (design/pixellab/chibi-motion/g1-chop-*/), in the viewer
design/prototypes/chibi-motion/.

Next prompt fixes: ask for PNG, ask Gemini to write the file into the repo path itself, and accept the diagonal
pose (the tools handle any angle) — only the handle end must be the lower-left end.
