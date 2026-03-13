import torch
import numpy as np
from PIL import Image
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.transforms import tensor_to_pil, pil_to_tensor


class StarburstZoomNode:
    """💫 Starburst Zoom - 星爆缩放动画"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "zoom_start": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 1.0, "step": 0.05}),
                "zoom_end": ("FLOAT", {"default": 3.0, "min": 1.0, "max": 10.0, "step": 0.1}),
                "blur_strength": ("INT", {"default": 2, "min": 0, "max": 5}),
                "total_seconds": ("INT", {"default": 6, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "enable"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_sequence"

    def generate_sequence(self, image, width, height, fps, zoom_start, zoom_end,
                          blur_strength, total_seconds, loop_mode="enable"):
        pil_img = tensor_to_pil(image).resize((width, height), Image.LANCZOS)
        img_np = np.array(pil_img).astype(np.float32) / 255.0
        iw, ih = width, height

        total_frames = int(total_seconds * fps)
        output_frames = []

        for i in range(total_frames):
            progress = i / total_frames

            if loop_mode == "enable":
                t = math.sin(progress * math.pi)
                zoom = zoom_start + (zoom_end - zoom_start) * t
            else:
                zoom = zoom_start + (zoom_end - zoom_start) * progress

            zoom = max(zoom, 0.01)
            crop_w = int(iw / zoom)
            crop_h = int(ih / zoom)
            x0 = (iw - crop_w) // 2
            y0 = (ih - crop_h) // 2
            x1 = x0 + crop_w
            y1 = y0 + crop_h

            frame_pil = pil_img.crop((x0, y0, x1, y1)).resize((iw, ih), Image.LANCZOS)

            if blur_strength > 0:
                frame_pil = self._radial_blur(frame_pil, blur_strength)

            frame_np = np.array(frame_pil).astype(np.float32) / 255.0
            output_frames.append(torch.from_numpy(frame_np))

        return (torch.stack(output_frames),)

    def _radial_blur(self, img_pil, strength):
        """Approximate radial motion blur by blending offset copies toward center."""
        arr = np.array(img_pil).astype(np.float32)
        result = arr.copy()
        h, w = arr.shape[:2]
        steps = strength * 2
        for k in range(1, steps + 1):
            scale = 1.0 - 0.01 * k
            new_w = max(1, int(w * scale))
            new_h = max(1, int(h * scale))
            shrunk = np.array(
                img_pil.resize((new_w, new_h), Image.BILINEAR)
            ).astype(np.float32)
            padded = np.zeros_like(arr)
            px = (w - new_w) // 2
            py = (h - new_h) // 2
            padded[py:py + new_h, px:px + new_w] = shrunk
            result += padded * (1.0 / steps)
        result = result / (1.0 + 1.0)
        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))


NODE_CLASS_MAPPINGS = {
    "StarburstZoomNode": StarburstZoomNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StarburstZoomNode": "💫 Starburst Zoom"
}
