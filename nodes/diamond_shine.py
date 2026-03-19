import torch
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DiamondShineNode:
    """💎 Diamond Shine - 钻石闪耀效果"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "shine_intensity": ("FLOAT", {"default": 1.5, "min": 0.1, "max": 3.0, "step": 0.1}),
                "shine_count": ("INT", {"default": 8, "min": 4, "max": 16}),
                "total_seconds": ("INT", {"default": 6, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "enable"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, width, height, fps, shine_intensity, shine_count, total_seconds, loop_mode):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img = image.squeeze(0) if image.shape[0] == 1 else image[0]

        img_tensor = img.permute(2, 0, 1).to(device)
        total_frames = int(total_seconds * fps)
        
        frames = []
        for frame_idx in range(total_frames):
            progress = frame_idx / total_frames
            phase = math.sin(progress * math.pi * 2 * shine_count) if loop_mode == "enable" else progress
            
            enhanced = self.add_shine(img_tensor, phase, shine_intensity)
            frames.append(enhanced)
        
        result = torch.stack(frames, dim=0).permute(0, 2, 3, 1).cpu().float()
        return (result,)
    
    def add_shine(self, img_tensor, phase, intensity):
        enhanced = img_tensor * (1 + intensity * math.sin(phase))
        return torch.clamp(enhanced, 0, 1)


NODE_CLASS_MAPPINGS = {"DiamondShine": DiamondShineNode}
NODE_DISPLAY_NAME_MAPPINGS = {"DiamondShine": "💎 Diamond Shine"}
