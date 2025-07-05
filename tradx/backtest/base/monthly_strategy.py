import pandas as pd
from core.strategy import Strategy

class MonthlyInvestmentStrategy(Strategy):
    def __init__(self, data: pd.DataFrame, amount_per_month: float = 1000):
        super().__init__(data)
        self.amount = amount_per_month

    def generate_signals(self) -> pd.DataFrame:
        df = self.data.copy()
        df['Signal'] = 0
        df = df.asfreq('D').ffill()  # tägliche Frequenz sicherstellen

        # Investiere jeden 1. Tag eines Monats
        mask = (df.index.day == 1) & (df.index.to_series().diff().dt.days != 1)
        df.loc[mask, 'Signal'] = 1

        df['Investment'] = df['Signal'] * self.amount
        return df