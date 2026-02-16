import json
import os
from pathlib import Path


def test_notebook_import_cell_runs_from_notebooks_cwd() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    nb_path = repo_root / "notebooks" / "visual_aid_pipeline.ipynb"
    nb = json.loads(nb_path.read_text(encoding="utf-8"))

    import_cell_code = "".join(nb["cells"][4]["source"])

    prev_cwd = Path.cwd()
    try:
        os.chdir(repo_root / "notebooks")
        ns = {}
        exec(import_cell_code, ns)
        assert "render_pipeline" in ns
        assert callable(ns["render_pipeline"])
    finally:
        os.chdir(prev_cwd)
