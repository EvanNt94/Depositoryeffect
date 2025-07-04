import yfinance as yf
import pandas as pd
import numpy as np
from itertools import product
import random
from tqdm import tqdm

# --- 1. Große Baskets (repräsentative Auswahl, Stand 2024) ---
BASKETS = {
    "Nasdaq 100 Tech-Stocks": [
        "AAPL", "MSFT", "GOOGL", "GOOG", "NVDA", "META", "AVGO", "TSLA", "ADBE", "CSCO", "AMD", "INTC", "AMZN", "QCOM", "TXN", "AMAT", "ASML", "LRCX", "ADI", "KLAC", "SNPS", "CRWD", "PANW", "CDNS", "MRVL", "MCHP", "ORCL", "INTU", "WDAY", "TEAM", "ZM"
    ],
    "S&P 500 Large Caps": [
        "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "BRK-B", "NVDA", "TSLA", "UNH", "JPM", "V", "MA", "HD", "PG", "LLY", "XOM", "CVX", "ABBV", "AVGO", "COST", "PEP", "KO", "MRK", "WMT", "BAC", "DIS", "MCD", "ADBE", "CMCSA"
    ],
    "MSCI World Top 50": [
        "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "TSLA", "UNH", "JPM", "V", "MA", "HD", "PG", "LLY", "XOM", "CVX", "ABBV", "AVGO", "COST", "PEP", "KO", "MRK", "WMT", "BAC", "DIS", "MCD", "ADBE", "CMCSA", "BHP", "TM", "SHEL", "TMO", "NVO", "SAP", "LIN", "ORCL", "ASML", "SNY", "AZN", "RDS-A", "RDS-B", "BAYRY", "UL", "NESN", "DHR", "HON", "AMGN", "TXN"
    ],
    "DAX 40": [
        "ADS", "AIR", "ALV", "BAS", "BAYN", "BEI", "BMW", "BNR", "CON", "1COV", "DB1", "DBK", "DHL", "DTE", "ENR", "EOAN", "FME", "FRE", "HEI", "HEN3", "IFX", "LIN", "MRK", "MTX", "MUV2", "PAH3", "PUM", "QIA", "RWE", "SAP", "SIE", "SHL", "SY1", "VOW3", "VNA", "ZAL"
    ],
    "EU Tech Leaders": [
        "ASML", "SAP", "ADYEN", "STM", "NOKIA", "INFN", "AMS", "SIE", "IFX", "NEM", "CAP", "SOP", "ATOS", "WDI", "LOGN", "ROG", "DSY", "SU", "OR", "AIR", "ALV", "BAS", "BAYN", "BEI", "BMW", "BNR", "CON"
    ],
    "Value Stocks (US)": [
        "WFC", "C", "BAC", "CVX", "XOM", "PFE", "VZ", "T", "GM", "F", "INTC", "CSCO", "IBM", "MMM", "GE", "WBA", "KHC", "MO", "TFC", "USB", "MET", "PRU", "AIG", "ALL", "KR", "GIS", "K", "CPB", "HSY", "SJM"
    ],
    "High Dividend Stocks (Global)": [
        "MO", "PM", "T", "VZ", "IBM", "XOM", "CVX", "BHP", "RIO", "SHEL", "ENB", "PFE", "GSK", "UL", "NGG", "TOT", "BCE", "BTI", "EPD", "MPLX", "OKE", "PSX", "SNP", "SU", "TEF", "VOD", "WMB", "ZIM", "FRO", "E", "EQNR"
    ],
    "Emerging Markets Top 30": [
        "TSM", "BABA", "TCEHY", "JD", "PDD", "INFY", "HDB", "VALE", "PBR", "ITUB", "MELI", "YPF", "GGB", "SBER", "GAZP", "LUKOY", "NORN", "YNDX", "MTL", "MBT", "NIO", "XPEV", "LI", "BYD", "JD", "BIDU", "NTES", "CTRP", "ZTO", "EDU"
    ],
    "Green & ESG Stocks": [
        "ORSTED.CO", "VWS.CO", "ENPH", "SEDG", "PLUG", "TSLA", "NIO", "BYD", "FSLR", "NEE", "ED", "REGI", "RUN", "SPWR", "VWDRY", "SGRE.MC", "ALB", "LIN", "NXPI", "AEP", "AES", "AY", "CWEN", "BE", "BLDP", "CVA", "DNNGY", "EVRG", "FANUY", "HASI"
    ],
    "Crypto-Exposed Equities": [
        "COIN", "MSTR", "RIOT", "MARA", "HUT", "BTBT", "BITF", "CAN", "SI", "SBNY", "OSTK", "NVDA", "TSLA", "PYPL", "SQ", "GLXY.TO", "CLSK", "SDIG", "HIVE", "DGHI", "BITF", "BTCS", "BKKT", "CIFR", "GREE", "HUT", "IREN", "WULF", "ARBK", "BRPHF"
    ]
}

