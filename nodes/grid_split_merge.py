import torch
import numpy as np
from PIL import Image
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.color import hex_to_rgb

class GridSplitMergeNode:
    """📦 Grid Split/Merge - 宫格拆分/拼装节点"""
    
    CATEGORY = "Image/Utility"
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": (["split", "merge"],),
                "grid_type": (["2x2 (4 格)", "3x3 (9 格)", "5x5 (25 格)", "custom"],),
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
    FUNCTION = "process_grid"
    
    def process_grid(self, mode, grid_type, custom_rows, custom_cols, 
                     gap_size, gap_color, image=None, images_batch=None):
        # 解析宫格行列数
        if grid_type == "2x2 (4 格)":
            rows, cols = 2, 2
        elif grid_type == "3x3 (9 格)":
            rows, cols = 3, 3
        elif grid_type == "5x5 (25 格)":
            rows, cols = 5, 5
        else:
            rows, cols = custom_rows, custom_cols
        
        if mode == "split":
            if image is None:
                raise ValueError("split mode requires 'image' input")
            return self.split_grid(image, rows, cols, gap_size, gap_color)
        else:
            if images_batch is None:
                raise ValueError("merge mode requires 'images_batch' input")
            return self.merge_to_grid(images_batch, rows, cols, gap_size, gap_color)
    
    def split_grid(self, image, rows, cols, gap_size, gap_color):
        """拆分宫格：1 张宫格图 → N 张独立图片"""
        img_tensor = image[0]
        pil_img = Image.fromarray((img_tensor.cpu().numpy() * 255).astype(np.uint8))
        
        img_w, img_h = pil_img.size
        
        # 等比例计算每个格子的尺寸
        cell_w = (img_w - gap_size * (cols - 1)) // cols
        cell_h = (img_h - gap_size * (rows - 1)) // rows
        
        output_images = []
        
        # 按行优先顺序拆分 (从左到右、从上到下)
        for r in range(rows):
            for c in range(cols):
                left = c * (cell_w + gap_size)
                top = r * (cell_h + gap_size)
                right = left + cell_w
                bottom = top + cell_h
                
                cell = pil_img.crop((left, top, right, bottom))
                cell_np = np.array(cell).astype(np.float32) / 255.0
                output_images.append(torch.from_numpy(cell_np))
        
        return (output_images,)
    
    def merge_to_grid(self, images_batch, rows, cols, gap_size, gap_color):
        """拼装宫格：N 张独立图片 → 1 张宫格图"""
        if images_batch is None or len(images_batch) == 0:
            raise ValueError("images_batch cannot be empty")
        
        bg_color = hex_to_rgb(gap_color)
        
        # 获取第一张图的尺寸
        first_img_tensor = images_batch[0]
        h, w = first_img_tensor.shape[0], first_img_tensor.shape[1]
        
        # 计算输出宫格的总尺寸
        output_w = w * cols + gap_size * (cols - 1)
        output_h = h * rows + gap_size * (rows - 1)
        
        # 创建背景画布
        bg = Image.new('RGB', (output_w, output_h), bg_color)
        
        # 按顺序粘贴每张图
        expected_count = rows * cols
        actual_count = min(len(images_batch), expected_count)
        
        for idx in range(actual_count):
            r = idx // cols
            c = idx % cols
            
            img_tensor = images_batch[idx]
            pil_img = Image.fromarray((img_tensor.cpu().numpy() * 255).astype(np.uint8))
            
            x = c * (w + gap_size)
            y = r * (h + gap_size)
            
            bg.paste(pil_img, (x, y))
        
        bg_np = np.array(bg).astype(np.float32) / 255.0
        return ([torch.from_numpy(bg_np)],)

NODE_CLASS_MAPPINGS = {
    "GridSplitMergeNode": GridSplitMergeNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GridSplitMergeNode": "📦 Grid Split/Merge"
}
