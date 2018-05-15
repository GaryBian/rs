import toolkit

boot = toolkit.Bootup()

tg = toolkit.TgData(boot)
# tg.symbols()

tg.daily()

tg.api2_get_daily()
