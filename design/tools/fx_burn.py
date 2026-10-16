"""Smoother element-on-weapon demo. Expands the attack into 40 ms ticks so the effect runs at 25 fps on its own
clock (as it will in the game), adds a particle trail along the blade and plays the hit burst frame by frame.
No network.

usage: fx_burn.py STRIP.png PICK.json FX_DIR ELEMENT OUT_PREFIX [--onto SWAPPED_STRIP] [--hit-x 112 --ground 79]
Writes OUT_PREFIX.png (strip, one frame per tick) and OUT_PREFIX.json (viewer spec).
Particles: every tick each blade spawns ~6 particles at random blade pixels; a particle lives 4 ticks, rises 1 px per
tick (fire/poison) or falls (ice) or jitters (lightning), and fades through light -> mid -> dark.
"""
import argparse, json, random
import numpy as np
from PIL import Image
from scipy import ndimage

RAMPS = {
    'fire': ((150, 40, 20), (240, 110, 30), (255, 225, 120), (255, 140, 40), -1),
    'ice': ((40, 90, 160), (110, 190, 240), (225, 248, 255), (140, 220, 255), 1),
    'poison': ((40, 110, 30), (110, 210, 60), (210, 255, 150), (120, 230, 60), -1),
    'lightning': ((170, 130, 20), (250, 220, 70), (255, 255, 200), (255, 240, 110), 0),
}
TICK = 40


def violet(a):
    r, g, b = [a[..., i].astype(float) for i in range(3)]
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b)
    return (a[..., 3] > 0) & (b == mx) & (mx > 90) & ((mx - mn) > 0.45 * mx) & (r > g)


def paste(dst, spr, cx, bottom):
    h, w = spr.shape[:2]; x0, y0 = int(cx - w / 2), int(bottom - h)
    ys, xs = np.nonzero(spr[..., 3])
    for yy, xx in zip(ys, xs):
        if 0 <= y0 + yy < dst.shape[0] and 0 <= x0 + xx < dst.shape[1]:
            dst[y0 + yy, x0 + xx] = spr[yy, xx]


def main():
    ap = argparse.ArgumentParser()
    for n in ('strip', 'pick', 'fx', 'element', 'out'): ap.add_argument(n)
    ap.add_argument('--onto'); ap.add_argument('--hit-x', type=int, default=112); ap.add_argument('--ground', type=int, default=79)
    o = ap.parse_args(); random.seed(7)
    pick = json.load(open(o.pick)); fw = pick['frameWidth']; impact = pick.get('impactFrame', 0)
    dark, mid, light, glow, drift = RAMPS[o.element]
    ids = [f['sourceFrame'] for f in json.load(open(f'{o.fx}/{o.element}/pick-burst.json'))['frames']]
    burst = [np.array(Image.open(f'{o.fx}/{o.element}/frames/frame-{i:02d}.png').convert('RGBA')) for i in ids]
    burst = [b for b in burst if (b[..., 3] > 0).sum() > 12]          # drop the tiny seed dots
    src = np.array(Image.open(o.strip).convert('RGBA'))
    dst = np.array(Image.open(o.onto).convert('RGBA')) if o.onto else src
    ticks, specs, parts = [], [], []
    hit_tick = None
    for k, fr in enumerate(pick['frames']):
        a0 = src[:, k * fw:(k + 1) * fw]; base = dst[:, k * fw:(k + 1) * fw].copy(); m = violet(a0)
        lab, n = ndimage.label(m, structure=np.ones((3, 3))); blade = np.zeros_like(m); smear = np.zeros_like(m)
        for j in range(1, n + 1):
            p = lab == j; ys, xs = np.nonzero(p)
            (smear if p.sum() / max(1, max(np.ptp(xs), np.ptp(ys)) + 1) > 3.2 else blade)[...] |= p
        if not o.onto:                                                   # recolour the violet weapon
            v = a0[..., :3].max(-1) / 255.0
            base[blade & (v > 0.85)] = (*light, 255); base[blade & (v > 0.6) & (v <= 0.85)] = (*mid, 255); base[blade & (v <= 0.6)] = (*dark, 255)
        base[smear] = (*mid, 255); base[smear & (a0[..., :3].max(-1) > 200)] = (*light, 255)
        if k == impact: hit_tick = len(ticks)
        bys, bxs = np.nonzero(blade | smear)
        for t in range(max(1, round(fr['ms'] / TICK))):
            a = base.copy()
            ring = ndimage.binary_dilation(blade, iterations=1) & ~blade & (a[..., 3] == 0); a[ring] = (*glow, 150)
            if len(bxs):
                for _ in range(6 if smear.any() is False else 9):
                    q = random.randrange(len(bxs)); parts.append([bxs[q] + random.uniform(-0.5, 0.5), bys[q], 0])
            alive = []
            for p in parts:
                age = p[2]; col = light if age < 1 else mid if age < 3 else dark
                x = int(round(p[0] + (random.choice((-1, 0, 1)) if drift == 0 else 0))); y = int(round(p[1]))
                if 0 <= y < a.shape[0] and 0 <= x < a.shape[1]: a[y, x] = (*col, 255)
                p[1] += drift if drift else 0; p[2] += 1
                if p[2] < 4: alive.append(p)
            parts = alive
            if hit_tick is not None and len(ticks) - hit_tick < len(burst):
                paste(a, burst[len(ticks) - hit_tick], o.hit_x, o.ground)
            ticks.append(a); specs.append({'note': fr.get('note', ''), 'ms': TICK, 'sourceFrame': k})
    Image.fromarray(np.concatenate(ticks, 1)).save(o.out + '.png')
    json.dump({'about': f'{o.element} on weapon, 25 fps ticks', 'frameWidth': fw, 'impactFrame': hit_tick or 0, 'frames': specs},
              open(o.out + '.json', 'w', encoding='utf8'), indent=1)
    print('ok', o.element, len(ticks), 'ticks')


if __name__ == '__main__':
    main()
