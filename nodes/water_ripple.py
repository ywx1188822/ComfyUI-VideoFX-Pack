import torch
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class WaterRippleNode:
    """🌊 Water Ripple - 水波涟漪效果"""

    CATEGORY = "Video/Animation"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 768}),
                "height": ("INT", {"default": 512}),
                "fps": ("INT", {"default": 24}),
                "ripple_amplitude": ("FLOAT", {"default": 5.0, "min": 1, "max": 20}),
                "ripple_frequency": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 5.0}),
                "total_seconds": ("INT", {"default": 6, "min": 2, "max": 60}),
                "loop_mode": (["enable", "disable"], {"default": "enable"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    OUTPUT_IS_LIST = (False,)

    def execute(self, image, width, height, fps, ripple_amplitude, ripple_frequency, total_seconds, loop_mode):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        img = image.squeeze(0) if image.shape[0] == 1 else image[0]

        img_tensor = img.permute(2, 0, 1).to(device)
        total_frames = int(total_seconds * fps)
        frames = []
        
        for frame_idx in range(total_frames):
            progress = frame_idx / total_frames
            phase = math.sin(progress * math.pi) if loop_mode == "enable" else progress
            frames.append(self.ripple(img_tensor, phase, ripple_amplitude, ripple_frequency))
        
        return (torch.stack(frames, dim=0).permute(0, 2, 3, 1).cpu().float(),)
    
    def ripple(self, img, phase, amp, freq):
        b, c, h, w = img.shape
        y, x = torch.meshgrid(torch.arange(h), torch.arange(w), indexing='ij')
        dx = amp * torch.sin(x.float() * freq * 0.1 + phase * 10)
        new_x = torch.clamp(x + dx, 0, w-1) / (w-1) * 2 - 1
        grid = torch.stack([new_x, torch.ones_like(new_x)], dim=-1).unsqueeze(0).expand(b, -1, -1, -1)
        return torch.nn.functional.grid_sample(img, grid, align_corners=False, padding_mode='border')


NODE_CLASS_MAPPINGS = {"WaterRipple": WaterRippleNode}
NODE_DISPLAY_NAME_MAPPINGS = {"WaterRipple": "🌊 Water Ripple"}
