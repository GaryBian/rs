import toolkit
import datetime
from pandas import HDFStore

boot = toolkit.Bootup()
vantage = toolkit.AlphaVantageData(boot.data_file)

vantage.audit_comprehensive()