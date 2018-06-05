from bokeh.models.sources import ColumnDataSource


def getPolyCoords(row, geom, coord_type):
    """Returns the coordinates ('x' or 'y') of edges of a Polygon exterior"""

    # Parse the exterior of the coordinate
    exterior = row[geom].exterior

    if coord_type == 'x':
        # Get the x coordinates of the exterior
        return list(exterior.coords.xy[0])
    elif coord_type == 'y':
        # Get the y coordinates of the exterior
        return list(exterior.coords.xy[1])


def returnPDS(p):
    p['x'] = p.apply(getPolyCoords, geom='geometry', coord_type='x', axis=1)
    p['y'] = p.apply(getPolyCoords, geom='geometry', coord_type='y', axis=1)
    dropped = p.drop("geometry", axis=1).copy()
    return ColumnDataSource(dropped)
