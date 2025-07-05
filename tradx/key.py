with open("/Users/a2/.crypted/alphavantage", "r") as f:
    data = f.read()
KEY = data.split("\n")[-2]
