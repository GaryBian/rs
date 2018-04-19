import talib
import pandas as pd
from pandas import HDFStore, DataFrame
import numpy


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
        self.head = self.high - self.body_top
        self.tail = self.body_bottom - self.low

    def displayCount(self):
        print(self.open)

    @classmethod
    def fromRandom(cls, row):
        return cls(row.open, row.high, row.low, row.close)


hdf = HDFStore('../data/daily.h5')
h1 = hdf['NVDA']

print(list(h1.columns.values))
print(h1.tail())

print(h1.iloc[1])

c1 = CandleStick.fromRandom(h1.iloc[1])
c2 = CandleStick.fromRandom(h1.iloc[2])

c3 = CandleStick.fromRandom(h1.iloc[30])

c35 = CandleStick.fromRandom(h1.iloc[35])

print(c1)
