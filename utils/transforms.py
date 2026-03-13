from PIL import Image
import numpy as np

def rotate_image(img, angle, bg_color=(0, 0, 0)):
    """旋转图像"""
    return img.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=bg_color)

def crop_and_scale(img, left, top, right, bottom, target_size):
    """裁剪并缩放"""
    cropped = img.crop((left, top, right, bottom))
    return cropped.resize(target_size, Image.LANCZOS)

def create_ellipse_mask(size, radius_x, radius_y, center=None):
    """创建椭圆遮罩"""
    from PIL import ImageDraw
    
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    
    if center is None:
        center = (size[0] // 2, size[1] // 2)
    
    cx, cy = center
    bbox = [cx - radius_x, cy - radius_y, cx + radius_x, cy + radius_y]
    draw.ellipse(bbox, fill=255)
    
    return mask

def apply_flash_effect(img, intensity):
    """应用闪光效果"""
    if intensity <= 0:
        return img
    
    overlay = Image.new("RGB", img.size, (255, 255, 255))
    return Image.blend(img, overlay, intensity)
