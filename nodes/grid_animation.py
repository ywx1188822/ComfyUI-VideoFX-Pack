import torch
import numpy as np
from PIL import Image, ImageDraw
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.transforms import tensor_to_pil, pil_to_tensor
from utils.color import hex_to_rgb


class GridAnimationNode:
    """📦 Grid Animation - 宫格动画（逐格出现/消失/随机/波浪）"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "grid_type": (["2x2", "3x3", "5x5"],),
                "animation_type": (["appear_one_by_one", "disappear_one_by_one", "random", "wave"],),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120}),
                "cell_duration": ("FLOAT", {"default": 0.3, "min": 0.05, "max": 2.0, "step": 0.05}),
                "gap_size": ("INT", {"default": 4, "min": 0, "max": 50}),
                "gap_color": ("STRING", {"default": "#000000"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_sequence"

    def generate_sequence(self, images, grid_type, animation_type, fps,
                          cell_duration, gap_size, gap_color):
        grid_map = {"2x2": 2, "3x3": 3, "5x5": 5}
        cols = grid_map[grid_type]
        rows = cols
        n_cells = rows * cols

        # Take first image
        pil_src = tensor_to_pil(images)
        sw, sh = pil_src.size

        cell_w = (sw - gap_size * (cols + 1)) // cols
        cell_h = (sh - gap_size * (rows + 1)) // rows

        # Compute order for each cell
        order = self._compute_order(rows, cols, animation_type)

        # Total frames: each cell starts revealing after order[k]*cell_duration seconds
        total_frames_per_cell = max(1, int(cell_duration * fps))
        max_order = max(order)
        total_frames = int((max_order + 1) * cell_duration * fps) + total_frames_per_cell

        gap_rgb = hex_to_rgb(gap_color)
        output_frames = []

        for f in range(total_frames):
            canvas = Image.new("RGB", (sw, sh), gap_rgb)
            for cell_idx in range(n_cells):
                r = cell_idx // cols
                c = cell_idx % cols
                start_frame = int(order[cell_idx] * cell_duration * fps)

                px = gap_size + c * (cell_w + gap_size)
                py = gap_size + r * (cell_h + gap_size)

                # Crop cell from source
                src_x = px
                src_y = py
                cell_img = pil_src.crop((src_x, src_y, src_x + cell_w, src_y + cell_h))
                if cell_img.size != (cell_w, cell_h):
                    cell_img = cell_img.resize((cell_w, cell_h), Image.LANCZOS)

                if animation_type == "appear_one_by_one":
                    if f >= start_frame:
                        fade_f = f - start_frame
                        alpha = min(1.0, fade_f / max(1, total_frames_per_cell))
                        if alpha >= 1.0:
                            canvas.paste(cell_img, (px, py))
                        else:
                            black = Image.new("RGB", (cell_w, cell_h), (0, 0, 0))
                            blended = Image.blend(black, cell_img, alpha)
                            canvas.paste(blended, (px, py))
                elif animation_type == "disappear_one_by_one":
                    if f < start_frame:
                        canvas.paste(cell_img, (px, py))
                    else:
                        fade_f = f - start_frame
                        alpha = 1.0 - min(1.0, fade_f / max(1, total_frames_per_cell))
                        if alpha > 0:
                            black = Image.new("RGB", (cell_w, cell_h), (0, 0, 0))
                            blended = Image.blend(black, cell_img, alpha)
                            canvas.paste(blended, (px, py))
                else:
                    # random / wave: same as appear
                    if f >= start_frame:
                        fade_f = f - start_frame
                        alpha = min(1.0, fade_f / max(1, total_frames_per_cell))
                        if alpha >= 1.0:
                            canvas.paste(cell_img, (px, py))
                        else:
                            black = Image.new("RGB", (cell_w, cell_h), (0, 0, 0))
                            blended = Image.blend(black, cell_img, alpha)
                            canvas.paste(blended, (px, py))

            frame_np = np.array(canvas).astype(np.float32) / 255.0
            output_frames.append(torch.from_numpy(frame_np))

        return (torch.stack(output_frames),)

    def _compute_order(self, rows, cols, animation_type):
        n = rows * cols
        if animation_type in ("appear_one_by_one", "disappear_one_by_one"):
            return list(range(n))
        elif animation_type == "random":
            import random
            order = list(range(n))
            random.shuffle(order)
            return order
        else:  # wave: diagonal order
            order = []
            for idx in range(n):
                r = idx // cols
                c = idx % cols
                order.append(r + c)
            return order


NODE_CLASS_MAPPINGS = {
    "GridAnimationNode": GridAnimationNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GridAnimationNode": "📦 Grid Animation"
}
