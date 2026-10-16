# Prompts for Gemini (Google Antigravity)

Gemini in Antigravity takes the same role Codex had: it designs pieces and writes files in `design/` only, and
Claude converts its images into real pixel art and connects them to PixelLab / MiniMax. Paste one prompt per task.
Gemini's images are not on a true pixel grid (same as Codex/GPT images); that is expected — Claude's tools
(`concept_to_native.py`, `video_to_sprite.py`, palette lock) rebuild the grid afterwards.

---

## Prompt G1 — 16 weapon sprites in one sheet (weapon layer + MiniMax first frames)

```text
You are working in the repository at C:\AppServ\www\Projects-1 (an idle ARPG desktop widget, chibi pixel art).

RULES (always):
- Write only inside design/. Do not edit client/, server/, design/sprites/manifest.json or any file the game loads.
- Never write API keys, tokens or passwords into any file.
- Do not modify or delete existing files; create new ones. Record what you did in the folder's notes.md.

TASK: create ONE image, design/concepts/weapons-g1/sheet.png, a 4x4 grid of 16 weapons for the hero
design/pixellab/chibi-motion/hero-ref-64.png (open it first and match its style exactly: chunky pixel art,
1-pixel dark warm outline #2e1816, flat 3-shade colour ramps, no gradients, no glow, no anti-aliasing).

Layout (critical, a script will cut it):
- Image 2048x2048 px, 16 cells of 512x512 px, plain flat chroma-key green background #00B140 everywhere
  (no grid lines, no labels, no shadows, no text).
- Draw every weapon as if each art pixel is an 8x8 block (so a 64-px-wide design fills the cell).
- Every weapon lies HORIZONTALLY and points RIGHT: grip/handle on the left, blade/head on the right.
- In every cell the centre of the grip (where a fist would hold it) is at exactly x=96, y=256 of that cell.
- Keep a clear green gap around each weapon; nothing touches a cell edge.

Weapons (cell order left-to-right, top-to-bottom; native length in art pixels in brackets):
 1 dagger [11]          2 short sword [16]       3 long sword [24]      4 greatsword [30]
 5 curved sabre [20]    6 katana [24]            7 hand axe [16]        8 battle axe [24]
 9 mace [18]           10 war hammer [24]       11 spear [34]          12 halberd [34]
13 wooden staff [30]   14 crystal wand [14]     15 scythe [30]         16 club [18]
Metal parts use cool steel greys only; wood is brown; no weapon may use the hero's ivory, moss-green or
terracotta. Simple, readable silhouettes at small size beat detail.

Also write design/concepts/weapons-g1/weapons.json: [{"cell":1,"name":"dagger","lengthPx":11}, ...] and
design/concepts/weapons-g1/notes.md (model used, prompt, anything you could not follow exactly).
```

What Claude does with it: cut the 16 cells, rebuild each on a true 8-px grid, find each grip, save them as
weapon-layer sprites (`design/pixellab/chibi-motion/weapons/`), and make MiniMax first frames per weapon type.

---

## Prompt G1b — redo of G1 with the permanent rules in /GEMINI.md

Result of G1 (14 Oct): good drawing, but not saved in the repo, JPEG 1024 instead of PNG, weapons ~1.7× longer
than asked. `/GEMINI.md` now carries those lessons permanently; this prompt also checks that Gemini read it.

```text
Read GEMINI.md in the repository root first, then reply with the 5 rules from it that matter most for this task,
in your own words, before you start.

TASK (redo of the weapon sheet): one 1024x1024 PNG, 4x4 grid (256x256 cells, 32x32 art pixels each, one art
pixel = 8x8 image pixels), chroma green #00B140, house style from GEMINI.md, every weapon on the 45-degree
diagonal with the handle at the lower-left. Match design/pixellab/chibi-motion/hero-ref-64.png.

Lengths are strict, in art pixels from the end of the handle to the tip (the hero is ~50 art px tall):
 1 dagger 9         2 short sword 14    3 long sword 20     4 greatsword 26
 5 curved sabre 16  6 katana 20         7 hand axe 13       8 battle axe 20
 9 mace 14         10 war hammer 20    11 spear 30         12 halberd 30
13 wooden staff 26 14 crystal wand 11  15 scythe 26        16 club 15
(Last time every weapon came out about 1.7x too long — measure against the cell: a 14-art-px short sword is
only 112 image pixels long, less than half the cell width.)

Save into design/concepts/weapons-g1b/: sheet-v1.png (and -v2, -v3 if you retry), weapons.json
([{"cell":1,"name":"dagger","lengthPx":9}, ...]) and notes.md as GEMINI.md requires. List the saved files with
their sizes at the end.
```

---

## Prompt G2 — three outfit sets on the same hero (input for the animation videos)

Each image becomes the first/last frame of an animation video (Flow Veo / MiniMax H3), so the hero, pose, size
and placement must match the reference exactly; only the clothes change. Works for Codex or Gemini (AGENTS.md).

