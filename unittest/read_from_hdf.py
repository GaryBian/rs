from pandas import HDFStore, DataFrame

# load the data file in
hdf = HDFStore('../data/daily.h5')

# each symbol is organized as a key
print(hdf.keys())

# the index is Date
print(hdf['ADBE'].index.name)

print(hdf['ADBE'].shape)

v = hdf['SPX'].index.values

start_date = '2016-01-01'

# access one symbol
h1 = hdf['SPX']
h_spx = h1[h1.index >= start_date]
picked_min_date = h_spx.index.min()
print(h_spx.loc[picked_min_date])

# access the close price of a symbol and a specific date
# DataFrame	df.loc[row_indexer,column_indexer]
# '2016-01-11' is the row indexer, 'close' is column indexer
print(hdf['SPX'].loc['2016-01-11']['close'])

print(hdf['SPX'].loc['2016-01-11', 'close'])

