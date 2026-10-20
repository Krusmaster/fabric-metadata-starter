from pathlib import Path
import pytest
from fabric_metadata_starter import load_metadata, render_all

MD = Path(__file__).resolve().parents[1] / "metadata"


def test_example_metadata_is_valid():
    assert load_metadata(MD).validate() == []


def test_render_produces_expected_files():
    files = render_all(load_metadata(MD))
    assert set(files) == {"nb_bronze_vbak.py", "nb_bronze_vbap.py", "nb_silver_sales_order.py", "nb_orchestrator.py"}
    assert "kna1" not in "".join(files)           # inactive object not generated
    assert '"bronze.vbak"' in files["nb_silver_sales_order.py"]
    assert "nb_bronze_vbak" in files["nb_orchestrator.py"]


def test_render_is_deterministic():
    md = load_metadata(MD)
    assert render_all(md) == render_all(md)


def test_validation_catches_bad_join_key(tmp_path):
    for f in MD.glob("*.yaml"):
        (tmp_path / f.name).write_text(f.read_text())
    (tmp_path / "business_object.yaml").write_text(
        "- {id: x, name: X, header: VBAK, items: [VBAP], join_key: [VBELN], owner: a@b}")
    errs = load_metadata(tmp_path).validate()
    assert any("not a prefix" in e for e in errs)


def test_validation_requires_owner(tmp_path):
    for f in MD.glob("*.yaml"):
        (tmp_path / f.name).write_text(f.read_text())
    (tmp_path / "business_object.yaml").write_text(
        "- {id: x, name: X, header: VBAK, items: [], join_key: [MANDT, VBELN]}")
    assert any("owner" in e for e in load_metadata(tmp_path).validate())
