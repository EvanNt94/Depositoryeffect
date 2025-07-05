from backend.sim.derivative.base import Derivative
import numpy as np


class EuropeanCall(Derivative):
    """
    Europäischer Call-Optionskontrakt.

    Diese Klasse modelliert eine europäische Call-Option basierend auf einem gegebenen stochastischen Prozess 
    für den zugrunde liegenden Vermögenswert.

    Attribute:
        strike (float): Ausübungspreis der Option.
        maturity (float): Laufzeit der Option in Jahren.
        underlying_process (StochasticProcess): Stochastischer Prozess des Underlyings.

    Methoden:
        payoff(path: np.ndarray) -> np.ndarray:
            Berechnet den Auszahlungswert der Option für gegebene Pfade des Underlyings zum Fälligkeitszeitpunkt.
    """
    def __init__(self, strike, maturity, underlying_process):
        super().__init__(underlying_process, maturity)
        self.strike = strike

    def payoff(self, path):
        """
        Berechnet den Auszahlungswert (Payoff) einer europäischen Call-Option 
        zum Fälligkeitszeitpunkt für gegebene Simulationspfade des Underlyings.

        Args:
            path (np.ndarray): Ein 2D-Array mit simulierten Pfaden des Underlyings. 
                               Jede Zeile repräsentiert einen Pfad, die letzte Spalte 
                               enthält den Endwert zur Fälligkeit.

        Returns:
            np.ndarray: Array der Auszahlungswerte (Payoffs) für jeden Pfad.
        """
        terminal_values = path[:, -1]
        return np.maximum(terminal_values - self.strike, 0)
    




from backend.sim.derivative.base import Derivative


class EuropeanPut(Derivative):
    """
    A European put option that can only be exercised at maturity.
    """

    def __init__(self, strike: float, underlying_process, maturity: float):
        """
        Initialize a European put option.

        Parameters:
        - strike (float): The strike price of the option.
        - maturity (float): The time to maturity (in years).
        """
        super().__init__(underlying_process, maturity)
        self.strike = strike


    def payoff(self, path: np.ndarray) -> np.ndarray:
        """
        Calculate the payoff of the European put option.

        Parameters:
        - spot (float): The spot price of the underlying asset at maturity.

        Returns:
        - float: The payoff of the option.
        """
        terminal_values = path[:, -1]
        return np.maximum(self.strike - terminal_values, 0)
