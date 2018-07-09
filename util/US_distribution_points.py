from bokeh.plotting import figure
import geopandas as gpd
from conversions import returnPDS
import pandas as pd
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import show
import csv
filePath = r"./data/custom_us_map/US_from_world_map.shp"
p = gpd.read_file(filePath)
us_country_polygon = returnPDS(p)

fig = figure(plot_width=1382,plot_height=700,x_range=(-200,50),y_range=(0,100),output_backend="webgl",x_axis_label="x",
             y_axis_label='y')

fig.patches('x', 'y', source=us_country_polygon, color='COLOR',
            line_color='black', line_width=0.3)

path_restaurant_data = r"C:/Users/atrivedy/Documents/Visualilzation/data/Active_Restaurant_List_05282018.xlsx"
restaurant_data = pd.read_excel(path_restaurant_data)

#path_all_us_data = r"C:/Users/atrivedy/Documents/Visualilzation/data/store_data_text.txt"
#us_data = pd.read_csv(filePath,sep='\t',error_bad_lines=False)
path_all_us_data = r"C:/Users/atrivedy/Documents/Visualilzation/data/store_data_text.txt"
us_data = pd.read_csv(path_all_us_data,sep='\t')

x_arr = []
y_arr = []
region_name = []

def createListXandY():
    for i in range(13975): #14084 - 13975
        try:
            xval = float((us_data.loc[us_data['NatlStrNumber'] == restaurant_data.loc[i]['RESTAURANT NUMBER']])['Longitude'])
            yval = float((us_data.loc[us_data['NatlStrNumber'] == restaurant_data.loc[i]['RESTAURANT NUMBER']])['Latitude'])

            region = ((us_data.loc[us_data['NatlStrNumber'] == restaurant_data.loc[i]['RESTAURANT NUMBER']])['Region'])

            x_arr.append(xval)
            y_arr.append(yval)
            region_name.append(str(region.values[0]))
        except Exception as e:
            print(i)
            #pass

if __name__ == '__main__':
    createListXandY()
    df = pd.DataFrame(data={"x": x_arr, "y": y_arr, 'region':region_name})
    df.to_csv("./x_y.csv", sep=',',index=False)
    print(len(region_name),len(x_arr))
