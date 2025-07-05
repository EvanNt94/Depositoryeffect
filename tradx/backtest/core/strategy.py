import pandas as pd

class Strategy:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def generate_signals(self) -> pd.DataFrame:
        raise NotImplementedError("Bitte generate_signals() in Subklasse implementieren.")