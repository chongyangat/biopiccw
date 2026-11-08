from pathlib import Path
import os
import subprocess
import sys

import numpy as np
from skimage import io


def test_run_user_image_script_with_temp_image(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
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
    env["PYTHONPATH"] = os.pathsep.join(
        [str(repo_root), str(repo_root / "src"), env.get("PYTHONPATH", "")]
    )
    result = subprocess.run(
        cmd,
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert output_path.exists()
