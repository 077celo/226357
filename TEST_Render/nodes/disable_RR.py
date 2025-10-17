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
from ..preferences import get_prefs
from ..utilities.nodes import get_RR_nodes
from ..utilities.cache import cacheless
from ..utilities.view_transforms import disable_view_transform, set_available_view_xforms


@cacheless
def disable_RR(self, context):
    RR = Settings(context)
    VIEW = context.scene.view_settings

    set_available_view_xforms(context)
    disable_view_transform(context, RR.props_group)

    VIEW.exposure = RR.props_scene.exposure
    VIEW.gamma = 1 / RR.props_scene.gamma

    # Restore previous settings
    prev_look = RR.props_scene.prev_look
    view_transform = VIEW.view_transform
    if prev_look in ['None', '']:
        VIEW.look = 'None'
    elif view_transform == 'AgX':
        VIEW.look = f"{view_transform} - {prev_look}"
    else:
        VIEW.look = prev_look

    VIEW.use_curve_mapping = RR.props_scene.prev_use_curves

    if bpy.app.version >= (4, 3, 0):
        VIEW.use_white_balance = RR.props_scene.prev_use_white_balance
        VIEW.white_balance_temperature = RR.props_scene.prev_temperature
        VIEW.white_balance_tint = RR.props_scene.prev_tint

    for RR_node in get_RR_nodes(context):
        RR_node.mute = True
