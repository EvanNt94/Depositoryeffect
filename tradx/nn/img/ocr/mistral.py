import os
import requests
from dotenv import load_dotenv

# .env Datei laden
load_dotenv()

def mistral_ocr(file_path):
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("Fehler: MISTRAL_API_KEY nicht gesetzt!")
        return

    url = "https://api.mistral.ai/v1/ocr"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    with open(file_path, "rb") as file:
        files = {
            "file": (os.path.basename(file_path), file, "application/pdf")
        }
        data = {
            "model": "pixtral-12b-2409"  # Spezifiziert das OCR-Modell
        }
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        result = response.json()
        print("Erkannter Text:")
        for page in result.get('pages', []):
            print(page.get('text', ''))
    else:
        print(f"Fehler {response.status_code}: {response.text}")

if __name__ == "__main__":
    FILE_PATH = "/Users/a2/Downloads/blatt08_lsg.pdf"  # Passe den Pfad zur Datei an
    mistral_ocr(FILE_PATH)
