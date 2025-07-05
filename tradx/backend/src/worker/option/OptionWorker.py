"""
DEPRECATED

"""

import pandas as pd
import yfinance as yf
from tqdm import tqdm
from tradx.backend.src.init.risk_free import get_latest_risk_free_rate
from py_vollib.black_scholes.greeks.analytical import delta, gamma, vega, theta, rho
from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.implied_volatility import implied_volatility
from multiprocessing import Queue 
from datetime import datetime
import numpy as np



def cast_float(x):
    return float(x) if isinstance(x, (np.float32, np.float64)) else x

def generate_readable_symbol(ticker: str, expiry: str, strike: float, callput: str) -> str:
    return f"{ticker}_{expiry}_{callput.upper()}_{strike:.2f}"

def main(full_search=False):
    # build_underlying()

    STOCK_DB = StockDB(Queue())
    ISINS = STOCK_DB.get_isins()

    q = Queue()
    option_db = OptionDBWorker(q)
    option_db.start()

    for isin in tqdm(ISINS):
        # print(isin)
        underlying = get_or_build_underlying(isin, option_db, STOCK_DB)
        if not (underlying.get("has_option", False) or full_search):
            continue
        try:
            ticker_yf  = yf.Ticker(isin)
        except ValueError as e:
            print(e)
        expiries = ticker_yf.options
        if len(expiries) == 0:
            continue
        if not underlying:
            print("No underlying.")
            continue
        ticker = underlying["ticker"]
        for expiry in expiries:
            try:
                chain = ticker_yf.option_chain(expiry)
            except Exception as E:
                print(f"Error fetching option chain for {isin} on {expiry}: {expiry}. Skipping expiry.")
                continue

            pending_price_inserts = []

            for df, ctype in [(chain.calls, "CALL"), (chain.puts, "PUT")]:
                for _, row in df.iterrows():
                    option_symbol = generate_occ_symbol(ticker, expiry, row["strike"], ctype)
                    if not option_db.is_alive():
                        raise RuntimeError("option db died.")
                    if  option_db.queue.full():
                        raise RuntimeError("Queue full.")
                    option_db.queue.put({
                        "table": options_schema.name,
                        "underlying_id": underlying["id"],
                        "type": ctype,
                        "strike": row["strike"],
                        "expiry": expiry,
                        "option_symbol": option_symbol
                    })
                    S = ticker_yf.info.get("regularMarketPrice", None)
                    K = row["strike"]
                    expiry_dt = datetime.strptime(expiry, "%Y-%m-%d").astimezone()
                    now = datetime.now().astimezone()
                    t = max((expiry_dt - now).days, 1) / 365        # Zeit bis Verfall (in Jahren)
                    r = get_latest_risk_free_rate()
                    flag = 'c' if ctype == "CALL" else "p"      
                    iv = row.get("impliedVolatility", None)
                    if all([S, K, t, r, iv]) and iv > 0:
                        d = delta(flag, S, K, t, r, iv)
                        g = gamma(flag, S, K, t, r, iv)
                        th = theta(flag, S, K, t, r, iv)
                        v = vega(flag, S, K, t, r, iv)
                        rh = rho(flag, S, K, t, r, iv)
                        mp = black_scholes(flag, S, K, t, r, iv)
                    else:
                        d = g = th = v = rh = mp = None
                    insert_data = {
                        "spot_price": ticker_yf.info.get("regularMarketPrice", None),
                        "timestamp": datetime.now().astimezone(),
                        "bid": row["bid"],
                        "ask": row["ask"],
                        "last": row["lastPrice"],
                        "volume": int(row["volume"]) if pd.notnull(row["volume"]) else None,
                        "oi": int(row["openInterest"]) if pd.notnull(row["openInterest"]) else None,
                        "iv": row.get("impliedVolatility", None),
                        "iv_bid": None,
                        "iv_ask": None,
                        "delta": d,
                        "gamma": g,
                        "theta": th,
                        "vega": v,
                        "rho": rh,
                        "model_price": mp,
                        "source": "yfinance",
                        "incomplete": True,
                        "anomaly_score": None,
                        "bid_size": None,
                        "ask_size": None,
                    }
                    insert_data = {k: cast_float(v) for k, v in insert_data.items()}
                    pending_price_inserts.append({
                        "table": option_prices_schema.name,
                        "lookup": {
                            "option_symbol": option_symbol
                        },
                        "insert": insert_data
                    })

            for item in pending_price_inserts:
                option_db.queue.put(item)
    option_db.queue.put(None)
    option_db.join()

if __name__ == "__main__":
    main(full_search=True)
