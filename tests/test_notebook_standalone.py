import json
from pathlib import Path


def test_notebook_embeds_core_pipeline_logic() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    nb_path = repo_root / "notebooks" / "visual_aid_pipeline.ipynb"
    nb = json.loads(nb_path.read_text(encoding="utf-8"))

    core_cell = "".join(nb["cells"][4]["source"])

    assert "def load_image(" in core_cell
    assert "def apply_magnification(" in core_cell
    assert "def enhance_contrast(" in core_cell
    assert "def sharpen_image(" in core_cell
    assert "def adjust_dynamic_range(" in core_cell
    assert "def simulate_latency(" in core_cell
    assert "def render_pipeline(" in core_cell
    assert "def save_image(" in core_cell
