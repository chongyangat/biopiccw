import json
from pathlib import Path


def test_notebook_uses_user_provided_windows_path() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    nb_path = repo_root / "notebooks" / "visual_aid_pipeline.ipynb"
    nb = json.loads(nb_path.read_text(encoding="utf-8"))

    source = "".join(nb["cells"][6]["source"])
    assert r"D:\\vrcontent\\biopiccw\\test.jpg" in source
    assert "cv2.imread" in source
    assert "io.imread" in source
