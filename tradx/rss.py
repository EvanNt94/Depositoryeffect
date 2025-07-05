#%%
import feedparser

#%%
x = "https://api.boerse-frankfurt.de/v1/feeds/news.rss"
NewsFeed = feedparser.parse(x)
entry = NewsFeed.entries[0]

# %%
import json
with open("js.json", "w") as f:
    json.dump(entry, f)

# %%
