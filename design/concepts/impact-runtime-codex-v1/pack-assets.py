from pathlib import Path
from PIL import Image
import shutil,json
r=Path(r'C:/AppServ/www/Projects-1'); o=r/'design/concepts/impact-runtime-codex-v1'; a=o/'assets'; a.mkdir()
for name,src in [('slash','slash-c-sword'),('chop','g1-chop-long-sword')]:
 frames=[Image.open(p).convert('RGBA') for p in sorted((r/'design/pixellab/chibi-motion'/src).glob('frame-*.png'))]
 sheet=Image.new('RGBA',(80*len(frames),80));
 for i,im in enumerate(frames): sheet.paste(im,(i*80,0))
 sheet.save(a/(name+'.png'))
for name in ['slime_idle','slime_death']: shutil.copyfile(r/'design/sprites'/(name+'.png'),a/(name+'.png'))
shutil.copyfile(r/'client/node_modules/phaser/dist/phaser.min.js',a/'phaser.min.js')
shutil.copyfile(r/'client/node_modules/phaser/LICENSE.md',a/'phaser-LICENSE.md')
print([(p.name,Image.open(p).size) for p in a.glob('*.png')])
