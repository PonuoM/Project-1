"""Inspect original PixelLab sprites without changing them."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw

parser=argparse.ArgumentParser()
parser.add_argument('folder',type=Path)
parser.add_argument('--pattern',default='candidate-*.png')
parser.add_argument('--columns',type=int,default=4)
args=parser.parse_args()
files=sorted(args.folder.glob(args.pattern))
if not files: raise SystemExit('No original images yet.')
images=[Image.open(p).convert('RGBA') for p in files]
zoom=5
cellw=max(im.width for im in images)*zoom+24
cellh=max(im.height for im in images)*zoom+48
sheet=Image.new('RGB',(args.columns*cellw,((len(files)+args.columns-1)//args.columns)*cellh),'#20282b')
d=ImageDraw.Draw(sheet)
for i,(path,im) in enumerate(zip(files,images)):
    x=(i%args.columns)*cellw+12;y=(i//args.columns)*cellh+10
    sheet.paste(im.resize((im.width*zoom,im.height*zoom),Image.Resampling.NEAREST),(x,y),im.resize((im.width*zoom,im.height*zoom),Image.Resampling.NEAREST))
    d.text((x,y+im.height*zoom+8),f'{path.name} / {im.width}x{im.height}',fill='#f4ead5')
sheet.save(args.folder/'contact-sheet.png')
print(args.folder/'contact-sheet.png')
