"""Minimal PixelLab v2 connector. Credentials come only from PIXELLAB_API_KEY."""
import argparse,base64,json,os,sys,urllib.request,urllib.error
from pathlib import Path
BASE='https://api.pixellab.ai/v2/'
def call(endpoint,payload=None):
    key=os.environ.get('PIXELLAB_API_KEY')
    if not key:raise SystemExit('Set PIXELLAB_API_KEY in this process environment; do not put credentials in project files.')
    if not endpoint or any(v in endpoint for v in (':','?','#','..')):raise SystemExit('Use a relative PixelLab endpoint only.')
    request=urllib.request.Request(BASE+endpoint.lstrip('/'),data=json.dumps(payload).encode() if payload is not None else None,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(request,timeout=60) as response:return json.load(response)
    except urllib.error.HTTPError as e:
        # Never dump headers/authentication or remote request echoes.
        raise SystemExit(f'PixelLab returned HTTP {e.code}; check account access, request schema and credits.')
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('endpoint',help='e.g. balance, generate-image-v2, background-jobs/JOB_ID')
parser.add_argument('--payload',type=Path,help='JSON body, without credentials')
parser.add_argument('--out',type=Path,help='Write JSON result (may contain generated image base64)')
parser.add_argument('--images-dir',type=Path,help='Decode completed last_response.images to original PNGs')
parser.add_argument('--prefix',default='candidate',help='PNG filename prefix when exporting images')
args=parser.parse_args()
payload=json.loads(args.payload.read_text(encoding='utf-8')) if args.payload else None
if payload is not None:
    recorded_endpoint=payload.pop('endpoint',None)
    if recorded_endpoint and recorded_endpoint.lstrip('/')!=args.endpoint.lstrip('/'):raise SystemExit('The payload belongs to a different endpoint.')
    for key,api_field in [('firstFrameFile','first_frame'),('lastFrameFile','last_frame')]:
        source=payload.pop(key,None)
        if source:payload[api_field]={'base64':base64.b64encode((args.payload.parent/source).read_bytes()).decode()}
result=call(args.endpoint,payload)
if args.out:args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2),encoding='utf-8')
if args.images_dir:
    images=result.get('last_response',{}).get('images',[])
    if not images:raise SystemExit('No completed images in this result; poll the same job later.')
    args.images_dir.mkdir(parents=True,exist_ok=True)
    for i,image in enumerate(images,1):
        data=image['base64'].split(',',1)[-1] if image['base64'].startswith('data:') else image['base64']
        (args.images_dir/f'{args.prefix}-{i:02d}.png').write_bytes(base64.b64decode(data))
print(json.dumps({k:v for k,v in result.items() if k not in ('last_response','images','image')},ensure_ascii=False))
