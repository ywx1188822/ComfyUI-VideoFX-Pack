import torch
import numpy as np
from PIL import Image
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.easing import EASING_FUNCTIONS
from utils.color import hex_to_rgb

class PerspectiveFlipNode:
    """📐 Perspective Flip Card - 透视翻转节点"""
    
    CATEGORY = "Video/Animation"
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "flip_axis": (["horizontal", "vertical"],),
                "flip_angle": ("FLOAT", {"default": 180.0, "min": 0.0, "max": 360.0, "step": 1.0}),
                "perspective_strength": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.1}),
                "background_color": ("STRING", {"default": "#000000"}),
                "total_seconds": ("INT", {"default": 10, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "disable"}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_sequence"
    
    def generate_sequence(self, image, width, height, fps, flip_axis, flip_angle,
                         perspective_strength, background_color, total_seconds, loop_mode="disable"):
        img_tensor = image[0]
        pil_img = Image.fromarray((img_tensor.cpu().numpy() * 255).astype(np.uint8))
        
        total_frames = int(total_seconds * fps)
        output_frames = []
        
        bg_color = hex_to_rgb(background_color)
        img_w, img_h = pil_img.size
        
        for i in range(total_frames):
            progress = i / total_frames
            
            if loop_mode == "enable":
                # 循环模式：翻转 360 度回到原点 (0→1→0)
                loop_phase = math.sin(progress * math.pi)
                current_angle = flip_angle * 2 * loop_phase
            else:
                # 单次模式：单向翻转
                current_angle = flip_angle * progress
            
            # 应用透视翻转
            frame = self.apply_perspective_flip(
                pil_img, current_angle, flip_axis, 
                perspective_strength, (width, height), bg_color
            )
            
            frame_np = np.array(frame).astype(np.float32) / 255.0
            output_frames.append(torch.from_numpy(frame_np))
        
        return (torch.stack(output_frames),)
    
    def apply_perspective_flip(self, img, angle, flip_axis, perspective_strength,
                               target_size, bg_color):
        """应用透视翻转效果（resize + paste 实现）"""
        angle_rad = math.radians(angle)
        result = Image.new('RGB', target_size, bg_color)

        scale = math.cos(angle_rad)
        if scale <= 0:
            # 翻转到背面，显示纯色背景
            return result

        if flip_axis == "horizontal":
            # perspective_strength=1 → 完全余弦缩放；0 → 保持原宽
            effective_scale = 1.0 - (1.0 - scale) * perspective_strength
            new_w = max(1, int(target_size[0] * effective_scale))
            scaled = img.resize((new_w, target_size[1]), Image.LANCZOS)
            x_offset = (target_size[0] - new_w) // 2
            result.paste(scaled, (x_offset, 0))
        else:
            # 垂直翻转：绕 X 轴旋转，压缩高度
            effective_scale = 1.0 - (1.0 - scale) * perspective_strength
            new_h = max(1, int(target_size[1] * effective_scale))
            scaled = img.resize((target_size[0], new_h), Image.LANCZOS)
            y_offset = (target_size[1] - new_h) // 2
            result.paste(scaled, (0, y_offset))

        return result

NODE_CLASS_MAPPINGS = {
    "PerspectiveFlipNode": PerspectiveFlipNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PerspectiveFlipNode": "📐 Perspective Flip Card"
}
