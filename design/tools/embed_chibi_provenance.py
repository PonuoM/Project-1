"""Embed generation prompts/origins in PNG metadata without changing pixel data."""
import json
from pathlib import Path
from PIL import Image,PngImagePlugin
root=Path(__file__).resolve().parents[2]/'design/pixellab/chibi-modular'
def embed(path,prompt):
    with Image.open(path) as image:
        info=PngImagePlugin.PngInfo()
        for key,value in image.info.items():
            if isinstance(value,str) and key!='generation_prompt':info.add_text(key,value)
        info.add_text('generation_prompt',prompt)
        image.save(path,pnginfo=info)
for folder in ['base','walk','attack','slam','leap']:
    request=json.loads((root/folder/'submitted-request.json').read_text())
    prompt=request.get('description') or request['action']
    for path in (root/folder).glob('*.png'):embed(path,prompt if path.name.startswith(('candidate-','frame-')) else 'Nearest-neighbor inspection/contact sheet of original PixelLab outputs. Source prompt: '+prompt)
prompt=json.loads((root/'equipment-request.json').read_text())['description']
for path in (root/'equipment').glob('*.png'):embed(path,prompt)
for path in (root/'parts').glob('*.png'):embed(path,'Extracted component of PixelLab equipment/candidate-02.png; crop provenance in parts/provenance.json. Source prompt: '+prompt)
embed(root/'reference-native.png','PixelLab unzoom output of owner-selected design/concepts/chibi-v2/hero-concept.png; no new character generation in this reference preparation.')
concept=root.parents[1]/'concepts/chibi-v2/hero-concept.png'
embed(concept,concept.with_name('prompt.txt').read_text())
print('PNG metadata recorded; raster pixels unchanged.')
