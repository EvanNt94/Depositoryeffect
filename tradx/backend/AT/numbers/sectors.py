#%%
import json, pandas as pd, os
from dateutil.relativedelta import relativedelta

def get_sector_weights(sector: str):
    with open(f"/Users/a2/code/fin/trade/tradx/data/price/market/AT/sectors/{sector}.json", "r") as f:
        return json.load(f)["stocks"]

def get_ipos(infos, price_dir, output_dir):
    ipos = []
    
    for info in infos:
        try:
            # Versuche das IPO-Datum aus den Infos zu holen
            ipo_date = pd.Timestamp(info['listed_on']['AT'], tz='Europe/Athens').normalize()
        except (KeyError, TypeError, ValueError):
            # Falls `listed_on` nicht vorhanden ist, hole den ersten Eintrag aus den Preisdaten
            ticker = info['ticker_on']['AT']  # Gehe davon aus, dass 'ticker' in jedem Info vorhanden ist
            df_path = os.path.join(price_dir, f"{ticker}.parquet")
            
            try:
                df = pd.read_parquet(df_path)
                ipo_date = pd.Timestamp(df.index[0]).tz_convert('Europe/Athens').normalize()  # Erster Eintrag
            except Exception as e:
                print(f"Fehler beim Lesen der Preisdaten für {ticker}: {e}")
                continue  # Überspringe diesen Ticker, falls es ein Problem gibt
            
            # Füge das Datum zu den Infos hinzu
            info['listed_on'] = {'AT': ipo_date.strftime('%b %d, %Y')}
            
            # Speichere die aktualisierte Info-Datei
            output_path = os.path.join(output_dir, f"{ticker}.json")
            with open(output_path, 'w') as f:
                json.dump(info, f, indent=4)
        
        # Füge das IPO-Datum zur Liste hinzu
        ipos.append(ipo_date)
    
    return ipos

def _generate_index(ws):
    price_dir = "/Users/a2/code/fin/trade/tradx/data/price/company/AT/daily"
    index_dir = "/Users/a2/code/fin/trade/tradx/data/price/market/AT/sectors"
    info_dir = "/Users/a2/code/fin/trade/tradx/data/fundamentals/company/info/AT"
    tickers = [stock[0] for stock in ws]

    infos = [
        json.load(open(os.path.join("/Users/a2/code/fin/trade/tradx/data/fundamentals/company/info/AT", f"{ticker}.json"))) 
        for ticker in tickers
    ]

    ipos = get_ipos(infos, price_dir, info_dir)

    # Erstelle ein Datum für "heute" mit Mitternacht
    today = pd.Timestamp.now(tz='Europe/Athens').normalize()

    start_date_of_index = max(max(ipos), today - relativedelta(years=10))

    dfs = {
        ticker: pd.read_parquet(os.path.join(price_dir, f"{ticker}.AT.parquet"))
        for ticker in tickers
    }

    # Sicherstellen, dass die Indizes datetime-kompatibel sind
    for ticker, df in dfs.items():
        if not isinstance(df.index, pd.DatetimeIndex):
            dfs[ticker].index = pd.to_datetime(df.index).tz_localize('Europe/Athens').normalize()

    # Check that each dataframe has data at or before the start date
    for ticker, df in dfs.items():
        if df.index[0] > start_date_of_index:
            start_date_of_index = df.index[0]
    
    so = [max([info[l] for l in ["float_shares", "shares_outstanding", "implied_shares_outstanding"] if info[l] is not None]) for info in infos]

    start_prices = [dfs[ticker].loc[start_date_of_index, "Close"] * so[n] for n, ticker in enumerate(tickers)]
    weights = [price / sum(start_prices) for price in start_prices]

    dates = pd.date_range(start=start_date_of_index, end=today, freq='D', tz='Europe/Athens').normalize()
    index_values = []
    # Generiere den Index
    for date in dates:
        index_value = sum(
            dfs[ticker].loc[date, "Close"] * weights[i] 
            for i, ticker in enumerate(tickers) 
            if date in dfs[ticker].index
        )
        index_values.append(index_value)
    
    index_df = pd.DataFrame({"date": dates, "value": index_values})
    index_df.to_parquet(os.path.join(index_dir, f"{sector.replace(" ", "").lower().replace("/", "-")}.parquet"))

if __name__ == "__main__":
    with open("/Users/a2/code/fin/trade/tradx/data/price/market/AT/sectors/info.json", "r") as f:
        info = json.load(f)
    for sector in info:
        print(sector)
        ws = get_sector_weights(sector.replace(" ", "").lower().replace("/", "-"))
        _generate_index(ws)