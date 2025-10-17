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
from ..constants import RR_node_name, multiuser_subgroups
from ..utilities.scene import scene_nodes, scene_links
from .cache import RR_cache

""" Generic Node Operations """

def mix_all_outputs(outputs, name, blend_mode, location=[0,0]):
    """
    takes: array of node outputs
    returns: None or single output that is the result of the add
    """
    if not outputs:
        return
    nodes = outputs[0].id_data.nodes
    links = outputs[0].id_data.links
    prev_node = None
    for i in range(len(outputs) - 1):
        add = nodes.new('CompositorNodeMixRGB')
        add.blend_type = blend_mode
        add.location = location
        add.name = name
        add.hide = True
        if i == 0:
            links.new(outputs[0], add.inputs[1])
            links.new(outputs[1], add.inputs[2])
        else:
            links.new(prev_node.outputs[0], add.inputs[1])
            links.new(outputs[i + 1], add.inputs[2])
        prev_node = add
    if prev_node:
        return prev_node.outputs[0]


def get_nodes_by_id(nodes, bl_idname):
    matching_nodes = []
    for node in nodes:
        if node.bl_idname == bl_idname:
            matching_nodes.append(node)
    return matching_nodes


def get_groups_recursively(nodes, groups=None):
    if groups == None: groups = [] # In Python, defaults are an obj that persist through multiple fn calls. This forces a refresh
    sub_groups = set([x.node_tree for x in nodes if x.bl_idname == 'CompositorNodeGroup'])
    for g in sub_groups:
        if g and g not in groups:
            groups.append(g)
            get_groups_recursively(g.nodes, groups)
    return groups


def get_group_nodes_recursively(nodes, group_nodes=None):
    if group_nodes == None: group_nodes = [] # In Python, defaults are an obj that persist through multiple fn calls. This forces a refresh
    sub_groups = set([x for x in nodes if x.bl_idname == 'CompositorNodeGroup'])
    for g in sub_groups:
        if g and g not in group_nodes and g.node_tree:
            group_nodes.append(g)
            get_group_nodes_recursively(g.node_tree.nodes, group_nodes)
    return group_nodes


def make_subs_single_user(nodes):
    sub_groups = get_group_nodes_recursively(nodes)
    for node in sub_groups:
        group = node.node_tree
        is_multiuser = any(x in group.name for x in multiuser_subgroups)
        if group.users > 1 and not is_multiuser:
            node.node_tree = group.copy()


""" RR Node Operations """

@RR_cache(0.1)
def is_RR_node(node, include_legacy=False):
    if (
        node and
        node.bl_idname == 'CompositorNodeGroup' and
        node.node_tree
    ):
        node_names = [x.name for x in node.node_tree.nodes]
        if include_legacy:
            return (
                'Render Raw Input' in node_names or
                ('ACES Gamma' in node_names and 'Exposure' in node_names)
            )
        else:
            return ('Render Raw Input' in node_names)
    else:
        return False


def is_RR_group(group):
    return 'Render Raw Input' in [x.name for x in group.nodes]


@RR_cache(0.1)
def get_RR_groups(context, scene=True, use_cache=True):
    RR_groups = []

    if scene:
        nodes = scene_nodes(context)
        groups = get_groups_recursively(nodes)
        for group in groups:
            if is_RR_group(group): RR_groups.append(group)
    else:
        for group in bpy.data.node_groups:
            if is_RR_group(group): RR_groups.append(group)

    return RR_groups


@RR_cache(0.1)
def get_RR_nodes(context, use_cache=True):
    SCENE_NODES = scene_nodes(context)
    RR_nodes = []
    if not SCENE_NODES:
        return None
    group_nodes = get_group_nodes_recursively(SCENE_NODES)
    for node in group_nodes:
        if is_RR_node(node, include_legacy=True):
            RR_nodes.append(node)
    return RR_nodes


def remove_RR_nodes(context):
    nodes = scene_nodes(context)
    if nodes and RR_node_name in [x.name for x in nodes]:
        links = scene_links(context)

        if nodes[RR_node_name].inputs[0].links:
            from_socket = nodes[RR_node_name].inputs[0].links[0].from_socket
            for link in nodes[RR_node_name].outputs[0].links:
                to_socket = link.to_socket
                to_node = nodes[RR_node_name].outputs[0].links[0].to_node
                if to_node.bl_idname == 'CompositorNodeComposite':
                    to_node.location[0] -= 200
                links.new(from_socket, to_socket)

        nodes.remove(nodes[RR_node_name])


def remove_unused_groups():
    GROUPS = bpy.data.node_groups
    group_name_list = ['.RR_', '.LAB_', '.sRGB_to_LAB', '.YUV_', 'Render Raw']
    # The deepest node groups are currently 3 levels deep. 5 is for future proof
    for i in range(5):
        for group_name in [x.name for x in GROUPS]:
            if GROUPS[group_name].users == 0 and any(x in group_name for x in group_name_list):
                GROUPS.remove(GROUPS[group_name])


def clean_group_names():
    # Re-applies the .001, .002, etc.
    GROUPS = bpy.data.node_groups
    for group in GROUPS:
        for group_name in multiuser_subgroups:
            if group_name in group.name:
                group.name = group_name

