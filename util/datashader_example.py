import datashader as ds
import datashader.transfer_functions as tf
from datashader.utils import export_image
import pandas as pd

df = pd.read_csv(r"./data/store_data.csv",sep="\t")

cvs = ds.Canvas(plot_width=800, plot_height=800)
agg = cvs.points(df, 'Longitude', 'Latitude', ds.mean('NatlStrNumber'))
img = tf.shade(agg, cmap=['lightblue', 'darkblue'],color_key=['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#999999', '#66c2a5', '#fc8d62', '#8da0cb', '#a6d854', '#ffd92f', '#e5c494', '#ffffb3', '#fb8072', '#fdb462', '#fccde5', '#d9d9d9', '#ccebc5', '#ffed6f'],
               how='eq_hist',alpha=255, min_alpha=40)

export_image(img,"image")
