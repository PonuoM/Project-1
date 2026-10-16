# PixelLab swordsman trial

This is an isolated AI-generated art trial requested by the owner after rejecting the code-drawn prototype art. Do not replace the game's original sprites or manifest automatically.

Official API: <https://api.pixellab.ai/v2/docs>. The connector uses bearer authentication against `https://api.pixellab.ai/v2/` only. No credential is saved in this folder or in `tools/pixellab_client.py`.

## Initial direction

64×64 transparent sprite, visible character roughly 48–54px tall, adult armored swordsman facing right. Detailed silver plate armor, crimson plume/cape, heavy sword and compact brass-edged shield. Aim for readable handcrafted pixel clusters and distinct anatomy rather than a simplified cute/chibi style.

The initial `/generate-image-v2` request generates a candidate batch. `request.json` contains the exact prompt and parameters; `generation-job.json` contains the service job ID. Original downloaded images are retained without quantizing them into the old palette. The target is capped at 32 colors but does not force the existing palette; assess any palette change before game integration.

## Reuse the connector

Set `PIXELLAB_API_KEY` in your process environment using your own secret manager. Do not paste it into scripts, JSON prompts, documentation, git or generated HTML.

```powershell
python design/tools/pixellab_client.py balance
python design/tools/pixellab_client.py generate-image-v2 --payload design/pixellab/swordsman/request.json --out design/pixellab/swordsman/new-job.json
python design/tools/pixellab_client.py background-jobs/JOB_ID --out design/pixellab/swordsman/job-result.json
python design/tools/pixellab_client.py background-jobs/JOB_ID --images-dir design/pixellab/swordsman --prefix candidate
```

The balance command and job polling are read-only API calls. Generation calls use the account's available credits/generations. To inspect an existing result, poll the recorded job instead of submitting the generation again.

Polling an existing job does not submit a new generation; the last two examples write the retrieved result locally. The initial trial produced 16 native 64×64 candidates. The service reports 10 subscription generations for this batch (`generation-result.json`). Candidate 11 is an agent's provisional choice for the animation test; the owner has not selected a final character. `selection.json` records that distinction.

## Sword animation result

`animate-with-text-v3` used candidate 11 as both start/end reference with the exact action prompt in `animation-request.json`. Eight generated frames were requested; the service returned nine images including the supplied reference. All originals are kept in `attack-frames/`. `attack.png` packs exact RGBA copies horizontally for browser preview, without recoloring or modifying frames.

The service reports 1 additional subscription generation for animation, for a total of **11 generations** in this trial. `animation-result.json` records actual usage. No additional character/walk generations were submitted.

Open `preview.html` to inspect all 16 choices at native scale and 4× on light/dark backgrounds and to play the sword animation. Preview timing is 32 FPS with a 45ms visual hold at zero-based frame 3; slower playback is available for inspection. The animation is an exploratory visual result, not a gameplay damage/cooldown decision.

Some raw outputs contain isolated edge pixels, and the generated attack's frame baselines need a production alignment pass. Assess silhouette, shield/weapon consistency and effect clipping before adopting them. The original model output is preserved so later cleanup can be compared rather than overwriting evidence.

Rebuild the gallery/sheets/contact sheets without calling PixelLab:

```powershell
python design/tools/build_pixellab_preview.py
```

## Claude handoff

The owner explicitly requested trying PixelLab for the swordsman. Existing code-drawn assets are now an earlier experiment, not visual authority for this character. Keep trial assets out of `design/sprites/manifest.json` and `sync-design.mjs` until the direction is chosen. The prior action/camera timing experiment still applies; art quality and animation timing are separate decisions. See `../../CLAUDE_HANDOFF_ACTION_PROTOTYPE.md`.

PixelLab output uses an AI image-generation model. Record this provenance when any of these assets ship.

## Cleaned copy (Claude, 13 Oct 2026)

`cleaned/` holds a copy for the prototype: the 14-pixel detached fragment at x 0–4, y 30–33 (present in candidate-11 and the attack frames) is removed; white slash sparks in frames 05–06 are kept; no frame is moved because every frame's feet sit on row 63 and the planted front foot stays within x 49–51. Originals in this folder are unchanged. Regenerate with `python -I design/tools/clean_pixellab_frames.py design/pixellab/swordsman` (no PixelLab call). Details per frame: `cleaned/inspection.json`.
