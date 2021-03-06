import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
from pandas import HDFStore
import CandleStick as cs
import datetime
import talib
import numpy
import pandas as pd

symbol = 'PODD'

hdf = HDFStore('data/daily.h5')

fulldf = hdf[symbol]
analysis = pd.DataFrame(index=fulldf.index)
analysis['atr'] = talib.ATR(numpy.asarray(fulldf['high']), numpy.asarray(fulldf['low']), numpy.asarray(fulldf['close']),
                            timeperiod=60)
analysis['atr_emr'] = talib.EMA(numpy.asarray(analysis['atr']), 60)

# access one symbol, it gives back a DataFrame
maindf = hdf[symbol][-80:]
print(maindf.index.name)
maindf.index.name = 'date'

# print out candlestick debug info
file = open(symbol + "_candle.txt", "w")
for i, row in maindf.iterrows():
    c = cs.CandleStick.fromRow(row)
    c.associate_date(i)
    print(analysis['atr_emr'][i])
    print(c.describe2())
    file.write(c.describe2())
    file.write(" | B/ATR " + "{:0.1f}".format(c.body / analysis['atr_emr'][i]))
    file.write("\n")

file.close()

# Reset the index to remove Date column from index
df = maindf.reset_index()

df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
df["date"] = df["date"].apply(mdates.date2num)

f1 = plt.subplot2grid((6, 4), (1, 0), rowspan=6, colspan=4, facecolor='#ffffff')
candlestick_ohlc(f1, df.values, width=.6, colorup='#53c156', colordown='#ff1717')
f1.xaxis_date()
f1.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))

plt.xticks(rotation=45)
plt.ylabel(symbol)
plt.xlabel('Date')

dt = datetime.datetime(2018, 4, 4)
for i, row in df.iterrows():
    tt = mdates.num2date(row['date'])
    f1.annotate(tt.strftime("%#d"), xy=(tt, row['high'] * 1.002))


plt.show()
