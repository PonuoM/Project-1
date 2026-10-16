from pathlib import Path
from PIL import Image
import json, numpy as np
D=Path(__file__).parent
def write(name,value):
 p=D/name;assert not p.exists();p.write_text(value,encoding='utf-8')
def save(name,im):
 p=D/name;assert not p.exists();im.save(p)
src=Image.open(D/'land-raw-v1.png').convert('RGBA')
assert src.getchannel('A').getextrema()[0]==0,'Transparent sea required'
small=src.resize((246,184),Image.Resampling.NEAREST)
alpha=small.getchannel('A').point(lambda v:255 if v>=128 else 0)
rgb=small.convert('RGB').quantize(colors=80,method=Image.Quantize.MEDIANCUT).convert('RGB')
rgb.putalpha(alpha)
native=Image.new('RGBA',(256,192));native.paste(rgb,(5,4))
save('land-native-v1.png',native)
save('land-v1.png',native.resize((2048,1536),Image.Resampling.NEAREST))
water=Image.new('RGBA',native.size,'#145e78');water.alpha_composite(native)
save('overview-v1.png',water.convert('RGB').resize((2048,1536),Image.Resampling.NEAREST))
def pos(x,y):return [round(5+x/src.width*246,2),round(4+y/src.height*184,2)]
regions=[
 {'id':1,'name':'ทุ่งหญ้า','nameEn':'Greenhollow','color':'#739647','view':[6,88,112,84]},
 {'id':2,'name':'ป่าเห็ด','nameEn':'Mirewood','color':'#8254a5','view':[89,43,112,84]},
 {'id':3,'name':'ทะเลทราย','nameEn':'Vastsand','color':'#b7802c','view':[118,99,124,93]},
 {'id':4,'name':'ภูเขาหิมะ','nameEn':'Frostspire','color':'#4a94bd','view':[91,0,112,84]},
 {'id':5,'name':'ภูเขาไฟ','nameEn':'Cinderthorn','color':'#ac4d32','view':[162,15,92,69]}]
names=[['ทุ่งหน้าหมู่บ้าน','ไร่กังหันลม','สะพานโทรล','ป่ารังหมาป่า'],['โพรงเห็ดเรืองแสง','บึงวิญญาณ','ทางขนมหวาน','บ้านขนมแม่มด'],['เนินแมงทับทราย','หุบแมงป่อง','สุสานมัมมี่','วิหารตะเกียง'],['ช่องเขาสน','ถ้ำเยติ','ทะเลสาบน้ำแข็ง','พระราชวังน้ำแข็ง'],['ทุ่งเถ้าถ่าน','ผาสุนัขนรก','ประตูหนาม','บัลลังก์มังกร']]
centres=[[(270,785),(345,860),(453,771),(513,666),(497,573)],[(700,594),(650,453),(915,546),(873,432),(811,344)],[(813,818),(945,925),(1083,847),(1219,750),(1033,680)],[(637,184),(747,236),(816,137),(965,197),(1068,113)],[(1101,382),(1155,437),(1224,477),(1260,310),(1289,220)]]
roads=[
 [[(335,830),(365,832),(391,848),(373,875),(334,886)],[(385,811),(401,793),(414,771),(397,751),(390,726)],[(397,705),(410,681),(439,669),(469,671),(499,681)],[(517,639),(524,618),(522,598),(500,604),(480,620)]],
 [[(526,489),(548,502),(574,512),(591,535),(612,554)],[(765,548),(784,564),(801,586),(810,611),(827,634)],[(782,495),(814,480),(850,468),(886,451),(925,432)],[(928,410),(895,398),(860,384),(829,379),(811,357)]],
 [[(819,866),(849,886),(884,895),(919,906),(949,926)],[(1002,906),(1037,894),(1065,872),(1096,867),(1123,854)],[(1167,839),(1194,820),(1225,811),(1250,795),(1274,770)],[(1160,747),(1125,748),(1091,736),(1062,719),(1032,701)]],
 [[(646,235),(670,219),(698,202),(726,199),(754,211)],[(751,177),(773,165),(795,153),(811,141),(822,128)],[(878,221),(906,220),(934,221),(962,225),(988,231)],[(1000,200),(1021,189),(1040,174),(1058,155),(1068,137)]],
 [[(1092,427),(1116,414),(1139,410),(1160,391),(1170,370)],[(1185,473),(1209,468),(1234,470),(1259,454),(1281,435)],[(1183,358),(1207,350),(1231,347),(1250,333),(1255,310)],[(1240,281),(1224,256),(1240,231),(1270,234),(1294,219)]]]
