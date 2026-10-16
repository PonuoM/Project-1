"""Build pick-manual.json + strip-manual.png from hand-chosen video frames. usage: python make_pick.py"""
import json
from PIL import Image

PICKS = {
 'S01-slash-pixellab-v2': (7, [(0,60,'ready'),(1,50,'lift'),(2,50,'raise'),(3,60,'wind'),(4,60,'wind'),(5,100,'HOLD high'),(6,40,'launch'),(7,100,'IMPACT'),(8,60,'follow'),(9,60,'hold'),(10,50,'recover'),(11,50,'recover'),(12,80,'ready')]),
 'S01-slash-pixellab': (9, [(0,60,'ready'),(1,50,'swing up'),(2,50,'raise'),(3,60,'over head'),(4,100,'HOLD'),(7,40,'top'),(8,100,'IMPACT low'),(9,60,'hold'),(12,60,'recover'),(16,80,'ready')]),
 'S01-slash-spriteflow': (7, [(0,60,'ready'),(4,50,'crouch'),(5,50,'raise'),(6,60,'wind'),(8,100,'HOLD high'),(16,40,'coil'),(17,30,'swing'),(18,100,'IMPACT'),(23,60,'follow'),(24,50,'recover'),(25,50,'recover'),(26,50,'recover'),(31,80,'ready')]),
 'S01-slash-mmd768': (7, [(0,60,'ready'),(24,50,'step'),(26,50,'drop'),(27,60,'wind'),(29,90,'HOLD high'),(30,30,'swing'),(31,40,'swing smear'),(32,90,'IMPACT'),(40,60,'follow'),(52,50,'recover'),(53,50,'recover'),(55,80,'ready')]),
 'S01-slash-h3': (7, [(0,60,'ready'),(10,50,'raise'),(11,60,'wind'),(12,90,'HOLD over shoulder'),(17,40,'coil'),(18,30,'swing smear'),(19,40,'swing smear'),(20,90,'IMPACT'),(28,60,'follow'),(51,50,'recover'),(53,50,'recover'),(55,80,'ready')]),
 'S02-thrust-h3': (6, [(0,60,'ready'),(10,50,'drop'),(11,50,'pull back'),(12,60,'coil'),(14,80,'HOLD coil'),(15,40,'lunge'),(16,120,'IMPACT thrust'),(40,70,'hold'),(51,50,'recover'),(52,50,'recover'),(53,80,'ready')]),
 'S01-slash': (5, [(0,60,'ready'),(15,60,'wind back'),(16,100,'HOLD high'),(23,30,'launch'),(24,40,'slash'),(25,70,'IMPACT'),(27,60,'follow'),(40,50,'recover'),(41,80,'ready')]),
 'S02-thrust': (8, [(0,60,'ready'),(18,40,'drop'),(20,50,'raise'),(22,60,'pull back'),(24,90,'HOLD coil'),(27,40,'launch'),(28,30,'lunge'),(29,120,'IMPACT thrust'),(41,80,'hold'),(42,80,'ready')]),
 'S03-combo3': (14, [(0,50,'ready'),(7,40,'step'),(9,40,'slash 1'),(10,70,'HIT 1'),(12,40,'turn'),(13,70,'HIT 2'),(27,50,'raise'),(45,40,'crouch'),(47,50,'jump'),(49,40,'overhead'),(52,60,'HOLD air'),(60,40,'drop'),(62,30,'chop'),(64,90,'HIT 3'),(66,60,'recover'),(67,80,'ready')]),
 'S04-spin': (4, [(0,50,'ready'),(3,40,'extend'),(5,50,'set'),(20,45,'spin front'),(21,45,'spin back'),(22,45,'spin back-left'),(24,45,'spin front'),(25,45,'spin back'),(26,45,'spin back-left'),(44,50,'stop'),(45,50,'recover'),(47,80,'ready')]),
}
for clip, (impact, fr) in PICKS.items():
    imgs = [Image.open(f'{clip}/frames/frame-{i:02d}.png').convert('RGBA') for i, _, _ in fr]
    w, h = imgs[0].size
    strip = Image.new('RGBA', (w * len(imgs), h), (0, 0, 0, 0))
    for k, im in enumerate(imgs):
        strip.paste(im, (k * w, 0))
    strip.save(f'{clip}/strip-manual.png')
    spec = {'about': 'hand-picked by Claude from the Flow clip (fast timing)', 'source': 'frames/', 'frameWidth': w,
            'impactFrame': impact, 'frames': [{'note': n, 'ms': ms, 'sourceFrame': i} for i, ms, n in fr]}
    if clip == 'S04-spin':
        spec['loop'] = [3, 8]
    json.dump(spec, open(f'{clip}/pick-manual.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(clip, len(fr), 'frames', sum(m for _, m, _ in fr), 'ms')
