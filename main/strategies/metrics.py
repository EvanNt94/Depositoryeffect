import pandas as pd
from Depositoryeffect.main.portfolio.Portfolio import Portfolio
from Logger import Logger

import numpy as np

def calc_diff_disp_norm(apyDispo, apyNormal):
    return apyDispo - apyNormal

def calculate_metrics(portfolio: Portfolio, risk_free_rate: float = 0.0) -> pd.Series:
    """
    Berechnet zentrale Performance-Kennzahlen für ein Portfolio.

    Parameter
    ----------
    portfolio : Portfolio
        Instanz deiner Portfolio-Klasse.
    risk_free_rate : float, optional
        Tagesbasierter risikofreier Zinssatz (z.B. 0.0). Standard: 0.

    Returns
    -------
    pd.Series
        Series mit Metriken:
        - avg_return_daily
        - sigma_daily
        - sharpe_ratio
        - max_drawdown
        - apy
    """
    # Zeitreihe der Portfoliowerte
    series = portfolio.value_series().sort_index()

    # Tagesrenditen
    daily_returns = series.pct_change().dropna()

    if daily_returns.empty:
        raise ValueError("Portfolio enthält zu wenige Datenpunkte für Metrik-Berechnung.")

    # Durchschnittsrendite & Volatilität
    avg_return = daily_returns.mean()
    sigma = daily_returns.std()

    # Sharpe Ratio (annualisiert, 252 Handelstage)
    sharpe_ratio = np.nan
    if sigma != 0:
        sharpe_ratio = ((avg_return - risk_free_rate) / sigma) * np.sqrt(252)

    # Max Drawdown
    cum_max = series.cummax()
    drawdowns = (series - cum_max) / cum_max
    max_drawdown = drawdowns.min()

    # APY (Annual Percentage Yield)
    years = (series.index[-1] - series.index[0]).days / 365.25
    apy = np.nan
    if years > 0:
        apy = (series.iloc[-1] / series.iloc[0]) ** (1 / years) - 1

    metrics = pd.Series(
        {
            "avg_return_daily": avg_return,
            "sigma_daily": sigma,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "apy": apy,
        }
    )

    # Logge die Ergebnisse
    Logger(__name__).logger.info(f"Portfolio-Metriken:\n{metrics}")

    return metrics
