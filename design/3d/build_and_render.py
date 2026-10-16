"""Build a rigged source scene and render native atlases, color+depth per layer."""
import bpy,math,json,sys,time
from pathlib import Path
from mathutils import Vector,Matrix
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'design/sprites3d/adventurer';RAW=OUT/'raw';RAW.mkdir(parents=True,exist_ok=True)
preview='--preview-only' in sys.argv
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'design/3d/source/kaykit/Rogue.glb'))
scene=bpy.context.scene;rig=bpy.data.objects['Rig']
for o in list(bpy.data.objects):
    if o.type=='MESH' and not o.name.startswith('Rogue_'):bpy.data.objects.remove(o,do_unlink=True)
cape=bpy.data.objects.get('Rogue_Cape')
if cape:bpy.data.objects.remove(cape,do_unlink=True)
scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=1;scene.eevee.taa_samples=1;scene.render.filter_size=0.0
scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.color_depth='8';scene.render.resolution_percentage=100
scene.view_settings.view_transform='Raw';scene.render.dither_intensity=0;scene.view_settings.look='None';scene.world=bpy.data.worlds.new('fixed ambient');scene.world.color=(.4,.4,.4)
scene.render.use_file_extension=True
# Materials emit DATA, not colour (Claude, Prompt 8.1 takeover): R = material id, G = light band
# (0 / .5 / 1). pack_sprites3d.py paints each id with ramps sampled from the owner's reference, so the
# body matches the PixelLab head exactly instead of nearest-colour guessing.
BAND_EDGES=(.42,.74)
MATERIAL_IDS={'skin':1,'underwear':2,'cloth':3,'scarf':4,'red':5,'brass':6,'trousers':7,'leather':8,'blade':9,'steel':10,'plum':11,'grip':12,'iron':13}
def toon(name,mid):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();links=m.node_tree.links
    diffuse=n.new('ShaderNodeBsdfDiffuse');diffuse.inputs['Color'].default_value=(1,1,1,1)
    lighting=n.new('ShaderNodeShaderToRGB');links.new(diffuse.outputs[0],lighting.inputs[0])
    value=n.new('ShaderNodeRGBToBW');links.new(lighting.outputs[0],value.inputs[0])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='CONSTANT';els=ramp.color_ramp.elements
    els[0].position=0;els[0].color=(0,0,0,1);els[1].position=BAND_EDGES[0];els[1].color=(.5,.5,.5,1);e=els.new(BAND_EDGES[1]);e.color=(1,1,1,1)
    links.new(value.outputs[0],ramp.inputs[0]);band=n.new('ShaderNodeRGBToBW');links.new(ramp.outputs['Color'],band.inputs[0])
    combine=n.new('ShaderNodeCombineColor');combine.inputs['Red'].default_value=mid/255;combine.inputs['Blue'].default_value=0;links.new(band.outputs[0],combine.inputs['Green'])
    emission=n.new('ShaderNodeEmission');links.new(combine.outputs[0],emission.inputs['Color']);output=n.new('ShaderNodeOutputMaterial');links.new(emission.outputs[0],output.inputs[0]);return m
mats={k:toon(k,i) for k,i in MATERIAL_IDS.items()}
mats['head']=mats['teal_hair']=mats['skin']  # the KayKit head is never rendered (Prompt 8.1)
texture=None
groups={'body':[]};sources=[o for o in bpy.data.objects if o.type=='MESH']
for o in sources:
    if 'Head' in o.name:
        o.hide_render=True
        continue
    o.data.materials.clear();o.data.materials.append(mats['head' if 'Head' in o.name else 'underwear' if 'Body' in o.name else 'skin']);groups['body'].append(o)
    if 'Head' in o.name:
        o.data.materials.append(mats['teal_hair']);uv=o.data.uv_layers.active.data;pixels=list(texture.pixels);width,height=texture.size
        for p in o.data.polygons:
            coord=sum((uv[i].uv for i in p.loop_indices),Vector((0,0)))/len(p.loop_indices);x=min(width-1,max(0,int(coord.x*width)));y=min(height-1,max(0,int(coord.y*height)));r,g,b=pixels[(y*width+x)*4:(y*width+x)*4+3]
            if .25<r<.8 and r>g*1.3 and r>b*1.5:
                p.material_index=1
                for i in p.vertices:
                    v=o.data.vertices[i]
                    if v.co.z<1.48 and v.co.y>-.1:v.co.z=1.48+(v.co.z-1.2)*.2
