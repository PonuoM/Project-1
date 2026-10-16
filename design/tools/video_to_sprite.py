"""Turn an AI video of an upscaled sprite back into pixel-art frames. No network.

Usage: python -I design/tools/video_to_sprite.py VIDEO.mp4 OUT_DIR --ref SPRITE.png --scale 8 --origin X,Y
          [--canvas 1280x720] [--every 2] [--bg 230,230,230 | --key green] [--crop W,H,DX,DY]
  --ref     the native sprite that was upscaled into the first frame (its colours become the locked palette)
  --scale   upscale factor used for the first frame; --origin where its top-left sat on the --canvas
  The video may come back at another resolution: geometry is rescaled per axis (video size / canvas size).
  --every   keep every Nth video frame (24 fps -> every 2 = 12 fps of candidates)
  --crop    output window in sprite pixels relative to the sprite's origin (default: 96x80 starting 16 px left, 16 px up)
Writes OUT_DIR/frame-NN.png (+ strip.png, sheet.png) and OUT_DIR/convert.json (grid, palette, per-frame bbox).
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

video, out = Path(sys.argv[1]), Path(sys.argv[2])
o = dict(zip(sys.argv[3::2], sys.argv[4::2]))
ref = np.array(Image.open(o['--ref']).convert('RGBA'))
S = float(o.get('--scale', 8))
ox, oy = map(float, o['--origin'].split(','))
cw, ch = map(int, o.get('--canvas', '1280x720').split('x'))
every = int(o.get('--every', 2))
bg = np.array(list(map(int, o.get('--bg', '230,230,230').split(','))), float)
green = o.get('--key') == 'green'           # chroma key: saturated green is background (olive tunic / teal hair survive)
W, H, DX, DY = map(int, o.get('--crop', '96,80,16,16').split(','))

pal = np.unique(ref[ref[:, :, 3] > 0][:, :3], axis=0).astype(float)
out.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory() as td:
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), f'{td}/v%04d.png'], check=True)
    files = sorted(Path(td).glob('v*.png'))[::every]
    with Image.open(files[0]) as im0:      # close handles: Windows cannot delete the temp dir otherwise
        first = im0.copy()
    # MiniMax returns 1344x768 for a 1280x720 input: each axis is stretched separately (x1.05, x1.067)
    kx, ky = first.width / cw, first.height / ch
    cx, cy = S * kx, S * ky                   # video px per sprite pixel, per axis
    x0, y0 = (ox - DX * S) * kx, (oy - DY * S) * ky
    frames, info = [], []
    for fp in files:
        with Image.open(fp) as vim:
            v = np.array(vim.convert('RGB')).astype(float)
        o_img = np.zeros((H, W, 4), np.uint8)
        for j in range(H):
            for i in range(W):
                a0, b0 = x0 + i * cx, y0 + j * cy
                xs, ys = int(a0 + cx * .2), int(b0 + cy * .2)
                xe, ye = int(a0 + cx * .8), int(b0 + cy * .8)
                if xs < 0 or ys < 0 or xe > v.shape[1] or ye > v.shape[0] or xe <= xs or ye <= ys:
                    continue
                blk = v[ys:ye, xs:xe].reshape(-1, 3)
                if green:
                    fg = ~((blk[:, 1] - np.maximum(blk[:, 0], blk[:, 2]) > 50) & (blk[:, 1] > 100))
                else:
                    fg = np.abs(blk - bg).max(1) > 18     # far enough from the flat grey background
                if fg.mean() < .5:
                    continue
                c = np.median(blk[fg], 0)
                o_img[j, i, :3] = pal[np.abs(pal - c).sum(1).argmin()]   # palette lock
                o_img[j, i, 3] = 255
        # despeckle: drop 8-connected specks smaller than 6 px (green-spill leftovers away from the character)
        seen = np.zeros((H, W), bool)
        for sy0 in range(H):
            for sx0 in range(W):
                if o_img[sy0, sx0, 3] and not seen[sy0, sx0]:
                    comp, stack = [], [(sy0, sx0)]
                    seen[sy0, sx0] = True
                    while stack:
                        y, x = stack.pop(); comp.append((y, x))
                        for yy in (y - 1, y, y + 1):
                            for xx in (x - 1, x, x + 1):
                                if 0 <= yy < H and 0 <= xx < W and o_img[yy, xx, 3] and not seen[yy, xx]:
                                    seen[yy, xx] = True; stack.append((yy, xx))
                    if len(comp) < 6:
                        for y, x in comp:
                            o_img[y, x] = 0
        im = Image.fromarray(o_img)
        frames.append(im)
        info.append({'source': fp.name, 'bbox': im.getbbox()})
for n, im in enumerate(frames):
    im.save(out / f'frame-{n:02d}.png')
Z = 4
strip = Image.new('RGBA', (W * len(frames), H), (0, 0, 0, 0))
cols = 8
sheet = Image.new('RGB', (cols * W * Z, ((len(frames) + cols - 1) // cols) * H * Z), (236, 233, 226))
d = ImageDraw.Draw(sheet)
for n, im in enumerate(frames):
    strip.paste(im, (n * W, 0))
    t = Image.new('RGBA', (W, H), (236, 233, 226, 255)); t.alpha_composite(im)
    sheet.paste(t.resize((W * Z, H * Z), Image.NEAREST).convert('RGB'), ((n % cols) * W * Z, (n // cols) * H * Z))
    d.text(((n % cols) * W * Z + 3, (n // cols) * H * Z + 2), str(n), fill=(20, 20, 20))
strip.save(out / 'strip.png')
sheet.save(out / 'sheet.png')
(out / 'convert.json').write_text(json.dumps({'video': str(video), 'videoSize': [first.width, first.height], 'cellPx': [cx, cy],
                                              'every': every, 'palette': len(pal), 'window': [W, H, DX, DY], 'frames': info}, indent=1),
                                  encoding='utf-8')
print(json.dumps({'frames': len(frames), 'videoSize': [first.width, first.height], 'cellPx': [round(cx, 3), round(cy, 3)]}))
