# Collection Project Template Memory

These are the reusable steps captured while establishing `fung-qgis` from the
Manaslu reference project.

1. Copy the project scaffold: Python scripts, tests, QGIS project, lookup
   GeoPackages, and documentation.
2. Set the project code everywhere: folder name, QGIS title, relation IDs,
   QField export path, attachment path, and sample ID prefix.
3. Create an empty `observations.gpkg` from the reference schema.
4. Choose the map policy early. For `fung`, keep only online Google satellite
   and disable QFieldSync offline-basemap creation.
5. Set the QGIS canvas and QFieldSync area of interest to the target field area.
6. Fetch regional iNaturalist species by country and taxon, keeping metadata
   for the resolved place and taxon IDs.
7. Deduplicate fetched species, resolve names with `gnverifier`, derive and
   resolve higher taxa, then build `species_list.csv` and `species_list.gpkg`.
8. Scan for stale project strings and validate with `pytest`, `ruff`, `ogrinfo`,
   and a manual QGIS open.

For the future git-versioned template, parameterize: project code, sample ID
prefix, field center/extent, map layer policy, regional place, source taxa, and
attachment folder.
