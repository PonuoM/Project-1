from pathlib import Path
from PIL import Image
import json

D=Path(__file__).parent
r=json.loads((D/'verification-v1.json').read_text())
detail={
'kiki':('กีกี้','Kiki','swarm / ฝูง',
 'Hunched small goblin with pointed ears, two short horns, a visible fang, red eye and chipped rusty knife held toward the left.',
 'Hunched breathing, knife grip stable; fast short alternating steps with a low head bob.',
 'Brief shoulder recoil, one short leftward knife jab, recover to the same grip and stance.',
 'Short backward flinch; knees buckle, collapse with the knife still held. Extract hurt from the opening frames.'),
'thornboar':('หมูป่าหนาม','Thornboar','charger / พุ่งชน',
 'Heavy four-legged boar, curved tusks lowered leftward, thorn vines across its back.',
 'Snort and chest breathing, heavy four-leg walk with alternating near/far pairs; vines remain attached.',
 'Lower head and compress legs, anticipation hold, burst left with tusks, brake and return to ready.',
 'Head jerks back, front knees fold, heavy side collapse; tusks and thorn vines keep their shapes.'),
'hex-scarecrow':('หุ่นไล่กาสาป','Hex Scarecrow','ranged / ระยะไกล',
 'Leaning straw figure with sack face, stitched mouth, orange eyes and one black crow perched on its raised arm.',
 'Small uneven torso sway, slow alternating steps; crow keeps wings folded and stays perched.',
 'Draw raised arm inward, hold, thrust it left in a casting gesture, settle. Do not generate flying crows; the game adds the flock.',
 'Bend backward on hurt, sack head dips, knees and torso crumple. Avoid detached floating straw or smoke.'),
'bridge-troll':('ยักษ์ใต้สะพาน','Bridge Troll','tank / ถึก',
 'Short broad moss-skinned troll with thick feet and a whole tree-stump club physically gripped.',
 'Heavy breathing, shoulders sink, slow weight-shifting steps. Keep stump rigid in the same hand.',
 'Lean back and raise stump, long anticipation hold, fast heavy leftward/downward smash, recoil, slow recovery.',
 'Small armored-looking torso recoil; knees fail and the heavy body falls with its attached club.'),
'grimfang':('กริมแฟง หมาป่าตัวร้าย','Grimfang, the Big Bad Wolf','city boss / บอสใหญ่เมือง 1',
 'Bipedal charcoal werewolf crouching with claws extended leftward, ragged red trophy cloak and a wolf tail.',
 'Predatory breathing in the crouch, short bent-knee bipedal stalking steps; do not become a quadruped.',
 'Coil shoulders, hold, fast forward claw rake, weighty recovery back to the crouch. Keep each claw thick and readable.',
 'Shoulder flinch with feet planted; stagger, drop to knees then collapse. Cape follows body without changing design.'),
'thunderhead':('ยักษ์ต้นถั่ว ธันเดอร์เฮด','Thunderhead, the Beanstalk Giant','World Boss',
 'Whole giant body with leather armor, steel chains and a physically gripped uprooted beanstalk-tree club.',
 'Very slow chest breathing, shifting weight, ponderous steps; club, pods and roots retain their identities.',
 'Shift weight backward, wind up the beanstalk club, hold, fast broad leftward smash, long heavy recovery.',
 'Heavy shoulder recoil, stagger and knee drop, whole body falls. Keep the full body inside the animation input before runtime cropping.')}

lines=['# G8 — City 1 monsters and World Boss','',
 'Source: `design/world/BESTIARY-v1.md` (2026-10-15), City 1 and World Boss. Agent: Codex (GPT-6); built-in image_gen.', '',
 'Recommended: all six `*-v1.png` exports. Each native art pixel is exactly 8×8 image pixels. All face left. All share flat `#00B140` and outline `#2e1816`; no `#7a3cff`. Heights below include the entire occupied silhouette (headwear, perched bird and held weapon as applicable), measured from final pixels.', '',
 '| File | Canvas | Measured height | Measured width | Ground row (0-based art px) |',
 '|---|---|---|---|---|']
