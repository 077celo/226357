---
excerpt: Documentation for the Render Raw add-on for Blender
nav_order: 8
nav_exclude: false
search_exclude: false
---

# Customizing Blender

## Render Engines

You can use Render Raw with custom render engines in Blender besides Eevee and Cycles as long as they can provide a linear image to the compositor.

For example, in Octane for Blender, you'll need to set the Response Curve in the Tone Mapping panel to Linear/Off.

![Octane settings](/images/octane.png)

## View Transforms

Render Raw also supports all of the custom view transforms found in the [Pixel Manager OCIO config](https://github.com/Joegenco/PixelManager). 

Just be sure to enable an inactive space in the OCIO file that allows the transforms be used in the compositor, as shared in the Pixel Manager instructions. If you do not do this, the available view transforms list will appear empty. I would recommend using the `STUDIO-Comp-Grading` preset on line `309` so that all are available for Render Raw to use. Since only one inactive space can be used at a time, make sure you've commented out the `MINIMAL` inactive space on line `298`. 

You can also use any of your own view transforms if you specify them in the add-on's `supported_xforms` in `constants.py`. If there are any that you think should be supported by the add-on out of the box, let me know and I'd be happy to add them. 

## Add-ons

Render Raw should work with most add-ons. However, since it relies on the scene color management to be set to specific values under the hood, any add-ons that automatically update the scene exposure or view transform will break the look of the render. You can always fix this by toggling Render Raw correction off and on again, or by going to the Utilities section and using the Reset Scene Color Settings operator. 