import toolkit

boot = toolkit.Bootup()

# vantage = toolkit.AlphaVantageData(boot)
# vantage.audit_comprehensive()

dv = toolkit.DataView(boot)

print(dv.latest_data_date())
