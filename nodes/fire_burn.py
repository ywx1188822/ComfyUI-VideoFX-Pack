import torch
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FireBurnNode:
    """🔥 Fire Burn - 火焰燃烧效果"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768}),
                "height": ("INT", {"default": 512}),
                "fps": ("INT", {"default": 24}),
                "fire_intensity": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0}),
                "total_seconds": ("INT", {"default": 6, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "enable"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, width, height, fps, fire_intensity, total_seconds, loop_mode):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img = image.squeeze(0) if image.shape[0] == 1 else image[0]

        img_tensor = img.permute(2, 0, 1).to(device)
        total_frames = int(total_seconds * fps)
        frames = []
        
        for frame_idx in range(total_frames):
            progress = frame_idx / total_frames
            phase = math.sin(progress * math.pi * 2) if loop_mode == "enable" else progress
            frames.append(self.fire_effect(img_tensor, phase, fire_intensity))
        
        return (torch.stack(frames, dim=0).permute(0, 2, 3, 1).cpu().float(),)
    
    def fire_effect(self, img, phase, intensity):
        enhanced = img.clone()
        enhanced[:, 0] *= (1 + intensity * math.sin(phase))
        enhanced[:, 1] *= (1 + intensity * 0.5 * math.sin(phase * 1.5))
        return torch.clamp(enhanced, 0, 1)


NODE_CLASS_MAPPINGS = {"FireBurn": FireBurnNode}
NODE_DISPLAY_NAME_MAPPINGS = {"FireBurn": "🔥 Fire Burn"}
