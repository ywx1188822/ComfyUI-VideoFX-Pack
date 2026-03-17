import torch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class WatermarkAddNode:
    """🏷️ Watermark Add - 水印添加"""

    CATEGORY = "Image/Utility"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "watermark_text": ("STRING", {"default": "© Your Name"}),
                "font_size": ("INT", {"default": 24, "min": 12, "max": 100}),
                "position": (["bottom-right", "bottom-left", "top-right", "top-left"],),
                "opacity": ("FLOAT", {"default": 0.5, "min": 0.1, "max": 1.0, "step": 0.05}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, watermark_text, font_size, position, opacity):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img_tensor = image.permute(0, 3, 1, 2).to(device)
        b, c, h, w = img_tensor.shape
        
        watermarked = img_tensor.clone()
        # 简化实现：在角落添加色块表示水印位置
        block_size = int(len(watermark_text) * font_size * 0.6)
        
        if "right" in position:
            x_start = w - block_size - 20
            x_end = w - 20
        else:
            x_start = 20
            x_end = 20 + block_size
        
        if "bottom" in position:
            y_start = h - font_size - 20
            y_end = h - 20
        else:
            y_start = 20
            y_end = font_size + 20
        
        watermarked[:, :, y_start:y_end, x_start:x_end] *= (1 - opacity)
        
        return (watermarked.permute(0, 2, 3, 1).cpu().float(),)


NODE_CLASS_MAPPINGS = {"WatermarkAdd": WatermarkAddNode}
NODE_DISPLAY_NAME_MAPPINGS = {"WatermarkAdd": "🏷️ Watermark Add"}
