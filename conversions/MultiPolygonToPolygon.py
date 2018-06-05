import fiona
from shapely.geometry import shape,MultiLineString, mapping

with fiona.open("../data/us_states/cb_2017_us_state_20m.shp") as source:
    with fiona.open("../data/us_states/newfolder/world_dest.shp",'w', driver='ESRI Shapefile',
                crs=source.crs,schema=source.schema) as ouput:
        for elem in source:
            reconstruct = shape(elem['geometry'])
            if elem['geometry']['type'] == 'MultiPolygon':
                for line in reconstruct:
                    ouput.write({'geometry':mapping(line),'properties':elem['properties']})
            elif elem['geometry']['type'] == 'Polygon':
                ouput.write({'geometry':mapping(reconstruct),'properties':elem['properties']})
