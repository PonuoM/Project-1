from pathlib import Path
root=Path(__file__).parent
code=(root/'export-v1.py').read_text(encoding='utf-8')
code=code.replace('-v1','-v2').replace("f'{name}-raw-v2.png'","f'{name}-raw-v1.png'")
code=code.replace('factor=min(58/cw,58/raw.height)\n    sw,sh=round(cw*factor),round(raw.height*factor)', '''boxes=[]
    for k in range(4):
        a=np.asarray(raw.crop((round(k*cw),0,round((k+1)*cw),raw.height)),dtype=np.int16).mean(axis=2)
        yy,xx=np.where(a>30)
        boxes.append((int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)))
    box=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
    bw,bh=box[2]-box[0],box[3]-box[1]
    factor=min(58/bw,58/bh)
    sw,sh=round(bw*factor),round(bh*factor)''')
code=code.replace("cell=cell.resize((sw,sh),Image.Resampling.NEAREST)","cell=cell.crop(box).resize((sw,sh),Image.Resampling.NEAREST)")
exec(compile(code,str(root/'export-v1.py'),'exec'))
