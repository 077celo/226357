---
excerpt: Documentation for the Render Raw add-on for Blender
nav_order: 9
nav_exclude: false
search_exclude: false
---

# Changelog

## 1.2.19
- Added full HDR support for Blender 5.0 alpha
- Added full ACES 1.3 and 2.0 support for Blender 5.0 alpha
    - This includes wide gamut working spaces
- Added log space curves
- Fixed issue with resetting scene values
- Fixed linear curves not being saved in presets
- Fixed color temperature controls breaking in Blender 5.0 alpha

## 1.2.18
- Render and material previews without compositing are now shown as Standard instead of Raw
    - There will still be clipping, but it is at least a closer preview than before
- The above change also makes it so that EXRs are now exported with linear values
    - This better matches the default Blender behavior
    - The view transform is still baked in, but converted to linear space
- Changing the Allow Animated Values and Allow Transform During Render now requires restart
    - This makes rendering without those (non-default and potentially unstable) options more stable
- Improved quality when adjusting black and white levels in Blender 4.5+
- Fixed per-layer exposure not updating properly
- Fixed upgrading when View Transform is not specified
- Code cleanup

## 1.2.17
- Added option to make per-hue adjustments in pre-transform linear space
- Fixed issue with custom view transforms not appearing in menu
- Fixed glare not updating when disabling effects

## 1.2.16
- Added Halation effect to Glare panel in Blender 4.5+
- Improved glare parameter mixing
- Fixed glare pass output when glare is not used
- Fixed Fast film grain Animate option being inverted

## 1.2.15
New features:
- Added new control, Shadow Bleed, in Blender 4.5+
    - This simulates the film effect of softer edges around shadows
- Added new control, Split Tone, for warming highlights while cooling shadows and vice versa
- Added new controls for refining contrast in the shadows and highlights
- Added transparent film to the Alpha Utilities panel
- Added basic support for Blender 5.0 alpha

Changes:
- Improved film grain pattern and performance in Blender 4.5+
- Fix Clipping is now called Highlight Rolloff
- Adjusting the contrast no longer affects the amount of glare
- Improved presets for High Key Photo, Low Key Photo, and Polaroid
- Improved Filmic mix in Colors Tone Mapping to not affect values
- Fixed seemingly random crashes in Blender 4.5
- Fixed upgrading nodes leaving behind many unused node groups
- Fixed appending a new node when enabling Render Raw even when not necessary
- Fixed issue with toggling Render Raw after upgrading older files
- Fixed issue when upgrading from versions before 1.2
- Fixed Render Raw appending extra viewer node
- Fixed density affecting fully black areas
- Fixed density not getting saved in presets
- Fixed layer factor being applied twice to some effects
- Fixed post-curves tone control not updating correctly

## 1.2.14
- Improved muting of unused nodes in Blender 4.5

## 1.2.13
- Fixed upgrading from some previous add-on versions
- Fixed vignette showing hard edges at half opacity in Blender 4.5

## 1.2.12
- Improved performance of Vignette
- Improved layout of new Render Raw nodes in Blender 4.5
- Improved adjusting layer factors in Blender 4.5
- Fixed older per hue presets not applying correctly

## 1.2.11
- Added support for all Pixel Manager view transforms
- Added new control for color density
- Added horizontal lens distortion for Blender 4.5
- Backported Per Hue masks for saturation and value for Blender 4.2 - 4.4
- Improved switching between incompatible Blender versions
- Improved preserving exposure and gamma when enabling and disabling Render Raw
- Improved saturation so that the default of 0.5 Perceptual is smart and won't cause clipping
- Removed option for improperly used ACES format

## 1.2.10
- Added new value control to smoothly dampen clipped values
- Fixed issue with color per value not affecting result
- Fixed saving presets that include values of 0
- Fixed applying presets with legacy vignette properties
- Fixed Clarity and Texture to avoid clipping
- Fixed refreshing nodes in Blender 4.5
- Improved glare for Blender 4.5
- Improved value levels for Blender 4.5
    - Fixed hue skewing when adjusting Shadows and Highlights
    - Adjusting black level no longer affects white areas and vice versa
