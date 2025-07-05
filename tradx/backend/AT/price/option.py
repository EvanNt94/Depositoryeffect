import requests
import requests
import brotlicffi
import json
import io

def fetch_options_data_equity(ticker:str):
    url = "https://api.godelterminal.com/api/optionsv2"
    
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "de-DE,de;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://app.godelterminal.com",
        "Referer": "https://app.godelterminal.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15"
    }
    
    data = {
        "underlying": f"EQ:{ticker}",
        "center": 414,
        "number_of_strikes_above": 10,
        "number_of_strikes_below": 10,
        "start_expiry": "2025-02-10T16:55:59.979Z",
        "end_expiry": "2025-09-10T15:55:59.979Z"
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        content_type = response.headers['Content-Type']
        content_encoding = response.headers['Content-Encoding']
        print(f"Content-Type: {content_type}")
        print(f"Content-Encoding: {content_encoding}")

        if content_encoding == 'br':
            compressed_content = response.content
            try:
                decompressed_content = brotlicffi.decompress(compressed_content)
                # Dekodieren der Bytes zu einem String (UTF-8 ist üblich für JSON)
                json_string = decompressed_content.decode('utf-8')
                # Parsen des JSON-Strings
                json_data = json.loads(json_string)
                return json_data # Hier haben Sie Ihr lesbares JSON-Objekt!

            except Exception as e:
                print(f"Fehler bei der Brotli-Dekompression oder JSON-Parsen: {e}")
        else:
            # Wenn keine Brotli-Komprimierung, versuchen Sie response.json() (oder response.text, falls es kein JSON sein sollte)
            try:
                json_data = response.json()
                return json_data
            except json.JSONDecodeError:
                print("Fehler beim Parsen von JSON (ohne Dekomprimierung). Versuchen Sie response.text:")
                print(response.text)
    else:
        response.raise_for_status()

# Beispielnutzung
if __name__ == "__main__":
    TICKER = "MSFT"
    try:
        options_data = fetch_options_data_equity(TICKER)

        
        print(json.dumps(options_data, indent=4) if isinstance(options_data, dict) else options_data)
    except Exception as e:
        print(f"Fehler bei der Anfrage: {e}")
