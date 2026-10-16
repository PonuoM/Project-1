"""Find the best loop inside a frame range: lag P and start s where frame s ~ frame s+P. usage: find_loop.py DIR A B PMIN PMAX"""
import sys
import numpy as np
from PIL import Image
d, a, b, pmin, pmax = sys.argv[1], *map(int, sys.argv[2:6])
fr = {i: np.array(Image.open(f'{d}/frames/frame-{i:02d}.png').convert('RGBA')).astype(int) for i in range(a, b + 1)}
def diff(i, j):
    x, y = fr[i], fr[j]
    return np.mean(np.abs(x - y)[..., :3] * ((x[..., 3] > 0) | (y[..., 3] > 0))[..., None])
best = []
for p in range(pmin, pmax + 1):
    for s in range(a, b - p + 1):
        best.append((diff(s, s + p), p, s))
best.sort()
for v, p, s in best[:6]:
    print(f'lag {p} start {s} diff {v:.2f}')
