# G8 — City 1 monsters and World Boss

Source: `design/world/BESTIARY-v1.md` (2026-10-15), City 1 and World Boss. Agent: Codex (GPT-6); built-in image_gen.

Recommended: all six `*-v2.png` exports. Each native art pixel is exactly 8×8 image pixels. All face left. All share flat `#00B140` and outline `#2e1816`; no `#7a3cff`. Heights below include the entire occupied silhouette (headwear, perched bird and held weapon as applicable), measured from final pixels.

| File | Canvas | Measured height | Measured width | Ground row (0-based art px) |
|---|---|---|---|---|
| kiki-v2.png | 384×384 | 28 | 29 | 45 |
| thornboar-v2.png | 384×384 | 30 | 40 | 45 |
| hex-scarecrow-v2.png | 384×384 | 40 | 29 | 45 |
| bridge-troll-v2.png | 512×512 | 44 | 55 | 61 |
| grimfang-v2.png | 1024×1024 | 96 | 101 | 125 |
| thunderhead-v2.png | 1280×1280 | 146 | 147 | 157 |

Lineup: `lineup-v1.png` (3960×1216), left to right: hero, Kiki, Thornboar, Hex Scarecrow, Bridge Troll, Grimfang, Thunderhead. Every figure uses the same 8× scale and its bottommost occupied pixel shares one ground row. Hero occupied height is 50 art px in the supplied reference; original canvas is 64×64.

Animation handoff: ordinary monsters need three clips each: idle-walk, attack, hurt-death. Bosses need four each, adding special. Total: 20 planned clips; none generated in G8. Fixed monster weapons stay drawn on the body. Projectiles, summoned creatures, shockwaves and other VFX are separate game effects. Use a clear anticipation, fast strike, follow-through hold and calm recovery. Idle-walk returns to the same start pose; hurt-death ends fallen and does not loop. Camera stays fixed, without zoom, floor or shadows. Near limbs are lighter and overlap darker far limbs.

## กีกี้ / Kiki

Role: swarm / ฝูง. Height as drawn: 28 art px. Recommended: `kiki-v2.png`.

Hunched small goblin with pointed ears, two short horns, a visible fang, red eye and chipped rusty knife held toward the left.

| Material | Shadow | Midtone | Highlight |
|---|---|---|---|
| olive | `#50502b` | `#858344` | `#b6ad63` |
| hide | `#49362c` | `#79503a` | `#aa7652` |
| cloth | `#542b27` | `#914437` | `#c16c4c` |
| steel | `#42434a` | `#777a7b` | `#b0b5ad` |
| bone | `#8e7a57` | `#c2b38e` | `#f0dfb6` |
| red | `#641f2a` | `#a5323a` | `#df5050` |

Three allowed shades per material; small materials can use fewer shades at native scale. Shared outline is additional. Bright eye colours are solid pixels, without a halo. Pixel counts by exact hex are in `verification-v2.json`.

- **Idle-walk:** Hunched breathing, knife grip stable; fast short alternating steps with a low head bob.
- **Attack:** Brief shoulder recoil, one short leftward knife jab, recover to the same grip and stance.
- **Hurt-death:** Short backward flinch; knees buckle, collapse with the knife still held. Extract hurt from the opening frames.

## หมูป่าหนาม / Thornboar

Role: charger / พุ่งชน. Height as drawn: 30 art px. Recommended: `thornboar-v2.png`.

Heavy four-legged boar, curved tusks lowered leftward, thorn vines across its back.

| Material | Shadow | Midtone | Highlight |
|---|---|---|---|
| hide | `#49362c` | `#79503a` | `#aa7652` |
| moss | `#35432b` | `#657445` | `#96a363` |
| bone | `#8e7a57` | `#c2b38e` | `#f0dfb6` |
| amber | `#a35c16` | `#e4a32a` | `#ffe067` |

Three allowed shades per material; small materials can use fewer shades at native scale. Shared outline is additional. Bright eye colours are solid pixels, without a halo. Pixel counts by exact hex are in `verification-v2.json`.

- **Idle-walk:** Snort and chest breathing, heavy four-leg walk with alternating near/far pairs; vines remain attached.
- **Attack:** Lower head and compress legs, anticipation hold, burst left with tusks, brake and return to ready.
- **Hurt-death:** Head jerks back, front knees fold, heavy side collapse; tusks and thorn vines keep their shapes.

## หุ่นไล่กาสาป / Hex Scarecrow

