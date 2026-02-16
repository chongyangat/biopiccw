# 辅助视觉设备渲染管线（Python）代码说明文档

## 1. 项目概述

本项目旨在通过 Python 图像处理流程模拟辅助视觉设备在虚拟现实（VR）场景中的渲染效果。通过将图像放大、对比度增强、边缘锐化、动态范围调整和延迟模拟等环节串联，生成接近患者实际视觉体验的图像结果，并支持后续量化评估。

---

## 2. 输入与输出

### 2.1 输入

1. **输入图像**：原始场景图像（通常为 RGB 图像），用于模拟患者在不同设备参数下的视觉体验。  
2. **辅助设备参数**：例如放大倍率、对比度增强强度、边缘锐化强度、动态范围压缩参数等。  
3. **病理视觉模型参数**：例如空间频率对比度、时间频率等，用于模拟不同视觉障碍患者特征。

### 2.2 输出

1. **渲染后图像**：经过完整渲染管线处理后的最终图像。  
2. **评估指标**：用于量化设备效果的任务指标，如完成时间、准确率、碰撞次数等。

---

## 3. 功能模块

### 3.1 图像加载与输入

使用 PIL 加载输入图像，作为后续渲染处理的起点。

```python
from PIL import Image


def load_image(image_path):
    return Image.open(image_path).convert("RGB")
```

---

### 3.2 图像放大（模拟放大设备）

根据放大倍率调整图像尺寸。

```python
def apply_magnification(image, magnification_factor):
    width, height = image.size
    new_size = (int(width * magnification_factor), int(height * magnification_factor))
    return image.resize(new_size, Image.Resampling.LANCZOS)
```

> 说明：如使用旧版 Pillow，可将 `Image.Resampling.LANCZOS` 替换为兼容写法。

---

### 3.3 对比度增强（模拟设备对比度增强功能）

通过 `PIL.ImageEnhance.Contrast` 增强图像对比度，提高视觉清晰度。

```python
from PIL import ImageEnhance


def enhance_contrast(image, contrast_factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(contrast_factor)
```

---

### 3.4 边缘锐化（模拟设备边缘增强功能）

通过 `PIL.ImageEnhance.Sharpness` 提升图像边缘细节表现。

```python
def sharpen_image(image, sharpness_factor):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(sharpness_factor)
```

---

### 3.5 动态范围调整（模拟 HDR 到 LDR 转换）

采用伽马校正（Gamma Correction）调整图像动态范围。

```python
def adjust_dynamic_range(image, gamma):
    lut = [min(255, int((x / 255) ** (1 / gamma) * 255)) for x in range(256)]
    return image.point(lut)
```

---

### 3.6 延迟模拟（模拟设备响应延迟）

通过 `time.sleep` 模拟设备响应延迟，适用于实时交互延迟影响测试。

```python
import time


def simulate_latency(image, delay_seconds):
    time.sleep(delay_seconds)
    return image
```

---

## 4. 渲染管线实现

### 4.1 核心函数

将各处理步骤串联，输出最终渲染图像。

```python
def render_pipeline(
    image_path,
    magnification_factor,
    contrast_factor,
    sharpness_factor,
    gamma,
    delay_seconds,
):
    # 1) 加载图像
    image = load_image(image_path)

    # 2) 放大
    image = apply_magnification(image, magnification_factor)

    # 3) 对比度增强
    image = enhance_contrast(image, contrast_factor)

    # 4) 边缘锐化
    image = sharpen_image(image, sharpness_factor)

    # 5) 动态范围调整
    image = adjust_dynamic_range(image, gamma)

    # 6) 延迟模拟
    image = simulate_latency(image, delay_seconds)

    return image
```

### 4.2 渲染步骤说明

1. 图像加载：读取输入图像。  
2. 图像放大：按倍率重采样。  
3. 对比度增强：提升亮暗差异。  
4. 边缘锐化：增强轮廓信息。  
5. 动态范围调整：执行伽马映射。  
6. 延迟模拟：模拟设备处理时延。

### 4.3 输出图像保存

```python
def save_image(image, output_path):
    image.save(output_path)
```

---

## 5. 示例用法

```python
from biopiccw.pipeline import render_pipeline, save_image

input_image_path = "input_scene.jpg"
output_image_path = "output_image.jpg"

magnification_factor = 2.0
contrast_factor = 1.5
sharpness_factor = 2.0
gamma = 2.2
delay_seconds = 0.5

output_image = render_pipeline(
    input_image_path,
    magnification_factor,
    contrast_factor,
    sharpness_factor,
    gamma,
    delay_seconds,
)

save_image(output_image, output_image_path)
print(f"Rendered image saved to {output_image_path}")
```

---

## 6. 命令行使用

安装依赖并运行：

```bash
pip install -e .
biopiccw-render --input input_scene.jpg --output output_image.jpg --magnification 2.0 --contrast 1.5 --sharpness 2.0 --gamma 2.2 --delay 0.0
```

---

## 常见问题排查

- 报错：`ValueError: wrong number of lut entries`  
  原因：在 Pillow 中对 RGB 图像执行 `image.point(lut)` 时，LUT 长度需为 `256 * 通道数`（RGB 即 768）。  
  处理：本项目已在 `adjust_dynamic_range` 中按通道自动扩展 LUT，请确保使用最新代码。

---

## 7. 测试

```bash
pip install -e . pytest
pytest
```

---


---

## 8. Jupyter Notebook 使用（推荐）

已提供可直接运行的 Notebook：

- `notebooks/visual_aid_pipeline.ipynb`

使用方式：

1. 在任意目录启动 Jupyter 并打开 `notebooks/visual_aid_pipeline.ipynb`。  
2. Notebook 会自动向上查找项目根目录并注入 `PROJECT_ROOT` 与 `src` 到 `sys.path`。  
3. 按顺序运行单元格，即可完成示例图像生成、渲染、保存与参数校验。

说明：Notebook 现已内置完整渲染管线函数实现（`load_image` 到 `render_pipeline`），可不依赖外部模块独立运行，便于调试和学习。

## 9. 可扩展方向（建议）

- 增加病理视觉模型接口（如视野缺损、中央暗点、对比敏感度函数衰减）。  
- 引入实时视频流处理，支持逐帧渲染与时延评估。  
- 增加客观图像质量指标（PSNR、SSIM）与任务表现指标联动分析。  
- 封装参数配置（JSON/YAML），便于实验复现实验条件。
