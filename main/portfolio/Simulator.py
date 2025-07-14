from datetime import datetime, timedelta
from Depositoryeffect.main.strategies.metrics import calculate_metrics

import pandas as pd
from config.Parameter import Parameter
from portfolio.Portfolio import Portfolio
from stockexchange.FetchStock import FetchStock
from strategies.strategy import Strategy


class Simulator:
    def __init__(
        self,
        fetchStock: FetchStock,
        strategy: Strategy,
        parameter: Parameter,
        portfolio: Portfolio,
    ):
        self.fetchStock = fetchStock
        self.strategy = strategy
        self.parameter = parameter
        self.stocks = []  # Liste für die Aktien im Portfolio
        self.stocks_analyzied = {}  # Liste für analysierte Aktien
        self.outstanding_shares = self.fetchStock.outstanding_shares
        self.portfolio = portfolio
        self.pos_start = None  # Startposition im DataFrame
        self.pos_end = None  # Endposition im DataFrame
        self.metrics = None
        # Portfolio, das die Aktien und deren Gewichtung enthält

    def get_pos(self, df, date, reverse=False):
        """
        Gibt die Position für ein bestimmtes Datum zurück.
        """

        notfound = True
        actual_date = date
        indexList = list(map(lambda i: i.date(), list(df.index)))

        while notfound:
            if actual_date in indexList:
                return indexList.index(actual_date)
            else:
                if reverse:
                    actual_date = actual_date - timedelta(days=1)
                else:
                    actual_date = actual_date + timedelta(days=1)

    def prepare_dates(self):

        start_date = datetime.strptime(self.parameter.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(self.parameter.end_date, "%Y-%m-%d").date()

        data = self.fetchStock.get_data()
        pos_start = self.get_pos(data, start_date, reverse=False)
        pos_end = self.get_pos(data, end_date, reverse=True)

        print("Start Position:", pos_start, " ", list(data.index)[pos_start])
        print("End Position:", pos_end, " ", list(data.index)[pos_end])
        self.portfolio.set_start_date(list(data.index)[pos_start])
        self.pos_start = pos_start
        self.pos_end = pos_end

    def sort_stocks(self, actual_pos, data, stocks_with_loss):

        current_date = list(data.index)[actual_pos].date()

        sorted_stocks = self.strategy.sort_stocks(
            actual_pos, self.fetchStock.get_data()
        )

        sorted_stocks = sorted_stocks.reset_index(level=0, drop=True)

        sorted_stocks["Outstanding Shares"] = self.outstanding_shares
        sorted_stocks["Market Cap"] = sorted_stocks["Close"] * self.outstanding_shares

        sorted_stocks_head = sorted_stocks.head(int(self.parameter.anzahlAktien)).copy()

        if len(stocks_with_loss) > 0:
            liste1 = list(stocks_with_loss)
            liste2 = list(sorted_stocks_head.index)
            unique = liste1.copy()
            for el in liste2:
                if len(unique) >= self.parameter.anzahlAktien:
                    break
                if el not in unique:
                    unique.append(el)

            sorted_stocks_head = sorted_stocks.loc[unique].copy()

        sorted_stocks_head = self.strategy.sort_df(sorted_stocks_head)

        sorted_stocks_head.loc[:, "Weight"] = (
            sorted_stocks_head["Market Cap"] / sorted_stocks_head["Market Cap"].sum()
        )

        if len(sorted_stocks_head.index) > self.parameter.anzahlAktien:
            raise RuntimeError("ERRRORRRRRRRRRRRRRRRRRRRRRRRRRRR")

        self.stocks_analyzied[current_date] = {
            "head": sorted_stocks_head,
            "full": sorted_stocks,
            "current_date": current_date,
        }
        return self.stocks_analyzied[current_date]

    def prepare_data(self):
        start_date = datetime.strptime(self.parameter.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(self.parameter.end_date, "%Y-%m-%d").date()
        current_date = start_date

        data = self.fetchStock.get_data()
        pos_start = self.get_pos(data, start_date, reverse=False)
        pos_end = self.get_pos(data, end_date, reverse=True)

        print("Start Position:", pos_start, " ", list(data.index)[pos_start])
        print("End Position:", pos_end, " ", list(data.index)[pos_end])

        self.portfolio.set_start_date(list(data.index)[pos_start])

        actual_pos = pos_start
        last_stocks = None

        while actual_pos <= pos_end:
            current_date = list(data.index)[actual_pos].date()
            stocks_with_loss = []
            if last_stocks is not None:
                stocks_with_loss = self.get_ticker_with_loss(
                    last_stocks, self.fetchStock.get_data(), actual_pos
                )

            sorted_stocks = self.strategy.sort_stocks(
                actual_pos, self.fetchStock.get_data(), stocks_with_loss
            )

            sorted_stocks = sorted_stocks.reset_index(level=0, drop=True)

            sorted_stocks["Outstanding Shares"] = self.outstanding_shares
            sorted_stocks["Market Cap"] = (
                sorted_stocks["Close"] * self.outstanding_shares
            )

            sorted_stocks_head = sorted_stocks.head(
                int(self.parameter.anzahlAktien)
            ).copy()

            sorted_stocks_head.loc[:, "Weight"] = (
                sorted_stocks_head["Market Cap"]
                / sorted_stocks_head["Market Cap"].sum()
            )

            self.stocks_analyzied[current_date] = {
                "head": sorted_stocks_head,
                "full": sorted_stocks,
            }

            actual_pos += 1
            last_stocks = sorted_stocks_head

    def get_ticker_with_loss(self, last_stocks, data, actual_pos):
        """
        Gibt eine Liste von Ticker-Symbolen zurück, die einen Kursverlust aufweisen.
        """
        return []

    def simulate(self):
        print("Start Simulation")
        self.prepare_dates()

        current_date = self.pos_start
        while current_date <= self.pos_end:
            ranking = self.sort_stocks(current_date, self.fetchStock.get_data(), [])
            self.portfolio.simulate_trading(
                ranking["head"], ranking["full"], ranking["current_date"]
            )
            current_date += self.parameter.frequency
        self.metrics = calculate_metrics(self.portfolio)