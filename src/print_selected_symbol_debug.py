import toolkit
from pandas import HDFStore
import CandleStick as cs
import datetime
from analysis import Metrics


def run_one(symbol, hdf):
    df = hdf[symbol]
    df = toolkit.DataView.add_analysis_data(df)
    file_s = open("../candledata/" + symbol + "_candle_volselected.txt", "w")
    for i, row in df.iterrows():
        file_s.write(" |Date " + i.strftime('%Y-%m-%d'))
        file_s.write(" |Bull " + "{:0.1f}".format(row['candle_bull']))
        file_s.write(" |H/Body " + "{:0.1f}".format(row['candle_head_bi_body']))
        file_s.write(" |T/Body " + "{:0.1f}".format(row['candle_tail_bi_body']))

        file_s.write(" |B/ATR " + "{:0.1f}".format(row['candle_body_bi_atr']))
        file_s.write(" |V/SHORT " + "{:0.1f}".format(row['vol_bi_short_ma']))
        file_s.write(" |V/LONG " + "{:0.1f}".format(row['vol_bi_long_ma']))
        file_s.write(" |V/PREV " + "{:0.1f}".format(row['vol_bi_prev']))
        file_s.write("\n")
    file_s.close()


boot = toolkit.Bootup()
hdf = HDFStore(boot.data_read_only_file)

keys = hdf.keys()
for symbol in keys:
    run_one(symbol.strip('/'), hdf)
hdf.close()
