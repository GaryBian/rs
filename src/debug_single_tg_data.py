import toolkit
from pandas import HDFStore
from toolkit import DataView

boot = toolkit.Bootup()
print(boot.base_path)

a = DataView.majority_latest_date(boot.base_path + '/../tg/tg_data.h5')

print(a)

# tg = toolkit.TgData(boot)
# df = tg.daily("GALE", go_back_days=1000)
# print(df)
