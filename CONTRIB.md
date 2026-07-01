# Contributing to the Fung QField Project

## Project Map

The QGIS project is centered on Neuchatel and uses an offline Swiss official
topographic basemap. The former online Google satellite layer was removed
because it did not load reliably in the QField app.

Open `qgis/fung/fung.qgs` in QGIS and confirm:

- `observations` is the active editable point layer.
- `species_list`, `collector_list`, and `observation_subject` are lookup layers.
- `neuchatel_canton` and `neuchatel_basemap` are the layers in the `map` group.
- Sample IDs validate as `fung_######`.

The offline files live in `qgis/fung/optimized_maps/`:

- `neuchatel_canton.gpkg`: official canton polygon from
  `ch.swisstopo.swissboundaries3d-kanton-flaeche.fill`.
- `neuchatel_basemap.mbtiles`: `ch.swisstopo.pixelkarte-farbe` rendered to
  MBTiles, currently about 58 MB.

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
`DCIM/fung` attachment folder convention. `optimized_maps` must be copied so the
local MBTiles and canton polygon are available on the device.