```text
Read AGENTS.md first and follow it (start/finish entries in design/AGENT_LOG.md).

TASK G2: three outfit sets for the hero, one image each.
Input: design/concepts/outfits-g2/input/hero-steel-x8-green.png (512x512 = the 64x64 hero sprite scaled 8x on
#00B140). Treat it as a tracing template: keep the head, teal bob hair, face, hands, feet, pose, the steel short
sword (same hand, same angle) and the exact position/size of everything. Change ONLY the clothing (and boots).

Sets:
 A plate-knight: dark steel plate chest armour with shoulder pauldrons, short crimson cape, dark armoured boots
 B mage: deep-blue hooded robe with gold trim reaching the knees, soft brown boots, hood DOWN so the hair shows
 C ranger: brown leather jerkin with a dark-grey scarf, belt with pouches, brown leather boots
No violet #7a3cff anywhere. Same chunky style as the template: one art pixel = 8x8 image pixels, 1-px dark
outline #2e1816, flat 3-shade ramps, no anti-aliasing, flat #00B140 background, nothing else in the picture.

Save into design/concepts/outfits-g2/ as set-a-v1.png, set-b-v1.png, set-c-v1.png (512x512 PNG; keep any retries
as -v2, -v3), plus notes.md. At the end list the saved files with sizes and say which ones keep the pose best.
```

---

## Prompt G4 — outfit concepts for the 3 launch classes (step 1 of "agents make the sprites")

Owner's decision (14 Oct): Codex and Gemini draw the sprites. Step 1 = outfit concepts; motion comes after the
owner picks concepts (then `design/MOTION_GUIDE.md` applies). Outfits are built from separate layer parts
(brief: hat, armour, gloves, boots, weapon, off-hand), so each concept must already be designed as parts.

```text
Read AGENTS.md first and follow it (start/finish entries in design/AGENT_LOG.md).

TASK G4: outfit concepts for the 3 launch classes of Idle Loot: melee (warrior), mage, archer.
Each class gets 3 tiers: T1 starter (simple cloth/leather), T2 mid (recognisable class gear), T3 endgame
(rare and impressive, but still readable at 48 px on screen). That is 9 outfits.

Input template: design/concepts/outfits-g4/input/hero-nosword-x8-green.png (512x512 = the 64x64 hero scaled 8x on
#00B140, empty hands). Every outfit is drawn on this template: keep the head, teal bob hair, face, hands, feet,
pose, size and position exactly; change only clothing. No weapons, no off-hand items (they are separate layers).

Each outfit is made of these layer parts, and must look right when parts are mixed with other outfits:
 - hat/helmet (optional for T1): sits on the head, must leave the face and eye visible
 - chest (torso + sleeves; a cape, robe skirt or mantle belongs to this part)
 - gloves (only the hands/forearms; same hand silhouette as the template, at most 1 art px bigger)
 - boots (only the feet/shins; same footprint as the template)
Keep the body outline within 2 art px of the template except for capes, pauldrons, hats and robe skirts.

Style: house style from AGENTS.md (one art pixel = 8x8 image pixels, 1-px outline #2e1816, flat 3-shade ramps, no
anti-aliasing, flat #00B140 background, nothing else in the picture). Do not reuse the hero's current ivory
mantle / moss-green tunic / terracotta sash colours. No violet #7a3cff. Each class needs its own main colour
family so the three classes are easy to tell apart, and tiers within a class get richer (more trim, metal, gems).

Make ONE image per outfit (image models drift on big multi-outfit sheets). Save into design/concepts/outfits-g4/:
 melee-t1-v1.png, melee-t2-v1.png, melee-t3-v1.png, mage-t1-v1.png ... archer-t3-v1.png (512x512 PNG each;
 retries as -v2, -v3), and concepts.md with, per outfit: name, one-line fantasy, the parts it has, the hex colour
 ramp of each material (3 shades), and which parts are drawn behind the hair or behind the body (capes, hoods).
Plus notes.md as AGENTS.md requires. At the end list the saved files with sizes and name your best version of each.
```

What Claude does with it: a contact sheet of all 9 for the owner, a check that head/hands/feet still match the
template, and a mix-and-match test of parts across outfits. After the owner picks, the next prompt (G5) splits the
chosen outfits into separate part sprites, and then motion frames follow `design/MOTION_GUIDE.md`.

---

## Prompt G4a — base body for motion videos (bodysuit hero + violet placeholder sword)

Owner's plan (14 Oct): generate ONE video per motion with an undressed base body (MiniMax H3, green screen), cut
it into frames, then dress those frames with outfits. A plain tight bodysuit instead of bare skin: it keeps the
body readable, separates cleanly from skin, and video models don't blur or refuse it. The violet sword is a
placeholder so the arms swing with real weight; Claude finds the violet pixels in every frame to get the hand
position and blade angle, then swaps in the real weapon layer.

