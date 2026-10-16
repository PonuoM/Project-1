"""Write a strip + pick json from a frame range. usage: loop_strip.py CLIP_DIR NAME START END MS [LABEL]"""
import json, sys
from PIL import Image
d, name, a, b, ms = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
label = sys.argv[6] if len(sys.argv) > 6 else name
ims = [Image.open(f'{d}/frames/frame-{i:02d}.png').convert('RGBA') for i in range(a, b + 1)]
w, h = ims[0].size
st = Image.new('RGBA', (w * len(ims), h))
for k, im in enumerate(ims):
    st.paste(im, (k * w, 0))
st.save(f'{d}/strip-{name}.png')
json.dump({'about': label, 'frameWidth': w, 'impactFrame': -1,
           'frames': [{'note': name, 'ms': ms, 'sourceFrame': i} for i in range(a, b + 1)]},
          open(f'{d}/pick-{name}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(name, len(ims), len(ims) * ms, 'ms')
