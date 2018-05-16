import toolkit
from pandas import HDFStore
import suite
import datetime
from pytz import timezone
import os

combo = suite.ComboBasic()
combo.date_selector = toolkit.DateSelector('2018-05-14', '2018-06-10')

boot = toolkit.Bootup()
run_label = boot.start_est_time.strftime("%Y%m%d%H%M")
print("select run:" + run_label)
os.makedirs("../candledata/" + run_label + "/")

data_file = boot.base_path + '/../tg/tg_data.h5'
hdf = HDFStore(data_file, mode='r')
keys = hdf.keys()
hdf.close()

for symbol in keys:
    symbol = symbol.strip('/')

    hdf = HDFStore(boot.base_path + '/../tg/tg_data.h5', mode='r')
    df = hdf[symbol]
    hdf.close()
    print("working on:" + symbol)
    df = toolkit.DataView.add_analysis_data(df)
    for i, row in df.iterrows():
        if combo.query(i, row):
            print(i)
            toolkit.DataView.write_query_result(symbol, i, row, run_label)
