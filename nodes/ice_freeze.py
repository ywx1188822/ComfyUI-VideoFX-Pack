import torch
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class IceFreezeNode:
    """❄️ Ice Freeze - 冰雪冻结效果"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768}),
                "height": ("INT", {"default": 512}),
                "fps": ("INT", {"default": 24}),
                "freeze_speed": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0}),
                "total_seconds": ("INT", {"default": 6, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "disable"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, width, height, fps, freeze_speed, total_seconds, loop_mode):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img_tensor = image.permute(0, 3, 1, 2).to(device)
        total_frames = int(total_seconds * fps)
        frames = []
        
        for frame_idx in range(total_frames):
            progress = frame_idx / total_frames
            frames.append(self.freeze(img_tensor, progress, freeze_speed))
        
        return (torch.stack(frames, dim=0).permute(0, 2, 3, 1).cpu().float(),)
    
    def freeze(self, img, progress, speed):
        frozen = img * (1 - progress * speed * 0.5)
        return torch.clamp(frozen, 0, 1)


NODE_CLASS_MAPPINGS = {"IceFreeze": IceFreezeNode}
NODE_DISPLAY_NAME_MAPPINGS = {"IceFreeze": "❄️ Ice Freeze"}
