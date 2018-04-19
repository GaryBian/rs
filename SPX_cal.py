import pandas as pd
from pandas import HDFStore, DataFrame
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# Go back N days from now
# return start date of the quarter which it falls in
def go_back_n_days(days):
    date_N_days_ago = datetime.now() - timedelta(days)
    # print('{:%Y-%m-%d}'.format(date_N_days_ago))
    return date_N_days_ago


# first and last day of the quarter for the input date
def first_last_day_of_quarter(day):
    curr_quarter = day.month // 3 + 1
    first_day = datetime(day.year, 3 * curr_quarter - 2, 1)
    if curr_quarter == 4:
        last_day = datetime(day.year + 1, 3 * 0 + 1, 1) + timedelta(days=-1)
    else:
        last_day = datetime(day.year, 3 * curr_quarter + 1, 1) + timedelta(days=-1)
    return first_day, last_day


go_back_n_days(290)
first_day, last_day = first_last_day_of_quarter(datetime.now())
print(first_day, last_day)

print(first_last_day_of_quarter(go_back_n_days(90)))

hdf = HDFStore('data/daily.h5')

start_date = '2016-01-01'
h1 = hdf['SPX']
h_spx = h1[h1.index >= start_date]
picked_min_date = h_spx.index.min()
print(h_spx.loc[picked_min_date])

plot_data = {}

for i, row in h_spx.iterrows():
    p_spx = (row['adjusted close'] / h_spx.loc[picked_min_date]['adjusted close'] - 1.0) * 100.0

    print('index: ', i,
          # row['adjusted close'],
          p_spx,
          'Diff:',
          )
    plot_data[i] = p_spx

print(plot_data)

plot_df = DataFrame(list(plot_data.items()), columns=['Date', 'DateValue'])

plot_df.plot(x='Date', y='DateValue')
plt.show()
