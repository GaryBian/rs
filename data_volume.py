from pandas import HDFStore
import talib
import numpy
import pandas as pd
from analysis import Metrics
import toolkit

symbol = 'MU'

hdf = HDFStore('data/daily.h5')

fulldf = hdf[symbol]

toolkit.add_analysis_data(fulldf)
