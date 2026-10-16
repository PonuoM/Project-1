# Design deliverables

Latest equipment/action proof: [`prototypes/wardrobe/index.html`](prototypes/wardrobe/index.html) tests six removable clothing/weapon layers, hidden jewelry, walk, normal attack, overhead slash and jumping dash. It now uses **actual PixelLab body animations and independent equipment textures**; per-frame clothing attachment is a trial art pass. The selected chibi concept is in `concepts/chibi-v2/`; PixelLab requests, original outputs and usage are documented in [`pixellab/chibi-modular/README.md`](pixellab/chibi-modular/README.md).

Latest direction experiment: [`prototypes/action/index.html`](prototypes/action/index.html) demonstrates actual world movement, scenery and fast heavy attacks. Read [`CLAUDE_HANDOFF_ACTION_PROTOTYPE.md`](CLAUDE_HANDOFF_ACTION_PROTOTYPE.md) before changing the game's layout/scene/FPS. The prototype is isolated and does not supersede production assets until the owner chooses the direction.

Latest art trial after the owner's feedback: [`pixellab/swordsman/preview.html`](pixellab/swordsman/preview.html), generated via PixelLab. Sixteen 64px swordsman candidates and one sword animation are isolated from the game manifest; see that folder's README and `CREDITS.md` for prompts and AI provenance.

All six prompts in `CODEX_PROMPTS.md` are implemented inside this directory. According to the brief, prompts 1–4 have been integrated by the game developer; the new icons and regional assets are ready for integration.

- Foundation: `tokens.json`, `STYLE_GUIDE.md`, `palette.png` (30 swatches, 480×16).
- Sprite assets: `sprites/manifest.json`, 74 PNG sheets / 307 frames, `sprites/preview.html`. All priority A/B and regional keys included; nothing skipped.
- App icons: `icons/preview.html`, seven native PNG sizes, two tray PNGs and `icons/app.ico`. 16/24/32px are hand-tuned.
- Regions: `regions.json`, wolf/spider/ghost, three 48px bosses and three seamless 64×8 ground tiles. The 47 original sprite files/entries are preserved.
- Desktop strip: `mockups/strip.html`, `strip.css`, `tokens.css`, `NOTES.md`. Five states × three backdrops × two variants.
- Main window: `mockups/window.html`, `window.css`, shared `tokens.css`. Five keyboard-accessible tabs within 960×600.
- Provenance: `CREDITS.md`. Original code-generated pixel art, no external image or font assets.
- QA: `qa/assets.json`, sprite contact sheet and desktop screenshots. PNG format and engine contract checked by `tools/verify_assets.py`; browser layout checks recorded in `qa/browser.json`.
- New asset QA: `qa/icons.json` validates all PNG/ICO sizes; `qa/prompt56-browser.json` checks icon/region galleries, image loading, playback and mobile overflow. `qa/prompt56_before.json` records original manifest entries and PNG hashes before the extension.

Open the HTML pages directly, or serve this project using the existing local web server. No package install or build is needed to view them.

## Regeneration

Python + Pillow are needed only to regenerate assets:

```powershell
python design/tools/build_sprites.py
python design/tools/build_regions.py
python design/tools/build_icons.py
python design/tools/build_mockups.py
python design/tools/verify_assets.py
python design/tools/verify_icons.py
```

The manifest is the engine contract. Mockups are visual references: controls do not mutate game state or save preferences. Read `mockups/NOTES.md` for native window integration, dimensions and unresolved gameplay values.
