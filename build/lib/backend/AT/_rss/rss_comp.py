"""
this is a script we want to run to notify us about some changes. There should be a dev that integrates the new shit.
propably not time intensive, jsut adding some strings to dbs...


we add notify_change objects in the respective stock exchange folders in the following format:
filename: id.TICKER
content:
published [s: ISO 8601]
Title
Link
Link-PDF
Summary


There is also the pdf for the filing with id.pdf in the same folder.
todo: - als ticker
"""
from tradx import config
from datetime import datetime, timezone
import feedparser, requests
import json
import re, os

def extract_hrefs(html_string):
    # Regex zum Extrahieren von href-Werten
    href_pattern = r'href=["\'](.*?)["\']'
    # Alle Übereinstimmungen finden
    hrefs = re.findall(href_pattern, html_string)
    return hrefs


### this is athex rss for that use case 
### later make this a wrapper for all sx//s

def is_younger(date1: str, date2: str) -> bool:
    """
    Vergleicht zwei Datumsstrings im ISO 8601-Format und gibt zurück, 
    ob date1 jünger (später) als date2 ist.

    Args:
    date1 (str): Erster Datumstring im ISO 8601-Format (z.B. '2024-09-17T10:00:00Z').
    date2 (str): Zweiter Datumstring im ISO 8601-Format (z.B. '2024-09-16T10:00:00Z').

    Returns:
    bool: True, wenn date1 jünger als date2 ist, sonst False.
    """
    # Konvertiere die Strings in datetime-Objekte
    dt1 = datetime.fromisoformat(date1.replace("Z", "+00:00"))
    dt2 = datetime.fromisoformat(date2.replace("Z", "+00:00"))
    
    # Überprüfen, ob dt1 später (jünger) ist als dt2
    return dt1 > dt2

def add_link(l:str)-> None: # maybe useless
    p = ""
    with open(p, "r") as f :
        ll = json.load(f)
    ll.append(l)
    with open(p, "w") as f:
        json.dump(ll, p)

def main():
    name_ticker_map_gr:dict = json.load(open(os.path.join(config.BASE_TRADX_DIR, "static/tickers/AT_name_ticker_gr.json")))
    named_tickers_gr = name_ticker_map_gr.values()
    name_ticker_map_en:dict = json.load(open(os.path.join(config.BASE_TRADX_DIR, "static/tickers/AT_name_ticker_en.json")))
    named_tickers_en = name_ticker_map_en.values()


    ## english
    p_athex = os.path.join(config.BASE_TRADX_DIR, "data/news/comp/AT")
    url = "https://www.athexgroup.gr/web/guest/rss-feeds/-/asset_publisher/companiesrss/custom-rss"
    feed = feedparser.parse(url)
    with open(p_athex+"/last_entry.txt", "r") as f:
        last = f.read()
    # dict_keys(['title', 'title_detail', 'links', 'link', 'authors', 'author_detail', 'author', 'id', 'guidislink', 'updated', 'updated_parsed', 'published', 'published_parsed', 'content', 'summary', 'hlxcd_company-data-language-id', 'hlxcd_company-name', 'hlxcd_company-ticker-symbol', 'hlxcd_helex-company-data'])
    # note: first entries are younger than later ones

    for entry in feed.entries:
        birth = entry.published
        
        if not is_younger(birth, last):
            break

        link = entry.link
        hrefs = extract_hrefs(requests.get(link).text)
        for l in hrefs:
            if l.startswith("/documents"):
                if "Cookies" in l:
                    continue
                link_pdf = "https://www.athexgroup.gr" + l
                break
        else:
            link_pdf = ""

        sum = entry.summary
        ident = link.split("/")[-1]
        title = entry.title
        text = f"{birth}\n{title}\n{link}\n{link_pdf}\n{sum}"
        ticker = entry["hlxcd_company-ticker-symbol"]

        """ 
        temporary company name scrape
        """
        if ticker not in named_tickers_en:
            name_ticker_map_en[entry["hlxcd_company-name"]] = ticker



        with open(p_athex + "/" +str(ident) + "." + ticker, "w") as f:
            f.write(text)
        if link_pdf != "":
            with open(p_athex + "/" +str(ident) + "." + ticker + ".pdf", "wb") as f:
                f.write(requests.get(link_pdf).content)

    print("english done")
    ## gr
    url = "https://www.athexgroup.gr/el/web/guest/rss-feeds/-/asset_publisher/companiesrss/custom-rss"
    feed = feedparser.parse(url)
    # dict_keys(['title', 'title_detail', 'links', 'link', 'authors', 'author_detail', 'author', 'id', 'guidislink', 'updated', 'updated_parsed', 'published', 'published_parsed', 'content', 'summary', 'hlxcd_company-data-language-id', 'hlxcd_company-name', 'hlxcd_company-ticker-symbol', 'hlxcd_helex-company-data'])
    # note: first entries are younger than later ones

    for entry in feed.entries:
        birth = entry.published
        
        if not is_younger(birth, last):
            break

        link = entry.link
        hrefs = extract_hrefs(requests.get(link).text)
        for l in hrefs:
            if l.startswith("/documents"):
                if "Cookies" in l:
                    continue
                link_pdf = "https://www.athexgroup.gr" + l
                break
        else:
            link_pdf = ""

        sum = entry.summary
        ident = link.split("/")[-1]
        title = entry.title
        text = f"{birth}\n{title}\n{link}\n{link_pdf}\n{sum}"
        ticker = entry["hlxcd_company-ticker-symbol"]


        if ticker not in named_tickers_gr:
            name_ticker_map_gr[entry["hlxcd_company-name"]] = ticker


        with open(p_athex + "/" +str(ident) + "." + ticker, "w") as f:
            f.write(text)
        if link_pdf != "":
            with open(p_athex + "/" +str(ident) + "." + ticker + ".pdf", "wb") as f:
                f.write(requests.get(link_pdf).content)



    n = datetime.now(timezone.utc).isoformat()
    with open(p_athex+"/last_entry.txt", "w") as f:
        f.write(n)

    with open("/Users/a2/code/fin/trade/tradx/static/tickers/AT_name_ticker_gr.json", "w") as f:
        json.dump(name_ticker_map_gr, f)

    with open("/Users/a2/code/fin/trade/tradx/static/tickers/AT_name_ticker_en.json", "w") as f:
        json.dump(name_ticker_map_en, f)

if __name__ == "__main__":
    main()
