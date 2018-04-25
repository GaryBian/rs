from pandas import HDFStore
import talib
import numpy
import pandas as pd
from analysis import Metrics
import toolkit


def full_quote(symbol):
    symbol = symbol.strip().upper()
    if len(symbol) < 1:
        raise ValueError('Invalid symbol')

    store = HDFStore('data/daily.h5')

    # check whether key exists in store
    if symbol in store:
        print(symbol + ' in store')
        # get last row
        lastrowindex = store[symbol].tail(1).index
    else:
        print(symbol + ' not in store')
        get_both_merge(symbol)


def get_both_merge(symbol):
    data_full, meta_full = toolkit.alpha_vantage_daily_full(symbol)
    data_compact, meta_compact = toolkit.alpha_vantage_daily_compact(symbol)
    bigdata = data_full.append(data_compact)
    print(data_full.shape)
    print(data_compact.shape)
    print(bigdata.shape)

    # then merge
    bigdata = bigdata[~bigdata.index.duplicated(keep='first')]

    print('after merge')
    print(bigdata.shape)

    print(bigdata)
    return bigdata


full_quote('akam')

full_quote('AKAM')
