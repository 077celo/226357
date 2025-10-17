---
excerpt: Documentation for the Render Raw add-on for Blender
nav_order: 1
nav_exclude: false
search_exclude: false
---

# Enabling Render Raw

The Render Raw color settings can be found in the Properties Editor in the Render tab under Color Management.

_Render Raw replaces the existing Color Management panel because it needs to change those settings under the hood in order for it to work correctly._

To use the add-on, click Enable Render Raw. This will add the compositing setup, switch on Viewport Compositing (if enabled in the preferences), and display the adjustment panels.

The adjustment panels are also displayed in the Render tab in the 3D Viewport sidebar and in the Node tab of the Compositor sidebar when a Render Raw node is selected.

The Render Raw compositing node is added right before the output node by default. You can move it to anywhere in your node tree if you have an existing compositing setup, but if the node is deleted, renamed, or altered too much the add-on will not work.

You can duplicate the Render Raw node and use it in multiple places in the compositor if you'd like. Because it makes use of sub-groups, if you want each Render Raw node to have fully independant settings, you will need to use the Duplicate Render Raw Node button under Utilities -> Node instead of using Shift + D.

## How it works

As the name implies, Render Raw makes use of the Raw view transform option behind the scenes for advanced color management via the Compositor. When using the add-on, viewport compositing needs to be enabled in order for the correct colors to display in the viewport. If you create a new 3D View, be sure to go to Viewport Shading and set Compositing to Always. Because Blender allows but does not favor custom color management, material previews and other results of rendering that do not recieve compositing may look incorrect while Render Raw correction is enabled.

The View Transform, Exposure, Gamma, and other color management settings seen when Render Raw is enabled are not the same as the default Blender settings by the same name. Changing the Blender settings via python while Render Raw is enabled may break the look of the scene. If this happens, just toggle Enable Render Raw off and on again or go to Utilities -> Actual Scene Values -> Reset Scene Color Settings. I will try to make Render Raw more compatible with other add-ons which set exposure in the future.

In tooltips and in the documentation, effects are either listed as pre-transform or post-transform. Pre-transform means that the effect is happening in the linear colorspace before your chosen color transform (like AgX) is applied. Post-transform means that the effect is happening in the sRGB colorspace after the transform is applied. Pre-transform effects are considered "safe" because they will not cause clipping and are fully reversible when used with a proper transform like AgX or Filmic. Post-transform effects are considered less safe because they can skew, compress, or "break" the colors. However, this ability to break the colors is exactly what gives you the ability to control their exact output.

If you want to add your own effects in the compositor in addition to the Render Raw node, be sure that any linear effects (such as glare) are added before the Render Raw node and any sRGB effects (like sharpening) are added after it.