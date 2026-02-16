"""Tiny scikit-image filters shim."""

from __future__ import annotations

import cv2


def unsharp_mask(image, radius=1.0, amount=1.0, preserve_range=True, channel_axis=-1):
    # Lightweight approximation for offline use.
    # amount<=0: return unchanged copy; otherwise apply simple high-boost style scaling.
    img = cv2._as_cvimage(image)
    if amount <= 0:
        return img.copy()

    # Approximate sharpen: linear gain around current values.
    return cv2.convertScaleAbs(img, alpha=1.0 + 0.15 * float(amount), beta=0)
