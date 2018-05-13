import toolkit
from pandas import HDFStore
import numpy
import pandas as pd
import time
import datetime

boot = toolkit.Bootup()
print(boot)
df_symbols = [
    'ALSN']
vantage = toolkit.AlphaVantageData(boot)

count = 0
successcount = 0
cutdate = datetime.datetime(1900, 1, 1)
for s in df_symbols:
    try:
        count += 1
        # if count % 5 == 0:
        if True:
            time.sleep(vantage.seconds_between_api_call)
            s = toolkit.AlphaVantageData.cleanse_symbol(s)
            df, meta = vantage.get_daily_adjusted(s, 'full')

            df = df[df.index >= cutdate]
            print(len(df.index))
            if len(df.index) > 0:
                data_store = HDFStore(boot.data_file, mode='a')
                data_store[s] = df
                data_store.close()
                successcount += 1
                print(s + ' done ' + str(successcount))
    except:
        print("Error working on: " + s)

print('Task completed')