def shell(source,name,material,predicate=lambda v:True,inflate=.015):
    verts=[];faces=[];mapping={}
    for poly in source.data.polygons:
        if not all(predicate(source.data.vertices[i].co) for i in poly.vertices):continue
        face=[]
        for i in poly.vertices:
            if i not in mapping:mapping[i]=len(verts);v=source.data.vertices[i];verts.append(v.co+v.normal*inflate)
            face.append(mapping[i])
        faces.append(face)
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);scene.collection.objects.link(o);o.data.materials.append(material)
    for g in source.vertex_groups:o.vertex_groups.new(name=g.name)
    for old,new in mapping.items():
        for g in source.data.vertices[old].groups:o.vertex_groups[g.group].add([new],g.weight,'REPLACE')
    modifier=o.modifiers.new('same skeleton','ARMATURE');modifier.object=rig;groups.setdefault(name.split('__')[0],[]).append(o);return o
body=next(o for o in sources if 'Body' in o.name);arms=[o for o in sources if 'Arm' in o.name];legs=[o for o in sources if 'Leg' in o.name]
for item,mat in [('tunic',mats['cloth']),('plate',mats['steel']),('plum',mats['plum'])]:
    shell(body,f'chest_{item}__body',mat,inflate=.025 if item!='plate' else .04)
    if item=='plate':
        for i,o in enumerate(arms):shell(o,f'chest_{item}__sleeve{i}',mat,lambda v:v.z>.98,inflate=.03)
for item,mat in [('trousers',mats['trousers']),('leather',mats['leather'])]:
    for i,o in enumerate(legs):shell(o,f'legs_{item}__{i}',mat,lambda v:v.z>.40,inflate=.024)
for item,mat in [('boots',mats['leather']),('greaves',mats['steel'])]:
    for i,o in enumerate(legs):shell(o,f'boots_{item}__{i}',mat,lambda v:v.z<.28,inflate=.03)
for item,mat in [('bracer',mats['brass']),('cuff',mats['underwear'])]:
    for i,o in enumerate(arms):
        if item=='bracer' and 'Right' not in o.name:continue
        shell(o,f'wrist_{item}__{i}',mat,lambda v:abs(v.x)>.51,inflate=.026)
def rigid(name,mesh,bone,material):
    o=bpy.data.objects.new(name,mesh);scene.collection.objects.link(o);o.data.materials.clear();o.data.materials.append(material);g=o.vertex_groups.new(name=bone);g.add(list(range(len(mesh.vertices))),1,'REPLACE');mod=o.modifiers.new('bone parent','ARMATURE');mod.object=rig;groups.setdefault(name.split('__')[0],[]).append(o);return o
def primitive(name,location,scale,mat,bone,kind='cube'):
    if kind=='sphere':bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=location)
    else:bpy.ops.mesh.primitive_cube_add(size=1,location=location)
    o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);mesh=o.data;bpy.data.objects.remove(o,do_unlink=True);return rigid(name,mesh,bone,mat)
head=next(o for o in sources if 'Head' in o.name);headbounds=[head.matrix_world@Vector(v) for v in head.bound_box];hcenter=sum(headbounds,Vector())/8
for item,mat in []: # Prompt 8.1: hats authored in pixel space around the ORIGINAL head.
    # Open front shell: actual geometry opening, not a face pasted onto clothing.
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=10,location=hcenter);temp=bpy.context.object;temp.scale=(.60,.56,.58);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    coords=[v.co.copy() for v in temp.data.vertices];faces=[]
    for p in temp.data.polygons:
        center=sum((coords[i] for i in p.vertices),Vector())/len(p.vertices)
        if center.y<hcenter.y-.22 and hcenter.z-.36<center.z<hcenter.z+.24:continue
        faces.append(list(p.vertices))
    mesh=bpy.data.meshes.new(item+' shell');mesh.from_pydata(coords,[],faces);mesh.update();bpy.data.objects.remove(temp,do_unlink=True);rigid(f'hat_{item}__shell',mesh,'head',mat)
    if item=='helm':primitive('hat_helm__plume',(0,.10,hcenter.z+.59),(.18,.32,.30),mats['red'],'head')
    else:primitive('hat_hood__collar',(0,.08,hcenter.z-.42),(.72,.52,.16),mat,'head')
