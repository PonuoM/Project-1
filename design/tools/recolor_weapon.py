"""Weapon tiers by palette swap: recolour only the blade's colours in every frame of a clip. No network.

Usage: python -I design/tools/recolor_weapon.py STRIP.png OUT.png --weapon-ref WITH.png --base-ref WITHOUT.png --ramp fire
  Blade colours = colours in WITH.png (reference holding the weapon in its own colours, e.g. the steel-blade pixen edit)
  that never appear in WITHOUT.png (the same character with the original blade). Pick blade colours that the
  outfit never uses, otherwise the outfit would be recoloured too. Colours are matched dark-to-light onto the ramp.
  --ramp fire | ice | gold | "#hex,#hex,..." (dark -> light)
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

RAMPS = {
    'fire': ['#3a0d0a', '#7a1a10', '#c2361a', '#ef6a1f', '#ffb13b', '#ffe9a6'],
    'ice': ['#0e1f3a', '#1f4f7a', '#3d8fc0', '#7cc8e8', '#c4f0ff', '#f4feff'],
    'gold': ['#3a2408', '#7a4e12', '#b9821f', '#e8b53c', '#f9dc7a', '#fff6cf'],
}
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
o = dict(zip(sys.argv[3::2], sys.argv[4::2]))
ramp = RAMPS.get(o['--ramp']) or o['--ramp'].split(',')
ramp = np.array([[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in ramp], float)
with_ = np.array(Image.open(o['--weapon-ref']).convert('RGBA'))
base = np.array(Image.open(o['--base-ref']).convert('RGBA'))
cols = {tuple(p[:3]) for p in with_.reshape(-1, 4) if p[3]} - {tuple(p[:3]) for p in base.reshape(-1, 4) if p[3]}
# metal only: low-saturation colours (pixen also re-shades the grip/guard slightly; those must keep their colour)
# Dark blade greys are skipped too: palette-locked video frames reuse them for hair/boot outlines, and a dark
# outline on a recoloured blade still reads fine. --min-lum sets the cut (default 70).
L = lambda c: .299 * c[0] + .587 * c[1] + .114 * c[2]
cols = sorted((c for c in cols if max(c) - min(c) < 40 and L(c) >= float(o.get('--min-lum', 70))), key=L)
lum = np.array([.299 * c[0] + .587 * c[1] + .114 * c[2] for c in cols])
t = (lum - lum.min()) / max(1, lum.max() - lum.min())          # 0 = darkest blade colour, 1 = brightest
# light steel greys cover most of the blade: land them on the ramp's mid/upper tones, keep its lightest tone for
# the brightest highlight only (otherwise every tier looks white at the impact frame)
pos = lambda x: .15 + .65 * x if x < .999 else 1.0
mapping = {c: tuple(int(v) for v in ramp[int(round(pos(x) * (len(ramp) - 1)))]) for c, x in zip(cols, t)}
a = np.array(Image.open(src).convert('RGBA'))
out = a.copy()
for c, n in mapping.items():
    m = (a[:, :, 3] > 0) & (a[:, :, 0] == c[0]) & (a[:, :, 1] == c[1]) & (a[:, :, 2] == c[2])
    out[m, :3] = n
Image.fromarray(out).save(dst)
print({'bladeColours': len(cols), 'ramp': o['--ramp']})
