import pandas as pd
from pandas import HDFStore, DataFrame
import stockstats
from stockstats import StockDataFrame

hdf = HDFStore('daily.h5')

start_date = '2015-09-01'
h1 = hdf['BABA'].filter(items=['open', 'high', 'low', 'adjusted close', 'volume'])

h1.rename(columns={'adjusted close': 'close'}, inplace=True)

h_spx = h1[h1.index >= start_date]

picked_min_date = h_spx.index.min()
print(h_spx.loc[picked_min_date])

print(h_spx.head())

print(h_spx.tail())

print(h_spx.shape)

stock = StockDataFrame.retype(h_spx)

m = stock['macd']
print(m)

print(stock['atr_30'])


print(h_spx['volume'].rolling(window=15).mean())
