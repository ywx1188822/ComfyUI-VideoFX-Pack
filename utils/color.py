import numpy as np

def adjust_brightness(img_np, brightness):
    """调节亮度 (-100 到 100)"""
    return np.clip(img_np + brightness / 255.0, 0, 1)

def adjust_contrast(img_np, contrast):
    """调节对比度 (-100 到 100)"""
    factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
    return np.clip(factor * (img_np - 0.5) + 0.5, 0, 1)

def adjust_saturation(img_np, saturation):
    """调节饱和度 (-100 到 100)"""
    gray = np.dot(img_np[...,:3], [0.299, 0.587, 0.114])
    gray = np.stack([gray]*3, axis=-1)
    return np.clip(gray + (img_np - gray) * (1 + saturation / 100.0), 0, 1)

def hex_to_rgb(hex_color):
    """HEX 颜色转 RGB 元组"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
