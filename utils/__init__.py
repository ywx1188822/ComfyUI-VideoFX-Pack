"""
ComfyUI VideoFX Pack - 工具函数库
=================================

包含以下模块:
- easing: 7 种缓动函数
- transforms: 几何变换函数
- color: 色彩处理函数
"""

from .easing import (
    linear,
    ease_in,
    ease_out,
    ease_in_out,
    smoothstep,
    smootherstep,
    bounce_out,
)

from .transforms import (
    tensor_to_pil,
    pil_to_tensor,
)

from .color import (
    hex_to_rgb,
)

__all__ = [
    # Easing
    'linear',
    'ease_in',
    'ease_out',
    'ease_in_out',
    'smoothstep',
    'smootherstep',
    'bounce_out',
    # Transforms
    'tensor_to_pil',
    'pil_to_tensor',
    # Color
    'hex_to_rgb',
]
