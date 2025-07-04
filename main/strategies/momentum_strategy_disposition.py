
import pandas as pd
from strategies.momentum_strategy import MomentumStrategy

class MomentumDispositionStrategy(MomentumStrategy):

    def generate_signals(self) -> pd.DataFrame:
        df = self.data.copy()
        df['Signal'] = 0
        holding = False
        buy_price = 0

        for i in range(1, len(df)):
            price = df['Close'].iloc[i]

            if not holding:
                df.iloc[i, df.columns.get_loc('Signal')] = 1  # Buy
                holding = True
                buy_price = price
            else:
                change = (price - buy_price) / buy_price
                if change > 0.05:
                    df.iloc[i, df.columns.get_loc('Signal')] = -1  # Sell
                    holding = False
                    buy_price = 0
                else:
                    df.iloc[i, df.columns.get_loc('Signal')] = 0  # Hold

        return df