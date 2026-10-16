"""Retain thin silhouette tips during reduction; keep v1 attempts untouched."""
from pathlib import Path
p=Path(__file__).parent
source=(p/'export-v1.py').read_text(encoding='utf-8')
source=source.replace('m=m.resize((w,h),Image.Resampling.NEAREST)',
 'm=m.resize((w,h),Image.Resampling.BOX).point(lambda v: 255 if v else 0)')
source=source.replace("name+'-v1.png'", "name+'-v2.png'")
source=source.replace('lineup-v1.png','lineup-v2.png').replace('verification-v1.json','verification-v2.json')
exec(compile(source,str(p/'export-v1.py'),'exec'))
