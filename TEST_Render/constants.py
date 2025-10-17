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

RR_node_name = 'Render Raw'
RR_node_group_name = 'Render Raw'


default_xforms = [
    # (color transform name, view transform name, description, item number)
    ('None', 'None', '', 0),
    ('AgX', 'AgX', '', 1),
    ('AgX Log', 'AgX Log', '', 2),
    ('False Color', 'False Color', '', 3),
    ('Filmic', 'Filmic', '', 4),
    ('Filmic Log', 'Filmic Log', '', 5),
    ('PBR Neutral', 'PBR Neutral', '', 6),
    ('Standard', 'Standard', '', 7),
]


supported_xforms = {
    # Most view transforms are called something different in the compositor vs. the color management panel.
    # Be sure to include both names in the list of what they could be called so that Render Raw can find it.
    'Standard': {'Names': ['sRGB']},
    'ACES': {'Names': ['ACES sRGB']},
    'ACES Gamut Comp': {'Names': ['ACES GamutComp', 'ACES LMT sRGB']},
    'ACES 1.3': {'Names': ['ACES 1.3 sRGB']},
    'ACES 1.3 - SDR': {'Names': []},
    'ACES 1.3 - HDR 1000 nits': {'Names': []},
    'ACES 1.3 - HDR 2000 nits': {'Names': []},
    'ACES 1.3 - HDR 4000 nits': {'Names': []},
    'ACES 2.0': {'Names': ['ACES 2.0 sRGB']},
    'ACES 2.0 - SDR': {'Names': []},
    'ACES 2.0 - HDR 500 nits': {'Names': []},
    'ACES 2.0 - HDR 1000 nits': {'Names': []},
    'ACES 2.0 - HDR 2000 nits': {'Names': []},
    'ACES 2.0 - HDR 4000 nits': {'Names': []},
    'AgX': {'Names': ['AgX', 'AgX Base sRGB']},
    'AgX - SDR': {'Names': []},
    'AgX - HDR 1000 nits': {'Names': []},
    'AgX Log': {'Names': []},
    'AgX Kraken': {'Names': ['AgX Base Kraken sRGB']},
    'AgX Kraken 800T': {'Names': ['AgX Base Kraken 800T sRGB']},
    'AgX NR2383': {'Names': ['AgX NR2383 sRGB']},
    'AgX Resolve': {'Names': ['AgX-Resolve Default', 'AgX Resolve Default sRGB']},
    'AgX Resolve Bombastic': {'Names': ['AgX-Resolve Bombastic', 'AgX Resolve Bombastic sRGB']},
    'ARRI ALF2': {'Names': ['ARRI ALF2 sRGB']},
    'ARRI K1S1': {'Names': ['ARRI K1S1 sRGB']},
    'ARRI Reveal': {'Names': ['ARRI Reveal sRGB']},
    'Blackmagic Extended Video': {'Names': ['Blackmagic Extended Video sRGB']},
    'Canon 201911': {'Names': ['Canon 201911 sRGB']},
    'Filmic': {'Names': ['Filmic sRGB']},
    'Filmic Log': {'Names': []},
    'JP2499': { 'Names': ['JP2499DRT', '2499DRT Base sRGB']},
    'JzDT': {'Names': ['JzDT sRGB']},
    'OpenDRT': {'Names': ['OpenDRT sRGB']},
    'PBR Neutral': {'Names': ['Khronos PBR Neutral', 'Khronos PBR Neutral sRGB', 'Khronos Neutral', 'Khronos Neutral sRGB']},
    'RED IPP2': {'Names': ['RED IPP2 sRGB']},
    'Sony S-Cinetone': {'Names': ['Sony S-Cinetone sRGB']},
    'TCAMv2': {'Names': ['TCAMv2 sRGB']},
    'Unreal Engine': {'Names': ['UnrealEngine', 'UnrealEngine Viewport sRGB']},
    'False Color': {'Names': []},
    'None': {'Names': ['Raw', 'Linear Rec.709', 'Linear', 'Non-Color']},
}


