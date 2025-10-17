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
from ..utilities.conversions import map_range, set_alpha
from ..utilities.settings import Settings
from ..utilities.layers import is_layer_used


def update_vignette(self, context, RR_group=None, layer_index=None):
    RR = Settings(context, RR_group, layer_index)
    PROPS = RR.props_post # Could be saved in pre or post now, but in post for reading older files

    NODE_PRE = RR.nodes_pre['Vignette']
    NODE_POST = RR.nodes_post['Vignette']

    if not RR.use_effects or PROPS.vignette_factor == 0 or not is_layer_used(RR):
        NODE_PRE.mute = True
        NODE_POST.mute = True
    else:
        NODE_PRE.mute = False
        NODE_POST.mute = PROPS.vignette_linear_blend == 1

    for V in [NODE_PRE, NODE_POST]:
            V.inputs['Highlights'].default_value = PROPS.vignette_highlights
            V.inputs['Feathering'].default_value = PROPS.vignette_feathering
            V.inputs['Roundness'].default_value = PROPS.vignette_roundness
            V.inputs['Color'].default_value = PROPS.vignette_color
            V.inputs['Scale X'].default_value = PROPS.vignette_scale_x
            V.inputs['Scale Y'].default_value = PROPS.vignette_scale_y
            V.inputs['Shift X'].default_value = PROPS.vignette_shift_x
            V.inputs['Shift Y'].default_value = PROPS.vignette_shift_y
            V.inputs['Rotation'].default_value = PROPS.vignette_rotation

    # All linear blending happens pre-transform, while the simple mix happens post-transform
    NODE_PRE.inputs['Factor'].default_value = PROPS.vignette_factor
    NODE_POST.inputs['Factor'].default_value = PROPS.vignette_factor * (1 - PROPS.vignette_linear_blend)


