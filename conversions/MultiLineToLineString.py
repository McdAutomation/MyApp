import fiona
from shapely.geometry import shape,MultiLineString, mapping

with fiona.open("IND_water_lines_dcw.shp") as source:
    with fiona.open("IND_water_lines_dcw_dest.shp",'w', driver='ESRI Shapefile',
                crs=source.crs,schema=source.schema) as ouput:
        for elem in source:
            reconstruct = shape(elem['geometry'])
            if elem['geometry']['type'] == 'MultiLineString':
                for line in reconstruct:
                    ouput.write({'geometry':mapping(line),'properties':elem['properties']})
            elif elem['geometry']['type'] == 'LineString':
                ouput.write({'geometry':mapping(reconstruct),'properties':elem['properties']})