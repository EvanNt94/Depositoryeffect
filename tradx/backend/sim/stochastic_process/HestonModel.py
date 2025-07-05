import numpy as np
from tradx.backend.sim.stochastic_process.StochasticProcess import StochasticProcess

class HestonProcess(StochasticProcess):
    def __init__(self, S0, v0, mu, kappa, theta, sigma, rho, dt):
        self.S0 = S0      # Initialer Preis
        self.v0 = v0      # Initiale Varianz
        self.mu = mu      # Drift (Rendite)
        self.kappa = kappa  # Mean-Reversion-Geschwindigkeit
        self.theta = theta  # Langfristige mittlere Varianz
        self.sigma = sigma  # Volatilität der Volatilität
        self.rho = rho    # Korrelation zwischen Preis und Varianz
        self.dt = dt      # Zeitschritt

    def simulate(self, T, steps, n_paths=1)-> tuple[np.ndarray, np.ndarray]:
        dt = self.dt
        N = steps
        S = np.zeros((n_paths, N))
        v = np.zeros((n_paths, N))
        S[:, 0] = self.S0
        v[:, 0] = self.v0

        for t in range(1, N):
            z1 = np.random.normal(size=n_paths)
            z2 = self.rho * z1 + np.sqrt(1 - self.rho**2) * np.random.normal(size=n_paths)

            v[:, t] = np.abs(
                v[:, t - 1] + self.kappa * (self.theta - v[:, t - 1]) * dt + self.sigma * np.sqrt(v[:, t - 1] * dt) * z1
            )
            S[:, t] = S[:, t - 1] * np.exp(
                (self.mu - 0.5 * v[:, t - 1]) * dt + np.sqrt(v[:, t - 1] * dt) * z2
            )

        return S, v