```text
Read AGENTS.md first and follow it (start/finish entries in design/AGENT_LOG.md).

TASK G4a: two base-body images of the hero for animation videos.
Input template: design/concepts/outfits-g4/input/hero-nosword-x8-green.png (512x512, 64x64 hero scaled 8x).
Keep the head, teal bob hair, face, hands, feet, pose, size and position exactly as in the template.
Replace ALL clothing (mantle, tunic, sash, boots) with one plain tight-fitting mid-grey bodysuit covering neck to
wrists and ankles, with simple dark-grey flat shoes. 3 shades of grey only, no seams, no folds, no logos, no belt.
The body silhouette under the suit must look like a slim chibi body, so later outfits can be drawn over it.

 1 base-body-v1.png: as above, empty hands.
 2 base-body-sword-v1.png: same as 1, plus a plain short sword (blade + guard + grip) held in the same hand and at
   the same angle as the steel sword in design/concepts/outfits-g2/input/hero-steel-x8-green.png, ENTIRE sword
   flat saturated violet #7a3cff (2 shades max: #7a3cff and #5a24c8), no other colour on it.

House style from AGENTS.md (8x8 art pixels, 1-px outline #2e1816, flat ramps, no anti-aliasing, flat #00B140
background). No violet anywhere except the sword. Save both into design/concepts/base-g4a/ (512x512 PNG,
retries -v2, -v3) with notes.md. List the saved files with sizes at the end.
```

What Claude does with it: snap to the exact grid, copy the original head/hand pixels back, then one MiniMax H3
video per motion (first frame = last frame), frame extraction, and the violet-blade tracking.

---

## Prompt G5 — character roster concepts (fixed characters, no outfit swapping)

Owner's decision (14 Oct): no swappable clothing. Each playable character has one fixed look, like a hero roster.
World mood the owner loves: a classic storybook high-fantasy world in the spirit of Final Fantasy IX (airships,
misty kingdoms, cosy medieval towns, theatre troupes, many races living together), but fully ORIGINAL. Sprite feel
from a modern pixel roster: every character a different, instantly readable silhouette.

```text
Read AGENTS.md first and follow it (start/finish entries in design/AGENT_LOG.md).
For this task the hero colour reservations in AGENTS.md do NOT apply (these are new characters); everything else does.

TASK G5: design the first playable character roster for Idle Loot.

WORLD (write it into the concepts): an original whimsical high-fantasy world. Floating airship routes between
misty kingdoms, clockwork-and-stone castle towns, mossy forests with spirit lights, a desert of buried giants,
travelling theatre troupes and guild halls. Many races live together: humans, small beast-folk, tailed folk,
tiny mage-folk, stone/plant folk. Tone: warm, adventurous, a little melancholy, never grimdark.
It must feel like the same kind of world as Final Fantasy IX but contain NOTHING from it: no names, no Vivi-style
pointy hat with glowing eyes in a shadow face, no rat dragoon, no monkey-tailed thief, no Moogles, no
recognisable costume, emblem or weapon from any Final Fantasy or other game.

ROSTER: 9 characters = 3 candidates for each launch class, so the owner can pick one per class:
 melee (sword/axe/hammer/spear), mage (staff/wand/book/orb), archer/ranged (bow/crossbow/sling/thrown).
Mix races across the 9 (at least 4 non-human or part-human). Every character needs:
 - a silhouette hook readable as a black shape (huge hat, cape, tail, ears, giant weapon, armour shape, hair…);
 - one main colour family different from the other candidates of the same class;
 - one signature weapon that is part of the design.

SPRITE (one image per character): side view facing RIGHT, idle-ready stance holding the weapon, whole body.
 - CHIBI, exactly the proportions of our hero (owner, 14 Oct: "keep our chibi, only change the design"):
   open design/pixellab/chibi-motion/hero-ref-64.png and design/concepts/base-claude-v1/base-body-64-x8-green.png
   (grey bodysuit version) and use that body as the template: body ~50 art px tall, the HEAD (with hair) ~28 of
   those 50 px, short arms and legs, same stance, same position. Only the design changes: hair, face details,
   clothing, hats, ears, tails, species features. Hats, ears, tails and capes may extend beyond the template.
 - Canvas 512x512 = a 64x64 sprite with every art pixel an exact 8x8 block. Feet on the template's ground line
   (art row 62). Keep 2+ art px of empty margin on every side.
 - Weapon at chibi scale and held low and forward like the template's sword: a sword ~14 art px long, a staff
   ~26, a bow ~20 tall. Never a weapon longer than the character is tall.
 - House style from AGENTS.md: flat #00B140 background, 1-px dark warm outline #2e1816, flat 3-shade ramps,
   no anti-aliasing, no glow, no floor shadow, no text.

Save into design/concepts/characters-g5/: melee-1-v1.png, melee-2-v1.png, melee-3-v1.png, mage-1-v1.png …
archer-3-v1.png (retries -v2, -v3), plus lineup-v1.png (all 9 side by side on #00B140, same scale, for the owner
to compare; 1536x1536 = 3 rows of 3 cells of 512) and characters.md with, per character: original name, race,
class, one-line personality, silhouette hook, weapon, hex palette (3 shades per material), and 3 signature move
ideas that fit the weapon (for later animation). Start characters.md with a half-page world description.
Plus notes.md as AGENTS.md requires. At the end list the saved files with sizes and name your favourite per class.
```

