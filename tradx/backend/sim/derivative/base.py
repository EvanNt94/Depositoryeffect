from abc import ABC, abstractmethod

from tradx.backend.sim.stochastic_process import StochasticProcess

class Derivative(ABC):
    """
    Abstrakte Klasse für derivative Finanzprodukte.
    """

    def __init__(self, underlying_process:StochasticProcess, maturity:float):
        """
        :param underlying_process: Instanz eines StochasticProcess
        """
        self.underlying_process = underlying_process
        self.maturity = maturity

    @abstractmethod
    def payoff(self, path):
        """
        Berechnet den Payoff basierend auf einem Pfad.
        :param path: np.array eines simulierten Pfads
        """
        pass

    def simulate(self, S0, n_steps, n_paths=1):
        """
        Simuliert den zugrundeliegenden Prozess.
        """
        return self.underlying_process.simulate_path(S0, n_steps, n_paths)