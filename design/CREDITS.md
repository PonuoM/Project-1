# Asset provenance

The initial pixel maps, procedural animation poses, icons, CSS and mockups are original code authored with assistance from OpenAI Codex. Those initial raster files are produced deterministically by Pillow, not by an AI image-generation model. Installed system fonts are referenced only, not bundled. Pillow is a build dependency, not a shipped game asset. The subsequent PixelLab experiment is recorded separately below.

This records provenance; the publisher must assess any platform disclosure requirements for the final shipped product.

## Chibi concept and wardrobe proof

`concepts/chibi-v1/` and `concepts/chibi-v2/hero-concept.png` were generated with the built-in image generation tool; exact prompts are retained alongside them. The chibi-v2 image is the owner's selected visual direction and appears unchanged as a reference thumbnail in the wardrobe proof.

`prototypes/wardrobe/character.js` draws a temporary original code-authored pixel paper doll and six independently switchable equipment layers in browser canvases; `wardrobe.js` draws procedural scenery and combat effects. These are placeholders for a mechanics proof, **not PixelLab-generated images** or final art. The code paper doll was rejected. The current preview uses actual PixelLab rasters from `pixellab/chibi-modular/`: a native base body, six wearable components from a generated equipment sheet, and walk/attack/slash/jumping-dash animations. `prototypes/wardrobe/pixellab-character.js` attaches those textures to annotated frame coordinates. Original responses, prompts, crop provenance and usage are retained. It is an isolated AI-generated art trial, not production approval.

## Prompts 5–6

Application and tray icons are native-size, hand-tuned pixel geometry drawn by `tools/build_icons.py`. Every PNG is drawn separately; `app.ico` packs those exact PNGs without scaling. The 16, 24 and 32px app icons and both tray sizes use explicitly tuned coordinates. All larger sizes also have independent native geometry and extra facets/rivets.

Wolf, spider, ghost, king slime, treant and lich animations plus seamless regional ground tiles are original integer-coordinate pixel art drawn by `tools/build_regions.py`. No third-party assets or AI image-generation models were used. `tools/refresh_previews.py` rebuilds the combined gallery and QA atlas from the manifest. These additions retain the locked palette and preserve the original 47 sprite sheets byte-for-byte.

## Action prototype

`prototypes/action/build_art.py` creates original isolated knight and forest guard poses; `prototype.js` draws original procedural pixel scenery and combat effects. Optional impact audio is synthesized locally with Web Audio. Codex assisted the code. The two user-provided MP4 files inform structure and animation direction; no reference artwork, sprites, music or sound recordings are reused. No AI image-generation model or third-party asset pack was used.

## PixelLab swordsman trial

The owner requested PixelLab after rejecting the code-drawn character art. Assets under `pixellab/swordsman/` are generated using PixelLab's AI image/animation APIs from text prompts. The exact prompts and service job IDs are retained alongside outputs; no account credential is included. No reference artwork or video frames are uploaded for this trial. These images are isolated from the game's original manifest. If adopted for release, they are AI-generated artwork and should be included in the publisher's applicable disclosure.


Right-hand slash revision: actual PixelLab slam-v2 frames retain original artwork; the renderer re-poses original near-arm skin textures at explicit joints because the generated arm did not achieve the requested overhead silhouette. Hood opening/foreground alpha masks retain original generated cloth pixels. These are manually prepared AI-art derivatives, with provenance in parts/hood-masks.json and prototype NOTES.

## 3D → pixel sprites (design/3d, design/sprites3d) — added by Claude 14 Oct 2026

- **KayKit Character Pack: Adventurers 1.0** by Kay Lousberg — CC0 1.0 (licence file: `design/3d/source/kaykit/LICENSE.txt`, pinned URLs + SHA-256 in `design/3d/source/kaykit/sources.json`, fetched by `design/tools/fetch_kaykit.py`). Used for the Rogue skeleton, its animation clips and the base body/limb meshes. **Not AI-generated.** KayKit's head, hair and face texture are never rendered.
- Clothing shells, scarf, sash, sword/sabre and the toon/ramp/outline rendering are authored in `design/3d/build_and_render.py` and `design/tools/pack_sprites3d.py` (Blender 5.2.2, rendered locally, no network services).
- **The head is the owner's PixelLab character** (`design/pixellab/chibi-modular/base/candidate-01.png`, AI-generated) with offline pixel-edited tilt variants, and hats are hand-authored pixels. So the composite sprites are a hybrid: AI head + non-AI body/equipment. Declare the head in Steam's AI disclosure if it ships.
- Colour ramps are sampled from `design/pixellab/chibi-modular/reference-native.png` and `base/candidate-01.png`.