What Claude does next: put the lineup in front of the owner, snap the chosen three to the exact grid, then make
their moves with PixelLab animate-with-text-v3 (per-phase prompts, ~1 gen per move) or H3 video.

---

## Prompt G6 — anime key art for each roster character

Owner (14 Oct): one character = one class (10 classes). Each needs a beautiful, detailed anime illustration
(character select / profile / store art), matching its pixel sprite exactly in identity.

```text
Read AGENTS.md first and follow it (start/finish entries in design/AGENT_LOG.md). Write ONLY into
design/art/keyart-g6-codex/ (or keyart-g6-gemini/ if you are Gemini) — never into another agent's folder.
The pixel-art house style in AGENTS.md does NOT apply to this task (these are illustrations); all other rules do.

TASK G6: one anime key-art illustration per roster character, 10 images.

Identity sources (open each sprite and read its section before drawing; the illustration must be recognisably the
SAME character: same species features, hair colour and shape, face, outfit design and colours, signature weapon):
 design/concepts/characters-g5/codex/characters.md + the sprites in design/concepts/characters-g5/codex/
 design/concepts/characters-g5-expansion-codex-v1/characters.md + its sprites
Roster and file names:
 melee:  mara (melee-1-v2.png, sword) · rika (melee-brawler-v1.png, mechanical gauntlets) ·
         sella (melee-3-v1.png, hare, spear) · yara (melee-assassin-v1.png, ninja, dual daggers)
 mage:   pipra (mage-1-v1.png, coral, ring wand) · vessa (mage-2-v1.png, troupe, spellbook) ·
         noll (mage-summoner-v1.png, forest summoner, staff held mid-shaft)
 ranged: tavi (archer-1-v1.png, fox, recurve bow) · ilen (archer-2-v1.png, airship crossbow) ·
         bramble (ranged-gunner-dual-v1.png, dormouse, twin guns; the heavy laser may appear on the back)

STYLE: high-end 2D anime game key art, the quality of a premium gacha / JRPG character reveal. Normal anime
proportions (about 6-7 heads tall for humans; small folk stay small but not chibi), expressive face, clean
confident line art, cel shading with soft painterly light, rich but harmonious colour, detailed fabric, leather,
metal and fur. Dynamic full-body pose that shows the class fantasy and the weapon clearly (mid-action or a
heroic ready stance). Original designs only: nothing copied from Final Fantasy or any other game.

WORLD BACKDROP: a soft, slightly blurred scene from the character's home in our world (sky-port docks with
airships, misty forest with spirit lights, desert of buried giants, theatre-troupe wagons, coral shore, guild
town), kept behind the character so the character reads first. A gentle aura in the character's signature colour
around the weapon or hands (weapons will glow by tier in the game). No text, no logo, no UI, no frame, no watermark.

FORMAT: portrait 1024x1536 PNG per character: design/art/keyart-g6-codex/<name>-v1.png (retries -v2, -v3).
Then lineup-v1.png (all 10 small, 5x2 grid) for the owner, and notes.md as AGENTS.md requires (exact prompt per
image, which sprite/details you matched, anything that differs from the sprite and why). At the end list the
saved files with sizes and say which three you think are strongest.
```

---

## Prompt G7 — Mara's swappable sword blades (8 tiers)

Claude's `design/tools/weapon_swap.py` finds the violet blade in every animation frame (angle, base at the hand,
length) and pastes a new blade there, so one animation works for every blade. Only the BLADE is swapped; Mara's
hilt/guard stay from the animation. Aura and glow are added by the game, not drawn.

```text
Read AGENTS.md first and follow it (start/finish entries in design/AGENT_LOG.md). Write ONLY into
design/concepts/weapons-mara-g7-codex/ (or weapons-mara-g7-gemini/ if you are Gemini).

TASK G7: 8 sword BLADES for Mara (design/concepts/characters-g5/codex/melee-1-v2.png; read her section in
design/concepts/characters-g5/codex/characters.md). They replace her blade in the game, from a plain starter to a
legendary one. Same size class so they fit her slash: every blade 12-16 art px long and 2-4 art px wide.

Draw ONLY the blade (no grip, no guard, no hand): it starts where it would leave the guard.
Layout (a script will cut it): one 1024x512 PNG, 4 columns x 2 rows of 256x256 cells (each cell = 32x32 art px,
one art pixel = an exact 8x8 block). In every cell the blade lies FLAT, pointing RIGHT; its base (the end that
touches the guard) is centred on art pixel x=4, y=16 of the cell, the tip toward the right. Nothing touches a cell
edge. House style from AGENTS.md: flat #00B140 background, 1-px outline #2e1816, flat 3-shade ramps, no
anti-aliasing, NO glow, NO aura, NO sparkles (the game adds those), no violet #7a3cff, no text or labels.

Cells, left to right, top row then bottom row (tier: idea; keep each silhouette clearly different):
 1 common: worn iron straight blade, slightly chipped
 2 uncommon: polished steel blade with a fuller (centre groove)
 3 rare: sky-port sabre, gently curved, brass-tinted spine
 4 rare: broad cleaver blade, wider toward the tip
 5 epic: frost crystal blade, faceted, pale cyan
 6 epic: storm blade with a zig-zag edge, steel and electric blue
 7 legendary: ember blade, dark steel with molten orange cracks, wavy flame edge
 8 legendary: airship-captain's gilded blade, ivory-white steel with gold inlay and a small engraved crest
Colours must stay readable at 14 px: one strong main colour per blade.

Save: blades-v1.png (retries -v2, -v3), blades.json ([{"cell":1,"name":"worn iron","tier":"common","lengthPx":13,
"widthPx":2}, ...] measured in art px), and notes.md as AGENTS.md requires. List the saved files with sizes.
```

