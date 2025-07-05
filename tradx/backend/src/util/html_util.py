from html import unescape
from xml.etree import ElementTree
import re
import html
from bs4 import BeautifulSoup


def extract_text_from_html_bs4(html_str: str) -> str:
    """
    Extracts visible, non-redundant text content from HTML using BeautifulSoup.
    Handles malformed HTML more robustly than ElementTree.
    """
    print("NORMAL DID NOT WORK")
    print("NORMAL DID NOT WORK")
    print("NORMAL DID NOT WORK")
    print("NORMAL DID NOT WORK")
    print("NORMAL DID NOT WORK")
    print("NORMAL DID NOT WORK")
    print("NORMAL DID NOT WORK")
    if not html_str:
        return ""
    soup = BeautifulSoup(html_str, "html.parser")
    texts = [t.strip() for t in soup.stripped_strings]
    seen = set()
    unique = []
    for t in texts:
        if t not in seen:
            unique.append(t)
            seen.add(t)
    return "\n".join(unique)



def extract_text_from_html(html_str: str) -> str:
    """
    Extrahiert reinen Text aus einem HTML-String.
    Entfernt alle Tags und gibt nur den sichtbaren Text zurück.
    """
    if not html_str:
        return ""
    try:
        unescaped = unescape(html_str)
        wrapped = f"<root>{unescaped}</root>"
        root = ElementTree.fromstring(wrapped)
        texts = [t.strip() for t in root.itertext()]
        cleaned = []
        for t in texts:
            if not any(t in c or c in t for c in cleaned):
                cleaned.append(t)
        text = "\n".join(cleaned)
        if "<" in text and ">" in text:
            return extract_text_from_html_bs4(text)
        return text
    except Exception:
        return unescape(html_str)
    

def extract_attachment_url(attachment_html: str) -> str:
    """
    Extrahiert die wahrscheinlichste URL aus einem HTML-Attachment-String.
    1. Sucht nach der ersten URL hinter 'href' (egal wie kaputt das Attribut ist).
    2. Fällt zurück auf den längsten http(s)-Link im String.
    3. Repariert auf 'https://' falls nach dem Protokoll nur ein Slash steht.
    """
    if not attachment_html:
        return ""
    s = html.unescape(attachment_html)
    # Schritt 1: Suche nach href gefolgt von URL (egal wie kaputt)
    match = re.search(r'href[=:"\']*\s*(https?:/?/?[^\s"\'<>]+)', s)
    if match:
        url = match.group(1)
    else:
        # Schritt 2: Fallback – finde alle http(s)-Links
        candidates = re.findall(r'https?:/?/?[^\s"\'<>]+', s)
        if not candidates:
            return ""
        url = max(candidates, key=len)
    # Schritt 3: Repariere auf https://, falls nur ein Slash
    url = re.sub(r'^(https?:)/([^/])', r'\1//\2', url)
    return url


