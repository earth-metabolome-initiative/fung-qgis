from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_qgis_project_uses_fung_sample_id_convention() -> None:
    qgs = (PROJECT_ROOT / "qgis/fung/fung.qgs").read_text(encoding="utf-8")

    assert "^fung_[0-9]{6}$" in qgs
    assert "DCIM/fung/" in qgs
    assert "dbgi_" not in qgs
    assert "DCIM/manaslu" not in qgs


def test_qgis_project_has_only_google_map_layer() -> None:
    qgs = (PROJECT_ROOT / "qgis/fung/fung.qgs").read_text(encoding="utf-8")

    assert 'name="google-satellite"' in qgs
    assert "basemap.mbtiles" not in qgs
    assert "optimized_maps" not in qgs
    assert "Fung-EMI" not in qgs
