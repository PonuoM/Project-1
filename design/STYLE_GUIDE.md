# Hearth & Hoard — visual foundation

Cozy medieval adventure, warm brass and worn oak against midnight ink. Tiny characters have chunky silhouettes, readable faces and a little red scarf; loot is the brightest object. This is a visual direction, not a final game name.

## Pixel discipline

- Characters, monsters, boxes and large effects: 32×32 frames. Icons, coins and arrows: 16×16. Integer coordinates only, no anti-aliasing or partially transparent pixels.
- Every solid silhouette has a 1px `outline` edge. On dark backgrounds retain a light interior edge so the silhouette survives; a dark outline alone cannot separate a dark sprite from a dark desktop.
- Top-left light: light upper/left facets, dark lower/right facets. Use at most 18 palette colors per character, 10 per monster and 8 per icon; effects at most 6. Character sheets currently use no more than 17.
- Characters face right, monsters left. Standing characters are centered around x=16, boots touch y=31. Death frames fall onto the floor. Effects need not touch the floor.
- Render at 1×, 2× or 3× with `image-rendering: pixelated`. Never resize source sheets or use fractional sprite positions. Frames share a baseline, not a changing crop.
- Palette is locked to `tokens.json`. Transparent pixels are RGBA (0,0,0,0), opaque pixels alpha 255. No blurred glow; use stepped light-color pixels instead.

## Palette roles

Ink/outline/slates: outlines, metal, plates. Cream/white: text, bone, highlights. Skin: faces. Wood: leather and chests. Gold: coins, brass and rewards. Red: scarf, injury; green: slime/goblin; blue: steel and magic; purple: mage robes and skill gems. Item sprites stay neutral: rarity is applied by the UI border, never baked into the item icon.

## Rarity

| Key | Thai | Color | Redundant marker |
|---|---|---|---|
| common | ธรรมดา | #8794A7 | I / 1 notch |
| uncommon | ดี | #6DB586 | II / 2 notches |
| rare | หายาก | #5389CA | III / 3 notches |
| epic | มหากาพย์ | #B19AD8 | IV / 4 notches |
| legendary | ตำนาน | #FFD875 | V / 5 notches |

Blue is darkest; purple and gold become progressively lighter. Adjacent tiers also differ in hue. Color alone is never the rarity signal: keep the Thai label and Roman marker, including in inventory tooltips. In monochrome or color-vision deficiency some pairs still converge; markers resolve that ambiguity. All rarity borders use a dark outer edge and light inner keyline. Do not put pale gold text directly on a white desktop.

## Text and desktop readability

Use GameFont when the integration supplies it; for these mockups use installed Leelawadee UI / Tahoma, without downloading fonts. Thai body text is 12–16px, headline 24px; 10px only for short numeric micro-labels. Preserve Thai vowel/tonal marks with line-height at least 1.5. Font rendering may use browser anti-aliasing; the no-AA rule applies to bitmap assets.

All strip text has a 1px eight-direction ink shadow. Variant A uses the 94% ink plate; it is the recommended production default. Variant B has no band plate and uses outlines and double-edge sprite silhouettes. Popups retain their own opaque ink background in either variant. Damage numbers use cream with ink outline; never red-only information.

## Do / don't

- Do: draw a 32px hero at 32 or 96px. Don't: draw it at 45px or smooth its edges.
- Do: show `V ตำนาน` with a double-edge gold border. Don't: communicate rarity solely by a gold glow.
- Do: use a 24px minimum interactive target around a 16px icon. Don't: make the whole battle band clickable.
- Do: keep overlays empty except a transient reward/toast. Don't: fill the 156px overlay with permanent HUD.
- Do: keep wood chests warm and gold chests clearly metal with a visible lock. Don't: distinguish locked/ready states solely by brightness.

## Animation

Idle 4 frames, small breathing/cloth movement; walk 6 frames, alternating boots and arm swing; attacks anticipate, extend, impact, recover. Event indices in manifest are zero-based. Death is non-looping. Use reduced motion in previews; game integration should respect its own settings. No frame blending.

## Handoff

Region bosses use 48×48 frames, at most 10 colors and a baseline at y=47, fitting the 64px band. The floating ghost may leave the bottom row empty but retains pixels in the bottom four rows. Ground tiles are 64×8, binary alpha and low contrast; their left/right edge samples match. Continuous ground gets an outline along its top contour rather than a vertical outline at each repeat seam. App icons are drawn on separate native grids (16–256px) with the same outline and top-left lighting; they are not scaled sprite exports.

Regenerate using `python design/tools/build_sprites.py`, then `python design/tools/build_mockups.py`. Preview pages work by opening files directly; the sprite preview embeds the manifest to avoid file-URL fetch restrictions. Engine integration must read `manifest.json`, dispatch impact events and configure native click-through regions; HTML pointer-events do not implement Windows click-through.
