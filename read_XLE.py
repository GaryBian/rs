import pandas as pd
from pandas import HDFStore, DataFrame

hdf = HDFStore('daily.h5')

start_date = '2016-01-01'
h1 = hdf['SPX']
h_spx = h1[h1.index >= start_date]
picked_min_date = h_spx.index.min()
print(h_spx.loc[picked_min_date])

target_s = 'XLE'
h2 = hdf[target_s]
h_adbe = h2[h2.index >= start_date]

for i, row in h_spx.iterrows():
    p_spx = (row['adjusted close'] / h_spx.loc[picked_min_date]['adjusted close'] - 1.0) * 100.0
    p_adbe = (h_adbe.loc[i]['adjusted close'] / h_adbe.loc[picked_min_date]['adjusted close'] - 1.0) * 100.0
    p_diff = p_adbe - p_spx
    print('index: ', i,
          # row['adjusted close'],
          p_spx,
          target_s,
          p_adbe,
          'Diff:',
          p_diff,
          "{0:.1f}%".format(p_diff)
          )
