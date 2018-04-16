import talib
import pandas as pd
from pandas import HDFStore, DataFrame
import numpy

hdf = HDFStore('../data/daily.h5')
h1 = hdf['NVDA']

print(list(h1.columns.values))

# list of functions

print(h1['close'].describe())

# This will align the result's index (date) with the input data
analysis = pd.DataFrame(index=h1.index)

open = numpy.asarray(h1['open'], dtype=float)
high = numpy.asarray(h1['high'], dtype=float)
low = numpy.asarray(h1['low'], dtype=float)
close = numpy.asarray(h1['close'], dtype=float)

analysis['CDLTRISTAR'] = talib.CDLTRISTAR(open, high, low, close)
analysis['CDLINVERTEDHAMMER '] = talib.CDLINVERTEDHAMMER(open, high, low, close)
analysis['CDLCLOSINGMARUBOZU'] = talib.CDLCLOSINGMARUBOZU(open, high, low, close)

print(analysis)
