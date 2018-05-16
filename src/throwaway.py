import toolkit
from pandas import HDFStore
import pandas as pd

boot = toolkit.Bootup()

data_file = boot.base_path + '/../tg/tg_data.h5'
hdf = HDFStore(data_file, mode='r')
keys = hdf.keys()
hdf.close()

for symbol in keys:
    symbol = symbol.strip('/')

    hdf = HDFStore(boot.base_path + '/../tg/tg_data.h5', mode='a')
    df = hdf[symbol]

    df['volume'] = df['volume'].astype('float64')

    # df[['open', 'close', 'volume']] = df[['open', 'close', 'volume']].apply(pd.to_numeric)
    hdf[symbol] = df
    hdf.close()
    print(symbol)

print('all converted')