primitive('body__neck',(0,0,1.23),(.26,.25,.22),mats['skin'],'head')
for item in ['tunic','plum']:
    primitive(f'chest_{item}__scarf',(0,-.01,1.04),(.58,.48,.16),mats['scarf'],'chest',kind='sphere')
    primitive(f'chest_{item}__sash',(0,-.025,.66),(.84,.62,.12),mats['red'],'hips')
for item,length,mat in [('sword',.85,mats['blade']),('sabre',.95,mats['brass'])]:
    # Model coordinates in handslot.r's local space, transform through rest bone.
    rest=rig.data.bones['handslot.r'].matrix_local
    parts=[('blade',(0,length*.53+.12,0),(.2,length,.2),mat),('grip',(0,0,0),(.12,.22,.12),mats['grip']),('guard',(0,.12,0),(.36,.08,.32),mats['brass'])]
    for name,loc,scale,material in parts:
        o=primitive(f'weapon_{item}__{name}',(0,0,0),scale,material,'handslot.r')
        transform=rest@Matrix.Translation(Vector(loc))
        for v in o.data.vertices:v.co=transform@v.co
        if name=='grip':o['grip']=True;o['grip_local']=[0,0,0]
        if name=='blade':o['tip_local']=[0,length+.12,0]
groups={k:v for k,v in groups.items() if v}
# Camera looks from anatomical right side; character's -Y forward projects RIGHT.
AZIMUTH=math.radians(35)  # rotate from the right side toward the face: the head art is a 3/4 view
bpy.ops.object.camera_add(location=(-6*math.cos(AZIMUTH),-6*math.sin(AZIMUTH),.674));camera=bpy.context.object;camera.rotation_euler=(Vector((0,0,.674))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=4.4;scene.camera=camera
camR=camera.rotation_euler.to_matrix();cam_right=(camR@Vector((1,0,0))).normalized();cam_up=(camR@Vector((0,1,0))).normalized();cam_forward=(camR@Vector((0,0,-1))).normalized()
bpy.ops.object.light_add(type='SUN',location=(-3,-4,5));light=bpy.context.object;light.rotation_euler=(-cam_up*.55+cam_right*.45+cam_forward*.70).normalized().to_track_quat('-Z','Y').to_euler();light.data.energy=2
light.data.use_shadow=False
scene.render.resolution_x=scene.render.resolution_y=96
animation={
 'idle':{'action':'Idle','samples':[0,7,14,21],'frameMs':[250]*4,'impact':None,'loop':True},
 'walk':{'action':'Walking_A','samples':[0,3,6,9,13,16,19,23],'frameMs':[85]*8,'impact':None,'loop':True},
 'attack':{'action':'1H_Melee_Attack_Slice_Diagonal','samples':[0,4,8,11,14,18,24],'frameMs':[60,90,30,40,80,65,100],'impact':3,'loop':False},
 'slam':{'action':'1H_Melee_Attack_Chop','samples':[0,4,7,10,12,14,17,22,25.6],'frameMs':[35,70,90,30,45,80,90,70,65],'impact':4,'loop':False},
 'leap':{'action':'1H_Melee_Attack_Chop','samples':[0,3,6,9,11,13,16,19,23,25.6],'frameMs':[45,60,80,75,30,45,70,90,70,60],'impact':5,'loop':False},
}
# Remove glTF NLA tracks: one explicit action and one source rig in every pass.
for track in list(rig.animation_data.nla_tracks):rig.animation_data.nla_tracks.remove(track)
def set_pose(name,i):
    spec=animation[name];rig.animation_data.action=bpy.data.actions[spec['action']];scene.frame_set(int(spec['samples'][i]),subframe=spec['samples'][i]%1)
    # Body weight (Pixelblog 9): lean back on the wind-up, throw the chest forward on impact, settle after.
    lean={'attack':[0,-.45,-.35,.85,.70,.30,0],'slam':[0,.15,.25,.20,.65,.60,.35,.12,0],'leap':[0,.15,.25,.20,.65,.60,.35,.12,0,.0]}
    if name in lean:
        strength=lean[name][i]
        pb=rig.pose.bones['spine'];pb.rotation_mode='QUATERNION';from mathutils import Quaternion;pb.rotation_quaternion=pb.rotation_quaternion@Quaternion((1,0,0),-.22*strength)
    bpy.context.view_layer.update()
    # Re-author the right-arm swing in the side-view plane. Raw clips swing toward
    # the camera, which hides their arc in pixels. These are actual bone poses.
    # Walking with a sword: KayKit's walk is unarmed, so the sword arm keeps the idle grip (blade down-forward)
    # with a small swing in step, instead of swinging the blade up across the face.
    swing=[0,4,8,4,0,-4,-8,-4]
    poses={'idle':[(-65,-40,-30)]*4,'walk':[(-65+d,-40+d,-30+d/2) for d in swing],
      'attack':[(-60,-25,-30),(125,110,145),(45,20,40),(-10,-25,-35),(-50,-60,-80),(-65,-50,-55),(-60,-25,-30)],
      'slam':[(-60,-25,-30),(70,110,95),(100,120,95),(35,30,45),(-25,-40,-65),(-60,-65,-80),(-65,-50,-65),(-65,-35,-40),(-60,-25,-30)],
      'leap':[(-60,-25,-30),(65,110,95),(90,110,95),(65,65,65),(30,20,35),(-15,-25,-50),(-55,-60,-75),(-65,-50,-60),(-65,-35,-40),(-60,-25,-30)]}
    if name in poses:
        def aim(bone,angle):
            pb=rig.pose.bones[bone];pos=pb.head.copy();a=math.radians(angle);direction=Vector((0,-math.cos(a),math.sin(a)))
            m=direction.to_track_quat('Y','X').to_matrix().to_4x4();m.translation=pos;pb.matrix=m;bpy.context.view_layer.update()
        upper,lower,blade=poses[name][i];aim('upperarm.r',upper);aim('lowerarm.r',lower);aim('handslot.r',blade)
set_pose('idle',0)
for o in [o for group in groups.values() for o in group]:o.hide_render=not(o in groups['body'] or any(o in groups.get(k,[]) for k in ['chest_tunic','legs_trousers','boots_boots','wrist_bracer','weapon_sword']))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'design/3d/adventurer.blend'))
if preview:
    scene.render.filepath=str(ROOT/'design/3d/native-preview.png');bpy.ops.render.render(write_still=True);raise SystemExit(0)
