"""Clean converted frames of one clip: drop pieces of neighbouring creatures and specks, then crop every frame to
the union bounding box (+margin) so nothing is cut and frames stay aligned.
usage: clean_window.py FRAMES_DIR [--margin 2]
Rule per frame: keep the largest connected piece; drop any other piece that touches the left/right window edge
(that is a neighbour in a group clip) or is under 4% of the largest. Writes frames in place + frames/trim.json."""
import glob, json, sys
import numpy as np
from PIL import Image
from scipy import ndimage
d = sys.argv[1]; margin = int(sys.argv[sys.argv.index('--margin') + 1]) if '--margin' in sys.argv else 2
fs = sorted(glob.glob(f'{d}/frame-*.png')); arrs = []
for f in fs:
    a = np.array(Image.open(f).convert('RGBA')); m = a[..., 3] > 0
    lab, k = ndimage.label(m, structure=np.ones((3, 3)))
    if k > 1:
        sz = ndimage.sum(m, lab, range(1, k + 1)); big = int(np.argmax(sz)) + 1
        for j in range(1, k + 1):
            if j == big: continue
            ys, xs = np.nonzero(lab == j)
            if xs.min() == 0 or xs.max() == a.shape[1] - 1 or sz[j - 1] < sz.max() * 0.04:
                a[lab == j] = 0
    arrs.append(a)
alpha = np.any([a[..., 3] > 0 for a in arrs], axis=0); ys, xs = np.nonzero(alpha)
x0, y0 = max(xs.min() - margin, 0), max(ys.min() - margin, 0)
x1, y1 = min(xs.max() + margin + 1, alpha.shape[1]), min(ys.max() + margin + 1, alpha.shape[0])
for f, a in zip(fs, arrs):
    Image.fromarray(a[y0:y1, x0:x1]).save(f)
json.dump({'crop': [int(x0), int(y0), int(x1), int(y1)]}, open(f'{d}/trim.json', 'w'))
print(d, 'trim', x0, y0, x1, y1)
