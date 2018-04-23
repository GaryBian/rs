from pandas import HDFStore
import talib
import numpy
import pandas as pd

symbol = 'PRAA'

hdf = HDFStore('data/daily.h5')

fulldf = hdf[symbol]
analysis = pd.DataFrame(index=fulldf.index)

# shift(1) is to get previous
# shift(-1) is to get next row
analysis['volume'] = fulldf['volume']

analysis['volume_sma5'] = talib.SMA(numpy.asarray(fulldf['volume']), 5)
analysis['volume_sma5_prev'] = analysis['volume_sma5'].shift(1)
analysis['volume_ema50'] = talib.EMA(numpy.asarray(fulldf['volume']), 50)
analysis['volume_ema50_prev'] = analysis['volume_ema50'].shift(1)

analysis['close_ema8'] = talib.EMA(numpy.asarray(fulldf['close']), 8)
analysis['close_ema21'] = talib.EMA(numpy.asarray(fulldf['close']), 21)
analysis['close_ema200'] = talib.EMA(numpy.asarray(fulldf['close']), 200)

analysis['close'] = fulldf['close']
analysis['close_prev'] = fulldf['close'].shift(1)
analysis['chg_calc'] = analysis['close'] / analysis['close_prev'] - 1.0
analysis['close_pct_change'] = fulldf['close'].pct_change()

analysis['atr'] = talib.ATR(numpy.asarray(fulldf['high']), numpy.asarray(fulldf['low']), numpy.asarray(fulldf['close']),
                            timeperiod=60)
analysis['atr_ema60'] = talib.EMA(numpy.asarray(analysis['atr']), 60)

analysis['chg_calc_vs_atr'] = (analysis['close'] - analysis['close_prev']) / analysis['atr_ema60']

print(analysis)