frames=[];anchors={};snapshots={k:[] for k in groups};deps=bpy.context.evaluated_depsgraph_get()
for name,spec in animation.items():
    anchors[name]=[]
    for i in range(len(spec['samples'])):
        set_pose(name,i);deps.update();frozen={}
        # Translate vertical root so all grounded clips plant lowest vertex at floor.
        allcoords=[]
        for o in groups['body']:
            ev=o.evaluated_get(deps);allcoords.extend(ev.matrix_world@v.co for v in ev.data.vertices)
        dz=-min(v.z for v in allcoords)
        if name=='leap':dz += [0,0,.08,.16,.20,.12,.06,0,0,0][i]
        cell=len(frames);offset=cam_right*(4.4*cell)+Vector((0,0,dz))
        for key,objects in groups.items():
            for obj in objects:
                ev=obj.evaluated_get(deps);mesh=bpy.data.meshes.new_from_object(ev,depsgraph=deps)
                mesh.transform(ev.matrix_world);new=bpy.data.objects.new(f'{key}_{name}_{i}_{obj.name}',mesh);scene.collection.objects.link(new);new.location=offset;snapshots[key].append(new)
        def projected(world):
            v=world_to_camera_view(scene,camera,world+Vector((0,0,dz)));return [round(v.x*96,3),round((1-v.y)*96,3)]
        record={}
        for label,bone in {'rightHand':'handslot.r','leftHand':'handslot.l','head':'head','chest':'chest','hip':'hips','frontFoot':'foot.r','backFoot':'foot.l'}.items():record[label]=projected(rig.matrix_world@rig.pose.bones[bone].head)
        slot=rig.matrix_world@rig.pose.bones['handslot.r'].matrix;record['weaponTip']=projected(slot@Vector((0,.97,0)));record['weaponGrip']=projected(slot@Vector((0,0,0)));record['rightHandBone']='handslot.r';record['rootY']=round(-dz*96/4.4,3)
        # Camera-space depth of the head bone (same metric as the Z pass): lets the 2D head sit behind a raised sword.
        record['headDepth']=round((rig.matrix_world@rig.pose.bones['head'].head-camera.location).dot(cam_forward),4)
        record['headVariant']='forward' if name in ['attack','slam','leap'] and i in [3,4,5,6] else 'back' if name in ['slam','leap'] and i in [1,2] else 'neutral'
        anchors[name].append(record);frames.append({'animation':name,'index':i,'cell':cell})
