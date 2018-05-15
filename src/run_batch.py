import toolkit
import fix_yahoo_finance as yf

data = yf.download(["SPY", "IWM"], start="2018-05-10", end="2018-05-14", group_by='ticker')

print(data)
boot = toolkit.Bootup()
vantage = toolkit.AlphaVantageData(boot)
data, meta = vantage.get_batch_quote()

print(data)
