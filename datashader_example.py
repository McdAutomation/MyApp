import datashader as ds
import datashader.transfer_functions as tf
from datashader.utils import export_image
import pandas as pd

df = pd.read_csv(r"./data/store_data.csv",sep="\t")

cvs = ds.Canvas(plot_width=800, plot_height=800)
agg = cvs.points(df, 'Latitude', 'Longitude', ds.mean('NatlStrNumber'))
img = tf.shade(agg, cmap=['white', 'black'], how='log')

export_image(img,"image")
