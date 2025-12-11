import re

def clean_text(text):
    # Remove HTML tags only, keep punctuation for LLM
    text = re.sub(r'<[^>]*>', ' ', text)
    # Collapse extra spaces
    text = ' '.join(text.split())
    return text
