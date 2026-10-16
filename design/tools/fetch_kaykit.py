"""Fetch pinned source assets with their original CC0 license."""
from pathlib import Path
import urllib.request,json,hashlib
ROOT=Path(__file__).resolve().parents[2]/'design/3d/source/kaykit'
ROOT.mkdir(parents=True,exist_ok=True)
BASE='https://raw.githubusercontent.com/KayKit-Game-Assets/KayKit-Character-Pack-Adventures-1.0/main/'
PATHS=['LICENSE.txt','README.md',*[f'addons/kaykit_character_pack_adventures/Characters/gltf/{name}.glb' for name in ['Rogue','Barbarian','Rogue_Hooded']], 'addons/kaykit_character_pack_adventures/Assets/fbx/sword_1handed.fbx']
records=[]
for source in PATHS:
    path=ROOT/Path(source).name
    if not path.exists():path.write_bytes(urllib.request.urlopen(BASE+source,timeout=60).read())
    data=path.read_bytes()
    records.append({'file':path.name,'url':BASE+source,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'license':'CC0-1.0'})
(ROOT/'sources.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print([(r['file'],r['bytes']) for r in records])
