# Motion guide for hand-made sprite animation (Codex / Gemini)

What Claude learned from the PixelLab skeleton tests and the MiniMax / Veo / Hailuo / Seedance video tests
(details: `design/pixellab/chibi-motion/README.md`, viewer: `design/prototypes/chibi-motion/index.html`).
Use this when a task asks you to draw animation frames. Step 1 (outfit concepts, Prompt G4) does not need it yet.

## Body facts of our chibi (64×64 frame, ~50 art px tall, side view facing right)
- The head is about 28 of the 50 px. Arms are only ~11 px long, so the hands barely reach above the head.
- Anything held straight overhead disappears behind the head. For overhead chops, draw the blade **behind the
  head** and make it long enough to show above it; otherwise it looks like the sword goes through the head.
- Keep the feet on one ground line (same y in every frame) unless the move is a jump. Feet that slide or float
  are the most visible error.
- Keep the head shape and face identical in every frame. Move the head as a whole (bob 1–2 px), never redraw it.

## Weapons are a separate layer
- Draw the body with an **empty fist**; the weapon is a separate sprite placed at the hand each frame.
  When AI draws the weapon into the body, it vanishes or changes length in the wind-up (seen in every test).
- For each frame record the hand position (x, y in art px) and blade angle in degrees, plus whether the weapon is
  in front of or behind the body. Claude places the weapon layer from that data, so one body animation works
  for every weapon of that type.
- Weapon lengths stay constant. Video models (Veo, Hailuo) turned the short sword into a katana mid-swing.

## Timing that reads as weight (ms per frame, from the attack Claude tuned)
Overhead chop, 15 frames, ~1.0 s:

| # | phase | ms | note |
|---|---|---|---|
| 1 | ready | 80 | rest pose |
| 2–4 | sink → raise → coil | 60/60/70 | anticipation: knees bend, weapon goes back |
| 5 | **HOLD** | 110 | the pause at the top is what makes it heavy |
| 6–7 | launch → chop | 40/30 | very fast; big change between these two frames |
| 8 | **IMPACT** | 50 | game adds hit stop + screen shake here |
| 9 | squash | 60 | body lowest, weapon tip at the ground |
| 10 | follow HOLD | 90 | second pause after the hit |
| 11–15 | recover → step back → settle → ready | 60 each, last 80 | ease back into the rest pose |

Rules behind the numbers: slow in (anticipation 3–4 frames + hold), 1–2 very fast strike frames, a hold after
impact, then a calm recovery. Last frame = first frame so it loops. Walk: 8 frames × 95 ms (contact, down,
passing, up, ×2).

## Lessons from the owner's earlier game (C:\AppServ\www\game_E-Sport, Codex built-in imagegen)
Codex drew in-game animation sheets there that shipped (Gale walk 8 directions × 4 frames, 5 action sheets of
32 frames; Hawk 8-frame walk). What made them work:
- **Draw a whole animation as ONE sheet** (e.g. 4 columns × 2 rows = 8 frames, read left→right, top→bottom),
  not one image per frame: identity, outfit and scale stay locked far better inside one image.
- **Describe every frame's pose explicitly**, numbered (1 CONTACT: …, 2 DOWN: …). A vague "walk cycle" came back
  as 12 near-identical strides; a first Hawk walk led with the same leg in frames 1 and 5.
- **Near/far limb shading rule**: the limb nearer the viewer is a slightly lighter shade and is drawn over the
  far limb, which is darker. Saying this explicitly fixed the left/right leg mix-ups.
- **Fix with a targeted edit of the same sheet** ("keep everything, change ONLY the legs …"), not a new sheet.
- **Cutout parts sheet**: Codex also drew a 3×3 sheet of separate body parts (upper body, thighs, shins, boots)
  with rounded overlapping joint ends, drawn complete including the hidden overlap. This is the model for our
  layered outfit parts (Prompt G5).
- Leave generous gutters; Claude's packer finds the real empty gutter, trims each figure, applies ONE shared scale
  to every frame and puts the planted foot on a fixed pivot. Don't try to align frames yourself.
- At game size small drift barely shows (there ~24–33 px; ours 48 px), but face, hair and outfit shape must not
  change between frames.

## What the video tests taught about poses
- The motion the owner liked most (MiniMax H3): big wind-up with the body leaning back, a lunge forward on the
  strike, and a clear return to the starting pose.
- Outfits changed mid-motion in every video model (mantle → hood, cape vanished). In hand-drawn frames, keep
  every outfit part the same shape from frame to frame; only rotate or shift it with the body.
- Exaggerate: at 48 px on screen, small pose changes are invisible. Change the silhouette between key poses.
