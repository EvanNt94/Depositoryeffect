import requests, time

def fetch_feed_with_conditional_get(url, etag=None, last_modified=None):
    headers = {}
    if etag:
        headers['If-None-Match'] = etag
    if last_modified:
        headers['If-Modified-Since'] = last_modified

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Inhalt wurde geändert, aktualisiere ETag und Last-Modified
        etag = response.headers.get('ETag')
        last_modified = response.headers.get('Last-Modified')
        return response.text, etag, last_modified
    elif response.status_code == 304:
        # Keine Änderungen
        return None, etag, last_modified
    else:
        # Fehlerbehandlung für andere Statuscodes
        response.raise_for_status()

# Beispielaufruf:
import requests

url = "https://www.athexgroup.gr/web/guest/rss-feeds/-/asset_publisher/companiesrss/custom-rss"
response = requests.head(url)

print("Headers:", response.headers)