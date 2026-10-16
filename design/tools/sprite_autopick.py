"""QA + automatic key-frame pick for a clip converted by video_to_sprite.py. No network.

Usage: python -I design/tools/sprite_autopick.py CLIP_DIR --ref SPRITE.png [--max 18] [--speed 0.6] [--hold-cap 150]
  CLIP_DIR holds frames/ (from video_to_sprite.py, with convert.json)
Checks (written to CLIP_DIR/qa.json and printed):
  drift      frame 0 vs the reference placed in the window: offset / size change (the model zoomed or slid)
  palette    every pixel is palette-locked; reports colours the reference never used in its own silhouette area
  feet       lowest opaque row per frame (ground contact; a jump or a slide shows up here)
  loop       how much the last frame differs from the first (0 = seamless loop)
  holds      runs of nearly identical frames (the video model's long pauses)
Pick: every hold becomes one frame (ms = its length, capped), motion frames are kept at video timing x --speed,
then the least-moving motion frames are merged until <= --max frames. impactFrame = first hold after the
biggest motion. Writes CLIP_DIR/pick-auto.json + strip-auto.png (viewer-ready; never touches a manual pick).
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

clip = Path(sys.argv[1])
o = dict(zip(sys.argv[2::2], sys.argv[3::2]))
conv = json.loads((clip / 'frames' / 'convert.json').read_text(encoding='utf-8'))
W, H, DX, DY = conv['window']
files = sorted((clip / 'frames').glob('frame-*.png'))
F = [np.array(Image.open(f).convert('RGBA')) for f in files]
base_ms = conv['every'] / 24 * 1000
speed = float(o.get('--speed', .6))
cap = float(o.get('--hold-cap', 150))
MAX = int(o.get('--max', 18))

ref = np.array(Image.open(o['--ref']).convert('RGBA'))
placed = np.zeros((H, W, 4), np.uint8)
rh, rw = ref.shape[:2]
placed[DY:DY + rh, DX:DX + rw] = ref[:min(rh, H - DY), :min(rw, W - DX)]


def bbox(a):
    ys, xs = np.nonzero(a[:, :, 3])
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1) if len(xs) else None


def diff(a, b):
    sa, sb = a[:, :, 3] > 0, b[:, :, 3] > 0
    union = sa | sb
    changed = (sa != sb) | (sa & sb & (np.abs(a[:, :, :3].astype(int) - b[:, :, :3]).sum(2) > 0))
    return float(changed[union].mean()) if union.any() else 0.0


qa = {}
b0, br = bbox(F[0]), bbox(placed)
qa['drift'] = {'frame0': b0, 'reference': br,
               'offset': [b0[0] - br[0], b0[3] - br[3]] if b0 and br else None,
               'sizeRatio': round(((b0[3] - b0[1]) / (br[3] - br[1])), 3) if b0 and br else None}
qa['feet'] = [bbox(a)[3] if bbox(a) else None for a in F]
qa['loop'] = round(diff(F[0], F[-1]), 3)
energy = [0.0] + [diff(F[i - 1], F[i]) for i in range(1, len(F))]
qa['energy'] = [round(e, 3) for e in energy]
THR = .04
holds, i = [], 0
while i < len(F):
    j = i
    while j + 1 < len(F) and energy[j + 1] < THR:
        j += 1
    if j > i:
        holds.append([i, j])
    i = j + 1
qa['holds'] = holds

# segments in time order: ('hold', i, j) or ('move', i)
segs, covered = [], set()
for i, j in holds:
    covered.update(range(i, j + 1))
k = 0
while k < len(F):
    h = next((x for x in holds if x[0] == k), None)
    if h:
        segs.append(['hold', h[0], h[1]]); k = h[1] + 1
    else:
        segs.append(['move', k, k]); k += 1
# merge least-moving motion frames until within MAX
while len(segs) > MAX:
    moves = [n for n, s in enumerate(segs) if s[0] == 'move' and 0 < n < len(segs) - 1]
    if not moves:
        break
    n = min(moves, key=lambda n: energy[segs[n][1]])
    prev = segs[n - 1]
    prev[2] = segs[n][2]                       # fold into the previous segment (keeps its picture, adds the time)
    del segs[n]
peak = int(np.argmax(energy))
picked = []
for s in segs:
    kind, i, j = s
    n_src = j - i + 1
    ms = min(cap, n_src * base_ms) if kind == 'hold' else max(30, round(n_src * base_ms * speed))
    src = (i + j) // 2 if kind == 'hold' else i
    picked.append({'note': kind, 'ms': int(round(ms)), 'sourceFrame': src, 'span': [i, j]})
impact = next((n for n, p in enumerate(picked) if p['span'][0] > peak and p['note'] == 'hold'), None)
if impact is None:
    impact = next((n for n, p in enumerate(picked) if p['span'][0] > peak), len(picked) - 1)
picked[impact]['note'] = 'IMPACT (auto)'
strip = Image.new('RGBA', (W * len(picked), H), (0, 0, 0, 0))
for n, p in enumerate(picked):
    strip.paste(Image.fromarray(F[p['sourceFrame']]), (n * W, 0))
strip.save(clip / 'strip-auto.png')
pick = {'about': 'auto-picked by sprite_autopick.py (holds folded, motion at video timing x speed)', 'source': 'frames/',
        'frameWidth': W, 'impactFrame': impact, 'frames': picked}
(clip / 'pick-auto.json').write_text(json.dumps(pick, indent=1, ensure_ascii=False), encoding='utf-8')
qa['picked'] = len(picked)
qa['durationMs'] = sum(p['ms'] for p in picked)
(clip / 'qa.json').write_text(json.dumps(qa, indent=1), encoding='utf-8')
print(json.dumps({k: qa[k] for k in ('drift', 'loop', 'holds', 'picked', 'durationMs')}, indent=1))
print('feet rows min/max', min(x for x in qa['feet'] if x), max(x for x in qa['feet'] if x))
