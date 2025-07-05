import asyncio
from datetime import datetime
import yfinance as yf
import numpy as np
from datetime import date, datetime
from tradx.backend.src.worker.db.OptionDBHandler import get_option_id_by_symbol, insert_option_price, get_all_underlyings_with_options


def safe_int(x):
    return int(x) if isinstance(x, (int, float)) and not np.isnan(x) else None

def generate_occ_symbol(ticker: str, expiry: str, strike: float, callput: str) -> str:
    """
    OCC: TickerYYMMDDCPStrike × 1000
    """
    expiry_fmt = expiry.replace("-", "")[2:]  # z. B. "2025-06-06" → "250606"
    cp_flag = "C" if callput.upper() == "CALL" or callput.upper() == "C" else "P"
    strike_formatted = f"{int(strike * 1000):08d}"
    return f"{ticker.upper()}{expiry_fmt}{cp_flag}{strike_formatted}"

def cast_float(x):
    return float(x) if isinstance(x, (np.float32, np.float64)) else x


def to_date(expiry):
    return datetime.strptime(expiry, "%Y-%m-%d").date()


async def fetch_and_store_option_prices_for_underlyings():
    """ TODO: contractsize (0.1,...), 
    wann wird gescraped"""
    underlyings = await get_all_underlyings_with_options()
    for underlying in underlyings:
        isin = underlying["isin"]
        underlying_id = underlying["id"]
        try:
            ticker = yf.Ticker(isin)
            expiries = ticker.options
        except Exception as e:
            print(f"Failed to initialize ticker or get expiries for {isin}: {e}")
            continue

        for expiry in expiries:
            await asyncio.sleep(1)
            try:
                chain = ticker.option_chain(expiry)
            except Exception as e:
                print(f"Failed to get option chain for {isin} @ {expiry}: {e}")
                continue
            spot_price = chain.underlying.get("regularMarketPrice", None)
            for opt_type, df in [("C", chain.calls), ("P", chain.puts)]:
                for _, row in df.iterrows():
                    try:
                        strike = row.get("strike")
                        last = row.get("lastPrice")
                        bid = row.get("bid")
                        ask = row.get("ask")
                        volume = row.get("volume")
                        open_interest = row.get("openInterest")

                        if None in (spot_price, strike, last, bid, ask, volume, open_interest):
                            incomplete = True
                        else:
                            incomplete = False

                        symbol = generate_occ_symbol(ticker.ticker, expiry, float(strike), opt_type)
                        option_id = await get_option_id_by_symbol(symbol)
                        if option_id is None:
                            print(f"Unknown option symbol: {symbol}")
                            continue

                        price_payload = {
                            "option_id": option_id,
                            "timestamp": datetime.now().astimezone().replace(microsecond=0).astimezone(),
                            "spot_price": spot_price,
                            "bid": cast_float(bid),
                            "bid_size": None,
                            "ask": cast_float(ask),
                            "ask_size": None,
                            "last": cast_float(last),
                            "volume": safe_int(volume),
                            "oi": safe_int(open_interest),
                            "source": "yfinance",
                            "incomplete": incomplete
                        }
                        await insert_option_price(price_payload)
                    except Exception as e:
                        print(f"Failed to insert price for {row.get('contractSymbol')} ({isin}): {e}")

async def main():
    await fetch_and_store_option_prices_for_underlyings()

if __name__ == "__main__":
    asyncio.run(main())