def update_bloom(self, context, RR_group=None, layer_index=None):
    RR = Settings(context, RR_group, layer_index)
    PROPS = RR.props_pre

    GLARE = RR.nodes_pre['Glare']
    GLARE.mute = False
    GLARE_NODES = GLARE.node_tree.nodes
    GLARE_LINKS = GLARE.node_tree.links
    GLARE_NODES['Add Bloom'].mute = PROPS.bloom * PROPS.glare == 0

    if bpy.app.version >= (4, 5, 0):
        GLARE.inputs['Threshold'].default_value = PROPS.glare_threshold
        GLARE.inputs['Saturation'].default_value = PROPS.bloom_saturation
        GLARE.inputs['Tint'].default_value = [PROPS.bloom_tint[0], PROPS.bloom_tint[1], PROPS.bloom_tint[2], 1]
        GLARE.inputs['Bloom Strength'].default_value = PROPS.bloom * PROPS.glare
        GLARE.inputs['Size'].default_value = PROPS.bloom_size_float

    elif bpy.app.version >= (4, 4, 0):
        # The whole glare node was overhauled
        BLOOM = GLARE_NODES['Bloom']
        GLARE_LINKS.new(BLOOM.outputs[1], GLARE_NODES['Bloom Result'].inputs[0])
        GLARE_NODES['Bloom Strength'].outputs[0].default_value = PROPS.bloom * PROPS.glare
        BLOOM.glare_type = 'BLOOM'
        BLOOM.inputs['Strength'].default_value = 1
        BLOOM.inputs['Threshold'].default_value = PROPS.glare_threshold
        BLOOM.inputs['Smoothness'].default_value = 1
        BLOOM.inputs['Saturation'].default_value = PROPS.bloom_saturation
        BLOOM.inputs['Tint'].default_value = set_alpha(PROPS.bloom_tint, 1)
        BLOOM.inputs['Size'].default_value = PROPS.bloom_size_float
        if PROPS.glare_quality == 5:
            BLOOM.quality = 'HIGH'
        elif PROPS.glare_quality == 4:
            BLOOM.quality = 'MEDIUM'
        elif PROPS.glare_quality == 3:
            BLOOM.quality = 'MEDIUM'
        elif PROPS.glare_quality == 2:
            BLOOM.quality = 'LOW'
        elif PROPS.glare_quality == 1:
            BLOOM.quality = 'LOW'

    elif bpy.app.version >= (4, 2, 0):
        # Bloom was implemented in the compositor's glare node
        BLOOM = GLARE_NODES['Bloom']
        GLARE_LINKS.new(BLOOM.outputs[0], GLARE_NODES['Bloom Result'].inputs[0])
        GLARE_NODES['Bloom Strength'].outputs[0].default_value = PROPS.bloom * PROPS.glare
        BLOOM.glare_type = 'BLOOM'
        BLOOM.threshold = PROPS.glare_threshold + 0.001
        BLOOM.size = PROPS.bloom_size
        if PROPS.glare_quality == 5:
            BLOOM.quality = 'HIGH'
        elif PROPS.glare_quality == 4:
            BLOOM.quality = 'MEDIUM'
        elif PROPS.glare_quality == 3:
            BLOOM.quality = 'MEDIUM'
        elif PROPS.glare_quality == 2:
            BLOOM.quality = 'LOW'
        elif PROPS.glare_quality == 1:
            BLOOM.quality = 'LOW'

    else:
        # Fakes bloom with multiple blur nodes before better bloom was implemented
        BLOOM = GLARE_NODES['Custom Bloom']
        BLOOM_NODES = BLOOM.node_tree.nodes
        GLARE_LINKS.new(BLOOM.outputs[1], GLARE_NODES['Bloom Result'].inputs[0])
        GLARE_NODES['Bloom Strength'].outputs[0].default_value = PROPS.bloom * PROPS.glare
        BLOOM.inputs['Threshold'].default_value = PROPS.glare_threshold + 0.001
        if PROPS.glare_quality == 5:
            BLOOM_NODES['Blur 1'].mute = False
            BLOOM_NODES['Blur 2'].mute = False
            BLOOM_NODES['Blur 3'].mute = False
            BLOOM_NODES['Blur 4'].mute = False
            BLOOM_NODES['Blur 5'].mute = False
        elif PROPS.glare_quality == 4:
            BLOOM_NODES['Blur 1'].mute = False
            BLOOM_NODES['Blur 2'].mute = False
            BLOOM_NODES['Blur 3'].mute = False
            BLOOM_NODES['Blur 4'].mute = False
            BLOOM_NODES['Blur 5'].mute = True
        elif PROPS.glare_quality == 3:
            BLOOM_NODES['Blur 1'].mute = True
            BLOOM_NODES['Blur 2'].mute = False
            BLOOM_NODES['Blur 3'].mute = False
            BLOOM_NODES['Blur 4'].mute = False
            BLOOM_NODES['Blur 5'].mute = True
        elif PROPS.glare_quality == 2:
            BLOOM_NODES['Blur 1'].mute = True
            BLOOM_NODES['Blur 2'].mute = True
            BLOOM_NODES['Blur 3'].mute = False
            BLOOM_NODES['Blur 4'].mute = False
            BLOOM_NODES['Blur 5'].mute = True
        elif PROPS.glare_quality == 1:
            BLOOM_NODES['Blur 1'].mute = True
            BLOOM_NODES['Blur 2'].mute = True
            BLOOM_NODES['Blur 3'].mute = True
            BLOOM_NODES['Blur 4'].mute = False
            BLOOM_NODES['Blur 5'].mute = True
        # BLOOM.inputs['Blend Highlights'].default_value = PROPS.bloom_blending


def update_streaks(self, context, RR_group=None, layer_index=None):
    # Only used pre Blender 4.5
    RR = Settings(context, RR_group, layer_index)
    PROPS = RR.props_pre
    GLARE = RR.nodes_pre['Glare']
    GLARE_NODES = GLARE.node_tree.nodes
    GLARE_LINKS = GLARE.node_tree.links
    GLARE_NODES['Add Streaks'].mute = PROPS.streaks * PROPS.glare == 0

    if bpy.app.version >= (4, 5, 0):
        GLARE.inputs['Threshold'].default_value = PROPS.glare_threshold
        GLARE.inputs['Streaks Strength'].default_value = PROPS.streaks * PROPS.glare
        GLARE.inputs['Length'].default_value = PROPS.streak_length
        GLARE.inputs['Count'].default_value = PROPS.streak_count
        GLARE.inputs['Angle'].default_value = PROPS.streak_angle

    elif bpy.app.version >= (4, 4, 0):
        # The whole glare node was overhauled
        GLARE_NODES['Streaks Strength'].outputs[0].default_value = PROPS.streaks * PROPS.glare
        STREAKS = GLARE_NODES['Streaks']
        GLARE_LINKS.new(STREAKS.outputs[1], GLARE_NODES['Streaks Result'].inputs[0])
        STREAKS.inputs['Strength'].default_value = 1
        STREAKS.inputs['Threshold'].default_value = PROPS.glare_threshold
        STREAKS.inputs['Streaks'].default_value = PROPS.streak_count
        STREAKS.inputs['Streaks Angle'].default_value = PROPS.streak_angle
        STREAKS.inputs['Fade'].default_value = map_range(PROPS.streak_length, 0, 1, 0.9, 1)

    else:
        GLARE_NODES['Streaks Strength'].outputs[0].default_value = PROPS.streaks * PROPS.glare
        STREAKS = GLARE_NODES['Streaks']
        STREAKS.threshold = PROPS.glare_threshold
        STREAKS.streaks = PROPS.streak_count
        STREAKS.angle_offset = PROPS.streak_angle
        STREAKS.fade = map_range(PROPS.streak_length, 0, 1, 0.9, 1)


