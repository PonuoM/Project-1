"""Prepare a real PixelLab chibi trial. Never prints or persists the API key."""
import argparse
import base64
import io
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'design/pixellab/chibi-modular'
API = 'https://api.pixellab.ai/v2/'
BASE_PROMPT = (
    'One compact chibi fantasy adventurer base body, facing RIGHT in a side view, '
    'matching the reference identity and chunky low-resolution art style. Large rounded '
    'head almost half of total height, dark teal bob hair, tiny simple profile eye, '
    'short torso and legs. Plain fitted ivory undershirt and shorts only, bare feet '
    'and bare hands. NO hat, cloak, scarf, armor, tunic, pants, gloves, boots or weapon. '
    'This is the reusable body beneath interchangeable fashion layers. Standing neutral '
    'combat-ready pose with arms and legs readable and separated. Whole figure about '
    '48 pixels tall, centered in 64x64, feet around row 59, margins for motion. '
    'Crisp deliberate pixel clusters, dark warm one-pixel outline, restrained 24-color '
    'palette, flat 2-3 shade ramps. True transparent background, no floor, no text, '
    'no shadow, no blur, no realistic adult proportions, no extra characters.'
)
ACTIONS = {
    'walk': ('Looping side-view walk toward RIGHT in place: alternate left and right '
             'leg contact, down, passing and up phases with natural opposite arm swing. '
             'Modest head bob. End in the original pose for a seamless loop. Keep the '
             'same chibi proportions, teal hair, undershirt and shorts. No added clothing '
             'or weapon. Stable baseline, transparent background, keep all limbs inside 64x64.'),
    'attack': ('One quick ordinary RIGHT-facing unarmed swing, with a visible gripping '
               'hand reserved for a separate sword layer. Brief anticipation, forceful '
               'forward diagonal swing, short recovery to the exact original pose. '
               'Preserve chibi identity, base undershirt and shorts, no added weapon '
               'or effect baked into body. Keep whole figure inside canvas, transparent.'),
    'slam': ('One heavy overhead RIGHT-facing attack with an empty gripping hand for '
             'a separate weapon. Raise arm above head, short held anticipation, sharply '
             'swing down with torso lean and bent knees, recover to original pose. '
             'Keep chibi head size, hair, undershirt and shorts consistent. Do not add '
             'equipment or slash FX. Entire body inside canvas, transparent.'),
    'leap': ('One RIGHT-facing jumping dash attack: crouch, jump with tucked legs, '
             'lean forward in midair and swing the empty gripping hand down-forward, '
             'land with bent knees, recover to the original pose. Hand is reserved '
             'for a separate weapon layer. Preserve chibi identity and base clothes. '
             'Animate pose only, no large horizontal displacement (game moves root). '
             'Keep all pixels inside 64x64, no weapon or effects, transparent.')
}

