import json

import numpy as np
import pandas as pd
from Logger import Logger
from portfolio.Portfolio import Portfolio


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
    if not isinstance(series.index, pd.DatetimeIndex):
        raise ValueError("Portfolio-Zeitreihe benötigt DatetimeIndex.")

    # Tagesrenditen
    daily_returns = series.pct_change(fill_method=None).dropna()

    if daily_returns.empty:
        raise ValueError(
            "Portfolio enthält zu wenige Datenpunkte für Metrik-Berechnung."
        )

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
    start = series.iloc[0]
    end = series[series.notna()].iloc[-1]
    apy = np.nan

    print(f"[DEBUG] Startwert: {start}, Endwert: {end}, Jahre: {years}")
    if pd.notna(start) and pd.notna(end):
        if start > 0 and years > 0.01:
            try:
                apy = (end / start) ** (1 / years) - 1
            except Exception as e:
                print(f"[ERROR] Fehler bei APY-Berechnung: {e}")
        else:
            print(
                f"[WARN] Ungültige Werte für APY-Berechnung: start={start}, years={years}"
            )
    else:
        print(f"[WARN] Start oder Endwert ist NaN: start={start}, end={end}")

    safe_dict = {
        k.strftime("%Y-%m-%d %H:%M"): v for k, v in portfolio.portfolio.items()
    }

    safe_amount = {str(k): v for k, v in portfolio.current_amount.items()}

    metrics = {
        "avg_return_daily": avg_return,
        "sigma_daily": sigma,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "apy": apy,
        "start_amount": portfolio.amount_start,
        "end_amount": portfolio.current_amount_value,
        "amount_list": safe_amount,
        "portfolio_history": safe_dict,
    }

    # Logge die Ergebnisse
    # Logger(__name__).logger.info(f"Portfolio-Metriken:\n{metrics}")

    return metrics
