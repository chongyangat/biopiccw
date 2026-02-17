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

使用 `skimage.io.imread` 加载输入图像，作为渲染处理起点，并归一化到 `[0,1]`。

```python
from skimage import io
import numpy as np


def load_image(image_path):
    image = io.imread(image_path)
    return image.astype(np.float32) / 255.0
```

---

### 3.2 图像放大（模拟放大设备）

根据放大倍率调整图像尺寸。

```python
def apply_magnification(image, magnification_factor):
    height, width = image.shape[:2]
    new_size = (int(width * magnification_factor), int(height * magnification_factor))
    return transform.resize(image, (new_size[1], new_size[0], image.shape[2]), preserve_range=True)
```

> 说明：统一在 `[0,1]` 浮点域处理，避免跨库数值范围不一致。

---

### 3.3 对比度增强（模拟设备对比度增强功能）

统一在 `skimage` 的归一化浮点域（[0,1]）进行对比度增强，避免跨库数值范围不一致。

```python
import numpy as np


def enhance_contrast(image, contrast_factor):
    enhanced = (image - 0.5) * contrast_factor + 0.5
    return (enhanced - enhanced.min()) / (enhanced.max() - enhanced.min())
```

---

### 3.4 边缘锐化（模拟设备边缘增强功能）

通过 `scikit-image` 的 `unsharp_mask` 提升图像边缘细节表现。

```python
from skimage import filters


def sharpen_image(image, sharpness_factor):
    return filters.unsharp_mask(image, radius=1.0, amount=sharpness_factor, preserve_range=True, channel_axis=-1)
```

---

### 3.5 动态范围调整（模拟 HDR 到 LDR 转换）

采用伽马校正（Gamma Correction）调整图像动态范围（输入建议为 [0,1] 浮点）。

```python
from skimage import exposure


def adjust_dynamic_range(image, gamma):
    return exposure.adjust_gamma(image, gamma=gamma)
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
    image_u8 = (np.clip(image, 0.0, 1.0) * 255).astype("uint8")
    io.imsave(output_path, image_u8)
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

- 报错：`ModuleNotFoundError: No module named skimage`  
  原因：当前 Python 环境未安装 scikit-image。  
  处理：安装依赖后重试，例如 `pip install scikit-image numpy`。

---

## 跨库处理与归一化约定

归一化采用最小-最大归一化（Min-Max）：

```python
normalized_arr = (arr - arr.min()) / (arr.max() - arr.min())
```

当 `arr.max() == arr.min()` 时，代码中会回退为全零数组，避免除零错误。

为避免你提到的“不同库处理时数值范围不一致”问题，项目采用以下统一规则：

- **读入阶段（skimage）**：`skimage.io.imread` 读取后立即归一化到 `float32` 的 `[0,1]`。
- **处理阶段（skimage）**：放大、对比度增强、锐化、Gamma 调整都在 `[0,1]` 浮点域完成。
- **写出阶段（skimage）**：保存前把 `[0,1]` 转回 `uint8`，再 `skimage.io.imsave`。

这样可确保在切换不同库时不会出现“某一步按 0-255、某一步按 0-1”导致的结果偏差。

---

## 7. 环境配置（Conda，推荐）

为避免本地同名文件影响第三方库导入，建议使用全新 Conda 环境运行：

```bash
conda create -n visual_sim python=3.10 -y
conda activate visual_sim
conda install -c conda-forge scikit-image numpy pytest -y
pip install -e .
```

验证导入：

```bash
python -c "import skimage, numpy; print(skimage.__version__)"
```

---

## 8. 测试

```bash
pip install -e . pytest
pytest
```

---


---

## 9. Jupyter Notebook 使用（推荐）

已提供可直接运行的 Notebook：

- `notebooks/visual_aid_pipeline.ipynb`

使用方式：

1. 在任意目录启动 Jupyter 并打开 `notebooks/visual_aid_pipeline.ipynb`。  
2. Notebook 会自动向上查找项目根目录并注入 `PROJECT_ROOT` 与 `src` 到 `sys.path`。  
3. 按顺序运行单元格，即可完成示例图像生成、渲染、保存与参数校验。

说明：Notebook 与主代码均采用“skimage-first + 归一化 [0,1]”策略；读取、处理与保存均统一使用 scikit-image。
说明：Notebook 默认直接读取你提供的图片路径 `D:\\vrcontent\\biopiccw\\test.jpg`，并在运行前用 `skimage.io` 做读取检查。

## 10. 可扩展方向（建议）

- 增加病理视觉模型接口（如视野缺损、中央暗点、对比敏感度函数衰减）。  
- 引入实时视频流处理，支持逐帧渲染与时延评估。  
- 增加客观图像质量指标（PSNR、SSIM）与任务表现指标联动分析。  
- 封装参数配置（JSON/YAML），便于实验复现实验条件。

---


## 11. 使用你自己的测试图片（skimage 直接读取）

可直接运行下面命令测试你提供的三通道 JPG：

```bash
PYTHONPATH=.:src python scripts/run_user_image_test.py --image "D:\\vrcontent\\biopiccw\\test.jpg" --output "user_test_output.jpg"
```

脚本会用 `skimage.io.imread` 读取图像，然后执行完整渲染管线并保存输出。

