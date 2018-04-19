import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc
import pandas as pd
from pandas import HDFStore

import mpl_finance

hdf = HDFStore('../data/daily.h5')

# access one symbol, it gives back a DataFrame
df = hdf['TSLA'][-50:]

# Reset the index to remove Date column from index
df = df.reset_index()

df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
df["date"] = df["date"].apply(mdates.date2num)

f1 = plt.subplot2grid((6, 4), (1, 0), rowspan=6, colspan=4, facecolor='#07000d')
candlestick_ohlc(f1, df.values, width=.6, colorup='#53c156', colordown='#ff1717')
f1.xaxis_date()
f1.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M:%S'))

plt.xticks(rotation=45)
plt.ylabel('Stock Price')
plt.xlabel('Date Hours:Minutes')
plt.show()
