from alpha_vantage.timeseries import TimeSeries
import time
from pandas import HDFStore
import CandleStick as cs
import talib
import numpy
import pandas as pd
from analysis import Metrics


# print two files, one for all candles
# one for selected only
def print_candle_debug(symbol):
    fulldf = HDFStore('data/daily.h5')[symbol]
    analysis = pd.DataFrame(index=fulldf.index)
    analysis['atr'] = talib.ATR(numpy.asarray(fulldf['high']), numpy.asarray(fulldf['low']),
                                numpy.asarray(fulldf['close']),
                                timeperiod=60)
    analysis['atr_emr'] = talib.EMA(numpy.asarray(analysis['atr']), 60)

    # print out candlestick debug info
    file = open(symbol + "_candle.txt", "w")
    file_s = open(symbol + "_candle_selected.txt", "w")
    for i, row in fulldf.iterrows():
        c = cs.CandleStick.fromRow(row)
        c.associate_date(i)
        print(analysis['atr_emr'][i])
        print(c.describe2())
        file.write(c.describe2())
        file.write(" | B/ATR " + "{:0.1f}".format(c.body / analysis['atr_emr'][i]))
        file.write("\n")

        if yang_candle_filter(c, analysis['atr_emr'][i]):
            file_s.write(c.describe2())
            file_s.write(" | B/ATR " + "{:0.1f}".format(c.body / analysis['atr_emr'][i]))
            file_s.write("\n")

    file.close()
    file_s.close()


def download_alpha_vantage(symbol):
    # alpha_vantage's column name has index at the beginning, like "1. open"
    # so rename it
    symbol = symbol.strip()
    ts = TimeSeries(key='EI7H5JUGQ20Q3GDK', output_format='pandas')
    hdf_daily = HDFStore('data/daily.h5')
    print(symbol)

    data, meta_data = ts.get_daily_adjusted(symbol=symbol, outputsize='full')
    data.rename(columns={'1. open': 'open',
                         '2. high': 'high',
                         '3. low': 'low',
                         '4. close': 'close',
                         '5. adjusted close': 'adjusted close',
                         '6. volume': 'volume'
                         }, inplace=True)

    data.index = pd.to_datetime(data.index)
    hdf_daily[symbol] = data
    time.sleep(1)


def yang_candle_filter(candle, atr):
    head_to_body_ratio_max = 0.2
    tail_to_body_ratio_max = 0.2
    body_atr_ratio_min = 1.5

    if candle.is_bull \
            and candle.head_to_body_ratio < head_to_body_ratio_max \
            and candle.tail_to_body_ratio < tail_to_body_ratio_max \
            and candle.body / atr > body_atr_ratio_min:
        return True

    return False


def yang_candle_filter_vol(row):
    candle = cs.CandleStick.fromRow(row)

    head_to_body_ratio_max = 0.2
    tail_to_body_ratio_max = 0.2
    body_atr_ratio_min = 1.5
    times_short_vol = 2.0
    times_long_vol = 1.5

    if candle.is_bull and (candle.head_to_body_ratio < head_to_body_ratio_max) and (
            candle.tail_to_body_ratio < tail_to_body_ratio_max) and (
            candle.body / row[Metrics.ATR_SMOOTH] > body_atr_ratio_min) and (
            (row['volume'] > row[Metrics.VOL_SHORT_MA_PREV] * times_short_vol) or (
            row['volume'] > row[Metrics.VOL_LONG_MA_PREV] * times_long_vol)):
        return True

    return False


def add_analysis_data(fulldf):
    # shift(1) is to get previous
    # shift(-1) is to get next row

    fulldf[Metrics.VOL_SHORT_MA] = talib.SMA(numpy.asarray(fulldf['volume']), 5)
    fulldf[Metrics.VOL_SHORT_MA_PREV] = fulldf[Metrics.VOL_SHORT_MA].shift(1)
    fulldf[Metrics.VOL_LONG_MA] = talib.EMA(numpy.asarray(fulldf['volume']), 50)
    fulldf[Metrics.VOL_LONG_MA_PREV] = fulldf[Metrics.VOL_LONG_MA].shift(1)

    fulldf[Metrics.MA8] = talib.EMA(numpy.asarray(fulldf['close']), 8)
    fulldf[Metrics.MA21] = talib.EMA(numpy.asarray(fulldf['close']), 21)
    fulldf[Metrics.MA200] = talib.EMA(numpy.asarray(fulldf['close']), 200)

    fulldf[Metrics.CLOSE_PREV] = fulldf['close'].shift(1)
    fulldf[Metrics.CHANGE] = fulldf['close'] - fulldf[Metrics.CLOSE_PREV]
    fulldf[Metrics.CHANGE_PCT] = fulldf['close'].pct_change()

    fulldf[Metrics.ATR] = talib.ATR(numpy.asarray(fulldf['high']), numpy.asarray(fulldf['low']),
                                    numpy.asarray(fulldf['close']),
                                    timeperiod=50)
    fulldf[Metrics.ATR_SMOOTH] = talib.EMA(numpy.asarray(fulldf[Metrics.ATR]), 50)

    return fulldf