START_DATE = "2018-01-01"
END_DATE = "2021-12-31"
WIN_THRESHOLDS = [0.02, 0.05, 0.08, 0.12, 0.20]  # 2%, 5%, 8%, 12%, 20%
LOSS_THRESHOLDS = [-0.05, -0.10, -0.15, -0.20, -0.30]  # -5%, -10%, -15%, -20%, -30%
HOLD_PERIODS = [21, 63, 126, 252, 504]  # 1, 3, 6, 12, 24 Monate (21 Handelstage/Monat)

# --- 2. Kursdaten laden ---
def load_prices(tickers, start, end):
    data = yf.download(tickers, start=start, end=end)["Close"]
    if isinstance(data, pd.Series):
        data = data.to_frame()
    data = data.dropna()
    return data

# --- 3. Auswahlmechanismen für Aktienkäufe nach Verkauf ---
def get_fundamentals(tickers):
    # Holt fundamentale Daten für die Ticker (sofern möglich)
    info = {}
    for t in tickers:
        try:
            yf_t = yf.Ticker(t)
            d = yf_t.info
            info[t] = d
        except Exception:
            info[t] = {}
    return info

def pick_stock(prices, day, strategy, fundamentals=None, last_idx=None):
    tickers = list(prices.columns)
    if strategy == "random":
        return random.choice(tickers)
    elif strategy == "momentum":
        # Höchste 6-Monats-Rendite
        if day < 126:
            return random.choice(tickers)
        returns = (prices.iloc[day-126:day].iloc[-1] / prices.iloc[day-126:day].iloc[0]) - 1
        return returns.idxmax()
    elif strategy == "value":
        # Niedrigstes KGV (sofern verfügbar)
        if fundamentals:
            kgvs = {t: fundamentals[t].get('trailingPE', np.inf) for t in tickers}
            kgvs = {k: v for k, v in kgvs.items() if v is not None and v > 0}
            if kgvs:
                return min(kgvs, key=kgvs.get)
        return random.choice(tickers)
    elif strategy == "low_volatility":
        # Geringste 6-Monats-Volatilität
        if day < 126:
            return random.choice(tickers)
        vol = prices.iloc[day-126:day].pct_change().std()
        return vol.idxmin()
    elif strategy == "mean_reversion":
        # Schlechteste Monatsperformance
        if day < 21:
            return random.choice(tickers)
        perf = (prices.iloc[day-21:day].iloc[-1] / prices.iloc[day-21:day].iloc[0]) - 1
        return perf.idxmin()
    elif strategy == "high_dividend":
        # Höchste Dividendenrendite (sofern verfügbar)
        if fundamentals:
            yields = {t: fundamentals[t].get('dividendYield', 0) for t in tickers}
            yields = {k: v for k, v in yields.items() if v is not None}
            if yields:
                return max(yields, key=yields.get)
        return random.choice(tickers)
    elif strategy == "growth":
        # Platzhalter: Zufall (Wachstum nicht direkt verfügbar)
        return random.choice(tickers)
    elif strategy == "market_cap":
        # Größte Marktkapitalisierung (sofern verfügbar)
        if fundamentals:
            caps = {t: fundamentals[t].get('marketCap', 0) for t in tickers}
            caps = {k: v for k, v in caps.items() if v is not None}
            if caps:
                return max(caps, key=caps.get)
        return random.choice(tickers)
    elif strategy == "equal_weighted":
        # Feste Reihenfolge
        if last_idx is None:
            return tickers[0], 0
        idx = (last_idx + 1) % len(tickers)
        return tickers[idx], idx
    elif strategy == "sector_rotation":
        # Platzhalter: Zufall (Sektor nicht direkt verfügbar)
        return random.choice(tickers)
    else:
        return random.choice(tickers)

