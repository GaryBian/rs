import talib
from alpha_vantage.timeseries import TimeSeries
import time
from pandas import HDFStore
import numpy
import pandas as pd
import os
from datetime import datetime, timedelta
from pytz import timezone
import glob
from shutil import copyfile


class CandleStick:

    def __init__(self, open, high, low, close):
        self.open = open
        self.high = high
        self.low = low
        self.close = close

        if self.open > self.close:
            self.is_bull = False
            self.body_top = self.open
            self.body_bottom = self.close
            self.body = self.close
        else:
            self.is_bull = True
            self.body_top = self.close
            self.body_bottom = self.open

        self.body = self.body_top - self.body_bottom
        if self.body < 0.01:
            self.body = 0.01
        self.head = self.high - self.body_top
        self.tail = self.body_bottom - self.low

        self.head_to_body_ratio = self.head / self.body
        self.tail_to_body_ratio = self.tail / self.body

    def describe(self):
        if (self.is_bull):
            print("BULL")
        else:
            print("BEAR")
        print("body:" + str(self.body))
        print("change %:" + str((self.close - self.open) * 100.0 / self.open))
        print("head_to_body_ratio %:" + str(self.head_to_body_ratio * 100.0))
        print("tail_to_body_ratio %:" + str(self.tail_to_body_ratio * 100.0))
        print(self.date.strftime('%Y-%m-%d'))

    def describe2(self):
        d = {}
        d['bullflag'] = ("Bull" if self.is_bull else "Bear")
        d['body'] = "{:0.2f}".format(self.body)
        d['close'] = self.close
        d['date'] = self.date.strftime('%Y-%m-%d')
        d['head_to_body_ratio'] = "{:0.0f}".format(self.head_to_body_ratio * 100.0)
        d['tail_to_body_ratio'] = "{:0.0f}".format(self.tail_to_body_ratio * 100.0)
        d['change'] = "{:0.1f}".format((self.close - self.open) * 100.0 / self.open)
        s = "{date} | {bullflag} | {close} / {change}% | HEAD {head_to_body_ratio}% | TAIL {tail_to_body_ratio}%".format(
            **d)

        return s

    def associate_date(self, date):
        self.date = date

    @classmethod
    def fromRow(cls, row):
        return cls(row.open, row.high, row.low, row.close)


class Bootup:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.normpath(os.path.join(self.base_path, '..', 'data'))
        self.data_read_path = os.path.normpath(os.path.join(self.base_path, '..', 'dataread'))
        self.data_file = os.path.normpath(os.path.join(self.data_path, 'daily.h5'))
        self.meta_file = os.path.normpath(os.path.join(self.data_path, 'meta.h5'))
        self.data_read_only_file = os.path.normpath(os.path.join(self.data_read_path, 'readonly.h5'))
        print('boot up base path:' + self.base_path)
        print('boot up data path:' + self.data_path)
        print('boot up data file:' + self.data_file)
        print('boot up meta_file:' + self.meta_file)


class AlphaVantageData:
    def __init__(self, boot):
        print('AlphaVantageData init')
        self.data_store_file = boot.data_file
        self.data_read_only_file = boot.data_read_only_file
        self.max_gap_to_cover = 50
        self.seconds_between_api_call = 3
        self.time_series = TimeSeries(key='EI7H5JUGQ20Q3GDK', retries=2, output_format='pandas')

    def symbols_to_increment(self):
        print('AlphaVantageData symbols_to_increment')
        symbols = self.all_symbols_in_store()
        data_store = HDFStore(self.data_store_file, mode='r')
        symbols_to_increment = []
        for s in symbols:
            lastrowindex = data_store[s].tail(1).index
            if lastrowindex > datetime.today() - timedelta(days=self.max_gap_to_cover):
                symbols_to_increment.append(s)
            else:
                print(s)
        print("incremental_update number of symbols:" + str(len(symbols_to_increment)))
        data_store.close()
        return symbols_to_increment

    def incremental_update(self):
        print('AlphaVantageData incremental update')
        symbols = self.all_symbols_in_store()
        data_store = HDFStore(self.data_store_file, mode='r')

        symbols_to_increment = []
        for s in symbols:
            lastrowindex = data_store[s].tail(1).index
            if lastrowindex > datetime.today() - timedelta(days=self.max_gap_to_cover):
                symbols_to_increment.append(s)
            else:
                print(s)
        print("incremental_update number of symbols:" + str(len(symbols_to_increment)))
        data_store.close()

        success_download_count = 0
        up_to_today_count = 0
        copy_read_only_per_count = 500
        for symbol in symbols_to_increment:
            time.sleep(self.seconds_between_api_call)
            try:
                data, meta_data = self.get_daily_adjusted(symbol, 'compact')
                self.merge_and_add_to_store(symbol, data)
                print("complete download incremental data of:" + symbol)
                success_download_count += 1
                if data.tail(1).index.date == datetime.now(timezone('US/Eastern')).date():
                    up_to_today_count += 1
                if success_download_count % copy_read_only_per_count == 0:
                    print("copy to read only location")
                    copyfile(self.data_store_file, self.data_read_only_file)
            except:
                print("Error working on: " + symbol)
        copyfile(self.data_store_file, self.data_read_only_file)

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


