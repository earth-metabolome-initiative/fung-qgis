# Offline Basemap Notes

The online Google Earth/satellite XYZ layer was removed because it did not load
in QField. The project now uses Swiss official data from geo.admin.ch:

- Canton polygon: `ch.swisstopo.swissboundaries3d-kanton-flaeche.fill`
- Basemap: `ch.swisstopo.swissimage`
- Projection: EPSG:3857 Web Mercator
- Output: `qgis/fung/optimized_maps/neuchatel_basemap.mbtiles`
- QGIS/QField provider: GDAL raster
- Datasource: `./optimized_maps/neuchatel_basemap.mbtiles`
- Current size: about 147 MB
- MBTiles zoom metadata: minzoom 13, maxzoom 16 after overviews
- QFieldSync layer action: `copy`
- QFieldCloud action: `no_action`
- QFieldSync `createBaseMap`: `false`

The basemap is an aerial/orthophoto mosaic, not a drawn topographic map. It was
generated at 2.5 m source resolution with JPEG quality 75 so the whole canton
remains well below the 500 MB QField package target.

QFieldCloud packages the project by rewriting relative file paths under
`files/`. The phone must therefore receive and load
`files/optimized_maps/neuchatel_basemap.mbtiles` directly. The basemap layer is
kept as a GDAL raster layer; it is not a WMS/MBTiles connection and is not
removed from the cloud project.

If a QField download is only a few megabytes, the MBTiles file was not uploaded
or packaged. The QFieldCloud project details should show `providerKey`/provider
as GDAL and a package size roughly 150 MB larger than the vector-only project.

Official references checked:

- geo.admin.ch WMTS documentation:
  https://docs.geo.admin.ch/visualize-data/wmts.html
- geo.admin.ch XYZ documentation:
  https://docs.geo.admin.ch/visualize-data/xyz.html
- geo.admin.ch identify endpoint documentation:
  https://docs.geo.admin.ch/access-data/identify-features.html
