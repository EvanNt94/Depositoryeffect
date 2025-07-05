import json
with open("/Users/a2/code/fin/trade/data/NASDAQ/symbols.json") as f:
    nasdaq = json.load(f)

with open("/Users/a2/code/fin/trade/data/FRA/symbols.json") as f:
    fra = json.load(f)



for sn in nasdaq:
    if sn in fra:
        print(sn)