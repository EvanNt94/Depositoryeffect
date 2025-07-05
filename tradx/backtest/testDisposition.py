import pandas as pd
from tradx.backtest.core.backtester import Backtester
from strategies.disposition_strategy import DispositionEffectStrategy

df = pd.read_csv("data/sample_data.csv", index_col="Date", parse_dates=True)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

bt = Backtester(DispositionEffectStrategy, df)
results = bt.run()
print(results.tail())