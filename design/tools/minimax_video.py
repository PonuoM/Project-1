"""Minimal MiniMax H3 video client (V2 API). Credentials only from MINIMAX_API_KEY in the process environment.

  create  OUT_DIR --prompt-file P.txt --first IMG [--last IMG] [--duration 5] [--resolution 768P] [--model MiniMax-H3]
  wait    OUT_DIR            poll the task saved in OUT_DIR/task.json, then download OUT_DIR/video.mp4
  quota                      remaining M Plan usage (read-only)

Billing (owner's M Plan 'Yearly Max', checked 14 Oct 2026): `create` = MiniMax-H3, NOT in the plan -> charged to credits
at $0.08/s (5 s 768P = 400 credits). `create-v1` with MiniMax-Hailuo-2.3 = the plan's included 3 clips/day.
  create-v1 OUT_DIR --prompt-file P.txt --first IMG [--last IMG] [--duration 6] [--resolution 768P] [--model MiniMax-Hailuo-2.3]
            (--last needs --model MiniMax-Hailuo-02)
  wait-v1   OUT_DIR
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = 'https://api.minimax.io'


def key():
    k = os.environ.get('MINIMAX_API_KEY')
    if not k:
        raise SystemExit('Set MINIMAX_API_KEY in this process environment; never write it to project files.')
    return k


def call(url, body=None, method=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, method=method,
                                 headers={'Authorization': 'Bearer ' + key(), 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', 'replace')[:500]
        raise SystemExit(f'MiniMax returned HTTP {e.code}: {detail}')


def data_uri(p):
    p = Path(p)
    fmt = {'.png': 'png', '.jpg': 'jpeg', '.jpeg': 'jpeg', '.webp': 'webp'}[p.suffix.lower()]
    return f'data:image/{fmt};base64,' + base64.b64encode(p.read_bytes()).decode()


def create(a):
    out = Path(a[0])
    o = dict(zip(a[1::2], a[2::2]))
    content = [{'type': 'text', 'text': Path(o['--prompt-file']).read_text(encoding='utf-8').strip()},
               {'type': 'image_url', 'image_url': {'url': data_uri(o['--first'])}, 'role': 'first_frame'}]
    if '--last' in o:
        content.append({'type': 'image_url', 'image_url': {'url': data_uri(o['--last'])}, 'role': 'last_frame'})
    body = {'model': o.get('--model', 'MiniMax-H3'), 'content': content,
            'resolution': o.get('--resolution', '768P'), 'duration': int(o.get('--duration', 5))}
    res = call(API + '/v2/video_generation', body)
    out.mkdir(parents=True, exist_ok=True)
    record = {'task_id': res.get('task_id'), 'response': res,
              'request': {**body, 'content': [{k: (v if k != 'image_url' else '<image>') for k, v in c.items()} for c in content]},
              'inputs': {k: o[k] for k in ('--first', '--last', '--prompt-file') if k in o}}
    (out / 'task.json').write_text(json.dumps(record, indent=1, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({'task_id': record['task_id']}))


def wait(a):
    out = Path(a[0])
    tid = json.loads((out / 'task.json').read_text(encoding='utf-8'))['task_id']
    if not str(tid).isdigit():
        raise SystemExit('bad task id')
    start = time.time()
    while True:
        res = call(f'{API}/v2/query/video_generation/{tid}', method='GET')
        task = res.get('task', res)
        st = task.get('status')
        if st in ('succeeded', 'failed', 'cancelled') or time.time() - start > 1800:
            break
        time.sleep(20)
    (out / 'result.json').write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')
    url = (task.get('content') or {}).get('url')
    if st == 'succeeded' and url:
        if not url.startswith('https://'):
            raise SystemExit('unexpected download url')
        urllib.request.urlretrieve(url, out / 'video.mp4')
    print(json.dumps({'status': st, 'seconds': round(time.time() - start), 'usage': task.get('usage'), 'video': bool(url)}))


def create_v1(a):
    """Hailuo models (V1 API): first frame only. MiniMax-Hailuo-2.3 is the M Plan's included 3 clips/day."""
    out = Path(a[0])
    o = dict(zip(a[1::2], a[2::2]))
    body = {'model': o.get('--model', 'MiniMax-Hailuo-2.3'),
            'prompt': Path(o['--prompt-file']).read_text(encoding='utf-8').strip()[:2000],
            'first_frame_image': data_uri(o['--first']), 'duration': int(o.get('--duration', 6)),
            'resolution': o.get('--resolution', '768P'), 'prompt_optimizer': o.get('--optimizer', 'false') == 'true'}
    if '--last' in o:                          # first & last frame: MiniMax-Hailuo-02 only
        body['last_frame_image'] = data_uri(o['--last'])
    res = call(API + '/v1/video_generation', body)
    if (res.get('base_resp') or {}).get('status_code', 0) != 0:
        raise SystemExit(f"MiniMax refused: {res.get('base_resp')}")
    out.mkdir(parents=True, exist_ok=True)
    (out / 'task.json').write_text(json.dumps({'api': 'v1', 'task_id': res.get('task_id'), 'response': res,
                                               'request': {**body, 'first_frame_image': '<image>', **({'last_frame_image': '<image>'} if 'last_frame_image' in body else {})}}, indent=1, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({'task_id': res.get('task_id')}))


def wait_v1(a):
    out = Path(a[0])
    tid = json.loads((out / 'task.json').read_text(encoding='utf-8'))['task_id']
    if not str(tid).isdigit():
        raise SystemExit('bad task id')
    start = time.time()
    while True:
        res = call(f'{API}/v1/query/video_generation?task_id={tid}', method='GET')
        st = res.get('status')
        if st in ('Success', 'Fail') or time.time() - start > 1800:
            break
        time.sleep(20)
    (out / 'result.json').write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')
    if st == 'Success':
        fid = res['file_id']
        if not str(fid).isdigit():
            raise SystemExit('bad file id')
        f = call(f'{API}/v1/files/retrieve?file_id={fid}', method='GET')
        url = (f.get('file') or {}).get('download_url', '')
        if not url.startswith('https://'):
            raise SystemExit('unexpected download url')
        urllib.request.urlretrieve(url, out / 'video.mp4')
    print(json.dumps({'status': st, 'seconds': round(time.time() - start)}))


def quota(_):
    print(json.dumps(call('https://www.minimax.io/v1/token_plan/remains'), indent=1))


if __name__ == '__main__':
    {'create': create, 'wait': wait, 'create-v1': create_v1, 'wait-v1': wait_v1, 'quota': quota}[sys.argv[1]](sys.argv[2:])