What Claude does with it: cut the 8 blades, paste each into Mara's slash with `weapon_swap.py` (sprite mode,
rotated by RotSprite to the measured angle), add the tier aura, and show all 8 in the viewer.

---

## Prompt G8 — city 1 monsters + Grimfang + World Boss (MiniMax start frames)

Design source: `design/world/BESTIARY-v1.md` (15 Oct, owner chose: classic fairy tales twisted dark, monsters
fierce from city 1). These sprites become the first frames of MiniMax H3 videos, so each one is an idle-ready pose
that already shows how the creature attacks. MiniMax credits run out around 15 Nov: speed matters, exact grid
does not (Claude snaps the images to the grid afterwards).

```text
Read AGENTS.md first and follow it (start/finish entries in design/AGENT_LOG.md). Write ONLY into
design/concepts/monsters-g8-codex/ (or monsters-g8-gemini/ if you are Gemini). Hero colour reservations in
AGENTS.md do NOT apply to monsters; never use violet #7a3cff.

TASK G8: draw the 4 monsters and the boss of city 1 plus the World Boss of Idle Loot, one sprite each.
Read design/world/BESTIARY-v1.md first: the "City 1" table and the "World Boss" row are the design brief
(names, look, attack). Open design/pixellab/chibi-motion/hero-ref-64.png for style and scale: the hero is ~50
art px tall in a 64x64 frame.

TONE: fierce and cool from the very first city (owner's choice), dark twisted fairy tale, glowing eyes, bold
readable silhouettes. Same pixel style as the hero so they live in one game: 1-px dark warm outline #2e1816,
flat 3-shade ramps, chunky shapes, no anti-aliasing, no glow halo, no blur, no floor shadow, no text.

POSE: side view facing LEFT (they walk toward the hero, who faces right), whole body, idle-ready stance that
shows the attack: Kiki holds its rusty knife, Thornboar lowers its tusks, Hex Scarecrow raises one arm with a
crow perched on it, Bridge Troll holds its tree-stump club, Grimfang crouches with claws out, Thunderhead holds
his beanstalk club. Monster weapons are drawn ON the body (they never change weapons). No projectiles, fire,
crows in flight or other effects (the game adds them). Avoid thin parts thinner than 1 art px.

SIZES (art px tall / canvas; one art pixel = an exact 8x8 block; feet on the bottom ground line with 2 art px
margin below; 2+ art px empty margin on every other side; flat #00B140 background):
 kiki            swarm    26-30 px tall  canvas 384x384   (48x48 art px)
 thornboar       charger  28-32 px tall, ~40 long  384x384
 hex-scarecrow   ranged   38-42 px tall  384x384
 bridge-troll    tank     42-46 px tall  512x512   (64x64)
 grimfang        city boss  90-100 px tall  1024x1024 (128x128)
 thunderhead     World Boss 140-150 px tall 1280x1280 (160x160); he is so big the game shows him overflowing
                 the scene, but draw the WHOLE body here

Save: kiki-v1.png, thornboar-v1.png, hex-scarecrow-v1.png, bridge-troll-v1.png, grimfang-v1.png,
thunderhead-v1.png (retries -v2, -v3), plus lineup-v1.png: all six and hero-ref-64.png side by side at the SAME
scale on #00B140, bottoms aligned, so the owner sees the sizes against the hero. Then monsters.md with, per
creature: name (TH/EN), role, height in art px as drawn, hex palette (3 shades per material), and its moves for
animation (idle-walk, attack, hurt-death; bosses also their special move from the bestiary), and notes.md as
AGENTS.md requires. At the end list the saved files with pixel sizes and name your recommended version of each.
```

What Claude does next: show the lineup to the owner, snap the chosen versions to the grid, build the
1280x720 MiniMax inputs (`design/motion/_inputs/`), and generate idle-walk / attack / hurt-death clips
(bosses: + special move) with H3. Cities 2–5, the pinnacle bosses and the guild boss follow as G9+ in the same
format.

**Result (15 Oct):** Grimfang and Thunderhead approved. The four small monsters failed at native size: their
high-detail source art turned into brown speckle when shrunk to 28–44 px (faces and the crow vanished), and three
of them share one brown hue. Redo them with G8b.

---

## Prompt G8b — redo the 4 small city-1 monsters for low resolution

Owner (15 Oct): keep them fierce, make the head bigger, give each its own main colour.

