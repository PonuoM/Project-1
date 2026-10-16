"""Build an /animate-with-skeleton-v3 request body from a pose spec (see chibi_skeleton_pose.py). No network.

Usage: python -I design/tools/pixellab_skeleton_payload.py SPEC.pose.json OUT.json --description "..." --action "..."
           [--reference other.png] [--direction east] [--view side] [--seed 0]
--reference swaps the look (another outfit/weapon on the same rest pose) while keeping the motion.
Send it with: python -I design/tools/pixellab_client.py animate-with-skeleton-v3 --payload OUT.json --out JOB.json
"""
import argparse
import base64
import io
import json
from pathlib import Path

from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('spec', type=Path)
ap.add_argument('out', type=Path)
ap.add_argument('--description', required=True)
ap.add_argument('--action', required=True)
ap.add_argument('--reference', type=Path)
ap.add_argument('--direction', default='east')
ap.add_argument('--view', default='side')
ap.add_argument('--seed', type=int, default=0)
a = ap.parse_args()

spec = json.loads(a.spec.read_text(encoding='utf-8'))
kp = json.loads(Path(str(a.spec.with_suffix('')) + '.keypoints.json').read_text(encoding='utf-8'))  # written by chibi_skeleton_pose.py
ref = Image.open(a.reference or (a.spec.parent / spec['reference'])).convert('RGBA')
if ref.size != (spec['referenceSize'],) * 2:
    raise SystemExit(f'reference must be {spec["referenceSize"]}px square like the estimated rest pose')
canvas = Image.new('RGBA', (spec['canvas'],) * 2, (0, 0, 0, 0))
canvas.alpha_composite(ref, tuple(spec['offset']))
buf = io.BytesIO()
canvas.save(buf, 'PNG')
body = {
    'endpoint': 'animate-with-skeleton-v3',
    'description': a.description,
    'action': a.action,
    'direction': a.direction,
    'view': a.view,
    'first_frame': {'type': 'base64', 'base64': base64.b64encode(buf.getvalue()).decode(), 'format': 'png'},
    'first_frame_keypoints': kp['first_frame_keypoints'],
    'keypoints': kp['keypoints'],
    'template_id': 'mannequin',
    'seed': a.seed,
    'no_background': True,
}
a.out.write_text(json.dumps(body), encoding='utf-8')
print(json.dumps({'frames': len(body['keypoints']), 'canvas': spec['canvas'], 'out': str(a.out)}))
