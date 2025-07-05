import os

def add_rss_feed_from_txt(path:str):
    with open(path) as f:
        urls = f.read().split("\n")
    