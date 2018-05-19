import toolkit
from toolkit import DataView

boot = toolkit.Bootup()
vantage = toolkit.AlphaVantageData(boot)
vantage.incremental_update()

dv = toolkit.DataView(boot)
print("majority latest date:" + str(DataView.majority_latest_date()))
