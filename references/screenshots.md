# Authentic simulator captures

Use this optional workflow for demos or store imagery. Marketing imagery is not interaction acceptance evidence.

## Capture

Use one identifiable candidate build with synthetic content. Capture outer display, expanded landscape, expanded portrait, partial folding and actual software-keyboard input as relevant. Localized screenshots should show the corresponding actual UI language.

For a real device chassis, capture the native simulator window or screen with the rendered frame, hinge and side buttons. Move the pointer away, wait for settled animation and dismiss transient overlays. Do not crop the body at the window edge.

`simctl io ... screenshot` generally provides display pixels rather than the simulator chassis. For multi-display debug captures, enumerate the current device's displays before choosing a display ID. Do not assume IDs from a different run or capture a stale inactive display.

## Preserve authentic edges

Generative editing may change text, keyboards or device geometry. Color-threshold masks can preserve internal RGB yet damage edge antialiasing that was blended against the original backdrop. Pixel equality inside a cutout does not prove correct edges.

For a uniform backdrop, an alternative is to preserve an opaque rectangular crop of the entire chassis plus a small background collar, then give the composition the same sampled background color. This retains the original edge transition and shadow without an alpha mask. It is an optional production technique, not an Apple UI requirement.

Sample a blank area outside the chassis, away from chrome, shadows and the pointer. Do not sample the app canvas or hard-code a color from another capture. With gradients, textures or contaminated crop edges, adjust the capture rather than assuming a single color will match.

## Compose

Requires Pillow. Measure current-image coordinates; the following values are only examples:

```sh
python3 scripts/compose_capture.py capture.png composed.png \
  --crop 220,300,1650,1750 --sample 100,200 \
  --canvas 2007,2853 --image-box 140,720,1867,2700
```

Crop and image-box use left,top,right,bottom. Sample coordinates refer to the original whole image. Output is an opaque RGB PNG plus JSON containing source hash, crop, background and placement. The script does not capture UI, add titles, regenerate a device or apply perspective.

Inspect complete chassis, text, keyboard, border blending, scale and claimed features. Enlarge the original capture when resolution is insufficient; interpolation is not native resolution. Add editable titles separately in your design tool if needed.

## Export and publish

Check current [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) for accepted dimensions, device groups and opacity. Keep source provenance, build, locale and pose. Device-framed promotional images are not guaranteed to pass review.

Uploads require authorization in the current task. Inspect the version's editable state before changing assets. Verify actual ordering and processing after asynchronous uploads; do not repeatedly delete and re-upload merely because processing is still pending. Distinguish prepared, uploaded, validated, submitted, approved and published states.
