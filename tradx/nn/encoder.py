"""
We have the following data:
time -> positional
vector (open, high, low, volume)
"""

import pandas as pd, datetime

class Encoder:
    def __init__(self, x:pd.DataFrame):
        self.data = x
        self.time_interval = None

    def get_interval(self) :
        return datetime.datetime.fromisoformat(self.data.date[0])-datetime.datetime.fromisoformat(self.data.date[1])
