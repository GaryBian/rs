import toolkit

boot = toolkit.Bootup()
vantage = toolkit.AlphaVantageData(boot)
vantage.incremental_update()
