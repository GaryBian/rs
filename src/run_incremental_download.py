import toolkit

boot = toolkit.Bootup()
vantage = toolkit.AlphaVantageData(boot.data_file)
vantage.incremental_update()
