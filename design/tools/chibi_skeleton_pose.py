"""Author PixelLab skeleton animations (animate-with-skeleton-v3) from a pose spec, and preview them offline.

Motion is designed here, before any generation: per frame we give pelvis offset, torso lean, foot and hand
targets (in reference-sprite pixels); arms and legs are solved with 2-bone IK from the rest skeleton that
PixelLab's /estimate-skeleton returned. Output:
  <spec>.keypoints.json  first_frame_keypoints + keypoints in canvas fractions (request-ready, no image)
  <spec>.sheet.png       stick-figure contact sheet (sword drawn from the spec's blade angle, preview only)
  <spec>.gif             stick-figure playback at the spec's frame timing
  <spec>.overlay.png     rest skeleton over the reference sprite (check labels before paying for anything)

Usage: python -I design/tools/chibi_skeleton_pose.py design/pixellab/chibi-motion/heavy-slash.pose.json
No network calls. The spec's paths are relative to the spec file.
"""
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

spec_path = Path(sys.argv[1])
spec = json.loads(spec_path.read_text(encoding='utf-8'))
base = spec_path.parent
rest_raw = {k['label']: k for k in json.loads((base / spec['restSkeleton']).read_text(encoding='utf-8'))['keypoints']}
REF = spec['referenceSize']                      # reference sprite px (the estimate is in fractions of this)
CANVAS = spec['canvas']                          # output canvas px
OX, OY = spec['offset']                          # where the reference sits inside the canvas
rest = {k: (v['x'] * REF, v['y'] * REF) for k, v in rest_raw.items()}
rest['HEADC'] = tuple(spec.get('headCenter', (0, 0)))   # preview only: chibi head circle, moves with the face points
# integer draw order preserving the estimate's ordering (it returns halves)
zidx = {k: int(round(v['z_index'] * 2)) for k, v in rest_raw.items()}

S = {'R': 'RIGHT', 'L': 'LEFT'}
HEAD = ['NOSE', 'LEFT EYE', 'RIGHT EYE', 'LEFT EAR', 'RIGHT EAR', 'HEADC']
pelvis0 = tuple((rest['LEFT HIP'][i] + rest['RIGHT HIP'][i]) / 2 for i in (0, 1))
dist = lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1])
bone = {s: {'upper': dist(rest[f'{S[s]} SHOULDER'], rest[f'{S[s]} ELBOW']),
            'fore': dist(rest[f'{S[s]} ELBOW'], rest[f'{S[s]} ARM']),
            'thigh': dist(rest[f'{S[s]} HIP'], rest[f'{S[s]} KNEE']),
            'shin': dist(rest[f'{S[s]} KNEE'], rest[f'{S[s]} LEG'])} for s in 'RL'}


def rot(p, c, deg):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def ik(root, target, l1, l2, prefer):
    """2-bone IK in screen space (y down). prefer(mid_a, mid_b) picks the bend. Returns (mid, end, reached)."""
    dx, dy = target[0] - root[0], target[1] - root[1]
    d = math.hypot(dx, dy)
    reached = d <= l1 + l2
    d = min(max(d, abs(l1 - l2) + 1e-3), l1 + l2 - 1e-3)
    a = math.atan2(dy, dx)
    al = math.acos((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d))
    mids = [(root[0] + l1 * math.cos(a + s * al), root[1] + l1 * math.sin(a + s * al)) for s in (1, -1)]
    end = (root[0] + d * math.cos(a), root[1] + d * math.sin(a))
    return prefer(*mids), end, reached


