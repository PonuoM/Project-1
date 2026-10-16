"""Recolour each roster character's weapon to the violet weapon ID colour (#7a3cff / #5a24c8). No network.
Regions are art-pixel boxes (x0, y0, x1, y1) on the 64x64 grid of the 512x512 concept sprites; inside them a
per-character colour rule picks the weapon pixels (outline and skin are always kept). Writes, per character,
motion/_inputs/<name>-violet-64.png, -512.png and -1280x720.png (sprite x8 at (300,168) on #00B140) plus a check sheet.
"""
import colorsys
from PIL import Image

C = 'concepts/'
V1, V2 = (122, 60, 255), (90, 36, 200)


def hsv(c):
    return colorsys.rgb_to_hsv(*(v / 255 for v in c))


def outline(c):
    return max(c) < 75
def skin(c):
    h, s, v = hsv(c)
    return 0.03 < h < 0.11 and 0.18 < s < 0.55 and v > 0.78
def any_(c):
    return True
def not_red(c):
    h, s, v = hsv(c)
    return not ((h > 0.92 or h < 0.02) and s > 0.45)
def leafy(c):
    h, s, v = hsv(c)
    return 0.10 < h < 0.36 and s > 0.25
def pale(c):
    h, s, v = hsv(c)
    return s < 0.3 and v > 0.5
def not_coat_teal(c):
    h, s, v = hsv(c)
    return not (0.45 < h < 0.58 and s > 0.25)
def brownish(c):
    h, s, v = hsv(c)
    return 0.0 <= h < 0.12 and v < 0.75
def very_pale(c):
    h, s, v = hsv(c)
    return s < 0.2 and v > 0.78
def bow_metal(c):
    h, s, v = hsv(c)
    return v > 0.38 and ((0.0 <= h < 0.16 and s > 0.3) or (s < 0.15 and v > 0.55))
def gunmetal(c):
    h, s, v = hsv(c)
    return (s < 0.22 and v > 0.3) or (0.07 < h < 0.16 and s > 0.4)

CHARS = {
    'mara':    ('characters-g5/codex/melee-1-v2.png', [((29, 49, 45, 59), pale)]),
    'rika':    ('characters-g5-expansion-codex-v1/melee-brawler-v1.png', [((19, 43, 30, 54), not_red), ((35, 37, 48, 50), not_red)]),
    'sella':   ('characters-g5/codex/melee-3-v1.png', [((42, 49, 61, 59), leafy)]),
    'yara':    ('characters-g5-expansion-codex-v1/melee-assassin-v1.png', [((41, 47, 51, 52), pale), ((23, 50, 30, 58), very_pale)]),
    'pipra':   ('characters-g5/codex/mage-1-v1.png', [((40, 45, 52, 56), any_)]),
    'vessa':   ('characters-g5/codex/mage-2-v1.png', [((37, 41, 44, 51), any_)]),
    'noll':    ('characters-g5-expansion-codex-v1/mage-summoner-v1.png', [((43, 25, 57, 44), any_)]),
    'tavi':    ('characters-g5/codex/archer-1-v1.png', [((40, 41, 48, 56), brownish)]),
    'ilen':    ('characters-g5/codex/archer-2-v1.png', [((38, 45, 49, 53), bow_metal)]),
    'bramble': ('characters-g5-expansion-codex-v1/ranged-gunner-dual-v1.png', [((39, 38, 50, 46), gunmetal)]),
}


def main():
    sheet = Image.new('RGB', (64 * 6 * 5, 64 * 6 * 2), (0, 177, 64))
    for k, (name, (path, rules)) in enumerate(CHARS.items()):
        im = Image.open(C + path).convert('RGB')
        s = Image.new('RGBA', (64, 64))
        for y in range(64):
            for x in range(64):
                c = im.getpixel((x * 8 + 4, y * 8 + 4))
                if c[1] > 140 and c[0] < 60 and c[2] < 100:
                    continue
                for (x0, y0, x1, y1), rule in rules:
                    if x0 <= x < x1 and y0 <= y < y1 and not outline(c) and not skin(c) and rule(c):
                        c = V1 if hsv(c)[2] > 0.55 else V2
                        break
                s.putpixel((x, y), c + (255,))
        s.save(f'motion/_inputs/{name}-violet-64.png')
        big = s.resize((512, 512), Image.NEAREST)
        g = Image.new('RGBA', (512, 512), (0, 177, 64, 255)); g.alpha_composite(big)
        g.convert('RGB').save(f'motion/_inputs/{name}-violet-512.png')
        cv = Image.new('RGBA', (1280, 720), (0, 177, 64, 255)); cv.alpha_composite(big, (300, 168))
        cv.convert('RGB').save(f'motion/_inputs/{name}-violet-1280x720.png')
        cv2 = cv.copy(); cv2.putpixel((0, 0), (0, 178, 64, 255)); cv2.convert('RGB').save(f'motion/_inputs/{name}-violet-1280x720-end.png')
        sheet.paste(g.convert('RGB').resize((384, 384), Image.NEAREST), ((k % 5) * 384, (k // 5) * 384))
    sheet.save('motion/_inputs/check-sheet.png')
    print('ok', len(CHARS))


if __name__ == '__main__':
    main()
