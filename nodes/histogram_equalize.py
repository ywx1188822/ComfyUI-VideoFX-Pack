import torch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class HistogramEqualizeNode:
    """📊 Histogram Equalize - 直方图均衡"""

    CATEGORY = "Image/Adjustment"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 1.0, "step": 0.05}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, strength):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img_tensor = image.permute(0, 3, 1, 2).to(device)
        
        equalized = self.equalize(img_tensor)
        result = equalized * strength + img_tensor * (1 - strength)
        
        return (result.permute(0, 2, 3, 1).cpu().float(),)
    
    def equalize(self, img):
        b, c, h, w = img.shape
        equalized = []
        
        for i in range(c):
            channel = img[:, i]
            hist = torch.histc(channel, bins=256, min=0, max=1)
            cdf = hist.cumsum(dim=0)
            cdf_min = cdf[cdf > 0].min() if (cdf > 0).any() else 0
            cdf_normalized = (cdf - cdf_min) / (h * w - cdf_min)
            equalized_channel = cdf_normalized[(channel * 255).long()]
            equalized.append(equalized_channel)
        
        return torch.stack(equalized, dim=1)


NODE_CLASS_MAPPINGS = {"HistogramEqualize": HistogramEqualizeNode}
NODE_DISPLAY_NAME_MAPPINGS = {"HistogramEqualize": "📊 Histogram Equalize"}
