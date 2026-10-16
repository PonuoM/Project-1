# Codex impact runtime experiment — 2026-10-14

Agent: Codex. Model: GPT-6 (session). No image model, PixelLab, MiniMax or paid generation service was used. Image-tool prompt: none; all artwork is reused from repo PNG assets, with contact sheets / frame packing / runtime captures made programmatically.

## Brief and recommendation
User referenced Screen_Recording_20261014_180756_Facebook.mp4 and asked for comparable attack weight plus evidence it can work in a game. Reference was probed (1078x566, variable frame timing, ~8.55s container) and sampled at 3fps. The reference shows snap movement, repeated hit accents, short anticipation and a strong final launch. It is inspiration for rhythm, not a frame-exact reconstruction.

Recommended: viewer-v2.html, demo-v2.mjs, attack-driver.mjs, phaser-impact-v2.mjs. The v1 files and both sets of captured frames are retained. V2 adds a vertical finisher smear, stronger lift reaction and explicit stage positioning.

Open live demo: http://127.0.0.1:8768/viewer-v2.html while the current local server runs. Restart with PowerShell: & .\design\concepts\impact-runtime-codex-v1\RUN.ps1 (requires free port 8768 and Python). Or use python -m http.server 8768 --bind 127.0.0.1 --directory design/concepts/impact-runtime-codex-v1. Open via HTTP; browser module imports do not work reliably via file://.

## Implementation and source assets
Phaser 3.90.0 copied from installed client/node_modules/phaser/dist/phaser.min.js with its MIT license. Live Phaser sprites, collision-at-contact query, per-contact events, local hit-stop, weapon smear, pooled afterimages, recoil, shake, recover and optional WebAudio placeholder hits. Controls: normal/heavy/3-hit combo, miss, restart, left/right, reduced shake, speed and 30/60 FPS cap.
Hero ref inspected: design/pixellab/chibi-motion/hero-ref-64.png. Slash strip comes from slash-c-sword/frame-00..14.png; chop from g1-chop-long-sword/frame-00..14.png. Slime strips copied from design/sprites. Existing artwork and palette unchanged.

## Verification
- node verify-runtime.mjs PASS: 30/60fps-sized deltas, 125/5000ms long steps, three unique events for combo, repeated start rejected, no contact/no hold on a miss, hit-stop remainder correctly consumed, cancel/restart, left-facing and invalid delta.
- Browser Phaser v1 combo: hits=3, hp=2, active=false; miss: hits=0, hp=5, hold=0; left-facing: hits=1, hp=4, direction=-1. Live 30fps-cap capture also ends at hits=3/hp=2.
- Browser Phaser v2 live capture: hits=3, hp=2, active=false. Desktop + 390x844 mobile inspected; mobile has no horizontal overflow. UI detector returned [].
- Real Phaser stage captures, not a prerecorded animation used to drive the demo: 32 PNG samples about 50ms apart per version. APNG compresses identical consecutive samples into 25 stored frames while retaining 1.6s total timing. Capture timer is approximate; runner timing tests are deterministic.
- All outputs verified inside the task folder. See files.json for every saved file, byte size, and PNG dimensions.

## Limitations / departures from the brief
This is a completed runtime prototype and integration handoff, not an integrated game release. No client/, server/, manifest, AGENTS.md, GEMINI.md or game-loaded asset was edited. The reference's long flurry/cross-ups are condensed into three readable sword contacts; exact body choreography needs additional authored poses. Existing source chop frames clip the long sword at the 80px canvas edge; FX suggests continued reach but does not repair those source pixels. Slime is a temporary target; final enemy reactions and balance need integration work.
Runtime images and captures use transparent sprite PNGs and a game-stage background instead of the chroma-key conversion sheet style. No new concept artwork for Claude to convert was generated; stage captures intentionally retain the floor so recoil is visible. Output display scale is 3x for the APNG and responsive for the live demo, not an 8x concept sheet. No JPEG/WebP conversion was needed; every saved image is PNG/APNG.
No live Electron performance benchmark or reward/sync integration test was performed. The comparison demonstrates usable Phaser timing/effects and correctness at tested delta sizes, not production readiness. See integration.md for exact ownership, coordinate/camera adaptation and killMs constraints.

## Saved images (relative to this folder)
- reference-contact-v1.png: 2156x1698.
- assets-check-v1.png: 600x240.
- assets/slash.png, assets/chop.png: 1200x80 each (15 frames of 80x80).
- assets/slime_idle.png: 128x32; assets/slime_death.png: 160x32.
- live-frames/frame-00..31.png and live-frames-v2/frame-00..31.png: 320x120 each.
- combo-contact-v1.png, combo-contact-v2.png: 1280x360.
- combo-preview-v2.png: 960x360, animated PNG, 25 stored frames / 1.6s loop.
- preview-desktop-v1.png, preview-desktop-v2.png: 1425x814.
- preview-mobile-v2.png: 390x844.

Scripts pack-assets.py and make-preview*.py document the transformations. Do not rerun against existing outputs: use a new version folder to respect append-only asset rules. Remaining work: Claude integration, runtime coordinate cleanup and in-game tuning as detailed in integration.md.
