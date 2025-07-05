# %% # nicht was ich suche aber useful AF
import requests
requests.get("https://www.athexgroup.gr")
from bs4 import BeautifulSoup
url = 'https://www.athexgroup.gr/web/guest/financial-statements-in-pdf-format'

params = {
    'p_p_id': '101_INSTANCE_rszQq5Xl8b45',
    'p_p_lifecycle': '0',
    'p_p_state': 'exclusive',
    'p_p_mode': 'view',
    'p_p_col_id': 'column-1',
    'p_p_col_pos': '4',
    'p_p_col_count': '5',
    '_101_INSTANCE_rszQq5Xl8b45_noAjaxRendering': 'https://www.athexgroup.gr/web/guest/financial-statements-in-pdf-format',
}

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'de-DE,de;q=0.9',
    'Referer': 'https://www.athexgroup.gr/web/guest/financial-statements-in-pdf-format',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, wie Gecko) Version/18.0 Safari/605.1.15',
    'X-Requested-With': 'XMLHttpRequest',
}

cookies = {
    'GUEST_LANGUAGE_ID': 'en_US',
    'COOKIE_SUPPORT': 'true',
}

resp2 = requests.get(url,params=params, cookies=cookies, headers=headers)
soup = BeautifulSoup(resp2.text, "lxml")
aa = soup.find_all("a")[:-1]
# %%
#### check for next page!!
### greek and english are different

### we need company name -> ticker english and greek.

# todo Ημερολόγιο



#%% selenium try
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time, pandas as pd

driver = webdriver.Safari()
driver.maximize_window()
driver.get("https://www.athexgroup.gr")
driver.get('https://www.athexgroup.gr/web/guest/financial-statements-in-pdf-format')

cc = driver.get_cookies()

for cookie in cc:  
    cookies[cookie["name"]] = cookie["value"]



resp2 = requests.get(url,params=params, cookies=cookies, headers=headers)
soup = BeautifulSoup(resp2.text, "lxml")
aa = soup.find_all("a")[:-1]
aa
# %%
import re
for a in aa:
    page = a.get("href")
    ## timer
    idnet = re.findall(r'id/(\d+)\?', page)[0]
    driver.get(page)
    s2 = BeautifulSoup(driver.page_source, "lxml")
    a = None
    while a is None:
        s2 = BeautifulSoup(driver.page_source, "lxml")
        a = driver.execute_script('return document.querySelector("#portlet_101_INSTANCE_rszQq5Xl8b45 > div > div > div > div > div.asset-full-content.show-asset-title > div.asset-content > div.asset-resource-info > a")')
    link=a.get_attribute("href")
    title=a.text
    pattern = r"([A-Z_\s\.]+) \("
    match = re.search(pattern, title)
    if match:
        comp_name = match.group(1).strip()  # Die gefundene Gruppe ist der Firmenname
        print("Company Name:", comp_name)
    else:
        print("Kein Firmenname gefunden", title)
        comp_name = ""
    with open("/Users/a2/code/fin/trade/data/fundamentals/company/fin_st/AT/sort/"+ comp_name+":"+ idnet + ".pdf", 'wb') as f:
        f.write(requests.get(link).content) # wir fügen noch ticker hinzu und Qs


# %%
title
#%%
driver.close()
# %%
requests.get("https://www.athexgroup.gr/el/financial-statements-in-pdf-format/-/asset_publisher/rszQq5Xl8b45/document/id/7563672?controlPanelCategory=portlet_101_INSTANCE_rszQq5Xl8b45&amp;redirect=https%3A%2F%2Fwww.athexgroup.gr%2Fweb%2Fguest%2Ffinancial-statements-in-pdf-format%3Fp_p_id%3D101_INSTANCE_rszQq5Xl8b45%26p_p_lifecycle%3D0%26p_p_state%3Dnormal%26p_p_mode%3Dview%26controlPanelCategory%3Dportlet_101_INSTANCE_rszQq5Xl8b45%26_101_INSTANCE_rszQq5Xl8b45_").text
# %%
