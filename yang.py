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

bar = h_spx.loc['2015-10-02']

print(bar)

body = bar['close'] - bar['open']
head = bar['high'] - bar['close']
tail = bar['open'] - bar['low']
print(body / bar['open'])

print(body)
print(head)
print(tail)

print('gain', 100.0 * body / bar['open'])
print('head', 100.0 * head / body)
print('tail', 100.0 * tail / body)
print('volume', bar['volume'])
