from alpha_vantage.timeseries import TimeSeries
from pandas import HDFStore
import time

# Get all symbols in meta.h5 and get data from alpha_vantage

# Standard format
# open
# high
# low
# nonadj close
# close
# volume

df_symbol = HDFStore('data/meta.h5')['Symbol']

ts = TimeSeries(key='EI7H5JUGQ20Q3GDK', output_format='pandas')
hdf_daily = HDFStore('data/daily.h5')

for i, row in df_symbol.iterrows():
    print(i, row['Symbol'])
    data, meta_data = ts.get_daily_adjusted(symbol=row['Symbol'], outputsize='full')
    data.rename(columns={'1. open': 'open',
                         '2. high': 'high',
                         '3. low': 'low',
                         '4. close': 'nonadj close',
                         '5. adjusted close': 'close',
                         '6. volume': 'volume'
                         }, inplace=True)
    hdf_daily[row['Symbol']] = data
    time.sleep(1)

# alpha_vantage's column name has index at the beginning, like "1. open"