for objects in groups.values():
    for o in objects:o.hide_render=True
rig.hide_render=True
scene.render.resolution_x=96*len(frames);scene.render.resolution_y=96;camera.data.ortho_scale=4.4*len(frames);camera.location=camera.location+cam_right*(4.4*(len(frames)-1)/2)
# Depth pass written alongside color. Depth is encoded in fixed camera-space range.
scene.view_layers[0].use_pass_z=True
tree=bpy.data.node_groups.new('Sprite Color and Depth','CompositorNodeTree');scene.compositing_node_group=tree
layers=tree.nodes.new('CompositorNodeRLayers');output=tree.nodes.new('CompositorNodeOutputFile');depthitem=output.file_output_items.new('FLOAT','Depth');depthitem.override_node_format=True;depthitem.format.file_format='PNG';depthitem.format.color_mode='BW';depthitem.format.color_depth='16';depthitem.save_as_render=False
mapnode=tree.nodes.new('ShaderNodeMapRange');mapnode.inputs['From Min'].default_value=4;mapnode.inputs['From Max'].default_value=8;mapnode.inputs['To Min'].default_value=0;mapnode.inputs['To Max'].default_value=1;tree.links.new(layers.outputs['Depth'],mapnode.inputs[0]);tree.links.new(mapnode.outputs[0],output.inputs[0])
tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');composite=tree.nodes.new('NodeGroupOutput');tree.links.new(layers.outputs['Image'],composite.inputs[0])
start=time.time()
passes=list(snapshots)+['ref_cloth','ref_iron']
for key in passes:
    visible=[key] if not key.startswith('ref_') else ['body',*(['chest_tunic','legs_trousers','boots_boots','wrist_bracer','weapon_sword'] if key=='ref_cloth' else ['chest_plate','legs_leather','boots_greaves','wrist_cuff','weapon_sabre'])]
    for group,objects in snapshots.items():
        for o in objects:o.hide_render=group not in visible
    output.directory=str(RAW);output.file_name=f'{key}_depth_';scene.render.filepath=str(RAW/f'{key}.png');scene.frame_set(0)
    bpy.ops.render.render(write_still=True);print(f'RENDERED {key}',flush=True)
metadata={'frameWidth':96,'frameHeight':96,'footRow':63,'footOrigin':[48,64],'camera':{'orthoScalePerFrame':4.4,'side':'anatomical right (-X)','sameCameraEveryPass':True},'animations':animation,'frames':frames,'anchors':anchors,'groups':list(snapshots),'renderSeconds':time.time()-start,'blenderVersion':bpy.app.version_string,'depthRange':[4,8]}
(RAW/'render.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8');print('ATLAS RENDERS COMPLETE',flush=True)
