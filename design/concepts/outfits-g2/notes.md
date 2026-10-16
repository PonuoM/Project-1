# G2 hero outfits

Agent: Codex (GPT-6). Image backend: built-in image_gen; model identifier not exposed.
Status: started; A/B/C edits pending. Input: input/hero-steel-x8-green.png (512×512). Preserve original head, hair, face, hands, pose, feet positions and steel sword; change clothing and boots only.

## Saved files and recommendation

- set-a-v1.png — 512×512 PNG; recommended plate-knight.
- set-b-v1.png — 512×512 PNG; recommended mage.
- set-c-v1.png — 512×512 PNG; recommended ranger.
- set-a-raw-v1.png, set-b-raw-v1.png, set-c-raw-v1.png — each 1254×1254 PNG; original built-in outputs retained.

Export: each raw image sampled at 64×64 cell centers and enlarged by exact nearest-neighbor 8×, with green background normalized to #00B140. No JPEG conversion. No other image attempts were discarded.

## Limitations

The edits preserve the overall placement and down-right sword pose visually, but are NOT exact pixel-for-pixel traces. The generator changed preserved colors and some face/hand details. Head-region exact RGB comparisons differ at 599/598/599 art cells (A/B/C); sword-region comparisons differ at 79/79/78 cells. These counts include palette changes, not just movement. Armour, robe and jerkin are recognizable; mage hood is down. Exact original head, hand and sword pixels and strictly three-color material ramps are not certified. All final images have exact 8×8 solid blocks, opaque background, and zero exact #7a3cff pixels. Treat as clothing concepts for integration, not drop-in sprite replacements.

## Exact image-tool prompts

### Set A

```text
Use case: identity-preserve. Edit target: the provided 512x512 hero-steel-x8-green.png, a 64x64 sprite enlarged exactly 8x. Use it as a TRACING TEMPLATE. Output one 512x512 PNG. Keep the exact head, teal bob hair, face, skin, hands, feet locations, body pose, placement, proportions and steel short sword unchanged, including the sword in the SAME hand pointing diagonally down-right at the SAME angle. Do not recenter, enlarge, shrink, rotate or redraw those preserved parts. Change ONLY clothing and boots. Keep the sprite precisely on its original 64x64 grid: every art pixel an exact solid 8x8 image-pixel square, warm dark outline #2e1816 one ART pixel wide, flat three-shade color ramps, no antialiasing. All background flat exact #00B140. No violet #7a3cff, text, labels, extra objects, floor, shadows, gradients, glow or blur. Set A plate-knight: dark steel plate chest armour with shoulder pauldrons, short crimson cape, dark armoured boots. Keep all clothing in the existing body placement and keep original boots' footprint.
```

### Set B

```text
Use case: identity-preserve. Edit target: the provided 512x512 hero-steel-x8-green.png, a 64x64 sprite enlarged exactly 8x. Use it as a TRACING TEMPLATE. Output one 512x512 PNG. Keep the exact head, teal bob hair, face, skin, hands, feet locations, body pose, placement, proportions and steel short sword unchanged, including the sword in the SAME hand pointing diagonally down-right at the SAME angle. Do not recenter, enlarge, shrink, rotate or redraw those preserved parts. Change ONLY clothing and boots. Keep the sprite precisely on its original 64x64 grid: every art pixel an exact solid 8x8 image-pixel square, warm dark outline #2e1816 one ART pixel wide, flat three-shade color ramps, no antialiasing. All background flat exact #00B140. No violet #7a3cff, text, labels, extra objects, floor, shadows, gradients, glow or blur. Set B mage: deep-blue hooded robe with gold trim reaching the knees, soft brown boots. Hood DOWN behind the neck, all teal hair fully visible. Copy the original head and face pixels EXACTLY: tiny original vertical eye, no eyebrow additions. Maintain exact original hand silhouettes and foot spacing.
```

### Set C

```text
Use case: identity-preserve. Edit target: the provided 512x512 hero-steel-x8-green.png, a 64x64 sprite enlarged exactly 8x. Use it as a TRACING TEMPLATE. Output one 512x512 PNG. Keep the exact head, teal bob hair, face, skin, hands, feet locations, body pose, placement, proportions and steel short sword unchanged, including the sword in the SAME hand pointing diagonally down-right at the SAME angle. Do not recenter, enlarge, shrink, rotate or redraw those preserved parts. Change ONLY clothing and boots. Keep the sprite precisely on its original 64x64 grid: every art pixel an exact solid 8x8 image-pixel square, warm dark outline #2e1816 one ART pixel wide, flat three-shade color ramps, no antialiasing. All background flat exact #00B140. No violet #7a3cff, text, labels, extra objects, floor, shadows, gradients, glow or blur. Set C ranger: brown leather jerkin with a dark-grey scarf, belt with pouches, brown leather boots. Copy original head, tiny vertical eye and face exactly. Keep original hand shapes and boot locations. Do not add weapons or headgear.
```

## Pose verification and handoff

All three tie for best overall pose: zero changed foreground/background cells in the head region (y<37) and sword region (x>=38,y>=48), compared to the template at 64×64. Colours and interior details differ as above. Status: outfit concepts saved and verified; unfinished against the strict exact-pixel preservation requirement. Left: restore original protected head/hair/face/hand/sword pixels and enforce three-shade clothing ramps using an approved precise sprite-edit workflow. No game files changed.
