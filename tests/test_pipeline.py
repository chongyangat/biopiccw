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
    image = np.array(
        [
            [[0.2, 0.3, 0.4], [0.4, 0.5, 0.6]],
            [[0.6, 0.7, 0.8], [0.8, 0.9, 1.0]],
        ],
        dtype=np.float32,
    )
    out = adjust_dynamic_range(image, 1.0)
    assert np.allclose(out, image)


def test_enhance_contrast_factor_changes_output() -> None:
    image = np.array([[[0.25, 0.5, 0.75], [0.35, 0.5, 0.65]]], dtype=np.float32)
    low = enhance_contrast(image, 0.5)
    high = enhance_contrast(image, 2.0)
    assert not np.allclose(low, high)
    assert np.all((0.0 <= low) & (low <= 1.0))
    assert np.all((0.0 <= high) & (high <= 1.0))


def test_constant_image_preserves_intensity(tmp_path: Path) -> None:
    input_path = tmp_path / "constant.png"
    image = np.full((8, 8, 3), 128, dtype=np.uint8)
    io.imsave(str(input_path), image)

    loaded = load_image(input_path)
    rendered = render_pipeline(
        image_path=input_path,
        magnification_factor=1.0,
        contrast_factor=1.0,
        sharpness_factor=0.0,
        gamma=1.0,
        delay_seconds=0.0,
    )

    expected = 128.0 / 255.0
    assert np.allclose(loaded, expected, atol=1 / 255)
    assert np.allclose(rendered, expected, atol=1 / 255)


def test_save_image_preserves_constant_intensity(tmp_path: Path) -> None:
    output_path = tmp_path / "out" / "constant.png"
    save_image(np.full((4, 4, 3), 0.5, dtype=np.float32), output_path)

    saved = io.imread(str(output_path))
    assert saved.shape == (4, 4, 3)
    assert np.allclose(saved.mean(), 128, atol=1)


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
