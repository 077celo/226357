---
excerpt: Documentation for the Render Raw add-on for Blender
nav_order: 2
nav_exclude: false
search_exclude: false
---

# Value Adjustments

All value adjustments can be enabled or disabled at once by using the checkbox in the panel header. 

## Exposure
Used to control the image brightness (in stops). 

The exposure in Render Raw can be used just like Blender's scene exposure control but is a totally seperate property. The Render Raw exposure is the first node in the compositing chain, while Blender's exposure is applied last after all compositing. Because of this, Render Raw always needs the Blender scene exposure to be set to 0 under the hood. Enabling Render Raw will set the scene exposure to 0 and swap out that control for the Render Raw node exposure control and set it to the same value. You should not notice any difference in using the control. 

## Gamma
Extra gamma correction applied after the exposure. Similar to the exposure control, it is a seperate property from Blender's scene gamma. However, adjusting the scene gamma on top of Render Raw is not an issue. 

## Contrast
A scaling factor by which to make brighter pixels brighter while keeping the darker pixels dark. This is applied before the color transform and functions like the Filmic and AgX contrast looks but with more control. 

## Levels
The Blacks, Shadows, Hightlights, and Whites controls can be used to map the range of values in the render, similar to RGB curves but with sliders for ease of use. Increasing Whites is often helpful for making almost-white pixels perfectly white, and decreasing Blacks can be helpful for making almost-black pixels perfectly black. You may also want to do the opposite in order to expand the dynamic range if other Render Raw settings are causing the values to clip. 

The Shadows and Highlights controls smoothly increase or decrease the values around the 0.25 and 0.75 points respectively. If you need to adjust the midtones, consider changing the exposure or using curves. 

All of the Levels controls happen after the color transform and should be used carefully since they can easily cause clipping.

## Fix Clipping
Softly clamps the value and saturation of pixels to 1. While this won't help the look of extreme clipping, it can help salvage shots that have been pushed just a little too far. 

## Sharpness
Adds contrast to edges after the color transform to make the image appear more crisp. The Masking option can be used to only sharpen detected edges that already have a high contrast, which helps avoid the look of over-sharpening.

## Texture
Increases or decreases contrast in only the midtone values after the color transform. The Keep Color control makes it so that the contrast only affects the each color's values and not its hue and saturation. 

## Clarity
Increases or decreases the difference between neighboring values after the color transform. The main difference between Clarity and Sharpening is that Clarity can be smoothly spread over a wider area by using the Size control. 

Higher clarity can make subjects pop out from the background while lower clarity can help soften and blend harsh edges. 

## Curves 
Increases or decreases the output value per input value. The Pre curves adjust the linear values before the color transform while the Post curves adjust the sRGB values after the transform. The Pre curves are "safe" and will not cause clipping like the Post curves can, but are not as intuitive to work with since they are not bound to the 0-1 range. 

