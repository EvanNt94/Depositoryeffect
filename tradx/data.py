from alpha_vantage.timeseries import TimeSeries

# https://www.alphavantage.co/documentation/#intraday
ts = TimeSeries(key='DEFKZ1GRUJCJADBJ', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='full')
print(len(data))