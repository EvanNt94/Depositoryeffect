

from abc import ABC, abstractmethod
import numpy as np

class StochasticProcess(ABC):
    def __init__(self, mu: float, sigma: float, T: float, dt: float, n_paths: int):
        self.mu = mu
        self.sigma = sigma
        self.T = T
        self.dt = dt
        self.n_paths = n_paths
        self.n_steps = int(T / dt)
    
    @abstractmethod
    def simulate(self,  *args, **kwargs) -> np.ndarray | tuple[np.ndarray, np.ndarray]:
        pass