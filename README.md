# Gradio Base64-images Monkeypatch
#### (for stable-diffusion-webgui)

###### $$\color{red}{Warning:}$$
```diff
- By dint of being a monkeypatch in the guts of Gradio:
- This is VERY FRAGILE to any future changes!
- (And may break at any time!)
```

This is a monkeypatch that forces Gradio to serve base64 image URIs (rather than saving files to a temporary directory to host them) when serving an image gallery from PIL data sources (likely incidentally working with other Gradio projects that feed PIL images to an output gallery; however string-based and numpy images currently retain the original behaviour so your mileage may vary).

> __Note__
> When running this script as an extension in Stable Diffusion Webgui, you will need to restart the program after disabling this script for the disabling to take effect.

> __Warning__
> **If you find something breaks when the server attempts to serve an image, now or in the future, you are advised to remove this script** as the first step taken; likewise, it is generally **extremely inadvisable to place this script in any environment with more than one maintaining human involved** (lest someone be blindsided by a monkeypatch in files far away from the apparent problem)

The motivation for this monkeypatch is an apparent lack of built-in mechanisms for cleaning up the temporary files Gradio creates at runtime when hosting images that would not otherwise be saved (which can add up reasonably quickly when generating thousands of images).

There are obvious downsides: Handling large (or large numbers of) base64 images in this manner can cause browsers to hang even on quite beefy computers; additionally the Chrome browser refuses to let users copy the URI of even-moderately-large images or open them in a new tab/window, and of course there is the matter of moderately increased memory and internet-bandwidth usage. Accordingly desire for this modification is probably somewhat niche.

*This is an expediency over implementing base64 serving "the right way" (which would currently involve the possibly soon-to-be-depricated `postprocess=False` argument to galleries in Gradio, the use of which would require a major overhaul in stable-diffusion-webgui, which does not seem feasible or reasonable to maintain for a niche use-case).*
