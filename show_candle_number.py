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

cs.CandleStick.fromRow(hdf['TSLA'].loc['2018-3-12']).describe()
cs.CandleStick.fromRow(hdf['TSLA'].loc['2016-12-14']).describe()
cs.CandleStick.fromRow(hdf['TSLA'].loc['2016-12-13']).describe()
cs.CandleStick.fromRow(hdf['TSLA'].loc['2016-12-20']).describe()
cs.CandleStick.fromRow(hdf['TSLA'].loc['2017-1-4']).describe()

cs.CandleStick.fromRow(hdf['TSLA'].loc['2014-1-14']).describe()

cs.CandleStick.fromRow(hdf['TSLA'].loc['2012-10-24']).describe()

cs.CandleStick.fromRow(hdf['TSLA'].loc['2010-11-4']).describe()
