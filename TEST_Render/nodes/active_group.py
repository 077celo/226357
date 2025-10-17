import bpy
from ..utilities.nodes import get_RR_nodes, is_RR_node, get_group_nodes_recursively, make_subs_single_user
from ..utilities.version import set_RR_node_version
from ..utilities.append import append_node
from ..utilities.cache import cacheless, RR_cache
from ..utilities.scene import is_use_nodes, scene_nodes
from ..constants import RR_node_group_name


@RR_cache(0.1)
def get_active_group(context):
    NAME = context.scene.render_raw_scene.active_RR_group_name
    NODES = scene_nodes(context)

    if (
        NODES and
        is_RR_node(NODES.active, include_legacy=True)
    ):
        return NODES.active.node_tree

    for group in bpy.data.node_groups:
        if group.name == NAME:
            return group

    scene_RR_nodes = get_RR_nodes(context)
    if scene_RR_nodes:
        return scene_RR_nodes[0].node_tree

    print('No active Render Raw group found')
    return None


@RR_cache(0.1)
def get_active_node(context):
    NODES = scene_nodes(context)

    if (
        NODES and
        is_RR_node(NODES.active)
    ):
        return NODES.active

    RR_GROUP = get_active_group(context)
    group_nodes = get_group_nodes_recursively(NODES)
    for node in group_nodes:
        if node.node_tree == RR_GROUP:
            return node

    return None


def get_active_group_settings(context):
    RR_GROUP  = get_active_group(context)
    if RR_GROUP:
        return RR_GROUP.render_raw
    # Fallback to scene values just so interface doesn't error out
    return context.scene.render_raw


@cacheless
def set_active_group(context, group=None):
    NODES = scene_nodes(context)
    RR_NODES = get_RR_nodes(context)
    RR_SCENE = context.scene.render_raw_scene

    if group != None:
        RR_SCENE.active_RR_group_name = group.name
        for node in RR_NODES:
            if node.node_tree == group:
                node.id_data.nodes.active = node
    elif is_RR_node(NODES.active):
        RR_SCENE.active_RR_group_name = NODES.active.node_tree.name
    elif RR_SCENE.active_RR_group_name in [node.node_tree.name for node in RR_NODES]:
        pass
    elif RR_NODES:
        RR_SCENE.active_RR_group_name = RR_NODES[0].node_tree.name

    return bpy.data.node_groups[RR_SCENE.active_RR_group_name]


def apply_active_group(self, context):
    RR_SCENE = context.scene.render_raw_scene
    set_active_group(
        context, 
        group=bpy.data.node_groups[RR_SCENE.active_group]
    )


@cacheless
def rename_active_group(context, name):
    RR_SCENE = context.scene.render_raw_scene
    RR_GROUP = get_active_group(context)
    RR_GROUP.name = name
    RR_SCENE.active_RR_group_name = name


def active_group_items(self, context):
    RR_nodes = get_RR_nodes(context)
    if RR_nodes:
        groups = set()
        for node in RR_nodes:
            groups.add((node.node_tree.name, node.node_tree.name, ''))
        return list(groups)
    else:
        return [('NONE', 'None', '')]


@cacheless
def duplicate_active_group(context):
    RR_GROUP = get_active_group(context)
    PREV_NODE = get_active_node(context)
    NODES = PREV_NODE.id_data.nodes

    if RR_node_group_name in [x.name for x in bpy.data.node_groups]:
        RR_node = NODES.new("CompositorNodeGroup")
        RR_node.node_tree = RR_GROUP.copy()
    else:
        RR_node = append_node(NODES, RR_node_group_name, copy=True)

    RR_node.location = [PREV_NODE.location[0], PREV_NODE.location[1] - 250]
    RR_node.width = 175

    make_subs_single_user(RR_node.node_tree.nodes)
    set_RR_node_version(RR_node.node_tree)

    return RR_node
