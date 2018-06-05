from bokeh.models.sources import ColumnDataSource
def getCircleCoords(row, geom, coord_type):
    """Calculates coordinates ('x' or 'y') of a Point geometry"""
    if coord_type == 'x':
        return row[geom].x
    elif coord_type == 'y':
        return row[geom].y
def returnCircle(p):
    p['x'] = p.apply(getCircleCoords, geom='geometry', coord_type='x', axis=1)
    p['y'] = p.apply(getCircleCoords, geom='geometry', coord_type='y', axis=1)
    dropped = p.drop("geometry", axis=1).copy()
    return ColumnDataSource(dropped)