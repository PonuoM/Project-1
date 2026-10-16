"""Poll a PixelLab background job until it finishes, then save the JSON and its images. Read-only (no new generation).

Usage: python -I design/tools/pixellab_wait.py JOB_ID OUT_DIR [--prefix frame] [--timeout 900]
Credentials come only from PIXELLAB_API_KEY in the process environment.
"""
import argparse
import base64
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('job')
ap.add_argument('out', type=Path)
ap.add_argument('--prefix', default='frame')
ap.add_argument('--timeout', type=int, default=900)
a = ap.parse_args()
key = os.environ.get('PIXELLAB_API_KEY') or exit('Set PIXELLAB_API_KEY in this process environment.')
if not all(c.isalnum() or c == '-' for c in a.job):
    exit('job id must be a plain UUID')
start = time.time()
while True:
    req = urllib.request.Request(f'https://api.pixellab.ai/v2/background-jobs/{a.job}', headers={'Authorization': 'Bearer ' + key})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            res = json.load(r)
    except urllib.error.HTTPError as e:
        exit(f'PixelLab returned HTTP {e.code} while polling')
    status = res.get('status')
    if status in ('completed', 'failed') or time.time() - start > a.timeout:
        break
    time.sleep(15)
a.out.mkdir(parents=True, exist_ok=True)
lr = res.get('last_response') or {}
images = lr.get('images') or []
# single-image endpoints (edit-image-pixen...) return image + quantized_image instead of images[]
singles = {k: lr[k] for k in ('image', 'quantized_image') if isinstance(lr.get(k), dict) and lr[k].get('base64')}
slim = json.loads(json.dumps(res))                # keep the record small: images are saved as PNGs below
if images:
    slim['last_response']['images'] = f'{len(images)} images -> {a.prefix}-NN.png'
for k in singles:
    slim['last_response'][k] = f'-> {a.prefix}-{k}.png'
    data = singles[k]['base64'].split(',', 1)[-1]
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / f'{a.prefix}-{k}.png').write_bytes(base64.b64decode(data))
(a.out / 'result.json').write_text(json.dumps(slim, indent=1), encoding='utf-8')
for i, im in enumerate(images):
    data = im['base64'].split(',', 1)[-1]
    (a.out / f'{a.prefix}-{i:02d}.png').write_bytes(base64.b64decode(data))
print(json.dumps({'status': status, 'images': len(images) + len(singles), 'usage': res.get('usage') or (res.get('last_response') or {}).get('usage'),
                  'seconds': round(time.time() - start)}))
