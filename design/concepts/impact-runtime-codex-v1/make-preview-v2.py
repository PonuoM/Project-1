from PIL import Image
from pathlib import Path
p=Path(r'C:/AppServ/www/Projects-1/design/concepts/impact-runtime-codex-v1'); ims=[Image.open(f).convert('RGB') for f in sorted((p/'live-frames-v2').glob('*.png'))]
large=[im.resize((960,360),Image.Resampling.NEAREST) for im in ims]
large[0].save(p/'combo-preview-v2.png',save_all=True,append_images=large[1:],duration=50,loop=0)
sel=[0,1,2,3,6,7,8,9,11,12,13,15];out=Image.new('RGB',(1280,360),(0,177,64))
for n,i in enumerate(sel):out.paste(ims[i],((n%4)*320,(n//4)*120))
out.save(p/'combo-contact-v2.png')
for f in sorted(p.rglob('*.png')):
 im=Image.open(f); print(str(f.relative_to(p)), im.size, getattr(im,'n_frames',1))
