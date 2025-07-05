"""
wir versuchen das nochmal mit curl_cffi.
unnötig. wir brauchen nur p_p_id. diese ist im javascript. 
mit der definieren wir nun unsere base_url. hehe.
cookies haben wir nun auch.

"""


#%%
### cookie check
import grab_cookies_at
import os, re
import time

# Pfad zur Datei
file_path = '/Users/a2/code/fin/trade/data/session/AT/cookies.json'

# Letzte Schreibzeit ermitteln
last_modified_time = os.path.getmtime(file_path)

# Aktuelle Zeit
current_time = time.time()

# Differenz in Minuten berechnen
time_difference = (current_time - last_modified_time) / 60

if time_difference >= 10: # code beauty
    grab_cookies_at.renew()
    

#%%
import json
with open("/Users/a2/code/fin/trade/data/session/AT/cookies.json", "r") as f:
    cookies = json.load(f)
with open("/Users/a2/code/fin/trade/data/session/AT/p_p_id", "r") as f:
    ppid = f.read()

#%%


year = "2024"
month = "10"
day = "11"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15',
    'Accept': 'text/html, */*',
    'Accept-Language': 'de-DE,de;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'Referer: https://www.athexgroup.gr/el/home',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}


base_url = f"https://www.athexgroup.gr/el/web/guest/home?p_p_auth={ppid}&p_p_id=financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1&p_p_lifecycle=0&p_p_state=exclusive&p_p_mode=view&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_year=2024&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_month=9&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_day=18&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_noAjaxRendering=true"

requests.get(base_url, cookies=cookies, headers=headers).text
# %%
# now we want to make it usable.
import requests
import json, datetime
import os, re
import time
### cookie check
import grab_cookies_at
import os, re
import time
from bs4 import BeautifulSoup


# Pfad zur Datei
file_path = '/Users/a2/code/fin/trade/data/session/AT/cookies.json'

# Letzte Schreibzeit ermitteln
last_modified_time = os.path.getmtime(file_path)

# Aktuelle Zeit
current_time = time.time()

# Differenz in Minuten berechnen
time_difference = (current_time - last_modified_time) / 60

if time_difference >= 10: # code beauty
    grab_cookies_at.renew()


with open("/Users/a2/code/fin/trade/data/session/AT/cookies.json", "r") as f:
    cookies = json.load(f)

with open("/Users/a2/code/fin/trade/data/session/AT/cookies_gr.json", "r") as f:
    cookies_gr = json.load(f)

with open("/Users/a2/code/fin/trade/data/session/AT/p_p_id", "r") as f:
    ppid = f.read()

with open("/Users/a2/code/fin/trade/data/session/AT/p_p_id_gr", "r") as f:
    ppid_gr = f.read()

def extract_events(page, date:datetime.date):
    """
    input: html of calender request
    output:
        list of calender entry dict:
            company_name, date, title, ticker(?)
    
    
    """
    soup = BeautifulSoup(page, "lxml")
    event_divs = soup.select(".calendar-event")
    day  = date.strftime("%d-%m-%Y")
    events = []
    event_dict ={}
    if len(event_divs) == 0:
        return []
    for event in event_divs:
        print(day)
        aa = event.find_all("a")
        event_dict = {}
        for a in aa:
            link = a['href']
            print(a)
            if link.startswith("/company-profile/"):
                event_dict['company_name'] = a.get_text()
            elif link.startswith("/stock-snapshot/"):
                event_dict['ticker'] = a.get_text()
        
        event_dict['title'] = event.select('.calendar-event-title')[0].get_text()
        event_dict['date'] = day
        print(event_dict)
        events.append(event_dict)
    print(events)
    return events


def get_next_events(start:list[int], num_days:int): # start: [day, month, year]
    ### gr 
    with open("/Users/a2/code/fin/trade/data/session/AT/p_p_id_gr", "r") as f:
        ppid_gr = f.read()
    with open("/Users/a2/code/fin/trade/data/session/AT/p_p_id", "r") as f:
        ppid = f.read()

    with open("/Users/a2/code/fin/trade/data/session/AT/cookies.json", "r") as f:
        cookies = json.load(f)

    with open("/Users/a2/code/fin/trade/data/session/AT/cookies_gr.json", "r") as f:
        cookies_gr = json.load(f)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15',
        'Accept': 'text/html, */*',
        'Accept-Language': 'de-DE,de;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.athexgroup.gr/el',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    day, month, year = start
    startdate = datetime.date(year, month, day)
    for n in range(num_days):
        td = datetime.timedelta(n)
        wd = startdate + td
        time.sleep(5)
        day, month, year = wd.day, wd.month-1, wd.year
        base_url = f"https://www.athexgroup.gr/el/web/guest/home?p_p_auth={ppid_gr}&p_p_id=financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1&p_p_lifecycle=0&p_p_state=exclusive&p_p_mode=view&controlPanelCategory=portlet_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_q=dailyEvents&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_year={year}&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_month={month}&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_day={day}&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_noAjaxRendering=true"
        response = requests.get(base_url, cookies=cookies_gr, headers=headers).text
        print(response)
        events = extract_events(response, wd)
        time.sleep(1)
        with open("/Users/a2/code/fin/trade/data/calendar/AT/"+ wd.strftime("%d-%m-%Y")+"-gr", "w") as f:
            json.dump(events, f)

    ### en
    headers['Referer'] = "https://www.athexgroup.gr/web/guest/home"
    for n in range(num_days):
        td = datetime.timedelta(n)
        wd = startdate + td
        time.sleep(5)
        day, month, year = wd.day, wd.month-1, wd.year

        base_url_en = f"https://www.athexgroup.gr/web/guest/home?p_p_auth={ppid}&p_p_id=financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1&p_p_lifecycle=0&p_p_state=exclusive&p_p_mode=view&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_q=dailyEvents&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_year={year}&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_month={month}&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_day={day}&_financialcalendarportlet_WAR_HelexServiceportlet_INSTANCE_rcc1_noAjaxRendering=true"
        
        response_en = requests.get(base_url_en, cookies=cookies, headers=headers).text
        print(response_en)
        events_en = extract_events(response_en, wd)
        with open("/Users/a2/code/fin/trade/data/calendar/AT/"+ wd.strftime("%d-%m-%Y"), "w") as f:
            json.dump(events_en, f)
        print()
        print()
        print()
# %%
today = datetime.datetime.now()
date_arr = [today.day, today.month, today.year]
get_next_events(date_arr, 7)
# %%
