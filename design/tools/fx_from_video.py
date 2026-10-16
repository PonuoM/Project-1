"""Turn an FX video on black into pixel-art frames with alpha (for additive or normal blending). No network.
usage: fx_from_video.py VIDEO OUT_DIR --regions name:x0-x1,... [--cell 8] [--every 1] [--colors 10] [--black 40]
  regions are in 1280x720 canvas pixels (the video is mapped to that canvas per axis); one output folder per region.
  Each art pixel = --cell canvas pixels (median colour); alpha from brightness (below --black = transparent,
  ramps to opaque); colours reduced to --colors per region (shared palette across all frames of that region).
Writes OUT_DIR/<name>/frame-NN.png, strip.png and OUT_DIR/sheet.png."""
import argparse, os, subprocess, tempfile, glob
import numpy as np
from PIL import Image
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('out')
ap.add_argument('--regions', required=True); ap.add_argument('--cell', type=int, default=8)
ap.add_argument('--every', type=int, default=1); ap.add_argument('--colors', type=int, default=10); ap.add_argument('--black', type=int, default=40)
ap.add_argument('--video-coords', action='store_true', help='regions and cell are in video pixels (no 1280x720 mapping); y range via --rows y0-y1')
ap.add_argument('--rows', default=None)
o = ap.parse_args()
regions = [(r.split(':')[0], *map(int, r.split(':')[1].split('-'))) for r in o.regions.split(',')]
tmp = tempfile.mkdtemp()
subprocess.run(['ffmpeg', '-v', 'error', '-i', o.video, os.path.join(tmp, 'f%03d.png')], check=True)
files = sorted(glob.glob(os.path.join(tmp, 'f*.png')))[::o.every]
frames = []
for f in files:
    im = Image.open(f).convert('RGB'); frames.append(np.array(im if o.video_coords else im.resize((1280, 720), Image.BILINEAR)))
C = o.cell
Y0, Y1 = (map(int, o.rows.split('-')) if o.rows else (0, frames[0].shape[0]))
H = (Y1 - Y0) // C
os.makedirs(o.out, exist_ok=True); rows = []
for name, x0, x1 in regions:
    W = (x1 - x0) // C; cells = []
    for fr in frames:
        blk = fr[Y0:Y0 + H * C, x0:x0 + W * C].reshape(H, C, W, C, 3)
        cells.append(np.median(blk, axis=(1, 3)).astype(np.uint8))
    stack = np.stack(cells)                                  # T,H,W,3
    lum = stack.max(-1).astype(float)
    alpha = np.clip((lum - o.black) / 60.0, 0, 1)
    # shared palette from the visible pixels of all frames
    vis = stack[alpha > 0.5]
    if len(vis) == 0: continue
    pal_img = Image.fromarray(vis.reshape(-1, 1, 3)).quantize(colors=o.colors, method=Image.Quantize.MEDIANCUT)
    os.makedirs(f'{o.out}/{name}', exist_ok=True); outs = []
    for t in range(len(stack)):
        q = np.array(Image.fromarray(stack[t]).quantize(palette=pal_img, dither=Image.Dither.NONE).convert('RGB'))
        a = np.where(alpha[t] > 0.35, 255, 0).astype(np.uint8)   # hard alpha keeps the pixel-art edge
        rgba = np.dstack([q, a]); Image.fromarray(rgba).save(f'{o.out}/{name}/frame-{t:02d}.png'); outs.append(rgba)
    strip = np.concatenate(outs, 1); Image.fromarray(strip).save(f'{o.out}/{name}/strip.png')
    rows.append(np.concatenate(outs[::3], 1))
w = max(r.shape[1] for r in rows); sheet = np.zeros((sum(r.shape[0] for r in rows), w, 4), np.uint8); y = 0
for r in rows: sheet[y:y + r.shape[0], :r.shape[1]] = r; y += r.shape[0]
bg = Image.new('RGBA', (w, sheet.shape[0]), (20, 20, 28, 255)); bg.alpha_composite(Image.fromarray(sheet)); bg.save(f'{o.out}/sheet.png')
print('frames', len(frames), 'regions', [r[0] for r in regions])
