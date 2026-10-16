from pathlib import Path
from PIL import Image
import json

D=Path(__file__).parent
r=json.loads((D/'verification-g8b-v4.json').read_text())
assert all(m['eye2x2Squares'] and m['colorCount']<=12 for m in r['monsters'])
lines=['','### G8b final recommendations — eye correction v4','',
 'This table supersedes the v3-only recommendation above. Palettes remain exactly as recorded in the G8b material tables; all four final sprites use 12 colours including background and outline. The first export left Thornboar and Scarecrow eyes below 2×2. Their saved v3 sprites were sent back to built-in image_gen for eye-only enlargement. Both retries passed native checks. Exact edit prompts: `prompts-g8b-v4.json`.','',
 '| Final recommended sprite | Canvas | Height in art px | Eye check |','|---|---|---|---|']
for m in r['monsters']:lines.append(f"| `{m['file']}` | {m['size'][0]}×{m['size'][1]} | {m['heightArtPx']} | contains solid 2×2 eye block |")
lines+=['',
 'Final comparison: `lineup-v4.png` (2712×816), `lineup-1x-v4.png` (339×102). These replace the v3 comparison recommendation; all requested v3 files are retained. Order remains hero / Kiki / Thornboar / Scarecrow / Troll / approved Grimfang-v2. All are shown at one native scale, bottoms aligned.','',
 'Final silhouette review: `silhouettes-1x-v4.png` (184×50) and `silhouettes-v4.png` (1472×400). Visually opened both final native strips and the 8× colour comparison. Four different silhouettes remain readable. The perched crow has a broad roughly 17×12 native-pixel silhouette including beak/tail/feet, exceeding the 8-pixel minimum. Face/head proportions are approximate, with the sack head taller than one third and Kiki ears/horns extending the head silhouette.','',
 'Known limits: the tool returned 1254×1254 PNGs despite prompts specifying a tiny logical sprite. Art was requested and generated with large simple pixel clusters, then mechanically normalized to the requested native grid and 12-colour palette. Source PNGs retain mild background variation and approximate grids; final sprites have exact flat green and exact 8×8 blocks. Some internal outline junctions are thicker than one pixel; mouth stitches and stump/stone construction are necessarily abstract. The grey troll club reads mostly as a blunt stone head and short rigid handle rather than detailed wood. Eye retries preserve the overall designs but introduce small local cluster shifts.','',
 'Grimfang-v2.png and Thunderhead-v2.png remain untouched. No runtime file, manifest, client or server was edited. No paid animation generation was run. Next step is owner/integrator review and motion generation.']
with (D/'monsters.md').open('a',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')

files=[]
for p in sorted(D.glob('*.png')):
 if not any(t in p.name for t in ['-v3.png','-v4.png']):continue
 with Image.open(p) as im:files.append(dict(file=p.name,size=list(im.size),format=im.format))
fp=D/'files-g8b-v4.json';assert not fp.exists();fp.write_text(json.dumps(files,indent=2)+'\n',encoding='utf-8')
with (D/'notes.md').open('a',encoding='utf-8') as f:
 f.write('\n### G8b completion — 2026-10-15\n\nStatus: DONE. Final recommendations: **kiki-v3.png, thornboar-v4.png, hex-scarecrow-v4.png, bridge-troll-v3.png**. Final comparisons: **lineup-v4.png and lineup-1x-v4.png**. Prior v3 comparisons retained as requested.\n\n')
 f.write('Agent Codex (GPT-6); built-in image_gen, exact image model ID not exposed. Four original prompts: prompts-g8b-v3.json. Two targeted eye edits: prompts-g8b-v4.json, each references the corresponding exported v3 PNG. All six generated sources retained as lossless PNGs; no JPEG/WebP conversion. New drawings used no old detailed image as an edit target; earlier raw G8 images were opened only to understand the identities.\n\n')
 f.write('Measured final heights28/30/42/44; Thornboar width40. All four have12 total colours, exact8x8 blocks, warm outline, exact solid chroma green, no forbidden violet, >=2 empty native rows/columns above and beside, and exactly2 rows below. All four contain a solid2x2 main eye block; retry eyes are3x3. Source and final images were visually opened. True1x final lineup and true1x black silhouette strip were inspected, followed by the8x comparison. Blue-grey goblin/black boar/pale-yellow scarecrow/moss-green troll are distinct in the mixed pack. Crow is roughly17x12 native px including protrusions, visibly perched on the raised arm.\n\n')
 f.write('Limitations: generator returned1254x1254 sources rather than requested384/512, with approximate grids and some background variation; export normalizes simple generated pixel clusters. Head ratios are approximate, especially the tall sack head and horn/ear-inclusive Kiki head. Internal outline junctions can be thick. Stitches, fingertips, club construction and crow feet are simplified; grey club reads primarily stone. Eye edits introduce small cluster shifts beyond the eye. Source generation was intentionally low-detail, but this does not guarantee mathematical adherence to the requested logical canvas before export. No detailed painting was substituted.\n\n')
 f.write('Supporting files: export-g8b-v3.py, export-g8b-v4.py, verification-g8b-v3.json, verification-g8b-v4.json, document-g8b-v3.py, finish-g8b-v4.py, files-g8b-v3.json and files-g8b-v4.json. Palettes and native-height tables appended to monsters.md; prior sections retained. Approved boss PNGs unchanged. Remaining G8b work: none; owner/integrator review and motion generation follow.\n\nSaved G8b PNG inventory:\n\n')
 for row in files:f.write(f"- `{row['file']}` — {row['size'][0]}×{row['size'][1]} PNG.\n")
with (D.parents[1]/'AGENT_LOG.md').open('a',encoding='utf-8') as f:
 f.write('\n- 2026-10-15 · Codex (GPT-6; built-in image_gen) · G8b low-resolution redraw of four city1 monsters · **done** · `design/concepts/monsters-g8-codex/`: recommended `kiki-v3.png`, `thornboar-v4.png`, `hex-scarecrow-v4.png` (384x384), `bridge-troll-v3.png` (512x512); `lineup-v4.png` (2712x816), `lineup-1x-v4.png` (339x102), final silhouette strips184x50/1472x400. Requested v3 attempts/lineups and all six1254x1254 source PNGs retained. Palettes appended to monsters.md, exact prompts and verification JSONs, notes.md updated. All12 colours, heights28/30/42/44, eyes>=2x2, green/grid/margins verified; true1x and silhouette review done. Approved Grimfang/Thunderhead unchanged. Left: owner/integrator review and motion generation; no paid animation services run.\n')
print(json.dumps(files,indent=2))
