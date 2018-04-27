import toolkit
from pandas import HDFStore
import numpy
import pandas as pd
import time
import datetime

boot = toolkit.Bootup()
print(boot)
df_symbols = toolkit.read_symbols_meta_file(boot)
vantage = toolkit.AlphaVantageData(boot.data_file)

data_store = HDFStore(boot.data_file, mode='a')
count = 0
cutdate = datetime.datetime(2015, 1, 1)
for s in df_symbols:
    try:
        count += 1
        if count % 5 == 0:
            time.sleep(vantage.seconds_between_api_call)
            s = toolkit.AlphaVantageData.cleanse_symbol(s)
            df, meta = vantage.get_daily_adjusted(s, 'full')

            df = df[df.index >= cutdate]
            print(len(df.index))
            if len(df.index) > 0:
                data_store[s] = df
                print(s + ' done')
    except:
        print("Error working on: " + s)

data_store.close()
