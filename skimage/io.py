"""Tiny scikit-image io shim."""

from __future__ import annotations

import cv2


def imread(path: str):
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    if image is None:
        return None
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
