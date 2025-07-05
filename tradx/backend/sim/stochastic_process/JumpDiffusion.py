import numpy as np
from tradx.backend.sim.stochastic_process.StochasticProcess import StochasticProcess

class JumpDiffusion(StochasticProcess):
    """
    Merton's Jump Diffusion Prozess.
    Kombiniert GBM mit zufälligen Sprüngen (Poisson-Zählprozess und normalverteilte Jumps).
    """

    def __init__(self, mu, sigma, lamb, mu_j, sigma_j, dt=1/252):
        """
        :param mu: Drift des normalen Prozesses
        :param sigma: Volatilität des normalen Prozesses
        :param lamb: Intensität (λ) des Poisson-Prozesses (durchschnittliche Anzahl Jumps pro Jahr)
        :param mu_j: Erwartungswert der Jump-Größen (logarithmisch)
        :param sigma_j: Volatilität der Jump-Größen (logarithmisch)
        :param dt: Zeitschritt
        """
        self.mu = mu
        self.sigma = sigma
        self.lamb = lamb
        self.mu_j = mu_j
        self.sigma_j = sigma_j
        self.dt = dt

    def simulate_path(self, S0, n_steps, n_paths=1):
        paths = np.zeros((n_paths, n_steps))
        paths[:, 0] = S0
        for t in range(1, n_steps):
            Z = np.random.normal(size=n_paths)
            J = np.random.poisson(self.lamb * self.dt, size=n_paths)
            Y = np.random.normal(self.mu_j, self.sigma_j, size=n_paths) * J
            dS = (self.mu - 0.5 * self.sigma**2) * self.dt + self.sigma * np.sqrt(self.dt) * Z + Y
            paths[:, t] = paths[:, t - 1] * np.exp(dS)
        return paths