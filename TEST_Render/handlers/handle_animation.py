import bpy
from bpy.app.handlers import persistent
from ..nodes.update_RR import update_all
from ..utilities.settings import Settings

@persistent
def RR_frame_change(scene):
    from ..preferences import get_prefs
    prefs = get_prefs(bpy.context)
    if not prefs.animated_values:
        return

    # print('Render Raw: Updating values on frame change')
    RR = Settings(bpy.context)
    groups = RR.groups
    for group in groups:
        for idx, layer in enumerate(RR.layers):
            update_all(None, bpy.context, group, idx)


handlers = [
     bpy.app.handlers.frame_change_post,
     bpy.app.handlers.render_pre
]

def register():
    from ..preferences import get_prefs
    prefs = get_prefs(bpy.context)
    if prefs.animated_values:
        for handler in handlers:
            handler.append(RR_frame_change)

def unregister():
    for handler in handlers:
        if RR_frame_change in handler:
            handler.remove(RR_frame_change)
