import toolkit
from pandas import HDFStore

v = toolkit.VolChangeSelector(vol_vs_prev=1.5, vol_vs_short_ma=1.5, vol_vs_long_ma=1.5)
cg = toolkit.CloseGreaterThanSelector(greater_than=20)
vg = toolkit.VolGreaterThanSelector(greater_than=1000)

print(toolkit.DateSelector().describe())

print(toolkit.DateSelector('2018-03-02').describe())

print(toolkit.DateSelector('2018-03-02', '2018-03-10').describe())

print(v.describe())
print(cg.describe())
print(vg.describe())

boot = toolkit.Bootup()
hdf = HDFStore(boot.data_read_only_file)
df = hdf['CRC']
print(df.shape)

# toolkit.add_analysis_data(df)

toolkit.DataView.add_analysis_data(df)

for i, row in df.iterrows():
    print(v.evaluate(row))
    print(cg.evaluate(row))

print(v.evaluate(df.iloc[-1]))
