import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.transforms import tensor_to_pil, pil_to_tensor


class MagnifyingGlassNode:
    """🔍 Magnifying Glass Scan - 放大镜扫描动画"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "magnify_factor": ("FLOAT", {"default": 3.0, "min": 2.0, "max": 10.0, "step": 0.5}),
                "lens_size": ("INT", {"default": 200, "min": 50, "max": 500}),
                "scan_direction": (["horizontal", "vertical", "zigzag"],),
                "lens_shape": (["circle", "rectangle"],),
                "total_seconds": ("INT", {"default": 6, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "enable"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_sequence"

    def generate_sequence(self, image, width, height, fps, magnify_factor, lens_size,
                          scan_direction, lens_shape, total_seconds, loop_mode="enable"):
        pil_img = tensor_to_pil(image).resize((width, height), Image.LANCZOS)
        iw, ih = width, height
        half_lens = lens_size // 2

        total_frames = int(total_seconds * fps)
        output_frames = []

        for i in range(total_frames):
            progress = i / total_frames

            if loop_mode == "enable":
                t = math.sin(progress * math.pi)
            else:
                t = progress

            # Compute lens center
            if scan_direction == "horizontal":
                cx = int(half_lens + t * (iw - lens_size))
                cy = ih // 2
            elif scan_direction == "vertical":
                cx = iw // 2
                cy = int(half_lens + t * (ih - lens_size))
            else:  # zigzag
                row_count = 3
                seg = 1.0 / row_count
                row = int(t / seg)
                row_t = (t - row * seg) / seg
                if row % 2 == 0:
                    cx = int(half_lens + row_t * (iw - lens_size))
                else:
                    cx = int((iw - half_lens) - row_t * (iw - lens_size))
                cy = int(half_lens + (row / max(row_count - 1, 1)) * (ih - lens_size))

            cx = max(half_lens, min(iw - half_lens, cx))
            cy = max(half_lens, min(ih - half_lens, cy))

            frame = pil_img.copy()

            # Source crop (smaller area that gets magnified)
            src_w = int(lens_size / magnify_factor)
            src_h = int(lens_size / magnify_factor)
            sx0 = max(0, cx - src_w // 2)
            sy0 = max(0, cy - src_h // 2)
            sx1 = min(iw, sx0 + src_w)
            sy1 = min(ih, sy0 + src_h)

            magnified = pil_img.crop((sx0, sy0, sx1, sy1)).resize((lens_size, lens_size), Image.LANCZOS)

            # Create shape mask
            mask = Image.new("L", (lens_size, lens_size), 0)
            draw = ImageDraw.Draw(mask)
            if lens_shape == "circle":
                draw.ellipse([0, 0, lens_size - 1, lens_size - 1], fill=255)
            else:
                draw.rectangle([0, 0, lens_size - 1, lens_size - 1], fill=255)

            # Paste onto frame
            paste_x = cx - half_lens
            paste_y = cy - half_lens
            frame.paste(magnified, (paste_x, paste_y), mask)

            # Lens border ring
            border_draw = ImageDraw.Draw(frame)
            border_draw.ellipse(
                [paste_x, paste_y, paste_x + lens_size - 1, paste_y + lens_size - 1],
                outline=(200, 200, 200), width=2
            )

            frame_np = np.array(frame).astype(np.float32) / 255.0
            output_frames.append(torch.from_numpy(frame_np))

        return (torch.stack(output_frames),)


NODE_CLASS_MAPPINGS = {
    "MagnifyingGlassNode": MagnifyingGlassNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MagnifyingGlassNode": "🔍 Magnifying Glass Scan"
}
