import torch
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DoorTransitionNode:
    """🚪 Door Open/Close - 门开/关转场"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768}),
                "height": ("INT", {"default": 512}),
                "fps": ("INT", {"default": 24}),
                "open_direction": (["horizontal", "vertical"],),
                "total_seconds": ("INT", {"default": 3, "min": 1, "max": 10}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, width, height, fps, open_direction, total_seconds):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img = image.squeeze(0) if image.shape[0] == 1 else image[0]

        img_tensor = img.permute(2, 0, 1).to(device)
        total_frames = int(total_seconds * fps)
        frames = []
        
        for frame_idx in range(total_frames):
            progress = frame_idx / total_frames
            if open_direction == "horizontal":
                mask = self.horizontal_open(img_tensor.shape, progress)
            else:
                mask = self.vertical_open(img_tensor.shape, progress)
            frames.append(img_tensor * mask)
        
        return (torch.stack(frames, dim=0).permute(0, 2, 3, 1).cpu().float(),)
    
    def horizontal_open(self, shape, progress):
        b, c, h, w = shape
        mask = torch.zeros((b, 1, h, w), device='cuda' if torch.cuda.is_available() else 'cpu')
        center = w // 2
        open_width = int(center * progress)
        mask[:, :, :, max(0, center-open_width):min(w, center+open_width)] = 1
        return mask
    
    def vertical_open(self, shape, progress):
        b, c, h, w = shape
        mask = torch.zeros((b, 1, h, w), device='cuda' if torch.cuda.is_available() else 'cpu')
        center = h // 2
        open_height = int(center * progress)
        mask[:, :, max(0, center-open_height):min(h, center+open_height), :] = 1
        return mask


NODE_CLASS_MAPPINGS = {"DoorTransition": DoorTransitionNode}
NODE_DISPLAY_NAME_MAPPINGS = {"DoorTransition": "🚪 Door Open/Close"}
