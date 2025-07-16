import pandas as pd
from Logger import Logger


class Portfolio:
    def __init__(
        self,
        amount_start: int,
    ):
        self.amount_start = amount_start
        self.current_amount = {}
        self.current_amount_value = self.amount_start
        self.portfolio = {}
        self.history = {}
        self.first_buy = True
        self.logger = Logger(__name__).logger

    def value_series(self) -> pd.Series:
        data = {}
        for date, entry in self.portfolio.items():
            total_value = sum(
                inv["shares"] * inv["price_actual"] for inv in entry["invest"]
            )
            data[pd.to_datetime(date)] = total_value

        return pd.Series(data).sort_index()

    def set_start_date(self, start_date: str):
        self.current_amount[start_date] = self.amount_start

    def simulate_trading(self, df, df_full, date):
        if self.first_buy:
            self.buy_new_stocks(df, date)
        else:
            self.sell_old_stocks(df, df_full, date)
            self.buy_new_stocks(df, date)
        self.first_buy = False
        return self.portfolio[pd.to_datetime(date)]

    def sell_old_stocks(self, df, df_full, date):
        last_key = list(self.portfolio.keys())[-1]
        last_value = self.portfolio[last_key]
        invest_list = last_value["invest"]
        amount_sell_sum = 0
        for invest in invest_list:
            ticker = invest["ticker"]
            price_ticker = df_full.loc[ticker, "Close"]
            amount_selled = invest["shares"] * price_ticker
            invest["price_sell"] = price_ticker
            invest["amount_sell"] = amount_selled
            amount_sell_sum += amount_selled

        self.current_amount[date.strftime("%Y-%m-%d")] = amount_sell_sum
        self.current_amount_value = amount_sell_sum
        last_value["selled_amount"] = amount_sell_sum

    def buy_new_stocks(self, df, date):
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
            
            {log_str}
            
            
            """
        )

    def get_values(self):
        return self.current_amount
