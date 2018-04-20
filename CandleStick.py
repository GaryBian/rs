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
        d['date'] = self.date.strftime('%Y-%m-%d')
        d['head_to_body_ratio'] = "{:0.0f}".format(self.head_to_body_ratio * 100.0)
        d['tail_to_body_ratio'] = "{:0.0f}".format(self.tail_to_body_ratio * 100.0)
        d['change'] = "{:0.1f}".format((self.close - self.open) * 100.0 / self.open)
        s = "{date} | {bullflag} | {body} / {change}% | HEAD {head_to_body_ratio}% | TAIL {tail_to_body_ratio}%".format(
            **d)

        return s

    def associate_date(self, date):
        self.date = date

    @classmethod
    def fromRow(cls, row):
        return cls(row.open, row.high, row.low, row.close)
