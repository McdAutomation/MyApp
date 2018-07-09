import pandas as pd
import geopandas as gpd
from conversions import returnPDS
import json

county = pd.read_pickle('./test.pkl')
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

def plotContainers():
    ctr = {}
    for i in range(10): #13893
        print(i)
        x = points.loc[i]['x']
        y = points.loc[i]['y']
        for j in range(3304):
            ##
            xArr = county.loc[j]['x']
            yArr = county.loc[j]['y']
            _inside = False
            size = len(xArr)

            l = size - 1
            for k in range(0, size):
                xi = xArr[k]
                yi = yArr[k]
                xj = xArr[l]
                yj = yArr[l]

                intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)

                if intersect:
                    _inside = not _inside
                l = k
            ##
            if inside:
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
