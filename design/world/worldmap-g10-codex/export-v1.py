"""Save the generated map at the exact requested size; preserve the source PNG.
Does not draw, composite or replace generated map content.
"""
from pathlib import Path
from PIL import Image
import json
D=Path(__file__).parent
src=Image.open(D/'worldmap-raw-v1.png')
assert src.format=='PNG'
out=src.convert('RGB')
if out.size!=(1536,1024):out=out.resize((1536,1024),Image.Resampling.LANCZOS)
p=D/'worldmap-v1.png';assert not p.exists();out.save(p)
report={'sourceSize':list(src.size),'outputSize':list(out.size),'outputFormat':'PNG','sourcePreserved':True,'resizeOnly':src.size!=(1536,1024),'coordinates':'final1536x1024 image, origin top-left, x right, y down'}
p=D/'export-verification-v1.json';assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
