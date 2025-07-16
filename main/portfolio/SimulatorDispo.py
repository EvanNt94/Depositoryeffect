from datetime import datetime, timedelta

from config.Parameter import Parameter
from portfolio.Portfolio import Portfolio
from strategies.metrics import calculate_metrics
from portfolio.Simulator import Simulator
from stockexchange.FetchStock import FetchStock
from strategies.strategy import Strategy


class SimulatorDispo(Simulator):
    def __init__(
        self,
        fetchStock: FetchStock,
        strategy: Strategy,
        parameter: Parameter,
        portfolio: Portfolio,
    ):
        super().__init__(fetchStock, strategy, parameter, portfolio)

    def get_ticker_with_loss(self, last_stocks, data, actual_pos):
        """
        Gibt eine Liste von Ticker-Symbolen zurück, die einen Kursverlust aufweisen.
        """
        ticker_with_loss = []
        for invest in last_stocks:

            if (
                invest["initial_price_buy"] * (1 + (self.parameter.dispoGrenze / 100))
                > data.iloc[actual_pos][("Close", invest["ticker"])]
            ):
                ticker_with_loss.append(invest["ticker"])
        return ticker_with_loss

    def simulate(self):
        print("Start Simulation")
        self.prepare_dates()

        current_date = self.pos_start
        stocks_with_loss = []
        current_portfolio = None
        while current_date <= self.pos_end:
            if current_portfolio is not None:
                stocks_with_loss = self.get_ticker_with_loss(
                    current_portfolio["invest"],
                    self.fetchStock.get_data(),
                    current_date,
                )

            ranking = self.sort_stocks(
                current_date, self.fetchStock.get_data(), stocks_with_loss
            )
            current_portfolio = self.portfolio.simulate_trading(
                ranking["head"], ranking["full"], ranking["current_date"]
            )
            current_date += self.parameter.frequency
        self.metrics = calculate_metrics(self.portfolio)
        