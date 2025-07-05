import numpy as np
from tradx.backend.sim.stochastic_process.StochasticProcess import StochasticProcess

class BrownianMotion(StochasticProcess):
    def __init__(self, mu=0.0, sigma=1.0, T=1.0, n_steps=252, dt=None):
        self.mu = mu
        self.sigma = sigma
        self.T = T
        self.n_steps = n_steps
        self.dt = dt if dt is not None else T / n_steps

    def simulate_path(self, n_paths=1):
        dt = self.dt
        steps = self.n_steps
        mu = self.mu
        sigma = self.sigma

        dW = np.random.normal(scale=np.sqrt(dt), size=(n_paths, steps))
        W = np.cumsum(dW, axis=1)
        t = np.linspace(0, self.T, steps)

        # Brownian motion with drift
        X = mu * t + sigma * W
        return X
