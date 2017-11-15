from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from pandas import HDFStore, DataFrame

ts = TimeSeries(key='EI7H5JUGQ20Q3GDK', output_format='pandas')
hdf = HDFStore('daily.h5')

# slist = ['SPX', 'ADBE', 'BABA', 'TSLA', 'TXN']
# slist = ['XLF', 'XLE', 'SMH']
slist = ['RHT']

for s in slist:
    data, meta_data = ts.get_daily_adjusted(symbol=s, outputsize='full')
    hdf[s] = data
