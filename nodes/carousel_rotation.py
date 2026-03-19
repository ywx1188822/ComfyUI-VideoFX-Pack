import torch
import numpy as np
from PIL import Image
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.transforms import tensor_to_pil, pil_to_tensor


class CarouselRotationNode:
    """🎪 Carousel Rotation - 旋转木马效果"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "rotation_angle": ("FLOAT", {"default": 360, "min": -720, "max": 720, "step": 1}),
                "tilt_angle": ("FLOAT", {"default": 15, "min": -45, "max": 45, "step": 1}),
                "total_seconds": ("INT", {"default": 6, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "enable"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, width, height, fps, rotation_angle, tilt_angle, total_seconds, loop_mode):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img = image.squeeze(0) if image.shape[0] == 1 else image[0]

        img_tensor = img.permute(2, 0, 1).to(device)
        total_frames = int(total_seconds * fps)
        
        frames = []
        for frame_idx in range(total_frames):
            progress = frame_idx / total_frames
            
            if loop_mode == "enable":
                phase = math.sin(progress * math.pi)
            else:
                phase = progress
            
            current_rotation = rotation_angle * phase
            
            rotated = self.rotate_with_tilt(img_tensor, current_rotation, tilt_angle)
            frames.append(rotated)
        
        result = torch.stack(frames, dim=0).permute(0, 2, 3, 1).cpu().float()
        return (result,)
    
    def rotate_with_tilt(self, img_tensor, angle, tilt):
        b, c, h, w = img_tensor.shape
        angle_rad = math.radians(angle)
        
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        tilt_rad = math.radians(tilt)
        scale_y = math.cos(tilt_rad)
        
        theta = torch.tensor([
            [cos_a, -sin_a, 0],
            [sin_a * scale_y, cos_a * scale_y, 0]
        ], dtype=torch.float32, device=img_tensor.device).unsqueeze(0).expand(b, -1, -1)
        
        grid = torch.nn.functional.affine_grid(theta, (b, c, h, w), align_corners=False)
        rotated = torch.nn.functional.grid_sample(img_tensor, grid, align_corners=False, padding_mode='border')
        
        return rotated


NODE_CLASS_MAPPINGS = {
    "CarouselRotation": CarouselRotationNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CarouselRotation": "🎪 Carousel Rotation",
}
