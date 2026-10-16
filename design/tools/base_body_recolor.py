"""Turn the hero sprite into a grey-bodysuit base body (keeps outline, hair, skin pixels exactly).

usage: python tools/base_body_recolor.py SRC OUT [--violet-sword]
Rows above 36 (head) are kept. Clothing = every other pixel that is not outline, teal hair, skin or (with --violet-sword) steel sword grey.
Clothing is mapped to 3 greys by luminance; the sword's greys become violet #7a3cff / #5a24c8.
"""
import sys
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
violet = '--violet-sword' in sys.argv
im = Image.open(src).convert('RGBA')
px = im.load()
GREYS = [(78, 80, 86), (128, 130, 138), (176, 178, 186)]

def lum(c): return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
def is_outline(c): return c[0] < 60 and c[1] < 35 and c[2] < 35
def is_hair(c): return c[1] >= c[0] + 15 and abs(c[1] - c[2]) < 30
def is_skin(c): return c[0] > 235 and 150 <= c[1] <= 220 and c[2] < 180
def is_steel(c): return abs(c[0] - c[1]) < 14 and c[2] >= c[0] + 4 and c[2] - c[0] < 20

for y in range(im.height):
    for x in range(im.width):
        c = px[x, y]
        if c[3] == 0 or y < 36 or is_outline(c) or is_hair(c) or is_skin(c):  # y<36: head, kept as is
            continue
        if is_steel(c) and x >= 36 and y >= 46:  # the sword sits low right
            if violet:
                px[x, y] = ((122, 60, 255, 255) if lum(c) > 100 else (90, 36, 200, 255))
            continue
        l = lum(c)
        px[x, y] = GREYS[0] + (255,) if l < 90 else GREYS[1] + (255,) if l < 165 else GREYS[2] + (255,)
im.save(out)
big = im.resize((512, 512), Image.NEAREST)
bg = Image.new('RGBA', big.size, (0, 177, 64, 255)); bg.alpha_composite(big)
bg.convert('RGB').save(out.replace('.png', '-x8-green.png'))
