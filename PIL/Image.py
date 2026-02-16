from __future__ import annotations

import math
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


class Resampling:
    LANCZOS = "lanczos"


@dataclass
class Image:
    mode: str
    _size: tuple[int, int]
    _pixels: list[tuple[int, int, int]]

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @staticmethod
    def new(mode: str, size: tuple[int, int], color: tuple[int, int, int] = (0, 0, 0)) -> "Image":
        width, height = size
        pixels = [color for _ in range(width * height)]
        return Image(mode=mode, _size=size, _pixels=pixels)

    def copy(self) -> "Image":
        return Image(self.mode, self._size, self._pixels.copy())

    def convert(self, mode: str) -> "Image":
        if mode != "RGB":
            raise ValueError("Only RGB mode is supported in this shim")
        if self.mode == mode:
            return self.copy()
        return Image(mode=mode, _size=self._size, _pixels=self._pixels.copy())

    def _idx(self, x: int, y: int) -> int:
        width, _ = self._size
        return y * width + x

    def getpixel(self, xy: tuple[int, int]) -> tuple[int, int, int]:
        x, y = xy
        return self._pixels[self._idx(x, y)]

    def putpixel(self, xy: tuple[int, int], value: tuple[int, int, int]) -> None:
        x, y = xy
        self._pixels[self._idx(x, y)] = tuple(max(0, min(255, int(v))) for v in value)

    def resize(self, new_size: tuple[int, int], _resample: str | None = None) -> "Image":
        src_w, src_h = self._size
        dst_w, dst_h = new_size
        out = Image.new(self.mode, new_size)
        for y in range(dst_h):
            src_y = min(src_h - 1, int(y * src_h / max(1, dst_h)))
            for x in range(dst_w):
                src_x = min(src_w - 1, int(x * src_w / max(1, dst_w)))
                out.putpixel((x, y), self.getpixel((src_x, src_y)))
        return out

    def point(self, lut: Iterable[int]) -> "Image":
        table = list(lut)
        if len(table) != 256:
            raise ValueError("LUT must have 256 values")
        out = self.copy()
        out._pixels = [tuple(table[c] for c in px) for px in self._pixels]
        return out

    def save(self, path: str | Path) -> None:
        payload = {
            "mode": self.mode,
            "size": self._size,
            "pixels": self._pixels,
        }
        with Path(path).open("wb") as f:
            pickle.dump(payload, f)


def open(path: str | Path) -> Image:
    with Path(path).open("rb") as f:
        payload = pickle.load(f)
    return Image(mode=payload["mode"], _size=tuple(payload["size"]), _pixels=list(payload["pixels"]))


def new(mode: str, size: tuple[int, int], color: tuple[int, int, int] = (0, 0, 0)) -> Image:
    return Image.new(mode=mode, size=size, color=color)
