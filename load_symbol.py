import pandas as pd
from pandas import HDFStore, DataFrame
import glob

# read all csv files from symbol\csv directory
# http://www.nasdaq.com/screening/company-list.aspx
# add in the white list
# remove symbols with . - etc.
# read black list from symbol\black\black.txt. remove all black

# read all 3 csv
df_input = pd.concat([pd.read_csv(filename) for filename in glob.glob("symbol/csv/*.csv")], axis=0)
df_input['Symbol'] = df_input['Symbol'].str.strip()
print('Number of symbols from input csv:', len(df_input.index))

# read in white
df_white = pd.read_csv('symbol/override/white.txt', header=None, names=['Symbol'])
df_white['Symbol'] = df_white['Symbol'].str.strip()
df_white['Symbol'] = df_white['Symbol'].str.upper()
df_white = df_white[df_white['Symbol'] != '']
print('Number of symbols from white list:', len(df_white.index))

# add white
df_full = pd.concat([df_input, df_white])
df_full.reset_index(drop=True, inplace=True)
print('Number of symbols combined:', len(df_full.index))

# remove black

# clean up
df_full['Symbol'] = df_full['Symbol'].str.strip()
df_full = df_full[df_full['Symbol'].str.match(r'^[a-zA-Z]+$')]
df_full = df_full[df_full['Symbol'].str.len() < 5]
df_full.sort_values(by=['Symbol', 'Name'], ascending=[True, True], inplace=True)
df_full.drop_duplicates(subset='Symbol', inplace=True)
print('Number of symbols combined after cleanup:', len(df_full.index))

# export
store_meta = HDFStore('data/meta.h5')
store_meta.put('Symbol', df_full)

df_full.to_csv('symbol/export/export.csv', columns=['Symbol', 'Name', 'industry'])
print('Export complete!')