# Presets ARE stored on the Pre group, but not listed
# here so as not to be applied when applying a preset.
Pre_settings = [
    # Values
    'use_values',
    'exposure', 'gamma',
    'contrast', 'contrast_shadows', 'contrast_highlights',
    'pre_curves_factor', 'pre_curves_black', 'pre_curves_white', 'pre_curves_tone',
    # Colors
    'use_colors',
    'temperature', 'tint', 'white_balance_perceptual',
    'color_boost', 'color_boost_perceptual',
    'offset_color', 'power_color', 'slope_color', 'ops_factor',
    # Details
    'use_details',
    # Effects
    'use_effects',
    'glare', 'glare_threshold', 'glare_quality',
    'bloom', 'bloom_size', 'ghosting',
    'streaks', 'streak_length', 'streak_count', 'streak_angle',
    'halation', 'halation_size',
    # Alpha,
    'opacity'
]

Post_settings = [
    # Values
    'whites', 'highlights', 'shadows', 'blacks',
    'post_curves_factor', 'post_curves_black', 'post_curves_white', 'post_curves_tone',
    'fix_clipping',
    # Colors
    'saturation', 'saturation_perceptual', 'split_tone', 'density', 'density_depth',
    'preserve_hue', 'preserve_saturation', 'preserve_filmic', 'preserve_cutoff', 'preserve_spread',
    'hue_perceptual', 'hue_range', 'hue_smoothing',
    'hue_saturation_mask', 'hue_value_mask', 'hue_linear',
    'red_hue', 'red_saturation', 'red_value',
    'orange_hue', 'orange_saturation', 'orange_value',
    'yellow_hue', 'yellow_saturation', 'yellow_value',
    'green_hue', 'green_saturation', 'green_value',
    'teal_hue', 'teal_saturation', 'teal_value',
    'blue_hue', 'blue_saturation', 'blue_value',
    'pink_hue', 'pink_saturation', 'pink_value',
    'lift_color', 'gamma_color', 'gain_color', 'lgg_factor',
    'shadow_range', 'highlight_range', 'midtone_range',
    'shadow_factor', 'highlight_factor', 'midtone_factor',
    'highlight_color', 'midtone_color', 'shadow_color',
    'shadow_saturation', 'midtone_saturation', 'highlight_saturation',
    'shadow_saturation_range', 'midtone_saturation_range', 'highlight_saturation_range',
    'value_saturation_perceptual', 'dummy_blending', 'dummy_color',
    # Details
    'sharpness', 'sharpness_mask', 'texture', 'texture_color',
    'clarity', 'clarity_size',
    'negative_bleed', 'negative_bleed_size',
    # Effects
    'distortion', 'dispersion', 'horizontal_dispersion',
    'vignette_factor', 'vignette_feathering', 'vignette_linear_blend',
    'vignette_roundness', 'vignette_highlights',
    'vignette_scale_x', 'vignette_scale_y',
    'vignette_shift_x', 'vignette_shift_y', 'vignette_rotation',
    'grain', 'grain_method', 'grain_scale', 'grain_aspect',
    'grain_steps', 'grain_saturation', 'grain_is_animated',
    # Alpha
    'alpha_method', 'alpha_factor',
]

# These groups do not need to have a full copy made when creating a new layer
multiuser_subgroups = [
    # Values
    '.RR_contrast',
    # Colors
    '.RR_color_boost', '.RR_saturation', '.RR_hue_correct_pre', '.RR_color_density', 
    '.RR_split_tone', '.RR_preserve_color',
    # Effects 
    '.RR_sharpness','.RR_texture', '.RR_clarity',
    '.RR_lens_distortion', '.RR_vignette', '.RR_halation',
    '.RR_fast_grain_step', '.RR_grain_layer','.RR_displace_image',
    '.RR_alpha_fix', '.RR_fix_clipping',
    '.RR_clipping',
    # Utility
    '.RR_screeen_space_uvs', 
    '.RR_YUV_adjustments', '.RR_sRGB_to_LAB', '.RR_LAB_adjustments', '.RR_LAB_to_sRGB',
    '.RR_difference_mask', '.RR_mask_values', '.RR_adjust_mask', '.RR_mask_value', '.RR_flip_mask', 
    '.RR_mix_RGBA', '.RR_value_saturation', '.RR_value_screen'
]