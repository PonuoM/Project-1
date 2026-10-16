# G7 — Mara’s swappable blade tiers

Agent: Codex (GPT-6), built-in image_gen.
Status: generation in progress.

Exact prompt: `prompt-v1.txt`.

Mara identity references opened: `design/concepts/characters-g5/codex/melee-1-v2.png` and `design/pixellab/chibi-motion/hero-ref-64.png`; Mara section read in `characters.md`. G7 specifically permits ivory-white steel for tier 8, overriding the general reserved-colour rule.

Resume: inspect generated source, preserve source PNG, export/check 1024×512 exact 8×8 blocks with local base (4,16), widths 2–4 and lengths 12–16 native pixels, write blades.json measured from final pixels, record deviations and append completion to AGENT_LOG.md.

## Final result — 2026-10-15

Status: DONE. Recommended: **blades-v2.png**, paired with blades-v2.json. The requested blades.json also has the same dimensions, cell order and palettes and is compatible with v2.

Built-in image_gen produced blades-raw-v1.png (1774×887 PNG). Exact model identifier was not exposed by the tool. No external paid API, PixelLab or MiniMax was used. Exact tool prompt is preserved verbatim in prompt-v1.txt.

export-v1.py keyed the source, placed and resized the eight blades, and locked the palette/outline. That first automatic result (blades-v1.png) lost too much interior colour; retained as required. rebuild-v2.py is a retained failed export attempt (Pillow colour-string error); rebuild-v3.py is the successful native-pixel reconstruction of the generated designs into blades-v2.png. No generated attempt was discarded.

Files and sizes:
- blades-raw-v1.png — 1774×887, original generated PNG.
- blades-v1.png — 1024×512, automatic snapped attempt.
- blades-v2.png — 1024×512, recommended refined native sheet.
- blades.json / blades-v2.json — cell order, names, tiers, measured length/width including outline, local base [4,16], exclusive bounds and colour ramps.
- verification-v1.json / verification-v2.json — saved-file checks.
- prompt-v1.txt — exact image-tool prompt.
- export-v1.py / rebuild-v2.py / rebuild-v3.py — reproducible export history (v2 script failed; use rebuild-v3.py for recommended PNG).

Verified: 4 columns × 2 rows, 256×256 cells; exact flat #00B140; exact 8×8 pixel blocks; #2e1816 outline colour; no violet; all blades point right, no hilts/guards/hands; every base at local art pixel (4,16); lengths 13,14,15,14,15,15,16,16; widths 3,3,4,4,4,4,4,4. Each 3-shade material ramp is a permitted set; the limited space does not always use all three shades. No aura, sparkles, labels, shadows or grid. G7 explicitly overrides the general diagonal pose and ivory reservation.

Limitations: 2–4 total pixels of width including outline leaves only 1–2 interior rows. The steel fuller reads as a dark central strip; the captain crest is an abstract gold pixel mark, not a literal engraved emblem. Crystal facets, brass spine, zig-zag and flame contours are compressed to single pixels. Curves and taper are stepped. The geometrical checks do not evaluate aesthetic quality or every outline-neighbour relationship. Final v2 was visually opened and checked; Claude should preview the blade swap against actual slash frames for readability. No animation integration requested or performed.
