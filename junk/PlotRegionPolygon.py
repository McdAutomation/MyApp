import pandas as pd
from util.concave_hull import alpha_shape
from bokeh.plotting import figure
import geopandas as gpd
from conversions import returnPDS
from bokeh.plotting import show
from bokeh.models import HoverTool
path = "./x_y.csv"

data = pd.read_csv(path)

ctr = {}

for i in range(13894):
    try:
        ctr[data.loc[i]['region']].append( [data.loc[i]['x'],data.loc[i]['y']] )
    except:
        ctr[data.loc[i]['region']] = [[data.loc[i]['x'],data.loc[i]['y']]]

#print(ctr)
#color = ["#FF0000","#FF1100","#FF2300","#FF3400","#FF4600","#FF5700","#FF6900","#FF7B00","#FF8C00","#FF9E00","#FFAF00","#FFC100","#FFD300","#FFE400","#FFF600","#F7FF00","#E5FF00","#D4FF00","#C2FF00","#B0FF00","#9FFF00","#8DFF00","#7CFF00","#6AFF00","#58FF00","#47FF00","#35FF00","#24FF00","#12FF00","#00FF00","#787878",
 #        "#808080","909090","A8A8A8","FF69B4"]

color = ["#E52B50","#9F2B68","#F19CBB","#AB274F","#D3212D","#3B7A57","#FFBF00","#FF7E00","#3B3B6D","#804040","#CD9575","#665D1E","#915C83","#841B2D","#00FFFF","#7FFFD4","#D0FF14","#C0C0C0","#007FFF","#1DACD6","#9FFF00","#8DFF00","#7CFF00","#6AFF00","#58FF00","#47FF00","#35FF00","#24FF00","#12FF00","#00FF00","#787878",
         "#808080","909090","A8A8A8","FF69B4"]

cds_bokeh = dict(x=[], y=[], COLOR=[])
i=0
for key in ctr:
    try:
        concave_hull, edge_points = alpha_shape(ctr[key],alpha=0.5)
    except:
        continue
    try:
        list_poly = list(concave_hull)
    except:
        poly = concave_hull
        list_x, list_y = poly.exterior.coords.xy
        # print(list(poly))
        cds_bokeh['x'].append(list(list_x))
        cds_bokeh['y'].append(list(list_y))
        cds_bokeh['COLOR'].append(color[i])
        i+=1
        continue
    for poly in list_poly:
        list_x, list_y = poly.exterior.coords.xy
        #print(list(poly))
        cds_bokeh['x'].append(list(list_x))
        cds_bokeh['y'].append(list(list_y))
        cds_bokeh['COLOR'].append(color[i])
    i+=1
#print(cds_bokeh)



filePath = r"./data/custom_us_map/US_from_world_map.shp"
p = gpd.read_file(filePath)
us_country_polygon = returnPDS(p)

fig = figure(plot_width=1382,plot_height=700,x_range=(-200,50),y_range=(0,100),output_backend="webgl",x_axis_label="x",
             y_axis_label='y',title='alpha=0.5')



#########county

filepath_county = "./data/US_county/USA_county.shp"
p = gpd.read_file(filepath_county)
us_county_polygon = returnPDS(p)

#fig.multi_line('x','y',source=us_county_polygon,line_color='black',color='black')
fig.patches('x','y',source=us_county_polygon,line_color='black',color='white')

hover = HoverTool(tooltips=[
    ("index", "$index"),
    ("COUNTYFP", "@COUNTYFP")
])
fig.add_tools(hover)
############

#########country

#fig.patches('x', 'y', source=us_country_polygon, color='COLOR',line_color='black', line_width=0.3)

###########

fig.patches('x','y',source=cds_bokeh,color='COLOR')



points = pd.read_csv('./x_y.csv')

fig.circle(list(points['x']),list(points['y']),size=3,color='black')
show(fig)
