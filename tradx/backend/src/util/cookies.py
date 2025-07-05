import tradx
import os

def load_cookies(filename:str):
    path = os.path.join(tradx.TRADX_BASE, "data", "cookies", filename)
    s = open(path).read()
    cc = s.split("; ")
    dd = {}
    for c in cc:
        i = c.find("=")
        dd[c[:i]] = c[i+1:]
    return dd