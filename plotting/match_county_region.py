import pandas as pd
from concave_hull import alpha_shape
from bokeh.plotting import figure
import geopandas as gpd
from conversions import returnPDS
from bokeh.plotting import show
import json
fig = figure(plot_width=1382,plot_height=700,x_range=(-200,50),y_range=(0,100),output_backend="webgl",x_axis_label="x",
             y_axis_label='y')





county = pd.read_csv('../county_x_y.csv',sep=',')
points = pd.read_csv('../x_y.csv',sep=',')

#print(len(points['x'])) #13894
#print(len(county['x'])) #3304

def inside(x,y,xArr,yArr):
    _inside = False
    size = len(xArr)
    j = size -1
    for i in range(0,size):
        xi = xArr[i]
        yi = yArr[i]
        xj = xArr[j]
        yj = yArr[j]

        intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)

        if intersect:
            _inside = not _inside
        j = i
    return _inside

'''
arr = county.loc[0]['x'].strip()
print((arr))
arr = arr[1:len(arr)-1]
arr = list(map(float,arr.split(',')))
print((arr))
#
'''
def plotContainers():
    ctr = {}
    for i in range(13893):
        if i%50 == 0:
            print(i)
        line_x = []
        line_y = []
        points_x = []
        points_y = []
        for j in range(3304):
            xArr = county.loc[j]['x'].strip()
            xArr = xArr[1:len(xArr) - 1]
            xArr = list(map(float, xArr.split(',')))

            yArr = county.loc[j]['y'].strip()
            yArr = yArr[1:len(yArr) - 1]
            yArr = list(map(float, yArr.split(',')))

            x = points.loc[i]['x']
            y = points.loc[i]['y']


            if inside(x,y,xArr,yArr):
                #fig.line(xArr, yArr, line_color='black')
                #print(xArr,yArr)
                #fig.circle(x, y, size=3, color='black')
                '''
                try:
                    ctr[j].append([x,y,points.loc[i]['region']])
                    ctr[j][points.loc[i]['region']] += 1

                except:
                    ctr[j] = [[x,y,points.loc[i]['region']]]
                try:
                    ctr[points.loc[i]['region']] += 1
                except:
                    ctr[points.loc[i]['region']] = 1
                '''
                try:
                    ctr[j][points.loc[i]['region']] += 1
                except:
                    try:
                        ctr[j][points.loc[i]['region']] = 1
                    except:
                        ctr[j] = {}
                        ctr[j][points.loc[i]['region']] = 1

    #print(ctr)
    with open('./ctr.txt','w') as f:
        #f.write(json.dump(ctr))
        json.dump(ctr,f)

    '''
    region_ctr = {}
    for key in ctr:
        max = 0
        _dict = ctr[key]
        for subkey in _dict:
            if _dict[subkey] > max:
                _region = _dict[subkey]
    '''
    # assign regions
    arr = ["None"] * 3304

    for key in ctr:
        if len(ctr[key]) == 1:
            arr[key] = list(ctr[key].keys())[0] # assign the only region
        elif len(ctr[key]) > 1:
            max = 0
            _dict = ctr[key]
            _region = "Null"
            for subkey in _dict:
                if _dict[subkey] > max:
                    max = _dict[subkey]
                    _region = subkey
            arr[key] = _region
        elif len(ctr[key]) == 0:
            arr[key] = "Null_no_data"
    county["Region"] = arr

    county.to_csv("./region_added_county_final",sep=',',index=False)
plotContainers()


#show(fig)
