import bpy
from bpy.app.handlers import persistent
from ..utilities.view_transforms import set_available_color_xforms, set_available_view_xforms
from ..preferences import get_prefs

# This loads the view transforms when a new file is opened or when add-ons are reloaded
# https://blender.stackexchange.com/questions/321689/how-can-i-run-a-function-when-opening-blender-that-requires-context

@persistent
def on_file_load(*args, **kwargs):
    if not get_prefs(bpy.context).custom_transforms:
        return
    if on_file_load.is_register == True:
        return 
    on_file_load.is_register = True
    set_available_view_xforms(bpy.context)
    set_available_color_xforms()
on_file_load.is_register = False

def register():
    bpy.app.handlers.load_post.append(on_file_load)
    bpy.app.timers.register(on_file_load)

def unregister():
    on_file_load.is_register = False
    if on_file_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(on_file_load)
