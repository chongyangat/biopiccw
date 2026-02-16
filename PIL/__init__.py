"""A tiny local PIL-compatible shim for offline testing.

This is **not** a full Pillow implementation. It only supports APIs used by this project.
"""

from . import Image, ImageEnhance

__all__ = ["Image", "ImageEnhance"]
