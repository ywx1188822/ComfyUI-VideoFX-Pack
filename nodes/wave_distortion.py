import torch
import numpy as np
from PIL import Image
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.easing import EASING_FUNCTIONS
from utils.color import hex_to_rgb

class WaveDistortionNode:
    """🌊 Wave Distortion Animation - 波浪扭曲节点"""
    
    CATEGORY = "Video/Animation"
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "wave_amplitude": ("FLOAT", {"default": 50.0, "min": 0.0, "max": 200.0, "step": 1.0}),
                "wave_frequency": ("FLOAT", {"default": 2.0, "min": 0.1, "max": 10.0, "step": 0.1}),
                "wave_direction": (["horizontal", "vertical", "diagonal"],),
                "total_seconds": ("INT", {"default": 10, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "enable"}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_sequence"
    
    def generate_sequence(self, image, width, height, fps, wave_amplitude,
                         wave_frequency, wave_direction, total_seconds, loop_mode="enable"):
        img_tensor = image[0]
        pil_img = Image.fromarray((img_tensor.cpu().numpy() * 255).astype(np.uint8))
        
        total_frames = int(total_seconds * fps)
        output_frames = []
        
        img_w, img_h = pil_img.size
        
        for i in range(total_frames):
            progress = i / total_frames
            
            if loop_mode == "enable":
                # 循环模式：完成整数个波浪周期
                wave_phase = progress * int(wave_frequency) * 2 * math.pi
            else:
                # 单次模式：线性进展
                wave_phase = progress * wave_frequency * 2 * math.pi
            
            # 应用波浪扭曲
            frame = self.apply_wave_distortion(
                pil_img, wave_amplitude, wave_frequency, 
                wave_direction, wave_phase, (width, height)
            )
            
            frame_np = np.array(frame).astype(np.float32) / 255.0
            output_frames.append(torch.from_numpy(frame_np))
        
        return (torch.stack(output_frames),)
    
    def apply_wave_distortion(self, img, amplitude, frequency, direction,
                             phase, target_size):
        """应用波浪扭曲效果（numpy 向量化）"""
        img_array = np.array(img)
        h, w = img_array.shape[:2]

        # 创建坐标网格
        y_coords, x_coords = np.mgrid[0:h, 0:w]

        if direction == "horizontal":
            # 水平波浪：x 方向偏移，由 y 坐标驱动
            offset = (amplitude * np.sin(2 * np.pi * y_coords / h * frequency + phase)).astype(int)
            src_x = np.clip(x_coords + offset, 0, w - 1)
            src_y = y_coords
        elif direction == "vertical":
            # 垂直波浪：y 方向偏移，由 x 坐标驱动
            offset = (amplitude * np.sin(2 * np.pi * x_coords / w * frequency + phase)).astype(int)
            src_x = x_coords
            src_y = np.clip(y_coords + offset, 0, h - 1)
        else:  # diagonal
            # 对角线波浪：xy 双向偏移
            offset_x = (amplitude * np.sin(2 * np.pi * y_coords / h * frequency + phase)).astype(int)
            offset_y = (amplitude * np.cos(2 * np.pi * x_coords / w * frequency + phase)).astype(int)
            src_x = np.clip(x_coords + offset_x, 0, w - 1)
            src_y = np.clip(y_coords + offset_y, 0, h - 1)

        # 一次性完成像素映射
        output = img_array[src_y, src_x]

        result = Image.fromarray(output)
        result = result.resize(target_size, Image.LANCZOS)
        return result

NODE_CLASS_MAPPINGS = {
    "WaveDistortionNode": WaveDistortionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WaveDistortionNode": "🌊 Wave Distortion Animation"
}
