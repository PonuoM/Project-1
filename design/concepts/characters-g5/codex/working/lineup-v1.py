from PIL import Image
from pathlib import Path
p=Path(r'C:/AppServ/www/Projects-1/design/concepts/characters-g5')
files=['melee-1-v2.png','melee-2-v1.png','melee-3-v1.png','mage-1-v1.png','mage-2-v1.png','mage-3-v1.png','archer-1-v1.png','archer-2-v1.png','archer-3-v1.png']
im=Image.new('RGB',(1536,1536),'#00B140')
for i,f in enumerate(files): im.paste(Image.open(p/f),((i%3)*512,(i//3)*512))
if (p/'lineup-v1.png').exists(): raise RuntimeError('Never overwrite')
im.save(p/'lineup-v1.png')
for f in sorted(p.glob('*.png')): print(f.name,Image.open(f).size)
