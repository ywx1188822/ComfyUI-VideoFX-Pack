import torch
import numpy as np
from PIL import Image
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.transforms import tensor_to_pil, pil_to_tensor


class CinemaOpeningNode:
    """🎬 Cinema Opening - 电影院开幕效果"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "fade_duration": ("FLOAT", {"default": 1.5, "min": 0.5, "max": 3.0, "step": 0.1}),
                "aspect_ratio": (["16:9", "21:9", "4:3"],),
                "add_letterbox": (["enable", "disable"], {"default": "enable"}),
                "total_seconds": ("INT", {"default": 6, "min": 3, "max": 60}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_sequence"

    def generate_sequence(self, image, width, height, fps, fade_duration,
                          aspect_ratio, add_letterbox, total_seconds):
        pil_img = tensor_to_pil(image).resize((width, height), Image.LANCZOS)
        black = Image.new("RGB", (width, height), (0, 0, 0))

        # Compute letterbox bar height
        if add_letterbox == "enable":
            ratio_map = {"16:9": (16, 9), "21:9": (21, 9), "4:3": (4, 3)}
            rw, rh = ratio_map[aspect_ratio]
            target_h = int(width * rh / rw)
            bar_h = max(0, (height - target_h) // 2)
        else:
            bar_h = 0

        total_frames = int(total_seconds * fps)
        fade_frames = int(fade_duration * fps)
        output_frames = []

        for i in range(total_frames):
            if i < fade_frames:
                alpha = i / max(1, fade_frames)
                frame = Image.blend(black, pil_img, alpha)
            else:
                frame = pil_img.copy()

            if bar_h > 0:
                frame_np = np.array(frame)
                frame_np[:bar_h, :] = 0
                frame_np[height - bar_h:, :] = 0
                frame = Image.fromarray(frame_np)

            frame_np = np.array(frame).astype(np.float32) / 255.0
            output_frames.append(torch.from_numpy(frame_np))

        return (torch.stack(output_frames),)


NODE_CLASS_MAPPINGS = {
    "CinemaOpeningNode": CinemaOpeningNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CinemaOpeningNode": "🎬 Cinema Opening"
}
