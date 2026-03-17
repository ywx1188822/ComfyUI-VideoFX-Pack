import torch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CropResizeNode:
    """📐 Crop Resize - 裁剪缩放"""

    CATEGORY = "Image/Utility"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "crop_x": ("INT", {"default": 0, "min": -2048, "max": 2048}),
                "crop_y": ("INT", {"default": 0, "min": -2048, "max": 2048}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, width, height, crop_x, crop_y):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img_tensor = image.permute(0, 3, 1, 2).to(device)
        b, c, h, w = img_tensor.shape
        
        x_start = max(0, crop_x)
        y_start = max(0, crop_y)
        x_end = min(w, w + crop_x) if crop_x < 0 else min(w, crop_x + width)
        y_end = min(h, h + crop_y) if crop_y < 0 else min(h, crop_y + height)
        
        cropped = img_tensor[:, :, y_start:y_end, x_start:x_end]
        resized = torch.nn.functional.interpolate(cropped, size=(height, width), mode='bilinear', align_corners=False)
        
        return (resized.permute(0, 2, 3, 1).cpu().float(),)


NODE_CLASS_MAPPINGS = {"CropResize": CropResizeNode}
NODE_DISPLAY_NAME_MAPPINGS = {"CropResize": "📐 Crop Resize"}
