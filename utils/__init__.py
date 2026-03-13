# ComfyUI VideoFX Pack - 工具函数库

## easing.py - 缓动函数库

```python
import math

def linear(t):
    """线性 - 匀速运动"""
    return t

def ease_in(t):
    """加速 - 开始慢，越来越快"""
    return t * t

def ease_out(t):
    """减速 - 开始快，越来越慢"""
    return t * (2 - t)

def ease_in_out(t):
    """加速 - 减速 - 对称曲线，适合循环"""
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 - 2 * t) * t

def smoothstep(t):
    """平滑步进 - 更柔和的加减速"""
    return t * t * (3 - 2 * t)

def smootherstep(t):
    """更平滑步进 - 极其柔和"""
    return t * t * t * (t * (t * 6 - 15) + 10)

def bounce_out(t):
    """弹跳效果 - 结束时有弹跳"""
    if t < 1 / 2.75:
        return 7.5625 * t * t
    elif t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375

# 导出所有缓动函数
EASING_FUNCTIONS = {
    'linear': linear,
    'ease_in': ease_in,
    'ease_out': ease_out,
    'ease_in_out': ease_in_out,
    'smoothstep': smoothstep,
    'smootherstep': smootherstep,
    'bounce_out': bounce_out,
}
```

## transforms.py - 几何变换库

```python
from PIL import Image
import numpy as np

def rotate_image(img, angle, bg_color=(0, 0, 0)):
    """
    旋转图像
    
    Args:
        img: PIL Image
        angle: 旋转角度 (度)
        bg_color: 背景填充色 (RGB 元组)
    
    Returns:
        旋转后的 PIL Image
    """
    return img.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=bg_color)

def crop_and_scale(img, left, top, right, bottom, target_size):
    """
    裁剪并缩放
    
    Args:
        img: PIL Image
        left, top, right, bottom: 裁剪区域
        target_size: 目标尺寸 (width, height)
    
    Returns:
        裁剪缩放后的 PIL Image
    """
    cropped = img.crop((left, top, right, bottom))
    return cropped.resize(target_size, Image.LANCZOS)

def create_ellipse_mask(size, radius_x, radius_y, center=None):
    """
    创建椭圆遮罩
    
    Args:
        size: 图像尺寸 (width, height)
        radius_x, radius_y: 椭圆半径
        center: 椭圆中心 (默认图像中心)
    
    Returns:
        PIL Image (L 模式遮罩)
    """
    from PIL import ImageDraw
    
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    
    if center is None:
        center = (size[0] // 2, size[1] // 2)
    
    cx, cy = center
    bbox = [
        cx - radius_x, cy - radius_y,
        cx + radius_x, cy + radius_y
    ]
    draw.ellipse(bbox, fill=255)
    
    return mask

def apply_flash_effect(img, intensity):
    """
    应用闪光效果
    
    Args:
        img: PIL Image
        intensity: 闪光强度 (0.0-1.0)
    
    Returns:
        应用闪光后的 PIL Image
    """
    if intensity <= 0:
        return img
    
    overlay = Image.new("RGB", img.size, (255, 255, 255))
    return Image.blend(img, overlay, intensity)
```

## color.py - 色彩处理库

```python
import numpy as np

def adjust_brightness(img_np, brightness):
    """
    调节亮度
    
    Args:
        img_np: NumPy 数组 (0-1 范围)
        brightness: 亮度值 (-100 到 100)
    
    Returns:
        调整后的 NumPy 数组
    """
    return np.clip(img_np + brightness / 255.0, 0, 1)

def adjust_contrast(img_np, contrast):
    """
    调节对比度
    
    Args:
        img_np: NumPy 数组 (0-1 范围)
        contrast: 对比度值 (-100 到 100)
    
    Returns:
        调整后的 NumPy 数组
    """
    factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
    return np.clip(factor * (img_np - 0.5) + 0.5, 0, 1)

def adjust_saturation(img_np, saturation):
    """
    调节饱和度
    
    Args:
        img_np: NumPy 数组 (0-1 范围)
        saturation: 饱和度值 (-100 到 100)
    
    Returns:
        调整后的 NumPy 数组
    """
    gray = np.dot(img_np[...,:3], [0.299, 0.587, 0.114])
    gray = np.stack([gray]*3, axis=-1)
    return np.clip(gray + (img_np - gray) * (1 + saturation / 100.0), 0, 1)

def hex_to_rgb(hex_color):
    """
    HEX 颜色转 RGB 元组
    
    Args:
        hex_color: HEX 颜色字符串 (如 "#FF0000")
    
    Returns:
        RGB 元组 (R, G, B)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
```
