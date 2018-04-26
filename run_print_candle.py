import toolkit1
from pandas import HDFStore
import CandleStick as cs
import datetime
import talib
import numpy
import pandas as pd

# toolkit.print_candle_debug("TSLA")

# toolkit.print_candle_debug("AUMN")
# toolkit.print_candle_debug("ECOM")
# toolkit.print_candle_debug("PODD")
# toolkit.print_candle_debug("TXN")
# toolkit.print_candle_debug("MU")
# toolkit.print_candle_debug("SQ")

hdf = HDFStore('data/daily.h5')
keys = hdf.keys()
for symbol in keys:
    toolkit1.print_candle_debug(symbol.strip('/'))
