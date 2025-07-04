from main.strategies.strategy import Strategy


class Player:
    def __init__(self, name, initial_capital, strategy: Strategy):
        self.strategy = strategy
        self.name = name
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = []
        self.trades = []
