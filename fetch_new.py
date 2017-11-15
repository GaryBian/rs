from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from pandas import HDFStore, DataFrame

hdf_symbol = HDFStore('data/symbol.h5')

ts = TimeSeries(key='EI7H5JUGQ20Q3GDK', output_format='pandas')
hdf = HDFStore('daily.h5')

print(hdf_symbol)


# for index_val, series_val in hdf_symbol['Symbol'].iteritems():
#   print(index_val, series_val)
