import torch
import numpy as np
from PIL import Image
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.transforms import tensor_to_pil, pil_to_tensor


class CRTTVNode:
    """📺 CRT TV Power-On - 老电视开机效果"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "scanline_intensity": ("FLOAT", {"default": 0.4, "min": 0.0, "max": 1.0, "step": 0.05}),
                "power_on_duration": ("FLOAT", {"default": 2.0, "min": 1.0, "max": 5.0, "step": 0.5}),
                "add_static": (["enable", "disable"], {"default": "enable"}),
                "total_seconds": ("INT", {"default": 6, "min": 3, "max": 60}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_sequence"

    def generate_sequence(self, image, width, height, fps, scanline_intensity,
                          power_on_duration, add_static, total_seconds):
        pil_img = tensor_to_pil(image).resize((width, height), Image.LANCZOS)
        img_np = np.array(pil_img).astype(np.float32) / 255.0

        total_frames = int(total_seconds * fps)
        pod = power_on_duration  # seconds

        # Phase breakpoints (as fraction of total_seconds)
        p1 = pod * 0.15 / total_seconds   # noise
        p2 = pod * 0.40 / total_seconds   # white line expand
        p3 = pod * 0.85 / total_seconds   # image unfold
        p4 = 1.0                           # stable + scanlines

        output_frames = []
        rng = np.random.default_rng(42)

        for i in range(total_frames):
            t = i / total_frames

            if t < p1:
                # Pure black + noise
                frame_np = np.zeros((height, width, 3), dtype=np.float32)
                if add_static == "enable":
                    noise = rng.random((height, width, 3)).astype(np.float32) * 0.3
                    frame_np = noise

            elif t < p2:
                # White horizontal line growing from center
                local = (t - p1) / (p2 - p1)
                line_h = max(1, int(local * height * 0.1))
                frame_np = np.zeros((height, width, 3), dtype=np.float32)
                cy = height // 2
                y0 = max(0, cy - line_h // 2)
                y1 = min(height, cy + line_h // 2 + 1)
                frame_np[y0:y1, :] = 1.0
                if add_static == "enable":
                    noise = rng.random((height, width, 3)).astype(np.float32) * 0.05
                    frame_np = np.clip(frame_np + noise, 0, 1)

            elif t < p3:
                # Image unfolds vertically from center
                local = (t - p2) / (p3 - p2)
                visible_h = max(1, int(local * height))
                cy = height // 2
                y0 = max(0, cy - visible_h // 2)
                y1 = min(height, cy + visible_h // 2 + 1)
                frame_np = np.zeros((height, width, 3), dtype=np.float32)

                # Scale source region to visible strip
                strip_src = img_np[y0:y1, :, :]
                if strip_src.shape[0] > 0:
                    strip_pil = Image.fromarray((strip_src * 255).astype(np.uint8))
                    strip_pil = strip_pil.resize((width, y1 - y0), Image.LANCZOS)
                    frame_np[y0:y1, :] = np.array(strip_pil).astype(np.float32) / 255.0

            else:
                # Stable image with scanlines
                local = (t - p3) / (p4 - p3)
                frame_np = img_np.copy()

                # Gradually increase scanline intensity
                sl = scanline_intensity * min(1.0, local * 3)
                if sl > 0:
                    darken = 1.0 - sl * 0.5
                    frame_np[::2, :, :] *= darken  # even rows

            output_frames.append(torch.from_numpy(frame_np.astype(np.float32)))

        return (torch.stack(output_frames),)


NODE_CLASS_MAPPINGS = {
    "CRTTVNode": CRTTVNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CRTTVNode": "📺 CRT TV Power-On"
}
