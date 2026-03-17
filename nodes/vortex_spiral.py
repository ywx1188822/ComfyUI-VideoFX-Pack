import torch
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class VortexSpiralNode:
    """🌪️ Vortex Spiral - 漩涡螺旋效果"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "spiral_strength": ("FLOAT", {"default": 2.0, "min": 0.1, "max": 5.0, "step": 0.1}),
                "rotation_direction": (["clockwise", "counter-clockwise"],),
                "total_seconds": ("INT", {"default": 6, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "enable"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, width, height, fps, spiral_strength, rotation_direction, total_seconds, loop_mode):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img_tensor = image.permute(0, 3, 1, 2).to(device)
        total_frames = int(total_seconds * fps)
        
        frames = []
        for frame_idx in range(total_frames):
            progress = frame_idx / total_frames
            phase = math.sin(progress * math.pi) if loop_mode == "enable" else progress
            
            direction = 1 if rotation_direction == "clockwise" else -1
            rotated = self.spiral_distort(img_tensor, phase * spiral_strength * direction)
            frames.append(rotated)
        
        result = torch.stack(frames, dim=0).permute(0, 2, 3, 1).cpu().float()
        return (result,)
    
    def spiral_distort(self, img_tensor, strength):
        b, c, h, w = img_tensor.shape
        y, x = torch.meshgrid(torch.arange(h), torch.arange(w), indexing='ij')
        y, x = y.float().to(img_tensor.device), x.float().to(img_tensor.device)
        
        cx, cy = w // 2, h // 2
        dx, dy = x - cx, y - cy
        dist = torch.sqrt(dx**2 + dy**2)
        angle = torch.atan2(dy, dx) + dist * strength * 0.01
        
        new_x = cx + dist * torch.cos(angle)
        new_y = cy + dist * torch.sin(angle)
        
        new_x = torch.clamp(new_x, 0, w - 1) / (w - 1) * 2 - 1
        new_y = torch.clamp(new_y, 0, h - 1) / (h - 1) * 2 - 1
        
        grid = torch.stack([new_x, new_y], dim=-1).unsqueeze(0).expand(b, -1, -1, -1)
        distorted = torch.nn.functional.grid_sample(img_tensor, grid, align_corners=False, padding_mode='border')
        
        return distorted


NODE_CLASS_MAPPINGS = {"VortexSpiral": VortexSpiralNode}
NODE_DISPLAY_NAME_MAPPINGS = {"VortexSpiral": "🌪️ Vortex Spiral"}
