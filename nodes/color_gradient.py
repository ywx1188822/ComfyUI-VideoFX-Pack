import torch
import numpy as np
from PIL import Image
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.color import adjust_hue
from utils.transforms import tensor_to_pil, pil_to_tensor


class ColorGradientNode:
    """🌈 Color Gradient Transition - 色彩渐变过渡"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "transition_type": (["gray_to_color", "color_to_gray", "hue_rotate"],),
                "hue_range": ("FLOAT", {"default": 180.0, "min": 0.0, "max": 360.0, "step": 1.0}),
                "total_seconds": ("INT", {"default": 6, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "enable"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_sequence"

    def generate_sequence(self, image, width, height, fps, transition_type,
                          hue_range, total_seconds, loop_mode="enable"):
        pil_img = tensor_to_pil(image).resize((width, height), Image.LANCZOS)
        color_np = np.array(pil_img).astype(np.float32) / 255.0

        # Grayscale version
        gray_np = np.dot(color_np[..., :3], [0.299, 0.587, 0.114])
        gray_np = np.stack([gray_np] * 3, axis=-1)

        total_frames = int(total_seconds * fps)
        output_frames = []

        for i in range(total_frames):
            progress = i / total_frames

            if loop_mode == "enable":
                blend = math.sin(progress * math.pi)  # 0 → 1 → 0
            else:
                blend = progress  # 0 → 1

            if transition_type == "gray_to_color":
                frame_np = gray_np * (1.0 - blend) + color_np * blend
            elif transition_type == "color_to_gray":
                frame_np = color_np * (1.0 - blend) + gray_np * blend
            else:  # hue_rotate
                shift = blend * hue_range
                frame_np = adjust_hue(color_np, shift)

            frame_np = np.clip(frame_np, 0, 1).astype(np.float32)
            output_frames.append(torch.from_numpy(frame_np))

        return (torch.stack(output_frames),)


NODE_CLASS_MAPPINGS = {
    "ColorGradientNode": ColorGradientNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ColorGradientNode": "🌈 Color Gradient Transition"
}
