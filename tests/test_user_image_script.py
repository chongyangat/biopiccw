from pathlib import Path
import os
import subprocess
import sys

from PIL import Image


def test_run_user_image_script_with_temp_image(tmp_path: Path) -> None:
    image_path = tmp_path / "test.jpg"
    output_path = tmp_path / "out.jpg"
    Image.new("RGB", (16, 12), color=(100, 120, 140)).save(image_path)

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
