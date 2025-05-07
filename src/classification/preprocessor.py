import re
from unidecode import unidecode

def preprocess_text(text):
    text = text.lower()
    text = unidecode(text)
    text = re.sub(r"\s+", " ", text.strip())
    return text.split(" ")
