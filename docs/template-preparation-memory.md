# Collection Project Template Memory

These are the reusable steps captured while establishing `fung-qgis` from the
Manaslu reference project.

1. Copy the project scaffold: Python scripts, tests, QGIS project, lookup
   GeoPackages, and documentation.
2. Set the project code everywhere: folder name, QGIS title, relation IDs,
   QField export path, attachment path, and sample ID prefix.
3. Create an empty `observations.gpkg` from the reference schema.
4. Choose the map policy early. For `fung`, use an official Swiss offline
   MBTiles basemap because online Google tiles did not work in QField.
5. Set the QGIS canvas and QFieldSync area of interest to the target field area.
6. Fetch regional iNaturalist species by country and taxon, keeping metadata
   for the resolved place and taxon IDs.
7. Deduplicate fetched species, resolve names with `gnverifier`, derive and
   resolve higher taxa, then build `species_list.csv` and `species_list.gpkg`.
8. Scan for stale project strings and validate with `pytest`, `ruff`, `ogrinfo`,
   and a manual QGIS open.

For Swiss projects, prefer geo.admin.ch sources when possible:

- Use `ch.swisstopo.swissboundaries3d-kanton-flaeche.fill` for canton polygons.
- Use `ch.swisstopo.swissimage` for aerial/orthophoto MBTiles when field visual
  context matters.
- Keep offline basemaps below 500 MB and add lower-zoom overviews.

For the future git-versioned template, parameterize: project code, sample ID
prefix, field center/extent, map layer policy, regional place, source taxa, and
attachment folder.
