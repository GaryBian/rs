import pandas as pd
from pandas import HDFStore, DataFrame
import matplotlib.pyplot as plt

hdf = HDFStore('daily.h5')

start_date = '2016-01-01'
h1 = hdf['SPX']
h_spx = h1[h1.index >= start_date]
picked_min_date = h_spx.index.min()
print(h_spx.loc[picked_min_date])

target_s = 'XLF'
h2 = hdf[target_s]
h_adbe = h2[h2.index >= start_date]

plot_data = {}

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
          p_diff)
    plot_data[i] = p_diff

plot_df = DataFrame(list(plot_data.items()), columns=['Date', 'DateValue'])

plot_df['MA'] = plot_df['DateValue'].rolling(21).mean()

print(plot_df.head())

plot_df.plot(x='Date', y='MA')
plt.show()

print('XLF')
