import toolkit1
from pandas import HDFStore
import CandleStick as cs
import datetime
import talib
import numpy
import pandas as pd
from analysis import Metrics


def run_one(symbol, hdf):
    fulldf = hdf[symbol]
    print(symbol)
    print(fulldf.tail(1).index)


hdf = HDFStore('data/daily.h5')
keys = hdf.keys()
for symbol in keys:
    run_one(symbol.strip('/'), hdf)
