import bpy
from ..utilities.settings import Settings
from ..preferences import get_prefs
from ..nodes.update_colors import update_preserve_color
from ..constants import supported_xforms, default_xforms
from ..utilities.cache import RR_cache, cacheless


# These get populated by the set functions below when RR is enabled
available_view_xforms = []
available_color_xforms = []
xform_message = 'LOL why is this the only way to get a list of available color transforms'


def parse_xform_error(e):
    error_msg = f'bpy_struct: item.attr = val: enum "{xform_message}" not found in ('
    xforms_str = str(e).replace('TypeError: ', "").replace(error_msg,"").replace("'", "").replace(", ", ",")[:-1]
    xforms_list = xforms_str.split(",")
    return xforms_list


def set_available_view_xforms(context):
    try:
        context.scene.view_settings.view_transform = xform_message
    except Exception as e:
        global available_view_xforms
        available_view_xforms = parse_xform_error(e)
        # print('Render Raw: Fetched available view transforms')
        # print(available_view_xforms)


def set_available_color_xforms():
    images = [x for x in bpy.data.images]
    new_img = None
    if not images:
        new_img = bpy.data.images.new("RR Test Image", 16, 16)
    i = bpy.data.images[0]
    try:
        i.colorspace_settings.name = xform_message
    except Exception as e:
        global available_color_xforms
        available_color_xforms = parse_xform_error(e)
        # print('Render Raw: Fetched available color transforms')
        # print(available_color_xforms)
    if new_img != None:
        bpy.data.images.remove(new_img)


@RR_cache(0.1)
def get_view_transforms(context):
    # Updates the UI on mouse move, so no setting properties can be done here

    if not get_prefs(context).custom_transforms:
        return default_xforms

    xforms = []

    available_xforms = available_view_xforms if bpy.app.version >= (5, 0, 0) else available_color_xforms

    for idx, xform in enumerate(supported_xforms):
        color_xform = ''
        for possible_name in [xform] + supported_xforms[xform]['Names']:
            if possible_name in available_xforms:
                color_xform = possible_name
            if color_xform:
                break
        if color_xform:
            entry = (xform, xform, '', idx)
            xforms.append(entry)

    if bpy.app.version < (5, 0, 0) and 'False Color' in available_view_xforms:
        xforms.append(
            ('False Color', 'False Color', '')
        )

    return xforms if xforms else default_xforms


def set_raw(context):
    set_as_raw = False
    for x in ['Standard'] + supported_xforms['Standard']['Names']:
        if set_as_raw == False:
            try:
                context.scene.view_settings.view_transform = x
                set_as_raw = True
            except:
                set_as_raw = False
        else:
            break


def update_view_transform(context, RR_group=None):
    RR = Settings(context, RR_group)

    transform = RR.props_group.view_transform
    display = context.scene.display_settings.display_device

    if transform == 'False Color':
        context.scene.view_settings.view_transform = 'False Color'
        for node in RR.nodes_with_group:
            node.mute = True
        return
    else:
        for node in RR.nodes_with_group:
            node.mute = False

    set_available_color_xforms()
    set_available_view_xforms(context)
    set_raw(context)
    RR.props_group.display = display

    for node in [x for x in RR.nodes_group if 'Convert Colorspace' in x.name]:
        for x in [transform] + supported_xforms[transform]['Names']:
            if bpy.app.version >= (5, 0, 0) and x in available_view_xforms:
                node.display_settings.display_device = display
                node.view_settings.view_transform = x
                break
            elif bpy.app.version < (5, 0, 0) and x in available_color_xforms:
                node.to_color_space = x
                break


def enable_view_transform(context, RR_group_settings):
    active_xform = context.scene.view_settings.view_transform

    xform_name = ''

    for xform in supported_xforms:
        for possible_name in [xform] + supported_xforms[xform]['Names']:
            if possible_name == active_xform:
                xform_name = xform
                break
        if xform_name:
            RR_group_settings.view_transform = xform_name
            break

    if not xform_name:
        print(f'Render Raw: No matching transform was found for {active_xform}')

    set_raw(context)


def disable_view_transform(context, RR_group_settings):
    xform_name = ''
    RR_xform = RR_group_settings.view_transform
    for possible_name in [RR_xform] + supported_xforms[RR_xform]['Names']:
        if possible_name in available_view_xforms:
            xform_name = possible_name
            break
    if xform_name:
        context.scene.view_settings.view_transform = xform_name
    elif hasattr(context.scene.render_raw_scene, 'prev_transform'):
        context.scene.view_settings.view_transform = context.scene.render_raw_scene.prev_transform


@cacheless
def update_display(context, RR_group=None):
    RR = Settings(context, RR_group)
    prev_transform = RR.props_group.view_transform

    context.scene.display_settings.display_device = RR.props_group.display

    if bpy.app.version < (5, 0, 0):
        return 

    set_available_color_xforms()
    set_available_view_xforms(context)
    available_xforms = [x[0] for x in get_view_transforms(context)]

    if prev_transform in available_xforms:
        # update_view_transform(context, RR_group)
        pass
    # From SDR to HDR
    elif prev_transform == 'AgX' and 'AgX - SDR' in available_xforms:
        RR.props_group.view_transform = 'AgX - SDR'
    elif prev_transform == 'ACES 2.0' and 'ACES 2.0 - SDR' in available_xforms:
        RR.props_group.view_transform = 'ACES 2.0 - SDR'
    elif prev_transform == 'ACES 1.3' and 'ACES 1.3 - SDR' in available_xforms:
        RR.props_group.view_transform = 'ACES 1.3 - SDR'
    # From HDR to SDR
    elif 'AgX' in prev_transform and 'AgX' in available_xforms:
        RR.props_group.view_transform = 'AgX'
    elif 'ACES 2.0' in prev_transform and 'ACES 2.0' in available_xforms:
        RR.props_group.view_transform = 'ACES 2.0'
    elif 'ACES 1.3' in prev_transform and 'ACES 1.3' in available_xforms:
        RR.props_group.view_transform = 'ACES 1.3'
    # Misc.
    elif 'AgX' in available_xforms:
        RR.props_group.view_transform = 'AgX'
    elif 'AgX - SDR' in available_xforms:
        RR.props_group.view_transform = 'AgX - SDR'
    else:
        RR.props_group.view_transform = 'Standard'

    for node in [x for x in RR.nodes_group if x.bl_idname == 'CompositorNodeConvertToDisplay']:
        node.display_settings.display_device = RR.props_group.display


def reset_display(context, RR_group):
    RR_group.render_raw.display = context.scene.display_settings.display_device