import base64
from io import BytesIO
import numpy as np
from PIL import Image
import gradio as gr

# It's possible we could just use gradio.processing_utils.encode_pil_to_base64
# But that does something-or-other with metadata; I don't want to test it, and this is short and works.
def img_to_base64uri(image):
    if isinstance(image, str):
        return image # Theoretically could be an internet URL, but that should be fine too.
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image.astype(np.uint8))

    if not isinstance(image, Image.Image):
        raise NotImplementedError # We don't handle other types

    pseudofile = BytesIO()
    image.save(pseudofile, format="PNG")
    base64repr = base64.b64encode(pseudofile.getvalue())
    return f"data:image/png;base64,{base64repr.decode('utf8')}"

# Do a monkey-patch on the gradio gallery postprocess function to make it output base64 strings instead.
old_gallery_postprocess = gr.Gallery.postprocess
def gr_gallery_postprocess_monkeypatch(gallery, y):
    try:
        out_uris = []
        for img in y:
            out_uris.append(img_to_base64uri(img))
        return out_uris
    except Exception: # There are other possible input configurations than that which we address above,
                      # including some that get called during startup. So, fall back in those cases.
        return old_gallery_postprocess(gallery, y)
gr.Gallery.postprocess = gr_gallery_postprocess_monkeypatch
