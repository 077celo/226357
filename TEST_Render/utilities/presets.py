import bpy, os, json, shutil

from ..constants import Pre_settings, Post_settings
from ..preferences import get_prefs
from ..utilities.conversions import map_range
from ..utilities.version import get_addon_version, get_RR_node_version
from ..utilities.curves import RGB_curve_default, create_curve_preset, set_curve_node
from ..utilities.settings import is_default, Settings
from ..utilities.layers import get_layer_nodes, get_layer_node, reset_layer_settings, add_layer, remove_all_layers, refresh_layers
from ..nodes.update_values import update_group_exposure, update_group_gamma
from ..utilities.cache import cacheless

blank_preset = 'NONE'


preset_settings_to_skip = [
    'enable_RR', 'view_transform',
    'prev_look', 'prev_use_curves', 'prev_exposure',
    'preset', 'presets', 'preset_list', 'preset_name',
    'layer_name', 'layer_factor', 'use_layer', 'use_layer_mask', 'active_layer_index',
    'use_clipping', 'clipping_blacks', 'clipping_whites', 'clipping_saturation'
]


default_path = bpy.path.native_pathsep(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'assets', 'presets')
)


def get_path(context):
    prefs = get_prefs(context)
    prefs_path = prefs.preset_path
    if prefs_path and os.path.isdir(prefs_path):
        return prefs_path
    else:
        return default_path


