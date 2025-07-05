class MeasureChanger:

    @staticmethod
    def apply_girsanov(process, new_drift):
        """
        Applies Girsanov's theorem to simulate a process under a new drift
        using transformed Brownian motion and Radon-Nikodym density.

        Parameters:
        - process: StochasticProcess with attributes x0, drift, sigma
        - new_drift: function or float; the new drift under the risk-neutral measure

        Returns:
        - A function simulating the process under the new measure
        """
        import numpy as np

        def simulate_under_new_measure(T, N, seed=None):
            dt = T / N
            times = np.linspace(0, T, N)

            if seed is not None:
                np.random.seed(seed)

            W = np.random.normal(0, np.sqrt(dt), size=N)
            W_t = np.cumsum(W)

            mu = process.drift if not callable(process.drift) else np.array([process.drift(t) for t in times])
            nu = new_drift if not callable(new_drift) else np.array([new_drift(t) for t in times])
            sigma = process.sigma

            theta = (mu - nu) / sigma

            # Girsanov transformed Brownian motion
            W_t_girsanov = W_t + np.cumsum(theta * dt)

            # Simulate X under new measure with nu as drift
            X = np.zeros(N)
            X[0] = process.x0
            for t in range(1, N):
                nu_val = nu[t-1] if isinstance(nu, np.ndarray) else nu
                X[t] = X[t-1] + nu_val * dt + sigma * W[t-1]

            # Optional: Radon-Nikodym density for expectation reweighting
            rn_density = np.exp(-np.cumsum(theta * W) - 0.5 * np.cumsum(theta**2) * dt)

            return X, W_t_girsanov, rn_density

        return simulate_under_new_measure

    @staticmethod
    def expectation_under_Q(process, new_drift, f, T, N, M, seed=None):
        """
        Erwartungswert unter neuer Maßnahme (z.B. risk-neutral) via Radon-Nikodym-Reweighting.

        Parameters:
        - process: StochasticProcess mit Attributen x0, drift, sigma
        - new_drift: Ziel-Driftfunktion oder Konstante (unter Q)
        - f: Funktion auf X_T (z.B. Payoff)
        - T: Zeitdauer
        - N: Anzahl Zeitschritte
        - M: Anzahl Pfade
        - seed: Optionaler Seed

        Returns:
        - Erwartungswert von f(X_T) unter Maßnahme Q
        """
        import numpy as np

        dt = T / N
        if seed is not None:
            np.random.seed(seed)

        results = []

        for _ in range(M):
            times = np.linspace(0, T, N)
            W = np.random.normal(0, np.sqrt(dt), size=N)
            W_t = np.cumsum(W)

            mu = process.drift if not callable(process.drift) else np.array([process.drift(t) for t in times])
            nu = new_drift if not callable(new_drift) else np.array([new_drift(t) for t in times])
            sigma = process.sigma

            theta = (mu - nu) / sigma

            X = np.zeros(N)
            X[0] = process.x0
            for t in range(1, N):
                mu_val = mu[t-1] if isinstance(mu, np.ndarray) else mu
                X[t] = X[t-1] + mu_val * dt + sigma * W[t-1]

            term1 = np.cumsum(theta * W)
            term2 = 0.5 * np.cumsum(theta**2) * dt
            Z_T = np.exp(-term1[-1] - term2[-1])

            results.append(f(X[-1]) * Z_T)

        return np.mean(results)