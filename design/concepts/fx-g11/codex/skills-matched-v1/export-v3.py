from pathlib import Path
root=Path(__file__).parent
code=(root/'export-v2.py').read_text(encoding='utf-8').replace('-v2','-v3')
exec(compile(code,str(root/'export-v2.py'),'exec'))