class VolumeEval:
    def __init__(self, ratio_to_short=2.0, ratio_to_long=1.5):
        print('VolumeEval init')
        self.ratio_to_short = ratio_to_short
        self.ratio_to_long = ratio_to_long
        #    (row['volume'] > row[Metrics.VOL_SHORT_MA_PREV] * times_short_vol) or (
        #
        #           row['volume'] > row[Metrics.VOL_LONG_MA_PREV] * times_long_vol)):

    # verify the needed data exists
    def set(self, row):
        if 'volume' not in row.index:
            raise ValueError('VolumeEval missing required data column ' + 'volume')

        if Metrics.VOL_SHORT_MA_PREV not in row.index:
            raise ValueError('VolumeEval missing required data column ' + Metrics.VOL_SHORT_MA_PREV)

        if Metrics.VOL_LONG_MA_PREV not in row.index:
            raise ValueError('VolumeEval missing required data column ' + Metrics.VOL_LONG_MA_PREV)

        self.volume = row['volume']
        self.short_ma = row[Metrics.VOL_SHORT_MA_PREV]
        self.long_ma = row[Metrics.VOL_LONG_MA_PREV]


class DateRangeEval:
    def __init__(self):
        print('DateRangeEval')

    def set_start_end(self, start_date, end_date):
        # start_date, end_date needs to be in format 2015-10-20
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')

    def one_day(self, start_date):
        self.set_start_end(start_date, start_date)

    def isin(self, d):
        if d >= self.start_date and d <= self.end_date:
            return True
        else:
            return False


class Metrics:
    VOL_SHORT_MA = 'VOL_SHORT_MA'
    VOL_LONG_MA = 'VOL_LONG_MA'
    VOL_SHORT_MA_PREV = 'VOL_SHORT_MA_PREV'
    VOL_LONG_MA_PREV = 'VOL_LONG_MA_PREV'

    CLOSE_PREV = 'CLOSE_PREV'
    CHANGE = 'CHANGE'
    CHANGE_PCT = 'CHANGE_PCT'
    MA8 = 'MA8'
    MA21 = 'MA21'
    MA200 = 'MA200'

    ATR = 'ATR'
    ATR_SMOOTH = 'ATR_SMOOTH'


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


# read all csv files from symbol\csv directory
# http://www.nasdaq.com/screening/company-list.aspx
# add in the white list
# remove symbols with . - etc.
# read black list from symbol\black\black.txt. remove all black

# read all 3 csv
def prepare_symbols(boot):
    path = os.path.normpath(os.path.join(boot.base_path, '..', 'symbol'))
    print(path)
    df_input = pd.concat([pd.read_csv(filename) for filename in glob.glob(path + "/csv/*.csv")], axis=0)
    df_input['Symbol'] = df_input['Symbol'].str.strip()
    df_input = df_input[df_input['Symbol'] != '']
    print('Number of symbols from input csv:', len(df_input.index))

    # add white
    df_white = pd.read_csv(path + '/override/white.txt', header=None, names=['Symbol'])
    df_white['Symbol'] = df_white['Symbol'].str.strip()
    df_white['Symbol'] = df_white['Symbol'].str.upper()
    df_white = df_white[df_white['Symbol'] != '']
    print('Number of symbols from white list:', len(df_white.index))
    df_full = pd.concat([df_input, df_white])
    df_full.reset_index(drop=True, inplace=True)
    print('Number of symbols combined:', len(df_full.index))

    # remove black
    df_black = pd.read_csv(path + '/override/black.txt', header=None, names=['Symbol'])
    df_black['Symbol'] = df_black['Symbol'].str.strip()
    df_black['Symbol'] = df_black['Symbol'].str.upper()
    df_black = df_black[df_black['Symbol'] != '']
    print('Number of symbols from black list:', len(df_black.index))
    print(df_full.shape)
    for row in df_black['Symbol']:
        df_full = df_full[df_full.Symbol != row]
    print('after remove black')
    print(df_full.shape)

    # clean up
    df_full['Symbol'] = df_full['Symbol'].str.strip()
    df_full = df_full[df_full['Symbol'].str.match(r'^[a-zA-Z]+$')]
    df_full = df_full[df_full['Symbol'].str.len() < 5]
    df_full.sort_values(by=['Symbol', 'Name'], ascending=[True, True], inplace=True)
    df_full.drop_duplicates(subset='Symbol', inplace=True)
    print('Number of symbols combined after cleanup:', len(df_full.index))

    # export
    store_meta = HDFStore(boot.meta_file)
    store_meta.put('Symbol', df_full)

    df_full.to_csv(path + '/export/export.csv', columns=['Symbol', 'Name', 'industry'])
    print('Export complete!')


def read_symbols_meta_file(boot):
    store_meta = HDFStore(boot.meta_file)
    print(store_meta)
    return store_meta['Symbol']['Symbol']


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


def yang_candle_filter_vol(row):
    candle = CandleStick.fromRow(row)

    head_to_body_ratio_max = 0.2
    tail_to_body_ratio_max = 0.2
    body_atr_ratio_min = 1.5
    times_short_vol = 2.0
    times_long_vol = 3.0

    if candle.is_bull and (candle.head_to_body_ratio < head_to_body_ratio_max) and (
            candle.tail_to_body_ratio < tail_to_body_ratio_max) and (
            candle.body / row[Metrics.ATR_SMOOTH] > body_atr_ratio_min) and (
            (row['volume'] > row[Metrics.VOL_SHORT_MA_PREV] * times_short_vol) or (
            row['volume'] > row[Metrics.VOL_LONG_MA_PREV] * times_long_vol)):
        return True

    return False
