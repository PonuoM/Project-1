"""One-command offline Blender -> native pixel sprites. No game or PixelLab calls."""
from pathlib import Path
import argparse,json,subprocess,sys,shutil,time,os
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--blender');parser.add_argument('--preview-only',action='store_true');parser.add_argument('--pack-only',action='store_true');args=parser.parse_args()
start=time.time()
if not args.pack_only:
    blender=args.blender or shutil.which('blender')
    if not blender:
        candidates=sorted(Path('C:/Program Files/Blender Foundation').glob('Blender */blender.exe'))
        blender=str(candidates[-1]) if candidates else None
    if not blender:raise SystemExit('Blender not found. Install it yourself with winget install BlenderFoundation.Blender.')
    subprocess.run([sys.executable,str(ROOT/'design/tools/fetch_kaykit.py')],check=True)
    command=[blender,'--background','--threads','4','--python-exit-code','1','--python',str(ROOT/'design/3d/build_and_render.py'),'--']
    if args.preview_only:command+=['--preview-only']
    subprocess.run(command,check=True)
if not args.preview_only:subprocess.run([sys.executable,str(ROOT/'design/tools/pack_sprites3d.py')],check=True)
print(f'Elapsed {time.time()-start:.1f}s',flush=True)
