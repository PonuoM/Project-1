from PIL import Image
from pathlib import Path
p=Path(r'C:/AppServ/www/Projects-1/design/concepts/impact-runtime-codex-v1')
fs=sorted((p/'live-frames').glob('*.png')); ims=[Image.open(f).convert('RGB') for f in fs]
print('frames',len(ims),ims[0].size)
sel=[0,1,2,3,6,7,8,9,11,12,13,15]
w,h=ims[0].size; out=Image.new('RGB',(w*4,h*3),(0,177,64))
for n,i in enumerate(sel):out.paste(ims[i],((n%4)*w,(n//4)*h))
out.save(p/'combo-contact-v1.png')
print('contact',out.size)
