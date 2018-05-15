import toolkit

boot = toolkit.Bootup()
vantage = toolkit.AlphaVantageData(boot)
vantage.incremental_update()

dv = toolkit.DataView(boot)
print("majority latest date:" + str(dv.majority_latest_date()))
