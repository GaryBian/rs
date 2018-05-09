import toolkit
from pandas import HDFStore
import suite

c1 = suite.Combo1()
c1.date_selector = toolkit.DateSelector('2018-01-02', '2018-05-10')

boot = toolkit.Bootup()
hdf = HDFStore(boot.data_read_only_file)
df = hdf['ADSK']
print(df.shape)

toolkit.add_analysis_data(df)

for i, row in df.iterrows():
    print(i)
    print(c1.query(i, row))
