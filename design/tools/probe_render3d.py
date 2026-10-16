import bpy,math
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(root/'design/3d/source/kaykit/Rogue.glb'))
rig=bpy.data.objects['Rig'];rig.animation_data.action=bpy.data.actions['Idle'];bpy.context.scene.frame_set(0)
for o in bpy.data.objects:
    if o.type=='MESH' and not o.name.startswith('Rogue_'):o.hide_render=True
    if o.name=='Rogue_Cape':o.hide_render=True
bpy.ops.object.camera_add(location=(-6,0,1.0));camera=bpy.context.object;camera.rotation_euler=(Vector((0,0,1.0))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=2.5
scene=bpy.context.scene;scene.camera=camera;scene.render.engine='BLENDER_EEVEE';scene.render.resolution_x=scene.render.resolution_y=96;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='Standard'
bpy.ops.object.light_add(type='AREA',location=(-3,-4,5));bpy.context.object.data.energy=400;bpy.context.object.data.size=5
scene.render.filepath=str(root/'design/3d/probe.png');bpy.ops.render.render(write_still=True)
print('Probe saved')
