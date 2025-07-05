"""
Checks:     
 - asset.stock -> option.underlying
 - option.underlying -> option.options


"""

from datetime import datetime
import os
import yfinance as yf
from tradx.backend.src.worker.db.StockDBWorker import *
from tradx.backend.src.worker.db.OptionDBHandler import *
import asyncio
import requests
import numpy as np



def cast_float(x):
    return float(x) if isinstance(x, (np.float32, np.float64)) else x


def generate_occ_symbol(ticker: str, expiry: str, strike: float, callput: str) -> str:
    """
    OCC: TickerYYMMDDCPStrike × 1000
    """
    expiry_fmt = expiry.replace("-", "")[2:]  # z. B. "2025-06-06" → "250606"
    cp_flag = "C" if callput.upper() == "CALL" else "P"
    strike_formatted = f"{int(strike * 1000):08d}"
    return f"{ticker.upper()}{expiry_fmt}{cp_flag}{strike_formatted}"


async def check_options_availability(ticker: yf.Ticker, expiries: tuple[str], underlying_id: int, ticker_str: str):
    for expiry in expiries:
        try:
            chain = ticker.option_chain(expiry)
        except Exception as e:
            print(f"  -> Fehler beim Laden der Optionen für {ticker_str} @ {expiry}: {e}")
            continue

        for opt in chain.calls.to_dict("records"):
            strike = cast_float(opt.get("strike"))
            if not isinstance(strike, (float, int)):
                print(f"  -> Ungültiger Strike bei {ticker_str} @ {expiry}: {opt}")
                continue
            payload = {
                "underlying_id": underlying_id,
                "expiry": datetime.strptime(expiry, "%Y-%m-%d").date(),
                "strike": strike,
                "type": "CALL",
                "option_symbol": generate_occ_symbol(ticker_str, expiry, strike, "CALL")
            }
            await insert_option(payload)

        for opt in chain.puts.to_dict("records"):
            strike = cast_float(opt.get("strike"))
            if not isinstance(strike, (float, int)):
                print(f"  -> Ungültiger Strike bei {ticker_str} @ {expiry}: {opt}")
                continue
            payload = {
                "underlying_id": underlying_id,
                "expiry": datetime.strptime(expiry, "%Y-%m-%d").date(),
                "strike": strike,
                "type": "PUT",
                "option_symbol": generate_occ_symbol(ticker_str, expiry, strike, "PUT")
            }
            await insert_option(payload)



async def check_underlying_option_flags():
    debug = os.getenv("DEBUG", False)
    underlyings = await get_all_underlyings()
    print(f"Checking {len(underlyings)} underlyings for option availability...")

    for u in underlyings:
        try:
            ticker_yf = yf.Ticker(u["ticker"])
            opts = ticker_yf.options
            has_options_yf = bool(opts)
        except (requests.exceptions.RequestException, KeyError, IndexError, Exception) as e:
            print(f"  -> Fehler bei {u['ticker']} ({u['isin']}): {e}")
            continue
        if has_options_yf != u["has_option"]:
            payload = {
                "ticker": u["ticker"],
                "isin": u["isin"],
                "has_option": has_options_yf
            }
            await insert_underlying(payload)
            if debug: print(f"  -> Updated has_option for {u['ticker']} ({u['isin']}) to {has_options_yf}")

        if has_options_yf:
            try:
                await check_options_availability(ticker_yf, opts, u["id"], u["ticker"])
            except Exception as e:
                print(f"  -> Fehler beim Abrufen von Optionen für {u['ticker']}: {e}")


async def sync_underlyings_from_asset_stock():
    isins = await get_active_isin_wo_underlying()
    print(f"{len(isins)} ISINs without underlying:")
    for isin in isins:
        print("-", isin)

        # Hole Asset-Daten aus asset.stock
        stock = await get_stock_by_isin(isin)
        if stock is None:
            print(f"  -> Kein Asset-Eintrag für {isin} gefunden, überspringe.")
            continue

        # Baue Payload für neues Underlying
        payload = {
            "ticker": stock["ticker"],
            "isin": stock["isin"],
            "has_option": False
        }

        await insert_underlying(payload)
        print(f"  -> Underlying für {isin} eingefügt.")


async def main():
    await sync_underlyings_from_asset_stock()
    await check_underlying_option_flags()


if __name__ == "__main__":
    asyncio.run(main())