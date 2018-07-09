from shapely.ops import cascaded_union, polygonize
from scipy.spatial import Delaunay
from bokeh.plotting import figure, output_file, show
import numpy as np
import math
import shapely.geometry as geometry

output_file("patch.html")

p = figure(plot_width=400, plot_height=400)
'''
x_axis = [1, 2, 3, 4, 5]
y_axis = [6, 6, 8, 7, 3]
arr=[]
for i in range(len(x_axis)):
    arr.append([x_axis[i],y_axis[i]])
'''

#points = np.array(arr)

# ---------------
points = [(-85.70686500000001, 38.168409000000004), (-85.85045500000001, 38.127988), (-85.045275, 41.069272), (-87.365181, 36.539805)]
points = np.array(points)

def alpha_shape(points, alpha):
    """
    Compute the alpha shape (concave hull) of a set
    of points.
    @param points: Iterable container of points.
    @param alpha: alpha value to influence the
        gooeyness of the border. Smaller numbers
        don't fall inward as much as larger numbers.
        Too large, and you lose everything!
    """
    if len(points) < 4:
        # When you have a triangle, there is no sense
        # in computing an alpha shape.
        return False
    def add_edge(edges, edge_points, coords, i, j):
        """
        Add a line between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            return
        edges.add( (i, j) )
        edge_points.append(coords[ [i, j] ])
    coords = np.array([point
                       for point in points])
    tri = Delaunay(coords)
    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the
    # triangle
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]
        # Lengths of sides of triangle
        a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
        b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
        c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)
        # Semiperimeter of triangle
        s = (a + b + c)/2.0
        # Area of triangle by Heron's formula
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        circum_r = a*b*c/(4.0*area)
        # Here's the radius filter.
        #print circum_r
        if circum_r < 1.0/alpha:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)
    m = geometry.MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return cascaded_union(triangles), edge_points

if __name__ == '__main__':
    concave_hull, edge_points = alpha_shape(points,
                                            alpha=0.1)

    #p.circle(x_axis,y_axis,size=5,color="black")
    #p.circle(points[:,0],points[:,1],size=5,color="black")
    x_axis = []
    y_axis = []
    print(concave_hull)
    x_axis = list(concave_hull.exterior.coords.xy[0])
    y_axis = list(concave_hull.exterior.coords.xy[1])

    x_axis.append(x_axis[0])
    y_axis.append(y_axis[0])

    x_axis = [-85.045275, -87.365181, -85.85045500000001, -85.045275, -85.045275]
    y_axis = [41.069272, 36.539805, 38.127988, 41.069272, 41.069272]
    #print(list(x_axis),list(y_axis))
    p.line(x_axis,y_axis,color='blue')

    show(p)
