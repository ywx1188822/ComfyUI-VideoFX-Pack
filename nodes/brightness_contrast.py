import torch
import numpy as np
from PIL import Image
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.color import adjust_brightness, adjust_contrast

class BrightnessContrastNode:
    """🎚️ Brightness & Contrast - 亮度对比度调节节点"""
    
    CATEGORY = "Image/Adjustment"
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "brightness": ("INT", {"default": 0, "min": -100, "max": 100}),
                "contrast": ("INT", {"default": 0, "min": -100, "max": 100}),
                "gamma": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 5.0, "step": 0.1}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "adjust"
    
    def adjust(self, image, brightness, contrast, gamma):
        img_np = image.cpu().numpy()
        
        # 应用亮度调节
        if brightness != 0:
            img_np = adjust_brightness(img_np, brightness)
        
        # 应用对比度调节
        if contrast != 0:
            img_np = adjust_contrast(img_np, contrast)
        
        # 应用 Gamma 校正
        if gamma != 1.0:
            img_np = np.power(img_np, 1.0 / gamma)
            img_np = np.clip(img_np, 0, 1)
        
        return (torch.from_numpy(img_np),)

NODE_CLASS_MAPPINGS = {
    "BrightnessContrastNode": BrightnessContrastNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BrightnessContrastNode": "🎚️ Brightness & Contrast"
}
