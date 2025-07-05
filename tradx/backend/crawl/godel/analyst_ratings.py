from selenium import webdriver
import pandas as pd
import datetime
import json, os
import tradx
from pathlib import Path

BASE_URL = "https://api.godelterminal.com/api/analyst-ratings?symbol="

def get_analyst_ratings(ticker:str): # has RUNTIME ERROR
    driver = webdriver.Chrome()
    driver.get("https://app.godelterminal.com")
    data = driver.execute_async_script("""
        const callback = arguments[arguments.length - 1];
        fetch("https://api.godelterminal.com/api/analyst-ratings?symbol="""+ticker+"""")
            .then(resp => resp.json())
            .then(data => callback(data))
            .catch(err => callback({error: err.toString()}));
    """)
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(f"Fehler beim Abrufen: {data['error']}")
    exchange = data["meta"]["exchange"]
    currency = data["meta"]["currency"]
    symbol = data["meta"]["symbol"]
    df = pd.DataFrame(data["ratings"])
    df["currency"] = currency
    root_path = Path(tradx.__file__).resolve().parent
    asr_path = os.path.join(root_path, "data", "ratings", exchange)
    os.makedirs(asr_path, exist_ok=True)
    df.to_csv(os.path.join(asr_path, symbol+"."+datetime.date.today().strftime("%Y%m%d")+".v1.csv"))





if __name__ == "__main__":
    data = get_analyst_ratings("AAPL")
    print(data)