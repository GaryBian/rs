import toolkit1
from pandas import HDFStore
import CandleStick as cs
import datetime
import talib
import numpy
import pandas as pd
from analysis import Metrics


def run_one(symbol, hdf):
    fulldf = hdf[symbol]
    toolkit1.add_analysis_data(fulldf)
    file_s = open(symbol + "_candle_volselected.txt", "w")
    for i, row in fulldf.iterrows():
        if i > datetime.datetime(2016, 1, 1) and toolkit1.yang_candle_filter_vol(row):
            c = cs.CandleStick.fromRow(row)
            c.associate_date(i)
            file_s.write(c.describe2())
            file_s.write(" |B/ATR " + "{:0.1f}".format(c.body / row[Metrics.ATR_SMOOTH]))
            file_s.write(" |V/SHORT " + "{:0.1f}".format(row['volume'] / row[Metrics.VOL_SHORT_MA_PREV]))
            file_s.write(" |V/LONG " + "{:0.1f}".format(row['volume'] / row[Metrics.VOL_LONG_MA_PREV]))
            file_s.write("\n")

    file_s.close()


hdf = HDFStore('data/daily.h5')
keys = hdf.keys()
for symbol in keys:
    run_one(symbol.strip('/'), hdf)
