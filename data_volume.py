from pandas import HDFStore
import talib
import numpy
import pandas as pd

symbol = 'NVDA'

hdf = HDFStore('data/daily.h5')

fulldf = hdf[symbol]
analysis = pd.DataFrame(index=fulldf.index)

analysis['volume_sma5'] = talib.SMA(numpy.asarray(fulldf['volume']), 5)

print(analysis)