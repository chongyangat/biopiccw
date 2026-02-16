from pathlib import Path

import pytest
import cv2
from PIL import Image

from biopiccw.pipeline import (
    adjust_dynamic_range,
    apply_magnification,
    render_pipeline,
    save_image,
)


def make_test_image(path: Path, size=(20, 10), color=(120, 80, 40)) -> None:
    # Use PIL shim for deterministic local image creation; pipeline itself uses cv2/skimage APIs.
    image = Image.new("RGB", size=size, color=color)
    image.save(path)


def test_apply_magnification_changes_size() -> None:
    image = cv2.CVImage(Image.new("RGB", size=(10, 10), color=(100, 100, 100)))
    out = apply_magnification(image, 1.5)
    assert out.shape[:2] == (15, 15)


def test_adjust_dynamic_range_gamma_identity_approx() -> None:
    image = cv2.CVImage(Image.new("RGB", size=(1, 1), color=(128, 128, 128)))
    out = adjust_dynamic_range(image, 1.0)
    assert out.getpixel((0, 0)) == (128, 128, 128)


def test_render_pipeline_and_save(tmp_path: Path) -> None:
    input_path = tmp_path / "input.jpg"
    output_path = tmp_path / "out" / "output.jpg"
    make_test_image(input_path, size=(20, 10))

    output = render_pipeline(
        image_path=input_path,
        magnification_factor=2.0,
        contrast_factor=1.5,
        sharpness_factor=2.0,
        gamma=2.2,
        delay_seconds=0.0,
    )

    assert output.shape[:2] == (20, 40)
    save_image(output, output_path)
    assert output_path.exists()


@pytest.mark.parametrize(
    "kwargs",
    [
        {"magnification_factor": 0},
        {"contrast_factor": -1},
        {"sharpness_factor": -1},
        {"gamma": 0},
        {"delay_seconds": -0.1},
    ],
)
def test_invalid_params_raise(tmp_path: Path, kwargs: dict) -> None:
    input_path = tmp_path / "input.jpg"
    make_test_image(input_path)

    params = {
        "image_path": input_path,
        "magnification_factor": 1.0,
        "contrast_factor": 1.0,
        "sharpness_factor": 1.0,
        "gamma": 1.0,
        "delay_seconds": 0.0,
    }
    params.update(kwargs)

    with pytest.raises(ValueError):
        render_pipeline(**params)


def test_adjust_dynamic_range_smoke_rgb() -> None:
    image = cv2.CVImage(Image.new("RGB", size=(1, 1), color=(128, 128, 128)))
    out = adjust_dynamic_range(image, 2.2)
    assert out is not None
