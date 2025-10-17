---
excerpt: Documentation for the Render Raw add-on for Blender
nav_order: 6
nav_exclude: false
search_exclude: false
---

# Preferences

## Presets Folder
In order to save and load custom presets, you must specify where on your computer those presets should be saved. This ensures that they are not overwritten when moving between versions of Blender and Render Raw.

## Interface
You may turn off Render Raw's 3D View sidebar panel or choose which tab it appears in.

## Layers
Enabling layers will change the Render Raw interface to show a layer stack, where settings can be customized per layer. This is off by default because it takes up space and is not currently all that useful. But it will be extremely useful in the future when masking is added and Blender adds support for using render passes in the viewport compositor. Imagine easily color correcting just the materials with emission, adding different glare to a specific light source, or mixing in haze based on the Z-depth. Coming soon!

## Viewport Compositing 
All 3D viewports switch over to enabling the compositor when Render Raw is enabled, but you can disable this feature or set it to only influence the active workspace or no viewports at all if you don't want it messing with your settings. 

## Render Compositing
Render Raw can temporarily turn off the Raw view transform while rendering with Cycles so that you can get a better view of the final result while its working. This also temporarily disables viewport compositing during rendering, so that the viewport doesn't appear washed out due to the double transform. While nice, this is disabled by default since it relies on a part of Blender's API that is not always stable when rendering animations (the pre-render and post-render handlers). 

## Animation
Due to not all of Blender's compositing nodes having sockets for their controls, many of Render Raw's node groups cannot be controlled from the node itself and need some adjusting via Python, and are therefore custom properties. Blender does not like changing custom properties during renders, but you can force animation to work by choosing the Enable Animated Values option. This is disabled by default because it can be unstable. It also requires you to change your timeline to the beginning of the animation before rendering in order for the first frame to recieve the correct values. 

Now that Blender 4.5 has proper sockets for more compositing node controls, I will be going through and upgrading the setup so that values can be animated directly and not need custom properties. This will remove the animation limitations of Render Raw for most effects but will take some time to implement. 