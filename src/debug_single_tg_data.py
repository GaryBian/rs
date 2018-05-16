import toolkit
from pandas import HDFStore

boot = toolkit.Bootup()
print(boot.base_path)

tg = toolkit.TgData(boot)
df = tg.daily("GALE", go_back_days=1000)

print(df)
