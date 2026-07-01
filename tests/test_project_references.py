from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_qgis_project_uses_fung_sample_id_convention() -> None:
    qgs = (PROJECT_ROOT / "qgis/fung/fung.qgs").read_text(encoding="utf-8")

    assert "^fung_[0-9]{6}$" in qgs
    assert "DCIM/fung/" in qgs
    assert "dbgi_" not in qgs
    assert "DCIM/manaslu" not in qgs


def test_qgis_project_uses_offline_neuchatel_map_layers() -> None:
    qgs = (PROJECT_ROOT / "qgis/fung/fung.qgs").read_text(encoding="utf-8")

    assert 'name="neuchatel_basemap"' in qgs
    assert 'name="neuchatel_canton"' in qgs
    assert "neuchatel_basemap.mbtiles" in qgs
    assert "neuchatel_canton.gpkg" in qgs
    assert "\"optimized_maps\": true" in qgs
    assert "mt1.google.com" not in qgs
    assert "Fung-EMI" not in qgs


def test_offline_basemap_stays_under_500_mb() -> None:
    mbtiles = PROJECT_ROOT / "qgis/fung/optimized_maps/neuchatel_basemap.mbtiles"

    assert mbtiles.stat().st_size < 500 * 1024 * 1024
