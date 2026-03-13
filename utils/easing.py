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

EASING_FUNCTIONS = {
    'linear': linear,
    'ease_in': ease_in,
    'ease_out': ease_out,
    'ease_in_out': ease_in_out,
    'smoothstep': smoothstep,
    'smootherstep': smootherstep,
    'bounce_out': bounce_out,
}
