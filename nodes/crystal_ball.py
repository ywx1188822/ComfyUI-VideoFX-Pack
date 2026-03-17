import torch
import numpy as np
from PIL import Image
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.transforms import tensor_to_pil, pil_to_tensor
from utils.easing import ease_in_out


class CrystalBallRevealNode:
    """🔮 Crystal Ball Reveal - 水晶球揭示效果"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "reveal_radius": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.05}),
                "glow_strength": ("INT", {"default": 2, "min": 0, "max": 5}),
                "total_seconds": ("INT", {"default": 6, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "enable"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, width, height, fps, reveal_radius, glow_strength, total_seconds, loop_mode):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img_tensor = image.permute(0, 3, 1, 2).to(device)
        total_frames = int(total_seconds * fps)
        
        frames = []
        for frame_idx in range(total_frames):
            progress = frame_idx / total_frames
            
            if loop_mode == "enable":
                phase = math.sin(progress * math.pi)
            else:
                phase = progress
            
            # 水晶球揭示效果
            revealed = self.crystal_reveal(img_tensor, phase, reveal_radius, glow_strength)
            frames.append(revealed)
        
        result = torch.stack(frames, dim=0).permute(0, 2, 3, 1).cpu().float()
        return (result,)
    
    def crystal_reveal(self, img_tensor, phase, radius, glow):
        b, c, h, w = img_tensor.shape
        cx, cy = w // 2, h // 2
        
        y, x = torch.meshgrid(torch.arange(h), torch.arange(w), indexing='ij')
        dist = torch.sqrt((x - cx)**2 + (y - cy)**2) / min(cx, cy)
        
        mask = (dist < radius * phase).float().unsqueeze(0).unsqueeze(0)
        
        if glow > 0:
            glow_mask = torch.clamp(mask * (1 - dist / (radius * phase + 0.1)) * glow, 0, 1)
            mask = mask + glow_mask
        
        return img_tensor * torch.clamp(mask, 0, 1)


NODE_CLASS_MAPPINGS = {
    "CrystalBallReveal": CrystalBallRevealNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CrystalBallReveal": "🔮 Crystal Ball Reveal",
}