def pose(f):
    """One frame of the spec -> {label: (x, y)} in reference pixels, plus warnings."""
    warn = []
    px, py = f.get('pelvis', [0, 0])
    pel = (pelvis0[0] + px, pelvis0[1] + py)
    lean = f.get('lean', 0)                       # degrees, + leans forward (toward +x)
    tilt = f.get('head', -0.5 * lean)             # head counter-rotates by default: eyes stay on the target
    out = {}
    for k in ['NECK', 'LEFT SHOULDER', 'RIGHT SHOULDER', *HEAD]:
        p = (rest[k][0] - pelvis0[0] + pel[0], rest[k][1] - pelvis0[1] + pel[1])
        out[k] = rot(p, pel, lean)
    for k in HEAD:
        out[k] = rot(out[k], out['NECK'], tilt)
    for s in 'RL':
        n = S[s]
        out[f'{n} HIP'] = (rest[f'{n} HIP'][0] - pelvis0[0] + pel[0], rest[f'{n} HIP'][1] - pelvis0[1] + pel[1])
        foot = tuple(f.get('feet', {}).get(s, rest[f'{n} LEG']))
        knee, end, ok = ik(out[f'{n} HIP'], foot, bone[s]['thigh'], bone[s]['shin'],
                           lambda a, b: a if a[0] > b[0] else b)          # knees bend forward
        if not ok:
            warn.append(f'{n} foot out of reach by {dist(out[f"{n} HIP"], foot) - bone[s]["thigh"] - bone[s]["shin"]:.1f}px')
        out[f'{n} KNEE'], out[f'{n} LEG'] = knee, end
        sh = out[f'{n} SHOULDER']
        hand = f.get('hands', {}).get(s)
        if hand is None:                          # hang relaxed relative to the shoulder, plus an optional swing offset
            rel = f.get('handsRel', {}).get(s, (0, 0))
            hand = (rest[f'{n} ARM'][0] - rest[f'{n} SHOULDER'][0] + sh[0] + rel[0], rest[f'{n} ARM'][1] - rest[f'{n} SHOULDER'][1] + sh[1] + rel[1])
        bend = f.get('elbow', {}).get(s, 'down')
        pick = {'down': lambda a, b: a if a[1] > b[1] else b, 'up': lambda a, b: a if a[1] < b[1] else b,
                'back': lambda a, b: a if a[0] < b[0] else b, 'front': lambda a, b: a if a[0] > b[0] else b}[bend]
        elbow, end, ok = ik(sh, tuple(hand), bone[s]['upper'], bone[s]['fore'], pick)
        if not ok:
            warn.append(f'{n} hand out of reach by {dist(sh, hand) - bone[s]["upper"] - bone[s]["fore"]:.1f}px')
        out[f'{n} ELBOW'], out[f'{n} ARM'] = elbow, end
    return out, warn


def to_request(p, zover=None):
    pts = []
    for k in rest_raw:                            # same label order as the estimate
        x, y = (p[k][0] + OX) / CANVAS, (p[k][1] + OY) / CANVAS
        if not (0 <= x <= 1 and 0 <= y <= 1):
            raise SystemExit(f'{k} leaves the canvas ({x:.2f},{y:.2f}); move offset or enlarge canvas')
        # per-frame draw-order override, e.g. the far (weapon) arm crossing in front of the chest
        pts.append({'x': round(x, 4), 'y': round(y, 4), 'label': k, 'z_index': (zover or {}).get(k, zidx[k])})
    return pts


LIMBS = [('NECK', 'RIGHT SHOULDER'), ('NECK', 'LEFT SHOULDER'), ('RIGHT SHOULDER', 'RIGHT ELBOW'),
         ('RIGHT ELBOW', 'RIGHT ARM'), ('LEFT SHOULDER', 'LEFT ELBOW'), ('LEFT ELBOW', 'LEFT ARM'),
         ('RIGHT HIP', 'RIGHT KNEE'), ('RIGHT KNEE', 'RIGHT LEG'), ('LEFT HIP', 'LEFT KNEE'),
         ('LEFT KNEE', 'LEFT LEG'), ('RIGHT HIP', 'LEFT HIP')]
COL = {'RIGHT': (40, 110, 220), 'LEFT': (220, 70, 50), 'NECK': (30, 30, 30)}
Z = 4  # preview zoom


