"""Element demo: put an element (fire/ice/poison/lightning) on a character's attack strip. No network.
usage: fx_compose.py STRIP.png PICK.json FX_DIR ELEMENT OUT.png [--hit-x 112 --ground 78]
Layers per frame, using the violet weapon-ID pixels of the strip:
  1 weapon: blade recoloured to the element ramp; the wide swing smear becomes a bright element trail
  2 aura: 1-px glow ring around the blade + a small looping element sprite (status loop, half size) at the blade tip
  3 hit: from the impact frame on, the element burst plays at (hit-x, ground)
FX_DIR/<element>/frames/frame-NN.png (+ pick-burst.json / pick-loop.json) come from fx_from_video.py.
"""
import argparse, json
import numpy as np
from PIL import Image
from scipy import ndimage

RAMPS = {  # dark, mid, light, glow
    'fire': ((150, 40, 20), (240, 110, 30), (255, 225, 120), (255, 140, 40)),
    'ice': ((40, 90, 160), (110, 190, 240), (225, 248, 255), (140, 220, 255)),
    'poison': ((40, 110, 30), (110, 210, 60), (210, 255, 150), (120, 230, 60)),
    'lightning': ((170, 130, 20), (250, 220, 70), (255, 255, 200), (255, 240, 110)),
}


def violet(a):
    r, g, b = [a[..., i].astype(float) for i in range(3)]
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b)
    return (a[..., 3] > 0) & (b == mx) & (mx > 90) & ((mx - mn) > 0.45 * mx) & (r > g)


def paste(dst, spr, cx, bottom):
    h, w = spr.shape[:2]; x0, y0 = int(cx - w / 2), int(bottom - h)
    for yy in range(h):
        for xx in range(w):
            if spr[yy, xx, 3] and 0 <= y0 + yy < dst.shape[0] and 0 <= x0 + xx < dst.shape[1]:
                dst[y0 + yy, x0 + xx] = spr[yy, xx]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('strip'); ap.add_argument('pick'); ap.add_argument('fx'); ap.add_argument('element'); ap.add_argument('out')
    ap.add_argument('--onto', help='draw the aura sprite and hit burst onto this strip (e.g. a weapon_swap result) instead of recolouring the violet blade')
    ap.add_argument('--hit-x', type=int, default=112); ap.add_argument('--ground', type=int, default=78)
    o = ap.parse_args()
    pick = json.load(open(o.pick)); fw = pick['frameWidth']; impact = pick.get('impactFrame', 0)
    dark, mid, light, glow = RAMPS[o.element]
    def fxframes(kind):
        ids = [f['sourceFrame'] for f in json.load(open(f'{o.fx}/{o.element}/pick-{kind}.json'))['frames']]
        return [np.array(Image.open(f'{o.fx}/{o.element}/frames/frame-{i:02d}.png').convert('RGBA')) for i in ids]
    burst, loop = fxframes('burst'), fxframes('loop')
    small = [np.array(Image.fromarray(f).resize((max(1, f.shape[1] // 2), max(1, f.shape[0] // 2)), Image.NEAREST)) for f in loop]
    src = np.array(Image.open(o.strip).convert('RGBA')); out = np.array(Image.open(o.onto).convert('RGBA')) if o.onto else src.copy()
    for k in range(src.shape[1] // fw):
        a = src[:, k * fw:(k + 1) * fw].copy(); m = violet(a)
        if o.onto: base = out[:, k * fw:(k + 1) * fw].copy()
        lab, n = ndimage.label(m, structure=np.ones((3, 3)))
        blade = np.zeros_like(m); tip = None
        for j in range(1, n + 1):
            part = lab == j; ys, xs = np.nonzero(part)
            width = part.sum() / max(1, max(np.ptp(xs), np.ptp(ys)) + 1)
            v = a[..., :3].max(-1) / 255.0
            if width > 3.2:   # swing smear -> element trail
                a[part & (v > 0.8)] = (*light, 255); a[part & (v <= 0.8)] = (*mid, 255)
            else:
                blade |= part
                a[part & (v > 0.85)] = (*light, 255); a[part & (v > 0.6) & (v <= 0.85)] = (*mid, 255); a[part & (v <= 0.6)] = (*dark, 255)
                far = np.argmax(xs - ys * 0.3); tip = (xs[far], ys[far])
        if o.onto: a = base                        # keep the swapped weapon, only add the element layers
        if blade.any() and not o.onto:   # glow ring
            ring = ndimage.binary_dilation(blade, iterations=1) & ~blade & (a[..., 3] == 0)
            a[ring] = (*glow, 150)
        if tip is not None:
            paste(a, small[k % len(small)], tip[0], tip[1] + 2)
        if k >= impact and k - impact < len(burst):
            paste(a, burst[min(len(burst) - 1, (k - impact) * 2)], o.hit_x, o.ground)
        elif k >= impact:
            paste(a, loop[(k - impact) % len(loop)], o.hit_x, o.ground)
        out[:, k * fw:(k + 1) * fw] = a
    Image.fromarray(out).save(o.out); print('ok', o.element)


if __name__ == '__main__':
    main()
