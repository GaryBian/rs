import pandas as pd
from pandas import HDFStore, DataFrame

# load the data file in
hdf = HDFStore('../data/daily.h5')

# access one symbol, it gives back a DataFrame
h1 = hdf['SPX']

print(h1.head())

