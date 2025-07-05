
import numpy as np
from tradx.backend.sim.stochastic_process.StochasticProcess import StochasticProcess

class GeometricBrownianMotion(StochasticProcess):
    def __init__(self, mu, sigma, T, dt, n_paths):
        self.mu = mu
        self.sigma = sigma
        self.T = T
        self.dt = dt
        self.n_paths = n_paths
        self.n_steps = int(T / dt)

    def simulate(self):
        t = np.linspace(0, self.T, self.n_steps)
        W = np.cumsum(np.random.normal(0, np.sqrt(self.dt), size=(self.n_paths, self.n_steps)), axis=1)
        X = (self.mu - 0.5 * self.sigma ** 2) * t + self.sigma * W
        return np.exp(X)