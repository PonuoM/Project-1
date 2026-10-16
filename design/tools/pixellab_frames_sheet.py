"""Contact sheet + timed GIF + 1x strip for generated frames, using the pose spec's frame timing. No network.

Usage: python -I design/tools/pixellab_frames_sheet.py SPEC.pose.json FRAMES_DIR [--prefix frame] [--skeleton]
Writes FRAMES_DIR/sheet.png, FRAMES_DIR/play.gif and FRAMES_DIR/strip.png, and prints per-frame bbox/feet rows.
--skeleton draws the requested skeleton over each frame (checks whether the model followed the pose).
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument('spec', type=Path)
ap.add_argument('dir', type=Path)
ap.add_argument('--prefix', default='frame')
ap.add_argument('--skeleton', action='store_true')
ap.add_argument('--zoom', type=int, default=4)
a = ap.parse_args()
spec = json.loads(a.spec.read_text(encoding='utf-8'))
kp = json.loads(Path(str(a.spec.with_suffix('')) + '.keypoints.json').read_text(encoding='utf-8'))
files = sorted(a.dir.glob(f'{a.prefix}-*.png'))
frames = [Image.open(f).convert('RGBA') for f in files]
ms = [f.get('ms', 60) for f in spec['frames']]
Z = a.zoom
W, H = frames[0].size
BG = (236, 233, 226, 255)
BONES = [('NECK', 'RIGHT SHOULDER'), ('NECK', 'LEFT SHOULDER'), ('RIGHT SHOULDER', 'RIGHT ELBOW'), ('RIGHT ELBOW', 'RIGHT ARM'),
         ('LEFT SHOULDER', 'LEFT ELBOW'), ('LEFT ELBOW', 'LEFT ARM'), ('RIGHT HIP', 'RIGHT KNEE'), ('RIGHT KNEE', 'RIGHT LEG'),
         ('LEFT HIP', 'LEFT KNEE'), ('LEFT KNEE', 'LEFT LEG'), ('RIGHT HIP', 'LEFT HIP'), ('NECK', 'RIGHT HIP'), ('NECK', 'LEFT HIP')]


def tile(i, im):
    t = Image.new('RGBA', (W, H), BG)
    t.alpha_composite(im)
    t = t.resize((W * Z, H * Z), Image.NEAREST)
    d = ImageDraw.Draw(t)
    if a.skeleton and i < len(kp['keypoints']):
        p = {k['label']: (k['x'] * W * Z, k['y'] * H * Z) for k in kp['keypoints'][i]}
        for u, v in BONES:
            d.line([p[u], p[v]], fill=(220, 60, 50, 255) if 'LEFT' in u + v and 'RIGHT' not in u + v else (40, 110, 220, 255), width=1)
    note = spec['frames'][i].get('note', '') if i < len(spec['frames']) else ''
    d.text((3, 2), f'{i} {note} {ms[i] if i < len(ms) else ""}ms', fill=(20, 20, 20, 255))
    return t


tiles = [tile(i, im) for i, im in enumerate(frames)]
cols = 5
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new('RGBA', (cols * W * Z, rows * H * Z), (255, 255, 255, 255))
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * W * Z, (i // cols) * H * Z))
sheet.save(a.dir / ('sheet-skeleton.png' if a.skeleton else 'sheet.png'))
plain = []
for im in frames:
    t = Image.new('RGBA', (W, H), BG)
    t.alpha_composite(im)
    plain.append(t.resize((W * Z, H * Z), Image.NEAREST).convert('P', palette=Image.ADAPTIVE))
plain[0].save(a.dir / 'play.gif', save_all=True, append_images=plain[1:], duration=ms[:len(plain)], loop=0, disposal=2)
strip = Image.new('RGBA', (W * len(frames), H), (0, 0, 0, 0))
for i, im in enumerate(frames):
    strip.paste(im, (i * W, 0))
strip.save(a.dir / 'strip.png')
for i, im in enumerate(frames):
    al = im.split()[3].point(lambda v: 255 if v > 0 else 0)
    bb = al.getbbox()
    print(i, 'bbox', bb, 'colours', len(set(px for px in im.getdata() if px[3])))
