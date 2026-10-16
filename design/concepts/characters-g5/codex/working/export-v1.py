from PIL import Image
from pathlib import Path
p=Path(r'C:/AppServ/www/Projects-1/design/concepts/characters-g5')
for src in p.glob('*-raw-v*.png'):
 dst=p/src.name.replace('-raw','')
 if not dst.exists():
  im=Image.open(src).convert('RGB'); im.resize((64,64),Image.Resampling.NEAREST).resize((512,512),Image.Resampling.NEAREST).save(dst)
  print(dst.name, Image.open(dst).size)
