import toolkit
from pandas import HDFStore
import suite
import os
import multiprocessing


def worker(symbol, combo, boot, run_label):
    """thread worker function"""
    # print('worker ' + symbol)
    symbol = symbol.strip('/')

    hdf = HDFStore(boot.data_read_only_file, mode='r')
    df = hdf[symbol]
    hdf.close()
    print("working on:" + symbol)
    df = toolkit.DataView.add_analysis_data(df)
    for i, row in df.iterrows():
        if combo.query(i, row):
            print(i)
            toolkit.DataView.write_query_result(symbol, i, row, run_label)
    return


if __name__ == '__main__':
    combo = suite.ComboBasic()
    combo.date_selector = toolkit.DateSelector('2018-05-01', '2018-06-10')

    boot = toolkit.Bootup()
    run_label = boot.start_est_time.strftime("%Y%m%d%H%M")
    print("select run:" + run_label)
    os.makedirs("../candledata/" + run_label + "/")

    hdf = HDFStore(boot.data_read_only_file, mode='r')
    keys = hdf.keys()
    hdf.close()

    jobs = []
    for i in keys:
        p = multiprocessing.Process(target=worker, args=(i, combo, boot, run_label))
        jobs.append(p)
        p.start()
