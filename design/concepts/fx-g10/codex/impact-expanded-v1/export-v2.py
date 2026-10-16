"""Register generated contact cores and reserve room for expansion at torso height."""
from pathlib import Path
D=Path(__file__).parent
code=(D/'export-v1.py').read_text()
code=code.replace('-v1.png','-v2.png').replace('-raw-v2.png','-raw-v1.png').replace("D/'effects-v1.json'","D/'effects-v2.json'")
anchor='  im=Image.fromarray(a);frames.append(im);native.paste(im,(col*64,row*64))'
replacement='''  # Observed contact bases, not per-frame bounding-box recentering:
  # drifting sparks remain drifting relative to the launch position.
  if s['id']=='fire':
   anchors=[(32,36),(30,37),(23,45),(22,48),(17,49),(21,49),(22,49),(24,49),(24,49),(24,49),(24,49),(24,49)]
   ax,ay=anchors[i];factor=.70
  elif s['id']=='poison-slash':
   anchors=[(30,41),(23,42),(20,46),(20,46),(14,42),(19,42),(22,40),(25,38),(29,35),(32,32),(32,32),(32,32)]
   ax,ay=anchors[i];factor=.75
  elif s['id']=='ice-shatter':ax,ay=32,39;factor=.85
  else:ax,ay=32,32;factor=.85
  registered=np.zeros_like(a)
  for yy in range(3,61):
   for xx in range(3,61):
    sx=round(ax+(xx-32)/factor);sy=round(ay+(yy-32)/factor)
    if 0<=sx<64 and 0<=sy<64:registered[yy,xx]=a[sy,sx]
  a=registered
  im=Image.fromarray(a);frames.append(im);native.paste(im,(col*64,row*64))'''
assert anchor in code;code=code.replace(anchor,replacement)
exec(compile(code,str(D/'export-v1.py'),'exec'))
