import asyncio
import feedparser
from feedparser import parse
from tradx.backend.src.worker.db.SourcesDBHandler import get_rss_sources_full

rss_entry_cols = ["id", "feed", "title", "link", "summary", "date", "company", "ticker", "isin", "language", "attachment_url", "pdf_path", "last_updated", "summary_tsv"]
idioms = ["title", "link", "summary", "date", "language", ]

def get_value_deep(d, key):
    if isinstance(d, dict):
        if key in d:
            return d[key]
        for v in d.values():
            result = get_value_deep(v, key)
            if result is not None:
                return result
    elif isinstance(d, list):
        for i in d:
            result = get_value_deep(i, key)
            if result is not None:
                return result
    return None


async def main():
    feeds = get_rss_sources_full()
    for feed in feeds:
        parsed_feed = parse(feed["url"])
        if parsed_feed["status"] != 200:
            print("something went wrong. status: "+ parsed_feed["status"])
        if parsed_feed.bozo:
            print("error at parsing "+ feed["url"])
        for entry in parsed_feed["entries"]:
            entry_dict = {
                "feed": feed["url"],
                
            }
            
            entries = [
                {
                    "id": "entry-1",
                    "feed": "athex",
                    "title": "Title",
                    "link": "http://example.com",
                    "summary": "Some summary",
                    "date": "2025-06-22T13:00:00Z",
                    "company": "SomeCo",
                    "ticker": "SC",
                    "isin": "GR0000000001",
                    "language": "en",
                    "attachment_url": None,
                    "pdf_path": None,
                    "last_updated": "2025-06-22T13:10:00Z",
                },
            ]

    await insert_rss_entries(pool, entries)

if __name__ == "__main__":
    asyncio.run(main())
