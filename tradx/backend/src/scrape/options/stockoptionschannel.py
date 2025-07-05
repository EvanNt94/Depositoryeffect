import requests
from datetime import datetime
import pandas as pd
from tradx.backend.util.cookies import load_cookies


DELAY = 10 # as in robots.txt

def get_expirations(ticker: str):
    today = datetime.today()
    base_url = f"https://www.stockoptionschannel.com/symbol/?symbol={ticker}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    cookies = load_cookies("stockoptionschannel.cookies")
    resp  = requests.get(base_url, headers=headers, )
    html = resp.text

    df = pd.read_html(html)
    try:
        df = df[7]
    except:
        raise RuntimeError("COOKIE HAS TO BE VALIDATED FOR www.stockoptionschannel.com")
    aa = [datetime.strptime(x, "%B %d, %Y") for x in df.iloc[:, 0] if datetime.strptime(x, "%B %d, %Y") >= today]
    return aa




if __name__ == "__main__":
    print(get_expirations("AAPL"))
