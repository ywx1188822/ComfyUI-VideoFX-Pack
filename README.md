# ComfyUI VideoFX Pack - P0 Release

🎬 **5 个核心图像转视频特效节点**

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

## 🎯 P0 节点清单

| 图标 | 节点名称 | 功能 | 类别 |
|------|----------|------|------|
| 🔄 | 360° Rotate Showcase | 旋转展示 | 视频特效 |
| 📐 | Perspective Flip Card | 透视翻转 | 视频特效 |
| 📦 | Grid Split/Merge | 宫格拆分/拼装 | 图像工具 |
| 🎚️ | Brightness & Contrast | 亮度对比度 | 图像调节 |
| 🌊 | Wave Distortion Animation | 波浪扭曲 | 视频特效 |

---

## 🚀 快速开始

### 1. 🔄 旋转展示节点

**功能**: 图像旋转动画，支持循环/单次模式

**参数**:
- `rotation_angle`: 旋转角度 (-720° 到 720°)
- `rotation_direction`: 顺时针/逆时针
- `easing`: 速度曲线 (linear/ease_in/ease_out/ease_in_out)
- `loop_mode`: 启用循环 (首尾一致)
- `total_seconds`: 视频时长
- `fps`: 帧率

**工作流示例**:
```
Load Image → 🔄 Rotate Showcase → Video Combine → Save Video
```

---

### 2. 📐 透视翻转节点

**功能**: 模拟卡片翻转效果，带透视变形

**参数**:
- `flip_axis`: 水平/垂直翻转
- `flip_angle`: 翻转角度 (0-360°)
- `perspective_strength`: 透视强度 (0-1)
- `loop_mode`: 启用循环 (翻转 360° 回原位)

**工作流示例**:
```
Load Image → 📐 Perspective Flip → Video Combine → Save Video
```

---

### 3. 📦 宫格拆分/拼装节点

**功能**: 
- **拆分模式**: 1 张宫格图 → N 张独立图片
- **拼装模式**: N 张独立图片 → 1 张宫格图

**参数**:
- `mode`: split(拆分) / merge(拼装)
- `grid_type`: 2x2(4 格) / 3x3(9 格) / 5x5(25 格) / custom(自定义)
- `gap_size`: 格子间距 (像素)
- `gap_color`: 间距颜色

**拆分顺序**: 从左到右、从上到下 (Z 字形)

**工作流示例**:
```
拆分: Load Image (4 宫格) → 📦 Grid Split/Merge (mode=split) → 4 张独立图片

拼装: [Load Image × 4] → 📦 Grid Split/Merge (mode=merge) → 1 张 4 宫格图
```

---

### 4. 🎚️ 亮度对比度节点

**功能**: 调节图像亮度、对比度、Gamma

**参数**:
- `brightness`: 亮度 (-100 到 100)
- `contrast`: 对比度 (-100 到 100)
- `gamma`: Gamma 校正 (0.1-5.0)

**工作流示例**:
```
Load Image → 🎚️ Brightness & Contrast → Save Image
```

---

### 5. 🌊 波浪扭曲节点

**功能**: 图像产生正弦波浪扭曲动画

**参数**:
- `wave_amplitude`: 波浪振幅 (0-200 像素)
- `wave_frequency`: 波浪频率 (0.1-10.0)
- `wave_direction`: 水平/垂直/对角线
- `loop_mode`: 启用循环 (整数周期)

**工作流示例**:
```
Load Image → 🌊 Wave Distortion → Video Combine → Save Video
```

---

## 🔄 循环模式说明

**视频特效节点支持两种模式**:

### 循环模式 (loop_mode=enable)
- ✅ 尾帧回归首帧状态
- ✅ 可无缝循环播放
- ✅ 适合动态背景、持续展示

### 单次模式 (loop_mode=disable)
- ✅ 特效执行到最终状态
- ✅ 首尾帧可以不同
- ✅ 适合转场过渡、开场动画

---

## 📁 目录结构

```
ComfyUI-VideoFX-Pack/
├── __init__.py                    # 主入口 (节点注册)
├── requirements.txt               # 依赖
├── README.md                      # 本文件
├── nodes/                         # 节点实现
│   ├── rotate_showcase.py        # 🔄 旋转展示
│   ├── perspective_flip.py       # 📐 透视翻转
│   ├── grid_split_merge.py       # 📦 宫格拆分/拼装
│   ├── brightness_contrast.py    # 🎚️ 亮度对比度
│   └── wave_distortion.py        # 🌊 波浪扭曲
├── utils/                         # 工具函数
│   ├── easing.py                 # 缓动函数
│   ├── transforms.py             # 几何变换
│   └── color.py                  # 色彩处理
└── workflows/                     # 示例工作流 (待添加)
```

---

## ✅ 测试清单

### 基础功能测试
- [ ] 所有节点能在 ComfyUI 中正常加载
- [ ] 无错误和警告
- [ ] 参数界面显示正确

### 节点功能测试
- [ ] 🔄 旋转展示：顺时针/逆时针旋转，循环模式首尾一致
- [ ] 📐 透视翻转：水平/垂直翻转，透视效果正常
- [ ] 📦 宫格拆分：4/9/25 宫格正确拆分
- [ ] 📦 宫格拼装：多张图片正确拼装
- [ ] 🎚️ 亮度对比度：调节效果明显
- [ ] 🌊 波浪扭曲：动画流畅，循环模式无缝

### 性能测试
- [ ] 10 秒 24fps 视频生成时间 < 30 秒
- [ ] 内存占用合理
- [ ] 无内存泄漏

---

## 🐛 已知问题

- P0 版本暂无

---

## 📝 更新日志

### v0.1.0 (2026-03-13) - P0 Release
- ✅ 实现 5 个核心节点
- ✅ 支持循环模式
- ✅ 基础工具函数库

---

## 🙏 致谢

- ComfyUI 团队
- HD Image Browser 节点提供的参考

---

## 📄 许可证

MIT License

---

**QQ**: 1188822  
**GitHub**: https://github.com/ywx1188822/ComfyUI-VideoFX-Pack
