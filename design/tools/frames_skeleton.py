"""Estimate a PixelLab skeleton for picked video frames, so the weapon layer can follow a video-made body.

Usage: python -I design/tools/frames_skeleton.py PICK.json
  PICK.json (from a video_to_sprite clip): {"source": "frames/", "frameWidth": W, "frames": [{"sourceFrame": n, "note", "ms", "blade"?}...]}
Writes PICK.keypoints.json in the same shape chibi_skeleton_pose.py produces ({"keypoints": [[{x,y,label,z_index}...]...]},
fractions of the W x H frame) and caches every estimate in estimates/frame-NN.json (re-runs never pay twice).
Each new estimate costs 0.1 PixelLab generation. Credentials only from PIXELLAB_API_KEY.
"""
import base64
import io
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

pick_p = Path(sys.argv[1])
pick = json.loads(pick_p.read_text(encoding='utf-8'))
src = pick_p.parent / pick['source']
cache = pick_p.parent / 'estimates'
cache.mkdir(exist_ok=True)
key = os.environ.get('PIXELLAB_API_KEY')
out = []
for f in pick['frames']:
    n = f['sourceFrame']
    cp = cache / f'frame-{n:02d}.json'
    im = Image.open(src / f'frame-{n:02d}.png').convert('RGBA')
    W, H = im.size
    S = 128                                     # estimate-skeleton accepts 16/32/64/128/256 squares only
    ox, oy = (S - W) // 2, S - H
    if not cp.exists():
        if not key:
            raise SystemExit('Set PIXELLAB_API_KEY (needed for frames without a cached estimate).')
        pad = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        pad.alpha_composite(im, (ox, oy))
        buf = io.BytesIO(); pad.save(buf, 'PNG')
        req = urllib.request.Request('https://api.pixellab.ai/v2/estimate-skeleton',
                                     data=json.dumps({'image': {'type': 'base64', 'base64': base64.b64encode(buf.getvalue()).decode(), 'format': 'png'}}).encode(),
                                     headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                res = json.load(r)
        except urllib.error.HTTPError as e:
            raise SystemExit(f'PixelLab returned HTTP {e.code} on frame {n}')
        cp.write_text(json.dumps({'pad': [S, ox, oy], 'usage': res.get('usage'), 'keypoints': res['keypoints']}, indent=1), encoding='utf-8')
    est = json.loads(cp.read_text(encoding='utf-8'))
    S, ox, oy = est['pad']
    out.append([{'x': round((k['x'] * S - ox) / W, 4), 'y': round((k['y'] * S - oy) / H, 4), 'label': k['label'],
                 'z_index': int(round(k['z_index'] * 2))} for k in est['keypoints']])
Path(str(pick_p.with_suffix('')) + '.keypoints.json').write_text(json.dumps({'keypoints': out}, indent=1), encoding='utf-8')
print(json.dumps({'frames': len(out)}))
