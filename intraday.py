from alpha_vantage.timeseries import TimeSeries
from pandas import HDFStore
import time
import pandas

# Get all symbols in meta.h5 and get data from alpha_vantage

# Standard format
# open
# high
# low
# nonadj close
# close
# volume


ts = TimeSeries(key='EI7H5JUGQ20Q3GDK', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='TSLA', interval='5min', outputsize='compact')

print(data)
print(meta_data)





data, meta_data = ts.get_daily(symbol='TSLA', outputsize='compact')

print(data)
print(meta_data)


data, meta_data = ts.get_daily_adjusted(symbol='TSLA', outputsize='compact')

print(data)
print(meta_data)
