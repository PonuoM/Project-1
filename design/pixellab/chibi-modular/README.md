# Chibi modular PixelLab trial

Actual PixelLab API generation is complete. The trial uses the selected teal-haired chibi direction from `../../concepts/chibi-v2/hero-concept.png`.

Open: http://localhost/Projects-1/design/prototypes/wardrobe/index.html

- Base: `base/candidate-01.png`, provisionally selected from 16 actual native 64x64 outputs.
- Equipment: 4 actual 128x128 sheets; six components extracted from `equipment/candidate-02.png` into `parts/`.
- Current animation frames: idle 1, walk 9, normal attack 9, heavy slash (`slam-v2`) 9, jumping dash 13. The original 11-frame heavy slash is preserved. PixelLab includes the reference in the returned sequence.
- Separate visible slots: hat, shirt, pants, weapon, wrist, boots. Jewelry is data only.
- `assets.json` records files and per-frame garment coordinates. `parts/provenance.json` records lossless crops and detached neighboring-item cleanup; component colors are retained.

The prototype uses actual full-frame PixelLab body animations, with original skin textures reposed on the near arm during the current heavy slash to make the overhead motion clear. Code attaches the separate generated clothing textures to per-frame anchors and controls root movement, weapon rotation and effects. PixelLab did not automatically produce a rigged wardrobe. The cream hood now uses an opening mask and a foreground cloth mask over the hair crown and neck; hair stays visible inside the opening. Bare feet are masked in the final composite when boots are worn; wardrobe changes leave the base layer unchanged.

## Provenance and usage

Original service responses, image payloads, job IDs and exact prompts are retained with outputs. No API credential is saved in this repository or exposed to the preview browser.

Initial usage: base 10 generations, equipment 10, four animations at 1 each, and reference `/unzoom` 0.1: **24.1 generations**, with a recorded balance of **3.65** at that point. One additional `slam-v2` generation brings cumulative usage to **25.1 generations** and the estimated remaining balance to **2.65**. No further generation is needed to inspect this trial.

Official schema: https://api.pixellab.ai/v2/openapi.json

## Asset preparation without generation

```powershell
python design/tools/extract_chibi_equipment.py
python design/tools/build_chibi_manifest.py
```

Generation scripts retain recorded job IDs and poll existing jobs rather than resubmit. Keep credentials in the environment only. A different approved character/outfit should use a new isolated trial directory.

## Limits

This is a real art/wardrobe prototype. Attachment coordinates and wearable transforms are a first art pass; inspect seams and all extreme poses before producing more fashion. Additional outfits have not been generated. Owner acceptance of this native trial is pending.

The earlier procedural `character.js` remains historical code: only its root/weapon motion formulas are reused. Its body/clothing drawing is not displayed. No client, server or production sprite manifest changes were made.

Current revision: `slam-v2` has 9 frames with right-hand attachment and reposed original arm textures; the hood uses separate foreground/opening masks. Heavy slash uses a nonuniform 620ms schedule, impact at 310ms and 70ms visual hit stop. `../../qa/right-hand-hood.json` records 41 poses and 246 passing equipment-removal checks, zero boundary touches or frame mismatches, correct right-hand anchors, no mobile overflow and a verified heavy-slash impact. The original generation records remain preserved. See `../../prototypes/wardrobe/NOTES.md` for timing and provenance. Owner acceptance remains pending.
