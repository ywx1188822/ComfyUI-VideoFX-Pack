import torch
import numpy as np
from PIL import Image
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.color import hex_to_rgb


def _tensor_to_pil(tensor):
    """[B,H,W,C] 或 [H,W,C] tensor → PIL RGB 图像"""
    if tensor.dim() == 4:
        tensor = tensor[0]
    arr = np.ascontiguousarray(tensor.cpu().numpy())
    arr = (arr * 255).clip(0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode='RGB')


def _pil_to_tensor(pil_img):
    """PIL 图像 → [1,H,W,C] float32 tensor"""
    arr = np.ascontiguousarray(np.array(pil_img.convert('RGB')))
    return torch.from_numpy(arr.astype(np.float32) / 255.0).unsqueeze(0)


class GridSplitMergeNode:
    """📦 Grid Split/Merge - 宫格拆分/拼装节点"""

    CATEGORY = "Image/Utility"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": (["split", "merge"],),
                "grid_type": (["2x2 (4 格)", "3x3 (9 格)", "4x4 (16 格)", "5x5 (25 格)", "custom"],),
                "custom_rows": ("INT", {"default": 2, "min": 1, "max": 20}),
                "custom_cols": ("INT", {"default": 2, "min": 1, "max": 20}),
                "gap_size": ("INT", {"default": 0, "min": 0, "max": 100}),
                "gap_color": ("STRING", {"default": "#000000"}),
            },
            "optional": {
                "image": ("IMAGE",),
                "images_batch": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    OUTPUT_IS_LIST = (True,)
    INPUT_IS_LIST = True
    FUNCTION = "process_grid"

    def process_grid(self, mode, grid_type, custom_rows, custom_cols,
                     gap_size, gap_color, image=None, images_batch=None):
        # INPUT_IS_LIST=True means all inputs arrive as lists; unwrap scalars
        mode = mode[0]
        grid_type = grid_type[0]
        custom_rows = custom_rows[0]
        custom_cols = custom_cols[0]
        gap_size = gap_size[0]
        gap_color = gap_color[0]

        # Consolidate list-of-tensors into single batch tensor
        if image is not None:
            image = torch.cat(image, dim=0) if isinstance(image, list) else image
        if images_batch is not None:
            images_batch = torch.cat(images_batch, dim=0) if isinstance(images_batch, list) else images_batch
        if grid_type == "2x2 (4 格)":
            rows, cols = 2, 2
        elif grid_type == "3x3 (9 格)":
            rows, cols = 3, 3
        elif grid_type == "4x4 (16 格)":
            rows, cols = 4, 4
        elif grid_type == "5x5 (25 格)":
            rows, cols = 5, 5
        else:
            rows, cols = custom_rows, custom_cols

        if mode == "split":
            if image is None:
                raise ValueError("split mode requires 'image' input")
            return self.split_grid(image, rows, cols, gap_size)
        else:
            if images_batch is None:
                raise ValueError("merge mode requires 'images_batch' input")
            return self.merge_to_grid(images_batch, rows, cols, gap_size, gap_color)

    def split_grid(self, image, rows, cols, gap_size):
        """拆分宫格：1 张宫格图 → N 张独立图片，每张为 [1,H,W,C]"""
        pil_img = _tensor_to_pil(image[0])
        img_w, img_h = pil_img.size

        cell_w = (img_w - gap_size * (cols - 1)) // cols
        cell_h = (img_h - gap_size * (rows - 1)) // rows

        output_images = []
        for r in range(rows):
            for c in range(cols):
                left = c * (cell_w + gap_size)
                top  = r * (cell_h + gap_size)
                cell = pil_img.crop((left, top, left + cell_w, top + cell_h))
                output_images.append(_pil_to_tensor(cell))

        return (output_images,)

    def merge_to_grid(self, images_batch, rows, cols, gap_size, gap_color):
        """拼装宫格：N 张独立图片 → 1 张宫格图"""
        bg_color = hex_to_rgb(gap_color)

        # 将 batch tensor 转为 PIL 列表，正确处理 [B,H,W,C] 或 [H,W,C]
        pil_images = [_tensor_to_pil(images_batch[i]) for i in range(len(images_batch))]

        # 以第一张图的 PIL 尺寸为准（width, height），避免 tensor 维度混淆
        cell_w, cell_h = pil_images[0].size
        output_w = cell_w * cols + gap_size * (cols - 1)
        output_h = cell_h * rows + gap_size * (rows - 1)

        bg = Image.new('RGB', (output_w, output_h), bg_color)

        actual_count = min(len(pil_images), rows * cols)
        for idx in range(actual_count):
            r = idx // cols
            c = idx % cols
            x = c * (cell_w + gap_size)
            y = r * (cell_h + gap_size)
            bg.paste(pil_images[idx], (x, y))

        return ([_pil_to_tensor(bg)],)


NODE_CLASS_MAPPINGS = {
    "GridSplitMergeNode": GridSplitMergeNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GridSplitMergeNode": "📦 Grid Split/Merge"
}
