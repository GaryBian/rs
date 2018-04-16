import pandas as pd
from pandas import HDFStore, DataFrame

# load the data file in
hdf = HDFStore('../data/daily.h5')

# access one symbol, it gives back a DataFrame
h1 = hdf['SPX']

list(h1.columns.values)

print(h1.head())
print(h1.tail())
print(h1.describe())
