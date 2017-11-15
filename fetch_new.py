from alpha_vantage.timeseries import TimeSeries
from pandas import HDFStore
import time

df_symbol = HDFStore('data/meta.h5')['Symbol']

ts = TimeSeries(key='EI7H5JUGQ20Q3GDK', output_format='pandas')
hdf_daily = HDFStore('data/daily.h5')

for i, row in df_symbol.iterrows():
    print(i, row['Symbol'])
    data, meta_data = ts.get_daily_adjusted(symbol=row['Symbol'], outputsize='full')
    hdf_daily[row['Symbol']] = data
    time.sleep(1)
