import toolkit

# Get all symbols in meta.h5 and get data from alpha_vantage

# Standard format
# open
# high
# low
# nonadj close
# close
# volume


# toolkit.alpha_vantage_daily_full('TSLA')

boot = toolkit.Bootup()
print(boot)

vantage = toolkit.AlphaVantageData(boot.data_file)

vantage.get_daily_adjusted('TSLA', 'compact')
