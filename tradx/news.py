"""
Our newspaper3k library extracts a lot of things but its a wrapper for apis.
We need store.
"""
import json

class Article:
    def __init__(self, source:str, url:str, date:str, authors:list[str], title:str, text:str, keyowrds:list[str], summary:str):
        self.source = source.strip() # just to be sure
        self.url = url.strip()
        self.date = date.strip()
        self.authors = json.dumps([a.strip() for a in authors])
        self.title = title.strip()
        self.text = text
        self.keywords = json.dumps([k.strip() for k in keyowrds])
        self.summary = summary.strip()



    def get_article(self)-> str:
        return "\n".join([self.source, self.url, self.date, self.authors, self.title, self.text])

    def get_nlp(self)-> str:
        return "\n".join([self.keywords, self.summary])