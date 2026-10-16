"""Finish the recorded equipment job, then request the four authorized native animations."""
import json
from pathlib import Path
import subprocess
import sys
from chibi_pixellab_trial import OUT, ROOT, complete, find_key, image_bytes

key=find_key()
if not key:raise SystemExit('PixelLab key missing; no requests made.')
job=json.loads((OUT/'equipment-job.json').read_text(encoding='utf-8'))
folder=OUT/'equipment'
folder.mkdir(parents=True,exist_ok=True)
result=complete(job,folder,key)
if result.get('status')!='completed':raise SystemExit('Equipment job failed; no animation requests submitted.')
images=result.get('last_response',{}).get('images',[])
for i,image in enumerate(images,1):(folder/f'candidate-{i:02d}.png').write_bytes(image_bytes(image))
print(f'Equipment: exported {len(images)} original sheets.',flush=True)
first=OUT/'base/candidate-01.png'
for action in ['walk','attack','slam','leap']:
    print(f'Starting {action}.',flush=True)
    subprocess.run([sys.executable,str(ROOT/'design/tools/chibi_pixellab_trial.py'),action,'--first-frame',str(first)],check=True)
print('All authorized native animations exported.',flush=True)
