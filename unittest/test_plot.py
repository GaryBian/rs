import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
from pandas import HDFStore, DataFrame

from datetime import datetime

hdf = HDFStore('../data/daily.h5')

# access one symbol, it gives back a DataFrame
df = hdf['SPX']

trace = go.Candlestick(x=df.Date,
                       open=df.Open,
                       high=df.High,
                       low=df.Low,
                       close=df.Close)
data = [trace]
py.iplot(data, filename='simple_candlestick')
