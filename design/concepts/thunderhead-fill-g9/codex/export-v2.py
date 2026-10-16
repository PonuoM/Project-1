"""Register top and right fill strips separately; never move original pixels."""
from pathlib import Path
D=Path(__file__).parent
code=(D/'export-v1.py').read_text()
code=code.replace("name+'-v1.png'","name+'-v2.png'").replace("D/'verification-v1.json'","D/'verification-v2.json'")
anchor='  af=np.any(a!=BG,axis=2)&~protected'
replacement='''  # A generated full-sheet edit can shift the elbow independently of the club.
  # Register right-edge fill against the original right-edge anatomical region.
  if np.any(ofg[pad:,w-1]):
   rmask=np.zeros_like(protected);rmask[pad:,w-16:w]=True
   rbest=(-1,0,0,a)
   raw=palette[nearest]
   for ry in range(-14,15):
    for rx in range(-10,15):
     cand=shifted(raw,rx,ry);cf=np.any(cand!=BG,axis=2)
     join=np.sum(cf[pad:,w]&ofg[pad:,w-1])/max(1,np.sum(ofg[pad:,w-1]))
     rs=.75*overlap(ofg,cf,rmask)+.25*join
     if rs>rbest[0]:rbest=(rs,rx,ry,cand)
   a[:,w:]=rbest[3][:,w:]
  af=np.any(a!=BG,axis=2)&~protected'''
assert anchor in code
code=code.replace(anchor,replacement)
exec(compile(code,str(D/'export-v1.py'),'exec'))
