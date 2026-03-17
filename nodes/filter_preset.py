import torch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FilterPresetNode:
    """🎨 Filter Preset - 滤镜预设"""

    CATEGORY = "Image/Adjustment"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "preset": (["vintage", "cool", "warm", "black_white", "sepia"],),
                "intensity": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.05}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, preset, intensity):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img_tensor = image.permute(0, 3, 1, 2).to(device)
        
        if preset == "vintage":
            filtered = self.vintage_filter(img_tensor, intensity)
        elif preset == "cool":
            filtered = self.cool_filter(img_tensor, intensity)
        elif preset == "warm":
            filtered = self.warm_filter(img_tensor, intensity)
        elif preset == "black_white":
            filtered = self.black_white(img_tensor, intensity)
        elif preset == "sepia":
            filtered = self.sepia(img_tensor, intensity)
        else:
            filtered = img_tensor
        
        return (filtered.permute(0, 2, 3, 1).cpu().float(),)
    
    def vintage_filter(self, img, intensity):
        result = img.clone()
        result[:, 0] *= (1 + 0.1 * intensity)
        result[:, 1] *= (1 - 0.1 * intensity)
        return torch.clamp(result, 0, 1)

    def cool_filter(self, img, intensity):
        result = img.clone()
        result[:, 2] *= (1 + 0.2 * intensity)
        return torch.clamp(result, 0, 1)

    def warm_filter(self, img, intensity):
        result = img.clone()
        result[:, 0] *= (1 + 0.2 * intensity)
        result[:, 2] *= (1 - 0.1 * intensity)
        return torch.clamp(result, 0, 1)

    def black_white(self, img, intensity):
        gray = 0.299 * img[:, 0] + 0.587 * img[:, 1] + 0.114 * img[:, 2]
        return torch.stack([gray, gray, gray], dim=1) * intensity + img * (1 - intensity)

    def sepia(self, img, intensity):
        original = img.clone()
        r, g, b = img[:, 0], img[:, 1], img[:, 2]
        sepia_img = img.clone()
        sepia_img[:, 0] = torch.clamp(r * 0.393 + g * 0.769 + b * 0.189, 0, 1)
        sepia_img[:, 1] = torch.clamp(r * 0.349 + g * 0.686 + b * 0.168, 0, 1)
        sepia_img[:, 2] = torch.clamp(r * 0.272 + g * 0.534 + b * 0.131, 0, 1)
        return sepia_img * intensity + original * (1 - intensity)


NODE_CLASS_MAPPINGS = {"FilterPreset": FilterPresetNode}
NODE_DISPLAY_NAME_MAPPINGS = {"FilterPreset": "🎨 Filter Preset"}
