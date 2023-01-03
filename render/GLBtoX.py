""" Run as blender -b -P GLBtoX.py -- regexp
    Converts all glb files with names matching regexp in `SOURCE_DIR` to OBJ files with the same name in `TARGET_DIR`
"""
import os
import os.path as osp
import re
import sys
import traceback

import bpy

sys.path.append(os.path.dirname(__file__))
from blender_misc import eprint, initialize_blender_cuda, import_glb,

# basedir = 'C:\\Users\\Achleshwar\\Desktop\\UCB\\3d_sample_data\\3d_sample_data\\'
SOURCE_DIR = '/home/jazzie/AMAZON3D146K/3dmodels/'
TARGET_DIR = '/home/jazzie/AMAZON3D146K/3dmodels_obj/'

def glb_to_X(glb_path: str, target_dir: str, out_format: str = 'obj') -> None:
    # Delete all objects in scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import glb
    object = import_glb(glb_path)

    # Select only the mesh object
    bpy.ops.object.select_all(action='DESELECT')
    object.select_set(True)

    # Target filepath
    portion = osp.splitext(osp.basename(glb_path))
    out_file = portion[0]+ "." + out_format
    out_path = osp.join(target_dir, out_file)

    # Export
    if out_format == 'obj':
        bpy.ops.export_scene.obj(filepath = out_path)
    elif out_format == 'ply':
        bpy.ops.export_mesh.ply(filepath = out_path)
    else:
        raise ValueError

if __name__ == "__main__":

    # Initizlize blender
    initialize_blender_cuda()

    # Check if only part of data has to be rerun
    try:
        regexp = str(sys.argv[sys.argv.index('--') + 1])
    except (IndexError, ValueError):
        regexp = ".*"
    pattern = re.compile(regexp)

    for _mi, model_name in enumerate(os.listdir(SOURCE_DIR)):
        if not pattern.match(model_name):
            print(f'Skipping1 {_mi:04d}: {model_name}')
            continue
        if not osp.splitext(model_name)[1]=='.glb':
            print(f'Skipping2 {_mi:04d}: {model_name}')
            continue
        print(f'{_mi:04d}: {model_name}')
        eprint(f'{_mi:04d}: {model_name}')
        glb_path = f'{SOURCE_DIR}/{model_name}'

        try:
            glb_to_X(glb_path, TARGET_DIR, out_format='obj')
        except:
            eprint("*** failed", model_name)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            eprint("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stderr)
            eprint("*** print_exception:")
            # exc_type below is ignored on 3.5 and later
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                    limit=2, file=sys.stderr)
    print('Done')
    eprint('Done')
