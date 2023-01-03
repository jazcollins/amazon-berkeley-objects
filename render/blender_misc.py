import sys
import os.path as osp
import requests

import bpy


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def initialize_blender_cuda():
    # FROM https://gist.github.com/S1U/13b8efe2c616a25d99de3d2ac4b34e86
    # Mark all scene devices as GPU for cycles
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'

    eprint("---------------   SCENE LIST   ---------------")
    for scene in bpy.data.scenes:
        eprint(scene.name)
        scene.cycles.device = 'GPU'

    # Enable CUDA
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'

    # Enable and list all devices, or optionally disable CPU
    eprint("----------------------------------------------")
    eprint(bpy.context.preferences.addons['cycles'].preferences.get_devices())
    eprint("----------------------------------------------")
    print("----------------------------------------------")
    for devices in bpy.context.preferences.addons['cycles'].preferences.get_devices():
        eprint(devices)
        for d in devices:
            d.use = True
            if d.type == 'CPU':
                d.use = False
            eprint("Device '{}' type {} : {}" . format(d.name, d.type, d.use))
            print("Device '{}' type {} : {}" . format(d.name, d.type, d.use))
    eprint("----------------------------------------------")
    print("----------------------------------------------")

def import_glb(glb_path) -> bpy.types.Object:
    """
        Import GLB at glb_path, return corresponding mesh object
        Assumes the scene is empty
    """
    status = bpy.ops.import_scene.gltf(filepath=glb_path)
    assert('FINISHED' in status)
    bpy.ops.object.select_all(action='SELECT')
    objects = bpy.context.selected_objects[:]
    obj = [o for o in objects if o.type=='MESH'][0]
    obj.rotation_euler = 0,0,0      # clear default rotation
    obj.location = 0,0,0            # clear default translation
    bpy.context.view_layer.update()
    return obj

def hdrihaven_fetch(hdri_name: str, res='4k', out_dir='hdris/'):
    # download hdri if it doesn't exist
    hdri_path = f'{out_dir}/{hdri_name}_{res}.hdr'
    if not osp.isfile(hdri_path):
        url  = f'https://hdrihaven.com/files/hdris/{hdri_name}_{res}.hdr'
        print(f'Downloading HDRI from {url}')
        r = requests.get(url)
        with open(hdri_path, 'wb') as f:
            f.write(r.content)
        # Retrieve HTTP meta-data
        print(r.status_code)
        print(r.headers['content-type'])
        print(r.encoding)
    return hdri_path
