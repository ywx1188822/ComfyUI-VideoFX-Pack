# ComfyUI VideoFX Pack

🎬 **14 个图像转视频特效节点**

---

## 📦 安装方式

### 手动安装

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/ywx1188822/ComfyUI-VideoFX-Pack
# 重启 ComfyUI
```

### ComfyUI Manager (即将发布)

在 ComfyUI Manager 中搜索 **"VideoFX Pack"** 并安装

---

## 🎯 节点清单

### P0 节点（5 个）

| 图标 | 节点名称 | 功能 | 类别 | 循环 |
|------|----------|------|------|------|
| 🔄 | 360° Rotate Showcase | 旋转展示 | Video/Animation | 往返 |
| 📐 | Perspective Flip Card | 透视翻转 | Video/Animation | 往返 |
| 📦 | Grid Split/Merge | 宫格拆分/拼装 | Image/Utility | 无动画 |
| 🎚️ | Brightness & Contrast | 亮度对比度 | Image/Adjustment | 无动画 |
| 🌊 | Wave Distortion Animation | 波浪扭曲 | Video/Animation | 完美循环 |

### P1 节点（9 个）

| 图标 | 节点名称 | 功能 | 类别 | 循环 |
|------|----------|------|------|------|
| 🔍 | Magnifying Glass Scan | 放大镜扫描 | Video/Animation | 往返 |
| 🎞️ | Film Strip Scroll | 胶片条滚动 | Video/Animation | 完美循环 |
| 💫 | Starburst Zoom | 星爆缩放 | Video/Animation | 往返 |
| 🎭 | Mask Reveal Transition | 遮罩揭幕 | Video/Animation | 往返 |
| 🎨 | Saturation & Hue | 饱和度/色调/明度 | Image/Adjustment | 无动画 |
| 🌈 | Color Gradient Transition | 色彩渐变过渡 | Video/Animation | 往返 |
| 📺 | CRT TV Power-On | 老电视开机 | Video/Animation | 单次 |
| 🎬 | Cinema Opening | 电影院开幕 | Video/Animation | 单次 |
| 📦 | Grid Animation | 宫格动画 | Video/Animation | 单次 |

---

## 🚀 节点详情

### P0 节点

#### 1. 🔄 360° Rotate Showcase

**功能**: 图像旋转动画，支持循环/单次模式

**参数**:
- `rotation_angle`: 旋转角度 (-720° 到 720°)
- `rotation_direction`: 顺时针/逆时针
- `easing`: 速度曲线 (linear/ease_in/ease_out/ease_in_out)
- `loop_mode`: 启用循环 (首尾一致)
- `total_seconds` / `fps`

---

#### 2. 📐 Perspective Flip Card

**功能**: 模拟卡片翻转效果，带透视变形

**参数**:
- `flip_axis`: 水平/垂直翻转
- `flip_angle`: 翻转角度 (0-360°)
- `perspective_strength`: 透视强度 (0-1)
- `loop_mode`: 启用循环

---

#### 3. 📦 Grid Split/Merge

**功能**:
- **拆分模式**: 1 张宫格图 → N 张独立图片
- **拼装模式**: N 张独立图片 → 1 张宫格图

**参数**:
- `mode`: split / merge
- `grid_type`: 2x2 / 3x3 / 5x5 / custom
- `gap_size`: 格子间距 (像素)
- `gap_color`: 间距颜色

---

#### 4. 🎚️ Brightness & Contrast

**功能**: 调节图像亮度、对比度、Gamma

**参数**:
- `brightness`: 亮度 (-100 到 100)
- `contrast`: 对比度 (-100 到 100)
- `gamma`: Gamma 校正 (0.1-5.0)

---

#### 5. 🌊 Wave Distortion Animation

**功能**: 图像产生正弦波浪扭曲动画

**参数**:
- `wave_amplitude`: 波浪振幅 (0-200 像素)
- `wave_frequency`: 波浪频率 (0.1-10.0)
- `wave_direction`: horizontal / vertical / diagonal
- `loop_mode`: 启用循环 (整数周期)

---

### P1 节点

#### 6. 🔍 Magnifying Glass Scan

**功能**: 放大镜在图像上扫描，局部放大显示细节

**参数**:
- `magnify_factor`: 放大倍数 (2-10)
- `lens_size`: 镜头大小 (50-500 px)
- `scan_direction`: horizontal / vertical / zigzag
- `lens_shape`: circle / rectangle
- `loop_mode`: 启用往返循环

---

#### 7. 🎞️ Film Strip Scroll

**功能**: 图像以胶片条形式无缝滚动，带老胶片边框和齿孔

**参数**:
- `scroll_direction`: left / right / up / down
- `film_border`: 启用/禁用胶片边框
- `frame_gap`: 帧间距 (0-50 px)
- `total_seconds` / `fps`

---

#### 8. 💫 Starburst Zoom

**功能**: 以图像中心为基点的星爆式缩放，带径向模糊

**参数**:
- `zoom_start`: 起始缩放 (0.1-1.0)
- `zoom_end`: 结束缩放 (1.0-10.0)
- `blur_strength`: 径向模糊强度 (0-5)
- `loop_mode`: 启用往返循环

---

#### 9. 🎭 Mask Reveal Transition

**功能**: 用遮罩形状从无到有揭幕图像，支持边缘羽化

**参数**:
- `mask_shape`: circle / rectangle / diamond
- `reveal_direction`: center_out / left_right / top_bottom
- `feather_edge`: 羽化边缘 (0-30 px)
- `loop_mode`: 启用往返循环

---

#### 10. 🎨 Saturation & Hue

**功能**: 静态调节图像饱和度、色调、明度（支持批次处理）

**参数**:
- `saturation`: 饱和度 (-100 到 100)
- `hue_shift`: 色调偏移 (0-360°)
- `lightness`: 明度 (-100 到 100)

---

#### 11. 🌈 Color Gradient Transition

**功能**: 灰度↔彩色渐变，或色调旋转动画

**参数**:
- `transition_type`: gray_to_color / color_to_gray / hue_rotate
- `hue_range`: 色调旋转范围 (0-360°，hue_rotate 模式)
- `loop_mode`: 启用往返循环

---

#### 12. 📺 CRT TV Power-On

**功能**: 模拟老式 CRT 电视开机效果（4 阶段动画）

**阶段**: 噪点 → 中央白线展开 → 图像垂直展开 → 稳定画面+扫描线

**参数**:
- `scanline_intensity`: 扫描线强度 (0-1)
- `power_on_duration`: 开机动画时长 (1-5s)
- `add_static`: 启用/禁用噪点

---

#### 13. 🎬 Cinema Opening

**功能**: 电影院风格开幕，淡入 + letterbox 黑边

**参数**:
- `fade_duration`: 淡入时长 (0.5-3.0s)
- `aspect_ratio`: 16:9 / 21:9 / 4:3
- `add_letterbox`: 启用/禁用黑边

---

#### 14. 📦 Grid Animation

**功能**: 图像按宫格逐格出现/消失，支持多种动画顺序

**参数**:
- `grid_type`: 2x2 / 3x3 / 5x5
- `animation_type`: appear_one_by_one / disappear_one_by_one / random / wave
- `cell_duration`: 每格动画时长 (秒)
- `gap_size` / `gap_color`

---

## 🔄 循环模式说明

| 模式 | 行为 | 适用场景 |
|------|------|---------|
| `loop_mode=enable` | 尾帧回归首帧，可无缝循环 | 动态背景、持续展示 |
| `loop_mode=disable` | 线性从起点到终点 | 转场过渡 |
| 单次 (one-shot) | 不支持循环，天然是开场动画 | CRT、Cinema、Grid Animation |

---

## 📁 目录结构

```
ComfyUI-VideoFX-Pack/
├── __init__.py
├── nodes/
│   ├── rotate_showcase.py        # 🔄
│   ├── perspective_flip.py       # 📐
│   ├── grid_split_merge.py       # 📦
│   ├── brightness_contrast.py    # 🎚️
│   ├── wave_distortion.py        # 🌊
│   ├── magnifying_glass.py       # 🔍 P1
│   ├── film_strip.py             # 🎞️ P1
│   ├── starburst_zoom.py         # 💫 P1
│   ├── mask_reveal.py            # 🎭 P1
│   ├── saturation_hue.py         # 🎨 P1
│   ├── color_gradient.py         # 🌈 P1
│   ├── crt_tv.py                 # 📺 P1
│   ├── cinema_opening.py         # 🎬 P1
│   └── grid_animation.py         # 📦 P1
├── utils/
│   ├── easing.py                 # 缓动函数
│   ├── transforms.py             # 几何变换 + tensor↔PIL 工具
│   └── color.py                  # 色彩处理 (HSV/亮度/饱和度)
└── workflows/                    # 示例工作流
```

---

## 📝 更新日志

### v0.2.0 (2026-03-14) - P1 Release
- ✅ 新增 9 个节点（共 14 个）
- ✅ utils 新增 `tensor_to_pil`、`pil_to_tensor`、`adjust_hue`、`adjust_lightness`

### v0.1.0 (2026-03-13) - P0 Release
- ✅ 实现 5 个核心节点
- ✅ 支持循环模式
- ✅ 基础工具函数库

---

## 🙏 致谢

- ComfyUI 团队

---

## 📄 许可证

MIT License

---

**QQ**: 1188822
**GitHub**: https://github.com/ywx1188822/ComfyUI-VideoFX-Pack
