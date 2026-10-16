"""Document the successful v2 exports; retain the preflight v1 script."""
from pathlib import Path
p=Path(__file__).parent
source=(p/'document-v1.py').read_text(encoding='utf-8')
source=source.replace('verification-v1.json','verification-v2.json')
source=source.replace('all six `*-v1.png`','all six `*-v2.png`')
source=source.replace('files-v1.json','files-v2.json')
exec(compile(source,str(p/'document-v1.py'),'exec'))
