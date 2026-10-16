# G5 — Codex export handoff, 2026-10-14

Agent: Codex (GPT-6 assistant). Image service: built-in image_gen; underlying image model not exposed. No PixelLab, MiniMax or paid API CLI was run.

Status: all nine roster concepts saved. Exact anatomical tracing and production palette locking remain outstanding; these are reviewable concepts, not validated production sprites.

Owner rejected melee-1-v1 for three-head proportions. The revised generation used both local references: design/pixellab/chibi-motion/hero-ref-64.png and design/concepts/base-claude-v1/base-body-64-x8-green.png. The requested redraw is preserved in the parent directory as melee-1-v2.png; this isolated folder contains its green-normalized export under the same name.

Every image in this Codex run, including mage-2..3 and archer-1..3, was generated using the built-in image_gen tool, as PNG 1254x1254. This differs from the concurrent Gemini notes describing their separate JPEG attempts. Codex raw outputs are the parent folder's *-raw-v1.png and melee-1-raw-v2.png. Rejected melee-1-raw-v1.png and melee-1-v1.png remain there. No original files were deleted.

## Exact prompts

prompts-v2.json copied into this folder contains the nine exact revised prompts. Both references were passed to every revised generation. Parent prompts-v1.json records the rejected direction.

## Recommended Codex files

- melee-1-v2.png — 512x512
- melee-2-v1.png — 512x512
- melee-3-v1.png — 512x512
- mage-1-v1.png — 512x512
- mage-2-v1.png — 512x512
- mage-3-v1.png — 512x512
- archer-1-v1.png — 512x512
- archer-2-v1.png — 512x512
- archer-3-v1.png — 512x512
- lineup-v1.png — 1536x1536

All exports use nearest-neighbour 64x64 to 512x512: exact aligned 8x8 blocks. Chroma background pixels are normalized to #00B140. Every figure has its lowest foreground pixel on native row62. Only archer-1 required a +1 native-pixel vertical shift. Side margins are at least3 native pixels. Row62 leaves one blank bottom row; the owner's explicit template ground line takes precedence over the contradictory 2-pixel bottom-margin wording.

Recommended favourites: melee-1 / Mara; mage-1 / Pipra; archer-2 / Ilen.

## Limitations and what remains

- The model follows the giant-head / short-limb template visually, but does not preserve all anatomical anchors exactly pixel for pixel. Hair volume, eye, hands and feet vary by roughly a few native pixels. No claim of exact template tracing.
- Source images contain many intermediate shades. Export makes a strict grid and background; it does not enforce three shades per material or the exact #2e1816 outline. Integrator must lock material palettes.
- Orrik's sandstone head currently reads like golden human hair. Sella has humanoid facial features with hare ears. Stronger species anatomy may be needed.
- Weapon scales are small, but exact target lengths were not individually verified. Bow/string, crossbow mechanism, book tabs, sling cords and the long staff need clearer native-pixel definitions before animation. The source staff reads too short.
- These exports deliberately preserve generated art without restoring protected body pixels. Owner/integrator review determines accepted three; then refine exact body anchors and weapons.
- Concurrent Gemini work appeared in the same parent folder during this run. Its existing characters.md and notes.md were preserved. This folder isolates Codex outputs to avoid confusing authorship and version names.
- characters.md here is a copy of Gemini's concurrent world/roster document, with a Codex selection/caveat appended. It contains the world, nine identities, colour ramps and 27 move ideas.
- All source image attempts retained as PNG in parent folder, no JPEG conversion for Codex outputs.

Resume using this folder's lineup-v1.png, prompts-v2.json, verification-v1.json and export.py, with original raw images one directory up. Only write new versions.

## Export verification

PNG dimensions, foreground bounding boxes and row62 are recorded in verification-v1.json. Images were visually inspected together in the saved lineup. export.py builds this isolated folder from the PNG sources; it refuses to overwrite its outputs.
