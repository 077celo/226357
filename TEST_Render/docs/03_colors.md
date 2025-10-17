---
excerpt: Documentation for the Render Raw add-on for Blender
nav_order: 3
nav_exclude: false
search_exclude: false
---

# Color Adjustments
All color adjustments can be enabled or disabled at once by using the checkbox in the panel header. 

## Temperature and Tint
Increasing or decreasing the Temperature control moves the colors towards a warmer or cooler hue by adjusting the red and blue channels of each pixel. Tint manages the amount of green in the green channel. Both controls are pre-transform. 

The Perceptual slider allows you to blend between simply multiplying the RGB values or using Blender's chromatic adaption formula for the white balance. The latter is generally nicer for most cases but becomes less stable at very low temperatures

## Color Boost
Increases or decreases the saturation in lower saturated areas without affecting higher saturated areas. This is helpful for making the image more colorful overall without blowing out the already saturated colors or for emphasizing the most saturated colors by desaturating the rest. This effect is very safe because it is pre-transform and cannot cause color clipping.

## Saturation
Increases or decreases the saturation uniformly. The Perceptual control attempts to keep the perceived values of the colors the same using the YUV color model instead of the HSV color model. Using the Perceltual method is almost always preferred when decreasing saturation, but can cause value clipping when increasing saturation. Since saturation is a post-transform effect, increasing it too much can cause color clipping in either model. 

## Density
Decreases the value of saturated areas while also boosting their saturation, resulting in a "deeper" color. Its Value Mask determines whether the effect is applied to just the bright areas or just the dark areas. 

## Color Balance
Offset, Power, and Slope can be adjusted for safe, pre-transform color correction while Lift, Gamma, and Gain can be adjusted for more intuitive but less safe post-transform corrections. 

## Per Hue Adjustments 
Hue, Saturation, and Value can also be adjusted per hue, post-transform. Each hue control is evenly spaced around the color wheel except for Orange, which has been added for convenience. 

The Perceptual slider allows you to use the LAB color model for shifting hue and saturation, which should result in more pleasing and expected results than when using HSV. Range adjusts how similar colors need to be to the target hue in order to be affected, and Smoothing adjusts how smooth that falloff is. 

The Saturation Mask and Value Mask sliders allow you to target saturated or unsaturated areas and bright or dark areas to be really specific about which shade of the color you are adjusting. 

## Per Value Adjustments 
The Highlight, Midtone, and Shadow color blending options allow for a wide variety of creative looks. To set highlights, midtones, or shadows to an exact color, just set the blending type to Mix. 

Saturation can be adjusted separately for highlights, midtones, and shadows as well, which can be helpful for emulating some film looks and making sure highlights are not blown out. 

Both the Color and Saturation Per-Value controls are post-transform. 

## Tone Mapping
The properties in the Tone Mapping panel give more control over the colors that result from the chosen View Transform. 

The Filmic slider allows you to mix in vibrant colors from the Filmic transform up to the Highlight Cutoff threshold value. This effect is quite safe, unlike the sRGB controls. 

the sRGB sliders allow you to mix in colors from the Standard color transform while retaining the soft highlight rolloff of AgX or your chosen View Transform. This allows AgX to function like the PBR Neutral transform that preserves hues from textures but with greater control and dynamic range. However, transitions between saturated colors may look worse. There is a good reason AgX shifts hues! It is recommended to have sRGB Hue and Saturation set to the same value, but they are provided as seperate controls for greater flexibility. 

One of the best uses for the above controls is mixing in color back into areas that are supposed to be both bright and colorful. However, areas that are too bright in Blender have their hue set to 0. This is usually not visible since they are fully desaturated at that point, but when bringing back in saturation after the fact, those areas will appear red. The Highlight Cutoff prevents this by making sure that the colors are desaturated before getting to that value. You can customize the cutoff and how smoothly it transitions by adjusting the Spread value. A low spread will preserve the mixed Filmic or sRGB colors all the way up to the highlight, while a higher spread allows for a better transition at the cost of some hue shifting. 

