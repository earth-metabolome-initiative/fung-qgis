# Fung QField project

Project code: `fung`

This repository contains the QGIS/QField collection project for the UniNe fungi
collection program. The project is centered on Neuchatel, Switzerland, and uses
an offline basemap generated from Swiss official geo.admin.ch services.

## Main files

- QGIS/QField project: `qgis/fung/fung.qgs`
- Active observation layer: `qgis/fung/observations.gpkg`
- Species lookup: `qgis/fung/species_list.gpkg`
- Collector lookup: `qgis/fung/collector_list.gpkg`
- Observation subject lookup: `qgis/fung/observation_subject.gpkg`
- Canton polygon: `qgis/fung/optimized_maps/neuchatel_canton.gpkg`
- Offline basemap: `qgis/fung/optimized_maps/neuchatel_basemap.mbtiles`

## QField conventions

- The active observation layer follows the same schema as the Manaslu reference
  project.
- Sample identifiers must match `fung_######`.
- QField image paths are generated from the sample identifier only, for example
  `DCIM/fung/fung_000001_01.jpg`.
- `uuid_qfield` is generated automatically with QGIS `uuid('WithoutBraces')`.

## Offline basemap

The QField app did not load the online Google Earth/Google satellite layer
reliably, so the project now uses a local MBTiles basemap.

- Boundary source: geo.admin.ch identify endpoint, layer
  `ch.swisstopo.swissboundaries3d-kanton-flaeche.fill`, point inside Neuchatel.
- Basemap source: geo.admin.ch WMTS/XYZ, layer `ch.swisstopo.swissimage`.
- Output: JPEG MBTiles at 2.5 m source resolution with lower-zoom overviews.
- Current file size: about 147 MB, below the 500 MB target.

Regenerate the canton polygon and basemap:

```bash
mkdir -p qgis/fung/optimized_maps

curl -L --fail \
  "https://api3.geo.admin.ch/rest/services/ech/MapServer/identify?geometry=6.93,46.99&geometryType=esriGeometryPoint&layers=all:ch.swisstopo.swissboundaries3d-kanton-flaeche.fill&tolerance=0&returnGeometry=true&geometryFormat=geojson&sr=4326&lang=en&limit=10" \
  --output qgis/fung/optimized_maps/neuchatel_canton_identify.json

jq '{type:"FeatureCollection", features:.results}' \
  qgis/fung/optimized_maps/neuchatel_canton_identify.json \
  > qgis/fung/optimized_maps/neuchatel_canton.geojson

ogr2ogr -f GPKG \
  qgis/fung/optimized_maps/neuchatel_canton.gpkg \
  qgis/fung/optimized_maps/neuchatel_canton.geojson \
  -nln neuchatel_canton -overwrite

gdalwarp -overwrite -of GTiff \
  -t_srs EPSG:3857 \
  -te 716255.65 5917003.10 788915.67 5969319.94 \
  -tr 2.5 2.5 -r bilinear \
  -co TILED=YES -co COMPRESS=JPEG -co JPEG_QUALITY=75 \
  "WMTS:https://wmts.geo.admin.ch/EPSG/3857/1.0.0/WMTSCapabilities.xml,layer=ch.swisstopo.swissimage" \
  /tmp/neuchatel_swissimage_2_5m.tif

gdal_translate -of MBTILES \
  -co TILE_FORMAT=JPEG -co QUALITY=75 \
  /tmp/neuchatel_swissimage_2_5m.tif \
  qgis/fung/optimized_maps/neuchatel_basemap.mbtiles

gdaladdo -r average qgis/fung/optimized_maps/neuchatel_basemap.mbtiles 2 4 8
```

## Taxonomic resolution

The active QField species lookup is built from Swiss iNaturalist species-count
exports for Basidiomycota and the iNaturalist-resolved `Trees` query. On
2026-07-01, iNaturalist resolved `Trees` to `Tracheophyta`; the metadata files
record this so the future template can replace it with a stricter curated tree
source if needed.

```bash
uv sync

uv run python scripts/fetch_inaturalist_species.py \
  --country-code CH \
  --taxon-name Basidiomycota \
  --output data/inaturalist/switzerland_basidiomycota_species_observations.csv

uv run python scripts/fetch_inaturalist_species.py \
  --country-code CH \
  --taxon-name Trees \
  --output data/inaturalist/switzerland_trees_species_observations.csv

uv run python scripts/combine_inaturalist_fetches.py \
  data/inaturalist/switzerland_basidiomycota_species_observations.csv \
  data/inaturalist/switzerland_trees_species_observations.csv \
  --output data/inaturalist/switzerland_species_observations.csv

uv run python scripts/resolve_taxa.py \
  --input data/inaturalist/switzerland_species_observations.csv \
  --header scientific_name \
  --dedupe-input \
  --force \
  --ro-crate data/inaturalist/switzerland_species_observations_ro-crate-metadata.json

uv run python scripts/build_higher_taxa_input.py \
  --input data/inaturalist/switzerland_species_observations_resolved.csv \
  --output data/inaturalist/switzerland_higher_taxa.csv

uv run python scripts/resolve_taxa.py \
  --input data/inaturalist/switzerland_higher_taxa.csv \
  --header scientific_name \
  --dedupe-input \
  --force \
  --ro-crate data/inaturalist/switzerland_higher_taxa_ro-crate-metadata.json

uv run python scripts/combine_species_and_higher_taxa.py \
  --species data/inaturalist/switzerland_species_observations_resolved.csv \
  --higher-taxa data/inaturalist/switzerland_higher_taxa_resolved.csv \
  --output qgis/fung/species_list.csv

ogr2ogr -f GPKG qgis/fung/species_list.gpkg qgis/fung/species_list.csv \
  -nln species_list -nlt NONE -overwrite -oo EMPTY_STRING_AS_NULL=YES
```

Current generated counts:

- Basidiomycota Swiss species rows: 2,152
- iNaturalist `Trees` query rows: 5,905
- Deduplicated species rows: 8,057
- Higher taxa rows: 4,075
- Final lookup rows: 12,132

## Checks

```bash
uv run pytest
uv run ruff check .
ogrinfo -so qgis/fung/observations.gpkg observations
ogrinfo -so qgis/fung/species_list.gpkg species_list
ogrinfo -so qgis/fung/optimized_maps/neuchatel_canton.gpkg neuchatel_canton
gdalinfo qgis/fung/optimized_maps/neuchatel_basemap.mbtiles
```
