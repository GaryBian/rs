from alpha_vantage.timeseries import TimeSeries
from pandas import HDFStore
import time
import pandas
import toolkit1

# Get all symbols in meta.h5 and get data from alpha_vantage

# Standard format
# open
# high
# low
# nonadj close
# close
# volume


# toolkit.alpha_vantage_daily_full('TSLA')

b = toolkit1.Bootup()
print(b)
