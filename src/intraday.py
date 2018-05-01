import toolkit
import datetime
from pandas import HDFStore


def run_one(symbol, hdf):
    fulldf = hdf[symbol]
    toolkit.add_analysis_data(fulldf)

    date_range_eval = toolkit.DateRangeEval()
    date_range_eval.one_day('2018-04-30')
    vol_eval = toolkit.VolumeEval()
    for i, row in fulldf.iterrows():
        vol_eval.set(row)
        # print(row)
        # print(i)
        if date_range_eval.isin(i):
            print(i)
            print(symbol)


boot = toolkit.Bootup()
hdf = HDFStore(boot.data_file)
keys = hdf.keys()
for symbol in keys:
    run_one(symbol.strip('/'), hdf)
