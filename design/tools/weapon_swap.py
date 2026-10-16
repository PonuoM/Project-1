"""Swap the violet ID blade in an animation strip for another blade shape + colour + aura. No network.

usage: python design/tools/weapon_swap.py STRIP.png OUT.png --frame-width 128 --style sabre|cleaver|crystal|flame
                                          [--length 1.0] [--no-aura]
       sprite mode: --blades SHEET.png --cell N [--glow r,g,b]   (G7 sheet: 4x2 cells of 32x32 art px, 8x scale,
       blade flat pointing right, base at art px (4,16); the blade is RotSprite-rotated to the measured angle)
Per frame: the violet pixels (#7a3cff family) are the blade. A long thin violet shape is a real blade: its axis
(PCA), base (end nearest the body) and length are measured, the violet is removed (holes filled from neighbours)
and the new blade is drawn along the same axis, same base, --length x the measured length, with a 1-px dark
outline and a 3-shade ramp. A wide violet shape is the video's swing smear: it is only recoloured (it becomes the
coloured slash trail). Aura = a soft 1-px ring in the style's glow colour.
"""
import argparse
import colorsys
import math

import numpy as np
from scipy import ndimage
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from weapon_layer import rotsprite
from PIL import Image

STYLES = {
    #           dark            mid             light           glow            width profile w(t), t=0 base..1 tip, curve
    'sabre':   ((70, 76, 92),   (150, 158, 172), (225, 230, 238), (180, 220, 255), lambda t: 1.6 - 0.6 * t, 0.10),
    'cleaver': ((60, 60, 66),   (125, 128, 136), (200, 204, 212), (255, 200, 140), lambda t: 1.4 + 1.6 * t, 0.0),
    'crystal': ((30, 90, 150),  (80, 190, 230),  (210, 250, 255), (120, 230, 255), lambda t: 1.0 + 1.8 * math.sin(math.pi * min(t, .999)), 0.0),
    'flame':   ((150, 40, 20),  (235, 110, 30),  (255, 225, 120), (255, 140, 40),  lambda t: 1.8 + 0.6 * math.sin(t * 9), 0.04),
}
OUTLINE = (46, 24, 22)


def violet(a):
    r, g, b, al = [a[..., i] / 255 for i in range(4)]
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b)
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    h = np.zeros_like(mx)
    m = (mx == b) & (mx > mn)
    h[m] = (4 + (r[m] - g[m]) / (mx[m] - mn[m])) / 6
    return (al > 0.5) & m & (h > 0.68) & (h < 0.80) & (s > 0.45) & (mx > 0.35)


def fill_holes(a, mask):
    a = a.copy()
    todo = mask.copy()
    a[todo, 3] = 0
    for _ in range(4):                       # grow surrounding colours into the hole (blade over the body)
        if not todo.any():
            break
        nxt = todo.copy()
        for y, x in zip(*np.nonzero(todo)):
            best = None
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < a.shape[0] and 0 <= xx < a.shape[1] and not todo[yy, xx] and a[yy, xx, 3] > 0:
                    best = a[yy, xx]
                    break
            if best is not None:
                n = sum(1 for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))
                        if 0 <= y + dy < a.shape[0] and 0 <= x + dx < a.shape[1] and a[y + dy, x + dx, 3] > 0
                        and not todo[y + dy, x + dx])
                if n >= 2:                   # only fill pixels enclosed by the body, not the outside of the blade
                    a[y, x] = best
                nxt[y, x] = False
        todo = nxt
    return a


def draw_blade(a, base, direc, length, style, aura):
    dark, mid, light, glow, wf, curve = STYLES[style]
    perp = np.array([-direc[1], direc[0]])
    h, w = a.shape[:2]
    fill = np.zeros((h, w), bool)
    shade = np.zeros((h, w), float)
    for y in range(h):
        for x in range(w):
            p = np.array([x + .5, y + .5]) - base
            t = p @ direc / max(length, 1)
            if t < 0 or t > 1:
                continue
            off = p @ perp - curve * length * t * t
            half = wf(t) / 2 + .35
            if abs(off) <= half:
                fill[y, x] = True
                shade[y, x] = off / half
    ring = np.zeros_like(fill)
    ring[1:] |= fill[:-1]; ring[:-1] |= fill[1:]; ring[:, 1:] |= fill[:, :-1]; ring[:, :-1] |= fill[:, 1:]
    ring &= ~fill
    halo = np.zeros_like(fill)
    halo[1:] |= ring[:-1]; halo[:-1] |= ring[1:]; halo[:, 1:] |= ring[:, :-1]; halo[:, :-1] |= ring[:, 1:]
    halo &= ~fill & ~ring
    if aura:
        for y, x in zip(*np.nonzero(halo)):
            if a[y, x, 3] == 0:
                a[y, x] = (*glow, 110)
    for y, x in zip(*np.nonzero(ring)):
        a[y, x] = (*OUTLINE, 255)
    for y, x in zip(*np.nonzero(fill)):
        s = shade[y, x]
        a[y, x] = (*(light if s < -0.25 else mid if s < 0.45 else dark), 255)
    return a


