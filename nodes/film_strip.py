import torch
import numpy as np
from PIL import Image, ImageDraw
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.transforms import tensor_to_pil, pil_to_tensor


class FilmStripScrollNode:
    """🎞️ Film Strip Scroll - 胶片条滚动动画"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "scroll_direction": (["left", "right", "up", "down"],),
                "film_border": (["enable", "disable"], {"default": "enable"}),
                "frame_gap": ("INT", {"default": 10, "min": 0, "max": 50}),
                "total_seconds": ("INT", {"default": 6, "min": 2, "max": 60}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_sequence"

    def generate_sequence(self, image, width, height, fps, scroll_direction,
                          film_border, frame_gap, total_seconds):
        pil_img = tensor_to_pil(image).resize((width, height), Image.LANCZOS)

        # Slight yellow tint for old film look
        pil_arr = np.array(pil_img).astype(np.float32)
        pil_arr[..., 0] = np.clip(pil_arr[..., 0] * 1.05, 0, 255)
        pil_arr[..., 1] = np.clip(pil_arr[..., 1] * 1.02, 0, 255)
        pil_arr[..., 2] = np.clip(pil_arr[..., 2] * 0.90, 0, 255)
        pil_img = Image.fromarray(pil_arr.astype(np.uint8))

        total_frames = int(total_seconds * fps)
        output_frames = []

        is_horizontal = scroll_direction in ("left", "right")

        for i in range(total_frames):
            progress = i / total_frames

            if is_horizontal:
                offset = int(progress * width) % width
                # Tile 3 copies horizontally
                canvas = Image.new("RGB", (width * 3, height))
                for k in range(3):
                    canvas.paste(pil_img, (k * width + frame_gap, 0))
                if scroll_direction == "left":
                    x0 = width - offset
                else:
                    x0 = offset
                frame = canvas.crop((x0, 0, x0 + width, height))
            else:
                offset = int(progress * height) % height
                canvas = Image.new("RGB", (width, height * 3))
                for k in range(3):
                    canvas.paste(pil_img, (0, k * height + frame_gap))
                if scroll_direction == "up":
                    y0 = height - offset
                else:
                    y0 = offset
                frame = canvas.crop((0, y0, width, y0 + height))

            if film_border == "enable":
                frame = self._add_film_border(frame, width, height, is_horizontal)

            frame_np = np.array(frame).astype(np.float32) / 255.0
            output_frames.append(torch.from_numpy(frame_np))

        return (torch.stack(output_frames),)

    def _add_film_border(self, frame, w, h, is_horizontal):
        draw = ImageDraw.Draw(frame)
        border = 18
        hole_r = 6
        if is_horizontal:
            # Top and bottom black strips
            draw.rectangle([0, 0, w, border], fill=(10, 10, 10))
            draw.rectangle([0, h - border, w, h], fill=(10, 10, 10))
            # Sprocket holes
            spacing = 30
            for x in range(15, w, spacing):
                draw.ellipse([x - hole_r, 3, x + hole_r, border - 3], fill=(50, 50, 50))
                draw.ellipse([x - hole_r, h - border + 3, x + hole_r, h - 3], fill=(50, 50, 50))
        else:
            draw.rectangle([0, 0, border, h], fill=(10, 10, 10))
            draw.rectangle([w - border, 0, w, h], fill=(10, 10, 10))
            spacing = 30
            for y in range(15, h, spacing):
                draw.ellipse([3, y - hole_r, border - 3, y + hole_r], fill=(50, 50, 50))
                draw.ellipse([w - border + 3, y - hole_r, w - 3, y + hole_r], fill=(50, 50, 50))
        return frame


NODE_CLASS_MAPPINGS = {
    "FilmStripScrollNode": FilmStripScrollNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FilmStripScrollNode": "🎞️ Film Strip Scroll"
}
