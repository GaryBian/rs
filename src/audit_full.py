import toolkit

boot = toolkit.Bootup()
vantage = toolkit.AlphaVantageData(boot)

vantage.audit_comprehensive()
