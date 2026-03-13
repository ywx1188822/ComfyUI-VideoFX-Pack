import torch
import numpy as np
from PIL import Image
import math
import sys
import os

# 添加 utils 到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.easing import EASING_FUNCTIONS
from utils.color import hex_to_rgb

class RotateShowcaseNode:
    """🔄 360° Rotate Showcase - 旋转展示节点"""
    
    CATEGORY = "Video/Animation"
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "rotation_angle": ("FLOAT", {"default": 360.0, "min": -720.0, "max": 720.0, "step": 1.0}),
                "rotation_direction": (["clockwise", "counter-clockwise"],),
                "easing": (["linear", "ease_in", "ease_out", "ease_in_out"],),
                "background_color": ("STRING", {"default": "#000000"}),
                "total_seconds": ("INT", {"default": 10, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "enable"}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_sequence"
    
    def generate_sequence(self, image, width, height, fps, rotation_angle, 
                         rotation_direction, easing, background_color, 
                         total_seconds, loop_mode="enable"):
        # 解析输入图像
        img_tensor = image[0]
        pil_img = Image.fromarray((img_tensor.cpu().numpy() * 255).astype(np.uint8))
        
        total_frames = int(total_seconds * fps)
        output_frames = []
        
        # 解析背景色
        bg_color = hex_to_rgb(background_color)
        
        # 确定旋转方向
        direction_multiplier = 1 if rotation_direction == "clockwise" else -1
        
        # 获取缓动函数
        ease_func = EASING_FUNCTIONS.get(easing, EASING_FUNCTIONS['linear'])
        
        for i in range(total_frames):
            progress = i / total_frames
            
            if loop_mode == "enable":
                # 循环模式：使用正弦函数确保首尾一致 (0→1→0)
                loop_phase = math.sin(progress * math.pi)
                current_angle = rotation_angle * loop_phase * direction_multiplier
            else:
                # 单次模式：线性或缓动变化
                eased_progress = ease_func(progress)
                current_angle = rotation_angle * eased_progress * direction_multiplier
            
            # 应用旋转
            frame = pil_img.rotate(current_angle, resample=Image.BICUBIC, 
                                  expand=False, fillcolor=bg_color)
            frame = frame.resize((width, height), Image.LANCZOS)
            
            # 转换为张量
            frame_np = np.array(frame).astype(np.float32) / 255.0
            output_frames.append(torch.from_numpy(frame_np))
        
        return (torch.stack(output_frames),)

NODE_CLASS_MAPPINGS = {
    "RotateShowcaseNode": RotateShowcaseNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RotateShowcaseNode": "🔄 360° Rotate Showcase"
}
