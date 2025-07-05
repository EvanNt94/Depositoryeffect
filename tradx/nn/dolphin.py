# Load model directly
from transformers import AutoTokenizer, AutoModelForImageTextToText

tokenizer = AutoTokenizer.from_pretrained("ByteDance/Dolphin")
model = AutoModelForImageTextToText.from_pretrained("ByteDance/Dolphin")
