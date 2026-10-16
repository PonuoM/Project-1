from pathlib import Path
from PIL import Image
import json, hashlib

D=Path(__file__).parent
r=json.loads((D/'verification-g8b-v3.json').read_text())
names={'kiki':('กีกี้','Kiki','swarm / ฝูง'), 'thornboar':('หมูป่าหนาม','Thornboar','charger / พุ่งชน'), 'hex-scarecrow':('หุ่นไล่กาสาป','Hex Scarecrow','ranged / ระยะไกล'), 'bridge-troll':('ยักษ์ใต้สะพาน','Bridge Troll','tank / ถึก')}
lines=['','## G8b revision — 2026-10-15: small-size readability','',
 'This section supersedes only the four small G8 v2 recommendations. Grimfang-v2 and Thunderhead-v2 remain approved. Earlier sections and files are retained. Agent: Codex (GPT-6), built-in image_gen; exact image model ID not exposed. Exact prompts: `prompts-g8b-v3.json`.','',
 'New sources were explicitly requested as tiny 48×48 / 64×64 sprites at 8× zoom, with broad flat clusters, enlarged heads and no texture. Each exported sprite permits at most 12 colours including background and outline. Native pixels are enlarged exactly 8×.','',
 '| Recommended file | Canvas | Height in art px | Width in art px | Colours incl. background | 2×2 eye squares |','|---|---|---|---|---|---|']
for m in r['monsters']: lines.append(f"| {m['file']} | {m['size'][0]}×{m['size'][1]} | {m['heightArtPx']} | {m['widthArtPx']} | {m['colorCount']} | {m['eye2x2Squares']} |")
lines+=['','Background `#00B140`; warm outline `#2e1816`. Facing left, physically held weapons, two empty native rows below feet and at least two on every other side. Eye colours are flat bright blocks without a glow halo.','']
for m in r['monsters']:
 th,en,role=names[m['id']]
 lines += [f'### {th} / {en} — v3','',f'Role: {role}. Height {m["heightArtPx"]} art px; ground row {m["groundRow"]} (zero-based).','',
 '| Material | Shadow | Midtone | Highlight |','|---|---|---|---|']
 for mat,cols in m['palette'].items():
  if len(cols)==3: lines.append('| '+mat+' | '+' | '.join('`'+c+'`' for c in cols)+' |')
  else: lines.append('| '+mat+' | `'+cols[0]+'` (flat bright eye) | — | — |')
 lines+=['','Animation moves retain the idle-walk, attack and hurt-death instructions in the original G8 entry above. Preserve the new simple clusters and face at all times.','']
lines+=['### Readability review','',
 'The two requested lineups contain exactly: hero, Kiki-v3, Thornboar-v3, Hex Scarecrow-v3, Bridge Troll-v3, Grimfang-v2. They share native scale and bottom alignment. Thunderhead is deliberately excluded from G8b lineups.','',
 f"- `lineup-1x-v3.png`: {r['lineupNativeSize'][0]}×{r['lineupNativeSize'][1]}, true native size.",
 f"- `lineup-v3.png`: {r['lineupSize'][0]}×{r['lineupSize'][1]}, exactly 8×.",
 f"- `silhouettes-1x-v3.png`: {r['silhouetteNativeSize'][0]}×{r['silhouetteNativeSize'][1]}, four silhouettes on green.",
 '- `silhouettes-v3.png`: the same silhouette strip at 8×.','',
 'Silhouette cues: Kiki has projecting ears, horns and a forward knife; Thornboar is low and quadrupedal with large tusks and a thorn crest; Scarecrow is tall and thin with a raised crow-bearing arm; Troll is broad and squat with a club and large underbite. Colour cues: blue-grey / charcoal with bright green / pale yellow with purple-black crow / moss green with grey club.','',
 'No boss sprite was modified. The approved Grimfang is composited read-only into the new comparison. New material ramps are recorded above; every used export colour is restricted to the chosen palette. Native-frame visual review and any deviations are recorded in notes.md.']
with (D/'monsters.md').open('a',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
files=[]
for p in sorted(D.glob('*v3.png')):
 with Image.open(p) as im:files.append(dict(file=p.name,size=list(im.size),format=im.format))
inventory=D/'files-g8b-v3.json'; assert not inventory.exists()
inventory.write_text(json.dumps(files,indent=2)+'\n',encoding='utf-8')
with (D/'notes.md').open('a',encoding='utf-8') as f:
 f.write('\n### G8b saved PNG files\n\n')
 for row in files:f.write(f"- `{row['file']}` — {row['size'][0]}×{row['size'][1]}, {row['format']}.\n")
 f.write('\nRecommended: the four named `*-v3.png` sprites, lineup-v3.png and lineup-1x-v3.png. Every imagegen source is retained as *-raw-v3.png. Prompts: prompts-g8b-v3.json; exporter: export-g8b-v3.py; measurements: verification-g8b-v3.json.\n')
print(json.dumps(files,indent=2))
