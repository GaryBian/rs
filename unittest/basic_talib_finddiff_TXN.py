import talib
import pandas as pd
from pandas import HDFStore, DataFrame
import numpy

hdf = HDFStore('../data/daily.h5')
h1 = hdf['TXN']

print(list(h1.columns.values))
print(h1.tail())

# This will align the result's index (date) with the input data
analysis = pd.DataFrame(index=h1.index)

analysis['ema21'] = talib.EMA(numpy.asarray(h1['nonadj close']), 21)
analysis['ema8'] = talib.EMA(numpy.asarray(h1['nonadj close']), 8)
analysis['atr'] = talib.ATR(numpy.asarray(h1['high']), numpy.asarray(h1['low']), numpy.asarray(h1['nonadj close']),
                            timeperiod=100)

analysis['8-21diff'] = (analysis['ema8'] - analysis['ema21']) * 100.0 / analysis['atr']

analysis['volume'] = h1['volume']


print(analysis)
