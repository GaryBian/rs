import toolkit1
from pandas import HDFStore
import CandleStick as cs
import datetime
import talib
import numpy
import pandas as pd
from analysis import Metrics
import toolkit


def run_one(symbol, hdf):
    fulldf = hdf[symbol]

    date_range_eval = toolkit.DateRangeEval()
    # date_range_eval.one_day('2018-04-30')
    date_range_eval.set_start_end('2018-04-20', '2018-04-30')

    toolkit.add_analysis_data(fulldf)

    for i, row in fulldf.iterrows():
        if date_range_eval.isin(i) and toolkit.yang_candle_filter_vol(row):
            file_s = open("../candledata/" + symbol + "_candle_volselected.txt", "a")
            c = cs.CandleStick.fromRow(row)
            c.associate_date(i)
            file_s.write(c.describe2())
            file_s.write(" |B/ATR " + "{:0.1f}".format(c.body / row[Metrics.ATR_SMOOTH]))
            file_s.write(" |V/SHORT " + "{:0.1f}".format(row['volume'] / row[Metrics.VOL_SHORT_MA_PREV]))
            file_s.write(" |V/LONG " + "{:0.1f}".format(row['volume'] / row[Metrics.VOL_LONG_MA_PREV]))
            file_s.write("\n")
            file_s.close()


boot = toolkit.Bootup()
hdf = HDFStore(boot.data_file)
keys = hdf.keys()
for symbol in keys:
    run_one(symbol.strip('/'), hdf)
hdf.close()
