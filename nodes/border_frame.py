import torch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.color import hex_to_rgb


class BorderFrameNode:
    """🔲 Border Frame - 边框相框"""

    CATEGORY = "Image/Utility"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "border_size": ("INT", {"default": 20, "min": 1, "max": 200}),
                "border_color": ("STRING", {"default": "#FFFFFF"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, border_size, border_color):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img_tensor = image.permute(0, 3, 1, 2).to(device)
        b, c, h, w = img_tensor.shape
        
        rgb = hex_to_rgb(border_color)
        border = torch.tensor(rgb, device=device).view(1, 3, 1, 1) / 255.0
        
        framed = img_tensor.clone()
        framed[:, :, :border_size, :] = border
        framed[:, :, -border_size:, :] = border
        framed[:, :, :, :border_size] = border
        framed[:, :, :, -border_size:] = border
        
        return (framed.permute(0, 2, 3, 1).cpu().float(),)


NODE_CLASS_MAPPINGS = {"BorderFrame": BorderFrameNode}
NODE_DISPLAY_NAME_MAPPINGS = {"BorderFrame": "🔲 Border Frame"}
