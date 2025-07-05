import json
import os

wd = "/Users/a2/code/fin/trade/data/news/comp/AT"
files = os.listdir(wd)

map_gr_en:dict = json.load(open("/Users/a2/code/fin/trade/static/tickers/AT_gr_en.json"))

def detect_language(text):
    greek_count = 0
    english_count = 0

    for char in text:
        # Überprüfen, ob das Zeichen ein griechischer Buchstabe ist
        if '\u0370' <= char <= '\u03FF' or '\u1F00' <= char <= '\u1FFF':
            greek_count += 1
        # Überprüfen, ob das Zeichen ein englischer Buchstabe ist (Lateinische Buchstaben)
        elif 'A' <= char <= 'Z' or 'a' <= char <= 'z':
            english_count += 1

    # Rückgabe basierend auf der Anzahl der erkannten Buchstaben
    if greek_count > english_count:
        return "Greek"
    elif english_count > greek_count:
        return "English"
    else:
        return "Unknown"


for f in files:
    end:str = f.split(".")[-1]
    if end == "pdf":
        continue
    if end not in map_gr_en.keys() and end not in map_gr_en.values():
        selected =f.split(".")[0] 
        if detect_language(end) == "Greek":
            for ff in files:
                if ff.endswith(".pdf"):
                    continue
                if selected == ff.split(".")[0] and end != ff.split(".")[1]:
                    map_gr_en[end] = ff.split(".")[1] 


json.dump(map_gr_en, open("/Users/a2/code/fin/trade/static/tickers/AT_gr_en.json", "w"))