for m in r['monsters']:
 lines.append(f"| {m['file']} | {m['size'][0]}×{m['size'][1]} | {m['heightArtPx']} | {m['widthArtPx']} | {m['groundRow']} |")
lines+=['',f"Lineup: `lineup-v1.png` ({r['lineupSize'][0]}×{r['lineupSize'][1]}), left to right: hero, Kiki, Thornboar, Hex Scarecrow, Bridge Troll, Grimfang, Thunderhead. Every figure uses the same 8× scale and its bottommost occupied pixel shares one ground row. Hero occupied height is {r['heroHeightArtPx']} art px in the supplied reference; original canvas is 64×64.",'',
 'Animation handoff: ordinary monsters need three clips each: idle-walk, attack, hurt-death. Bosses need four each, adding special. Total: 20 planned clips; none generated in G8. Fixed monster weapons stay drawn on the body. Projectiles, summoned creatures, shockwaves and other VFX are separate game effects. Use a clear anticipation, fast strike, follow-through hold and calm recovery. Idle-walk returns to the same start pose; hurt-death ends fallen and does not loop. Camera stays fixed, without zoom, floor or shadows. Near limbs are lighter and overlap darker far limbs.','']
for m in r['monsters']:
 th,en,role,look,idle,attack,death=detail[m['id']]
 lines += [f'## {th} / {en}','',f'Role: {role}. Height as drawn: {m["heightArtPx"]} art px. Recommended: `{m["file"]}`.','',look,'',
 '| Material | Shadow | Midtone | Highlight |','|---|---|---|---|']
 for mat,cols in m['materials'].items(): lines.append('| '+mat+' | '+' | '.join('`'+c+'`' for c in cols)+' |')
 lines+=['','Three allowed shades per material; small materials can use fewer shades at native scale. Shared outline is additional. Bright eye colours are solid pixels, without a halo. Pixel counts by exact hex are in `verification-v1.json`.','',
 '- **Idle-walk:** '+idle,'- **Attack:** '+attack,'- **Hurt-death:** '+death]
 if m['id']=='grimfang': lines+=['- **Special — howl and pounce:** plant feet, raise muzzle and howl, sink low, leap left and land with a two-claw pounce. Kiki summons are added by the game and must not be baked into the clip.']
 if m['id']=='thunderhead': lines+=['- **Special — stomp and club:** lift one boot, hold, stamp down, then wind up and slam the beanstalk club. The shockwave is added by the game; do not draw a wave or ground cracks into the source animation.']
 lines+=['']
lines+=['## Integration notes','',
 'These are start-frame designs, not sprite strips. The full-body World Boss source intentionally differs from the upper-body-only runtime presentation described in the bestiary: G8 explicitly requests the whole body. Claude can frame it when preparing MiniMax inputs. Do not use a generic chroma-green threshold on moss or beanstalk pixels after export; key the exact RGB background.','',
 'No runtime manifests or game-loaded assets were edited. Claude owns owner review, MiniMax framing, motion generation, final pixel cleanup and integration.']
p=D/'monsters.md'; assert not p.exists(); p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
files=[]
for p in sorted(D.glob('*.png')):
 with Image.open(p) as im: files.append({'file':p.name,'size':list(im.size),'format':im.format})
p=D/'files-v1.json'; assert not p.exists(); p.write_text(json.dumps(files,indent=2)+'\n',encoding='utf-8')
with (D/'notes.md').open('a',encoding='utf-8') as f:
 f.write('\n## Final saved-file inventory\n\n')
 for row in files: f.write(f"- `{row['file']}` — {row['size'][0]}×{row['size'][1]}, {row['format']}.\n")
 f.write('\nRecommended: all six named `*-v1.png` exports and `lineup-v1.png`; `*-raw-v1.png` retain every generated source. Exact prompts: prompts-v1.json. Materials and animation moves: monsters.md. Pixel-level measurements: verification-v1.json.\n')
print(json.dumps(files,indent=2))
