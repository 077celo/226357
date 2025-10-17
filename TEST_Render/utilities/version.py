'''
Copyright (C) 2024 Orange Turbine
https://orangeturbine.com
orangeturbine@cgcookie.com

This file is part of the Render Raw add-on, created by Jonathan Lampel for Orange Turbine.

All code distributed with this add-on is open source as described below.

Render Raw is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses/>.
'''

import bpy, addon_utils
from ..constants import RR_node_group_name
from .append import append_group
from .nodes import get_RR_nodes, make_subs_single_user
from .cache import RR_cache, cacheless


minimum_version = '(1, 2, 19)'


def prettify_version(version):
    return version.replace('(', '').replace(')', '').replace(',', '.').replace(' ', '')


@RR_cache(0.1)
def get_addon_version(evaluate=False, pretty=False, use_cache=True):
    version = str(
        [
            addon.bl_info.get("version", (-1, -1, -1))
            for addon in addon_utils.modules()
            if addon.bl_info["name"] == 'Render Raw'
        ][0]
    )

    if evaluate:
        return eval(version)
    elif pretty:
        return prettify_version(version)
    else:
        return version


def set_RR_node_version(RR_group):
    try:
        RR_group.nodes['Version'].label = get_addon_version()
    except:
        print('Addon version could not be saved in the node tree')


@RR_cache(0.1)
def get_RR_node_version(RR_group, evaluate=False, pretty=False, use_cache=True):
    if 'Version' in [x.name for x in RR_group.nodes]:
        version = RR_group.nodes['Version'].label
    else:
        version = str((-1, -1, -1))

    if evaluate:
        return eval(version)
    elif pretty:
        if eval(version) > (0, 0, 0):
            return prettify_version(version)
        else: return ' Unknown'
    else: return version


def set_RR_blender_version(RR_group):
    RR_group.nodes['Blender Version'].label = str(bpy.app.version)


@RR_cache(0.1)
def get_RR_blender_version(RR_group, evaluate=False, pretty=False, use_cache=True):
    if 'Blender Version' in [x.name for x in RR_group.nodes]:
        version = RR_group.nodes['Blender Version'].label
    else:
        version = str((-1, -1, -1))

    if evaluate:
        return eval(version)
    elif pretty:
        if eval(version) > (0, 0, 0):
            return prettify_version(version)
        else: return ' Unknown'
    else: return version


@RR_cache(0.1)
def is_incompatible_group(RR_group, use_cache=True):
    RR_node_version = get_RR_node_version(RR_group, evaluate=True)
    RR_bl = get_RR_blender_version(RR_group, evaluate=True)
    if RR_node_version < eval(minimum_version):
        return True
    elif RR_bl:
        return (
            (bpy.app.version >= (4,5,0) and RR_bl < (4,5,0)) or
            (bpy.app.version < (4,5,0) and RR_bl >= (4,5,0))
        )
    else:
        return False


def upgrade_group_colorspace_nodes(RR_group):
    if bpy.app.version < (5, 0, 0) or get_RR_blender_version(RR_group, evaluate=True) >= (5, 0, 0):
        return 
    
    for node in [x for x in RR_group.nodes if x.bl_idname == 'CompositorNodeConvertColorSpace']:
        new_node = RR_group.nodes.new('CompositorNodeConvertToDisplay')

        RR_group.links.new(node.inputs[0].links[0].from_socket, new_node.inputs[0])
        RR_group.links.new(new_node.outputs[0], node.outputs[0].links[0].to_socket)

        new_node.hide = node.hide
        new_node.location = node.location_absolute
        new_node.use_custom_color = node.use_custom_color
        new_node.color = node.color
        new_node.label = node.label
        new_node.parent = node.parent

        name = node.name
        RR_group.nodes.remove(node)
        new_node.name = name

        if 'Convert Colorspace' in name:
            new_node.view_settings.view_transform = RR_group.render_raw.view_transform
        elif 'Inverse Transform' in name:
            new_node.inputs['Invert'].default_value = True
    


@cacheless
def upgrade_group(context, RR_group, default_RR=None, include_current=False):
    addon_version = get_addon_version(evaluate=True, use_cache=False)
    RR_node_version = get_RR_node_version(RR_group, evaluate=True, use_cache=False)

    if include_current or RR_node_version != 0 and is_incompatible_group(RR_group, use_cache=False):
        # No version indicates that the nodes are freshly imported and do not need upgrading
        print(f"Upgrading Render Raw nodes from version {RR_node_version} to {addon_version}")
        from .presets import get_group_preset, apply_group_preset

        GROUPS = bpy.data.node_groups
        GROUP_NAME = RR_group.name
        LAYER_IDX = RR_group.render_raw.active_layer_index
        preset = get_group_preset(context, RR_group)

        if default_RR:
            new_RR = default_RR.copy()
        else:
            new_RR = append_group(RR_node_group_name).copy()

        upgrade_group_colorspace_nodes(new_RR)
        set_RR_node_version(new_RR)
        set_RR_blender_version(new_RR)
        make_subs_single_user(new_RR.nodes)
        apply_group_preset(context, new_RR, preset)

        new_RR.render_raw.active_layer_index = LAYER_IDX

        GROUPS.remove(GROUPS[GROUP_NAME])
        new_RR.name = GROUP_NAME

        if default_RR == None:
            bpy.data.node_groups.remove(default_RR)

        return new_RR

    else:
        return RR_group
