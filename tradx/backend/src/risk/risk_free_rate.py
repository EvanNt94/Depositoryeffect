import requests
from dotenv import load_dotenv
load_dotenv()
import os

def get_risk_free_rate(currency: str = "USD") -> float:
    if currency == "USD":
        try:
            r = requests.get("https://api.stlouisfed.org/fred/series/observations",
                             params={
                                 "series_id": "GS1",
                                 "api_key": os.getenv("FRED_API_KEY"),
                                 "file_type": "json",
                                 "sort_order": "desc",
                                 "limit": 1
                             }).json()
            print(r)
            return float(r["observations"][0]["value"]) / 100
        except Exception as e:
            print(e)
            return 0.05  
    elif currency == "EUR":
        try:
            ecb = requests.get("https://api.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")
            return 0.035  
        except Exception:
            return 0.035
    return 0.01
