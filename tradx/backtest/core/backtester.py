from tradx.backtest.core.portfolio import Portfolio

class Backtester:
    def __init__(self, strategy_cls, data):
        self.strategy_cls = strategy_cls
        self.data = data

    def run(self):
        strategy = self.strategy_cls(self.data)
        signals = strategy.generate_signals()
        portfolio = Portfolio(signals)
        return portfolio.backtest()