import toolkit
from pandas import HDFStore
from toolkit import DataView

v = toolkit.VolChangeSelector(vol_vs_prev=1.5, vol_vs_short_ma=1.5, vol_vs_long_ma=1.5)
cg = toolkit.CloseGreaterThanSelector(greater_than=20)
vg = toolkit.VolGreaterThanSelector(greater_than=1000)

print(toolkit.DateSelector().describe())

print(toolkit.DateSelector('2018-03-02').describe())

print(toolkit.DateSelector('2018-03-02', '2018-03-10').describe())

print(v.describe())
print(cg.describe())
print(vg.describe())

for n in (1.23456789 * 10 ** r for r in range(-2, 19, 1)):
    print(DataView.millify(n))
    print('%20.1f: %20s' % (n, DataView.millify(n)))

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
