from multiprocessing import Queue
import os
import json
import feedparser
import time
import tradx
import re
from tradx.backend.util.html_util import *
from tradx.backend.src.worker.db.StockExchangeDBWorker import StockExchangeDBWorker as SXW
from tradx.backend.src.worker.db.RSSFeedDBWorker import RSSFeedDBWorker as RSSDB
import requests
from datetime import datetime


FEEDS_FILE = os.path.join(tradx.TRADX_BASE, "data", "static", "feeds", "AT", "feed_links.json")
CHECKPOINTS_FILE = os.path.join(tradx.TRADX_BASE, "data", "checkpoints", "AT", "rss", "checkpoints.json")

def save_attachement(url, path):
    print(url)
    resp = requests.get(url)
    with open(path, "wb") as f:
        f.write(resp.content)


def get_id(entry):
    raw_id = entry.get("id", "")
    match = re.search(r"\b(\d+)\b", raw_id)
    if match:
        return int(match.group(1))
    return -1  # fallback für ungültige IDs

def load_feed_links():
    with open(FEEDS_FILE, "r") as f:
        return json.load(f)

def fetch_and_parse_feed(url: str):
    feed = feedparser.parse(url)
    if feed.bozo:
        print(f"[WARN] Fehler beim Parsen von Feed: {url}")
    return feed

def load_checkpoints():
    with open(CHECKPOINTS_FILE, "r") as f:
        return json.load(f)

def save_checkpoints(checkpoints):
    with open(CHECKPOINTS_FILE, "w") as f:
        json.dump(checkpoints, f)

def get_language_of_link(url: str) -> str:
    if "/el/" in url:
        return "Greek"
    elif "/en/" in url:
        return "English"
    return "unknown"

def process_feed(name: str, url: str, last:int, sx_worker:SXW, rssdb:RSSDB, debug=False):
    if debug: 
        print(f"\n== {name.upper()} ==")
    directory = os.path.join(tradx.TRADX_BASE, "data", "static", "feeds", "AT", "pdfs", name)
    os.makedirs(directory, exist_ok=True)
    feed = fetch_and_parse_feed(url)
    max_id = 0
    for entry in feed.entries: 
        dd = {}
        dd["id"] = get_id(entry)
        if dd["id"] > max_id:
            max_id = dd["id"]
        if dd["id"] <= last:
            return last
        time.sleep(1)
        
        dd["feed"] = "AT_" + name
        dd["title"] = entry.get("title", "No Title")
        dd["link"] = extract_attachment_url(entry.get("link", ""))
        dd["summary"] = extract_text_from_html(entry.get("summary", "No Summary"))
        dd["date"] = entry.get("published", "No Date")
        dd["company"] = entry.get("hlxcd_company-name", "No Company")
        dd["ticker"] = entry.get("hlxcd_company-ticker-symbol", "No Ticker")
        if dd["ticker"] != "No Ticker":
            if get_language_of_link(url=url) == "Greek" and dd["ticker"] != "":
                try:
                    dd["ticker"] = sx_worker.get_intl_ticker_from_local("AT", dd["ticker"])[0]
                except:
                    print("[WARN]: stock not found in db: "+ entry.get("hlxcd_company-ticker-symbol", "No Ticker"))
                    continue
            else:
                dd["ticker"]  = dd["ticker"]+".AT"
        isin_list = sx_worker.get_isin_from_ticker("AT", dd["ticker"])
        dd["isin"] = isin_list[0] if isin_list else "unknown"
        dd["language"] = get_language_of_link(dd["link"])
        dd["attachment_url"] = extract_attachment_url(entry.get("attachment", ""))
        # PDF-Verzeichnis anlegen, bevor auf attachment geprüft wird
        if dd["attachment_url"] == "":
            dd["attachment_url"] = dd["link"]
        dd["pdf_path"] = os.path.join(directory, str(dd["id"])+".pdf")
        save_attachement(dd["attachment_url"], dd["pdf_path"])
        dd["last_updated"] = datetime.now().isoformat()
        if debug:
            print(dd)
        rssdb.queue.put({
            "type": "insert_rss",
            "payload": dd
        })
    return max_id


def main(debug=False, rss_db=None):
    if rss_db is None:
        raise RuntimeError("only start with DB worker")
    sx_worker = SXW()
    feed_dict = load_feed_links()
    checkpoints = load_checkpoints()
    for name, url in feed_dict.items():
        time.sleep(1)
        new_max =  process_feed(name, url, checkpoints[name], sx_worker=sx_worker, rssdb=rss_db, debug=debug)
        checkpoints[name] = new_max
        save_checkpoints(checkpoints)
    rss_db.queue.put(None)

if __name__ == "__main__":
    queue = Queue()
    rss_db = RSSDB(queue=queue)
    rss_db.start()
    main(debug=True, rss_db=rss_db)