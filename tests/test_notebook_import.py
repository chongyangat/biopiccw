import json
import os
from pathlib import Path

import pytest

pytest.importorskip("cv2")
pytest.importorskip("skimage")


def test_notebook_core_cell_runs_from_notebooks_cwd() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    nb_path = repo_root / "notebooks" / "visual_aid_pipeline.ipynb"
    nb = json.loads(nb_path.read_text(encoding="utf-8"))

    core_cell_code = "".join(nb["cells"][4]["source"])

    prev_cwd = Path.cwd()
    try:
        os.chdir(repo_root / "notebooks")
        ns = {}
        exec(core_cell_code, ns)
        assert "render_pipeline" in ns
        assert callable(ns["render_pipeline"])
    finally:
        os.chdir(prev_cwd)
