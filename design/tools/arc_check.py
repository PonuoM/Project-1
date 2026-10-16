"""Render each Mara skill's hit frames with its arc the way combat-feel/index.html places it (for checking)."""
import json, sys
import numpy as np
from PIL import Image, ImageDraw
C = [(255, 246, 200), (255, 154, 46), (168, 40, 26)]
def tint(sheet, f):
    a = np.array(Image.open(f'concepts/fx-g11/codex/{sheet}-native-v3.png').convert('RGB'))[:, f * 64:(f + 1) * 64]; v = a[..., 0]
    o = np.zeros(a.shape[:2] + (4,), np.uint8)
    for m, c in [(v > 200, C[0]), ((v > 110) & (v <= 200), C[1]), ((v >= 20) & (v <= 110), C[2])]: o[m, :3] = c; o[m, 3] = 255
    return Image.fromarray(o)
FILES = {'down': 'arc-down', 'rl': 'arc-sweep-rl', 'lr': 'arc-sweep-lr', 'up': 'arc-up', 'thrust': 'arc-thrust', 'spin': 'arc-spin'}
plans = json.loads(sys.argv[1])   # {move: [k, s, dx, dy]}
G = 100; rows = []
for mv, (k, s, dx, dy) in plans.items():
    spec = json.load(open(f'motion/mara/skills/{mv}/pick-fast.json')); strip = Image.open(f'motion/mara/skills/{mv}/strip-fast-blade-7.png').convert('RGBA')
    hits = [i for i, f in enumerate(spec['frames']) if f['note'] == 'HIT'][:2]
    row = Image.new('RGBA', (300 * len(hits), 130), (27, 24, 48, 255)); d = ImageDraw.Draw(row)
    for j, h in enumerate(hits):
        c = Image.new('RGBA', (300, 130), (27, 24, 48, 255)); c.alpha_composite(strip.crop((h * 128, 0, h * 128 + 128, 80)), (40, G - 79 + 10))
        sz = int(64 * s); arc = tint(FILES[k], 1).resize((sz, sz), Image.NEAREST)
        hx, hy = 40 + 62 + dx, G - 79 + 10 + 42 + dy
        c.alpha_composite(arc, (int(hx - sz * 0.1), int(hy - sz / 2)))
        row.alpha_composite(c, (j * 300, 0)); d.text((j * 300 + 4, 2), f'{mv} hit {h}', fill=(255, 255, 255))
    rows.append(row)
W = max(r.width for r in rows); out = Image.new('RGBA', (W, 130 * len(rows)), (0, 0, 0, 255))
for i, r in enumerate(rows): out.alpha_composite(r, (0, i * 130))
out.save(sys.argv[2])
