"""Core rendering pipeline for visual-aid simulation."""

from __future__ import annotations

import time
from pathlib import Path

import cv2
from skimage import exposure, filters


def load_image(image_path: str | Path):
    """Load an image from disk as RGB."""
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def apply_magnification(image, magnification_factor: float):
    """Resize an image according to magnification factor."""
    if magnification_factor <= 0:
        raise ValueError("magnification_factor must be > 0")

    height, width = image.shape[:2]
    new_size = (max(1, int(width * magnification_factor)), max(1, int(height * magnification_factor)))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_LANCZOS4)


def enhance_contrast(image, contrast_factor: float):
    """Enhance image contrast via linear scaling."""
    if contrast_factor < 0:
        raise ValueError("contrast_factor must be >= 0")

    return cv2.convertScaleAbs(image, alpha=contrast_factor, beta=0)


def sharpen_image(image, sharpness_factor: float):
    """Sharpen image edges and details."""
    if sharpness_factor < 0:
        raise ValueError("sharpness_factor must be >= 0")

    return filters.unsharp_mask(
        image,
        radius=1.0,
        amount=sharpness_factor,
        preserve_range=True,
        channel_axis=-1,
    )


def adjust_dynamic_range(image, gamma: float):
    """Apply gamma correction to map dynamic range."""
    if gamma <= 0:
        raise ValueError("gamma must be > 0")

    return exposure.adjust_gamma(image, gamma=gamma)


def simulate_latency(image, delay_seconds: float):
    """Simulate device latency."""
    if delay_seconds < 0:
        raise ValueError("delay_seconds must be >= 0")

    time.sleep(delay_seconds)
    return image


def render_pipeline(
    image_path: str | Path,
    magnification_factor: float,
    contrast_factor: float,
    sharpness_factor: float,
    gamma: float,
    delay_seconds: float,
):
    """Run the complete rendering pipeline and return the output image."""
    image = load_image(image_path)
    image = apply_magnification(image, magnification_factor)
    image = enhance_contrast(image, contrast_factor)
    image = sharpen_image(image, sharpness_factor)
    image = adjust_dynamic_range(image, gamma)
    image = simulate_latency(image, delay_seconds)
    return image


def save_image(image, output_path: str | Path) -> None:
    """Save RGB image to disk."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    ok = cv2.imwrite(str(output), bgr)
    if not ok:
        raise IOError(f"Failed to save image: {output}")
