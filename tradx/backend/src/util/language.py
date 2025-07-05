from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  # deterministic results

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "unknown"