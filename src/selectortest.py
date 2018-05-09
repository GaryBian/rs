import toolkit
from pandas import HDFStore

v = toolkit.VolChangeSelector(vol_vs_prev=1.5, vol_vs_short_ma=1.5, vol_vs_long_ma=1.5)

print(v.describe())

boot = toolkit.Bootup()
hdf = HDFStore(boot.data_read_only_file)
df = hdf['ADSK']
print(df.shape)

toolkit.add_analysis_data(df)

for i, row in df.iterrows():
    print(v.evaluate(row))

print(v.evaluate(df.iloc[-1]))
