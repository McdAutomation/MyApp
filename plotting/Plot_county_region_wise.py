import pandas as pd
from bokeh.plotting import figure
import geopandas as gpd
from conversions import returnPDS
from bokeh.plotting import show
from bokeh.models import HoverTool
path = "C:/Users/atrivedy/Documents/Visualilzation/testing/x_y.csv"

data = pd.read_csv(path)

fig = figure(plot_width=1382,plot_height=700,x_range=(-200,50),y_range=(0,100),output_backend="webgl",x_axis_label="x",
             y_axis_label='y',title='alpha=0.5')


def plot_alpha_shape(fig):
    """
    plot alpha shape
    :param fig: Bokeh figure
    :return:
    """
    cds_bokeh = pd.read_pickle('../data/region_analog.pkl')
    fig.patches('x','y',source=cds_bokeh,color='COLOR')


def plot_county(fig):
    color = ["#E52B50", "#9F2B68", "#F19CBB", "#AB274F", "#D3212D", "#3B7A57", "#FFBF00", "#FF7E00", "#3B3B6D",
             "#804040", "#CD9575", "#665D1E", "#915C83", "#841B2D", "#00FFFF", "#7FFFD4", "#D0FF14", "#C0C0C0",
             "#007FFF", "#1DACD6", "#9FFF00", "#8DFF00", "#7CFF00", "#6AFF00", "#58FF00", "#47FF00", "#35FF00",
             "#24FF00", "#12FF00", "#00FF00", "#787878",
             "#808080", "909090", "A8A8A8", "FF69B4"]

    regions = pd.read_csv('C:/Users/atrivedy/Documents/Visualilzation/region_wise.csv',sep=',')
    _color = {}
    _color['None'] = 'white'
    for i in range(len(regions['region'])):
        _color[regions.loc[i]['region']] = color[i]

    filepath_county = "C:/Users/atrivedy/Documents/Visualilzation/data/US_county/USA_county.shp"
    p = gpd.read_file(filepath_county)

    arr = []
    _data = pd.read_csv("C:/Users/atrivedy/Documents/Visualilzation/plotting/thisisit.csv",sep=',') # region_added_county_final.csv
    #print(_color[_data.loc[1]['Region']])
    for i in range(3304):
        arr.append([ _color[_data.loc[i]['Region']] ])
        #arr.append('#D3D3D3')


    p['COLOR'] = arr
    p['Region'] = _data['Region']
    us_county_polygon = returnPDS(p)

    renderer = fig.patches('x','y',source=us_county_polygon,line_color='Black',color='COLOR',line_width=0.1,name='bokehPatch')

    hover = HoverTool(
        renderers = [renderer],
        tooltips=[
        #("index", "$index"),
        ("Name", "@NAME"),
        ("Region", "@Region"),
        #("GEOID", "@GEOID")
    ])
    fig.add_tools(hover)

    return renderer, us_county_polygon


def plot_restaurants(fig):
    """
    plot restaurant points
    :param fig:
    :return:
    """
    points = pd.read_csv('../x_y.csv')
    fig.circle(list(points['x']),list(points['y']),size=3,color='black')


if __name__ == '__main__':
    plot_county(fig)
    show(fig)
