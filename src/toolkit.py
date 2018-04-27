from alpha_vantage.timeseries import TimeSeries
import time
from pandas import HDFStore
import numpy
import pandas as pd
import os
from datetime import datetime, timedelta
from pytz import timezone


class Bootup:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.normpath(os.path.join(self.base_path, '..', 'data'))
        self.data_file = os.path.normpath(os.path.join(self.data_path, 'daily.h5'))
        self.meta_file = os.path.normpath(os.path.join(self.data_path, 'meta.h5'))
        print('boot up base path:' + self.base_path)
        print('boot up data path:' + self.data_path)
        print('boot up data file:' + self.data_file)
        print('boot up meta_file:' + self.meta_file)


class AlphaVantageData:
    def __init__(self, data_store_file):
        print('AlphaVantageData init')
        self.data_store_file = data_store_file
        self.max_gap_to_cover = 50
        self.time_series = TimeSeries(key='EI7H5JUGQ20Q3GDK', output_format='pandas')

    def incremental_update(self):
        print('AlphaVantageData incremental update')
        symbols = self.all_symbols_in_store()
        data_store = HDFStore(self.data_store_file, mode='r')

        symbols_to_increment = []
        for s in symbols:
            lastrowindex = data_store[s].tail(1).index
            if lastrowindex > datetime.today() - timedelta(days=self.max_gap_to_cover):
                symbols_to_increment.append(s)
        print("incremental_update number of symbols:" + str(len(symbols_to_increment)))
        data_store.close()

        success_download_count = 0
        up_to_today_count = 0
        for symbol in symbols_to_increment:
            data, meta_data = self.get_daily_adjusted(symbol, 'compact')
            self.merge_and_add_to_store(symbol, data)
            print("complete download incremental data of:" + symbol)
            success_download_count += 1
            if data.tail(1).index.date == datetime.now(timezone('US/Eastern')).date():
                up_to_today_count += 1
            time.sleep(1)

        self.audit()
        print('AlphaVantageData incremental update fully completed')
        print('Total symbols in store:' + str(len(symbols)))
        print('Symbol qualify for increment:' + str(len(symbols_to_increment)))
        print('success_download_count:' + str(success_download_count))
        print('up_to_today_count:' + str(up_to_today_count))

    def merge_and_add_to_store(self, symbol, data):
        print('AlphaVantageData merge_and_add_to_store')
        symbol = self.cleanse_symbol(symbol)
        data_store = HDFStore(self.data_store_file, mode='a')
        existing_df = data_store[symbol]
        bigdata = existing_df.append(data)
        print(existing_df.shape)
        print(data.shape)
        print(bigdata.shape)

        # then merge
        bigdata = bigdata[~bigdata.index.duplicated(keep='last')]
        print('after merge')
        data_store[symbol] = bigdata
        print('AlphaVantageData add_to_store added:' + symbol)
        print(bigdata.shape)
        data_store.close()

    def add_to_store(self, symbol, data):
        print('AlphaVantageData add_to_store')
        symbol = self.cleanse_symbol(symbol)
        data_store = HDFStore(self.data_store_file, mode='a')
        data_store[symbol] = data
        print('AlphaVantageData add_to_store added:' + symbol + ',count: ' + str(data.count))
        data_store.close()

    def all_symbols_in_store(self):
        print('AlphaVantageData all_symbols_in_store')
        data_store = HDFStore(self.data_store_file, mode='r')
        symbols = []
        for symbol in data_store.keys():
            symbols.append(symbol.strip('/'))
        data_store.close()
        print('Total number of symbols in data store:' + str(len(symbols)))
        return symbols

    def audit(self):
        # make sure all symbols in store has data
        # return True if all passed audit
        print('AlphaVantageData audit')
        data_store = HDFStore(self.data_store_file, mode='r')
        for symbol in data_store.keys():
            df = data_store[symbol.strip('/')]
            print(df.shape)
            print(df.tail(1).index)
            if df.count == 0:
                return False
        data_store.close()
        print('no error found in audit')
        return True

    @classmethod
    def cleanse_symbol(self, symbol):
        symbol = symbol.strip().upper()
        if len(symbol) < 1:
            raise ValueError('Invalid symbol')
        return symbol

    def get_daily_adjusted(self, symbol, outputsize):
        # this method only download, do NOT deal with data store
        symbol = self.cleanse_symbol(symbol)
        df, meta_data = self.time_series.get_daily_adjusted(symbol=symbol, outputsize=outputsize)

        if df.count == 0:
            raise ValueError('Data empty:' + symbol)

        print(df.index.name)
        print(df.columns.values)

        if df.index.name == 'Date' or df.index.name == 'date':
            df.index.name = 'date'
        else:
            raise ValueError('DataFrame index name wrong:' + df.index.name)

        if 'open' in df.columns and 'high' in df.columns and 'low' in df.columns and 'close' in df.columns \
                and 'adjusted close' in df.columns and 'volume' in df.columns:
            print('column names are good')
        elif '1. open' in df.columns and '2. high' in df.columns and '3. low' in df.columns and '4. close' in df.columns \
                and '5. adjusted close' in df.columns and '6. volume' in df.columns:
            print('column names renamed')
            df.rename(columns={'1. open': 'open',
                               '2. high': 'high',
                               '3. low': 'low',
                               '4. close': 'close',
                               '5. adjusted close': 'adjusted close',
                               '6. volume': 'volume'
                               }, inplace=True)
        else:
            raise ValueError('DataFrame column names wrong')

        df = df.filter(items=['open', 'high', 'low', 'close', 'adjusted close', 'volume'])
        df.index = pd.to_datetime(df.index)
        return df, meta_data


# print two files, one for all candles
# one for selected only
def print_candle_debug(symbol):
    fulldf = HDFStore('data/daily.h5')[symbol]
    analysis = pd.DataFrame(index=fulldf.index)
    analysis['atr'] = talib.ATR(numpy.asarray(fulldf['high']), numpy.asarray(fulldf['low']),
                                numpy.asarray(fulldf['close']),
                                timeperiod=50)
    analysis['atr_emr'] = talib.EMA(numpy.asarray(analysis['atr']), 50)

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


def alpha_vantage_daily_full(symbol):
    return alpha_vantage(symbol, 'full')


def alpha_vantage_daily_compact(symbol):
    return alpha_vantage(symbol, 'compact')


def alpha_vantage(symbol, outputsize):
    # alpha_vantage's column name has index at the beginning, like "1. open"
    # so rename it
    symbol = symbol.strip()
    ts = TimeSeries(key='EI7H5JUGQ20Q3GDK', output_format='pandas')
    print(ts.retries)
    print(symbol)

    data, meta_data = ts.get_daily_adjusted(symbol=symbol, outputsize=outputsize)
    data.rename(columns={'1. open': 'open',
                         '2. high': 'high',
                         '3. low': 'low',
                         '4. close': 'close',
                         '5. adjusted close': 'adjusted close',
                         '6. volume': 'volume'
                         }, inplace=True)
    data.index = pd.to_datetime(data.index)
    return data, meta_data


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

    fulldf["v_vs_short"] = fulldf['volume'] / fulldf[Metrics.VOL_SHORT_MA_PREV]
    fulldf["v_vs_long"] = fulldf['volume'] / fulldf[Metrics.VOL_LONG_MA_PREV]

    return fulldf
