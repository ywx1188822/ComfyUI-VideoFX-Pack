import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.transforms import tensor_to_pil, pil_to_tensor


class MaskRevealNode:
    """🎭 Mask Reveal Transition - 遮罩揭幕过渡"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "mask_shape": (["circle", "rectangle", "diamond"],),
                "reveal_direction": (["center_out", "left_right", "top_bottom"],),
                "feather_edge": ("INT", {"default": 10, "min": 0, "max": 30}),
                "total_seconds": ("INT", {"default": 6, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "enable"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_sequence"

    def generate_sequence(self, image, width, height, fps, mask_shape,
                          reveal_direction, feather_edge, total_seconds, loop_mode="enable"):
        pil_img = tensor_to_pil(image).resize((width, height), Image.LANCZOS)
        black_bg = Image.new("RGB", (width, height), (0, 0, 0))
        cx, cy = width // 2, height // 2
        max_radius = int(math.sqrt(cx * cx + cy * cy)) + 1

        total_frames = int(total_seconds * fps)
        output_frames = []

        for i in range(total_frames):
            progress = i / total_frames

            if loop_mode == "enable":
                t = math.sin(progress * math.pi)  # 0→1→0
            else:
                t = progress

            mask = self._build_mask(width, height, mask_shape, reveal_direction,
                                    t, max_radius, cx, cy)

            if feather_edge > 0:
                mask = mask.filter(ImageFilter.GaussianBlur(feather_edge))

            frame = Image.composite(pil_img, black_bg, mask)
            frame_np = np.array(frame).astype(np.float32) / 255.0
            output_frames.append(torch.from_numpy(frame_np))

        return (torch.stack(output_frames),)

    def _build_mask(self, w, h, shape, direction, t, max_radius, cx, cy):
        mask = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(mask)

        if direction == "center_out":
            r = int(t * max_radius)
            if shape == "circle":
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
            elif shape == "rectangle":
                rw = int(t * w / 2)
                rh = int(t * h / 2)
                draw.rectangle([cx - rw, cy - rh, cx + rw, cy + rh], fill=255)
            else:  # diamond
                pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
                draw.polygon(pts, fill=255)

        elif direction == "left_right":
            rw = int(t * w / 2)
            if shape == "circle":
                draw.ellipse([cx - rw, 0, cx + rw, h], fill=255)
            elif shape == "rectangle":
                draw.rectangle([cx - rw, 0, cx + rw, h], fill=255)
            else:
                pts = [(cx - rw, cy), (cx, 0), (cx + rw, cy), (cx, h)]
                draw.polygon(pts, fill=255)

        else:  # top_bottom
            rh = int(t * h / 2)
            if shape == "circle":
                draw.ellipse([0, cy - rh, w, cy + rh], fill=255)
            elif shape == "rectangle":
                draw.rectangle([0, cy - rh, w, cy + rh], fill=255)
            else:
                pts = [(cx, cy - rh), (w, cy), (cx, cy + rh), (0, cy)]
                draw.polygon(pts, fill=255)

        return mask


NODE_CLASS_MAPPINGS = {
    "MaskRevealNode": MaskRevealNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MaskRevealNode": "🎭 Mask Reveal Transition"
}