def update_ghosting(self, context, RR_group=None, layer_index=None):
    RR = Settings(context, RR_group, layer_index)
    PROPS = RR.props_pre
    GLARE = RR.nodes_pre['Glare']
    GLARE_NODES = GLARE.node_tree.nodes
    GLARE_LINKS = GLARE.node_tree.links
    GLARE.node_tree.nodes['Add Ghosting'].mute = PROPS.ghosting * PROPS.glare == 0

    if bpy.app.version >= (4, 5, 0):
        GLARE.inputs['Threshold'].default_value = PROPS.glare_threshold
        GLARE.inputs['Ghosting Strength'].default_value = PROPS.ghosting * PROPS.glare

    elif bpy.app.version >= (4, 4, 0):
        # The whole glare node was overhauled
        GLARE_NODES['Ghosting Strength'].outputs[0].default_value = PROPS.ghosting / 4 * PROPS.glare
        GHOSTING = GLARE_NODES['Ghosting']
        GLARE_LINKS.new(GHOSTING.outputs[1], GLARE_NODES['Ghosting Result'].inputs[0])
        GHOSTING.inputs['Strength'].default_value = 1
        GHOSTING.inputs['Threshold'].default_value = PROPS.glare_threshold
        if PROPS.glare_quality == 5:
            GHOSTING.quality = 'HIGH'
        elif PROPS.glare_quality == 4:
            GHOSTING.quality = 'MEDIUM'
        elif PROPS.glare_quality == 3:
            GHOSTING.quality = 'MEDIUM'
        elif PROPS.glare_quality == 2:
            GHOSTING.quality = 'LOW'
        elif PROPS.glare_quality == 1:
            GHOSTING.quality = 'LOW'

    else:
        GLARE_NODES['Ghosting Strength'].outputs[0].default_value = PROPS.ghosting / 4 * PROPS.glare
        GHOSTING = GLARE_NODES['Ghosting']
        GHOSTING.threshold = PROPS.glare_threshold
        if PROPS.glare_quality == 5:
            GHOSTING.quality = 'HIGH'
        elif PROPS.glare_quality == 4:
            GHOSTING.quality = 'MEDIUM'
        elif PROPS.glare_quality == 3:
            GHOSTING.quality = 'MEDIUM'
        elif PROPS.glare_quality == 2:
            GHOSTING.quality = 'LOW'
        elif PROPS.glare_quality == 1:
            GHOSTING.quality = 'LOW'


def update_halation(self, context, RR_group=None, layer_index=None):
    RR = Settings(context, RR_group, layer_index)
    PROPS = RR.props_pre

    if bpy.app.version >= (4, 5, 0):
        GLARE = RR.nodes_pre['Glare']
        GLARE.mute = False
        GLARE.inputs['Threshold'].default_value = PROPS.glare_threshold
        GLARE.inputs['Halation Strength'].default_value = PROPS.halation * PROPS.glare
        GLARE.inputs['Halation Size'].default_value = PROPS.halation_size
        GLARE.node_tree.nodes['Add Halation'].mute = PROPS.halation * PROPS.glare == 0


def update_glare(self, context, RR_group=None, layer_index=None):
    RR = Settings(context, RR_group, layer_index)
    PROPS = RR.props_pre

    GLARE = RR.nodes_pre['Glare']
    GLARE.mute = False
    GLARE.node_tree.nodes['Add Glare'].mute = PROPS.glare == 0 or not PROPS.use_effects
    GLARE.node_tree.nodes['Glare Alpha'].mute = PROPS.glare == 0 or not PROPS.use_effects

    update_bloom(self, context, RR_group, layer_index)
    update_streaks(self, context, RR_group, layer_index)
    update_ghosting(self, context, RR_group, layer_index)
    update_halation(self, context, RR_group, layer_index)


