from pathlib import Path

import numpy as np
import pytest
from skimage import io

from biopiccw.pipeline import (
    adjust_dynamic_range,
    apply_magnification,
    enhance_contrast,
    load_image,
    render_pipeline,
    save_image,
)


def make_test_image(path: Path, size=(20, 10), color=(120, 80, 40)) -> None:
    h, w = size[1], size[0]
    image = np.zeros((h, w, 3), dtype=np.uint8)
    image[:, :] = color
    io.imsave(str(path), image)


def test_apply_magnification_changes_size() -> None:
    image = np.zeros((10, 10, 3), dtype=np.float32)
    out = apply_magnification(image, 1.5)
    assert out.shape[:2] == (15, 15)


def test_adjust_dynamic_range_gamma_identity() -> None:
    image = np.array([[[0.2, 0.3, 0.4], [0.8, 0.9, 1.0]]], dtype=np.float32)
    out = adjust_dynamic_range(image, 1.0)
    assert np.allclose(out, image)


def test_constant_grayscale_is_preserved(tmp_path: Path) -> None:
    input_path = tmp_path / "gray.png"
    image = np.full((4, 6), 128, dtype=np.uint8)
    io.imsave(str(input_path), image)

    out = load_image(input_path)
    assert out.shape == (4, 6, 3)
    assert np.allclose(out, 128 / 255.0, atol=1e-6)


def test_contrast_identity_preserves_brightness() -> None:
    image = np.full((2, 2, 3), 0.25, dtype=np.float32)
    out = enhance_contrast(image, 1.0)
    assert np.allclose(out, image)


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
    assert output.dtype == np.float32
    assert output.min() >= 0.0 and output.max() <= 1.0
    save_image(output, output_path)
    assert output_path.exists()


def test_save_image_preserves_constant_value(tmp_path: Path) -> None:
    output_path = tmp_path / "constant.png"
    image = np.full((3, 4, 3), 128 / 255.0, dtype=np.float32)
    save_image(image, output_path)

    saved = io.imread(str(output_path))
    assert np.allclose(saved, 128, atol=1)


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
