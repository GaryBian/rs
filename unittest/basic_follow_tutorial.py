import talib
import pandas as pd
from pandas import HDFStore
import numpy

hdf = HDFStore('../data/daily.h5')
h1 = hdf['SPX']
print(h1.index)

print(h1.columns)

ts = h1['close'][-10:]

print(type(ts))

print(ts)

# loc for label-based indexing
# iloc for positional indexing.
print(h1.loc['2017-11-01': '2017-12-31'])

print(h1.iloc[[22, 43], [0, 2]])

sample = h1.sample(20)
print(sample)

h1['diff'] = h1.open - h1.close

print(h1)

del h1['diff']

print(h1)

print(h1.values)

print(h1.T)

print(h1.describe())

monthly_aapl = h1.resample('M').mean()
print(monthly_aapl)

print(h1[h1.volume > 5000000000])

daily_close = h1.close
print(daily_close.pct_change())