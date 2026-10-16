"""Read-only map inspection and pin validation; QA crops are separate from final art."""
from pathlib import Path
from PIL import Image
import json, math
D=Path(__file__).parent
im=Image.open(D/'worldmap-v1.png');assert im.size==(1536,1024) and im.format=='PNG'
pins=json.loads((D/'zones.json').read_text())
assert len(pins)==30
assert len([p for p in pins if p['kind']=='zone'])==20
assert len([p for p in pins if p['kind'] in ['camp','village']])==5
assert len([p for p in pins if p['kind']=='special'])==5
for c in range(1,6):assert sorted(p['zone'] for p in pins if p.get('city')==c)==[0,1,2,3,4]
for p in pins:assert 0<=p['x']<1536 and 0<=p['y']<1024
assert len({(p['x'],p['y']) for p in pins})==30
nearest=min(math.hypot(a['x']-b['x'],a['y']-b['y']) for i,a in enumerate(pins) for b in pins[i+1:])
# Each unlabelled 128x128 tile is centred exactly on its stored pin.
# Order follows zones.json: five groups of five city pins, then five specials.
sheet=Image.new('RGB',(640,768),'#e8dfcc')
for i,p in enumerate(pins):
 tile=im.crop((p['x']-64,p['y']-64,p['x']+64,p['y']+64))
 sheet.paste(tile,((i%5)*128,(i//5)*128))
p=D/'pin-crops-v1.png';assert not p.exists();sheet.save(p)
report=dict(imageSize=list(im.size),format=im.format,pinCount=len(pins),zoneCount=20,villageCampCount=5,specialCount=5,allPinsInsideImage=True,allCoordinatesUnique=True,minPinDistancePx=round(nearest,2),coordinateOrigin='top-left',xDirection='right',yDirection='down',centres='manually observed on final image, not copied from planned coordinates',cropSheetOrder='rows1-5 cities1-5; columns village/camp, zones1-4; row6 specials in zones.json order')
p=D/'verification-v1.json';assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
