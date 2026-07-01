# Offline Basemap Notes

The online Google Earth/satellite XYZ layer was removed because it did not load
in QField. The project now uses Swiss official data from geo.admin.ch:

- Canton polygon: `ch.swisstopo.swissboundaries3d-kanton-flaeche.fill`
- Basemap: `ch.swisstopo.pixelkarte-farbe`
- Projection: EPSG:3857 Web Mercator
- Output: `qgis/fung/optimized_maps/neuchatel_basemap.mbtiles`
- Current size: about 58 MB
- MBTiles zoom metadata: minzoom 12, maxzoom 15 after overviews

Why `pixelkarte-farbe` instead of SWISSIMAGE: the topographic JPEG tiles are
much smaller for a canton-wide offline package and still useful for field
navigation. SWISSIMAGE can be regenerated later for a smaller field polygon if
orthophoto detail becomes more important than file size.

Official references checked:

- geo.admin.ch WMTS documentation:
  https://docs.geo.admin.ch/visualize-data/wmts.html
- geo.admin.ch XYZ documentation:
  https://docs.geo.admin.ch/visualize-data/xyz.html
- geo.admin.ch identify endpoint documentation:
  https://docs.geo.admin.ch/access-data/identify-features.html
