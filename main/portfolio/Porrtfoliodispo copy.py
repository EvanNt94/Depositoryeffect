import pandas as pd
from portfolio.Portfolio import Portfolio


class Portfoliodispo(Portfolio):
    def __init__(
        self,
        amount_start: int,
        anzahl_aktien: int,
    ):
        super().__init__(amount_start)
        self.non_selled_invests = []
        self.anzahl_aktien = anzahl_aktien
        self.stocks_in_loss = []

    def simulate_trading(self, df, df_full, date):
        return super().simulate_trading(df, df_full, date)

    def sell_old_stocks(self, df, df_full, date):
        last_key = list(self.portfolio.keys())[-1]
        last_value = self.portfolio[last_key]
        invest_list = last_value["invest"]

        amount_sell_sum = 0
        for invest in invest_list:
            ticker = invest["ticker"]
            price_ticker = df_full.loc[ticker, "Close"]
            if price_ticker < invest["price_buy"]:
                self.stocks_in_loss.append(invest.copy())

            amount_selled = invest["shares"] * price_ticker
            invest["price_sell"] = price_ticker
            invest["amount_sell"] = amount_selled
            amount_sell_sum += amount_selled

        self.current_amount[date.strftime("%Y-%m-%d")] = amount_sell_sum
        self.current_amount_value = amount_sell_sum
        last_value["selled_amount"] = amount_sell_sum

    def buy_new_stocks(self, df, date):
        tickers = list(df.index)
        self.invest = []

        sold_tickers_in_ticker = []

        free_amount = self.current_amount_value

        # Behalte aktien im minus
        for invest in self.non_selled_invests:
            ticker = invest["ticker"]
            shares = invest["shares"]
            price_ticker = df.loc[ticker, "Close"]
            amount_to_invest = shares * price_ticker
            weight_ticker = amount_to_invest / self.current_amount_value

            if ticker not in tickers:
                self.invest.append(
                    {
                        "ticker": ticker,
                        "amount": amount_to_invest,
                        "shares": shares,
                        "price_buy": price_ticker,
                        "weight": weight_ticker,
                        "initial_price_buy": invest["initial_price_buy"],
                    }
                )
                free_amount -= amount_to_invest
            else:
                weight_of_sold_stock = (
                    price_ticker * shares
                ) / self.current_amount_value
                if weight_of_sold_stock < weight_ticker:
                    amount_to_invest = free_amount * weight_ticker
                    # TODO
                else:
                    self.invest.append(
                        {
                            "ticker": ticker,
                            "amount": amount_to_invest,
                            "shares": shares,
                            "price_buy": price_ticker,
                            "weight": weight_ticker,
                            "initial_price_buy": invest["initial_price_buy"],
                        }
                    )
                    free_amount -= amount_to_invest

        remaining_stocks = self.anzahl_aktien - len(self.stocks_in_loss)

        for invest in sold_tickers_in_ticker:
            ticker = invest["ticker"]
            shares = invest["shares"]
            price_ticker = df.loc[ticker, "Close"]

        # Nur die ersten remaining_stocks (n) ausgeben
        for ticker in tickers:
            weight_ticker = df.loc[ticker, "Weight"]
            price_ticker = df.loc[ticker, "Close"]

            amount_to_invest = self.current_amount_value * weight_ticker
            anzahl_aktien = amount_to_invest / price_ticker

            self.invest.append(
                {
                    "ticker": ticker,
                    "amount": amount_to_invest,
                    "shares": anzahl_aktien,
                    "price_buy": price_ticker,
                    "weight": weight_ticker,
                    "initial_price_buy": price_ticker,
                }
            )
        self.portfolio[pd.to_datetime(date)] = {
            "invest": self.invest,
            "amount_buy": self.current_amount_value,
            "date": date.strftime("%Y-%m-%d"),
        }

        self.non_selled_invests = []
