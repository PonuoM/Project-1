# G10 elemental hit effects — designed keyframes

2026-10-15. Codex (GPT-6), built-in image_gen; exact image model ID not exposed. Status: unfinished, generation in progress.

This is the NEW G10 elemental-hit section at the end of GEMINI_PROMPTS.md, not the earlier world-map G10. User requested redesigned combat elemental effects. Existing combat-feel/index.html inspected read-only. All three reference PNGs opened: scale-hero-and-monster.png, lootbox-hero-combat.png, our-current-hits.png. Scale/style guide only, no other game's shapes copied.

Exact prompts/palettes in prompts-v1.json. Each separate sheet has4 temporal keys,1024x256,64x64 native cells enlarged4x,hit anchor(32,52). Pure black additive background overrides green. Lightning's muted violet edge is explicitly allowed; #7a3cff is excluded. No videos generated, no game/runtime assets edited.

Resume: copy imagegen sources as *-raw-v1.png; inspect all five. Export crisp4x pixel sheets with palette-only content and pure black background, preserve every attempt. Verify4 cells/no spills, phase progression and dimensions. Save lineup-v1.png1024x1280, optional native-size comparison and scale preview. Complete notes with exact sizes, recommendations and deviations, append AGENT_LOG.md.

## Completion — 2026-10-15

Status: DONE for G10 designed keyframes. Recommend **fire-v2.png, ice-v2.png, poison-v2.png, lightning-v2.png, explosion-v2.png** (all1024x256 PNG) and **lineup-v2.png** (1024x1280). Native-scale comparison lineup-1x-v2.png256x320. Requested v1 sheets/lineup retained.

Built-in image_gen produced one separate PNG per effect. Exact prompts and4-colour ramps in prompts-v1.json. Three references were all visually opened; reference images were used for reasoning/style/scale, not provided as edit targets. Every generated attempt saved in repo, no JPEG/WebP conversion. Raw fire/ice/poison/lightning are2172x724 each; raw explosion1983x793. Source model ID not exposed. No video call, external paid API, PixelLab or MiniMax.

Diagnosis from inspected combat-feel prototype and reference: several burst animations share a round silhouette, colouring alone does not communicate material; small generic rising status spots obscure the intended distinction. G10 designs establish5 different gestures and temporal key poses: upward flame tongues/embers, faceted ice/shards, lateral liquid arcs/falling droplets/puddle, thin vertical lightning/ground arcs, radial explosion ring/debris/smoke. Black gaps keep the shapes readable on additive compositing. No reference-game icons copied.

Export history: export-v1.py locks4x grid/4 content colours plus black and common anchor, but resizes full source panels to squares. Different source aspect ratios made shapes too wide or short. Retained all v1 outputs. export-v2.py extracts each generated cell, finds a common source anchor from the initial key, and applies one UNIFORM scale across all four source keys, preserving proportions. Frame anchor is native(32,52),4x image(128,208). Exact key placement is approximate around that footpoint; source-generated shapes can shift locally. No replacement effect art was drawn with code.

Verification-final-v2.json checks exact1024x256,4x4 solid blocks, at most5 colours including black, no weapon-ID violet,3 native-pixel black gutters on all sides of all cells, nonempty start, and final-key occupancy lower than impact. lineup-v2.png dimensions1024x1280 checked. All5 source sheets visually opened, recommended large lineup and native1x lineup visually inspected. Four phases are start/impact/breakup/remains. Large peak heights: fire49px,ice49px,poison40px,lightning49px,explosion37px including debris. Sizes in art-direction.md; these fit roughly a hero's scale but should be tuned to actual enemy size during integration.

Limitations: source tool ignored requested canvas size and exact block scale; final exports normalize them. Flames' breakup still shares a small base rather than completely detached ribbons. Poison puddle remains visible in each phase. Explosion's final wisps occupy84 native pixels and read less sparse than fire15/ice30; still much smaller than its432-pixel peak. Generated fragment placement is not frame-perfect or guaranteed temporally coherent. Lightning source touched the top; final bolt starts atnativey4. Uniform fit and nearest palette reduce tiny specks and may simplify particles. Muted violet#6741a4 is explicitly permitted for lightning edging, #7a3cff never used. Anchors are a design contract, not extracted physical collision points. These are4 KEYFRAMES, not smooth animation strips or generated videos.

art-direction.md contains shape language, recommended per-key timing, additive placement and combo hierarchy suggestions. Keep first2 combo hits smaller, reserve full peak for finisher, avoid stacking full-screen white flash over every effect. Changes to actual combat code were not performed; user requested design sheets first per the new G10. Owner review then Claude's H3 Max generation/extraction/integration follow. Existing combat-feel page, motion files and game files unchanged.

Saved PNGs: fire/ice/poison/lightning/explosion-v1.png and-v2.png1024x256 each; lineup-v1.png and-v2.png1024x1280 each; lineup-1x-v1.png and-v2.png256x320 each; four2172x724 sources plus explosion1983x793. Full inventory files-v2.json. Supporting files prompts-v1.json, export-v1.py, export-v2.py, verification-v1.json, verification-v2.json, verify-final-v2.py, verification-final-v2.json, art-direction.md and notes.md.

Remaining G10 art deliverables: none. Next: owner selects/approves shapes, Claude animates and connects them to combat preview. No overwrite/delete of existing files.
