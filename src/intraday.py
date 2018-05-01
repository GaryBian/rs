import toolkit
import datetime
from pandas import HDFStore


def run_one(symbol, hdf):
    fulldf = hdf[symbol]
    toolkit.add_analysis_data(fulldf)

    date_range_eval = toolkit.DateRangeEval()
    date_range_eval.set_start_end('2015-01-12', '2015-01-14')
    vol_eval = toolkit.VolumeEval()
    for i, row in fulldf.iterrows():
        vol_eval.set(row)
        print(row)
        print(i)
        print(date_range_eval.isin(i))


boot = toolkit.Bootup()
hdf = HDFStore(boot.data_file)
keys = hdf.keys()
for symbol in keys:
    run_one(symbol.strip('/'), hdf)
