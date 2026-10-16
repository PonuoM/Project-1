"""Small labelled contact sheet of a converted clip (every Nth frame). usage: mini_sheet.py CLIP_DIR OUT.png [STEP]"""
import sys, glob
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]
step = int(sys.argv[3]) if len(sys.argv) > 3 else 2
fs = sorted(glob.glob(f'{d}/frames/frame-*.png'))[::step]
w, h = Image.open(fs[0]).size
cols = 8
s = Image.new('RGBA', (w * cols, (h + 10) * ((len(fs) + cols - 1) // cols)), (236, 233, 226, 255))
dr = ImageDraw.Draw(s)
for k, f in enumerate(fs):
    x, y = (k % cols) * w, (k // cols) * (h + 10)
    s.alpha_composite(Image.open(f).convert('RGBA'), (x, y + 10))
    dr.text((x + 2, y), f[-6:-4], fill=(0, 0, 0))
s.save(out)
