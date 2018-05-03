from pandas import HDFStore
from toolkit import Metrics
import toolkit
from toolkit import CandleStick


def run_one(symbol, hdf):
    fulldf = hdf[symbol]

    date_range_eval = toolkit.DateRangeEval()
    # date_range_eval.one_day('2018-04-30')
    date_range_eval.set_start_end('2018-05-01', '2018-05-02')

    toolkit.add_analysis_data(fulldf)

    for i, row in fulldf.iterrows():
        if date_range_eval.isin(i) and toolkit.yang_candle_filter_vol(row):
            file_s = open("../candledata/" + symbol + "_candle_volselected.txt", "a")
            c = CandleStick.fromRow(row)
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
    try:
        run_one(symbol.strip('/'), hdf)
    except:
        print('Error on ' + symbol)
hdf.close()
