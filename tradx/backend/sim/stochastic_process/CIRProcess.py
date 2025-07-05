import numpy as np
from tradx.backend.sim.stochastic_process.StochasticProcess import StochasticProcess

class CIRProcess(StochasticProcess):
    """
    Cox-Ingersoll-Ross (CIR) process for modeling mean-reverting stochastic processes,
    commonly used in interest rate and stochastic volatility modeling.

    dX_t = κ(θ - X_t)dt + σ√(X_t)dW_t

    Parameters:
    - kappa (κ): Speed of mean reversion
    - theta (θ): Long-term mean level
    - sigma (σ): Volatility coefficient
    - x0: Initial value of the process
    """
    def __init__(self, kappa: float, theta: float, sigma: float, x0: float):
        self.kappa = kappa  # Speed of mean reversion
        self.theta = theta  # Long-term mean
        self.sigma = sigma  # Volatility
        self.x0 = x0        # Initial value

    def simulate_path(self, n_steps: int, dt: float = 1/252, n_paths: int = 1) -> np.ndarray:
        paths = np.zeros((n_paths, n_steps))
        paths[:, 0] = self.x0

        for t in range(1, n_steps):
            sqrt_term = np.sqrt(np.maximum(paths[:, t - 1], 0))
            dW = np.random.normal(0, np.sqrt(dt), size=n_paths)
            paths[:, t] = paths[:, t - 1] + self.kappa * (self.theta - paths[:, t - 1]) * dt + self.sigma * sqrt_term * dW

        return paths