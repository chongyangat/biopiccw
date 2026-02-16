"""Core rendering pipeline for visual-aid simulation."""

from __future__ import annotations

import time
from pathlib import Path

from PIL import Image, ImageEnhance


def load_image(image_path: str | Path) -> Image.Image:
    """Load an image from disk."""
    return Image.open(image_path).convert("RGB")


def apply_magnification(image: Image.Image, magnification_factor: float) -> Image.Image:
    """Resize an image according to magnification factor."""
    if magnification_factor <= 0:
        raise ValueError("magnification_factor must be > 0")

    width, height = image.size
    new_size = (int(width * magnification_factor), int(height * magnification_factor))
    new_size = (max(1, new_size[0]), max(1, new_size[1]))
    return image.resize(new_size, Image.Resampling.LANCZOS)


def enhance_contrast(image: Image.Image, contrast_factor: float) -> Image.Image:
    """Enhance image contrast."""
    if contrast_factor < 0:
        raise ValueError("contrast_factor must be >= 0")

    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(contrast_factor)


def sharpen_image(image: Image.Image, sharpness_factor: float) -> Image.Image:
    """Sharpen image edges and details."""
    if sharpness_factor < 0:
        raise ValueError("sharpness_factor must be >= 0")

    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(sharpness_factor)


def adjust_dynamic_range(image: Image.Image, gamma: float) -> Image.Image:
    """Apply gamma correction to map dynamic range."""
    if gamma <= 0:
        raise ValueError("gamma must be > 0")

    lut = [min(255, int((x / 255) ** (1 / gamma) * 255)) for x in range(256)]
    return image.point(lut)


def simulate_latency(image: Image.Image, delay_seconds: float) -> Image.Image:
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
) -> Image.Image:
    """Run the complete rendering pipeline and return the output image."""
    image = load_image(image_path)
    image = apply_magnification(image, magnification_factor)
    image = enhance_contrast(image, contrast_factor)
    image = sharpen_image(image, sharpness_factor)
    image = adjust_dynamic_range(image, gamma)
    image = simulate_latency(image, delay_seconds)
    return image


def save_image(image: Image.Image, output_path: str | Path) -> None:
    """Save image to disk."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