Role: ranged / ระยะไกล. Height as drawn: 40 art px. Recommended: `hex-scarecrow-v2.png`.

Leaning straw figure with sack face, stitched mouth, orange eyes and one black crow perched on its raised arm.

| Material | Shadow | Midtone | Highlight |
|---|---|---|---|
| sack | `#6c513a` | `#a08058` | `#d1b080` |
| cloth | `#542b27` | `#914437` | `#c16c4c` |
| straw | `#755b32` | `#ae8b48` | `#dfbc6b` |
| crow | `#25252e` | `#41434d` | `#626676` |
| orange | `#ad3b18` | `#ec781c` | `#ffd05a` |

Three allowed shades per material; small materials can use fewer shades at native scale. Shared outline is additional. Bright eye colours are solid pixels, without a halo. Pixel counts by exact hex are in `verification-v2.json`.

- **Idle-walk:** Small uneven torso sway, slow alternating steps; crow keeps wings folded and stays perched.
- **Attack:** Draw raised arm inward, hold, thrust it left in a casting gesture, settle. Do not generate flying crows; the game adds the flock.
- **Hurt-death:** Bend backward on hurt, sack head dips, knees and torso crumple. Avoid detached floating straw or smoke.

## ยักษ์ใต้สะพาน / Bridge Troll

Role: tank / ถึก. Height as drawn: 44 art px. Recommended: `bridge-troll-v2.png`.

Short broad moss-skinned troll with thick feet and a whole tree-stump club physically gripped.

| Material | Shadow | Midtone | Highlight |
|---|---|---|---|
| moss | `#35432b` | `#657445` | `#96a363` |
| steel | `#42434a` | `#777a7b` | `#b0b5ad` |
| leather | `#4b3029` | `#80503b` | `#b27c51` |
| bark | `#44332a` | `#70503b` | `#a17a4b` |
| bone | `#8e7a57` | `#c2b38e` | `#f0dfb6` |
| amber | `#a35c16` | `#e4a32a` | `#ffe067` |

Three allowed shades per material; small materials can use fewer shades at native scale. Shared outline is additional. Bright eye colours are solid pixels, without a halo. Pixel counts by exact hex are in `verification-v2.json`.

- **Idle-walk:** Heavy breathing, shoulders sink, slow weight-shifting steps. Keep stump rigid in the same hand.
- **Attack:** Lean back and raise stump, long anticipation hold, fast heavy leftward/downward smash, recoil, slow recovery.
- **Hurt-death:** Small armored-looking torso recoil; knees fail and the heavy body falls with its attached club.

## กริมแฟง หมาป่าตัวร้าย / Grimfang, the Big Bad Wolf

Role: city boss / บอสใหญ่เมือง 1. Height as drawn: 96 art px. Recommended: `grimfang-v2.png`.

Bipedal charcoal werewolf crouching with claws extended leftward, ragged red trophy cloak and a wolf tail.

| Material | Shadow | Midtone | Highlight |
|---|---|---|---|
| fur | `#30303b` | `#515460` | `#81848a` |
| red | `#641f2a` | `#a5323a` | `#df5050` |
| bone | `#8e7a57` | `#c2b38e` | `#f0dfb6` |

Three allowed shades per material; small materials can use fewer shades at native scale. Shared outline is additional. Bright eye colours are solid pixels, without a halo. Pixel counts by exact hex are in `verification-v2.json`.

- **Idle-walk:** Predatory breathing in the crouch, short bent-knee bipedal stalking steps; do not become a quadruped.
- **Attack:** Coil shoulders, hold, fast forward claw rake, weighty recovery back to the crouch. Keep each claw thick and readable.
- **Hurt-death:** Shoulder flinch with feet planted; stagger, drop to knees then collapse. Cape follows body without changing design.
- **Special — howl and pounce:** plant feet, raise muzzle and howl, sink low, leap left and land with a two-claw pounce. Kiki summons are added by the game and must not be baked into the clip.

## ยักษ์ต้นถั่ว ธันเดอร์เฮด / Thunderhead, the Beanstalk Giant

Role: World Boss. Height as drawn: 146 art px. Recommended: `thunderhead-v2.png`.

Whole giant body with leather armor, steel chains and a physically gripped uprooted beanstalk-tree club.

