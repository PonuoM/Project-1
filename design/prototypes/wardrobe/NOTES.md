# PixelLab wardrobe and action prototype

Question: can the selected chibi pixel look support six removable fashion slots while walking, attacking and jumping?

Open http://localhost/Projects-1/design/prototypes/wardrobe/index.html through AppServ. Or run `python -m http.server 8080` from the workspace and open `/design/prototypes/wardrobe/`.

## Current implementation

Actual PixelLab body/gear rasters and native body animations are loaded by `pixellab-character.js` through `../../pixellab/chibi-modular/assets.json`. The rejected code-drawn paper doll is not rendered; `character.js` supplies only root/weapon motion curves.

Body images remain an immutable base layer. Hat, shirt, pants, weapon, wrist and boots are separate canvases. Gear follows per-frame attachment coordinates. Base feet are masked only in the final composition when boots are worn. Mirror reverses the whole assembled character once. Jewelry changes state but never pixels.

- J normal attack; K heavy slash; L jumping dash attack.
- Walk, automatic cycling, mirror, size, pause, frame scrub and replay.
- Equipment can change mid-move or while paused.
- Current frames: idle 1, walk 9, attack 9, heavy slash (`slam-v2`) 9, jumping dash 13. The original 11-frame heavy slash remains preserved as generation history.
- Native body 64x64; composed canvases 128x128 with 32px gutters.
- Damage and timing are synthetic visual test values. No game API, reward mutation or persistence.

## Inherited visual identity

The compact dark fantasy workbench extends `../action/prototype.css` and `../../tokens.json`. Scene and controls sit beside gear on desktop and stack on narrow screens. The selected source concept remains visible. No root design system or production assets were replaced.

## Art acceptance

Exact requests, original responses and crop provenance are under `../../pixellab/chibi-modular/`. These are actual AI-generated PixelLab rasters, with code-authored attachment transforms and effects. This does not claim the generator produces perfectly aligned fashion automatically. Inspect seams and extremes before expanding the wardrobe.

Owner verdict on this native result: pending. The previous code-art proof was explicitly rejected and must not be presented as the chosen look.

## Initial native PixelLab trial verification (superseded)

`../../qa/pixellab-wardrobe.json` records the initial trial's 43 native poses and 258 slot-removal checks with zero failures. These are historical results; the current revision's 41 poses and 246 checks are recorded in `../../qa/right-hand-hood.json` below. The initial base layer remained immutable across wardrobe changes; jewelry did not change pixels. No sampled frame touched the composed canvas boundary. The selected reference loaded, and the mobile view had no horizontal overflow.

The checked frame counts are idle 1, walk 9, normal attack 9, heavy slash 11 and jumping dash 13. Native body frames are 64 by 64; every compositing layer is 128 by 128 with a 32px gutter. These values supersede the earlier procedural proof's dimensions and checks.

Captures are retained in `.impeccable/review/wardrobe/` at the workspace root: `pixellab-desktop.png`, `pixellab-mobile.png`, `pixellab-leap.png`, `pixellab-bare.png`, `pixellab-mirror.png`, `pixellab-walk.png`, `pixellab-attack.png` and `pixellab-slam.png`. The finish review cleared the boot-coverage, README and frame-count corrections for this isolated prototype trial. That review does not constitute owner acceptance or approval for production integration.

Initial generation usage was 24.1, with a recorded subscription balance of 3.65 at that point. The additional `slam-v2` generation brings cumulative usage to 25.1 and the estimated remaining balance to 2.65. Further generation is not needed to inspect the current trial. Wearable attachment coordinates, garment seams and occlusion remain a first art pass, and additional outfits have not been validated. Owner verdict remains pending.

## Right-hand / hood / weight revision

Owner feedback: sword should use the right hand, slash needs weight, hood behind hair looked wrong. The right hand is the near-side arm (screen-left in the initial right-facing sprite); `rightHand` per-frame anchors now drive the sword and near bracer.

A real PixelLab `slam-v2` generation returned 9 frames, but its near arm still failed to raise overhead clearly. The renderer therefore re-poses original PixelLab skin textures at explicitly annotated shoulder/elbow/hand coordinates for the loaded and follow-through poses. This hybrid correction is code-attached original art, not a claim that the generator returned the final choreography perfectly.

Heavy slash frame durations in milliseconds: 25,45,70,100,25,45,90,140,80 (620 total). Fast swing, held loaded pose and longer follow-through; impact at310ms with70ms visual hit stop. Root step, modest body lean and a wider impact arc add weight. User preference for reduced motion disables shake/hitstop.

The hood now uses original cloth pixels with native alpha opening/foreground masks; foreground cloth covers hair crown and neck instead of placing the complete hood behind all hair. Hair remains visible inside the opening. Mask preparation provenance: parts/hood-masks.json.

Source reference read: https://www.slynyrd.com/blog/2018/9/8/pixelblog-9-melee-attacks (anticipation, fast smear, follow-through hold). YouTube nJbzBSVy1u0 could not be fetched directly; no claim of watching its contents.

Revision QA (`../../qa/right-hand-hood.json`): 41 poses, 246 equipment-removal checks, zero failures, edge touches or frame mismatches; the sword reports right-hand attachment in all poses; mobile has no overflow; heavy slash registers one impact. Owner perception of weight and final clothing seams remain pending.

## 3D render source (Blender) — Codex Prompt 8/8.1, finished by Claude 14 Oct 2026 after Codex hit its usage limit

Default art source is now `3D render (ใหม่)`; `PixelLab (เดิม)` stays selectable for comparison. Rebuild everything with one command (≈15 s): `python -I design/tools/render_sprites3d.py`.

What Claude changed on top of Codex's pipeline:
- **Colours**: Blender renders data (Raw view transform, no dither): R = material id, G = light band. `pack_sprites3d.py` paints each id with dark/mid/light ramps sampled from the reference, replacing nearest-colour quantisation that had turned the olive tunic brown and the plate beige.
- **3/4 camera (35°)** to match the PixelLab head; frames are laid out along the camera's screen-right axis; the sun is fixed relative to the camera (upper-left, viewer side).
- **Outlines baked per layer**: a 1 px ring outside each layer (with a depth just behind the surface it outlines) plus inner lines where a nearer part of the same layer overlaps a farther one. Any outfit combination keeps correct outlines through the normal depth test; the browser no longer adds its own ring.
- **Head depth**: each frame records the head bone's camera depth; weapon/wrist pixels (and arm pixels above the chin) nearer than the head by 0.35 are flagged in the depth sheets' G channel, so a raised sword is drawn over the 2D head instead of behind it.
- Readable 4 px blade + larger guard; mantle-sized cream scarf and a red sash wider than the tunic; walk keeps the sword low (KayKit's walk is unarmed); the fast attack leans back on the wind-up and forward on impact.
- QA: feet are checked on the body+boots only (row 62, outline on 63), not on a lowered sword. Current: 38 poses, 0 layer-vs-reference differences, 0 feet failures, weapon grip in the right hand every frame, 2 edge touches (leap frames 2–3, iron outfit — longer sabre).

Known gaps: body still slimmer than the reference; hands are small mitts; head tilt variants are row-shifted copies; the impact arc FX is a placeholder; the plum chest is rendered but not in a preset outfit. Owner verdict pending.
