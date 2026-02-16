"""Tiny scikit-image exposure shim."""

from __future__ import annotations

import cv2


def adjust_gamma(image, gamma: float = 1.0):
    if gamma <= 0:
        raise ValueError("gamma must be > 0")

    img = cv2._as_cvimage(image)
    base_lut = [min(255, int((x / 255) ** (1 / gamma) * 255)) for x in range(256)]
    lut = base_lut * 3
    out = img._img.point(lut)
    return cv2.CVImage(out)
