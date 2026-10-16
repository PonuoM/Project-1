"""Cut an AI weapon sheet (N x N cells on chroma green) into native pixel-art weapon-layer sprites. No network.

Usage: python -I design/tools/weapons_from_sheet.py SHEET.(png|jpg) OUT_DIR --names a,b,c,... [--grid 4] [--period 8.2]
  --period   sheet pixels per art pixel (estimate it first; Gemini's 1024px sheet = ~8.2)
For every cell: key out saturated green, rebuild the grid (median of each art pixel's centre, JPEG-safe),
cluster the colours into one shared palette, drop specks, then find the weapon's long axis. The handle end is
the end lower on screen (the sheet draws weapons pointing up-right); the grip sits a per-type fraction along it.
Writes OUT_DIR/<name>.png + <name>.json ({grip, angle, length}, same format weapon_layer.py reads) and preview.png.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

src, out = Path(sys.argv[1]), Path(sys.argv[2])
o = dict(zip(sys.argv[3::2], sys.argv[4::2]))
names = o['--names'].split(',')
G = int(o.get('--grid', 4))
P = float(o.get('--period', 8.2))
# grip position along the weapon, measured from the handle end (fraction of length)
GRIP = {'spear': .32, 'halberd': .32, 'staff': .32, 'scythe': .3, 'wand': .15}
a = np.array(Image.open(src).convert('RGB')).astype(float)
H, W = a.shape[:2]
cw, ch = W / G, H / G
out.mkdir(parents=True, exist_ok=True)


def keyed(blk):
    return ~((blk[..., 1] - np.maximum(blk[..., 0], blk[..., 2]) > 50) & (blk[..., 1] > 100))


cells = []
for n, name in enumerate(names):
    cx0, cy0 = (n % G) * cw, (n // G) * ch
    cell = a[int(cy0):int(cy0 + ch), int(cx0):int(cx0 + cw)]
    fg = keyed(cell)
    # grid phase: column/row offsets where colour edges line up best with the period
    ex = (np.abs(np.diff(cell, axis=1)).sum(2) * fg[:, 1:]).sum(0)
    ey = (np.abs(np.diff(cell, axis=0)).sum(2) * fg[1:, :]).sum(1)
    phx = max(np.arange(0, P, .25), key=lambda ph: ex[np.arange(ph, len(ex) - 1, P).round().astype(int)].mean())
    phy = max(np.arange(0, P, .25), key=lambda ph: ey[np.arange(ph, len(ey) - 1, P).round().astype(int)].mean())
    nx, ny = int((cell.shape[1] - phx) / P), int((cell.shape[0] - phy) / P)
    px = np.zeros((ny, nx, 4), float)
    for j in range(ny):
        for i in range(nx):
            x0, y0 = phx + 1 + i * P, phy + 1 + j * P
            xs, xe, ys, ye = int(x0 + P * .25), int(x0 + P * .75), int(y0 + P * .25), int(y0 + P * .75)
            blk, f = cell[ys:ye, xs:xe].reshape(-1, 3), fg[ys:ye, xs:xe].reshape(-1)
            if len(f) and f.mean() > .5:
                px[j, i, :3] = np.median(blk[f], 0)
                px[j, i, 3] = 255
    cells.append(px)

# shared palette: greedy merge of near colours across all weapons (JPEG noise -> a few clean ramps)
cols = np.concatenate([c[c[:, :, 3] > 0][:, :3] for c in cells])
pal = []
for c in cols:
    for k, (s, m) in enumerate(pal):
        if np.abs(s / m - c).max() < 22:
            pal[k] = (s + c, m + 1); break
    else:
        pal.append((c.copy(), 1))
pal = np.array([s / m for s, m in pal if m >= 3])
# JPEG blends outlines with the green screen: weapons carry no green, so green-tinted entries are fringe
fringe = (pal[:, 1] > pal[:, 0] + 12) & (pal[:, 1] > pal[:, 2] + 12)
meta_all, previews = [], []
for name, px in zip(names, cells):
    op = px[:, :, 3] > 0
    d = np.abs(px[:, :, None, :3] - pal[None, None]).sum(3)
    px[:, :, :3] = pal[d.argmin(2)]
    px[op & fringe[d.argmin(2)]] = 0
    op = px[:, :, 3] > 0
    im = px.astype(np.uint8)
    # despeckle: keep the largest 8-connected component only (the weapon)
    Hh, Ww = op.shape
    lab = np.zeros(op.shape, int); best, cur = (0, 0), 0
    for y in range(Hh):
        for x in range(Ww):
            if op[y, x] and not lab[y, x]:
                cur += 1; stack = [(y, x)]; lab[y, x] = cur; size = 0
                while stack:
                    yy, xx = stack.pop(); size += 1
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            y2, x2 = yy + dy, xx + dx
                            if 0 <= y2 < Hh and 0 <= x2 < Ww and op[y2, x2] and not lab[y2, x2]:
                                lab[y2, x2] = cur; stack.append((y2, x2))
                if size > best[1]:
                    best = (cur, size)
    im[lab != best[0]] = 0
    ys, xs = np.nonzero(im[:, :, 3])
    im = im[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    ys, xs = np.nonzero(im[:, :, 3])
    pts = np.stack([xs, ys], 1).astype(float)
    mean = pts.mean(0)
    axis = np.linalg.svd(pts - mean)[2][0]
    proj = (pts - mean) @ axis
    e1, e2 = mean + axis * proj.min(), mean + axis * proj.max()
    if abs(e1[1] - e2[1]) < .3 * abs(e1[0] - e2[0]):            # lying flat: handle is the left end (sheet points right)
        handle, tip = (e1, e2) if e1[0] < e2[0] else (e2, e1)
    else:
        handle, tip = (e1, e2) if e1[1] > e2[1] else (e2, e1)  # diagonal/upright: handle = lower end on screen
    L = float(np.hypot(*(tip - handle)))
    grip = handle + (tip - handle) * GRIP.get(name, .12)
    angle = math.degrees(math.atan2(tip[1] - handle[1], tip[0] - handle[0]))
    Image.fromarray(im).save(out / f'{name}.png')
    meta = {'grip': [round(float(grip[0]), 2), round(float(grip[1]), 2)], 'angle': round(angle, 1), 'length': round(L, 1),
            'source': str(src), 'note': 'weapons_from_sheet.py: grid rebuilt from the AI sheet; grip = fraction along the long axis from the handle end'}
    (out / f'{name}.json').write_text(json.dumps(meta, indent=1), encoding='utf-8')
    meta_all.append((name, im, meta))
Z = 6
cellpx = max(max(m[1].shape[:2]) for m in meta_all) + 4
sheet = Image.new('RGB', (G * cellpx * Z, ((len(meta_all) + G - 1) // G) * cellpx * Z), (236, 233, 226))
from PIL import ImageDraw
dr = ImageDraw.Draw(sheet)
for n, (name, im, meta) in enumerate(meta_all):
    t = Image.new('RGBA', (cellpx, cellpx), (236, 233, 226, 255))
    t.alpha_composite(Image.fromarray(im), (2, 2))
    t = t.resize((cellpx * Z, cellpx * Z), Image.NEAREST).convert('RGB')
    x0, y0 = (n % G) * cellpx * Z, (n // G) * cellpx * Z
    sheet.paste(t, (x0, y0))
    gx, gy = (meta['grip'][0] + 2.5) * Z + x0, (meta['grip'][1] + 2.5) * Z + y0
    dr.ellipse([gx - 5, gy - 5, gx + 5, gy + 5], outline=(220, 40, 40), width=2)
    dr.text((x0 + 4, y0 + 4), f"{name} L{meta['length']:.0f}", fill=(20, 20, 20))
sheet.save(out / 'preview.png')
print(json.dumps({'palette': len(pal), 'weapons': {m[0]: [m[1].shape[1], m[1].shape[0], m[2]['length']] for m in meta_all}}))
