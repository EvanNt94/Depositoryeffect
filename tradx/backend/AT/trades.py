from tradx.backend.util.tables import *
from datetime import datetime
import re, os
import tradx

def save_block_trades_at():
    base_url = "https://www.athexgroup.gr/en/market-data/data-services/market-activity-blocks-trades"
    soup, dfs = request_soup_with_dfs(base_url)
    h2s = soup.find_all("h2")
    pattern = re.compile(r"(\d{4}\.\d{2}\.\d{2})\s+Stocks")
    matches = [h2 for h2 in h2s if pattern.fullmatch(h2.get_text(strip=True))]
    if len(matches) == 1:
        text = matches[0].get_text(strip=True)
        date_str = pattern.fullmatch(text).group(1)
        date = datetime.strptime(date_str, "%Y.%m.%d")
    dfs = dfs[0]
    df = dfs.drop(columns=(["Company"]+list(dfs.columns[dfs.columns.str.contains(r"^Unnamed")])))
    df.to_csv(os.path.join(tradx.TRADX_BASE, "data", "trades", "AT", date.date().isoformat()+".csv"))