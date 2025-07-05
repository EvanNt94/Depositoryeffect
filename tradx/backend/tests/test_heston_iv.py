import unittest
import numpy as np




class TestHestonProcess(unittest.TestCase):
    def test_simulate_heston_paths(self):
        from tradx.backend.sim.stochastic_process.HestonModel import HestonProcess

        process = HestonProcess(
            mu=0.05,
            kappa=1.0,
            theta=0.04,
            sigma=0.3,
            rho=-0.7,
            v0=0.04,
            S0=100.0,
            dt=1.0 / 252
        )

        n_paths = 10
        prices, variances = [], []

        for _ in range(n_paths):
            S, v = process.simulate(T=1.0, steps=252)
            self.assertEqual(S.shape, (1, 252))
            self.assertEqual(v.shape, (1, 252))
            prices.append(S[0])
            variances.append(v[0])

        prices = np.array(prices)
        variances = np.array(variances)

        self.assertFalse(np.any(np.isnan(prices)))
        self.assertFalse(np.any(np.isnan(variances)))
        self.assertTrue(np.all(prices > 0))
        self.assertTrue(np.all(variances >= 0))

        # Statistische Erwartungswerte prüfen mit Toleranz
        expected_final_price = process.S0 * np.exp(process.mu * 1.0)
        actual_final_price = np.mean(prices[:, -1])
        self.assertAlmostEqual(actual_final_price, expected_final_price, delta=expected_final_price * 0.2)

        expected_variance_mean = process.theta
        actual_variance_mean = np.mean(variances[:, -1])
        self.assertAlmostEqual(actual_variance_mean, expected_variance_mean, delta=expected_variance_mean * 0.3)