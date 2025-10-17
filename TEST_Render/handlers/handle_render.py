import bpy
from bpy.app.handlers import persistent

from ..preferences import get_prefs
from ..utilities.view_transforms import disable_view_transform, set_raw
from ..utilities.viewport import enable_viewport_compositing, disable_viewport_compositing
from ..utilities.settings import Settings

realtime_engines = ['BLENDER_WORKBENCH', 'BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE']

@persistent
def RR_pre_render(scene):
    PREFS = get_prefs(bpy.context)

    if (
        scene.render_raw_scene.enable_RR and
        not scene.render.engine in realtime_engines and
        PREFS.transform_during_render
    ):
        # print('Render Raw: Updating view transform before render for a better render preview')
        RR = Settings(bpy.context)
        disable_view_transform(bpy.context, RR.props_group)
        disable_viewport_compositing(bpy.context, 'ALL')


@persistent
def RR_post_render(scene):
    PREFS = get_prefs(bpy.context)

    if (
        scene.render_raw_scene.enable_RR and
        not scene.render.engine in realtime_engines and
        PREFS.transform_during_render
    ):
        # print('Render Raw: Restoring view transform after render')
        RR = Settings(bpy.context)
        if RR.props_group.view_transform == 'False Color':
            scene.view_settings.view_transform = 'False Color'
        else:
            set_raw(bpy.context)
        enable_viewport_compositing(bpy.context, 'SAVED')


def register():
    from ..preferences import get_prefs
    prefs = get_prefs(bpy.context)
    if prefs.transform_during_render:
        bpy.app.handlers.render_pre.append(RR_pre_render)
        bpy.app.handlers.render_post.append(RR_post_render)

def unregister():
    if RR_pre_render in bpy.app.handlers.render_pre:
        bpy.app.handlers.render_pre.remove(RR_pre_render)
    if RR_post_render in bpy.app.handlers.render_post:
        bpy.app.handlers.render_post.remove(RR_post_render)
