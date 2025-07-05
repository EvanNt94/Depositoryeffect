import unittest
import numpy as np

# Minimal-Klasse, die MeasureChanger erwartet
class StochasticProcess:
    def __init__(self, x0, drift, sigma):
        self.x0 = x0            # Anfangswert
        self.drift = drift      # Konstante Drift (float) oder callable
        self.sigma = sigma      # Konstante Volatilität

# Wir importieren MeasureChanger aus deiner Datei.
# Ersetze den Pfad gegebenenfalls, z. B.:
from tradx.backend.sim.MeasureChanger import MeasureChanger

class TestMeasureChanger(unittest.TestCase):
    def setUp(self):
        # Basis-Parameter für alle Tests
        self.x0 = 0.0
        self.mu = 0.5       # Originaldrift
        self.nu = 0.0       # Neue Drift unter Q (z. B. risk-neutral)
        self.sigma = 1.0    # Volatilität
        self.T = 1.0        # Zeithorizont
        self.N = 1000       # Zeitschritte
        self.M = 50000      # Simulationspfade (für Monte-Carlo)
        self.dt = self.T / self.N

        # Erzeugt einen einfachen Prozess mit konstanter Drift und sigma
        self.process = StochasticProcess(
            x0=self.x0,
            drift=self.mu,
            sigma=self.sigma
        )

    def test_simulate_under_new_measure_expectation(self):
        """
        Testet, ob simulate_under_new_measure für f(x)=x ungefähr x0 + nu * T ergibt,
        wenn wir unter Q simulieren (hier nu=0). Da es sich um Monte-Carlo handelt,
        erlauben wir einen kleinen Toleranzbereich.
        """
        nu = self.nu  # neue Drift
        model_simulator = MeasureChanger.apply_girsanov(self.process, nu)

        # Simuliere M Pfade (wir ignorieren W_t_girsanov und rn_density hier)
        final_values = []
        for seed in range(10):  # mehrere Seeds, um Glättung zu erzielen
            X, _, _ = model_simulator(self.T, self.N, seed=seed)
            final_values.append(X[-1])
        sample_mean = np.mean(final_values)

        # Erwartung unter Q von X_T = x0 + nu * T = 0 + 0*1 = 0
        expected = self.x0 + nu * self.T

        # Toleranz wegen Monte-Carlo-Rauschen:
        tol = 0.1  # ±0.1 toleriert
        self.assertAlmostEqual(sample_mean, expected, delta=tol,
            msg=f"Erwarteter Mittelwert ≈ {expected}, gemessen: {sample_mean}")

    def test_expectation_under_Q_linear_payoff(self):
        """
        Testet expectation_under_Q mit f(x)=x (lineare Auszahlung).
        Erwartet wird unter Q: E_Q[X_T] = x0 + nu * T.
        """
        def payoff(x):
            return x

        est = MeasureChanger.expectation_under_Q(
            process=self.process,
            new_drift=self.nu,
            f=payoff,
            T=self.T,
            N=self.N,
            M=self.M,
            seed=42
        )

        expected = self.x0 + self.nu * self.T
        tol = 0.01  # engere Toleranz bei großem M
        self.assertAlmostEqual(est, expected, delta=tol,
            msg=f"Erwarteter E_Q[X_T] ≈ {expected}, gemessen: {est}")

    def test_expectation_under_Q_non_linear_payoff(self):
        """
        Zusätzlicher Test: f(x)=x^2. Unter Q gilt:
        E_Q[X_T^2] = Var_Q[X_T] + (E_Q[X_T])^2.
        Für X_T = x0 + nu*T + sigma*W_T^Q gilt
        Var_Q[X_T] = sigma^2 * T,
        deshalb E_Q[X_T^2] = sigma^2*T + (x0 + nu*T)^2.
        """
        def payoff_squared(x):
            return x * x

        est = MeasureChanger.expectation_under_Q(
            process=self.process,
            new_drift=self.nu,
            f=payoff_squared,
            T=self.T,
            N=self.N,
            M=self.M,
            seed=123
        )

        # Analytischer Wert unter Q: Var = sigma^2 * T; Mittelwert = x0 + nu*T
        analytic = (self.sigma**2) * self.T + (self.x0 + self.nu * self.T)**2

        tol = 0.1  # ±0.1 toleriert
        self.assertAlmostEqual(est, analytic, delta=tol,
            msg=f"Erwarteter E_Q[X_T^2] ≈ {analytic}, gemessen: {est}")

if __name__ == "__main__":
    unittest.main()