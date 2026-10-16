import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'design/3d/source/kaykit/Rogue.glb'))
out={'objects':[],'actions':[]}
for o in bpy.data.objects:
    record={'name':o.name,'type':o.type,'dimensions':list(o.dimensions),'location':list(o.location),'scale':list(o.scale)}
    if o.type=='ARMATURE':record['bones']=[{'name':b.name,'head':list(b.head_local),'tail':list(b.tail_local)} for b in o.data.bones]
    if o.type=='MESH':record['materials']=[m.name if m else None for m in o.data.materials];record['groups']=[g.name for g in o.vertex_groups]
    out['objects'].append(record)
for a in bpy.data.actions:out['actions'].append({'name':a.name,'range':list(a.frame_range)})
(ROOT/'design/3d/source/inspection.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out))
