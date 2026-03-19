import torch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class WindowWipeNode:
    """🪟 Window Wipe - 窗户擦除"""
    CATEGORY = "Video/Animation"
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"image": ("IMAGE",), "width": ("INT", {"default": 768}), "height": ("INT", {"default": 512}), "fps": ("INT", {"default": 24}), "total_seconds": ("INT", {"default": 3, "min": 1, "max": 10})}}
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)
    
    def execute(self, image, width, height, fps, total_seconds):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img = image.squeeze(0) if image.shape[0] == 1 else image[0]

        img_tensor = img.permute(2, 0, 1).to(device)
        total_frames = int(total_seconds * fps)
        frames = [img_tensor * (frame_idx/total_frames) for frame_idx in range(total_frames)]
        return (torch.stack(frames, dim=0).permute(0, 2, 3, 1).cpu().float(),)

NODE_CLASS_MAPPINGS = {"WindowWipe": WindowWipeNode}
NODE_DISPLAY_NAME_MAPPINGS = {"WindowWipe": "🪟 Window Wipe"}