- Added new controls to the Per Hue panel for Blender 4.5
    - The Perceptual control allows you to shift using the LAB color model
    - Range and Smoothing control how similar colors are affected
    - Saturation and Value masking allow you to target specific shades of a color
- Improved Per Value Saturation for Blender 4.5
- Improved Color Blending falloff for Blender 4.5

## 1.2.9
- Lowered default highlight cutoff in Tone Mapping panel
- Ported improved vignette to Blender 4.2 - 4.4
- Fixed error when Render Raw is enabled but the node is deleted
- Fixed issue with getting preset from earlier versions

## 1.2.8
- Added improved vignette for Blender 4.5
- Added Tone Mapping options for blending aspects of sRGB and Filmic with AgX
- Fixed issue with upgrading from beta builds

## 1.2.7
- Fixed issue with Texture effect on transparent backgrounds
- Fixed issue with upgrading nodes when setup is corrupted
- Fixed CPU artifacting when saturation exceeded 1 in perceptual method
- Fixed CPU artifacting when extreme clarity settings push values above 1
- Fixed values in panels not showing as disabled when category is disabled
- Fixed Subtle Pop preset including grain
- Added support for Blender 4.5 alpha
    - Improved film grain performance
    - Improved film grain desaturation

## 1.2.6
- Added output socket for glare pass
- Added a tint control to the vignette
- Fixed install issue on Mac

## 1.2.5
- Fixed enabling Render Raw in multiple scenes

## 1.2.4
- Fixed some tabs not working

## 1.2.3
- Improved UI to be more compact
    - Properties are now grouped more tightly together
    - Added tabs to some panels
    - Hue / Hue, Hue / Saturation, and Hue / Value are now under Per Hue
    - Color Blending and Value / Saturation are now under Per Value
    - Fixed sub-panel header spacing
- Added pre-transform curves
- Added controls for curve tone, black level, and white level
- Re-added option to use a view transform instead of raw while rendering
- Allow Animated Values now works with layers
    - Though using it with them is currently super slow
- Fixed duplicated Render Raw node flagged as needing upgrade
- Fixed issue with saving gamma corrected colors in presets
- Improved upgrading nodes from previous versions
- Improved performance by caching active nodes and layers
- Improved error when loading a preset that was deleted outside of Blender
- Lots of code cleanup

## 1.2.2
This version includes a few hotfixes for issues in version 1.2. Please read the release notes for 1.2 as well if you are upgrading from 1.1 or before.
- Fixed enabling Render Raw in Edit Mode
- Fixed scene exposure and gamma not applied when refreshing nodes
- Fixed error when using render handlers
- Fixed issue with upgrading nodes from older versions
- Added strength sliders to Effects panels when closed

Due to a bug in Blender 4.4, the Show Raw During Rendering option has been removed for Blender 4.4 for now.

## 1.2.1
This version includes a few hotfixes for issues in version 1.2. Please read the release notes for 1.2 as well if you are upgrading from 1.1 or before.
- Fixed glare streaks and ghosting thresholds in Blender 4.4
- Fixed saving presets in Blender 4.4
- Fixed layers having some settings linked
- Fixed Refresh Nodes operator

## 1.2.0
Render Raw 1.2 is a fairly significant refactor that fixes some key issues.

If you are upgrading a project from an earlier version, please save a backup before upgrading. The new version will automatically upgrade your node setup (you may need to re-enable Render Raw) and you will not be able to use the new node setup with earlier versions of the add-on.

When you do upgrade though, you'll be able to use as many Render Raw nodes in your scene as you want, and they can all have separate settings. This change also fixes the issues with swapping between multiple scenes in the same file.

If you choose to work with multiple Render Raw nodes, here are some think you'll need to know:
- The settings are saved in the group and not the node itself, so you can have multiple nodes that all share the same settings if you'd like
- Duplicating the node and making it a single user does not make it a fully independant copy, since the sub-groups inside the node are still linked. To make a fully unique copy, either use the Duplicate Render Raw Node command in the Utilities section or use Unlink Render Raw Node on an existing node that you would like to make unique. I hope to remove this step in the future but it is needed for now.
- You can switch which group is being edited in the 3D View or Properties by selecting the node in the Compositor to make it the active node, or you can use the dropdown that will appear at the top of the settings when you have multiple groups in the scene.
- You should be able to nest Render Raw nodes inside of other groups just fine and the add-on will recursively search to find them.

