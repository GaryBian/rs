import toolkit
import datetime
from pandas import HDFStore

boot = toolkit.Bootup()
hdf = HDFStore(boot.data_file)
df = hdf['ADSK']
print(df.shape)

print(df.tail(1))
