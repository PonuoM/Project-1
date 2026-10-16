"""Prepare foreground/background paper-doll hood masks from the PixelLab texture."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2]/'design/pixellab/chibi-modular'
hood=Image.open(root/'parts/hood.png').convert('RGBA')
# Remove the generated mannequin's dark face insert. Keep cloth, rim and folds.
for y in range(7,36):
    for x in range(8,37):
        r,g,b,a=hood.getpixel((x,y))
        if a and 45<r<125 and 30<g<115 and 20<b<100:hood.putpixel((x,y),(0,0,0,0))
hood.save(root/'parts/hood-open.png')
front=hood.copy();mask=Image.new('L',hood.size);d=ImageDraw.Draw(mask)
d.polygon([(0,0),(37,0),(37,15),(31,18),(27,10),(20,8),(12,12),(9,24),(13,32),(31,32),(37,36),(37,47),(0,47)],fill=255)
front.putalpha(Image.composite(front.getchannel('A'),Image.new('L',hood.size),mask))
front.save(root/'parts/hood-front.png')
record={'source':'parts/hood.png (PixelLab equipment/candidate-02.png)','processing':'native transparent face-opening and occlusion masks, no new paint, generated cloth pixels preserved','opening':'remove mannequin fill, show character face; foreground cloth covers hair crown and rear silhouette'}
(root/'parts/hood-masks.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print('Hood occlusion masks prepared.')
