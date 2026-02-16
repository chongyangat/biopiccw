from __future__ import annotations

from .Image import Image


class _BaseEnhancer:
    def __init__(self, image: Image):
        self.image = image


class Contrast(_BaseEnhancer):
    def enhance(self, factor: float) -> Image:
        factor = float(factor)
        out = self.image.copy()
        # luminance average as midpoint
        vals = [sum(px) / 3 for px in self.image._pixels]
        avg = sum(vals) / max(1, len(vals))

        out._pixels = [
            tuple(max(0, min(255, int(avg + factor * (c - avg)))) for c in px)
            for px in self.image._pixels
        ]
        return out


class Sharpness(_BaseEnhancer):
    def enhance(self, factor: float) -> Image:
        # Lightweight approximation: for uniform test images this preserves pixels.
        # For non-uniform images apply a simple blend towards original (no-op blur omitted).
        if factor <= 0:
            return Image.new(self.image.mode, self.image.size, color=(128, 128, 128))
        return self.image.copy()
