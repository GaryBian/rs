from pandas import HDFStore
import CandleStick as cs

hdf = HDFStore('data/daily.h5')

cs.CandleStick.fromRow(hdf['TXN'].loc['2018-2-14']).describe()
cs.CandleStick.fromRow(hdf['TXN'].loc['2018-2-23']).describe()
cs.CandleStick.fromRow(hdf['TXN'].loc['2018-2-26']).describe()
cs.CandleStick.fromRow(hdf['TXN'].loc['2018-3-27']).describe()
cs.CandleStick.fromRow(hdf['TXN'].loc['2018-4-9']).describe()


cs.CandleStick.fromRow(hdf['TSLA'].loc['2018-4-4']).describe()
cs.CandleStick.fromRow(hdf['TSLA'].loc['2018-4-6']).describe()
cs.CandleStick.fromRow(hdf['TSLA'].loc['2018-4-11']).describe()
