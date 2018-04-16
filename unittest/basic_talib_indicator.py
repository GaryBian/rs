import talib
import pandas as pd
from pandas import HDFStore, DataFrame
import numpy

hdf = HDFStore('../data/daily.h5')
h1 = hdf['SPX']

print(list(h1.columns.values))

# list of functions
print(talib.get_functions())

# dict of functions by group
print(talib.get_function_groups())

print(h1['close'].describe())

# This will align the result's index (date) with the input data
analysis = pd.DataFrame(index=h1.index)

sma = talib.EMA(numpy.asarray(h1['close']), 21)
analysis['ema8'] = talib.EMA(numpy.asarray(h1['close']), 8)
analysis['atr'] = talib.ATR(numpy.asarray(h1['high']), numpy.asarray(h1['low']), numpy.asarray(h1['close']),
                            timeperiod=20)

analysis['test1'] = '5'
print(sma)
