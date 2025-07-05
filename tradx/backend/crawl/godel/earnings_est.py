from selenium import webdriver
import pandas as pd
import datetime
import json, os
import tradx
from pathlib import Path

BASE_URL = "https://api.godelterminal.com/api/earnings-estimates?symbol="

def get_earnings_estimates(ticker:str): # has RUNTIME ERROR
    driver = webdriver.Chrome()
    driver.get("https://app.godelterminal.com")
    data = driver.execute_async_script("""
        const callback = arguments[arguments.length - 1];
        fetch("https://api.godelterminal.com/api/earnings-estimates?symbol="""+ticker+"""")
            .then(resp => resp.json())
            .then(data => callback(data))
            .catch(err => callback({error: err.toString()}));
    """)
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(f"Fehler beim Abrufen: {data['error']}")
    exchange = data["meta"]["exchange"]
    currency = data["meta"]["currency"]
    symbol = data["meta"]["symbol"]
    df = pd.DataFrame(data["earnings_estimate"])
    root_path = Path(tradx.__file__).resolve().parent
    asr_path = os.path.join(root_path, "data", "estimates", "earnings", exchange)
    os.makedirs(asr_path, exist_ok=True)
    today = datetime.date.today().strftime("%Y%m%d")
    df.to_csv(os.path.join(asr_path, symbol+"."+today+".v1.csv"))

    td_5y = datetime.timedelta(days=5 * 365)
    five_years_ago = datetime.date.today() - td_5y
    data = driver.execute_async_script("""
        const callback = arguments[arguments.length - 1];
        fetch("https://api.godelterminal.com/api/earnings?symbol="""+ticker+"""&startDate="""+five_years_ago.strftime("%Y-%m-%d")+"""&endDate="""+datetime.date.today().strftime("%Y-%m-%d")+"""")
            .then(resp => resp.json())
            .then(data => callback(data))
            .catch(err => callback({error: err.toString()}));
    """)
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(f"Fehler beim Abrufen: {data['error']}")
    prior_path = os.path.join(root_path, "data", "estimates", "prior", exchange)
    os.makedirs(prior_path, exist_ok=True)
    df = pd.DataFrame(data["earnings"])
    df.to_csv(os.path.join(prior_path, symbol+"."+today+".v1.csv"))
    return data




if __name__ == "__main__":
    data = get_earnings_estimates("AAPL")
    print(type(data))