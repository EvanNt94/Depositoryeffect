from key import KEY as key
import requests
# https://www.tipranks.com/stocks
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=&apikey={key}'
r = requests.get(url)
data = r.json()

print(data)