# --- 4. Dispositionsstrategie ---
def simulate_dispo_strategy(prices, win_thresh, loss_thresh=None, pick_strategy="random", fundamentals=None):
    n_days = len(prices)
    capital = 1.0
    day = 0
    last_idx = None
    while day < n_days:
        if pick_strategy == "equal_weighted":
            pos, last_idx = pick_stock(prices, day, pick_strategy, fundamentals, last_idx)
        else:
            pos = pick_stock(prices, day, pick_strategy, fundamentals)
        entry_price = prices[pos].iloc[day]
        sell = False
        for d in range(day, n_days):
            current_price = prices[pos].iloc[d]
            ret = (current_price - entry_price) / entry_price
            if ret >= win_thresh:
                sell = True
            elif loss_thresh is not None and ret <= loss_thresh:
                sell = True
            if sell:
                capital *= (current_price / entry_price)
                day = d + 1
                break
        else:
            capital *= (prices[pos].iloc[-1] / entry_price)
            break
    cagr = capital ** (252 / n_days) - 1
    return cagr

# --- 5. Buy-and-Hold-Strategie ---
def simulate_bh_strategy(prices, hold_period, pick_strategy="random", fundamentals=None):
    n_days = len(prices)
    capital = 1.0
    day = 0
    last_idx = None
    while day < n_days:
        if pick_strategy == "equal_weighted":
            pos, last_idx = pick_stock(prices, day, pick_strategy, fundamentals, last_idx)
        else:
            pos = pick_stock(prices, day, pick_strategy, fundamentals)
        entry_price = prices[pos].iloc[day]
        exit_day = min(day + hold_period, n_days - 1)
        exit_price = prices[pos].iloc[exit_day]
        capital *= (exit_price / entry_price)
        day = exit_day + 1
    cagr = capital ** (252 / n_days) - 1
    return cagr

# --- 6. Turnierfunktion ---
def run_tournament():
    results = []
    strategies = [
        "random", "momentum", "value", "low_volatility", "mean_reversion",
        "high_dividend", "growth", "market_cap", "equal_weighted", "sector_rotation"
    ]
    # Anzahl aller Kombinationen berechnen
    n_baskets = len(BASKETS)
    n_strat = len(strategies)
    n_param = len(WIN_THRESHOLDS) * len(LOSS_THRESHOLDS) * len(HOLD_PERIODS)
    total = n_baskets * n_strat * n_strat * n_param
    pbar = tqdm(total=total, desc="Simulation fortschritt")
    for basket_name, basket in BASKETS.items():
        print(f"Lade Daten für Basket: {basket_name}")
        prices = load_prices(basket, START_DATE, END_DATE)
        fundamentals = get_fundamentals(basket)
        for dispo_strategy in strategies:
            for bh_strategy in strategies:
                for win, loss, hold in product(WIN_THRESHOLDS, LOSS_THRESHOLDS, HOLD_PERIODS):
                    cagr_dispo = simulate_dispo_strategy(prices, win, loss, dispo_strategy, fundamentals)
                    cagr_bh = simulate_bh_strategy(prices, hold, bh_strategy, fundamentals)
                    loss_pp = (cagr_bh - cagr_dispo) * 100
                    rel_loss = (loss_pp / (cagr_bh * 100)) * 100 if cagr_bh != 0 else np.nan
                    results.append({
                        'Basket': basket_name,
                        'Dispo_Strategie': dispo_strategy,
                        'BH_Strategie': bh_strategy,
                        'Tickers': ','.join(basket),
                        'Gewinnschwelle_%': win * 100,
                        'Verlustschwelle_%': loss * 100 if loss is not None else None,
                        'Haltedauer_Tage': hold,
                        'CAGR_Dispo': cagr_dispo,
                        'CAGR_BuyHold': cagr_bh,
                        'Verlust_pp': loss_pp,
                        'Relativer_Verlust_%': rel_loss
                    })
                    pbar.update(1)
    pbar.close()
    df = pd.DataFrame(results)
    return df

if __name__ == "__main__":
    df_results = run_tournament()
    print(df_results)
    df_results.to_csv('dispo_turnier_ergebnisse.csv', index=False)
    print('Ergebnisse als CSV gespeichert.')
