"""Core rendering pipeline for visual-aid simulation (pure scikit-image)."""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
from skimage import exposure, filters, io, transform, util


# Step 1: 图像加载与输入
# 功能：使用 skimage 读取输入图像并转换为 RGB float32（范围 [0, 1]）。
def load_image(image_path: str | Path):
    """Load image as normalized RGB float32 in [0, 1] using skimage."""
    image = io.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")

    # 统一为 3 通道 RGB
    if image.ndim == 2:
        image = np.stack([image, image, image], axis=-1)
    elif image.ndim == 3 and image.shape[2] == 4:
        image = image[:, :, :3]

    return util.img_as_float32(image)


# Step 2: 图像放大（模拟放大设备）
# 功能：按放大倍率调整图像尺寸（skimage.transform.resize）。
def apply_magnification(image, magnification_factor: float):
    if magnification_factor <= 0:
        raise ValueError("magnification_factor must be > 0")

    height, width = image.shape[:2]
    new_h = max(1, int(height * magnification_factor))
    new_w = max(1, int(width * magnification_factor))
    resized = transform.resize(
        image,
        output_shape=(new_h, new_w, image.shape[2]),
        order=3,
        anti_aliasing=True,
        preserve_range=True,
    )
    return np.clip(resized.astype(np.float32), 0.0, 1.0)


# Step 3: 对比度增强
# 功能：线性对比度增强（以 0.5 为中心缩放，保持 [0,1]）。
def enhance_contrast(image, contrast_factor: float):
    if contrast_factor < 0:
        raise ValueError("contrast_factor must be >= 0")

    enhanced = (image - 0.5) * contrast_factor + 0.5
    return np.clip(enhanced, 0.0, 1.0).astype(np.float32)


# Step 4: 边缘锐化
# 功能：使用 unsharp mask 提升边缘细节（输入输出均为 [0,1]）。
def sharpen_image(image, sharpness_factor: float):
    if sharpness_factor < 0:
        raise ValueError("sharpness_factor must be >= 0")

    sharpened = filters.unsharp_mask(
        image,
        radius=1.0,
        amount=sharpness_factor,
        preserve_range=True,
        channel_axis=-1,
    )
    return np.clip(sharpened, 0.0, 1.0).astype(np.float32)


# Step 5: 动态范围调整
# 功能：通过 gamma 校正模拟 HDR->LDR 映射（基于 [0,1]）。
def adjust_dynamic_range(image, gamma: float):
    if gamma <= 0:
        raise ValueError("gamma must be > 0")

    adjusted = exposure.adjust_gamma(image, gamma=gamma)
    return np.clip(adjusted, 0.0, 1.0).astype(np.float32)


# Step 6: 延迟模拟
# 功能：模拟设备处理延迟。
def simulate_latency(image, delay_seconds: float):
    if delay_seconds < 0:
        raise ValueError("delay_seconds must be >= 0")

    time.sleep(delay_seconds)
    return image


# Step 7: 串联渲染管线
def render_pipeline(
    image_path: str | Path,
    magnification_factor: float,
    contrast_factor: float,
    sharpness_factor: float,
    gamma: float,
    delay_seconds: float,
):
    image = load_image(image_path)
    image = apply_magnification(image, magnification_factor)
    image = enhance_contrast(image, contrast_factor)
    image = sharpen_image(image, sharpness_factor)
    image = adjust_dynamic_range(image, gamma)
    image = simulate_latency(image, delay_seconds)
    return image


# Step 8: 输出保存
# 功能：将 [0,1] RGB float 转为 uint8 并使用 skimage.io.imsave 写盘。
def save_image(image, output_path: str | Path) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    image_u8 = util.img_as_ubyte(np.clip(image, 0.0, 1.0))
    io.imsave(str(output), image_u8)
