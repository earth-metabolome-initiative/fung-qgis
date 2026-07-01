# Contributing to the Fung QField Project

## Project map

The QGIS project is centered on Neuchatel and keeps only one online map layer:
Google satellite XYZ tiles. There is no offline MBTiles basemap and no project
polygon layer in this first `fung` version.

Open `qgis/fung/fung.qgs` in QGIS and confirm:

- `observations` is the active editable point layer.
- `species_list`, `collector_list`, and `observation_subject` are lookup layers.
- `google-satellite` is the only layer in the `map` group.
- Sample IDs validate as `fung_######`.

## Rebuilding taxa

Use the commands in `README.md` to rebuild the Swiss iNaturalist exports,
gnverifier outputs, higher-taxa table, and `species_list.gpkg`.

The current `Trees` command resolves to iNaturalist taxon `211194`
(`Tracheophyta`). Treat that as an implementation note, not a final biological
definition of trees. A future template should support a curated tree taxon list
or an explicit source table.

## QField export

Recommended export directory:

```text
/Users/pma/QField/export/fung
```

When packaging with QFieldSync, include the GeoPackage lookup tables and the
`DCIM/fung` attachment folder convention. Do not create an offline basemap for
this project unless the map policy changes.