def get_preset_files(context, path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def copy_default_presets(context):
    prefs = get_prefs(context)
    path = prefs.preset_path
    if os.path.isdir(path):
        for file in get_preset_files(context, default_path):
            shutil.copy2(os.path.join(default_path, file), path)


def get_preset_list(preset_files):
    preset_names = []
    for file in preset_files:
        if file.endswith('.rr'):
            preset_names.append(file.replace('.rr', ''))
    return [blank_preset] + sorted(preset_names)


def preset_items(self, context):
    if hasattr(context.scene, 'render_raw_presets'):
        presets = []
        for preset_name in context.scene.render_raw_presets.keys():
            if preset_name == blank_preset:
                presets.append((blank_preset, 'None', '', 0))
            else:
                presets.append((preset_name, preset_name, ''))
        return presets
    else:
        return [(blank_preset, 'None', '', 0)]


def refresh_presets(context):
    path = get_path(context)
    prev_preset = context.scene.render_raw.preset

    context.scene.render_raw_presets.clear()

    preset_list = get_preset_list(get_preset_files(context, path))

    #TODO: Clear out presets that have been deleted from the folder
    for preset in preset_list:
        if preset not in context.scene.render_raw_presets.keys():
            new_preset = context.scene.render_raw_presets.add()
            new_preset.name = preset

    if prev_preset and prev_preset not in preset_list:
        context.scene.render_raw.preset = blank_preset


def get_props_from_key(RR_group, layer_index, key):
    PRE = get_layer_node(RR_group, layer_index, 'Pre')
    POST = get_layer_node(RR_group, layer_index, 'Post')
    if key in Pre_settings:
        return PRE.node_tree.render_raw
    elif key in Post_settings:
        return POST.node_tree.render_raw
    else:
        return RR_group.render_raw


def get_active_props_from_key(RR, key):
    # Both the main group and the layers groups have the same property group which contains all settings
    # But the add-on only reads and writes to the node groups which are affected
    if key in Pre_settings:
        return RR.props_pre
    elif key in Post_settings:
        return RR.props_post
    else:
        return RR.props_group


def key_to_preset(key, preset, props):
    if key in preset_settings_to_skip or is_default(props, key):
        value = None
    else:
        rna = props.bl_rna.properties[key]
        if rna.subtype in ['COLOR', 'COLOR_GAMMA']:
            value = []
            for i in range(rna.array_length):
                value.append(props[key][i])
        else:
            value = props[key]

    return value


def get_layer_preset(node_pre, node_post):
    preset = {}
    preset['version'] = get_addon_version()

    if False: # logic for 4.5+
        pass
        # Get map of property to node path
        # Save node input value to preset

    # Older versions would also save group props in the preset while
    # newer versions have different presets for groups and layers
    props_pre = node_pre.node_tree.render_raw
    props_post = node_post.node_tree.render_raw

    for key in [x for x in props_pre.keys()]:
        value = key_to_preset(key, preset, props_pre)
        if value != None:
            preset[key] = value

    for key in [x for x in props_post.keys()]:
        value = key_to_preset(key, preset, props_post)
        if value != None:
            preset[key] = value

    if 'Color Blending' in [x.name for x in node_post.node_tree.nodes]:
        CB = node_post.node_tree.nodes['Color Blending'].node_tree.nodes
    else:
        CB = node_post.node_tree.nodes['Color Balance'].node_tree.nodes
    preset['highlight_blending'] = CB['Highlight Color'].blend_type
    preset['midtone_blending'] = CB['Midtone Color'].blend_type
    preset['shadow_blending'] = CB['Shadow Color'].blend_type

    preset['value_curves'] = create_curve_preset(node_post.node_tree.nodes['Curves'])
    if 'Curves' in [x.name for x in node_pre.node_tree.nodes]:
        preset['value_curves_linear'] = create_curve_preset(node_pre.node_tree.nodes['Curves'])
    if 'Log Curves' in [x.name for x in node_pre.node_tree.nodes]:
        preset['value_curves_log'] = create_curve_preset(node_pre.node_tree.nodes['Log Curves'])

    return preset


def write_preset(context, preset, preset_name):
    path = get_path(context)
    with open(
        os.path.join(path, f"{preset_name}.rr"), "w"
    ) as file:
        file.write(json.dumps(preset, indent=4))


@cacheless
def save_preset(self, context):
    RR = Settings(context)
    preset = get_layer_preset(RR.layer_pre, RR.layer_post)
    write_preset(context, preset, self.preset_name)
    refresh_presets(context)
    RR.props_pre.preset = self.preset_name


def load_preset(context, preset_name):
    try:
        path = get_path(context)
        with open(
            os.path.join(path, f"{preset_name}.rr"), "r"
        ) as file:
            return json.load(file)
    except:
        refresh_presets(context)
        print('ERROR: Render Raw preset not found. Refreshing list instead.')


def remove_preset(context):
    RR = Settings(context)
    path = get_path(context)
    os.remove(
        os.path.join(path, f"{RR.props_pre.preset}.rr")
    )
    RR.props_pre.preset = 'NONE'


def upgrade_layer_preset(preset, preset_keys):
    new_preset = preset

    if 'version' not in preset_keys:
        preset['version'] = '(1, 0, 0)'
        for key in preset_keys:
            if key == 'blacks':
                new_preset[key] = map_range(preset[key], 0, 1, 0.5, -0.5)
            if key == 'whites':
                new_preset[key] = map_range(preset[key], 0, 1, 0.5, -0.5)
            if key == 'highlights':
                new_preset[key] = map_range(preset[key], 0, 1, -0.5, 0.5)
            if key == 'shadows':
                new_preset[key] = map_range(preset[key], 0, 1, -0.5, 0.5)

    if eval(preset['version']) < (1, 2, 3):
        if 'curves_factor' in preset_keys:
            new_preset['post_curves_factor'] = preset['curves_factor']

    if eval(preset['version']) < (1, 2, 8):
        if 'vignette_value' in preset_keys:
            new_preset['vignette_factor'] = abs(preset['vignette_value'])
            tint = preset['vignette_value'] if 'vignette_tint' in preset_keys else [0,0,0,1]
            value = [0,0,0,1] if preset['vignette_value'] < 0 else [1,1,1,1]
            new_preset['vignette_color'] = [tint[0]*value[0], tint[1]*value[1], tint[2]*value[2], 1]
        if 'vignette_highlights' in preset_keys:
            new_preset['vignette_linear_blend'] = preset['vignette_highlights']

    if eval(preset['version']) < (1, 2, 10):
        per_hue = [
            'red_saturation', 'red_value', 'orange_saturation', 'orange_value',
            'yellow_saturation', 'yellow_value', 'green_saturation', 'green_value',
            'teal_saturation', 'teal_value', 'blue_saturation', 'blue_value',
            'pink_saturation', 'pink_value',
        ]
        for key in per_hue:
            if key in preset_keys:
                new_preset[key] = preset[key] * 2
        new_preset['hue_perceptual'] = 0
        new_preset['hue_saturation_mask'] = 1

    return new_preset


def apply_layer_preset(context, RR_group, layer_index, preset):
    from ..nodes.update_RR import update_all

    reset_layer_settings(context, RR_group, layer_index)

    try:
        preset_keys = preset.keys()
    except:
        refresh_presets(context)
        print('ERROR: Render Raw preset not found. Refreshing list instead.')
        return

    preset = upgrade_layer_preset(preset, preset_keys)

    PRE = get_layer_node(RR_group, layer_index, 'Pre')
    POST = get_layer_node(RR_group, layer_index, 'Post')
    PROPS_POST = POST.node_tree.render_raw
    CB_NODES = POST.node_tree.nodes['Color Blending'].node_tree.nodes

    for key in preset_keys:
        # If 4.5+, apply value directly to node

        PROPS = get_props_from_key(RR_group, layer_index, key)

        if key == 'value_curves':
            set_curve_node(POST.node_tree.nodes['Curves'], preset[key])
        elif key == 'value_curves_linear':
            set_curve_node(PRE.node_tree.nodes['Curves'], preset[key])
        elif key == 'value_curves_log':
            set_curve_node(PRE.node_tree.nodes['Log Curves'], preset[key])
        elif key == 'highlight_blending':
            CB_NODES['Highlight Color'].blend_type = preset[key]
        elif key == 'midtone_blending':
            CB_NODES['Midtone Color'].blend_type = preset[key]
        elif key == 'shadow_blending':
            CB_NODES['Shadow Color'].blend_type = preset[key]
        elif hasattr(PROPS, key):
            prop = PROPS.bl_rna.properties[key]
            if prop.type == 'ENUM':
                default = prop.default
                PROPS[key] = prop.enum_items.get(default).value
            else:
                PROPS[key] = preset[key]

    update_all(None, context, RR_group, layer_index)


@cacheless
def apply_active_layer_preset(self, context):
    from ..nodes.update_RR import update_all
    RR = Settings(context)

    if RR.props_pre.preset == blank_preset:
        reset_layer_settings(context, RR.group, RR.active_layer_index)
        update_all(self, context, RR.group, RR.active_layer_index)
        return

    preset = load_preset(context, RR.props_pre.preset)
    apply_layer_preset(context, RR.group, RR.active_layer_index, preset)


def get_legacy_preset(context, RR_group):
    # Before version 1.2, settings were saved in the scene
    #TODO: This is structured like a layer preset but needs to be a group preset
    preset = {}
    props =  context.scene.render_raw

    props.enable_RR = False # This needs to be off so the scene doesn't get flagged as legacy
    for key in props.keys():
        if (key not in preset_settings_to_skip):
            if (
                hasattr(props.bl_rna.properties, key) and
                props.bl_rna.properties[key].subtype == 'COLOR'
            ):
                preset[key] = [props[key][0], props[key][1], props[key][2]]
            else:
                preset[key] = props[key]

    # Some settings were referenced directly rather than saved through props
    nodes = RR_group.nodes
    try:
        preset['value_curves'] = create_curve_preset(nodes['Curves'])
    except:
        print('Value Curve preset could not be created while upgrading')
    try:
        COLOR_BALANCE = nodes['Color Balance'].node_tree.nodes
        preset['highlight_blending'] = COLOR_BALANCE['Highlight Color'].blend_type
        preset['midtone_blending'] = COLOR_BALANCE['Midtone Color'].blend_type
        preset['shadow_blending'] = COLOR_BALANCE['Shadow Color'].blend_type
    except:
        print('Color Balance preset could not be created while upgrading')

    group_preset = {
        'group': RR_group.render_raw,
        'layers': {
            'Layer 1': preset
        },
        'version': get_RR_node_version(RR_group, evaluate=True),
        'view_transform': props.view_transform,
        'alpha_method': '1',
        'alpha_factor': 0.5,
    }

    return group_preset


def get_group_preset(context, RR_group):
    preset_version = get_RR_node_version(RR_group, evaluate=True)

    if preset_version >= (1, 2, 0):
        preset = {
            'group': RR_group.render_raw,
            'layers': {},
            'version': preset_version,
            'view_transform': RR_group.render_raw.view_transform,
            'alpha_method': RR_group.render_raw.alpha_method,
            'alpha_factor': RR_group.render_raw.alpha_factor,
        }
        layer_nodes = get_layer_nodes(RR_group)
        for index, layer_pre in enumerate(layer_nodes['Pre']):
            layer_post = layer_nodes['Post'][index]
            layer_name = layer_pre.node_tree.render_raw.layer_name
            preset['layers'][layer_name] = get_layer_preset(layer_pre, layer_post)

    else:
        preset = get_legacy_preset(context, RR_group)

    return preset

@cacheless
def apply_group_preset(context, RR_group, preset):
    from ..nodes.update_RR import update_all
    prefs = get_prefs(context)

    update_group_exposure(context, RR_group)
    update_group_gamma(context, RR_group)
    RR_group.render_raw.alpha_method = preset['alpha_method']
    RR_group.render_raw.alpha_factor = preset['alpha_factor']
    if preset['view_transform']:
        RR_group.render_raw.view_transform = preset['view_transform']

    refresh_layers(RR_group)
    remove_all_layers(RR_group)

    for index, layer_name in enumerate(preset['layers'].keys()):
        new_layer = add_layer(context, RR_group, layer_name)
        apply_layer_preset(context, RR_group, index, preset['layers'][layer_name])
        RR_group.render_raw.active_layer_index = index
        update_all(None, context, RR_group, index)

    # If layer exposure and gamma controls are not visible, add to scene
    if not prefs.enable_layers and len(preset['layers'].keys()) == 1:
        scene = context.scene.render_raw_scene
        layer = get_layer_node(RR_group, 0, 'Pre').node_tree.render_raw
        scene.exposure += layer.exposure
        scene.gamma *= layer.gamma
