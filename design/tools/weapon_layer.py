"""Weapon as its own layer, driven by the pose spec (grip = weapon-hand keypoint, angle = spec 'blade'). No network.

  extract  WITH.png WITHOUT.png OUT_STEM --hand X,Y [--region x0,y0,x1,y1]
      Pixels that differ between a reference holding the weapon and the same reference without it (both from
      edit-image-pixen, so everything else is identical) = the weapon. Writes OUT_STEM.png (tight crop) and
      OUT_STEM.json (grip point in the crop, blade angle in degrees, length).
  compose  SPEC.pose.json BODY_DIR WEAPON.json OUT_DIR [--prefix frame]
      Draws the weapon on every body frame at the spec's hand position/blade angle (RotSprite rotation: Scale2x
      x3, nearest rotate, centre-sample back), redraws the fist over the grip, writes OUT_DIR/frame-NN.png.

Angles: screen degrees, 0 = pointing right (forward), 90 = down, -90 = up.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def scale2x(a):
    """EPX/Scale2x on an RGBA array (edges compared on all 4 channels)."""
    h, w = a.shape[:2]
    p = np.pad(a, ((1, 1), (1, 1), (0, 0)), mode='edge')
    B, D, F, H, E = p[:-2, 1:-1], p[1:-1, :-2], p[1:-1, 2:], p[2:, 1:-1], p[1:-1, 1:-1]
    eq = lambda x, y: (x == y).all(2)
    c = ~eq(B, H) & ~eq(D, F)
    o = np.zeros((h * 2, w * 2, 4), a.dtype)
    o[0::2, 0::2] = np.where((c & eq(D, B))[..., None], D, E)
    o[0::2, 1::2] = np.where((c & eq(B, F))[..., None], F, E)
    o[1::2, 0::2] = np.where((c & eq(D, H))[..., None], D, E)
    o[1::2, 1::2] = np.where((c & eq(H, F))[..., None], F, E)
    return o


def rotsprite(sprite, grip, deg):
    """Rotate RGBA array about grip (x, y) by deg (screen, clockwise positive). Returns (array, new_grip)."""
    S = 8
    big = scale2x(scale2x(scale2x(sprite)))
    h, w = big.shape[:2]
    gx, gy = (grip[0] + .5) * S, (grip[1] + .5) * S
    r = math.hypot(max(gx, w - gx), max(gy, h - gy))
    size = int(math.ceil(r * 2 / S)) + 2
    out = np.zeros((size, size, 4), np.uint8)
    a = math.radians(-deg)                   # inverse map
    cos, sin = math.cos(a), math.sin(a)
    c = size / 2
    ys, xs = np.mgrid[0:size, 0:size]
    # 4x4 sub-samples per output pixel. Centre-only sampling drops 1-2px blades when they turn near-horizontal;
    # here a pixel is solid when >= 30% of its sub-samples are, coloured by the solid sample nearest the centre.
    subs = sorted(((u, v) for u in (.125, .375, .625, .875) for v in (.125, .375, .625, .875)),
                  key=lambda p: (p[0] - .5) ** 2 + (p[1] - .5) ** 2)
    hits = np.zeros((size, size), int)
    for u, v in subs:
        dx, dy = (xs + u - c) * S, (ys + v - c) * S
        sx = np.floor(gx + dx * cos - dy * sin).astype(int)
        sy = np.floor(gy + dx * sin + dy * cos).astype(int)
        ok = (sx >= 0) & (sx < w) & (sy >= 0) & (sy < h)
        px = np.zeros((size, size, 4), np.uint8)
        px[ok] = big[sy[ok], sx[ok]]
        solid = px[:, :, 3] > 0
        first = solid & (out[:, :, 3] == 0)
        out[first] = px[first]
        hits += solid
    out[hits < 5] = 0
    return out, (c - .5, c - .5)


def extract(argv):
    with_p, without_p, stem = argv[0], argv[1], Path(argv[2])
    opts = dict(zip(argv[3::2], argv[4::2]))
    A = np.array(Image.open(with_p).convert('RGBA')).astype(int)
    B = np.array(Image.open(without_p).convert('RGBA')).astype(int)
    m = (A[:, :, 3] > 0) & (np.abs(A - B).sum(2) > 24)
    if '--region' in opts:
        x0, y0, x1, y1 = map(int, opts['--region'].split(','))
        r = np.zeros_like(m); r[y0:y1, x0:x1] = True; m &= r
    ys, xs = np.nonzero(m)
    hand = tuple(map(float, opts['--hand'].split(',')))
    # principal axis of the weapon pixels; the grip is the end nearest the hand
    pts = np.stack([xs, ys], 1).astype(float)
    mean = pts.mean(0)
    _, _, vt = np.linalg.svd(pts - mean)
    axis = vt[0]
    proj = (pts - mean) @ axis
    ends = [mean + axis * proj.min(), mean + axis * proj.max()]
    near, far = sorted(ends, key=lambda e: math.hypot(e[0] - hand[0], e[1] - hand[1]))
    angle = math.degrees(math.atan2(far[1] - near[1], far[0] - near[0]))
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    crop = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    crop[ys - y0, xs - x0] = A[ys, xs]
    Image.fromarray(crop).save(str(stem) + '.png')
    meta = {'grip': [round(hand[0] - x0, 2), round(hand[1] - y0, 2)], 'angle': round(angle, 1),
            'length': round(float(proj.max() - proj.min()), 1), 'source': [str(with_p), str(without_p)], 'pixels': int(m.sum())}
    Path(str(stem) + '.json').write_text(json.dumps(meta, indent=1), encoding='utf-8')
    print(json.dumps(meta))


def compose(argv):
    spec_p, body_dir, weapon_p, out_dir = Path(argv[0]), Path(argv[1]), Path(argv[2]), Path(argv[3])
    prefix = dict(zip(argv[4::2], argv[5::2])).get('--prefix', 'frame')
    spec = json.loads(spec_p.read_text(encoding='utf-8'))
    kp = json.loads(Path(str(spec_p.with_suffix('')) + '.keypoints.json').read_text(encoding='utf-8'))
    wm = json.loads(weapon_p.read_text(encoding='utf-8'))
    sprite = np.array(Image.open(weapon_p.with_suffix('.png')).convert('RGBA'))
    side = {'L': 'LEFT', 'R': 'RIGHT'}[spec.get('weaponHand', 'L')]
    out_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(body_dir.glob(f'{prefix}-*.png'))
    for i, fp in enumerate(files):
        body = np.array(Image.open(fp).convert('RGBA'))
        H, W = body.shape[:2]
        f = spec['frames'][i]
        pts = {k['label']: (k['x'] * W, k['y'] * H) for k in kp['keypoints'][i]}
        e, w = pts[f'{side} ELBOW'], pts[f'{side} ARM']
        L = math.hypot(w[0] - e[0], w[1] - e[1]) or 1
        hand = (w[0] + (w[0] - e[0]) / L * 1.2, w[1] + (w[1] - e[1]) / L * 1.2)   # fist centre, just past the wrist
        rot, g = rotsprite(sprite, wm['grip'], f.get('blade', wm['angle']) - wm['angle'])
        ox, oy = int(round(hand[0] - g[0] - .5)), int(round(hand[1] - g[1] - .5))
        layer = np.zeros_like(body)
        hh, ww = rot.shape[:2]
        sx0, sy0 = max(0, -ox), max(0, -oy)
        dx0, dy0 = max(0, ox), max(0, oy)
        cw, ch = min(ww - sx0, W - dx0), min(hh - sy0, H - dy0)
        if cw > 0 and ch > 0:
            layer[dy0:dy0 + ch, dx0:dx0 + cw] = rot[sy0:sy0 + ch, sx0:sx0 + cw]
        front = f.get('weaponFront', True)
        out = body.copy()
        wmask = layer[:, :, 3] > 0
        if front:
            out[wmask] = layer[wmask]
            # fist over the grip: body pixels within 1.6px of the hand centre
            yy, xx = np.mgrid[0:H, 0:W]
            fist = (np.hypot(xx + .5 - hand[0], yy + .5 - hand[1]) < 1.6) & (body[:, :, 3] > 0)
            out[fist] = body[fist]
        else:
            behind = wmask & (body[:, :, 3] == 0)
            out[behind] = layer[behind]
        Image.fromarray(out).save(out_dir / fp.name)
    print(json.dumps({'frames': len(files), 'out': str(out_dir)}))


if __name__ == '__main__':
    {'extract': extract, 'compose': compose}[sys.argv[1]](sys.argv[2:])
