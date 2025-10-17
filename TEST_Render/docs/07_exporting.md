---
excerpt: Documentation for the Render Raw add-on for Blender
nav_order: 7
nav_exclude: false
search_exclude: false
---

# Exporting

Saving a JPG, PNG, or a TIFF file after rendering with Render Raw is the same as without the add-on. What you see is what you get! 

**Render Raw 1.2.18 and later**

Exporting EXRs now results in linear values, similar to default Blender. What is different, however, is that the view transform that you choose is applied to the render and then converted back into linear space. 

When importing an EXR into Resolve, for example, you will want to use the Linear to sRGB LUT to see the render properly. 

There are no extra steps needed when importing the EXR back into Blender since Blender already assumes that EXRs are linear. Just be sure that no additional view transforms are applied to the imported image besides Standard (Linear Rec 709 to sRGB). 

**Render Raw 1.2.17 and earlier**

EXRs in previous versions of Render Raw, however, work a bit differently than you may be used to. EXRs in Blender are saved without the color managment applied, but because the full view transform is applied directly in Render Raw's compositing node setup rather than the scene's color management, it is baked into the resulting image - just like with the other formats. 

Usually, you would need to import Blender's EXRs as Linear Rec.709 in other applications. But, since the full view transform is applied with Render Raw, you do not need to import them as linear and can import them as sRGB. This is the default in applications like Resolve and Photoshop, so there is often nothing you need to do. To import the image correctly in Blender, simply switch the imported image's Color Space property from Linear to sRGB. 