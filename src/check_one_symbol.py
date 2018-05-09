import toolkit
import datetime
from pandas import HDFStore

boot = toolkit.Bootup()
hdf = HDFStore(boot.data_read_only_file)
df = hdf['ADSK']
print(df.shape)

print(df.tail(1))

toolkit.add_analysis_data(df)
