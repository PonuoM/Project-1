"""Build MiniMax H3 start frames for monsters and bosses. No network.
Monsters face LEFT, so the frame sits right of centre (mirror of the heroes' x=300 origin) leaving room for
lunges to the left. Feet share the heroes' ground line (y=680 at the bottom of the frame).
Writes, per creature: motion/_inputs/<name>-64.png (native frame), <name>-1280x720.png, <name>-1280x720-end.png
(the app rejects the same file twice) and motion/_inputs/monsters.json with scale/origin for video_to_sprite.py.
"""
import json
from PIL import Image

SRC = 'concepts/monsters-g8-codex/'
OUT = 'motion/_inputs/'
GREEN = (0, 177, 64)
GROUND = 680
RIGHT = 980  # right edge of the sprite frame = 1280 - 300

# name, approved file, video scale (frame px x scale must fit 720 high)
CREATURES = [
    ('kiki', 'kiki-v3.png', 8),
    ('thornboar', 'thornboar-v4.png', 8),
    ('hex-scarecrow', 'hex-scarecrow-v4.png', 8),
    ('bridge-troll', 'bridge-troll-v3.png', 8),
    ('grimfang', 'grimfang-v2.png', 4),
    ('thunderhead', 'thunderhead-v2.png', 4),
]

meta = {}
for name, fname, scale in CREATURES:
    big = Image.open(SRC + fname).convert('RGB')
    native = big.resize((big.width // 8, big.height // 8), Image.NEAREST)
    native.save(OUT + f'{name}-64.png')
    w, h = native.width * scale, native.height * scale
    ox, oy = RIGHT - w, GROUND - h
    assert ox >= 0 and oy >= 0, (name, ox, oy)
    frame = Image.new('RGB', (1280, 720), GREEN)
    frame.paste(native.resize((w, h), Image.NEAREST), (ox, oy))
    frame.save(OUT + f'{name}-1280x720.png')
    frame.save(OUT + f'{name}-1280x720-end.png')
    meta[name] = {'source': SRC + fname, 'frame': native.width, 'scale': scale, 'origin': [ox, oy]}
    print(name, native.size, 'scale', scale, 'origin', (ox, oy))

json.dump(meta, open(OUT + 'monsters.json', 'w'), indent=1)