def draw(p, f, img=None, label=''):
    im = img or Image.new('RGB', (CANVAS * Z, CANVAS * Z), (236, 233, 226))
    d = ImageDraw.Draw(im)
    tp = lambda q: ((q[0] + OX) * Z, (q[1] + OY) * Z)
    gy = (spec.get('groundY', REF - 2) + OY + .5) * Z
    d.line([(0, gy), (CANVAS * Z, gy)], fill=(170, 160, 150), width=1)
    pel = tuple((p['LEFT HIP'][i] + p['RIGHT HIP'][i]) / 2 for i in (0, 1))
    d.line([tp(pel), tp(p['NECK'])], fill=(30, 30, 30), width=3)
    head_c, r = tp(p['HEADC']), spec.get('headRadius', 6) * Z
    d.ellipse([head_c[0] - r, head_c[1] - r, head_c[0] + r, head_c[1] + r], outline=(30, 30, 30), width=2)
    d.ellipse([tp(p['NOSE'])[0] - 3, tp(p['NOSE'])[1] - 3, tp(p['NOSE'])[0] + 3, tp(p['NOSE'])[1] + 3], fill=(30, 30, 30))
    for a, b in LIMBS:
        side = 'RIGHT' if a.startswith('RIGHT') or b.startswith('RIGHT') and not a.startswith('LEFT') else 'LEFT' if a.startswith('LEFT') else 'NECK'
        d.line([tp(p[a]), tp(p[b])], fill=COL[side], width=3 if side != 'LEFT' else 2)
    if f and 'blade' in f:                        # preview-only sword: grip in the weapon hand, blade angle from spec
        hand = p[f'{S[spec.get("weaponHand", "L")]} ARM']
        a = math.radians(f['blade'])
        L = spec.get('bladeLength', 15)
        tip = (hand[0] + L * math.cos(a), hand[1] + L * math.sin(a))
        pom = (hand[0] - 3 * math.cos(a), hand[1] - 3 * math.sin(a))
        d.line([tp(pom), tp(tip)], fill=(120, 120, 130), width=4)
        d.line([tp(hand), tp(tip)], fill=(250, 248, 240), width=2)
    if label:
        d.text((4, 4), label, fill=(20, 20, 20))
    return im


frames = spec['frames']
poses, warns = [], []
for i, f in enumerate(frames):
    p, w = pose(f)
    poses.append(p)
    warns += [f'frame {i}: {x}' for x in w]
    if 'blade' in f:
        side = S[spec.get('weaponHand', 'L')]
        e, h = p[f'{side} ELBOW'], p[f'{side} ARM']
        fa = math.degrees(math.atan2(h[1] - e[1], h[0] - e[0]))
        diff = abs((f['blade'] - fa + 180) % 360 - 180)
        if diff > 75:
            warns.append(f'frame {i}: forearm points {fa:.0f} deg but blade planned {f["blade"]} deg (off {diff:.0f})')
first = {k: rest[k] for k in rest}
stem = spec_path.with_suffix('')
req = {'first_frame_keypoints': to_request(first), 'keypoints': [to_request(p, f.get('z')) for p, f in zip(poses, frames)],
       'frameMs': [f.get('ms', 60) for f in frames], 'impactFrame': spec.get('impactFrame'),
       'canvas': CANVAS, 'offset': [OX, OY], 'referenceSize': REF}
Path(str(stem) + '.keypoints.json').write_text(json.dumps(req, indent=1), encoding='utf-8')

tiles = [draw(p, f, label=f"{i} {f.get('note', '')} {f.get('ms', 60)}ms") for i, (p, f) in enumerate(zip(poses, frames))]
cols = 5
sheet = Image.new('RGB', (cols * CANVAS * Z, math.ceil(len(tiles) / cols) * CANVAS * Z), (255, 255, 255))
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * CANVAS * Z, (i // cols) * CANVAS * Z))
sheet.save(str(stem) + '.sheet.png')
tiles[0].save(str(stem) + '.gif', save_all=True, append_images=tiles[1:], duration=[f.get('ms', 60) for f in frames], loop=0)

ref = Image.open(base / spec['reference']).convert('RGBA')
ov = Image.new('RGBA', (CANVAS, CANVAS), (236, 233, 226, 255))
ov.alpha_composite(ref, (OX, OY))
ov = ov.resize((CANVAS * Z, CANVAS * Z), Image.NEAREST).convert('RGB')
draw(first, None, ov, 'rest skeleton from /estimate-skeleton (blue=RIGHT, red=LEFT)')
ov.save(str(stem) + '.overlay.png')
print(json.dumps({'frames': len(frames), 'durationMs': sum(req['frameMs']), 'warnings': warns}, indent=1))
