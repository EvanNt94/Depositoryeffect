import pandas as pd

class Portfolio:
    def __init__(self, signals: pd.DataFrame, initial_cash: float = 10000):
        self.signals = signals
        self.initial_cash = initial_cash

    def backtest(self) -> pd.DataFrame:
        df = self.signals.copy()
        df['Position'] = 0
        df['Cash'] = self.initial_cash
        df['Holdings'] = 0
        df['Total'] = self.initial_cash
        position = 0
        cash = self.initial_cash

        for i in range(len(df)):
            price = df['Close'].iloc[i]
            signal = df['Signal'].iloc[i]

            if signal == 1:
                position = cash // price
                cash -= position * price
            elif signal == -1:
                cash += position * price
                position = 0

            df.at[df.index[i], 'Position'] = position
            df.at[df.index[i], 'Cash'] = cash
            df.at[df.index[i], 'Holdings'] = position * price
            df.at[df.index[i], 'Total'] = df.at[df.index[i], 'Cash'] + df.at[df.index[i], 'Holdings']

        return df[['Position', 'Cash', 'Holdings', 'Total']]