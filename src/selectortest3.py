import toolkit
from pandas import HDFStore
import suite

combo = suite.ComboHighVolume()
combo.date_selector = toolkit.DateSelector('2018-05-02', '2018-05-02')

boot = toolkit.Bootup()
hdf = HDFStore(boot.data_read_only_file)
keys = hdf.keys()
for symbol in keys:
    symbol = symbol.strip('/')
    df = hdf[symbol]
    toolkit.add_analysis_data(df)

    for i, row in df.iterrows():
        if combo.query(i, row):
            print(symbol)
            print(i)