```text
Read AGENTS.md first and follow it (start/finish entries in design/AGENT_LOG.md). Write ONLY into
design/concepts/monsters-g8-codex/ (or monsters-g8-gemini/ if you are Gemini), as NEW versions (-v3, -v4 …);
never overwrite. Never use violet #7a3cff.

TASK G8b: redraw kiki, thornboar, hex-scarecrow and bridge-troll. Grimfang and Thunderhead are approved, do not
touch them. Your G8 designs were good as ideas (see *-raw-v1.png), but at the real game size (28-46 art px) the
fine detail turned into brown speckle: faces, the crow and the knife could not be read, and kiki, thornboar and
the scarecrow are all the same brown, so a mixed pack is one brown blob on a green meadow.

DESIGN FOR THE SMALL SIZE FROM THE START (do not draw big and shrink):
 - Ask the image tool for a LOW-RESOLUTION sprite that is already blocky: e.g. "a 48x48 pixel-art sprite shown
   at 8x zoom, every pixel a clearly visible square". Then export to the exact grid.
 - A few big shapes, not texture: no fur strands, no straw fibres, no wood grain, no dithering, no noise. Each
   material = one flat colour + one shadow + one highlight. At most ~12 colours per sprite.
 - BIGGER HEAD: the head is about one third of the total height, with big glowing eyes (2x2 art px or larger)
   and a clear mouth/teeth shape, so the face reads at 1x. Still fierce, not cute.
 - Silhouette test: filled in black, each of the four must be recognisable and different from the others.
 - Check your result at 1x native size (zoom out), not only at 8x.

ONE MAIN COLOUR EACH (they must be told apart instantly in a mixed pack on a green meadow):
 kiki          ash blue-grey skin, red glowing eyes, rusty-orange knife, small dark-red loincloth;
               26-30 px tall, canvas 384x384
 thornboar     near-black charcoal fur, big bright ivory tusks, BRIGHT green thorny vines on the back,
               yellow eyes; 28-32 px tall, ~40 long, canvas 384x384
 hex-scarecrow pale straw-yellow body, dark rags, big orange eyes in a sack face with a stitched grin, a
               LARGE purple-black crow (at least 8 art px) perched on the raised arm; 40-44 px tall, 384x384
 bridge-troll  flat moss-green skin, big underbite with two white tusks, pale grey stone-and-stump club;
               42-46 px tall, canvas 512x512

Everything else exactly as G8: side view facing LEFT, idle-ready attack pose, weapons drawn on the body, no
effects or projectiles, flat #00B140 background, 1-px outline #2e1816, exact 8x8 art pixels, feet on the ground
line with 2 art px margin below and 2+ art px on every other side.

Save: kiki-v3.png, thornboar-v3.png, hex-scarecrow-v3.png, bridge-troll-v3.png (retries -v4 …), lineup-v3.png
(hero-ref-64.png + the four new sprites + grimfang-v2.png, same scale, bottoms aligned) and lineup-1x-v3.png (the
same lineup at 1x native size, so the owner sees the real game size). Update monsters.md with the new palettes
(new section, keep the old one) and append to notes.md. List the saved files with pixel sizes at the end.
```

---

## Prompt G10 — world map (overhead fantasy map of the 5 cities × 4 zones)