def update_distortion(self, context, RR_group=None, layer_index=None):
    RR = Settings(context, RR_group, layer_index)
    PROPS = RR.props_post
    DISTORTION = RR.nodes_post['Lens Distortion']

    if not is_layer_used(RR) or not RR.use_effects or (PROPS.distortion == 0 and PROPS.dispersion == 0):
        DISTORTION.mute = True
    else:
        DISTORTION.mute = False
        DISTORTION.inputs['Distortion'].default_value = PROPS.distortion / 2
        DISTORTION.inputs['Dispersion'].default_value = PROPS.dispersion / 4
        if bpy.app.version >= (4, 5, 0):
            DISTORTION.inputs['Horizontal Dispersion'].default_value = PROPS.horizontal_dispersion


def update_grain(self, context, RR_group=None, layer_index=None):
    RR = Settings(context, RR_group, layer_index)
    PROPS = RR.props_post

    FAST = RR.nodes_post['Film Grain Fast']

    if not is_layer_used(RR) or not RR.use_effects or PROPS.grain == 0 or PROPS.grain_method == 'ACCURATE':
        FAST.mute = True
    else:
        FAST.mute = False

        if bpy.app.version >= (4, 5, 0):
            FAST.inputs['Strength'].default_value = PROPS.grain
            FAST.inputs['Scale'].default_value = PROPS.grain_scale
            FAST.inputs['Saturation'].default_value = PROPS.grain_saturation
            FAST.inputs['Detail'].default_value = PROPS.grain_steps
            FAST.inputs['Animate'].default_value = PROPS.grain_is_animated

        else:
            FAST.inputs['Strength'].default_value = PROPS.grain
            FAST.inputs['Scale'].default_value = PROPS.grain_scale
            FAST.inputs['Saturation'].default_value = PROPS.grain_saturation
            FAST.inputs['Aspect Correction'].default_value = PROPS.grain_aspect
            FAST.node_tree.nodes['Animate Offset'].mute = not PROPS.grain_is_animated
            FAST.node_tree.links.new(
                FAST.node_tree.nodes[f'Step {PROPS.grain_steps}'].outputs[0],
                FAST.node_tree.nodes['HSV'].inputs[0]
            )

    ACCURATE = RR.nodes_post['Film Grain Accurate']

    if not RR.use_effects or PROPS.grain == 0 or PROPS.grain_method == 'FAST':
        ACCURATE.mute = True
    else:
        ACCURATE.mute = False

        if bpy.app.version >= (4, 5, 0):
            ACCURATE.inputs['Strength'].default_value = PROPS.grain
            ACCURATE.inputs['Scale'].default_value = PROPS.grain_scale
            ACCURATE.inputs['Saturation'].default_value = PROPS.grain_saturation
            ACCURATE.inputs['Animate'].default_value = PROPS.grain_is_animated
            ACCURATE.node_tree.links.new(
                ACCURATE.node_tree.nodes[f'Step {PROPS.grain_steps}'].outputs[0],
                ACCURATE.node_tree.nodes['Layer Result'].inputs[0]
            )
        else:
            ACCURATE.inputs['Strength'].default_value = PROPS.grain
            ACCURATE.inputs['Scale'].default_value = PROPS.grain_scale
            ACCURATE.inputs['Saturation'].default_value = PROPS.grain_saturation
            ACCURATE.inputs['Aspect Correction'].default_value = PROPS.grain_aspect
            ACCURATE.node_tree.nodes['Step 1'].node_tree.nodes['Animate Offset'].mute = not PROPS.grain_is_animated
            ACCURATE.node_tree.links.new(
                ACCURATE.node_tree.nodes[f'Step {PROPS.grain_steps}'].outputs[0],
                ACCURATE.node_tree.nodes['Layer Result'].inputs[0]
            )


def update_effects_panel(self, context, RR_group=None, layer_index=None):
    update_vignette(self, context, RR_group, layer_index)
    update_distortion(self, context, RR_group, layer_index)
    update_glare(self, context, RR_group, layer_index)
    update_grain(self, context, RR_group, layer_index)