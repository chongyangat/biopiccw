from pathlib import Path
import os
import subprocess
import sys

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("skimage")
from skimage import io


def test_run_user_image_script_with_temp_image(tmp_path: Path) -> None:
    image_path = tmp_path / "test.jpg"
    output_path = tmp_path / "out.jpg"

    image = np.zeros((12, 16, 3), dtype=np.uint8)
    image[:, :] = (100, 120, 140)
    io.imsave(str(image_path), image)

    cmd = [
        sys.executable,
        "scripts/run_user_image_test.py",
        "--image",
        str(image_path),
        "--output",
        str(output_path),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = ".:src"
    result = subprocess.run(
        cmd,
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert output_path.exists()
