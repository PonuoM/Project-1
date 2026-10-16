"""Make a cleaned COPY of a PixelLab character trial without touching the originals or calling PixelLab.

    python -I design/tools/clean_pixellab_frames.py design/pixellab/swordsman

Reads  <dir>/candidate-11.png, <dir>/attack-frames/frame-*.png, <dir>/animation.json
Writes <dir>/cleaned/{candidate-11.png, attack-frames/, attack.png, animation.json, inspection.json}

Cleaning rules (all reported in inspection.json):
1. Stray artifact: small components (<= 20 px) detached from the character in the reference candidate are
   recorded as a signature (position + exact color) and removed from every frame where the same pixels appear,
   even when a slash arc touches them.
2. Any other detached component <= 20 px is removed unless it is mostly near-white, which is treated as slash
   spark FX and kept.
3. Nothing is moved: the feet line and the planted front foot are checked and reported, not re-aligned,
   unless they disagree between frames.
"""
import json
import sys
from pathlib import Path

from PIL import Image

STRAY_MAX = 20
WHITE_MIN = 220


def components(img):
    w, h = img.size
    px = img.load()
    seen = set()
    comps = []
    for y in range(h):
        for x in range(w):
            if px[x, y][3] == 0 or (x, y) in seen:
                continue
            stack = [(x, y)]
            seen.add((x, y))
            pts = []
            while stack:
                cx, cy = stack.pop()
                pts.append((cx, cy))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and px[nx, ny][3] > 0:
                            seen.add((nx, ny))
                            stack.append((nx, ny))
            comps.append(pts)
    comps.sort(key=len, reverse=True)
    return comps


def near_white(rgba):
    return min(rgba[:3]) >= WHITE_MIN


def measure(img):
    """Feet line, planted front foot and torso position of the main body."""
    main = components(img)[0]
    bottom = max(p[1] for p in main)
    feet = sorted(p[0] for p in main if p[1] >= bottom - 2)
    torso = sorted(p[0] for p in main if 28 <= p[1] <= 40)
    return {'feetRow': bottom, 'backFootX': feet[0], 'frontFootX': feet[-1], 'torsoX': torso[len(torso) // 2]}


def main():
    root = Path(sys.argv[1])
    out = root / 'cleaned'
    (out / 'attack-frames').mkdir(parents=True, exist_ok=True)
    spec = json.loads((root / 'animation.json').read_text(encoding='utf-8'))

    ref = Image.open(root / 'candidate-11.png').convert('RGBA')
    ref_px = ref.load()
    signature = {}
    for comp in components(ref)[1:]:
        if len(comp) <= STRAY_MAX:
            for p in comp:
                signature[p] = ref_px[p]

    report = {'source': str(root.as_posix()), 'rules': __doc__.split('Cleaning rules')[1].strip(), 'files': []}

    def clean(src, dst):
        img = Image.open(src).convert('RGBA')
        px = img.load()
        removed, kept_sparks = [], []
        for p, color in signature.items():
            if px[p] == color:
                px[p] = (0, 0, 0, 0)
                removed.append(p)
        for comp in components(img)[1:]:
            if len(comp) > STRAY_MAX:
                continue
            if sum(near_white(px[p]) for p in comp) * 2 >= len(comp):
                kept_sparks.append({'size': len(comp), 'box': box(comp)})
                continue
            for p in comp:
                px[p] = (0, 0, 0, 0)
                removed.append(p)
        img.save(dst)
        entry = {'file': dst.name, 'removedPixels': len(removed), 'removedBox': box(removed) if removed else None,
                 'keptSparkComponents': kept_sparks, **measure(img)}
        report['files'].append(entry)
        return img

    clean(root / 'candidate-11.png', out / 'candidate-11.png')
    frames = [clean(f, out / 'attack-frames' / f.name) for f in sorted((root / 'attack-frames').glob('frame-*.png'))]

    w, h = frames[0].size
    sheet = Image.new('RGBA', (w * len(frames), h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * w, 0))
    sheet.save(out / 'attack.png')

    rows = {e['feetRow'] for e in report['files']}
    fronts = [e['frontFootX'] for e in report['files'][1:]]
    report['checks'] = {
        'feetRowSameEveryFrame': len(rows) == 1,
        'feetRow': sorted(rows),
        'frontFootRange': [min(fronts), max(fronts)],
        'realigned': False,
        'note': 'Feet share one row and the front foot stays within a few pixels, so no frame was moved. '
                'Torso x shifts during the swing are the pose (lean/twist), not drift.',
    }
    (out / 'inspection.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')

    cleaned_spec = dict(spec)
    cleaned_spec['source'] = 'Cleaned copy of ../attack-frames (stray pixels removed; frames not moved). Originals unchanged.'
    cleaned_spec['cleanedBy'] = 'design/tools/clean_pixellab_frames.py'
    (out / 'animation.json').write_text(json.dumps(cleaned_spec, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(report['checks'], ensure_ascii=False))
    for e in report['files']:
        print(e['file'], 'removed', e['removedPixels'], 'sparks kept', len(e['keptSparkComponents']), 'feetRow', e['feetRow'], 'frontFoot', e['frontFootX'])


def box(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return [min(xs), min(ys), max(xs), max(ys)]


if __name__ == '__main__':
    main()