def load_blade(sheet, cell):
    im = np.array(Image.open(sheet).convert('RGB'))
    col, row = (cell - 1) % 4, (cell - 1) // 4
    a = np.zeros((32, 32, 4), np.uint8)
    for y in range(32):
        for x in range(32):
            r, g, b = im[row * 256 + y * 8 + 4, col * 256 + x * 8 + 4]
            if not (g > 140 and r < 60 and b < 100):
                a[y, x] = (r, g, b, 255)
    cols = [tuple(int(v) for v in c) for c in a[a[..., 3] > 0][:, :3] if not (c[0] < 60 and c[1] < 40 and c[2] < 40)]
    uniq = sorted(set(cols), key=lambda c: -cols.count(c))[:6]
    uniq = sorted(uniq, key=lambda c: sum(c))
    ramp = (uniq[0], uniq[len(uniq) // 2], uniq[-1]) if uniq else ((70, 70, 70), (150, 150, 150), (230, 230, 230))
    return a, ramp


def paste_blade(a, blade, base, direc, glow, aura):
    deg = math.degrees(math.atan2(direc[1], direc[0]))
    rot, (gx, gy) = rotsprite(blade, (4, 16), deg)
    ox, oy = int(round(base[0] - .5 - gx)), int(round(base[1] - .5 - gy))
    h, w = a.shape[:2]
    lay = np.zeros_like(a)
    for y in range(rot.shape[0]):
        for x in range(rot.shape[1]):
            if rot[y, x, 3] and 0 <= y + oy < h and 0 <= x + ox < w:
                lay[y + oy, x + ox] = rot[y, x]
    solid = lay[..., 3] > 0
    if aura:
        ring = np.zeros_like(solid)
        ring[1:] |= solid[:-1]; ring[:-1] |= solid[1:]; ring[:, 1:] |= solid[:, :-1]; ring[:, :-1] |= solid[:, 1:]
        for y, x in zip(*np.nonzero(ring & ~solid)):
            if a[y, x, 3] == 0:
                a[y, x] = (*glow, 120)
    a[solid] = lay[solid]
    return a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('strip'); ap.add_argument('out')
    ap.add_argument('--frame-width', type=int, required=True)
    ap.add_argument('--style', choices=STYLES, default='sabre')
    ap.add_argument('--length', type=float, default=1.0)
    ap.add_argument('--no-aura', action='store_true')
    ap.add_argument('--blades'); ap.add_argument('--cell', type=int, default=1)
    ap.add_argument('--glow', default='255,255,255')
    o = ap.parse_args()
    blade = None
    if o.blades:
        blade, ramp = load_blade(o.blades, o.cell)
        glow = tuple(map(int, o.glow.split(',')))
    src = np.array(Image.open(o.strip).convert('RGBA'))
    fw = o.frame_width
    out = src.copy()
    dark, mid, light, glow = STYLES[o.style][:4]
    if blade is not None:
        dark, mid, light = ramp
        glow = tuple(map(int, o.glow.split(',')))
    for f in range(src.shape[1] // fw):
        a = src[:, f * fw:(f + 1) * fw].copy()
        allm = violet(a)
        lab, n = ndimage.label(allm, structure=np.ones((3, 3)))
        if n == 0:
            continue
        sizes = ndimage.sum(allm, lab, range(1, n + 1))
        main_id = int(np.argmax(sizes)) + 1
        for k in range(1, n + 1):            # small extra violet bits (hilt glints, split blade): recolour only
            if k == main_id:
                continue
            for y, x in zip(*np.nonzero(lab == k)):
                v = max(a[y, x, :3]) / 255
                a[y, x, :3] = light if v > 0.85 else mid if v > 0.6 else dark
        m = lab == main_id
        ys, xs = np.nonzero(m)
        if len(xs) < 3:
            out[:, f * fw:(f + 1) * fw] = a
            continue
        pts = np.stack([xs + .5, ys + .5], 1)
        c = pts.mean(0)
        u, sv, vt = np.linalg.svd(pts - c, full_matrices=False)
        direc = vt[0]
        proj = (pts - c) @ direc
        length = proj.max() - proj.min()
        width = len(xs) / max(length, 1)
        body = (a[..., 3] > 0) & ~allm
        by, bx = np.nonzero(body)
        bc = np.array([bx.mean(), by.mean()]) if len(bx) else c
        e1, e2 = c + direc * proj.min(), c + direc * proj.max()
        if np.linalg.norm(e1 - bc) > np.linalg.norm(e2 - bc):
            e1, e2 = e2, e1
        if width > 3.2:                      # swing smear: recolour into a slash trail of the style
            for y, x in zip(ys, xs):
                v = max(a[y, x, :3]) / 255
                a[y, x, :3] = light if v > 0.85 else mid if v > 0.6 else dark
        else:
            direc = (e2 - e1) / max(np.linalg.norm(e2 - e1), 1e-6)
            a = fill_holes(a, m)
            if blade is not None:
                a = paste_blade(a, blade, e1, direc, glow, not o.no_aura)
            else:
                a = draw_blade(a, e1, direc, (length + 1) * o.length, o.style, not o.no_aura)
        out[:, f * fw:(f + 1) * fw] = a
    Image.fromarray(out).save(o.out)
    print('ok', o.style)


if __name__ == '__main__':
    main()
