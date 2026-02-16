"""Tiny local OpenCV-compatible shim for offline tests.

Only implements APIs used by this project.
"""

from __future__ import annotations

from PIL import Image as _ImageModule

IMREAD_COLOR = 1
COLOR_BGR2RGB = 4
COLOR_RGB2BGR = 5
INTER_LANCZOS4 = 4


class CVImage:
    def __init__(self, pil_image):
        self._img = pil_image

    @property
    def shape(self):
        w, h = self._img.size
        return (h, w, 3)

    def getpixel(self, xy):
        return self._img.getpixel(xy)

    def copy(self):
        return CVImage(self._img.copy())


def _as_cvimage(image):
    if isinstance(image, CVImage):
        return image
    return CVImage(image)


def imread(path: str, _flag: int = IMREAD_COLOR):
    try:
        img = _ImageModule.open(path).convert("RGB")
    except Exception:
        return None
    return CVImage(img)


def imwrite(path: str, image) -> bool:
    img = _as_cvimage(image)
    img._img.save(path)
    return True


def cvtColor(image, code: int):
    img = _as_cvimage(image)
    if code not in (COLOR_BGR2RGB, COLOR_RGB2BGR):
        return img.copy()

    out = img._img.copy()
    w, h = out.size
    for y in range(h):
        for x in range(w):
            r, g, b = out.getpixel((x, y))
            out.putpixel((x, y), (b, g, r))
    return CVImage(out)


def resize(image, dsize, interpolation: int = INTER_LANCZOS4):
    img = _as_cvimage(image)
    width, height = dsize
    return CVImage(img._img.resize((width, height), interpolation))


def convertScaleAbs(image, alpha: float = 1.0, beta: float = 0.0):
    img = _as_cvimage(image)
    out = img._img.copy()
    w, h = out.size
    for y in range(h):
        for x in range(w):
            r, g, b = out.getpixel((x, y))
            out.putpixel(
                (x, y),
                tuple(max(0, min(255, int(alpha * c + beta))) for c in (r, g, b)),
            )
    return CVImage(out)