| Material | Shadow | Midtone | Highlight |
|---|---|---|---|
| skin | `#66513f` | `#a17d57` | `#c9a875` |
| leather | `#4b3029` | `#80503b` | `#b27c51` |
| steel | `#42434a` | `#777a7b` | `#b0b5ad` |
| bark | `#44332a` | `#70503b` | `#a17a4b` |
| leaf | `#30492c` | `#567b3c` | `#91a44f` |
| bone | `#8e7a57` | `#c2b38e` | `#f0dfb6` |
| amber | `#a35c16` | `#e4a32a` | `#ffe067` |

Three allowed shades per material; small materials can use fewer shades at native scale. Shared outline is additional. Bright eye colours are solid pixels, without a halo. Pixel counts by exact hex are in `verification-v2.json`.

- **Idle-walk:** Very slow chest breathing, shifting weight, ponderous steps; club, pods and roots retain their identities.
- **Attack:** Shift weight backward, wind up the beanstalk club, hold, fast broad leftward smash, long heavy recovery.
- **Hurt-death:** Heavy shoulder recoil, stagger and knee drop, whole body falls. Keep the full body inside the animation input before runtime cropping.
- **Special — stomp and club:** lift one boot, hold, stamp down, then wind up and slam the beanstalk club. The shockwave is added by the game; do not draw a wave or ground cracks into the source animation.

## Integration notes

These are start-frame designs, not sprite strips. The full-body World Boss source intentionally differs from the upper-body-only runtime presentation described in the bestiary: G8 explicitly requests the whole body. Claude can frame it when preparing MiniMax inputs. Do not use a generic chroma-green threshold on moss or beanstalk pixels after export; key the exact RGB background.

No runtime manifests or game-loaded assets were edited. Claude owns owner review, MiniMax framing, motion generation, final pixel cleanup and integration.

## G8b revision — 2026-10-15: small-size readability

This section supersedes only the four small G8 v2 recommendations. Grimfang-v2 and Thunderhead-v2 remain approved. Earlier sections and files are retained. Agent: Codex (GPT-6), built-in image_gen; exact image model ID not exposed. Exact prompts: `prompts-g8b-v3.json`.

New sources were explicitly requested as tiny 48×48 / 64×64 sprites at 8× zoom, with broad flat clusters, enlarged heads and no texture. Each exported sprite permits at most 12 colours including background and outline. Native pixels are enlarged exactly 8×.

| Recommended file | Canvas | Height in art px | Width in art px | Colours incl. background | 2×2 eye squares |
|---|---|---|---|---|---|
| kiki-v3.png | 384×384 | 28 | 30 | 12 | 1 |
| thornboar-v3.png | 384×384 | 30 | 40 | 12 | 0 |
| hex-scarecrow-v3.png | 384×384 | 42 | 32 | 12 | 0 |
| bridge-troll-v3.png | 512×512 | 44 | 50 | 12 | 1 |

Background `#00B140`; warm outline `#2e1816`. Facing left, physically held weapons, two empty native rows below feet and at least two on every other side. Eye colours are flat bright blocks without a glow halo.

### กีกี้ / Kiki — v3

Role: swarm / ฝูง. Height 28 art px; ground row 45 (zero-based).

| Material | Shadow | Midtone | Highlight |
|---|---|---|---|
| skin | `#3c5268` | `#7893aa` | `#b2c8d6` |
| knife | `#8b3d21` | `#cf6b2f` | `#f5aa56` |
| cloth | `#531e2a` | `#852d39` | `#b94b50` |
| eye | `#ff393e` (flat bright eye) | — | — |

Animation moves retain the idle-walk, attack and hurt-death instructions in the original G8 entry above. Preserve the new simple clusters and face at all times.

### หมูป่าหนาม / Thornboar — v3

Role: charger / พุ่งชน. Height 30 art px; ground row 45 (zero-based).

| Material | Shadow | Midtone | Highlight |
|---|---|---|---|
| fur | `#20212a` | `#343743` | `#505562` |
| tusks | `#948b71` | `#d8cfac` | `#fff0c9` |
| vines | `#12672b` | `#45c52d` | `#a1ed45` |
| eye | `#ffe447` (flat bright eye) | — | — |

Animation moves retain the idle-walk, attack and hurt-death instructions in the original G8 entry above. Preserve the new simple clusters and face at all times.

### หุ่นไล่กาสาป / Hex Scarecrow — v3

Role: ranged / ระยะไกล. Height 42 art px; ground row 45 (zero-based).

| Material | Shadow | Midtone | Highlight |
|---|---|---|---|
| straw | `#a58a43` | `#dcc16b` | `#fff0ac` |
| rags | `#272530` | `#46404c` | `#655b68` |
| crow | `#211d32` | `#403352` | `#655075` |
| eye | `#ff8d2c` (flat bright eye) | — | — |

