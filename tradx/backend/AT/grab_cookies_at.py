from selenium import webdriver
import json, re


def renew_gr():
    driver = webdriver.Safari()
    driver.maximize_window()
    driver.get("https://www.athexgroup.gr/el/web/guest/home")

    # they give too many params. we just need a simple dict.
    cc = driver.get_cookies()

    folder_to_save = "/Users/a2/code/fin/trade/data/session/AT"

    cookies = {}

    for cookie in cc:  
        cookies[cookie["name"]] = cookie["value"]

    with open(folder_to_save+ "/cookies_gr.json", "w") as f:
        json.dump(cookies, f)

    # p-p-id
    pattern = r"web/guest/home\?p_p_auth=([^&]+)&"
    match = re.search(pattern, driver.page_source)
    if match:
        ppid = match.group(1)
        open("/Users/a2/code/fin/trade/data/session/AT/p_p_id_gr", "w").write(ppid)
    else:
        print("no_match for p-p–id")

    driver.close()



def renew_en():
    driver = webdriver.Safari()
    driver.maximize_window()
    driver.get("https://www.athexgroup.gr/web/guest/companies-information-corporate-actions")

    # they give too many params. we just need a simple dict.
    cc = driver.get_cookies()

    folder_to_save = "/Users/a2/code/fin/trade/data/session/AT"

    cookies = {}

    for cookie in cc:  
        cookies[cookie["name"]] = cookie["value"]

    with open(folder_to_save+ "/cookies.json", "w") as f:
        json.dump(cookies, f)

    # p-p-id
    pattern = r"web/guest/home\?p_p_auth=([^&]+)&"
    match = re.search(pattern, driver.page_source)
    if match:
        ppid = match.group(1)
        open("/Users/a2/code/fin/trade/data/session/AT/p_p_id", "w").write(ppid)
    else:
        print("no_match for p-p–id")

    driver.close()

def renew():
    renew_gr()
    renew_en()
    

if __name__ == "__main__":
    renew()