Another important change this update made possible is the introduction of a layer system. With it, you can stack different effects on top of each other within each Render Raw group. While this opens the door to lots of crazy functionality down the road, it is currently not super useful and so it is disabled in the add-on preferences by default since it takes up some space in the UI. Once the system has masking and can support different render passes though, things will get interesting. For now, here's what you need to know about layers:
- The panel is disabled in the UI by default, but you can enable it if you want in the Render Raw preferences
- Layers do not yet work properly with the experimental Allow Animated Values option

Some other new features and fixes in this version include:
- Updated bloom to support Blender 4.4
    - Since the size property has changed in Blender 4.4, upgrading a scene from a previous version of Blender may require a bloom size adjustment
- Added option to visualize clipped white, black, and oversaturated areas
    - You can find this in Utilities under Overlays
    - The strength of the effect is controlled by the color's alpha
    - There is currently no way to only display it in the viewport and not the render, so be sure to turn it off before you render
- Added factor setting for the curves adjustments
- Fixed Lift / Gamma / Gain and Offset / Power / Slope gamma correction
- Fixed many smaller issues
- Reorganized property panels

## 1.1.1
- Fixed thin line around transparent images
- Added option to manage alpha type in Utilities
- Added panels to Utilities section

## 1.1.0
- Added support for the new white balance feature in Blender 4.3
- Improved built-in presets, including adding a new one called Subtle Pop
- Fixed issue with Allow Animated Values not actually turning off

## 1.0.9
- Enabled animated values as experimental option.
    - Currently, you need to move the current time to the start of the animation in order for the first frame to render correctly.
    - It is also currently more efficient to leave this setting off.
- Added option to change sidebar tab name
- Fixed issue with saving enum properties in presets

## 1.0.8
- Enabled Show Raw While Rendering by default since the transform swap does not work with some edge cases
- Fix CPU compositor vignette in Blender 4.2

## 1.0.7
- Added option to disable RAW view while rendering

## 1.0.6
- Added option to switch compositor device
- Added size control to Bloom

## 1.0.5
- Added support for Khronos PBR Neutral
- Fixed issue with ACES gamma

## 1.0.4
- Fixed shifting vignette in Blender 4.2 CPU compositor
- Added support for new bloom in Blender 4.2

## 1.0.3
- Added compatibility for Blender 4.2 Alpha

## 1.0.2
- Fixed Color Management panel appearing in all tabs after disabling RR

## 1.0.1
- Fixed incorrect preset names on Mac

## 1.0.0
- We're out of beta!
- Made highlight, midtone, and shadow ordering consistent
- Centered value controls around 0
- Added version handling to presets for when controls change
- Added steps control to fast film grain
- Added ability to scale vignette outside of camera bounds
- Added 'under the hood' scene color management settings to utilities panel
- Fixed darkening when desaturating film grain
- Fixed color blending not muting when Use Colors was disabled
- Improved default presets
- Minimum Blender version bumped to 4.1 for stability

## 0.9.5
- Added Perceptual control to saturation per value panel
- Added Offset Power Slope control to color balance panel
- Reorganized color panels

## 0.9.4
- Fixed issue with setting preset folder on Mac
- Added descriptive tooltips to all controls
- Removed the Keep Color control under Texture for being cryptic and not very useful
- Fixed panel error when addon preferences could not be found

## 0.9.3
- Fixed issue when duplicate RR sub node groups exist in the file
- Fixed issue with glare sometimes causing black spots in 8 bit renders

## 0.9.2
- Added button to refresh node tree
- Added link to docs

## 0.9.1
- Improved contrast control to better match AgX looks
- Improved color boost and perceptual saturation with the YUV color model
- Added control for saturation of film grain

## 0.9.0
- First public release