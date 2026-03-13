import numpy as np
from PIL import Image


def adjust_hue(img_np, hue_shift_deg):
    """Shift hue by hue_shift_deg (0-360). img_np is float32 RGB [0,1]."""
    img_uint8 = (np.clip(img_np, 0, 1) * 255).astype(np.uint8)
    pil_img = Image.fromarray(img_uint8, mode="RGB").convert("HSV")
    hsv = np.array(pil_img).astype(np.int32)
    hsv[..., 0] = (hsv[..., 0] + int(hue_shift_deg / 360.0 * 255)) % 256
    return np.array(Image.fromarray(hsv.astype(np.uint8), mode="HSV").convert("RGB")).astype(np.float32) / 255.0


def adjust_lightness(img_np, lightness):
    """Adjust lightness by -100~100 (additive on V channel). img_np is float32 RGB [0,1]."""
    img_uint8 = (np.clip(img_np, 0, 1) * 255).astype(np.uint8)
    pil_img = Image.fromarray(img_uint8, mode="RGB").convert("HSV")
    hsv = np.array(pil_img).astype(np.int32)
    hsv[..., 2] = np.clip(hsv[..., 2] + int(lightness / 100.0 * 255), 0, 255)
    return np.array(Image.fromarray(hsv.astype(np.uint8), mode="HSV").convert("RGB")).astype(np.float32) / 255.0


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
