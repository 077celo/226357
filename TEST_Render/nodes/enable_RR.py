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

import bpy
from ..utilities.settings import Settings
from ..utilities.append import append_node
from ..utilities.version import set_RR_node_version, set_RR_blender_version, upgrade_group_colorspace_nodes
from ..utilities.nodes import get_RR_nodes, get_nodes_by_id
from ..utilities.viewport import setup_viewport_compositing
from ..utilities.view_transforms import set_available_view_xforms, set_available_color_xforms, enable_view_transform, reset_display
from ..utilities.layers import refresh_layers
from ..utilities.cache import cacheless
from ..nodes.update_RR import refresh_RR_nodes
from ..preferences import get_prefs
from ..constants import RR_node_name, RR_node_group_name


def create_RR_node(nodes):
    if RR_node_group_name in [x.name for x in bpy.data.node_groups]:
        RR_node = nodes.new("CompositorNodeGroup")
        RR_node.node_tree = bpy.data.node_groups[RR_node_group_name].copy()
    else:
        RR_node = append_node(nodes, RR_node_group_name, copy=False)

    upgrade_group_colorspace_nodes(RR_node.node_tree)
    set_RR_node_version(RR_node.node_tree)
    set_RR_blender_version(RR_node.node_tree)
    RR_node.name = RR_node_name
    RR_node.label = RR_node_name
    RR_node.width = 175
    return RR_node


def link_RR_node(context, nodes, links, RR_node):
    if bpy.app.version >= (5, 0, 0):
        composite_nodes = get_nodes_by_id(nodes, 'NodeGroupOutput')
    else:
        composite_nodes = get_nodes_by_id(nodes, 'CompositorNodeComposite')

    if composite_nodes:
        composite = composite_nodes[0]
        created_composite = False
    else:
        if bpy.app.version >= (5, 0, 0):
            composite = nodes.new('NodeGroupOutput')
            scene_group = context.scene.compositing_node_group
            scene_group.interface.items_tree.data.new_socket(
                name='Image',
                in_out='OUTPUT',
                socket_type='NodeSocketColor'
            )
            scene_group.interface.items_tree.data.new_socket(
                name='Image',
                in_out='INPUT',
                socket_type='NodeSocketColor'
            )
        else:
            composite = nodes.new('CompositorNodeComposite')
        created_composite = True
    RR_node.location = composite.location

    if not created_composite and composite.inputs[0].links:
        from_socket = composite.inputs[0].links[0].from_socket
        for link in from_socket.links:
            links.new(RR_node.outputs[0], link.to_socket)
        links.new(from_socket, RR_node.inputs[0])
    else:
        render_layers_nodes = get_nodes_by_id(nodes, 'CompositorNodeRLayers')
        if render_layers_nodes:
            render_layers = render_layers_nodes[0]
        else:
            render_layers = nodes.new('CompositorNodeRLayers')
            render_layers.location[0] = -300
        links.new(render_layers.outputs[0], RR_node.inputs[0])
        links.new(RR_node.outputs[0], composite.inputs[0])

    for link in RR_node.outputs[0].links:
        link.to_socket.node.location[0] += 300

    viewer_nodes = get_nodes_by_id(nodes, 'CompositorNodeViewer')
    if viewer_nodes:
        viewer = viewer_nodes[0]
        links.new(RR_node.outputs[0], viewer.inputs[0])


def store_scene_settings(context):
    RR_SCENE = context.scene.render_raw_scene
    VIEW = context.scene.view_settings

    RR_SCENE.prev_transform = VIEW.view_transform
    RR_SCENE.prev_look = VIEW.look
    RR_SCENE.prev_use_curves = VIEW.use_curve_mapping
    RR_SCENE.prev_exposure = VIEW.exposure
    if bpy.app.version >= (4, 3, 0):
        RR_SCENE.prev_use_white_balance = VIEW.use_white_balance
        RR_SCENE.prev_temperature = VIEW.white_balance_temperature
        RR_SCENE.prev_tint = VIEW.white_balance_tint


def scene_settings_to_nodes(context):
    VIEW = context.scene.view_settings
    RR = Settings(context)

    # Convert scene settings to RR node settings
    RR.props_scene.exposure = VIEW.exposure
    RR.props_scene.gamma = 1 / VIEW.gamma

    # This only affects the active group
    # TODO: allow this to affect all groups in the scene
    enable_view_transform(context, RR.props_group)

    # Clear view settings
    VIEW.exposure = 0
    VIEW.gamma = 1
    VIEW.look = 'None'
    if bpy.app.version >= (4, 3, 0):
        VIEW.use_curve_mapping = False
        VIEW.use_white_balance = False


@cacheless
def enable_RR(context):
    prev_mode = context.mode
    if prev_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    RR_SCENE = context.scene.render_raw_scene

    if bpy.app.version >= (5, 0, 0):
        if not context.scene.compositing_node_group:
            context.scene.compositing_node_group = bpy.data.node_groups.new('Compositing Nodes', 'CompositorNodeTree')
        NODES = context.scene.compositing_node_group.nodes
        LINKS = context.scene.compositing_node_group.links
    else:
        context.scene.use_nodes = True
        NODES = context.scene.node_tree.nodes
        LINKS = context.scene.node_tree.links

    RR_nodes = get_RR_nodes(context)

    if RR_nodes:
        refresh_RR_nodes(context, include_current=False)
        for RR_node in RR_nodes:
            RR_node.mute = False
            refresh_layers(RR_node.node_tree)
    else:
        new_RR = create_RR_node(NODES)
        link_RR_node(context, NODES, LINKS, new_RR)
        RR_SCENE.active_RR_group_name = new_RR.node_tree.name
        refresh_layers(new_RR.node_tree)

    set_available_view_xforms(context)
    set_available_color_xforms()

    if not RR_SCENE.is_upgrading:
        store_scene_settings(context)
        scene_settings_to_nodes(context)

    from ..operators.op_presets import refresh_presets
    refresh_presets(context)

    setup_viewport_compositing(context)

    if prev_mode == 'OBJECT':
        pass
    elif 'EDIT' in prev_mode:
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    elif prev_mode == 'PAINT_TEXTURE':
        bpy.ops.object.mode_set(mode='TEXTURE_PAINT', toggle=False)
    elif prev_mode == 'PAINT_VERTEX':
        bpy.ops.object.mode_set(mode='VERTEX_PAINT', toggle=False)
    elif prev_mode == 'PAINT_WEIGHT':
        bpy.ops.object.mode_set(mode='WEIGHT_PAINT', toggle=False)
    else:
        bpy.ops.object.mode_set(mode=prev_mode, toggle=False)
