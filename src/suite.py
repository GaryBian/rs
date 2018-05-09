import toolkit


class Combo1:

    def __init__(self):
        print("create combo 1")
        self.basic_selectors = []
        self.basic_selectors.append(toolkit.CloseGreaterThanSelector(greater_than=20))
        self.basic_selectors.append(toolkit.VolGreaterThanSelector(greater_than=1000))
        self.basic_selectors.append(toolkit.VolChangeSelector(vol_vs_prev=1.5, vol_vs_short_ma=1.5, vol_vs_long_ma=1.5))

        self.date_selector = toolkit.DateSelector()

    def query(self, datevalue, row):
        if not self.date_selector.evaluate(datevalue):
            return False

        for selector in self.basic_selectors:
            if not selector.evaluate(row):
                return False

        return True
