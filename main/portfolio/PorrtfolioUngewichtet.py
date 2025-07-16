import pandas as pd
from Logger import Logger
from portfolio.Portfolio import Portfolio


class PortfolioUngewichtet(Portfolio):
    def __init__(
        self,
        amount_start: int,
        anzahl_aktien: int,
    ):
        super().__init__(amount_start)
        self.anzahl_aktien = anzahl_aktien
        self.logger = Logger(__name__).logger

    def simulate_trading(self, df, df_full, date):
        if self.first_buy:
            self.buy_first_stocks(df, date)
        else:
            self.simulate_stocks(df, df_full, date)
        self.first_buy = False
        return self.portfolio[pd.to_datetime(date)]

    def show_invest(self, invest):
        return dict(enumerate(invest))

    def get_current_amount(self, df_full, invest_list, date):
        amount = 0
        for invest in invest_list:
            ticker = invest["ticker"]
            price_ticker = df_full.loc[ticker, "Close"]
            amount_selled = invest["shares"] * price_ticker
            amount += amount_selled

        return amount

    def simulate_stocks(self, df, df_full, date):
        last_key = list(self.portfolio.keys())[-1]
        last_value = self.portfolio[last_key]
        invest_list = last_value["invest"]

        current_amount_value = self.get_current_amount(df_full, invest_list, date)
        self.current_amount_value = current_amount_value
        self.current_amount[date.strftime("%Y-%m-%d")] = current_amount_value
        last_value["selled_amount"] = current_amount_value

        invest = []

        for last_invest in invest_list:
            ticker = last_invest["ticker"]
            shares = last_invest["shares"]
            price_ticker = df_full.loc[ticker, "Close"]

            amount_to_invest = shares * price_ticker
            weight_ticker = amount_to_invest / current_amount_value
            anzahl_aktien = shares

            invest.append(
                {
                    "ticker": ticker,
                    "amount": amount_to_invest,
                    "shares": anzahl_aktien,
                    "price_buy": price_ticker,
                    "price_actual": price_ticker,
                    "weight": weight_ticker,
                    "initial_price_buy": price_ticker,
                }
            )
        self.portfolio[pd.to_datetime(date)] = {
            "invest": invest,
            "amount_buy": self.current_amount_value,
            "date": date.strftime("%Y-%m-%d"),
        }
        log_str = ""
        for my_invest in invest:
            log_str += f"""
            Ticker: {my_invest["ticker"]}  gekauft für {my_invest["price_buy"]}
                \n
            """
        self.logger.info(
            f"""Date:  {date.strftime("%Y-%m-%d")}
            
            {log_str}"""
        )

    def update_weight(self, df):
        df["Weight"] = df["Market Cap"] / df["Market Cap"].sum()
        df = df.sort_values(by="Weight", ascending=False)

    def sell_old_stock(self, invest, df, date):
        ticker = invest["ticker"]
        price_ticker = df.loc[ticker, "Close"]

        amount_selled = invest["shares"] * price_ticker
        invest["price_sell"] = price_ticker
        invest["amount_sell"] = amount_selled
        return amount_selled

    def buy_first_stocks(self, df, date):
        tickers = list(df.index)
        invest = []
        for ticker in tickers:
            weight_ticker = df.loc[ticker, "Weight"]
            price_ticker = df.loc[ticker, "Close"]

            amount_to_invest = self.current_amount_value * weight_ticker
            anzahl_aktien = amount_to_invest / price_ticker

            invest.append(
                {
                    "ticker": ticker,
                    "amount": amount_to_invest,
                    "shares": anzahl_aktien,
                    "price_buy": price_ticker,
                    "price_actual": price_ticker,
                    "weight": weight_ticker,
                    "initial_price_buy": price_ticker,
                    "date_buy": date.strftime("%Y-%m-%d"),
                }
            )
        self.portfolio[pd.to_datetime(date)] = {
            "invest": invest,
            "amount_buy": self.current_amount_value,
            "date": date.strftime("%Y-%m-%d"),
        }
        self.current_amount[date.strftime("%Y-%m-%d")] = self.current_amount_value
