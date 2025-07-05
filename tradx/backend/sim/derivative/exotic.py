import numpy as np
from backend.sim.derivative.base import Derivative

class AsianOption(Derivative):
    """
    Repräsentiert eine asiatische Option, bei der der Payoff auf dem durchschnittlichen Preis des Underlyings basiert.
    
    Unterstützt sowohl 'average price' als auch 'average strike' Varianten, sowie 'call' und 'put'.
    """

    def __init__(self, strike, option_type="call", average_type="arithmetic", average_on="price"):
        """
        :param strike: Strike-Preis der Option.
        :param option_type: 'call' oder 'put'.
        :param average_type: 'arithmetic' oder 'geometric'.
        :param average_on: 'price' für average-price oder 'strike' für average-strike Option.
        """
        self.strike = strike
        self.option_type = option_type
        self.average_type = average_type
        self.average_on = average_on

    def get_average(self, path):
        if self.average_type == "arithmetic":
            return np.mean(path)
        elif self.average_type == "geometric":
            return np.exp(np.mean(np.log(path)))
        else:
            raise ValueError("Unknown average type")

    def get_payoff(self, path):
        avg = self.get_average(path)
        if self.average_on == "price":
            effective_strike = self.strike
            effective_price = avg
        elif self.average_on == "strike":
            effective_strike = avg
            effective_price = path[-1]
        else:
            raise ValueError("Unknown average_on type")

        if self.option_type == "call":
            return max(effective_price - effective_strike, 0)
        elif self.option_type == "put":
            return max(effective_strike - effective_price, 0)
        else:
            raise ValueError("Unknown option type")
        

class BarrierOption(Derivative):
    """
    Modelliert eine Barriere-Option (Knock-In oder Knock-Out).

    Attributes:
        barrier_level (float): Das Preisniveau der Barriere.
        barrier_type (str): 'knock-in' oder 'knock-out'.
        direction (str): 'up' oder 'down' für Barrieren, die von unten oder oben getriggert werden.
    """

    def __init__(self, barrier_level: float, barrier_type: str, direction: str, strike: float):
        self.barrier_level = barrier_level
        self.barrier_type = barrier_type.lower()
        self.direction = direction.lower()
        self.strike = strike

    def is_active(self, price_path: list[float]) -> bool:
        """
        Prüft, ob die Barriere ausgelöst wurde.

        Args:
            price_path (list[float]): Die simulierten Asset-Preise.

        Returns:
            bool: True, wenn die Barrierebedingung erfüllt ist, sonst False.
        """
        if self.direction == "up":
            triggered = any(p >= self.barrier_level for p in price_path)
        elif self.direction == "down":
            triggered = any(p <= self.barrier_level for p in price_path)
        else:
            raise ValueError("Ungültige Barrierenrichtung")

        if self.barrier_type == "knock-in":
            return triggered
        elif self.barrier_type == "knock-out":
            return not triggered
        else:
            raise ValueError("Ungültiger Barriere-Typ")
    def get_payoff(self, price_path: list[float]) -> float:
        """
        Berechnet den Payoff der Option, abhängig von der Barriere und dem finalen Preis.

        Args:
            price_path (list[float]): Die simulierten Asset-Preise.

        Returns:
            float: Der Payoff (>= 0) der Option.
        """
        if not self.is_active(price_path):
            return 0.0
        final_price = price_path[-1]
        return max(final_price - self.strike, 0.0)  # Call-Option angenommen