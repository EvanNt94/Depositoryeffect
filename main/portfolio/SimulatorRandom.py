from datetime import datetime, timedelta

from config.Parameter import Parameter
from portfolio.Portfolio import Portfolio
from portfolio.SimulatorDispo import SimulatorDispo
from stockexchange.FetchStock import FetchStock
from strategies.metrics import calculate_metrics
from strategies.strategy import Strategy


class SimulatorRandom(SimulatorDispo):
    def __init__(
        self,
        fetchStock: FetchStock,
        strategy: Strategy,
        parameter: Parameter,
        portfolio: Portfolio,
    ):
        super().__init__(fetchStock, strategy, parameter, portfolio)
        self.stop_loss = 0.1
        self.take_profit = 0.1

    def get_ticker_with_loss(self, last_stocks, data, actual_pos):
        """
        Gibt eine Liste von Ticker-Symbolen zurück, die einen Kursverlust aufweisen.
        """
        ticker_with_loss = []
        for invest in last_stocks:

            if (
                invest["initial_price_buy"] * ((1 + self.take_profit) / 100)
                < data.iloc[actual_pos][("Close", invest["ticker"])]
                or invest["initial_price_buy"] * ((1 - self.stop_loss) / 100)
                > data.iloc[actual_pos][("Close", invest["ticker"])]
            ):
                ticker_with_loss.append(invest["ticker"])
        return ticker_with_loss
