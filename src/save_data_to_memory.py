import toolkit
from toolkit import AlphaVantageData
import time
from pandas import HDFStore

boot = toolkit.Bootup()
hdf = HDFStore(boot.data_file)
keys = hdf.keys()
dict = []
count = 0
for symbol in keys:
    count += 1
    if count < 1000000:
        df = hdf[symbol.strip('/')]
        dict.append(df.tail(1)['close'][0])

print(dict)

dict.sort()

print(dict)

printidx = 0
for d in dict:
    printidx += 1
    print(str(printidx) + " : " + str(d))
