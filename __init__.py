"""
ComfyUI VideoFX Pack - P0 Release
==================================

5 个核心节点：
1. 🔄 360° Rotate Showcase - 旋转展示
2. 📐 Perspective Flip Card - 透视翻转
3. 📦 Grid Split/Merge - 宫格拆分/拼装
4. 🎚️ Brightness & Contrast - 亮度对比度
5. 🌊 Wave Distortion Animation - 波浪扭曲
"""

import os
import sys
import importlib.util

# 节点文件列表（相对于本文件的路径）
NODE_FILES = [
    "nodes/rotate_showcase.py",
    "nodes/perspective_flip.py",
    "nodes/grid_split_merge.py",
    "nodes/brightness_contrast.py",
    "nodes/wave_distortion.py",
]

# 节点类映射
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

current_dir = os.path.dirname(os.path.abspath(__file__))

# 预先将 utils 子模块注入 sys.modules，避免与其他插件的同名 utils 冲突
import types
_utils_pkg = types.ModuleType("utils")
_utils_pkg.__path__ = [os.path.join(current_dir, "utils")]
_utils_pkg.__package__ = "utils"
sys.modules.setdefault("utils", _utils_pkg)

for _util in ["color", "easing", "transforms"]:
    _util_path = os.path.join(current_dir, "utils", f"{_util}.py")
    _mod_key = f"utils.{_util}"
    if _mod_key not in sys.modules and os.path.exists(_util_path):
        _spec = importlib.util.spec_from_file_location(_mod_key, _util_path)
        _mod = importlib.util.module_from_spec(_spec)
        sys.modules[_mod_key] = _mod
        _spec.loader.exec_module(_mod)

# 按文件路径直接加载，避免与 ComfyUI 内置 nodes 包冲突
for rel_path in NODE_FILES:
    abs_path = os.path.join(current_dir, rel_path)
    module_name = "videofx_" + os.path.splitext(os.path.basename(rel_path))[0]
    try:
        spec = importlib.util.spec_from_file_location(module_name, abs_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "NODE_CLASS_MAPPINGS"):
            NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
        if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
            NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)

        print(f"[VideoFX Pack] Loaded: {rel_path}")
    except Exception as e:
        print(f"[VideoFX Pack] Error loading {rel_path}: {e}")

print(f"[VideoFX Pack] Total nodes loaded: {len(NODE_CLASS_MAPPINGS)}")

# Web 目录 (可选)
WEB_DIRECTORY = "./web"

# 导出
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
