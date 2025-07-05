import requests, re, time, os, json
import multiprocessing as mp
from urllib.parse import urlparse
import validators


def _eval_resp(resp:requests.Response):
    headers = resp.headers
    pattern = r"^([a-z]+)/([a-z]+)"
    try:
        m = re.match(pattern,headers['Content-Type'])
    except KeyError:
        return None, None
    typ = m.group(1)
    filetype = m.group(2)
    return typ, filetype


def extract_all_links(page_source):
    # Regex zum Extrahieren von href-Werten
    href_pattern = r'href=["\'](.*?)["\']'
    # Alle Übereinstimmungen finden
    hrefs = re.findall(href_pattern, page_source)
    return hrefs

def gehört_url_zu_hauptdomain(url, hauptdomain):
    parsed_url = urlparse(url)
    # Überprüfe, ob die Hauptdomain am Ende des Hostnamens steht
    netloc = parsed_url.netloc
    parts = netloc.split(".")
    tl_domain = parts[-1]
    sl_domain = parts[-2]
    return hauptdomain == sl_domain



def list_all_public_links(base_url:str)->tuple[dict[str, list[str]]]:
    root_domain = urlparse(base_url).netloc.split(".")[-2]
    res_d = {"text/html": [base_url]}
    visited_set = {base_url}
    referrer_dict = {base_url: None}
    links = extract_all_links(requests.get(base_url).text)
    queue_set = set(links)
    for link in links:
        referrer_dict[link] = [base_url]
    while queue_set:
        current_elem = queue_set.pop()
        if current_elem.startswith("mailto:"):
            continue
        if not current_elem.startswith("https://"):
            if current_elem.startswith("/"):
                current_elem = base_url+current_elem
            else:
                current_elem = base_url+"/"+current_elem

        pattern = r'^(https?:\/\/.*?)(?=(https?:\/\/|$))'
        current_elem = re.match(pattern, current_elem).group(1)
        
        time.sleep(5)
        print(current_elem)
        print(f"Besuche: {current_elem}")
        try:
            resp = requests.get(current_elem)
        except Exception as e:
            print(f"Fehler beim Abrufen von {current_elem}: {e}")
            continue

        visited_set.add(current_elem)
        keys = res_d.keys()
        tf = _eval_resp(resp)
        content = "/".join(tf)
        if content not in keys:
            res_d[content] = []
        res_d[content].append(current_elem)
        if tf != ("text", "html"):
            continue
        if not gehört_url_zu_hauptdomain(current_elem, root_domain):
            continue
        new_links = set(extract_all_links(resp.text))
        links_not_visited = new_links - visited_set
        for link in links_not_visited:
            if link in referrer_dict:
                referrer_dict[link].append(current_elem)
            else:
                referrer_dict[link] = [current_elem]

        queue_set.update(links_not_visited)
    return res_d, referrer_dict

        

def worker(param):
    result = list_all_public_links(param)
    return result



def parallel_process(params, num_processes=None):
    if num_processes is None:
        # Setze die Prozessanzahl auf das Doppelte der CPU-Kerne für höheren Durchsatz
        num_processes = mp.cpu_count() * 2
    with mp.Pool(processes=mp.cpu_count()) as pool:
        for result in pool.imap(worker, params):
            yield result




if __name__ == "__main__":

    # add zu params auch eine ticker um die webseite zum ticker zu matchen! (save...)
    params = []
    with open("/Users/a2/code/fin/trade/static/tickers/AT_shitticker.json", "r") as f:
        sh = json.load(f)
    p = "/Users/a2/code/fin/trade/data/fundamentals/company/info"
    files = os.listdir(p)
    for f in files:
        tt = f.replace(".json", ".AT")
        if tt in sh:
            continue # shittickers - should stay
        # load info
        with open(os.path.join(p,f), "r") as fp:
            temp = json.load(fp)

        wp = temp["webpage"].strip() # to be sure
        wp = wp.lower() # to be sure

        if not wp.startswith("http"):
            wp = "http://" + wp

        if wp!= temp["webpage"]:
            print("webpage: ", wp, f)
            temp["webpage"] = wp
            with open(os.path.join(p,f), "w") as fp:
                json.dump(temp, fp)

        if wp == "":
            print(f)
            raise RuntimeError
    
    
        
        if "@" in wp:
            wp = wp.split("@")[-1]
            wp = "http://www." + wp
        
        if not validators.url(wp):
            print(wp, f)
            raise RuntimeError
        params.append(wp)

    
    for res in parallel_process(params):

        print(res)