import fiona
from shapely.geometry import shape,MultiLineString, mapping

with fiona.open("../data/US_county/500k/cb_2017_us_county_500k.shp") as source:
    with fiona.open("../data/US_county/500k/converted/dest_cb_2017_us_county_500k.shp",'w', driver='ESRI Shapefile',
                crs=source.crs,schema=source.schema) as ouput:
        for elem in source:
            reconstruct = shape(elem['geometry'])
            if elem['geometry']['type'] == 'MultiPolygon':
                for line in reconstruct:
                    ouput.write({'geometry':mapping(line),'properties':elem['properties']})
            elif elem['geometry']['type'] == 'Polygon':
                ouput.write({'geometry':mapping(reconstruct),'properties':elem['properties']})