Animation moves retain the idle-walk, attack and hurt-death instructions in the original G8 entry above. Preserve the new simple clusters and face at all times.

### ยักษ์ใต้สะพาน / Bridge Troll — v3

Role: tank / ถึก. Height 44 art px; ground row 61 (zero-based).

| Material | Shadow | Midtone | Highlight |
|---|---|---|---|
| skin | `#385339` | `#6f9252` | `#a8bc75` |
| club | `#525963` | `#939c9e` | `#dbe1da` |
| tusks | `#b6bba7` | `#e4e5d3` | `#fffdf0` |
| eye | `#ffe25a` (flat bright eye) | — | — |

Animation moves retain the idle-walk, attack and hurt-death instructions in the original G8 entry above. Preserve the new simple clusters and face at all times.

### Readability review

The two requested lineups contain exactly: hero, Kiki-v3, Thornboar-v3, Hex Scarecrow-v3, Bridge Troll-v3, Grimfang-v2. They share native scale and bottom alignment. Thunderhead is deliberately excluded from G8b lineups.

- `lineup-1x-v3.png`: 339×102, true native size.
- `lineup-v3.png`: 2712×816, exactly 8×.
- `silhouettes-1x-v3.png`: 184×50, four silhouettes on green.
- `silhouettes-v3.png`: the same silhouette strip at 8×.

Silhouette cues: Kiki has projecting ears, horns and a forward knife; Thornboar is low and quadrupedal with large tusks and a thorn crest; Scarecrow is tall and thin with a raised crow-bearing arm; Troll is broad and squat with a club and large underbite. Colour cues: blue-grey / charcoal with bright green / pale yellow with purple-black crow / moss green with grey club.

No boss sprite was modified. The approved Grimfang is composited read-only into the new comparison. New material ramps are recorded above; every used export colour is restricted to the chosen palette. Native-frame visual review and any deviations are recorded in notes.md.

### G8b final recommendations — eye correction v4

This table supersedes the v3-only recommendation above. Palettes remain exactly as recorded in the G8b material tables; all four final sprites use 12 colours including background and outline. The first export left Thornboar and Scarecrow eyes below 2×2. Their saved v3 sprites were sent back to built-in image_gen for eye-only enlargement. Both retries passed native checks. Exact edit prompts: `prompts-g8b-v4.json`.

| Final recommended sprite | Canvas | Height in art px | Eye check |
|---|---|---|---|
| `kiki-v3.png` | 384×384 | 28 | contains solid 2×2 eye block |
| `thornboar-v4.png` | 384×384 | 30 | contains solid 2×2 eye block |
| `hex-scarecrow-v4.png` | 384×384 | 42 | contains solid 2×2 eye block |
| `bridge-troll-v3.png` | 512×512 | 44 | contains solid 2×2 eye block |

Final comparison: `lineup-v4.png` (2712×816), `lineup-1x-v4.png` (339×102). These replace the v3 comparison recommendation; all requested v3 files are retained. Order remains hero / Kiki / Thornboar / Scarecrow / Troll / approved Grimfang-v2. All are shown at one native scale, bottoms aligned.

Final silhouette review: `silhouettes-1x-v4.png` (184×50) and `silhouettes-v4.png` (1472×400). Visually opened both final native strips and the 8× colour comparison. Four different silhouettes remain readable. The perched crow has a broad roughly 17×12 native-pixel silhouette including beak/tail/feet, exceeding the 8-pixel minimum. Face/head proportions are approximate, with the sack head taller than one third and Kiki ears/horns extending the head silhouette.

Known limits: the tool returned 1254×1254 PNGs despite prompts specifying a tiny logical sprite. Art was requested and generated with large simple pixel clusters, then mechanically normalized to the requested native grid and 12-colour palette. Source PNGs retain mild background variation and approximate grids; final sprites have exact flat green and exact 8×8 blocks. Some internal outline junctions are thicker than one pixel; mouth stitches and stump/stone construction are necessarily abstract. The grey troll club reads mostly as a blunt stone head and short rigid handle rather than detailed wood. Eye retries preserve the overall designs but introduce small local cluster shifts.

Grimfang-v2.png and Thunderhead-v2.png remain untouched. No runtime file, manifest, client or server was edited. No paid animation generation was run. Next step is owner/integrator review and motion generation.
