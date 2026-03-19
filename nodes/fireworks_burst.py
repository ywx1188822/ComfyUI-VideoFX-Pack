import torch
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FireworksBurstNode:
    """🎆 Fireworks Burst - 烟花绽放效果"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "burst_radius": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.05}),
                "particle_count": ("INT", {"default": 50, "min": 10, "max": 200}),
                "total_seconds": ("INT", {"default": 6, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "disable"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, width, height, fps, burst_radius, particle_count, total_seconds, loop_mode):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img = image.squeeze(0) if image.shape[0] == 1 else image[0]

        img_tensor = img.permute(2, 0, 1).to(device)
        total_frames = int(total_seconds * fps)
        
        frames = []
        for frame_idx in range(total_frames):
            progress = frame_idx / total_frames
            burst = self.burst_effect(img_tensor, progress, burst_radius, particle_count)
            frames.append(burst)
        
        result = torch.stack(frames, dim=0).permute(0, 2, 3, 1).cpu().float()
        return (result,)
    
    def burst_effect(self, img_tensor, progress, radius, count):
        b, c, h, w = img_tensor.shape
        mask = torch.zeros((b, 1, h, w), device=img_tensor.device)
        
        for _ in range(count):
            angle = torch.rand(1).item() * 2 * math.pi
            dist = torch.rand(1).item() * radius * progress
            cx, cy = w // 2 + int(dist * math.cos(angle) * w/2), h // 2 + int(dist * math.sin(angle) * h/2)
            cx, cy = max(0, min(w-1, cx)), max(0, min(h-1, cy))
            mask[:, :, max(0, cy-5):min(h, cy+5), max(0, cx-5):min(w, cx+5)] = 1
        
        return img_tensor * mask


NODE_CLASS_MAPPINGS = {"FireworksBurst": FireworksBurstNode}
NODE_DISPLAY_NAME_MAPPINGS = {"FireworksBurst": "🎆 Fireworks Burst"}
