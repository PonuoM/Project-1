from pathlib import Path
root=Path(__file__).parent
wrapper=(root/'export-v2.py').read_text(encoding='utf-8').replace('-v2','-v3')
wrapper=wrapper.replace("exec(compile(code,", "code=code.replace(\"root/f'{name}-raw-v1.png'\", \"root/(f'{name}-raw-v2.png' if name=='arc-sweep-lr' else f'{name}-raw-v1.png')\")\nexec(compile(code,")
exec(compile(wrapper,str(root/'export-v2.py'),'exec'))