Owner (15 Oct): wants an overhead world map like `design/world/style-ref-worldmap.png` (style reference only; it
is someone else's map, do not copy its layout, names or icons). Design: `design/world/WORLD-MAP-v1.md`.

```text
Read AGENTS.md first and follow it (start/finish entries in design/AGENT_LOG.md). Write ONLY into
design/world/worldmap-g10-codex/ (or worldmap-g10-gemini/ if you are Gemini). The pixel-art house style and the
#00B140 background rule in AGENTS.md do NOT apply to this task (it is an illustrated map); all other rules do.

TASK G10: paint the world map of Idle Loot. Read design/world/WORLD-MAP-v1.md (layout, the 5 cities, their 4
zones each, the special places) and design/world/BESTIARY-v1.md (what lives in each place). Open
design/world/style-ref-worldmap.png for the STYLE only.

STYLE: hand-painted fantasy board-game / RPG world map seen from high above at a slight angle: one continent in
a teal sea, painted mountains, forests, rivers, roads; towns and landmarks as small detailed illustrated icons;
soft parchment-like warmth, clean readable shapes. Original: copy nothing from the reference (no layout, no
names, no icons) and nothing from any other game. Bright daylight overall (the dark volcano region in the east
is the only dark area).

CONTENT (positions from WORLD-MAP-v1.md):
 - 5 clearly different regions: green meadow with a village and windmills (south-west, the start), purple-blue
   glowing mushroom forest (centre), golden desert with ruined temples (south-east), white snowy mountains with
   an ice palace (north), black castle wrapped in burning thorns on a volcano (east).
 - Each region shows its 4 zones as 4 distinct small landmarks (e.g. Windmill Farms = windmills and fields,
   Troll Bridge = a stone bridge, Wolfden Woods = dark wood with a wolf den), plus one village/camp, all linked
   by a main road that runs 1 -> 2 -> 3 -> 4 -> 5 in a zig-zag across the continent.
 - Special landmarks: a giant beanstalk piercing the clouds (centre, between regions 1 and 2), a tall stone
   tower vanishing into clouds (near region 1), a sewer gate beside the starting village, a swirling purple
   mist rift with floating island shards in the far eastern sea, a small harbour with a sailing ship on the west
   coast. Leave open sea and mist around the edges for future islands.
 - NO TEXT of any kind: no labels, no names, no compass letters, no legend, no title, no frame UI, no
   watermark. The game draws the names, stage pins and the hero marker on top in Thai/English.

FORMAT: landscape 1536x1024 PNG: worldmap-v1.png (retries -v2, -v3). Then zones.json listing the pixel centre
(x, y) of every village, every zone landmark and every special place in the final image, e.g.
{"city":1,"zone":2,"name":"Windmill Farms","x":312,"y":688} and {"special":"beanstalk","x":...,"y":...}, so the
game can place pins exactly. Plus notes.md as AGENTS.md requires. At the end list the saved files with sizes.
```

What Claude does next: show the map to the owner, check zones.json against the image, and build the in-game map
screen (pins per stage along the road, fog over cities not reached yet, hero marker).

---

## Prompt G9 — fill in the cut-off parts of Thunderhead (outpainting test)

The giant's video was cut at the top/right edge in 14 frames. Codex only paints the missing parts; Claude pastes the
original pixels back over everything that already exists, so nothing else can change.

```text
Read AGENTS.md first and follow it (start/finish entries in design/AGENT_LOG.md). Write ONLY into
design/concepts/thunderhead-fill-g9/codex/.

TASK G9: complete the cut-off parts of the giant Thunderhead in two animation sheets.
Inputs: design/concepts/thunderhead-fill-g9/input/sheet-a.png (6 frames, 3x2) and sheet-b.png (8 frames, 4x2), plus
the same sheets with red guide lines (sheet-a-cutlines.png, sheet-b-cutlines.png). In every cell the original frame
was cut off exactly at the red line along its TOP and its RIGHT side; above the top line and right of the right line
there is now empty green space.

For each cell, continue the cut-off shapes into that empty space so the character looks complete:
 - the top of the green beanstalk club (leaves, twisted stalk) where it hits the top line;
 - in sheet-b, also the giant's back, shoulder, arm and head where they hit the right line.
Rules:
 - Do NOT change any existing pixel below the top line / left of the right line. Only paint in the empty green space.
 - The new parts must connect seamlessly to the cut edge and match the existing pixel art exactly: same pixel size
   (one art pixel = 2x2 image pixels), same outline colour, same palette and shading, no anti-aliasing, no blur.
 - Keep the same frame positions and image size; flat #00B140 green everywhere else; no red lines in the output.
 - Stay consistent between neighbouring frames (the same beanstalk, the same head).
Save codex/sheet-a-v1.png and codex/sheet-b-v1.png (same pixel size as the inputs; retries -v2, -v3) and notes.md.
List the saved files with their pixel sizes at the end.
```

What Claude does with it: `design/tools/merge_fill.py` cuts each cell, keeps the original pixels wherever they
exist, takes only the new pixels outside the cut lines, and writes the completed frames back.

---

## Prompt G10 — elemental hit effects: designed keyframes (before any video)

Owner rule (15 Oct): always design the reference first, then animate. These sheets become the first frames for
H3 Max video and the style bible for every skill effect.

```text
Read AGENTS.md first and follow it (start/finish entries in design/AGENT_LOG.md). Write ONLY into
design/concepts/fx-g10/codex/. For this task the background is PURE BLACK #000000 (not green): effects are
blended additively in the game.

TASK G10: design the hit effects for the 4 elements of Idle Loot (fire, ice, poison, lightning) plus the
"explosion" support gem, as pixel-art keyframe sheets.

References (open all first):
 - design/concepts/fx-g10/ref/scale-hero-and-monster.png — our chibi hero (64 px tall sprite) and a 48 px goblin:
   effects must fit this scale and pixel size.
 - design/concepts/fx-g10/ref/lootbox-hero-combat.png — a game the owner likes: readable, punchy, short hit effects,
   bright on dark. Take the feeling, copy nothing.
 - design/concepts/fx-g10/ref/pack-fire.png, pack-ice.png, pack-electricity.png, pack-water.png, pack-earth.png,
   pack-wind.png, pack-void.png, pack-holy.png — the owner's favourite VFX style (a pixel VFX pack): every element
   has its own silhouette language (fire = curling flames and embers, ice = angular crystals and spikes,
   electricity = thin jagged bolts, water/poison = liquid splashes and waves). Small, crisp, 2-3 tones + white
   highlight. This is the target quality. Copy the design language, not the exact drawings.
 - design/concepts/fx-g10/ref/impact-1.png, impact-2.png — hit feedback: the enemy becomes a white silhouette, a thin
   ring and a few sparks; effects are short and minimal.
 - design/concepts/fx-g10/ref/our-current-hits.png — our first AI attempt. Problem: fire, poison and explosion are
   all the same round puff in different colours. Each element must have its OWN shape and motion.

Each element = one sheet, 1024x256 PNG, 4 keyframes left to right in 256x256 cells (one art pixel = 4x4 image
pixels, so a cell is 64x64 art px). The hit point is the centre-bottom of each cell, about art px (32, 52); the
enemy would stand there. Keyframes: 1 anticipation/start, 2 impact peak, 3 break-up, 4 last remains (almost gone).
 FIRE: tongues of flame flare UP around the hit point like something catching fire, licking upward, then
       shrinking into small embers that float up. Flames, never a round blast.
 ICE: a sharp crystal spike/ice block forms at the hit point, then SHATTERS: angular shards and splinters fly
      outward in straight lines, glittering, then tiny ice dust.
 POISON: thick toxic liquid SPLASHES sideways and up in arcs with big droplets, then the drops fall back down and
         leave a small bubbling puddle. Liquid, not gas.
 LIGHTNING: a jagged bolt strikes STRAIGHT DOWN from the top of the cell onto the hit point; a bright flash and
            electric sparks at the bottom; the bolt flickers once and is gone. Thin and sharp, not a puff.
 EXPLOSION (support gem, works with any element): a round blast with a clear shockwave ring and flying debris,
           then smoke wisps. Colours white/orange; it will be tinted per element in the game.
Style: chunky pixel art matching the hero, bright saturated 3-4 tone ramps per element (fire orange/yellow/red,
ice cyan/white/deep blue, poison lime/acid green/dark green, lightning white/yellow/violet edge, explosion
white/orange/grey), hard pixel edges, no anti-aliasing, no blur, no text, nothing outside its cell.

Save fire-v1.png, ice-v1.png, poison-v1.png, lightning-v1.png, explosion-v1.png (1024x256 each; retries -v2,
-v3), plus lineup-v1.png (all five stacked, 1024x1280) and notes.md. List the saved files with sizes at the end.
```

After the owner approves a sheet, Claude uses keyframe 1 as the first frame of an H3 Max video (16:9) so the motion
follows the approved design, then cuts it into pixel frames for the game.

---

## Prompt G11 — weapon slash arcs (the owner's main attack effect)

Owner reference (15 Oct, `20261015-1611-10.4235866.mp4`): the attack effect is a big crescent slash trail that
comes off the weapon, much bigger than the character, white core -> colour -> dark edge, visible for only a few
frames, with hitstop and the enemy flashing white. The same arcs serve every weapon; colour = element.

```text
Read AGENTS.md first and follow it (start/finish entries in design/AGENT_LOG.md). Write ONLY into
design/concepts/fx-g11/codex/. Background PURE BLACK #000000 (effects are tinted and blended in the game).

TASK G11: draw the slash-arc effect set for Idle Loot.
References: design/concepts/fx-g11/ref/pack-*.png (each element's slash-arc shape in the owner's favourite VFX pack, top-right and bottom-right of each page) and design/concepts/fx-g11/ref/slash-ref-1..6.png (the look the owner wants: thick crescent slash
trails, hard pixel edges, a bright white core, a coloured body and a darker outer edge, sharp tapering tips,
a few loose streak pieces breaking off) and scale-hero-and-monster.png (our hero is a 64 px chibi; arcs should be
about 1.2-1.8x the hero's height). Copy the feeling, not the exact shapes.

Draw each arc in GREYSCALE-by-role so the game can recolour it: core = pure white #FFFFFF, body = mid grey
#9A9A9A, edge = dark grey #3C3C3C. One art pixel = 4x4 image pixels, no anti-aliasing, no blur, no glow.

Sheets (each 1024x256, 4 cells of 256x256 = 64x64 art px, frames left to right: 1 thin start, 2 full arc at its
widest, 3 arc breaking up / thinning from the back end, 4 last streak pieces). The hero's hand (arc origin side) is
at the LEFT-centre of the cell, the arc sweeps toward the right where the enemy is:
 1 arc-down.png      diagonal chop from high behind the shoulder down to low in front
 2 arc-sweep-rl.png  wide flat horizontal sweep at chest height, right -> left (backhand)
 3 arc-sweep-lr.png  very wide, thick horizontal finisher, left -> right (the biggest, combo hit 3)
 4 arc-up.png        rising slash from low front up over the head
 5 arc-thrust.png    a straight spear/dagger thrust streak pointing right (a long tapered line with a burst at the tip)
 6 arc-spin.png      a full circle spin slash around the hero
Save the six sheets as -v1.png (retries -v2...), lineup-v1.png (all six stacked, 1024x1536) and notes.md. List
the saved files with their sizes.
```

Claude then maps white/grey/dark to each element's 3 colours (fire, ice, poison, lightning) and plays the arc at the
swing frame of every attack, for every weapon.

---

## Prompt G3 — weapon ID colour (later)

Same as G2 but the sword blade in saturated violet `#7a3cff` (never used by any outfit), so one animation
video can be recoloured into iron / fire / ice / gold blades afterwards.
