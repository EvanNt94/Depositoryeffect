from tradx.backtest.base.monthly_strategy import MonthlyInvestmentStrategy
from core.backtester import Backtester
from tradx.backtest.core.data_loader import load_price_data

df = load_price_data("US0378331005", "2015-01-01", "2025-01-01")
bt = Backtester(MonthlyInvestmentStrategy, df)
results = bt.run()
print(results.tail())