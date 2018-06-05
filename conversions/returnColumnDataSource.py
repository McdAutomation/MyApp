from bokeh.models.sources import ColumnDataSource
def getLineCoords(row, geom, coord_type):
    """Returns a list of coordinates ('x' or 'y') of a LineString geometry"""
    if coord_type == 'x':
        return list( row[geom].coords.xy[0] )
    elif coord_type == 'y':
        return list( row[geom].coords.xy[1] )

def returnCDS(p):
    p['x'] = p.apply(getLineCoords, geom='geometry', coord_type='x', axis=1)
    p['y'] = p.apply(getLineCoords, geom='geometry', coord_type='y', axis=1)
    dropped = p.drop("geometry",axis=1).copy()
    return ColumnDataSource(dropped)