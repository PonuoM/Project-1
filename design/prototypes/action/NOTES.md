# Action / journey prototype

Question: can a small scenic desktop RPG feel like a journey, with fast attacks and a heavy impact, before rewriting the existing game?

Open `index.html` directly; no build, server, account or install needed. The existing local web server can also serve `/Projects-1/design/prototypes/action/index.html`. Regenerate isolated PNGs with `python design/prototypes/action/build_art.py` (Pillow).

## Try it

- A: compact widget, scene 560×180, HUD and action row below.
- B: long journey, scene 800×160, compact controls inside the scene and health at the right.
- C: scene 560×240, equipment inspector to the side with its own scrolling.
- Switch via bottom bar or URL `?variant=A`, `B`, `C`.
- Space / skill button: heavy ground slash. The button can also trigger an immediate close-range encounter for testing.
- ฟัน: short basic slash. Press during recovery to queue one next strike.
- Drag the scene: pan the camera; กล้องตามตัวละคร resumes follow. Drag the title bar to move the widget inside the review area.
- Pause, auto battle, shake, optional synthetic impact sound and reset are available. Reduced motion disables shake and hit flashes.

## Hero art (PixelLab trial, added by Claude 13 Oct 2026)

Switch with the buttons under the scene or `?art=`:
- `clean` (default): `design/pixellab/swordsman/cleaned/` — copy with the 14 stray pixels on the left removed. Frames not moved (feet on row 63 in every frame, front foot within 49–51px). Made by `python -I design/tools/clean_pixellab_frames.py design/pixellab/swordsman`; report in `cleaned/inspection.json`.
- `raw`: the untouched PixelLab originals in `design/pixellab/swordsman/`.
- `code`: the earlier code-drawn knight with its hand-timed poses (unchanged).

PixelLab sheet size, frame count, fps, impact frame and hit stop are read from the folder's `animation.json` (64×64, 9 frames, 32 FPS, impact frame 3, hit stop 45ms) and checked against the PNG size; nothing is assumed in code. Impact lands at 94ms, the impact frame is held for the 45ms hit stop, the swing ends at ~326ms. The still candidate is taken from `selection.json`.

Limits, also listed on the page: no PixelLab walk sheet yet, so walking/idle is the still candidate sliding through the scene (never swapped for the old art); the skill reuses the attack frames with a 60ms stop and bigger wave; monsters are still the code-drawn 48×48; the hero is ~61px tall; frames 0 and 8 are PixelLab re-renders that differ from candidate-11 by ~21 visible pixels; the generated swing follows through behind the hero.

Impact feel for every hero art: monster squash/stretch + 1px shiver + knockback, a travelling slash wave that cuts through and past the monster, ground dust from both feet, and a short scene-only shake (HUD is DOM and never shakes). `ช้าลง 4 เท่า` slows simulation and stops for frame inspection; `F` = slash, `Space` = skill.

## Motion values

Basic: 35ms anticipation + 55ms swing/lunge + 45ms visual hit stop + 105ms recovery = approximately 240ms total before any between-attack gap.

Skill: 70ms anticipation + 65ms lunge + 60ms visual hit stop + 145ms recovery = approximately 340ms. Visual skill cooldown is 1.6 seconds for repeated evaluation, not a gameplay balance decision.

Rendering uses requestAnimationFrame. Walk advances the hero in world coordinates and scrolls multiple background layers; battle pauses world travel. Hit stop pauses only visual simulation; UI cooldown continues. The canvas alone shakes, not HUD or the desktop. No full-screen flash.

## Scope

All data and outcomes are simulated in memory. There is no game API or economy connection. The separate 64×64 knight frames have a visible silhouette around 48–54px high, with empty space around the sword/cape. Enemy frames are 48×48. These are original experimental poses, not polished production art and not an engine-facing manifest.

Production impact and coordination are documented in [`../../CLAUDE_HANDOFF_ACTION_PROTOTYPE.md`](../../CLAUDE_HANDOFF_ACTION_PROTOTYPE.md). The existing client/server, base tokens, main manifest and original assets remain as they were.

## Decision

Pending owner feedback: layout A/B/C, attack feel and character/scene direction. Do not infer a chosen layout from the default A. After deciding, update the brief, implement the selected behavior properly in the game, and remove/absorb this throwaway prototype.
