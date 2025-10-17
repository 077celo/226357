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


def is_use_nodes(context):
    if bpy.app.version >= (5, 0, 0):
        return context.scene.compositing_node_group != None
    else:
        return context.scene.use_nodes


def scene_nodes(context):
    if bpy.app.version >= (5, 0, 0):
        if context.scene.compositing_node_group:
            return context.scene.compositing_node_group.nodes
        else:
            return []
    else:
        if context.scene.use_nodes and context.scene.node_tree:
            return context.scene.node_tree.nodes
        else:
            return []


def scene_links(context):
    if bpy.app.version >= (5, 0, 0):
        if context.scene.compositing_node_group:
            return context.scene.compositing_node_group.links
        else:
            return []
    else:
        if context.scene.use_nodes and context.scene.node_tree:
            return context.scene.node_tree.links
        else:
            return []