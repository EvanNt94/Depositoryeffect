import pandas as pd
from portfolio.Portfolio import Portfolio
from Logger import Logger


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
        free_amount = 0
        current_amount_value = self.get_current_amount(df_full, invest_list, date)
        self.current_amount_value = current_amount_value
        self.current_amount[date.strftime("%Y-%m-%d")] = current_amount_value
        last_value["selled_amount"] = current_amount_value
        dropped_table = False

        self.logger.info(
            f"""
                         Date: {date}
                         Buy: {last_value["amount_buy"]}
                         Sell: {last_value["selled_amount"]}

                         """
        )

        new_invest_list = []
        df_adjusted = df.copy()

        aktien_darf_nicht_verkauft_werden = []
        aktien_dürfen_unter_oder_übergewichtet_werden = []
        ticker_from_last_buy = list(map(lambda x: x["ticker"], invest_list))

        for previous_invest in invest_list:
            ticker = previous_invest["ticker"]
            initial_price_buy = previous_invest["initial_price_buy"]
            price_ticker_today = df_full.loc[ticker, "Close"]
            actual_weight = (
                price_ticker_today * previous_invest["shares"] / current_amount_value
            )

            # Aktie wird ganz verkauft
            if ticker not in list(df.index):
                amount_selled = self.sell_old_stock(previous_invest, df_full, date)
                previous_invest["selled_amount"] = amount_selled
                previous_invest["price_sell"] = price_ticker_today
                previous_invest["date_sell"] = date.strftime("%Y-%m-%d")
                free_amount += amount_selled
            # Aktie wird behalten / dazukaufen oder verkaufen
            else:
                # Aktie ist im Minus
                if initial_price_buy > price_ticker_today:
                    # Nichts passiert
                    if actual_weight > df.loc[ticker, "Weight"]:
                        aktien_darf_nicht_verkauft_werden.append(previous_invest.copy())
                    # Aktie wird gekauft
                    else:
                        dif_weight = df_adjusted.loc[ticker, "Weight"] - actual_weight
                        if dif_weight > 0:
                            aktien_dürfen_unter_oder_übergewichtet_werden.append(
                                {"invest": previous_invest.copy(), "gewicht": 1}
                            )
                        else:
                            aktien_dürfen_unter_oder_übergewichtet_werden.append(
                                {"invest": previous_invest.copy(), "gewicht": -1}
                            )
                else:
                    dif_weight = df_adjusted.loc[ticker, "Weight"] - actual_weight
                    if dif_weight > 0:
                        aktien_dürfen_unter_oder_übergewichtet_werden.append(
                            {"invest": previous_invest.copy(), "gewicht": 1}
                        )
                    else:
                        aktien_dürfen_unter_oder_übergewichtet_werden.append(
                            {"invest": previous_invest.copy(), "gewicht": -1}
                        )

        # Behalte Aktien im Minus
        for aktie_darf_nicht_verkauft_werden in aktien_darf_nicht_verkauft_werden:
            ticker = aktie_darf_nicht_verkauft_werden["ticker"]
            shares = aktie_darf_nicht_verkauft_werden["shares"]
            price_ticker = df.loc[ticker, "Close"]
            amount_to_invest = shares * price_ticker
            weight_ticker = amount_to_invest / current_amount_value
            new_invest = {
                "ticker": ticker,
                "amount": amount_to_invest,
                "shares": shares,
                "price_buy": price_ticker,
                "price_actual": price_ticker,
                "weight": weight_ticker,
                "initial_price_buy": aktie_darf_nicht_verkauft_werden[
                    "initial_price_buy"
                ],
            }
            new_invest_list.append(new_invest)
            df_adjusted.drop(ticker, inplace=True)
            dropped_table = True
            current_amount_value -= amount_to_invest

        self.update_weight(df_adjusted)
        print(df_adjusted)

        alle_aktien_untergewichten = list(
            map(
                lambda x: x["invest"],
                filter(
                    lambda x: x["gewicht"] == -1,
                    aktien_dürfen_unter_oder_übergewichtet_werden,
                ),
            )
        )
        alle_aktien_übergewichten = list(
            map(
                lambda x: x["invest"],
                filter(
                    lambda x: x["gewicht"] == 1,
                    aktien_dürfen_unter_oder_übergewichtet_werden,
                ),
            )
        )

        for aktie_untergewicht in alle_aktien_untergewichten:
            ticker = aktie_untergewicht["ticker"]
            initial_price_buy = aktie_untergewicht["initial_price_buy"]
            price_ticker_today = df_adjusted.loc[ticker, "Close"]
            actual_weight = (
                price_ticker_today * aktie_untergewicht["shares"] / current_amount_value
            )

            dif_weight = df_adjusted.loc[ticker, "Weight"] - actual_weight

            amount_to_sell = dif_weight * current_amount_value
            shares_to_sell = amount_to_sell / price_ticker_today
            invest_copy = aktie_untergewicht.copy()
            invest_copy["amount"] = amount_to_sell + invest_copy["amount"]
            invest_copy["shares"] = shares_to_sell + invest_copy["shares"]
            invest_copy["weight"] = actual_weight + dif_weight
            invest_copy["price_buy"] = price_ticker_today
            new_invest_list.append(invest_copy)
            free_amount -= amount_to_sell

        for aktie_übergewichten in alle_aktien_übergewichten:
            ticker = aktie_übergewichten["ticker"]
            initial_price_buy = aktie_übergewichten["initial_price_buy"]
            price_ticker_today = df_adjusted.loc[ticker, "Close"]
            actual_weight = (
                price_ticker_today
                * aktie_übergewichten["shares"]
                / current_amount_value
            )

            dif_weight = df_adjusted.loc[ticker, "Weight"] - actual_weight

            amount_to_buy = dif_weight * current_amount_value
            shares_to_buy = amount_to_buy / price_ticker_today
            invest_copy = aktie_übergewichten.copy()
            invest_copy["amount"] = amount_to_buy + invest_copy["amount"]
            invest_copy["shares"] = shares_to_buy + invest_copy["shares"]
            invest_copy["weight"] = actual_weight + dif_weight
            invest_copy["price_buy"] = (dif_weight * price_ticker_today) + (
                1 - dif_weight
            ) * invest_copy["price_buy"]

            new_invest_list.append(invest_copy)  #

        # Kaufe Aktien
        for ticker_kaufe_aktien in df_adjusted.index:
            if ticker_kaufe_aktien not in ticker_from_last_buy:
                weight_ticker = df_adjusted.loc[ticker_kaufe_aktien, "Weight"]
                price_ticker = df_adjusted.loc[ticker_kaufe_aktien, "Close"]
                amount_to_invest = current_amount_value * weight_ticker
                shares_to_buy = amount_to_invest / price_ticker
                new_invest = {
                    "ticker": ticker_kaufe_aktien,
                    "amount": amount_to_invest,
                    "shares": shares_to_buy,
                    "price_buy": price_ticker,
                    "price_actual": price_ticker,
                    "weight": weight_ticker,
                    "initial_price_buy": price_ticker,
                }
                new_invest_list.append(new_invest)

        self.portfolio[pd.to_datetime(date)] = {
            "invest": new_invest_list,
            "amount_buy": self.current_amount_value,
            "date": date.strftime("%Y-%m-%d"),
        }

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
