from pandas import HDFStore
import CandleStick as cs
import talib
import numpy
import pandas as pd


def print_candle_debug(symbol):
    fulldf = HDFStore('data/daily.h5')[symbol]
    analysis = pd.DataFrame(index=fulldf.index)
    analysis['atr'] = talib.ATR(numpy.asarray(fulldf['high']), numpy.asarray(fulldf['low']),
                                numpy.asarray(fulldf['close']),
                                timeperiod=60)
    analysis['atr_emr'] = talib.EMA(numpy.asarray(analysis['atr']), 60)

    # print out candlestick debug info
    file = open(symbol + "_candle.txt", "w")
    for i, row in fulldf.iterrows():
        c = cs.CandleStick.fromRow(row)
        c.associate_date(i)
        print(analysis['atr_emr'][i])
        print(c.describe2())
        file.write(c.describe2())
        file.write(" | B/ATR " + "{:0.1f}".format(c.body / analysis['atr_emr'][i]))
        file.write("\n")

    file.close()
