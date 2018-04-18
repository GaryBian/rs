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

    @classmethod
    def fromRow(cls, row):
        return cls(row.open, row.high, row.low, row.close)
