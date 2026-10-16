"""Cut original PixelLab equipment sprites into transparent component PNGs; no repainting."""
import json
from pathlib import Path
from PIL import Image

root=Path(__file__).resolve().parents[2]/'design/pixellab/chibi-modular'
source=root/'equipment/candidate-02.png'
image=Image.open(source).convert('RGBA')
regions={'hood':(0,0,52,68),'shirt':(52,0,91,82),'pants':(92,0,128,49),
         'sword':(0,88,65,124),'wrist':(65,88,86,122),'boots':(88,85,128,125)}
out=root/'parts';out.mkdir(exist_ok=True)
record={}
def largest_component(part):
    pixels=part.load();seen=set();groups=[]
    for y in range(part.height):
        for x in range(part.width):
            if (x,y) in seen or not pixels[x,y][3]:continue
            stack=[(x,y)];group=[];seen.add((x,y))
            while stack:
                px,py=stack.pop();group.append((px,py))
                for nx in range(max(0,px-1),min(part.width,px+2)):
                    for ny in range(max(0,py-1),min(part.height,py+2)):
                        if (nx,ny) not in seen and pixels[nx,ny][3]:seen.add((nx,ny));stack.append((nx,ny))
            groups.append(group)
    keep=max(groups,key=len);clean=Image.new('RGBA',part.size)
    for x,y in keep:clean.putpixel((x,y),pixels[x,y])
    return clean,sum(len(g) for g in groups)-len(keep)
for name,region in regions.items():
    part=image.crop(region)
    part,discarded=largest_component(part)
    bounds=part.getbbox()
    if not bounds:raise SystemExit(f'Empty component: {name}')
    part=part.crop(bounds)
    part.save(out/f'{name}.png')
    record[name]={'file':f'parts/{name}.png','source':'equipment/candidate-02.png','region':region,'trim':bounds,'size':part.size,'discardedNeighborPixels':discarded,'processing':'lossless transparent crop and removal of detached neighboring-item pixels; original component colors retained'}
(out/'provenance.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({k:v['size'] for k,v in record.items()}))
