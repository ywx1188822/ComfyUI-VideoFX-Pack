import torch
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.color import adjust_saturation, adjust_hue, adjust_lightness
from utils.transforms import tensor_to_pil, pil_to_tensor


class SaturationHueNode:
    """🎨 Saturation & Hue - 饱和度/色调/明度静态调节"""

    CATEGORY = "Image/Adjustment"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "saturation": ("FLOAT", {"default": 0.0, "min": -100.0, "max": 100.0, "step": 1.0}),
                "hue_shift": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 360.0, "step": 1.0}),
                "lightness": ("FLOAT", {"default": 0.0, "min": -100.0, "max": 100.0, "step": 1.0}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "adjust"

    def adjust(self, image, saturation, hue_shift, lightness):
        # Process every frame in the batch
        output_frames = []
        for i in range(image.shape[0]):
            img_np = image[i].cpu().numpy()  # [H,W,C] float32
            if saturation != 0.0:
                img_np = adjust_saturation(img_np, saturation)
            if hue_shift != 0.0:
                img_np = adjust_hue(img_np, hue_shift)
            if lightness != 0.0:
                img_np = adjust_lightness(img_np, lightness)
            output_frames.append(torch.from_numpy(np.clip(img_np, 0, 1).astype(np.float32)))
        return (torch.stack(output_frames),)


NODE_CLASS_MAPPINGS = {
    "SaturationHueNode": SaturationHueNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaturationHueNode": "🎨 Saturation & Hue"
}