if __name__ == "__main__":
    t1 = '<span>ΠΡΟΣΚΛΗΣΗ ΣΕ ΠΑΡΟΥΣΙΑΣΗ ΟΙΚΟΝΟΜΙΚΩΝ ΑΠΟΤΕΛΕΣΜΑΤΩΝ</span>\n<ul class="links inline"><li><a href="https://www.athexgroup.gr/el/node/954384" hreflang="el" rel="tag" target="_blank" title="ΠΡΟΣΚΛΗΣΗ ΣΕ ΠΑΡΟΥΣΙΑΣΗ ΟΙΚΟΝΟΜΙΚΩΝ ΑΠΟΤΕΛΕΣΜΑΤΩΝ">Διαβάστε περισσότερα<span class="visually-hidden"> για το ΠΡΟΣΚΛΗΣΗ ΣΕ ΠΑΡΟΥΣΙΑΣΗ ΟΙΚΟΝΟΜΙΚΩΝ ΑΠΟΤΕΛΕΣΜΑΤΩΝ</span></a></li></ul>\n            <div><p>ΠΡΟΣΚΛΗΣΗ ΣΕ ΠΑΡΟΥΣΙΑΣΗ ΟΙΚΟΝΟΜΙΚΩΝ ΑΠΟΤΕΛΕΣΜΑΤΩΝ</p><br /></div>'
    t2 =  'https://www.athexgroup.gr/&lta&gt href&quothttps:/www.athexgroup.gr/en/more-options/announcements/invitation-financial-results-presentation-0&quot target=&quot_blank&quot&gt&lt/a&gt'
    t3 = """<p class="text-align-right">28.05.2025</p><p class="text-align-justify">\xa0</p><p class="text-align-justify">The <strong>Athens Exchange Group</strong> and <strong>FTSE Russell</strong> announces the results of the regular semi-annual review of the composition of the FTSE/ATHEX Index Series for the period November 2024 – April 2025.\xa0</p><p class="text-align-justify"><br />In summary, the following changes will be implemented in the index compositions:<br />\xa0</p><ul><li><p class="text-align-justify"><strong>FTSE/ATHEX Large Index</strong><br />One (1) addition, one (1) deletion, and two (2) changes to the free float adjustment factors. A total of twenty five (25) stocks will be included in the index.\xa0<br />\xa0</p></li><li><p class="text-align-justify"><strong>FTSE/ATHEX Mid Cap Index\xa0</strong><br />Two (2) additions, two (2) deletions, and two (2) changes to the free float adjustment factors. A total of twenty (20) stocks will be included in the index.\xa0<br />\xa0</p></li><li><p class="text-align-justify"><strong>FTSE/ATHEX Market Index</strong><br />Five (5) additions, seven (7) deletions, and twelve (12) changes to the free float adjustment factors. A total of eighty three (83) stocks will be included in the index.<br />\xa0</p></li><li><p class="text-align-justify"><strong>FTSE/ATHEX High Dividend Yield Index\xa0</strong><br />No (0) additions, no (0) deletions and no (0) changes to the free float adjustment factors. A total of twenty five (25) stocks will be included in the index.\xa0<br />\xa0</p><p class="text-align-justify"><strong>FTSE/ATHEX Sector Indices:</strong><br />\xa0</p></li><li><p class="text-align-justify">FTSE/ATHEX Banks<br />One (1) addition, no (0) deletions, and one (1) change to the free float adjustment factors. A total of six (6) stocks will be included in the index.<br />\xa0</p></li><li><p class="text-align-justify">FTSE/ATHEX Financial Services<br />One (1) addition, one (1) deletion, and two (2) changes to the free float adjustment factors. A total of nine (9) stocks will be included in the index.<br />\xa0</p></li><li><p class="text-align-justify">FTSE/ATHEX Real Estate<br />One (1) addition, no (0) deletions, and two (2) changes to the free float adjustment factors. A total of nine (9) stocks will be included in the index.<br />\xa0</p></li><li><p class="text-align-justify">FTSE/ATHEX Consumer Discretionary<br />Two (2) additions, no (0) deletions, and one (1) change to the free float adjustment factors. A total of fifteen (15) stocks will be included in the index.</p><p class="text-align-justify">\xa0</p></li><li><p class="text-align-justify">FTSE/ATHEX Consumer Staples<br />One (1) addition, no (0) deletions, and three (3) changes to the free float adjustment factors. A total of seven (7) stocks will be included in the index.<br />\xa0</p></li><li><p class="text-align-justify">FTSE/ATHEX Industrials<br />Two (2) additions, one (1) deletion, and four (4) changes to the free float adjustment factors. A total of twenty three (23) stocks will be included in the index.<br />\xa0</p></li><li><p class="text-align-justify">FTSE/ATHEX Basic Materials<br />No (0) additions, two (2) deletions, and no (0) changes to the free float adjustment factors. A total of six (6) stocks will be included in the index.<br />\xa0</p></li><li><p class="text-align-justify">FTSE/ATHEX Energy & Utilities<br />No (0) additions, one (1) deletion, and no (0) changes to the free float adjustment factors. A total of eight (8) stocks will be included in the index.<br />\xa0</p></li><li><p class="text-align-justify">FTSE/ATHEX Technology & Telecommunications<br />No (0) additions, no (0) deletions, and one (1) change to the free float adjustment factors. A total of twelve (12) stocks will be included in the index.<br />\xa0</p></li></ul><p>The capping factors of the stocks included in the indices will be calculated based on the closing prices of the trading session on Friday, June 13, 2025.</p><p><br />All changes will take effect as of the trading session on <strong>Monday, June 23, 2025</strong>.<br />\xa0</p><p>Please refer to the <strong>attached file</strong> for a detailed list of changes.<br />\xa0</p>"""
    print(extract_attachment_url(t2))
    print(extract_text_from_html(t3))
    # print(extract_attachment_url(t1))
    # print(extract_text_from_html(t1))