def find_key():
    key = os.getenv('PIXELLAB_API_KEY')
    if key or os.name != 'nt':
        return key
    import winreg
    for hive, subkey in [(winreg.HKEY_CURRENT_USER, 'Environment'),
                         (winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')]:
        try:
            with winreg.OpenKey(hive, subkey) as env:
                key = winreg.QueryValueEx(env, 'PIXELLAB_API_KEY')[0]
                if key:
                    return key
        except OSError:
            pass
    return None

def call(endpoint, payload, key):
    request = urllib.request.Request(API + endpoint,
        data=json.dumps(payload).encode('utf-8') if payload is not None else None,
        headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise SystemExit(f'PixelLab HTTP {error.code}. No generation retry was submitted.') from None
    except urllib.error.URLError:
        raise SystemExit('PixelLab connection failed. Check the recorded job before retrying.') from None

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def image_bytes(image):
    return base64.b64decode(image['base64'].split(',')[-1])

def complete(job, folder, key):
    job_id = job.get('background_job_id') or job.get('id')
    if not job_id:
        raise SystemExit('No job ID returned. Inspect job.json; no duplicate request submitted.')
    for _ in range(120):
        result = call('background-jobs/' + job_id, None, key)
        save(folder / 'result.json', result)
        status = result.get('status')
        if status in ('completed', 'failed', 'cancelled'):
            return result
        print('PixelLab job processing...', flush=True)
        time.sleep(5)
    raise SystemExit('Still processing. Run the same command to poll the saved job, not regenerate.')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['base', *ACTIONS])
    parser.add_argument('--first-frame', type=Path)
    parser.add_argument('--dry-run', action='store_true', help='Write request description only; no API call')
    args = parser.parse_args()
    folder = OUT / args.action
    frames = {'walk': 8, 'attack': 8, 'slam': 10, 'leap': 12}
    description = {'endpoint': 'generate-image-v2' if args.action == 'base' else 'animate-with-text-v3',
        'description': BASE_PROMPT if args.action == 'base' else ACTIONS[args.action],
        'image_size': {'width': 64, 'height': 64}, 'no_background': True,
        'status': 'prepared only; no generation submitted'}
    if args.action != 'base':
        description['frame_count'] = frames[args.action]
        description['first_frame_file'] = str(args.first_frame) if args.first_frame else 'owner-selected native base candidate required'
    save(folder / 'prepared-request.json', description)
    if args.dry_run:
        print(f'Prepared {args.action} request. No API call made.')
        return
    key = find_key()
    if not key:
        raise SystemExit('PIXELLAB_API_KEY is not configured. Prepared request saved; no API call made.')
    job_path = folder / 'job.json'
    if job_path.exists():
        job = json.loads(job_path.read_text(encoding='utf-8'))
        print('Polling the existing job; no new generation submitted.', flush=True)
    elif args.action == 'base':
        ref_path = OUT / 'unzoom-result.json'
        if ref_path.exists():
            reference = json.loads(ref_path.read_text(encoding='utf-8'))
        else:
            original = ROOT / 'design/concepts/chibi-v2/hero-concept.png'
            reference = call('unzoom', {'image': {'base64': base64.b64encode(original.read_bytes()).decode('ascii')}, 'quantize': 24}, key)
            save(ref_path, reference)
            (OUT / 'reference-native.png').write_bytes(image_bytes(reference['image']))
        payload = {'description': BASE_PROMPT, 'image_size': {'width': 64, 'height': 64},
                   'no_background': True, 'seed': 141026, 'target_palette': {'max_colors': 24},
                   'reference_images': [{'image': reference['image'], 'size': reference['unzoomed_size'],
                       'usage_description': 'Preserve chibi identity, face, teal bob hair, proportions and pixel style; remove all wearable fashion except base undershirt/shorts.'}]}
        save(folder / 'submitted-request.json', payload)
        job = call('generate-image-v2', payload, key)
        save(job_path, job)
    else:
        if not args.first_frame or not args.first_frame.is_file():
            raise SystemExit('Provide --first-frame with a selected native base candidate. No request made.')
        from PIL import Image
        with Image.open(args.first_frame) as image:
            if image.size != (64, 64):
                raise SystemExit('First frame must be native 64x64, not an enlarged concept.')
        encoded = {'base64': base64.b64encode(args.first_frame.read_bytes()).decode('ascii')}
        payload = {'first_frame': encoded, 'last_frame': encoded, 'action': ACTIONS[args.action],
                   'frame_count': frames[args.action], 'no_background': True, 'seed': 141026}
        save(folder / 'submitted-request.json', payload)
        job = call('animate-with-text-v3', payload, key)
        save(job_path, job)
    print('Job recorded. Polling without submitting additional jobs.', flush=True)
    result = complete(job, folder, key)
    if result.get('status') != 'completed':
        raise SystemExit('Job did not complete successfully. Inspect result.json; no retry submitted.')
    images = result.get('last_response', {}).get('images', [])
    if not images:
        raise SystemExit('No image array returned. Inspect saved result; no regeneration submitted.')
    prefix = 'candidate' if args.action == 'base' else 'frame'
    for i, image in enumerate(images, 1):
        (folder / f'{prefix}-{i:02d}.png').write_bytes(image_bytes(image))
    print(f'Exported {len(images)} original images to {folder}. Usage recorded in result.json.')

if __name__ == '__main__':
    main()
