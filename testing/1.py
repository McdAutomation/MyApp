import pandas as pd
import geopandas as gpd
from conversions import returnPandasDataFrame

county = pd.read_pickle('./test.pkl')
print(type(county.loc[0]['x']))
