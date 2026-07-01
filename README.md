# Fung QField project

Project code: `fung`

This repository contains the QGIS/QField collection project for the UniNe fungi
collection program. The project is centered on Neuchatel, Switzerland, and uses
an online Google satellite XYZ layer only.

## Main files

- QGIS/QField project: `qgis/fung/fung.qgs`
- Active observation layer: `qgis/fung/observations.gpkg`
- Species lookup: `qgis/fung/species_list.gpkg`
- Collector lookup: `qgis/fung/collector_list.gpkg`
- Observation subject lookup: `qgis/fung/observation_subject.gpkg`

## QField conventions

- The active observation layer follows the same schema as the Manaslu reference
  project.
- Sample identifiers must match `fung_######`.
- QField image paths are generated from the sample identifier only, for example
  `DCIM/fung/fung_000001_01.jpg`.
- `uuid_qfield` is generated automatically with QGIS `uuid('WithoutBraces')`.

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
```