zones=[];stages=[];relocations=[]
a=np.array(native.getchannel('A'))
for ri,r in enumerate(regions):
 for zi,(x,y) in enumerate(centres[ri]):
  px,py=pos(x,y);zones.append(dict(city=ri+1,zone=zi,nameTh=r['name']+' — ค่ายพัก' if zi==0 else names[ri][zi-1],x=px,y=py,kind='camp' if zi==0 else 'zone'))
 for zi,path in enumerate(roads[ri]):
  for si,(x,y) in enumerate(path):
   px,py=pos(x,y)
   if a[round(py),round(px)]==0:
    candidates=[(xx,yy) for yy in range(max(0,round(py)-3),min(192,round(py)+4)) for xx in range(max(0,round(px)-3),min(256,round(px)+4)) if a[yy,xx]>0]
    assert candidates,(r,zi,si)
    old=[px,py];px,py=min(candidates,key=lambda q:(q[0]-px)**2+(q[1]-py)**2);relocations.append(dict(city=r['id'],zone=zi+1,inZone=si+1,original=old,actual=[px,py]))
   stages.append(dict(id=ri*20+zi*5+si+1,city=ri+1,zone=zi+1,inZone=si+1,localStage=zi*5+si+1,x=px,y=py,boss=zi==3 and si==4,zoneName=names[ri][zi],regionName=r['name']))
specials=[]
for key,name,x,y in [('beanstalk','ต้นถั่วยักษ์',506,359),('endless-tower','หอคอยไม่สิ้นสุด',337,398),('sewer-gate','ประตูใต้เมือง',267,862),('harbour','ท่าเรือ',124,651),('fairy-tale-rift','รอยแยกนิทาน',1384,658)]:
 px,py=pos(x,y);specials.append(dict(special=key,nameTh=name,x=px,y=py,kind='special'))
data=dict(width=256,height=192,exportWidth=2048,exportHeight=1536,unit='native art pixels; multiply by8 for exported PNG',regions=regions,zones=zones+specials,stages=stages,clouds=[dict(x=15,y=24,near=False),dict(x=80,y=164,near=False),dict(x=145,y=15,near=False),dict(x=205,y=148,near=False),dict(x=37,y=68,near=True),dict(x=165,y=110,near=True),dict(x=228,y=57,near=True)])
write('map-data.js','window.MAP_DATA='+json.dumps(data,ensure_ascii=False)+';\n')
write('stages.json',json.dumps(stages,ensure_ascii=False,indent=2)+'\n')
write('zones.json',json.dumps(zones+specials,ensure_ascii=False,indent=2)+'\n')
write('map-layout.json',json.dumps({k:v for k,v in data.items() if k not in ['stages','zones']},ensure_ascii=False,indent=2)+'\n')
assert len(stages)==100 and len({s['id'] for s in stages})==100
assert all(a[round(s['y']),round(s['x'])]>0 for s in stages)
assert all(0<=s['x']<256 and 0<=s['y']<192 for s in stages)
report=dict(sourceSize=list(src.size),exportSize=[2048,1536],nativeSize=[256,192],gridBlockPx=8,sourceHasAlpha=True,exportAlphaValues=[0,255],colorLimit=80,stages=100,regions=5,zones=20,stagesPerZone=5,allStagesOnOpaqueTerrain=True,relocations=relocations,stagePlacement='prototype suggestions, not committed game progression')
write('verification-v1.json',json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
