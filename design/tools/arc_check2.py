"""Check arc placement using per-frame anchors (same rule as the playtest)."""
import json, sys
import numpy as np
from PIL import Image, ImageDraw
C = [(255, 246, 200), (255, 154, 46), (168, 40, 26)]
FILES = {'down': 'arc-down', 'rl': 'arc-sweep-rl', 'lr': 'arc-sweep-lr', 'up': 'arc-up', 'thrust': 'arc-thrust', 'spin': 'arc-spin'}
def tint(k, f=1):
    a = np.array(Image.open(f'concepts/fx-g11/codex/{FILES[k]}-native-v3.png').convert('RGB'))[:, f*64:(f+1)*64]; v = a[..., 0]
    o = np.zeros(a.shape[:2] + (4,), np.uint8)
    for m, c in [(v > 200, C[0]), ((v > 110) & (v <= 200), C[1]), ((v >= 20) & (v <= 110), C[2])]: o[m, :3] = c; o[m, 3] = 255
    return Image.fromarray(o)
def place(k, s, A):
    sz = 64 * s
    if k == 'thrust': return A['line'][0] - sz * 0.08, A['line'][1] - sz / 2
    if k == 'spin':   return A['body'][0] - sz / 2, A['body'][1] - sz / 2
    return A['body'][0] - sz * 0.22, A['body'][1] - 4 - sz / 2
plans = json.load(open(sys.argv[1])); anch = json.load(open('motion/mara/anchors.json'))
src = {'slash': ('motion/mara/S01-slash-h3/strip-blade-7.png', 'motion/mara/S01-slash-h3/pick-manual.json'),
       'combo': ('motion/mara/S03-combo/chain-blade-7.png', 'motion/mara/S03-combo/chain-1-2-3.json')}
rows = []
for mv, lst in plans.items():
    strip, spec = src.get(mv, (f'motion/mara/skills/{mv[3:]}/strip-fast-blade-7.png', f'motion/mara/skills/{mv[3:]}/pick-fast.json'))
    spec = json.load(open(spec)); strip = Image.open(strip).convert('RGBA')
    hits = [i for i, f in enumerate(spec['frames']) if f['note'] in ('HIT', 'IMPACT') or f['note'].startswith('HIT')]
    row = Image.new('RGBA', (220 * 3, 120), (27, 24, 48, 255)); d = ImageDraw.Draw(row)
    for j, h in enumerate(hits[:3]):
        k, s = lst[min(j, len(lst) - 1)]
        c = Image.new('RGBA', (220, 120), (27, 24, 48, 255)); ox, oy = 40, 20
        c.alpha_composite(strip.crop((h * 128, 0, h * 128 + 128, 80)), (ox, oy))
        x, y = place(k, s, anch[mv][h]); sz = int(64 * s)
        c.alpha_composite(tint(k).resize((sz, sz), Image.NEAREST), (int(ox + x), int(oy + y)))
        row.alpha_composite(c, (j * 220, 0)); d.text((j * 220 + 3, 2), f'{mv} h{h}', fill=(255, 255, 255))
    rows.append(row)
out = Image.new('RGBA', (660, 120 * len(rows)))
for i, r in enumerate(rows): out.alpha_composite(r, (0, i * 120))
out.save(sys.argv[2])
