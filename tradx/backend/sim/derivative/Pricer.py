import numpy as np
from backend.sim.derivative.base import Derivative
from tradx.backend.sim.stochastic_process.StochasticProcess import StochasticProcess

class Pricer:
    def __init__(self, discount_rate: float = 0.05):
        self.r = discount_rate

    def monte_carlo_price(self, derivative: Derivative, process: StochasticProcess, antithetic: bool = False) -> float:
        paths = derivative.simulate(process.S0, process.n_steps, process.n_paths)
        if paths is None or len(paths) == 0:
            raise ValueError("Simulation lieferte keine gültigen Pfade.")
        if antithetic:
            antithetic_paths = -paths + 2 * process.S0
            paths = np.concatenate([paths, antithetic_paths], axis=0)
        payoffs = np.array([derivative.payoff(path) for path in paths])
        discounted = np.exp(-self.r * derivative.maturity) * np.mean(payoffs)
        return discounted

    def binomial_tree_price(
        self,
        derivative: Derivative,
        S0: float,
        sigma: float,
        steps: int,
        K: float,
        is_call: bool = True
    ) -> float:
        dt = derivative.maturity / steps
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        q = (np.exp(self.r * dt) - d) / (u - d)

        prices = [S0 * (u ** j) * (d ** (steps - j)) for j in range(steps + 1)]
        payoffs = [max(p - K, 0) if is_call else max(K - p, 0) for p in prices]

        for i in range(steps - 1, -1, -1):
            payoffs = [np.exp(-self.r * dt) * (q * payoffs[j + 1] + (1 - q) * payoffs[j]) for j in range(i + 1)]
        return payoffs[0]

    def finite_difference_price(
        self,
        derivative: Derivative,
        S0: float,
        sigma: float,
        S_max: float,
        M: int,
        N: int
    ) -> float:
        K = derivative.strike
        is_call = derivative.is_call
        dt = derivative.maturity / N
        dS = S_max / M
        grid = np.zeros((M + 1, N + 1))
        S_values = np.linspace(0, S_max, M + 1)

        if is_call:
            grid[:, -1] = np.maximum(S_values - K, 0)
        else:
            grid[:, -1] = np.maximum(K - S_values, 0)

        for j in reversed(range(N)):
            for i in range(1, M):
                delta = (grid[i + 1, j + 1] - grid[i - 1, j + 1]) / (2 * dS)
                gamma = (grid[i + 1, j + 1] - 2 * grid[i, j + 1] + grid[i - 1, j + 1]) / (dS ** 2)
                theta = -0.5 * sigma ** 2 * S_values[i] ** 2 * gamma - self.r * S_values[i] * delta + self.r * grid[i, j + 1]
                grid[i, j] = grid[i, j + 1] - dt * theta

            grid[0, j] = 0
            grid[M, j] = S_max - K if is_call else 0

        i = int(S0 / dS)
        w = (S0 - S_values[i]) / dS
        return (1 - w) * grid[i, 0] + w * grid[i + 1, 0]
   
   
    def cos_price( # (Fang & Oosterlee))
        self,
        derivative: Derivative,
        S0: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        N: int = 128,
        L: float = 10
    ) -> float:
        from numpy.fft import fft

        c1 = (r - 0.5 * sigma ** 2) * T
        c2 = sigma ** 2 * T
        a = c1 - L * np.sqrt(c2)
        b = c1 + L * np.sqrt(c2)

        k = np.arange(N)
        u = k * np.pi / (b - a)

        def char_func(u):
            return np.exp(1j * u * c1 - 0.5 * c2 * u ** 2)

        payoff_coef = 2.0 / (b - a) * (
            K * np.sin(u * (b - a)) / (u + (u == 0))  # avoid division by 0
        )

        phi = char_func(u)
        V = np.exp(-r * T) * np.sum(np.real(phi * payoff_coef))

        return V
    
    def fft_price( #  (Carr & Madan)
        self,
        derivative: Derivative,
        S0: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        alpha: float = 1.5,
        N: int = 4096,
        eta: float = 0.25
    ) -> float:
        lambd = 2 * np.pi / (N * eta)
        b = np.log(K) - N * lambd / 2
        u = np.arange(N) * eta
        k = np.arange(N)
        x = b + k * lambd

        def char_func(u):
            return np.exp(1j * u * (np.log(S0)) + T * (1j * u * (r - 0.5 * sigma ** 2) - 0.5 * sigma ** 2 * u ** 2))

        psi = lambda v: np.exp(-r * T) * char_func(v - 1j * (alpha + 1)) / (alpha ** 2 + alpha - v ** 2 + 1j * (2 * alpha + 1) * v)

        SimpsonW = 3 + (-1) ** k
        SimpsonW[0] = 1
        SimpsonW = SimpsonW / 3.0

        fft_func = np.exp(1j * b * u) * psi(u) * eta * SimpsonW
        fft_res = np.fft.fft(fft_func).real
        strikes = np.exp(x)
        i = np.argmin(np.abs(strikes - K))

        return fft_res[i]
    

    def crank_nicolson_price(
        self,
        derivative: Derivative,
        S0: float,
        sigma: float,
        S_max: float,
        M: int,
        N: int
    ) -> float:
        K = derivative.strike
        is_call = derivative.is_call
        dt = derivative.maturity / N
        dS = S_max / M
        S = np.linspace(0, S_max, M + 1)

        V = np.zeros((M + 1, N + 1))
        if is_call:
            V[:, -1] = np.maximum(S - K, 0)
        else:
            V[:, -1] = np.maximum(K - S, 0)

        alpha = 0.25 * dt * ((sigma**2 * (np.arange(M+1))**2) - self.r * np.arange(M+1))
        beta  = -dt * 0.5 * ((sigma**2 * (np.arange(M+1))**2) + self.r)
        gamma = 0.25 * dt * ((sigma**2 * (np.arange(M+1))**2) + self.r * np.arange(M+1))

        A = np.zeros((M - 1, M - 1))
        B = np.zeros((M - 1, M - 1))

        for i in range(M - 1):
            if i > 0:
                A[i, i - 1] = -alpha[i+1]
                B[i, i - 1] =  alpha[i+1]
            A[i, i] = 1 - beta[i+1]
            B[i, i] = 1 + beta[i+1]
            if i < M - 2:
                A[i, i + 1] = -gamma[i+1]
                B[i, i + 1] =  gamma[i+1]

        for j in reversed(range(N)):
            rhs = B @ V[1:M, j + 1]
            V[1:M, j] = np.linalg.solve(A, rhs)
            V[0, j] = 0
            V[M, j] = S_max - K if is_call else 0

        i = int(S0 / dS)
        w = (S0 - S[i]) / dS
        return (1 - w) * V[i, 0] + w * V[i + 1, 0]