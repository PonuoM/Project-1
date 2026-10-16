"""Merge an outpainted sheet (Prompt G9) back into the original frames: original pixels always win; only new pixels
outside the original frame rectangle (in the top/right padding) are taken. No network.
usage: merge_fill.py LAYOUT.json SHEET_NAME FILLED.png FRAMES_ROOT OUT_ROOT
  FRAMES_ROOT/<move>/frames/frame-NN.png are the originals; OUT_ROOT/<move>/frame-NN.png get the merged, padded frames.
"""
import json, os, sys
import numpy as np
from PIL import Image
lay = json.load(open(sys.argv[1]))[sys.argv[2]]
filled = Image.open(sys.argv[3]).convert('RGB').resize(tuple(lay['size']))
S = lay['scale']
small = np.array(filled)[S // 2::S, S // 2::S]           # back to native pixels (centre sample)
for c in lay['cells']:
    x, y, pad = c['x'], c['y'], c['pad']
    orig = np.array(Image.open(f"{sys.argv[4]}/{c['move']}/frames/frame-{c['frame']:02d}.png").convert('RGBA'))
    h, w = orig.shape[:2]                                  # each frame keeps its own size inside the cell
    cell = np.zeros((h + pad, w + pad, 3), np.uint8); cell[...] = (0, 177, 64)
    part = small[y:y + h + pad, x:x + w + pad]; cell[:part.shape[0], :part.shape[1]] = part
    out = np.zeros((h + pad, w + pad, 4), np.uint8)
    green = (cell[..., 1] > 140) & (cell[..., 0] < 60) & (cell[..., 2] < 110)
    out[..., :3] = cell; out[..., 3] = np.where(green, 0, 255)
    out[pad:, :w] = orig                                   # the original area comes only from the original frame
    os.makedirs(f"{sys.argv[5]}/{c['move']}", exist_ok=True)
    Image.fromarray(out).save(f"{sys.argv[5]}/{c['move']}/frame-{c['frame']:02d}.png")
    print(c['move'], c['frame'])
