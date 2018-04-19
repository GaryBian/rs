import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
from pandas import HDFStore
from matplotlib import style
import CandleStick as cs

print(style.available)
style.use('fast')

hdf = HDFStore('data/daily.h5')

# access one symbol, it gives back a DataFrame
maindf = hdf['TSLA'][-70:]

#print out candlestick debug info
for i, row in maindf.iterrows():
    print(i)
    c = cs.CandleStick.fromRow(maindf.loc['2018-2-14'])
    c.associate_date(i)
    print(c.describe2())
    print(c)




# Reset the index to remove Date column from index
df = maindf.reset_index()

df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
df["date"] = df["date"].apply(mdates.date2num)

f1 = plt.subplot2grid((6, 4), (1, 0), rowspan=6, colspan=4, facecolor='#07000d')
candlestick_ohlc(f1, df.values, width=.6, colorup='#53c156', colordown='#ff1717')
f1.xaxis_date()
f1.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))

plt.xticks(rotation=45)
plt.ylabel('Stock Price')
plt.xlabel('Date Hours:Minutes')
plt.show()
