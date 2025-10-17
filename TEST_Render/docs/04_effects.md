---
excerpt: Documentation for the Render Raw add-on for Blender
nav_order: 4
nav_exclude: false
search_exclude: false
---

# Effects Adjustments
All Effects adjustments can be enabled or disabled at once by using the checkbox in the panel header. 

## Lens Distortion and Dispersion
Simulates the bulging, pinching, and fringing effects of real camera lenses. Unlike the default Blender Lens Distortion, the Render Raw setup supports transparency. It's important to note that the 3D View overlays will not be distorted, so the grid or outlines may overlap your objects a bit and it is recommended to turn off overlays when previewing distortion in the viewport. 

## Glare
Simulates glow around bright pixels. The Bloom effect is a custom implementation that supports transparency, avoids clipping on reflective surfaces, and matches the viewport result with the render result. 

## Vignette
Simulates darkening, lightening, or a custom color around the edges of the viewport. 

The Blending control adjusts how the vignette is mixed with the rendered colors. A value of 0 simply mixes the chosen color on top of the render, post-transform. A value of 1 calculates the effect pre-transform by using addition and multiplication. 

Highlights controls whether or not bright areas can be darkened by the vignette, Feathering blurs the transition of the vignette mask, and Roundness controls how rectangular or elliptical the vignette is. 

The transform controls can be used to precicely place the vignette.

## Film Grain
Simulates the grain from a camera's film or sensor, which is very different from render noise. 

The Fast method simply overlays instances of a voronoi texture on top of the image using a Soft Light blend mode while the Accurate method actually distorts the image so that each grain contains one color - just like real film. The Accurate method has a Steps setting which controls how many layers of grain get mixed together. Higher values look more natural but are much slower to calculate. 

Due to the lack of mapping options in the compositor, the Aspect Correction setting is sometimes needed to fix grain stretching in Blender versions before 4.5. 

The Animate option will change the grain pattern on every frame, which looks more believable but is much slow to preview in the viewport during animation playback. 