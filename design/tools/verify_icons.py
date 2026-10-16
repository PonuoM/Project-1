"""Check native PNGs and exact ICO payloads, with no implicit resizing."""
import json,struct,io
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'icons'
P=json.loads((ROOT/'tokens.json').read_text())['palette'];colors={tuple(bytes.fromhex(c[1:])) for c in P.values()}
results=[]
for prefix,sizes in [('icon',(16,24,32,48,64,128,256)),('tray',(16,32))]:
    for size in sizes:
        im=Image.open(OUT/f'{prefix}-{size}.png');assert im.mode=='RGBA' and im.size==(size,size)
        pixels=list(im.get_flattened_data());assert {p[3] for p in pixels}<={0,255}
        assert any(p[3]==0 for p in pixels) and any(p[3]==255 for p in pixels)
        opaque={p[:3] for p in pixels if p[3]};assert opaque<=colors and len(opaque)<=8
        assert im.getpixel((0,0))[3]==0
        results.append({'file':f'{prefix}-{size}.png','size':size,'colors':len(opaque)})
data=(OUT/'app.ico').read_bytes();assert struct.unpack_from('<HHH',data)==(0,1,6)
sizes=[]
for i in range(6):
    w,h,_,_,planes,depth,length,offset=struct.unpack_from('<BBBBHHII',data,6+i*16)
    size=w or 256;assert (h or 256)==size and planes==1 and depth==32
    assert data[offset:offset+length]==(OUT/f'icon-{size}.png').read_bytes()
    assert Image.open(io.BytesIO(data[offset:offset+length])).size==(size,size);sizes.append(size)
assert sizes==[16,24,32,48,64,256]
assert Image.open(OUT/'app.ico').ico.sizes()=={(n,n) for n in sizes}
report={'result':'pass','pngs':results,'icoSizes':sizes,'checks':['native dimensions','RGBA binary alpha','palette and color budget','transparent corners','ICO native PNG payload identity','ICO decoded size directory']}
(ROOT/'qa/icons.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS: 9 PNG icons and ICO with 6 independently drawn sizes.')
